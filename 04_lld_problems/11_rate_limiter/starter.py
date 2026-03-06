"""
Rate Limiter — Starter File
=============================
Your task: Implement three rate limiting algorithms.

Read problem.md and design.md before starting.

Design decisions:
  - RateLimiter is an ABC with a single method: is_allowed(client_id) -> bool
  - TokenBucketLimiter: tokens refill continuously; each request consumes 1 token
  - FixedWindowLimiter: count resets at the start of each fixed time window
  - SlidingWindowLimiter: only counts requests within the last window_seconds
  - All algorithms are thread-safe using threading.Lock
  - Use an injected clock function (default: time.time) for testability
  - RateLimiterService: composes multiple limiters (request allowed only if ALL allow it)
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
import threading
import time


class RateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, client_id: str) -> bool:
        """Return True if the request should be allowed, False if rate-limited."""
        ...


class TokenBucketLimiter(RateLimiter):
    """Allows burst traffic up to capacity, refills at a constant rate.

    Per client: tokens refill over time (elapsed * refill_rate), capped at capacity.
    Each allowed request consumes 1 token.
    """

    def __init__(self, capacity: int, refill_rate: float, clock=None) -> None:
        # TODO: Store _capacity, _refill_rate, _clock (default: time.time)
        # TODO: Create _buckets: dict[str, float] = {}  (client_id → token count)
        # TODO: Create _last_refill: dict[str, float] = {}  (client_id → last check time)
        # TODO: Create _lock = threading.Lock()
        pass

    def _refill(self, client_id: str) -> None:
        """Refill tokens for client_id based on elapsed time.

        TODO:
            - Compute elapsed = now - _last_refill[client_id]
            - Add elapsed * _refill_rate tokens to the bucket
            - Cap at _capacity (use min())
            - Update _last_refill[client_id] = now
        """
        pass

    def is_allowed(self, client_id: str) -> bool:
        """Check and consume a token if available (thread-safe).

        TODO (all under _lock):
            - If client is new: initialize bucket to full capacity, set last_refill = now
            - Call _refill(client_id) to add any accumulated tokens
            - If bucket >= 1: deduct 1 token, return True
            - Otherwise: return False
        """
        pass


class FixedWindowLimiter(RateLimiter):
    """Allows up to max_requests per fixed time window per client.

    Window resets when window_seconds have elapsed since the window started.
    """

    def __init__(self, max_requests: int, window_seconds: float, clock=None) -> None:
        # TODO: Store _max_requests, _window, _clock (default: time.time)
        # TODO: Create _counts: dict[str, int] = {}
        # TODO: Create _window_start: dict[str, float] = {}
        # TODO: Create _lock = threading.Lock()
        pass

    def is_allowed(self, client_id: str) -> bool:
        """Check request against fixed window (thread-safe).

        TODO (all under _lock):
            - If client is new: initialize window_start = now, count = 0
            - Elif now - window_start >= window_seconds: reset count = 0, window_start = now
            - If count < max_requests: increment count, return True
            - Otherwise: return False
        """
        pass


class SlidingWindowLimiter(RateLimiter):
    """Allows up to max_requests in any rolling window_seconds period.

    Uses a timestamp log per client; evicts timestamps older than window_seconds.
    """

    def __init__(self, max_requests: int, window_seconds: float, clock=None) -> None:
        # TODO: Store _max_requests, _window, _clock (default: time.time)
        # TODO: Create _logs: dict[str, deque] = {}  (client_id → timestamps deque)
        # TODO: Create _lock = threading.Lock()
        pass

    def is_allowed(self, client_id: str) -> bool:
        """Check request against sliding window (thread-safe).

        TODO (all under _lock):
            - Initialize deque for new clients
            - Evict timestamps <= (now - window_seconds) from the front
            - If len(log) < max_requests: append now, return True
            - Otherwise: return False
        """
        pass


class RateLimiterService:
    """Composes multiple limiters. A request is allowed only if ALL limiters allow it."""

    def __init__(self) -> None:
        # TODO: Create _limiters: list[RateLimiter] = []
        pass

    def add_limiter(self, limiter: RateLimiter) -> None:
        # TODO: Append limiter to _limiters
        pass

    def check(self, client_id: str) -> bool:
        """Return True only if all limiters allow the request.

        TODO:
            - Call is_allowed(client_id) on each limiter
            - Return True only if all return True
            - Note: call ALL limiters (don't short-circuit) so token counts stay consistent
        """
        pass
