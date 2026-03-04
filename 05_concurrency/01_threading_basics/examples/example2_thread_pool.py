"""
Example 2: ThreadPoolExecutor — High-Level Thread Pool
=======================================================
Demonstrates:
- concurrent.futures.ThreadPoolExecutor
- submit() and Future objects
- map() for parallel iteration
- result() and exception() on futures
- Context manager usage (recommended)
- Practical: parallel API calls simulation
- Comparing serial vs parallel execution time
"""

import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import Callable


# =============================================================================
# SECTION 1: Basic submit() and Future
# =============================================================================

def compute_square(n: int) -> int:
    """Simulate a computation that takes time."""
    time.sleep(random.uniform(0.05, 0.2))
    return n * n


def demo_submit_and_future() -> None:
    print("\n--- DEMO 1: submit() and Future ---")

    # ThreadPoolExecutor manages a pool of worker threads.
    # You submit tasks; the pool picks them up as workers become free.
    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="Pool") as executor:
        # submit() returns immediately with a Future
        futures: list[Future] = []
        for i in range(8):
            future = executor.submit(compute_square, i)
            futures.append(future)
            print(f"  Submitted task for {i}, future done: {future.done()}")

        print("\n  Waiting for results...")
        for i, future in enumerate(futures):
            result = future.result()  # blocks until this specific future is done
            print(f"  Square of {i} = {result}")

    # The 'with' block ensures all submitted tasks complete before exiting
    print("  All tasks complete (executor shut down)")


# =============================================================================
# SECTION 2: Handling exceptions with Future
# =============================================================================

def risky_task(n: int) -> int:
    """May raise an exception."""
    time.sleep(0.1)
    if n % 3 == 0:
        raise ValueError(f"Cannot process multiple of 3: {n}")
    return n * 10


def demo_exception_handling() -> None:
    print("\n--- DEMO 2: Exception Handling with Futures ---")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_task, i): i for i in range(9)}

        for future, input_val in futures.items():
            try:
                result = future.result()
                print(f"  Task({input_val}) = {result}")
            except ValueError as e:
                # exception() stores the exception; result() re-raises it
                print(f"  Task({input_val}) FAILED: {e}")

    # Key insight: one task failing does NOT crash other tasks


# =============================================================================
# SECTION 3: as_completed() — process results as they arrive
# =============================================================================

def fetch_data(endpoint: str) -> dict:
    """Simulate an API call with variable latency."""
    latency = random.uniform(0.05, 0.4)
    time.sleep(latency)
    return {"endpoint": endpoint, "data": f"Result from {endpoint}", "latency": latency}


