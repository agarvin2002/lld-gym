"""
WHAT YOU'RE BUILDING
====================
Three proxy types that all wrap a Database interface:

  CachingDatabaseProxy   — return stored results for repeated SQL queries
                           so the real database is only called once per query.
  LoggingDatabaseProxy   — record every SQL string before forwarding it
                           so you have a full audit trail.
  ProtectedDatabaseProxy — allow only users in an approved list to run queries;
                           raise PermissionError for everyone else.

The abstract base class (Database) and the real implementation (RealDatabase)
are already complete. You only need to implement the three proxy classes.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Subject interface — DO NOT MODIFY
# ---------------------------------------------------------------------------

class Database(ABC):
    """Abstract interface that all database objects must implement."""

    @abstractmethod
    def query(self, sql: str) -> list[dict]:
        """Execute *sql* and return a list of row dicts."""
        ...


# ---------------------------------------------------------------------------
# Real Subject — DO NOT MODIFY
# ---------------------------------------------------------------------------

class RealDatabase(Database):
    """Simulates a real database connection.

    query() returns mock data and records every SQL string in _query_log so
    tests can verify whether the real DB was actually called.
    """

    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._query_log: list[str] = []

    def query(self, sql: str) -> list[dict]:
        """Return mock data ``[{'result': sql}]`` and record the query."""
        self._query_log.append(sql)
        return [{'result': sql}]


# ---------------------------------------------------------------------------
# Proxy 1: Caching — implement this class
# ---------------------------------------------------------------------------

class CachingDatabaseProxy(Database):
    """Caches query results so identical SQL strings skip the real database."""

    def __init__(self, real: RealDatabase) -> None:
        # TODO: Store the real database as self._real
        # TODO: Create an empty cache dict: self._cache = {}
        # TODO: Set a hit counter: self._cache_hits = 0
        pass

    def query(self, sql: str) -> list[dict]:
        """Return cached result if available; otherwise forward to real DB."""
        # TODO: If sql is in self._cache, increment self._cache_hits and return the cached value.
        # TODO: Otherwise, call self._real.query(sql), store the result in the cache, then return it.
        # HINT: self._cache is a dict[str, list[dict]] — key is the SQL string, value is the result.
        pass

    @property
    def cache_hits(self) -> int:
        """Number of times a cached result was returned instead of querying the DB."""
        # TODO: Return self._cache_hits
        pass

    @property
    def cache_size(self) -> int:
        """Number of distinct SQL strings currently in the cache."""
        # TODO: Return len(self._cache)
        pass

    def clear_cache(self) -> None:
        """Empty the cache and reset the hit counter to zero."""
        # TODO: Clear self._cache and reset self._cache_hits to 0
        pass


# ---------------------------------------------------------------------------
# Proxy 2: Logging — implement this class
# ---------------------------------------------------------------------------

class LoggingDatabaseProxy(Database):
    """Records every SQL query before delegating to the wrapped database."""

    def __init__(self, db: Database) -> None:
        # TODO: Store the wrapped database as self._db
        # TODO: Create an empty list: self.query_log = []
        # HINT: Note the attribute is self.query_log (public), not self._query_log.
        pass

    def query(self, sql: str) -> list[dict]:
        """Append *sql* to query_log, delegate, and return the result."""
        # TODO: Add sql to self.query_log.
        # TODO: Forward the call to self._db.query(sql) and return the result.
        pass


# ---------------------------------------------------------------------------
# Proxy 3: Protection — implement this class
# ---------------------------------------------------------------------------

class ProtectedDatabaseProxy(Database):
    """Allows only users in *allowed_users* to execute queries."""

    def __init__(self, db: Database, allowed_users: list[str]) -> None:
        # TODO: Store the wrapped database as self._db
        # TODO: Store allowed_users as a set: self._allowed = set(allowed_users)
        pass

    def query(self, sql: str, user: str = "") -> list[dict]:  # type: ignore[override]
        """Raise PermissionError if *user* is not allowed; else delegate."""
        # TODO: If user is not in self._allowed, raise PermissionError.
        # TODO: Otherwise, forward to self._db.query(sql) and return the result.
        # HINT: Do NOT pass user downstream — call self._db.query(sql) (no user argument).
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/structural/proxy/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
