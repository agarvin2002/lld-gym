"""
Thread-safe Singleton and Thread-local Storage
===============================================
Section 1 — Thread-safe Singleton with double-checked locking.
Section 2 — Thread-local storage for per-thread request context.
"""

import threading
import time


# ===========================================================================
# SECTION 1: Thread-safe Singleton — Double-Checked Locking
# ===========================================================================

class DatabaseConnection:
    """Simulates a shared database connection pool.

    Only one instance is ever created regardless of how many threads call
    get_instance() concurrently. The double-checked locking pattern avoids
    lock acquisition on every call after the instance is created.
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        # In a real system this would open a connection pool.
        self.connection_id = id(self)
        self._query_count = 0
        self._query_lock = threading.Lock()
        print(f"  [DatabaseConnection] New instance created (id={self.connection_id})")

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        if cls._instance is None:           # First check — no lock (fast path)
            with cls._lock:
                if cls._instance is None:   # Second check — with lock (safe)
                    cls._instance = cls()
        return cls._instance

    def query(self, sql: str) -> str:
        with self._query_lock:
            self._query_count += 1
            count = self._query_count
        # Simulate query execution time
        time.sleep(0.001)
        return f"Result of '{sql}' (query #{count})"

    @property
    def query_count(self) -> int:
        with self._query_lock:
            return self._query_count


def demo_singleton() -> None:
    print("=" * 60)
    print("SECTION 1: Thread-safe Singleton")
    print("=" * 60)

    instances_seen: list = []
    lock = threading.Lock()

    def worker(thread_id: int) -> None:
        conn = DatabaseConnection.get_instance()
        result = conn.query(f"SELECT * FROM users WHERE id={thread_id}")
        with lock:
            instances_seen.append(id(conn))
        print(f"  Thread-{thread_id}: {result}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique_ids = set(instances_seen)
    print(f"\n  Threads run    : {len(threads)}")
    print(f"  Unique instances: {len(unique_ids)}")
    print(f"  Singleton holds : {len(unique_ids) == 1}")
    print(f"  Total queries  : {DatabaseConnection.get_instance().query_count}")


# ===========================================================================
# SECTION 2: Thread-local Storage — Per-thread Request Context
# ===========================================================================

class RequestContext:
    """Stores per-thread request metadata (user ID, request ID).

    Uses threading.local() so that each thread has its own independent
    copy of user_id and request_id — setting values in one thread never
    affects another thread.
    """

    _local = threading.local()

    @classmethod
    def set(cls, user_id: str, request_id: str) -> None:
        """Initialize context for the current thread."""
        cls._local.user_id = user_id
        cls._local.request_id = request_id

    @classmethod
    def get_user_id(cls) -> str:
        return getattr(cls._local, 'user_id', None)

    @classmethod
    def get_request_id(cls) -> str:
        return getattr(cls._local, 'request_id', None)

    @classmethod
    def clear(cls) -> None:
        """Remove context for the current thread (clean up after request)."""
        if hasattr(cls._local, 'user_id'):
            del cls._local.user_id
        if hasattr(cls._local, 'request_id'):
            del cls._local.request_id


def simulate_request_handler(user_id: str, request_id: str, delay: float) -> None:
    """Simulates a web framework's request handler running in a worker thread."""
    # Each thread initialises its own context at the start of the request
    RequestContext.set(user_id=user_id, request_id=request_id)

    # Simulate work that spans multiple function calls — context is always
    # available via RequestContext without passing it as a parameter.
    time.sleep(delay)

    uid = RequestContext.get_user_id()
    rid = RequestContext.get_request_id()

    print(f"  [{threading.current_thread().name}] "
          f"user_id={uid!r}, request_id={rid!r}")

    # Verify isolation: our values haven't been overwritten by other threads
    assert uid == user_id, f"Context polluted! Expected {user_id!r}, got {uid!r}"
    assert rid == request_id, f"Context polluted! Expected {request_id!r}, got {rid!r}"

    RequestContext.clear()


def demo_thread_local() -> None:
    print("\n" + "=" * 60)
    print("SECTION 2: Thread-local Storage")
    print("=" * 60)

    # Requests overlap in time — each thread must see only its own context
    requests = [
        ("user-alpha",   "req-001", 0.05),
        ("user-beta",    "req-002", 0.01),   # Finishes before alpha
        ("user-gamma",   "req-003", 0.03),
    ]

    threads = [
        threading.Thread(
            target=simulate_request_handler,
            args=args,
            name=f"Worker-{i+1}"
        )
        for i, args in enumerate(requests)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n  All threads completed — no context cross-contamination detected.")

    # Demonstrate that the main thread has no context set
    print(f"  Main thread user_id (should be None): {RequestContext.get_user_id()!r}")


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    demo_singleton()
    demo_thread_local()
