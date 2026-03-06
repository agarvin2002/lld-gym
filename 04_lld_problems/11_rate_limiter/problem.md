# Problem 11: Rate Limiter

## Problem Statement

Implement a rate limiter that controls how many requests a client can make within a time window. Support multiple rate-limiting algorithms so that the strategy can be swapped or combined.

## Requirements

### Core Algorithms

**Token Bucket**
- Each client gets a bucket that starts with `capacity` tokens.
- Tokens refill at `refill_rate` tokens per second (fractional tokens accumulate).
- Each request consumes 1 token.
- If no token is available the request is rejected.
- The bucket never exceeds `capacity` tokens.

**Fixed Window**
- Allow at most `max_requests` requests per fixed time window of `window_seconds`.
- The counter resets to 0 when the current window expires.
- Simple and low-overhead but can allow up to 2x `max_requests` at a window boundary.

**Sliding Window Log**
- Keep a timestamped log of every accepted request per client.
- On each new request, evict all log entries older than `window_seconds`.
- If the remaining log count is less than `max_requests`, allow the request and append the timestamp.
- Most accurate algorithm; memory is O(max_requests) per client.

### Classes to Implement

| Class | Description |
|---|---|
| `RateLimiter` | Abstract base class. Defines `is_allowed(client_id: str) -> bool`. |
| `TokenBucketLimiter(capacity, refill_rate, clock=None)` | Token bucket strategy. |
| `FixedWindowLimiter(max_requests, window_seconds, clock=None)` | Fixed window counter strategy. |
| `SlidingWindowLimiter(max_requests, window_seconds, clock=None)` | Sliding window log strategy. |
| `RateLimiterService` | Holds a list of limiters. `add_limiter(limiter)`, `check(client_id) -> bool`. |

### Constraints

- `is_allowed()` **must be thread-safe** (concurrent calls from multiple threads must not over-admit).
- `is_allowed()` **updates internal state** — consuming a token or recording a timestamp is part of the call.
- Time is injectable via an optional `clock` argument (callable returning `float` seconds). Default: `time.time`. This is mandatory for deterministic unit tests.
- `RateLimiterService.check()` requires **all** added limiters to allow the request; if any denies it, the service denies it.

## Example Usage

```python
import time

# Token bucket: 10 requests burst, refill 2 per second
limiter = TokenBucketLimiter(capacity=10, refill_rate=2.0)
client = "user:42"

for _ in range(10):
    assert limiter.is_allowed(client)   # all 10 succeed (full bucket)

assert not limiter.is_allowed(client)   # 11th denied (bucket empty)

time.sleep(0.5)                         # 0.5s × 2 tok/s = 1 token refilled
assert limiter.is_allowed(client)       # now allowed again

# Combine limiters in a service
service = RateLimiterService()
service.add_limiter(TokenBucketLimiter(capacity=5, refill_rate=1.0))
service.add_limiter(FixedWindowLimiter(max_requests=3, window_seconds=1.0))

# Request allowed only if BOTH limiters allow it
print(service.check("user:99"))         # True (first request)
```

## Hints

- Use `threading.Lock` (one per limiter instance) to protect shared per-client state.
- Store per-client state in dicts keyed by `client_id`; initialise lazily on first call.
- For the token bucket, calculate elapsed time since the last refill to determine how many tokens to add.
- For the sliding window, a `collections.deque` lets you efficiently pop old timestamps from the left.
- For `RateLimiterService.check()`, iterate limiters in order and call `is_allowed()` on each — do **not** short-circuit before calling every limiter, because each call has side-effects (state update).

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **Strategy** | `RateLimiter` ABC — Token Bucket, Fixed Window, Sliding Window are fully interchangeable |
| **Proxy** | `RateLimiterService` acts as a gating proxy — checks all limiters before forwarding to the real handler |
| **Thread Safety** | `threading.Lock` per limiter instance protects per-client state from concurrent requests |
| **OCP** | New algorithm → new `RateLimiter` subclass; `RateLimiterService` never changes |

**See also:** Module 03 → [Strategy](../../03_design_patterns/behavioral/strategy/), [Proxy](../../03_design_patterns/structural/proxy/), Module 02 → [OCP](../../02_solid_principles/02_open_closed/)