def demo_as_completed() -> None:
    print("\n--- DEMO 3: as_completed() — Process Results in Arrival Order ---")

    endpoints = [
        "/api/users", "/api/products", "/api/orders",
        "/api/reviews", "/api/inventory", "/api/analytics"
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Map future -> endpoint for identification
        future_to_endpoint = {
            executor.submit(fetch_data, ep): ep
            for ep in endpoints
        }

        # as_completed yields futures in the order they FINISH (not submission order)
        for future in as_completed(future_to_endpoint):
            endpoint = future_to_endpoint[future]
            try:
                result = future.result()
                print(f"  Completed: {endpoint} ({result['latency']:.2f}s)")
            except Exception as e:
                print(f"  Failed: {endpoint} — {e}")


# =============================================================================
# SECTION 4: map() — simplest parallel iteration
# =============================================================================

def process_item(item: str) -> str:
    """Process a single item."""
    time.sleep(random.uniform(0.05, 0.15))
    return f"processed:{item.upper()}"


def demo_map() -> None:
    print("\n--- DEMO 4: executor.map() ---")

    items = ["apple", "banana", "cherry", "date", "elderberry", "fig"]

    # Serial version
    start = time.time()
    serial_results = [process_item(item) for item in items]
    serial_time = time.time() - start
    print(f"  Serial results: {serial_results}")
    print(f"  Serial time: {serial_time:.2f}s")

    # Parallel version with map()
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        # map() preserves ORDER of results (unlike as_completed)
        parallel_results = list(executor.map(process_item, items))
    parallel_time = time.time() - start
    print(f"\n  Parallel results: {parallel_results}")
    print(f"  Parallel time: {parallel_time:.2f}s")
    print(f"  Speedup: {serial_time / parallel_time:.1f}x")

    # Note: map() raises immediately if any task raises (unlike manual future handling)


# =============================================================================
# SECTION 5: map() with timeout
# =============================================================================

def slow_operation(n: int) -> int:
    time.sleep(n * 0.2)
    return n

def demo_map_timeout() -> None:
    print("\n--- DEMO 5: map() with timeout ---")

    with ThreadPoolExecutor(max_workers=3) as executor:
        try:
            results = list(executor.map(slow_operation, [1, 2, 3, 4, 5], timeout=0.5))
            print(f"  Results: {results}")
        except Exception as e:
            print(f"  Timeout exceeded: {type(e).__name__}: {e}")


# =============================================================================
# SECTION 6: Practical — Parallel API Simulation
# =============================================================================

class APIClient:
    """Simulates an API client with rate limiting and retries."""

    def __init__(self, base_url: str, max_retries: int = 2) -> None:
        self.base_url = base_url
        self.max_retries = max_retries
        self._request_count = 0
        self._lock = threading.Lock()

    def get(self, path: str) -> dict:
        """Make a GET request (simulated)."""
        with self._lock:
            self._request_count += 1

        for attempt in range(self.max_retries + 1):
            try:
                # Simulate: 20% chance of transient failure
                latency = random.uniform(0.05, 0.3)
                time.sleep(latency)

                if random.random() < 0.15 and attempt < self.max_retries:
                    raise ConnectionError(f"Transient error on {path} (attempt {attempt + 1})")

                return {
                    "url": f"{self.base_url}{path}",
                    "status": 200,
                    "data": f"Data for {path}",
                    "latency_ms": int(latency * 1000),
                    "attempt": attempt + 1,
                }
            except ConnectionError:
                if attempt == self.max_retries:
                    raise

        raise RuntimeError("Should not reach here")

    @property
    def total_requests(self) -> int:
        return self._request_count


def fetch_user_data(client: APIClient, user_id: int) -> dict:
    """Fetch all data for a user: profile + orders + recommendations."""
    profile = client.get(f"/users/{user_id}")
    orders = client.get(f"/users/{user_id}/orders")
    recs = client.get(f"/users/{user_id}/recommendations")
    return {
        "user_id": user_id,
        "profile": profile["data"],
        "orders": orders["data"],
        "recommendations": recs["data"],
    }


def demo_parallel_api_calls() -> None:
    print("\n--- DEMO 6: Parallel API Calls (Realistic Simulation) ---")

    client = APIClient("https://api.example.com")
    user_ids = list(range(1, 7))  # 6 users

    # Serial approach
    print("  Serial fetch:")
    start = time.time()
    serial_results = []
    for uid in user_ids:
        try:
            data = fetch_user_data(client, uid)
            serial_results.append(data)
            print(f"    Fetched user {uid}")
        except Exception as e:
            print(f"    Failed user {uid}: {e}")
    serial_time = time.time() - start
    print(f"  Serial total: {serial_time:.2f}s, requests: {client.total_requests}")

    # Reset client
    client2 = APIClient("https://api.example.com")

    # Parallel approach
    print("\n  Parallel fetch (max_workers=3):")
    start = time.time()
    parallel_results = []

    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="APIWorker") as executor:
        future_to_uid = {
            executor.submit(fetch_user_data, client2, uid): uid
            for uid in user_ids
        }

        for future in as_completed(future_to_uid):
            uid = future_to_uid[future]
            try:
                data = future.result()
                parallel_results.append(data)
                print(f"    Fetched user {uid}")
            except Exception as e:
                print(f"    Failed user {uid}: {e}")

    parallel_time = time.time() - start
    print(f"  Parallel total: {parallel_time:.2f}s, requests: {client2.total_requests}")

    if serial_time > 0 and parallel_time > 0:
        print(f"\n  Speedup: {serial_time / parallel_time:.1f}x")


# =============================================================================
# SECTION 7: Choosing max_workers
# =============================================================================

def demo_worker_count_impact() -> None:
    print("\n--- DEMO 7: Impact of max_workers Count ---")

    def io_task(_: int) -> float:
        """Pure I/O task — sleep simulates waiting."""
        latency = 0.1
        time.sleep(latency)
        return latency

    tasks = list(range(20))  # 20 tasks, each takes 0.1s

    for workers in [1, 2, 4, 8, 20]:
        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            list(executor.map(io_task, tasks))
        elapsed = time.time() - start
        print(f"  max_workers={workers:2d}: {elapsed:.2f}s")

    print("  (For I/O tasks, more workers = faster, up to task count)")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ThreadPoolExecutor — Complete Demo")
    print("=" * 60)

    demo_submit_and_future()
    demo_exception_handling()
    demo_as_completed()
    demo_map()
    demo_map_timeout()
    demo_parallel_api_calls()
    demo_worker_count_impact()

    print("\n" + "=" * 60)
    print("All demos complete.")
    print("=" * 60)
