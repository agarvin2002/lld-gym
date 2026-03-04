# Explanation: Pluggable Storage System

## The Core Idea: Depend on Abstractions

`DataRepository` doesn't know or care whether it's talking to memory, files, a database, or Redis. It only knows the `StorageBackend` contract. This is the heart of abstraction.

```python
# Works identically — DataRepository doesn't change
repo1 = DataRepository(InMemoryStorage())
repo2 = DataRepository(FileStorage("/tmp/myapp"))
```

## Why ABC Over Duck Typing Here

Python supports duck typing — you could use `FileStorage` without it inheriting `StorageBackend`. But the ABC adds value:
1. **Documentation**: the ABC is the canonical list of required methods
2. **Early error**: missing a method raises `TypeError` at instantiation, not at the first call
3. **IDE support**: type hints on `DataRepository.__init__` enable autocomplete

## Testability Through Abstraction

In tests, you use `InMemoryStorage` everywhere:
```python
# No files, no disk, no cleanup — fast and isolated
repo = DataRepository(InMemoryStorage())
```

In production:
```python
repo = DataRepository(FileStorage("/var/myapp/data"))
```

Same code, different behavior. This is **dependency injection** — you inject the dependency rather than creating it inside.

## Protocol Alternative (Python 3.8+)

Instead of ABC, you could use `typing.Protocol`:
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class StorageBackend(Protocol):
    def save(self, key: str, data: str) -> None: ...
    def load(self, key: str) -> str: ...
    def delete(self, key: str) -> None: ...
    def exists(self, key: str) -> bool: ...
```
Advantage: no explicit inheritance needed — any class with the right methods qualifies. This is called **structural subtyping** (duck typing with type hints).

## Real-World Applications
- Django ORM backends (FileSystemStorage, S3Boto3Storage, etc.)
- Python's `io` module (BytesIO, StringIO, FileIO all implement the same interface)
- Cache backends in web frameworks
