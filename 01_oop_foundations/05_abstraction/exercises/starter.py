"""
WHAT YOU'RE BUILDING
--------------------
You are building a pluggable storage system.

There are two ways to store data:
  InMemoryStorage  — stores data in a Python dict (fast, lost when program ends)
  FileStorage      — stores data as files on disk (survives restarts)

DataRepository is a wrapper. It uses any storage backend.
The rest of the code only talks to DataRepository — it does not care which storage is used.

TIP: This same "plug in any backend" design appears in many real systems:
  - Logging (write to file, or to a database, or to the cloud)
  - Notifications (send via email, or SMS, or push notification)
  - Payment (Razorpay, Paytm, UPI — same interface, different implementations)

HOW TO RUN TESTS
    pytest tests.py -v
"""
import os
from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """
    The abstract interface. Any storage system must implement these 4 methods.
    You cannot create a StorageBackend directly — only its subclasses.
    """

    @abstractmethod
    def save(self, key: str, data: str) -> None:
        """Save data with the given key."""
        ...

    @abstractmethod
    def load(self, key: str) -> str:
        """
        Get data for the given key.
        Raises KeyError if the key does not exist.
        """
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove the key and its data."""
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Return True if the key exists, False if not."""
        ...


class InMemoryStorage(StorageBackend):
    """Stores data in a Python dict. Fast and simple."""

    def __init__(self) -> None:
        # TODO: Create an empty dict — save it as self._store
        # HINT: self._store = {}
        pass

    def save(self, key: str, data: str) -> None:
        # TODO: Save data in self._store using key
        # HINT: self._store[key] = data
        pass

    def load(self, key: str) -> str:
        # TODO: Return self._store[key]
        # If the key does not exist, Python will raise KeyError automatically — that is correct!
        pass

    def delete(self, key: str) -> None:
        # TODO: Remove the key from self._store if it exists
        # Do nothing if the key is not there (no error needed)
        # HINT: if key in self._store: del self._store[key]
        pass

    def exists(self, key: str) -> bool:
        # TODO: Return True if key is in self._store, False if not
        # HINT: return key in self._store   (one line!)
        pass


class FileStorage(StorageBackend):
    """Stores data as files on disk. Each key = one file."""

    def __init__(self, directory: str = "/tmp/lld_storage") -> None:
        # TODO: Save the directory path as self.directory
        # TODO: Create the directory if it does not exist
        # HINT: os.makedirs(directory, exist_ok=True)
        pass

    def _path(self, key: str) -> str:
        # TODO: Return the full file path for this key
        # HINT: return os.path.join(self.directory, key)
        pass

    def save(self, key: str, data: str) -> None:
        # TODO: Write data to the file at self._path(key)
        # HINT:
        #   with open(self._path(key), "w") as f:
        #       f.write(data)
        pass

    def load(self, key: str) -> str:
        # TODO: Read and return the contents of the file at self._path(key)
        # If the file does not exist, raise KeyError(key)
        # HINT:
        #   if not self.exists(key): raise KeyError(key)
        #   with open(self._path(key)) as f: return f.read()
        pass

    def delete(self, key: str) -> None:
        # TODO: Delete the file at self._path(key) if it exists
        # Do nothing if it does not exist
        # HINT: if self.exists(key): os.remove(self._path(key))
        pass

    def exists(self, key: str) -> bool:
        # TODO: Return True if the file exists, False if not
        # HINT: return os.path.exists(self._path(key))
        pass


class DataRepository:
    """
    A simple wrapper around any StorageBackend.

    The rest of your code uses DataRepository — not InMemoryStorage or FileStorage directly.
    This way you can switch the storage backend without changing anything else.

    TIP: This is called the Repository Pattern. You will see it in almost every
    large LLD problem (user repo, booking repo, product repo, etc.).
    """

    def __init__(self, backend: StorageBackend) -> None:
        # TODO: Save backend as self._backend
        # HINT: self._backend = backend
        pass

    def set(self, key: str, value: str) -> None:
        """Save a key-value pair."""
        # TODO: Call self._backend.save(key, value)
        pass

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get a value by key. Return default if the key does not exist."""
        # TODO: Try self._backend.load(key)
        # If KeyError is raised, return the default value instead
        # HINT:
        #   try:
        #       return self._backend.load(key)
        #   except KeyError:
        #       return default
        pass

    def remove(self, key: str) -> None:
        """Delete a key."""
        # TODO: Call self._backend.delete(key)
        pass

    def has(self, key: str) -> bool:
        """Check if a key exists."""
        # TODO: Call self._backend.exists(key) and return the result
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/05_abstraction/exercises/tests.py -v
#
# Run all OOP exercises at once:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/ -v
# =============================================================================
