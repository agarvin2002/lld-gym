"""Rate Limiter — Reference Solution."""
from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
import threading
import time


class RateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, client_id: str) -> bool: ...


class TokenBucketLimiter(RateLimiter):
    def __init__(self, capacity: int, refill_rate: float, clock=None) -> None:
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._clock = clock or time.time
        self._buckets: dict[str, float] = {}
        self._last_refill: dict[str, float] = {}
        self._lock = threading.Lock()

    def _refill(self, client_id: str) -> None:
        now = self._clock()
        last = self._last_refill.get(client_id, now)
        elapsed = now - last
        added = elapsed * self._refill_rate
        current = self._buckets.get(client_id, float(self._capacity))
        self._buckets[client_id] = min(self._capacity, current + added)
        self._last_refill[client_id] = now

    def is_allowed(self, client_id: str) -> bool:
        with self._lock:
            if client_id not in self._buckets:
                self._buckets[client_id] = float(self._capacity)
                self._last_refill[client_id] = self._clock()
            self._refill(client_id)
            if self._buckets[client_id] >= 1:
                self._buckets[client_id] -= 1
                return True
            return False


class FixedWindowLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_seconds: float, clock=None) -> None:
        self._max_requests = max_requests
        self._window = window_seconds
        self._clock = clock or time.time
        self._counts: dict[str, int] = {}
        self._window_start: dict[str, float] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> bool:
        with self._lock:
            now = self._clock()
            if client_id not in self._window_start:
                self._window_start[client_id] = now
                self._counts[client_id] = 0
            elif now - self._window_start[client_id] >= self._window:
                self._counts[client_id] = 0
                self._window_start[client_id] = now
            if self._counts[client_id] < self._max_requests:
                self._counts[client_id] += 1
                return True
            return False


class SlidingWindowLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_seconds: float, clock=None) -> None:
        self._max_requests = max_requests
        self._window = window_seconds
        self._clock = clock or time.time
        self._logs: dict[str, deque] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> bool:
        with self._lock:
            now = self._clock()
            if client_id not in self._logs:
                self._logs[client_id] = deque()
            log = self._logs[client_id]
            cutoff = now - self._window
            while log and log[0] <= cutoff:
                log.popleft()
            if len(log) < self._max_requests:
                log.append(now)
                return True
            return False


class RateLimiterService:
    def __init__(self) -> None:
        self._limiters: list[RateLimiter] = []

    def add_limiter(self, limiter: RateLimiter) -> None:
        self._limiters.append(limiter)

    def check(self, client_id: str) -> bool:
        results = [limiter.is_allowed(client_id) for limiter in self._limiters]
        return all(results)
