"""
Exercise: Pluggable Storage System

Fill in the TODOs. Run tests with: pytest tests.py -v
"""
import os
from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """
    Abstract interface for storage implementations.
    Any class that implements save, load, delete, exists can be used.
    """

    @abstractmethod
    def save(self, key: str, data: str) -> None:
        """Persist data under the given key."""
        ...

    @abstractmethod
    def load(self, key: str) -> str:
        """
        Retrieve data for the given key.

        Raises:
            KeyError: if key does not exist
        """
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove the key and its data."""
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Return True if key exists, False otherwise."""
        ...


class InMemoryStorage(StorageBackend):
    """Dict-backed in-memory storage. Fast and test-friendly."""

    def __init__(self) -> None:
        # TODO: initialize an empty dict self._store
        pass

    def save(self, key: str, data: str) -> None:
        # TODO: store data in self._store[key]
        pass

    def load(self, key: str) -> str:
        # TODO: return self._store[key], raise KeyError if missing
        pass

    def delete(self, key: str) -> None:
        # TODO: remove key from store (ignore if missing)
        pass

    def exists(self, key: str) -> bool:
        # TODO: return True if key is in store
        pass


class FileStorage(StorageBackend):
    """File-system backed storage. Each key = one file."""

    def __init__(self, directory: str = "/tmp/lld_storage") -> None:
        # TODO: store directory, create it if it doesn't exist
        pass

    def _path(self, key: str) -> str:
        # TODO: return os.path.join(self.directory, key)
        pass

    def save(self, key: str, data: str) -> None:
        # TODO: write data to file at self._path(key)
        pass

    def load(self, key: str) -> str:
        # TODO: read and return file contents, raise KeyError if file missing
        pass

    def delete(self, key: str) -> None:
        # TODO: remove file at self._path(key), ignore if missing
        pass

    def exists(self, key: str) -> bool:
        # TODO: return os.path.exists(self._path(key))
        pass


class DataRepository:
    """
    High-level interface over any StorageBackend.
    Accepts any object that implements StorageBackend.
    """

    def __init__(self, backend: StorageBackend) -> None:
        # TODO: store the backend
        pass

    def set(self, key: str, value: str) -> None:
        """Save key-value pair."""
        # TODO: delegate to backend.save()
        pass

    def get(self, key: str, default: str | None = None) -> str | None:
        """Retrieve value, or return default if not found."""
        # TODO: try backend.load(), catch KeyError and return default
        pass

    def remove(self, key: str) -> None:
        """Delete a key."""
        # TODO: delegate to backend.delete()
        pass

    def has(self, key: str) -> bool:
        """Check if key exists."""
        # TODO: delegate to backend.exists()
        pass
