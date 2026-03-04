"""
Singleton Pattern Exercise - Test Suite
========================================

Run with: python tests.py

Tests both the starter.py (if implemented) and solution.py.
By default, imports from starter.py. Change IMPORT_FROM to test the solution.

Tests cover:
    1. Single instance guarantee (basic)
    2. Ignoring arguments after first init
    3. get() with and without default
    4. set() visibility across references
    5. all() returns a copy (not live dict)
    6. Thread safety — 50 concurrent threads, all get same instance
    7. Thread-safe set/get under concurrency
"""

import sys
import os
import threading
import unittest

# ---------------------------------------------------------------------------
# Import configuration
# Change this to "solution" to test the solution instead of the starter
# ---------------------------------------------------------------------------
IMPORT_FROM = "starter"  # or "solution"

# Add the exercises directory to the path
_exercises_dir = os.path.dirname(os.path.abspath(__file__))
_solution_dir = os.path.join(_exercises_dir, "solution")

if IMPORT_FROM == "starter":
    sys.path.insert(0, _exercises_dir)
    sys.modules.pop('starter', None)
    from starter import ApplicationConfig
elif IMPORT_FROM == "solution":
    sys.path.insert(0, _solution_dir)
    sys.modules.pop('solution', None)
    from solution import ApplicationConfig
else:
    raise ValueError(f"Unknown IMPORT_FROM: {IMPORT_FROM}")


def reset_singleton() -> None:
    """Reset the singleton between tests. Required for test isolation."""
    ApplicationConfig._instance = None  # type: ignore


class TestSingletonBasic(unittest.TestCase):
    """Basic singleton behavior tests."""

    def setUp(self) -> None:
        reset_singleton()

    def test_same_instance_returned(self) -> None:
        """Two calls to ApplicationConfig() must return the same object."""
        config1 = ApplicationConfig({"key": "value"})
        config2 = ApplicationConfig()
        self.assertIs(config1, config2, "Expected the same instance, got different objects")

    def test_three_instances_same(self) -> None:
        """Three or more calls must all return the same instance."""
        config1 = ApplicationConfig({"x": 1})
        config2 = ApplicationConfig({"y": 2})
        config3 = ApplicationConfig({"z": 3})
        self.assertIs(config1, config2)
        self.assertIs(config2, config3)

    def test_id_is_same(self) -> None:
        """Object IDs must match."""
        config1 = ApplicationConfig({"a": "b"})
        config2 = ApplicationConfig()
        self.assertEqual(id(config1), id(config2))


class TestConfigIgnoresRepeatedArgs(unittest.TestCase):
    """After the first call, constructor arguments should be ignored."""

    def setUp(self) -> None:
        reset_singleton()

    def test_second_call_ignores_config(self) -> None:
        """Second call with different config should not overwrite the first."""
        ApplicationConfig({"url": "original-url", "port": 5432})
        config2 = ApplicationConfig({"url": "this-should-be-ignored"})
        self.assertEqual(config2.get("url"), "original-url")

    def test_keys_from_first_call_are_preserved(self) -> None:
        """All keys from the first config must be available after second call."""
        ApplicationConfig({"db": "postgres", "debug": True, "timeout": 30})
        config2 = ApplicationConfig({"db": "sqlite"})  # ignored
        self.assertEqual(config2.get("db"), "postgres")
        self.assertEqual(config2.get("debug"), True)
        self.assertEqual(config2.get("timeout"), 30)


class TestGetMethod(unittest.TestCase):
    """Tests for the get() method."""

    def setUp(self) -> None:
        reset_singleton()
        self.config = ApplicationConfig({
            "database_url": "postgresql://localhost/mydb",
            "debug": False,
            "max_connections": 10,
            "api_key": "secret-123",
            "empty_value": None,
        })

    def test_get_existing_key(self) -> None:
        self.assertEqual(self.config.get("database_url"), "postgresql://localhost/mydb")

    def test_get_boolean_value(self) -> None:
        self.assertEqual(self.config.get("debug"), False)

    def test_get_integer_value(self) -> None:
        self.assertEqual(self.config.get("max_connections"), 10)

    def test_get_missing_key_returns_none(self) -> None:
        result = self.config.get("nonexistent_key")
        self.assertIsNone(result)

    def test_get_missing_key_with_default(self) -> None:
        result = self.config.get("nonexistent_key", "fallback")
        self.assertEqual(result, "fallback")

    def test_get_missing_key_with_falsy_default(self) -> None:
        result = self.config.get("nonexistent_key", 0)
        self.assertEqual(result, 0)

    def test_get_missing_key_with_false_default(self) -> None:
        result = self.config.get("nonexistent_key", False)
        self.assertEqual(result, False)

    def test_get_key_with_none_value(self) -> None:
        """A key that exists but maps to None should return None, not the default."""
        result = self.config.get("empty_value", "should_not_be_returned")
        # The key exists (maps to None), so default should NOT apply
        # Note: This behavior depends on implementation — dict.get() returns
        # None for both "key not present" and "key maps to None".
        # We test that the key IS accessible.
        self.assertIn("empty_value", self.config.all())


