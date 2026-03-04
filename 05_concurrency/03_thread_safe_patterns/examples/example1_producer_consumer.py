"""
Producer-Consumer Pattern using queue.Queue
============================================
Demonstrates thread-safe data pipeline with:
- Multiple producers generating work items
- Multiple consumers processing those items
- Sentinel-based shutdown signaling
- Throughput measurement
"""

import queue
import threading
import time
import random


# ---------------------------------------------------------------------------
# Producer
# ---------------------------------------------------------------------------

class Producer(threading.Thread):
    """Generates numbered items and puts them on the shared queue.

    After producing all items, it places a sentinel (None) on the queue to
    signal that this producer is done. Each consumer needs one sentinel, so
    the caller must coordinate the right number of sentinels.
    """

    def __init__(self, producer_id: int, item_count: int, q: queue.Queue) -> None:
        super().__init__(name=f"Producer-{producer_id}", daemon=True)
        self.producer_id = producer_id
        self.item_count = item_count
        self.q = q
        self.produced = 0

    def run(self) -> None:
        for i in range(self.item_count):
            item = f"P{self.producer_id}-item-{i}"
            self.q.put(item)
            self.produced += 1
            # Simulate variable production speed
            time.sleep(random.uniform(0.001, 0.005))

        print(f"[{self.name}] Done — produced {self.produced} items")


# ---------------------------------------------------------------------------
# Consumer
# ---------------------------------------------------------------------------

class Consumer(threading.Thread):
    """Processes items from the shared queue until it receives a sentinel (None)."""

    def __init__(self, consumer_id: int, q: queue.Queue, results: list, lock: threading.Lock) -> None:
        super().__init__(name=f"Consumer-{consumer_id}", daemon=True)
        self.consumer_id = consumer_id
        self.q = q
        self.results = results      # shared list — write protected by lock
        self.lock = lock
        self.consumed = 0

    def _process(self, item: str) -> str:
        """Simulate processing work (e.g., transform/validate/store)."""
        time.sleep(random.uniform(0.002, 0.008))   # Simulate work
        return f"processed({item})"

    def run(self) -> None:
        while True:
            item = self.q.get()     # Blocks until an item is available

            if item is None:        # Sentinel — this consumer should stop
                self.q.task_done()
                print(f"[{self.name}] Received shutdown signal — consumed {self.consumed} items")
                break

            result = self._process(item)
            self.consumed += 1

            with self.lock:
                self.results.append(result)

            self.q.task_done()      # Signal that this item has been handled


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def run_pipeline(num_producers: int = 2, num_consumers: int = 3, items_per_producer: int = 20) -> None:
    print("=" * 60)
    print(f"Producer-Consumer Pipeline")
    print(f"  Producers : {num_producers}")
    print(f"  Consumers : {num_consumers}")
    print(f"  Items/producer: {items_per_producer}")
    print(f"  Total items   : {num_producers * items_per_producer}")
    print("=" * 60)

    q: queue.Queue = queue.Queue(maxsize=50)   # Bounded queue prevents unbounded memory use
    results: list = []
    results_lock = threading.Lock()

    # --- Start consumers first so they are ready when producers push items ---
    consumers = [
        Consumer(i + 1, q, results, results_lock)
        for i in range(num_consumers)
    ]
    for c in consumers:
        c.start()

    # --- Start producers ---
    start_time = time.perf_counter()

    producers = [
        Producer(i + 1, items_per_producer, q)
        for i in range(num_producers)
    ]
    for p in producers:
        p.start()

    # --- Wait for all producers to finish ---
    for p in producers:
        p.join()

    print("\n[Main] All producers finished. Sending shutdown sentinels...")

    # One sentinel per consumer — each consumer will stop on its own sentinel
    for _ in range(num_consumers):
        q.put(None)

    # --- Wait for all consumers to drain the queue ---
    q.join()   # Blocks until every item has had task_done() called

    for c in consumers:
        c.join()

    elapsed = time.perf_counter() - start_time

    # --- Report ---
    total_expected = num_producers * items_per_producer
    total_processed = len(results)

    print("\n" + "=" * 60)
    print("Pipeline complete")
    print(f"  Expected items  : {total_expected}")
    print(f"  Processed items : {total_processed}")
    print(f"  Items match     : {total_expected == total_processed}")
    print(f"  Elapsed time    : {elapsed:.3f}s")
    print(f"  Throughput      : {total_processed / elapsed:.1f} items/sec")
    print("=" * 60)

    # Spot-check a few results
    print("\nSample results (first 5):")
    for r in results[:5]:
        print(f"  {r}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Default demo: 2 producers, 3 consumers, 20 items each
    run_pipeline(num_producers=2, num_consumers=3, items_per_producer=20)

    print()

    # Scale-up demo: 4 producers, 2 consumers, 30 items each
    run_pipeline(num_producers=4, num_consumers=2, items_per_producer=30)
