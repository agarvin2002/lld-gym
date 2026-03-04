"""
Solution: Pluggable Storage System
"""
import os
from abc import ABC, abstractmethod


class StorageBackend(ABC):
    @abstractmethod
    def save(self, key: str, data: str) -> None: ...

    @abstractmethod
    def load(self, key: str) -> str: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def exists(self, key: str) -> bool: ...


class InMemoryStorage(StorageBackend):
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def save(self, key: str, data: str) -> None:
        self._store[key] = data

    def load(self, key: str) -> str:
        if key not in self._store:
            raise KeyError(f"Key not found: {key!r}")
        return self._store[key]

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def exists(self, key: str) -> bool:
        return key in self._store


class FileStorage(StorageBackend):
    def __init__(self, directory: str = "/tmp/lld_storage") -> None:
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def _path(self, key: str) -> str:
        return os.path.join(self.directory, key)

    def save(self, key: str, data: str) -> None:
        with open(self._path(key), "w") as f:
            f.write(data)

    def load(self, key: str) -> str:
        try:
            with open(self._path(key)) as f:
                return f.read()
        except FileNotFoundError:
            raise KeyError(f"Key not found: {key!r}")

    def delete(self, key: str) -> None:
        try:
            os.remove(self._path(key))
        except FileNotFoundError:
            pass

    def exists(self, key: str) -> bool:
        return os.path.exists(self._path(key))


class DataRepository:
    def __init__(self, backend: StorageBackend) -> None:
        self._backend = backend

    def set(self, key: str, value: str) -> None:
        self._backend.save(key, value)

    def get(self, key: str, default: str | None = None) -> str | None:
        try:
            return self._backend.load(key)
        except KeyError:
            return default

    def remove(self, key: str) -> None:
        self._backend.delete(key)

    def has(self, key: str) -> bool:
        return self._backend.exists(key)
