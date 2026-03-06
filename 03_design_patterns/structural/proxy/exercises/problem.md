# Exercise: Database Proxy System (Proxy Pattern)

## Problem

Build a proxy system around a `Database` interface to add caching, logging, and access control without modifying the real database class.

## What to build

### `Database` (ABC)
- `query(sql: str) -> list[dict]` — execute a SQL string and return rows as dicts

### `RealDatabase`
- `__init__(self, connection_string: str)` — stores the connection string
- `query(sql: str) -> list[dict]` — returns `[{'result': sql}]` (mock data) and appends `sql` to an internal `_query_log: list[str]`

### `CachingDatabaseProxy(Database)`
- Wraps a `RealDatabase` instance
- First call with a given SQL string forwards to the real DB and stores the result
- Subsequent calls with the **same** SQL return the cached result without touching the real DB
- `cache_hits` property — number of times the cache was used
- `cache_size` property — number of distinct queries cached
- `clear_cache()` method — empties the cache and resets `cache_hits` to 0

### `LoggingDatabaseProxy(Database)`
- Wraps **any** `Database` (could be `RealDatabase` or another proxy)
- Records every SQL string in `query_log: list[str]` before delegating
- Delegates to wrapped database and returns the result unchanged

### `ProtectedDatabaseProxy(Database)`
- Wraps **any** `Database`
- `__init__(self, db: Database, allowed_users: list[str])`
- `query(self, sql: str, user: str) -> list[dict]` — if `user` not in `allowed_users`, raise `PermissionError`; otherwise delegate to wrapped DB calling `query(sql)` (without the user argument)

## Constraints
- No external dependencies — stdlib only
- Each proxy class must implement `Database` (the ABC)
- `ProtectedDatabaseProxy.query` takes an extra `user` parameter (type-ignored override is acceptable)

## Run tests
```bash
/tmp/lld_venv/bin/pytest exercises/tests.py -v
```

## Hints
- `CachingDatabaseProxy` should store results in a `dict[str, list[dict]]`
- `LoggingDatabaseProxy` only needs a `list[str]` for the log
- For `ProtectedDatabaseProxy`, after checking the user, call `self._db.query(sql)` (not `query(sql, user)`)
