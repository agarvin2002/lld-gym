# Explanation: Proxy Pattern — Database Proxy System

## The Core Insight

Without a proxy, every call site that needs caching, logging, or access control must implement it inline:

```python
# Without proxy — each call site is responsible for everything
def run_analytics():
    if current_user not in ALLOWED:          # auth duplicated everywhere
        raise PermissionError
    key = sql
    if key in _cache:                        # caching duplicated everywhere
        return _cache[key]
    log(f"querying: {key}")                  # logging duplicated everywhere
    result = real_db.query(key)
    _cache[key] = result
    return result
```

With the Proxy pattern, each concern lives in one class and the call site is a single line:

```python
# With proxy — call site is clean
def run_analytics():
    return db.query("SELECT ...")            # db is whatever proxy was injected
```

## Why Each Proxy Is Separate

### Single Responsibility

Each proxy handles exactly one cross-cutting concern:

| Proxy | Concern |
|-------|---------|
| `CachingDatabaseProxy` | Performance (avoid redundant I/O) |
| `LoggingDatabaseProxy` | Observability (audit trail) |
| `ProtectedDatabaseProxy` | Security (access control) |

Keeping them separate means you can test each in isolation and combine only what a given context needs.

### Open/Closed Principle

`RealDatabase` never changed.  We added caching, logging, and protection by writing new classes and composing them — no modification of existing code.

## The Composition Chain

```python
real      = RealDatabase("postgres://...")
cached    = CachingDatabaseProxy(real)        # layer 1
logged    = LoggingDatabaseProxy(cached)      # layer 2
protected = ProtectedDatabaseProxy(logged, allowed_users=["alice"])  # layer 3
```

Calling `protected.query("SELECT 1", user="alice")` triggers:

```
ProtectedDatabaseProxy.query("SELECT 1", user="alice")
    → user check passes
    → LoggingDatabaseProxy.query("SELECT 1")
        → appends to query_log
        → CachingDatabaseProxy.query("SELECT 1")
            → cache miss → RealDatabase.query("SELECT 1")
            → stores result
        → returns result
    → returns result
→ returns result
```

On the second call with the same SQL, the chain short-circuits at the caching layer — the real DB is never reached.

## Key Design Detail: Protection Proxy Signature

`ProtectedDatabaseProxy.query` accepts an extra `user` parameter that the `Database` ABC does not define:

```python
def query(self, sql: str, user: str = "") -> list[dict]:  # type: ignore[override]
```

This is intentional and the `# type: ignore[override]` comment is honest about it.  The protected proxy is designed to be the **outermost** layer — callers that know they need auth use it directly; inner layers only see `query(sql)`.

An alternative design would pass credentials via a context object (e.g., a thread-local) so the signature stays identical throughout the chain.  Both designs are valid; the explicit `user` parameter trades interface purity for readability.

## Why `clear_cache()` Resets `cache_hits`

When the cache is cleared, the hit counter becomes meaningless (it counted hits against entries that no longer exist).  Resetting it to zero gives callers a clean slate to measure the effectiveness of a freshly populated cache.

## Testing Strategy

```python
# Test caching in isolation
real = RealDatabase("sqlite://test.db")
proxy = CachingDatabaseProxy(real)

proxy.query("SELECT 1")
assert len(real._query_log) == 1   # real DB was called once

proxy.query("SELECT 1")
assert len(real._query_log) == 1   # real DB NOT called again
assert proxy.cache_hits == 1
```

The `_query_log` on `RealDatabase` is the key observability hook — it lets tests verify whether the real DB was actually reached without mocking.

## Takeaway

> The proxy is transparent to callers: they see only the `Database` interface.
> Cross-cutting behaviour (caching, logging, auth) is additive, composable, and independently testable.
