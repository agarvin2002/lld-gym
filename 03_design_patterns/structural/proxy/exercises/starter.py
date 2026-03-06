"""Proxy Pattern Exercise — Reference Solution.

Three proxy types around a Database interface:
  CachingDatabaseProxy   — avoids redundant queries
  LoggingDatabaseProxy   — records every SQL string
  ProtectedDatabaseProxy — enforces user-based access control
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Subject interface
# ---------------------------------------------------------------------------

class Database(ABC):
    """Abstract interface that all database objects must implement."""

    @abstractmethod
    def query(self, sql: str) -> list[dict]:
        """Execute *sql* and return a list of row dicts."""
        ...


# ---------------------------------------------------------------------------
# Real Subject
# ---------------------------------------------------------------------------

class RealDatabase(Database):
    """Simulates a real database connection.

    query() returns mock data and records every SQL string in _query_log so
    tests can verify whether the real DB was actually called.
    """

    def __init__(self, connection_string: str) -> None:
        """Initialise with a connection string and an empty query log."""
        self._connection_string = connection_string
        self._query_log: list[str] = []

    def query(self, sql: str) -> list[dict]:
        """Return mock data ``[{'result': sql}]`` and record the query."""
        self._query_log.append(sql)
        return [{'result': sql}]


# ---------------------------------------------------------------------------
# Proxy 1: Caching
# ---------------------------------------------------------------------------

class CachingDatabaseProxy(Database):
    """Caches query results so identical SQL strings skip the real database.

    The first call for a given SQL string is forwarded to the wrapped
    ``RealDatabase``.  Every subsequent call with the same string returns
    the stored result and increments ``cache_hits``.
    """

    def __init__(self, real: RealDatabase) -> None:
        """Wrap *real* and initialise an empty cache."""
        self._real = real
        self._cache: dict[str, list[dict]] = {}
        self._cache_hits: int = 0

    def query(self, sql: str) -> list[dict]:
        """Return cached result if available; otherwise forward to real DB."""
        if sql in self._cache:
            self._cache_hits += 1
            return self._cache[sql]
        result = self._real.query(sql)
        self._cache[sql] = result
        return result

    @property
    def cache_hits(self) -> int:
        """Number of times a cached result was returned instead of querying the DB."""
        return self._cache_hits

    @property
    def cache_size(self) -> int:
        """Number of distinct SQL strings currently in the cache."""
        return len(self._cache)

    def clear_cache(self) -> None:
        """Empty the cache and reset the hit counter to zero."""
        self._cache.clear()
        self._cache_hits = 0


# ---------------------------------------------------------------------------
# Proxy 2: Logging
# ---------------------------------------------------------------------------

class LoggingDatabaseProxy(Database):
    """Records every SQL query before delegating to the wrapped database.

    The wrapped database may be a ``RealDatabase`` or another proxy,
    enabling composable proxy chains.
    """

    def __init__(self, db: Database) -> None:
        """Wrap *db* (any ``Database``) and initialise an empty query log."""
        self._db = db
        self.query_log: list[str] = []

    def query(self, sql: str) -> list[dict]:
        """Append *sql* to ``query_log``, delegate, and return the result."""
        self.query_log.append(sql)
        return self._db.query(sql)


# ---------------------------------------------------------------------------
# Proxy 3: Protection
# ---------------------------------------------------------------------------

class ProtectedDatabaseProxy(Database):
    """Allows only users in *allowed_users* to execute queries.

    Any call from an unrecognised user raises ``PermissionError`` before
    the wrapped database is ever contacted.
    """

    def __init__(self, db: Database, allowed_users: list[str]) -> None:
        """Wrap *db* and store the set of permitted user names."""
        self._db = db
        self._allowed: set[str] = set(allowed_users)

    def query(self, sql: str, user: str = "") -> list[dict]:  # type: ignore[override]
        """Raise ``PermissionError`` if *user* is not allowed; else delegate.

        The wrapped database is called with ``query(sql)`` — the ``user``
        argument is consumed here and not forwarded downstream.
        """
        if user not in self._allowed:
            raise PermissionError(
                f"User {user!r} is not authorised to query this database."
            )
        return self._db.query(sql)
