"""Rate Limiter — Extended Tests: Sliding Window and RateLimiterService."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import TokenBucketLimiter, FixedWindowLimiter, SlidingWindowLimiter, RateLimiterService


def make_clock(start=0.0):
    t = [start]
    return t, lambda: t[0]


class TestSlidingWindow:
    def test_requests_within_window(self):
        t, clock = make_clock(start=100.0)
        limiter = SlidingWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True

    def test_excess_denied(self):
        t, clock = make_clock(start=100.0)
        limiter = SlidingWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        for _ in range(3):
            limiter.is_allowed("c")
        assert limiter.is_allowed("c") is False

    def test_old_requests_age_out(self):
        t, clock = make_clock(start=100.0)
        limiter = SlidingWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        limiter.is_allowed("c")   # t=100
        limiter.is_allowed("c")   # t=100
        limiter.is_allowed("c")   # t=100 — bucket full
        t[0] = 110.01             # all 3 older timestamps are outside window
        assert limiter.is_allowed("c") is True

    def test_partial_age_out(self):
        t, clock = make_clock(start=100.0)
        limiter = SlidingWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        limiter.is_allowed("c")   # t=100
        t[0] = 105.0
        limiter.is_allowed("c")   # t=105
        limiter.is_allowed("c")   # t=105
        # now 3 requests: at t=100,105,105
        assert limiter.is_allowed("c") is False
        t[0] = 110.01  # t=100 ages out; 2 remain
        assert limiter.is_allowed("c") is True  # 3rd slot opened

    def test_boundary_exact(self):
        """Timestamp exactly at cutoff (now - window) should be evicted."""
        t, clock = make_clock(start=100.0)
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=10.0, clock=clock)
        limiter.is_allowed("c")   # t=100
        t[0] = 110.0              # cutoff = 100.0; t=100 is <= cutoff → evicted
        assert limiter.is_allowed("c") is True

    def test_multiple_clients(self):
        t, clock = make_clock(start=0.0)
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=5.0, clock=clock)
        limiter.is_allowed("a")
        limiter.is_allowed("a")
        assert limiter.is_allowed("a") is False
        assert limiter.is_allowed("b") is True


class TestRateLimiterService:
    def test_empty_service_allows(self):
        svc = RateLimiterService()
        assert svc.check("c") is True

    def test_single_limiter_passes(self):
        t, clock = make_clock()
        svc = RateLimiterService()
        svc.add_limiter(TokenBucketLimiter(5, 1.0, clock=clock))
        assert svc.check("c") is True

    def test_single_limiter_denies(self):
        t, clock = make_clock()
        svc = RateLimiterService()
        svc.add_limiter(TokenBucketLimiter(1, 1.0, clock=clock))
        svc.check("c")  # consume 1
        assert svc.check("c") is False

    def test_both_limiters_must_allow(self):
        t1, clock1 = make_clock()
        t2, clock2 = make_clock()
        svc = RateLimiterService()
        # limiter1 allows 2 per second, limiter2 allows only 1
        svc.add_limiter(TokenBucketLimiter(2, 1.0, clock=clock1))
        svc.add_limiter(FixedWindowLimiter(1, 10.0, clock=clock2))
        assert svc.check("c") is True   # first: both allow
        assert svc.check("c") is False  # second: fixed window denies

    def test_all_limiters_called_even_if_first_denies(self):
        """RateLimiterService must not short-circuit; all limiters update state."""
        t1, clock1 = make_clock()
        t2, clock2 = make_clock()
        svc = RateLimiterService()
        lim1 = FixedWindowLimiter(1, 10.0, clock=clock1)
        lim2 = FixedWindowLimiter(2, 10.0, clock=clock2)
        svc.add_limiter(lim1)
        svc.add_limiter(lim2)
        svc.check("c")  # both allowed, lim1 count=1, lim2 count=1
        svc.check("c")  # lim1 denies; if lim2 is still called its count becomes 2
        # Now lim2 should have count=2 (if called), denying next request
        assert lim2.is_allowed("c") is False

    def test_multiple_clients_tracked_independently(self):
        t, clock = make_clock()
        svc = RateLimiterService()
        svc.add_limiter(FixedWindowLimiter(1, 10.0, clock=clock))
        svc.check("alice")
        svc.check("bob")
        assert svc.check("alice") is False
        assert svc.check("bob") is False
        assert svc.check("carol") is True
