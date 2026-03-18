# Proxy Pattern

## What is it?
A Proxy sits in front of another object and implements the same interface. When you call
a method on the proxy, it can check permissions, return a cached result, log the call,
or defer creating the real object — before (or instead of) forwarding to it. The caller
never knows there is a proxy in the way.

## Analogy
A bank teller is a proxy for the vault. You hand over a cheque (same interface as
depositing directly), but the teller checks your ID, records the transaction, and only
opens the vault when necessary. You never touch the vault yourself.

## Minimal code
```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> list: ...

class RealDatabase(Database):
    def query(self, sql: str) -> list:
        return [{"result": sql}]       # pretend this hits Postgres

class CachingProxy(Database):
    def __init__(self, real: Database) -> None:
        self._real = real
        self._cache: dict[str, list] = {}

    def query(self, sql: str) -> list:
        if sql not in self._cache:
            self._cache[sql] = self._real.query(sql)
        return self._cache[sql]        # second call skips the real DB

db = CachingProxy(RealDatabase())
db.query("SELECT 1")   # hits real DB
db.query("SELECT 1")   # served from cache
```

## Real-world uses
- Razorpay/Paytm wrap the actual payment processor with a protection proxy that
  validates the merchant ID and checks rate limits before forwarding the charge.
- Aadhaar e-KYC uses a protection proxy to enforce that only authorised agencies
  can trigger biometric lookups.
- Django's `SimpleLazyObject` is a virtual proxy that defers loading the logged-in
  user from the database until `request.user` is first accessed.

## One mistake
Changing the method signature in the proxy (e.g. adding a `user=` parameter that
the base interface doesn't have). This breaks the substitution guarantee — callers
typed against the abstract interface can no longer swap in the proxy transparently.
Keep signatures identical; pass extra context through a thread-local or constructor.

## What to do next
- See `examples/example1_virtual_proxy.py` for lazy image loading.
- See `examples/example2_caching_logging_proxy.py` for composing multiple proxies.
- Try `exercises/starter.py` — build three proxy types over a Database interface.
