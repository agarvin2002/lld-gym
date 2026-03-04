# Rate Limiter — Design Document

## Class Diagram

```
         <<ABC>>
        RateLimiter
       +is_allowed(client_id: str) -> bool   (abstract)
              |
     _________|_________________________________
    |                   |                      |
TokenBucketLimiter  FixedWindowLimiter  SlidingWindowLimiter
- _capacity: int    - _max_requests:int  - _max_requests: int
- _refill_rate:float- _window: float     - _window: float
- _clock: callable  - _clock: callable   - _clock: callable
- _buckets: dict    - _counts: dict      - _logs: dict[str,deque]
- _last_refill:dict - _window_start:dict - _lock: Lock
- _lock: Lock       - _lock: Lock
+ is_allowed()      + is_allowed()       + is_allowed()


     RateLimiterService
     - _limiters: list[RateLimiter]
     + add_limiter(limiter: RateLimiter) -> None
     + check(client_id: str) -> bool
```

## Algorithm Deep Dives

### Token Bucket

```
  State per client:
    tokens        (float, 0 <= tokens <= capacity)
    last_refill   (float, unix timestamp)

  On is_allowed(client_id):
    1. elapsed = now - last_refill
    2. tokens  = min(capacity, tokens + elapsed * refill_rate)
    3. last_refill = now
    4. if tokens >= 1:
           tokens -= 1; return True
       else:
           return False
```

**Burst behaviour**: a client that has been idle accumulates up to `capacity` tokens and can then fire `capacity` requests instantaneously. After that, requests arrive at no more than `refill_rate` per second.

**Memory**: O(C) per client, where C is the number of distinct clients. Only two floats stored per client.

---

### Fixed Window Counter

```
  State per client:
    count         (int)
    window_start  (float, unix timestamp)

  On is_allowed(client_id):
    1. if now - window_start >= window_seconds:
           count = 0; window_start = now
    2. if count < max_requests:
           count += 1; return True
       else:
           return False
```

**Boundary burst problem**: if a client sends `max_requests` requests just before a window ends, and then another `max_requests` at the start of the next window, they effectively send `2 × max_requests` in a period shorter than `window_seconds`.

**Memory**: O(C) per client. Only two values stored per client.

---

### Sliding Window Log

```
  State per client:
    log  (deque of float timestamps, monotonically increasing)

  On is_allowed(client_id):
    1. cutoff = now - window_seconds
    2. while log and log[0] <= cutoff:
           log.popleft()       # evict expired entries
    3. if len(log) < max_requests:
           log.append(now); return True
       else:
           return False
```

**No boundary burst**: the window is always anchored to the current time, so at any instant the log contains at most `max_requests` entries within the last `window_seconds`.

**Memory**: O(max_requests) per client — the log can never grow beyond `max_requests` entries because entries beyond that are rejected.

---

### RateLimiterService (Composite / Chain-of-Responsibility)

Holds an ordered list of `RateLimiter` instances. `check()` calls `is_allowed()` on **every** limiter (not short-circuiting) because each call has the side-effect of consuming state. Returns `True` only if all limiters returned `True`.

```
  check(client_id):
    results = [limiter.is_allowed(client_id) for limiter in _limiters]
    return all(results)
```

This allows composing, for example, a global rate limit (shared TokenBucket) with a per-user rate limit (FixedWindow), both enforced simultaneously.

---

## Algorithm Trade-offs

| Property | Token Bucket | Fixed Window | Sliding Window Log |
|---|---|---|---|
| Burst handling | Controlled (up to capacity) | Poor (2x at boundary) | Precise |
| Memory per client | O(1) | O(1) | O(max_requests) |
| Computation per request | O(1) | O(1) | O(requests in window) amortised O(1) |
| Accuracy | High | Moderate | Highest |
| Typical use case | APIs allowing bursts | Simple quotas | Strict per-window limits |

---

## Thread Safety

Each limiter instance owns a single `threading.Lock`. The entire read-modify-write sequence inside `is_allowed()` executes under this lock, preventing race conditions when multiple threads call `is_allowed()` concurrently for the same or different client IDs.

Using one lock per instance (rather than one lock per client) keeps the implementation simple and avoids deadlocks from lock ordering. For very high concurrency with many clients, a per-client lock or a lock-striping scheme could reduce contention, but that optimisation is outside the scope of this exercise.

---

## Clock Injection for Testability

Passing `clock=time.time` as a default argument and accepting a custom callable allows tests to control time precisely:

```python
t = [0.0]
clock = lambda: t[0]
limiter = TokenBucketLimiter(capacity=3, refill_rate=1.0, clock=clock)

# consume all tokens
for _ in range(3):
    limiter.is_allowed("u1")

# advance time by 2 seconds → 2 tokens refilled
t[0] = 2.0
assert limiter.is_allowed("u1")   # deterministic, no real sleep needed
```

This pattern avoids flaky tests that depend on `time.sleep()` and makes the test suite run in milliseconds.
