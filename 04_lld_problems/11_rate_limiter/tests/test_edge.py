"""Rate Limiter — Edge Cases and Concurrency."""
import sys, os
import threading
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import TokenBucketLimiter, FixedWindowLimiter, SlidingWindowLimiter


def make_clock(start=0.0):
    t = [start]
    return t, lambda: t[0]


class TestCapacityBoundary:
    def test_capacity_one(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=1, refill_rate=1.0, clock=clock)
        assert limiter.is_allowed("c") is True
        assert limiter.is_allowed("c") is False

    def test_capacity_zero(self):
        t, clock = make_clock()
        limiter = TokenBucketLimiter(capacity=0, refill_rate=1.0, clock=clock)
        assert limiter.is_allowed("c") is False

    def test_max_requests_zero_fixed(self):
        t, clock = make_clock()
        limiter = FixedWindowLimiter(max_requests=0, window_seconds=10.0, clock=clock)
        assert limiter.is_allowed("c") is False

    def test_max_requests_zero_sliding(self):
        t, clock = make_clock(start=100.0)
        limiter = SlidingWindowLimiter(max_requests=0, window_seconds=10.0, clock=clock)
        assert limiter.is_allowed("c") is False


class TestConcurrentAccess:
    def test_token_bucket_exact_count(self):
        """10 threads race for 10 tokens — exactly 10 succeed."""
        limiter = TokenBucketLimiter(capacity=10, refill_rate=0.0)
        results = []
        lock = threading.Lock()

        def try_request():
            ok = limiter.is_allowed("shared")
            with lock:
                results.append(ok)

        threads = [threading.Thread(target=try_request) for _ in range(20)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert results.count(True) == 10
        assert results.count(False) == 10

    def test_fixed_window_exact_count(self):
        """20 threads race; only max_requests=5 should succeed."""
        t, clock = make_clock()
        limiter = FixedWindowLimiter(max_requests=5, window_seconds=60.0, clock=clock)
        results = []
        lock = threading.Lock()

        def try_request():
            ok = limiter.is_allowed("shared")
            with lock:
                results.append(ok)

        threads = [threading.Thread(target=try_request) for _ in range(20)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert results.count(True) == 5

    def test_sliding_window_concurrent(self):
        """15 threads race; only max_requests=7 should succeed."""
        limiter = SlidingWindowLimiter(max_requests=7, window_seconds=60.0)
        results = []
        lock = threading.Lock()

        def try_request():
            ok = limiter.is_allowed("shared")
            with lock:
                results.append(ok)

        threads = [threading.Thread(target=try_request) for _ in range(15)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert results.count(True) == 7

    def test_multiple_clients_no_interference(self):
        """Concurrent requests for different clients don't interfere."""
        limiter = TokenBucketLimiter(capacity=1, refill_rate=0.0)
        allowed_per_client: dict[str, int] = {}
        lock = threading.Lock()

        def try_request(client_id: str):
            ok = limiter.is_allowed(client_id)
            with lock:
                allowed_per_client[client_id] = allowed_per_client.get(client_id, 0) + ok

        threads = []
        for i in range(10):
            client = f"client_{i}"
            for _ in range(3):
                threads.append(threading.Thread(target=try_request, args=(client,)))

        for th in threads:
            th.start()
        for th in threads:
            th.join()

        # Each client has capacity=1, so exactly 1 allowed per client
        for i in range(10):
            assert allowed_per_client.get(f"client_{i}", 0) == 1
