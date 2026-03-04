"""Rate Limiter — Basic Tests: Token Bucket and Fixed Window happy path."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import TokenBucketLimiter, FixedWindowLimiter, RateLimiterService


def make_clock(start=0.0):
    """Returns a mutable clock. Advance via t[0] += seconds."""
    t = [start]
    return t, lambda: t[0]


class TestTokenBucket:
    def test_first_requests_allowed(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=3, refill_rate=1.0, clock=clock)
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True

    def test_exhausted_bucket_denied(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=3, refill_rate=1.0, clock=clock)
        for _ in range(3):
            limiter.is_allowed("c")
        assert limiter.is_allowed("c") is False

    def test_one_token_refilled(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=3, refill_rate=1.0, clock=clock)
        for _ in range(3):
            limiter.is_allowed("c")
        t[0] += 1.0  # 1 second → 1 token refilled
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is False  # only 1 token was added

    def test_full_refill_capped_at_capacity(self):
        t, clock = make_clock()
        capacity = 5
        limiter = TokenBucketLimiter(capacity=capacity, refill_rate=2.0, clock=clock)
        for _ in range(capacity):
            limiter.is_allowed("c")
        t[0] += 100.0  # way more than needed to refill
        allowed = sum(limiter.is_allowed("c") for _ in range(capacity + 2))
        assert allowed == capacity  # capped at capacity, not 100*2=200

    def test_multiple_clients_independent(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=2, refill_rate=1.0, clock=clock)
        limiter.is_allowed("a")
        limiter.is_allowed("a")
        assert limiter.is_allowed("a") is False
        assert limiter.is_allowed("b") is True  # b has its own bucket

    def test_fractional_refill(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=10, refill_rate=2.0, clock=clock)
        for _ in range(10):
            limiter.is_allowed("c")
        t[0] += 0.4   # 0.4 * 2 = 0.8 tokens — not enough for 1
        assert limiter.is_allowed("c") is False
        t[0] += 0.1   # total 0.5s → 1.0 token
        assert limiter.is_allowed("c") is True


class TestFixedWindow:
    def test_requests_within_window_allowed(self):
        t, clock = make_clock()
        limiter = FixedWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True

    def test_excess_in_window_denied(self):
        t, clock = make_clock()
        limiter = FixedWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        for _ in range(3):
            limiter.is_allowed("c")
        assert limiter.is_allowed("c") is False

    def test_new_window_resets_counter(self):
        t, clock = make_clock()
        limiter = FixedWindowLimiter(max_requests=3, window_seconds=10.0, clock=clock)
        for _ in range(3):
            limiter.is_allowed("c")
        t[0] += 10.0  # move into next window
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is False

    def test_multiple_clients(self):
        t, clock = make_clock()
        limiter = FixedWindowLimiter(max_requests=1, window_seconds=5.0, clock=clock)
        limiter.is_allowed("x")
        assert limiter.is_allowed("x") is False
        assert limiter.is_allowed("y") is True
