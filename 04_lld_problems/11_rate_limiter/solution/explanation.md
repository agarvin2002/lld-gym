# Rate Limiter — Solution Explanation

## Algorithm Comparison

| Algorithm | Memory | Accuracy | Burst behaviour |
|-----------|--------|----------|----------------|
| Token Bucket | O(1) per client | High | Allows bursts up to capacity |
| Fixed Window | O(1) per client | Low | 2× burst at window boundary |
| Sliding Window Log | O(max_requests) per client | Highest | No boundary burst |

## Token Bucket: fractional accumulation

```python
added = elapsed * self._refill_rate
self._buckets[client_id] = min(self._capacity, current + added)
```

Fractional tokens accumulate between calls. Only whole tokens (`>= 1`) are consumed. This gives smooth rate enforcement without requiring a background refill thread.

## Fixed Window: boundary burst problem

Suppose max_requests=10 per 60s window. A client can send 10 at t=59s (last second of window) and 10 at t=61s (first second of next window) — 20 requests in 2 seconds. This is why high-accuracy systems prefer sliding window.

## Sliding Window Log: exact enforcement

```python
cutoff = now - self._window
while log and log[0] <= cutoff:
    log.popleft()
```

Evict timestamps `<= cutoff` (not `< cutoff`) to correctly handle the boundary: a timestamp exactly at `now - window` is at the edge of the window and should no longer count.

## Why `clock` injection matters

Without injectable time:
- Tests are slow (must `time.sleep()` to advance time)
- Tests are flaky (timing-sensitive on slow CI)
- Concurrency tests are impossible to make deterministic

With `clock=lambda: t[0]`, tests advance time instantly: `t[0] += 1.0`.

## Thread safety pattern

All mutable state is protected by a single per-instance `threading.Lock`. The critical section includes both the read of current state and the write of new state, making the check-then-update atomic.

## RateLimiterService: no short-circuit

```python
results = [limiter.is_allowed(client_id) for limiter in self._limiters]
return all(results)
```

Evaluating all limiters (not `all(l.is_allowed(...) for l in ...)`) ensures every limiter's internal state is updated even when the first denies. This matters when limiters track usage for metrics or quota tracking purposes.

## Lazy per-client initialization

Client state is initialized on the first call to `is_allowed()`, not in `__init__`. This avoids pre-registration and works naturally with any client ID that appears at runtime.