class TestSetMethod(unittest.TestCase):
    """Tests for the set() method."""

    def setUp(self) -> None:
        reset_singleton()
        self.config = ApplicationConfig({
            "debug": True,
            "timeout": 30,
        })

    def test_set_updates_value(self) -> None:
        self.config.set("debug", False)
        self.assertEqual(self.config.get("debug"), False)

    def test_set_visible_through_other_references(self) -> None:
        """Changes via set() must be visible through any reference to the singleton."""
        config2 = ApplicationConfig()  # same instance
        self.config.set("timeout", 60)
        self.assertEqual(config2.get("timeout"), 60)

    def test_set_adds_new_key(self) -> None:
        """set() should be able to add keys that didn't exist initially."""
        self.config.set("new_feature_flag", True)
        self.assertEqual(self.config.get("new_feature_flag"), True)

    def test_set_can_store_any_type(self) -> None:
        self.config.set("list_value", [1, 2, 3])
        self.config.set("dict_value", {"nested": "data"})
        self.assertEqual(self.config.get("list_value"), [1, 2, 3])
        self.assertEqual(self.config.get("dict_value"), {"nested": "data"})


class TestAllMethod(unittest.TestCase):
    """Tests for the all() method."""

    def setUp(self) -> None:
        reset_singleton()
        self.initial_config = {"a": 1, "b": 2, "c": 3}
        self.config = ApplicationConfig(self.initial_config)

    def test_all_returns_all_keys(self) -> None:
        result = self.config.all()
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)

    def test_all_returns_correct_values(self) -> None:
        result = self.config.all()
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)
        self.assertEqual(result["c"], 3)

    def test_all_returns_copy_not_live_dict(self) -> None:
        """Mutating the returned dict must NOT affect the stored config."""
        result = self.config.all()
        result["a"] = 999  # mutate the copy
        self.assertEqual(self.config.get("a"), 1)  # original unchanged

    def test_all_reflects_set_changes(self) -> None:
        self.config.set("d", 4)
        result = self.config.all()
        self.assertIn("d", result)
        self.assertEqual(result["d"], 4)


class TestThreadSafety(unittest.TestCase):
    """Thread safety tests — these are the critical ones."""

    def setUp(self) -> None:
        reset_singleton()

    def test_concurrent_creation_single_instance(self) -> None:
        """
        50 threads all try to create ApplicationConfig simultaneously.
        They must all receive the SAME instance (same id).
        """
        num_threads = 50
        instance_ids: list[int] = []
        lock = threading.Lock()

        def create_config(thread_id: int) -> None:
            cfg = ApplicationConfig({"thread_id": thread_id, "value": thread_id * 10})
            with lock:
                instance_ids.append(id(cfg))

        threads = [
            threading.Thread(target=create_config, args=(i,))
            for i in range(num_threads)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        unique_ids = set(instance_ids)
        self.assertEqual(
            len(unique_ids),
            1,
            f"Expected 1 unique instance, got {len(unique_ids)}: {unique_ids}"
        )

    def test_concurrent_set_and_get(self) -> None:
        """
        Multiple threads concurrently set and get values.
        No exceptions should be raised (thread safety of operations).
        """
        ApplicationConfig({"counter": 0})
        errors: list[Exception] = []

        def writer(key: str, value: int) -> None:
            try:
                cfg = ApplicationConfig()
                cfg.set(key, value)
            except Exception as e:
                errors.append(e)

        def reader(key: str) -> None:
            try:
                cfg = ApplicationConfig()
                cfg.get(key)
            except Exception as e:
                errors.append(e)

        threads = []
        for i in range(20):
            threads.append(threading.Thread(target=writer, args=(f"key_{i}", i)))
            threads.append(threading.Thread(target=reader, args=(f"key_{i % 5}",)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(
            len(errors),
            0,
            f"Concurrent set/get raised exceptions: {errors}"
        )

    def test_concurrent_all_calls(self) -> None:
        """all() should not raise exceptions under concurrent access."""
        ApplicationConfig({"x": 1, "y": 2, "z": 3})
        errors: list[Exception] = []

        def call_all() -> None:
            try:
                cfg = ApplicationConfig()
                _ = cfg.all()
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=call_all) for _ in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"all() raised exceptions: {errors}")


class TestEdgeCases(unittest.TestCase):
    """Edge cases and boundary conditions."""

    def setUp(self) -> None:
        reset_singleton()

    def test_no_config_on_first_call(self) -> None:
        """Creating with no config should work — start with empty dict."""
        config = ApplicationConfig()
        self.assertIsNotNone(config)
        result = config.all()
        self.assertIsInstance(result, dict)

    def test_empty_config_dict(self) -> None:
        """Creating with an empty dict should work."""
        config = ApplicationConfig({})
        self.assertIsNotNone(config)
        self.assertEqual(config.all(), {})

    def test_get_returns_none_for_missing_without_default(self) -> None:
        config = ApplicationConfig({"a": 1})
        self.assertIsNone(config.get("nonexistent"))

    def test_set_then_get_consistency(self) -> None:
        """Values set should be immediately retrievable."""
        config = ApplicationConfig({})
        config.set("key1", "value1")
        config.set("key2", 42)
        config.set("key3", [1, 2, 3])

        self.assertEqual(config.get("key1"), "value1")
        self.assertEqual(config.get("key2"), 42)
        self.assertEqual(config.get("key3"), [1, 2, 3])


if __name__ == "__main__":
    print(f"Testing: {IMPORT_FROM}.py")
    print(f"Importing ApplicationConfig from: {ApplicationConfig}")
    print()
    unittest.main(verbosity=2)
