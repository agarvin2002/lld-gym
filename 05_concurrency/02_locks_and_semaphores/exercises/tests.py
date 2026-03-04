"""Tests for ConnectionPool (thread-safe semaphore-based connection pool)."""

import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import ConnectionPool


class TestInitialState:
    def test_initial_state(self):
        pool = ConnectionPool(4)
        assert pool.available == 4
        assert pool.size == 4

    def test_size_matches_constructor_argument(self):
        for n in (1, 3, 10):
            pool = ConnectionPool(n)
            assert pool.size == n
            assert pool.available == n


class TestAcquire:
    def test_acquire_returns_connection_string(self):
        pool = ConnectionPool(3)
        conn = pool.acquire()
        assert isinstance(conn, str)
        assert conn.startswith("conn-")

    def test_acquire_reduces_available_by_one(self):
        pool = ConnectionPool(3)
        pool.acquire()
        assert pool.available == 2

    def test_acquire_multiple_reduces_available(self):
        pool = ConnectionPool(5)
        for expected_available in (4, 3, 2):
            pool.acquire()
            assert pool.available == expected_available


class TestRelease:
    def test_release_restores_available(self):
        pool = ConnectionPool(3)
        conn = pool.acquire()
        assert pool.available == 2
        pool.release(conn)
        assert pool.available == 3

    def test_release_same_conn_can_be_reacquired(self):
        pool = ConnectionPool(2)
        conn = pool.acquire()
        pool.release(conn)
        # The same connection string should be usable again
        conn2 = pool.acquire()
        assert conn2.startswith("conn-")

    def test_acquire_release_cycle_restores_full_availability(self):
        pool = ConnectionPool(3)
        conns = [pool.acquire() for _ in range(3)]
        assert pool.available == 0
        for c in conns:
            pool.release(c)
        assert pool.available == 3


class TestExhaustPool:
    def test_acquire_all_then_no_more_available(self):
        pool = ConnectionPool(3)
        conns = []
        for _ in range(3):
            conns.append(pool.acquire())
        assert pool.available == 0

    def test_pool_size_one_acquire_release_cycle(self):
        pool = ConnectionPool(1)
        assert pool.size == 1
        conn = pool.acquire()
        assert pool.available == 0
        pool.release(conn)
        assert pool.available == 1


class TestConcurrency:
    def test_concurrent_workers_no_errors(self):
        """20 threads each do: acquire → sleep(0.01) → release.
        No exceptions must be raised and the pool must be fully
        available once all threads have finished.
        """
        pool = ConnectionPool(5)
        errors: list[Exception] = []

        def worker() -> None:
            try:
                conn = pool.acquire()
                time.sleep(0.01)
                pool.release(conn)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5.0)

        assert errors == [], f"Unexpected errors: {errors}"
        assert pool.available == pool.size, (
            f"Pool should be fully available after all workers finish; "
            f"got available={pool.available}, size={pool.size}"
        )

    def test_acquire_blocks_when_exhausted(self):
        """Drain the pool, then verify a new acquire() call blocks.
        After releasing one connection the blocked thread should unblock.
        """
        pool = ConnectionPool(2)
        conns = [pool.acquire() for _ in range(2)]   # drain the pool
        assert pool.available == 0

        acquired_by_thread: list[str] = []

        def blocking_acquire() -> None:
            conn = pool.acquire()    # must block until a connection is released
            acquired_by_thread.append(conn)

        t = threading.Thread(target=blocking_acquire, daemon=True)
        t.start()
        time.sleep(0.1)   # give the thread time to start and block

        assert t.is_alive(), (
            "Thread should still be blocked; the pool is exhausted"
        )
        assert acquired_by_thread == [], (
            "Thread should not have acquired a connection yet"
        )

        # Release one connection — the blocked thread should now unblock
        pool.release(conns[0])
        t.join(timeout=1.0)

        assert not t.is_alive(), (
            "Thread should have unblocked and finished after a connection was released"
        )
        assert len(acquired_by_thread) == 1
        assert acquired_by_thread[0].startswith("conn-")

    def test_no_connection_served_twice_simultaneously(self):
        """Each connection must be held by at most one thread at a time."""
        pool = ConnectionPool(3)
        held: dict[str, threading.Event] = {}
        held_lock = threading.Lock()
        violations: list[str] = []

        def worker() -> None:
            conn = pool.acquire()
            with held_lock:
                if conn in held:
                    violations.append(f"{conn} held by two threads simultaneously")
                held[conn] = threading.Event()

            time.sleep(0.02)

            with held_lock:
                del held[conn]
            pool.release(conn)

        threads = [threading.Thread(target=worker) for _ in range(9)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5.0)

        assert violations == [], f"Exclusivity violations: {violations}"
