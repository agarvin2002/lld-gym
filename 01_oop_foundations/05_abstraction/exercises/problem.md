# Exercise: Pluggable Storage System

## What You'll Build

A storage abstraction layer where the `DataRepository` works with any storage backend — memory, file system, or anything else — without knowing the implementation details.

## Classes

### `StorageBackend` (ABC)
- `save(key: str, data: str) -> None`
- `load(key: str) -> str` — raises `KeyError` if key not found
- `delete(key: str) -> None`
- `exists(key: str) -> bool`

### `InMemoryStorage(StorageBackend)`
- Backed by a Python `dict`
- All operations are O(1)

### `FileStorage(StorageBackend)`
- Each key maps to a file in a directory (configurable, default `/tmp/lld_storage/`)
- Key is used as filename (sanitize for safety)
- `load()` raises `KeyError` if file doesn't exist

### `DataRepository`
- Constructor: `__init__(backend: StorageBackend)`
- `set(key: str, value: str) -> None`
- `get(key: str, default: str | None = None) -> str | None` — returns default if not found
- `remove(key: str) -> None`
- `has(key: str) -> bool`

## Constraints
- `StorageBackend` must be a true ABC — instantiating it directly must raise `TypeError`
- `DataRepository` must accept **any** `StorageBackend` implementation
- `FileStorage` must create its directory if it doesn't exist

## Hints
1. `os.makedirs(self.directory, exist_ok=True)` in `FileStorage.__init__`
2. `os.path.join(self.directory, key)` to build file path
3. `DataRepository.get()` should catch `KeyError` and return default

## What You'll Practice
- Abstract base classes as contracts
- Dependency injection (passing backend to repository)
- How abstraction enables swapping implementations
- Why this pattern makes testing easy (swap in InMemoryStorage for tests)
