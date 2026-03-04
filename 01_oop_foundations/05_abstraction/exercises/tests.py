"""
Tests for the Storage System exercise.
Run: pytest tests.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import StorageBackend, InMemoryStorage, FileStorage, DataRepository


class TestStorageBackendABC:
    def test_cannot_instantiate_abstract_backend(self):
        with pytest.raises(TypeError):
            StorageBackend()


class TestInMemoryStorage:
    def setup_method(self):
        self.storage = InMemoryStorage()

    def test_save_and_load(self):
        self.storage.save("key1", "hello")
        assert self.storage.load("key1") == "hello"

    def test_load_missing_raises_key_error(self):
        with pytest.raises(KeyError):
            self.storage.load("nonexistent")

    def test_exists_returns_true_after_save(self):
        self.storage.save("key1", "data")
        assert self.storage.exists("key1") is True

    def test_exists_returns_false_for_missing(self):
        assert self.storage.exists("missing") is False

    def test_delete_removes_key(self):
        self.storage.save("key1", "data")
        self.storage.delete("key1")
        assert self.storage.exists("key1") is False

    def test_delete_missing_key_does_not_raise(self):
        self.storage.delete("nonexistent")  # should not raise


class TestFileStorage:
    def setup_method(self, tmp_path=None):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.storage = FileStorage(directory=self.tmpdir)

    def test_save_and_load(self):
        self.storage.save("testkey", "testdata")
        assert self.storage.load("testkey") == "testdata"

    def test_load_missing_raises_key_error(self):
        with pytest.raises(KeyError):
            self.storage.load("nofile")

    def test_exists_after_save(self):
        self.storage.save("k", "v")
        assert self.storage.exists("k") is True

    def test_exists_returns_false_for_missing(self):
        assert self.storage.exists("missing") is False

    def test_delete_removes_file(self):
        self.storage.save("k", "v")
        self.storage.delete("k")
        assert self.storage.exists("k") is False


class TestDataRepository:
    def setup_method(self):
        self.repo = DataRepository(InMemoryStorage())

    def test_set_and_get(self):
        self.repo.set("name", "Alice")
        assert self.repo.get("name") == "Alice"

    def test_get_default_for_missing_key(self):
        assert self.repo.get("missing") is None
        assert self.repo.get("missing", "default") == "default"

    def test_has_returns_true_after_set(self):
        self.repo.set("x", "1")
        assert self.repo.has("x") is True

    def test_has_returns_false_for_missing(self):
        assert self.repo.has("nope") is False

    def test_remove_deletes_key(self):
        self.repo.set("x", "1")
        self.repo.remove("x")
        assert self.repo.has("x") is False

    def test_can_swap_backends(self):
        """Repository works identically with any backend."""
        import tempfile
        file_repo = DataRepository(FileStorage(directory=tempfile.mkdtemp()))
        file_repo.set("key", "value")
        assert file_repo.get("key") == "value"
