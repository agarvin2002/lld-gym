"""Tests for Proxy Pattern — Database Proxy System."""
import sys, os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    Database,
    RealDatabase,
    CachingDatabaseProxy,
    LoggingDatabaseProxy,
    ProtectedDatabaseProxy,
)


# ---------------------------------------------------------------------------
# RealDatabase
# ---------------------------------------------------------------------------

class TestRealDatabase:
    def test_query_returns_list_with_result_dict(self):
        db = RealDatabase("sqlite://test.db")
        result = db.query("SELECT 1")
        assert result == [{'result': 'SELECT 1'}]

    def test_query_records_sql_in_query_log(self):
        db = RealDatabase("sqlite://test.db")
        db.query("SELECT 1")
        db.query("SELECT 2")
        assert "SELECT 1" in db._query_log
        assert "SELECT 2" in db._query_log

    def test_query_log_grows_with_each_call(self):
        db = RealDatabase("sqlite://test.db")
        for i in range(5):
            db.query(f"SELECT {i}")
        assert len(db._query_log) == 5

    def test_is_database_subclass(self):
        assert issubclass(RealDatabase, Database)


# ---------------------------------------------------------------------------
# CachingDatabaseProxy
# ---------------------------------------------------------------------------

class TestCachingDatabaseProxy:
    def setup_method(self):
        self.real = RealDatabase("sqlite://test.db")
        self.proxy = CachingDatabaseProxy(self.real)

    def test_first_query_hits_real_database(self):
        self.proxy.query("SELECT name FROM users")
        assert len(self.real._query_log) == 1

    def test_second_identical_query_does_not_hit_real_database(self):
        self.proxy.query("SELECT name FROM users")
        self.proxy.query("SELECT name FROM users")
        # Real DB should only have been called once
        assert len(self.real._query_log) == 1

    def test_cache_hit_count_increments_on_repeated_query(self):
        self.proxy.query("SELECT *")
        assert self.proxy.cache_hits == 0
        self.proxy.query("SELECT *")
        assert self.proxy.cache_hits == 1
        self.proxy.query("SELECT *")
        assert self.proxy.cache_hits == 2

    def test_different_queries_both_hit_real_database(self):
        self.proxy.query("SELECT 1")
        self.proxy.query("SELECT 2")
        assert len(self.real._query_log) == 2

    def test_cache_size_reflects_distinct_queries(self):
        self.proxy.query("SELECT 1")
        self.proxy.query("SELECT 2")
        self.proxy.query("SELECT 1")  # duplicate
        assert self.proxy.cache_size == 2

    def test_cache_returns_correct_result(self):
        first = self.proxy.query("SELECT 42")
        second = self.proxy.query("SELECT 42")
        assert first == second == [{'result': 'SELECT 42'}]

    def test_clear_cache_empties_cache(self):
        self.proxy.query("SELECT 1")
        self.proxy.query("SELECT 2")
        self.proxy.clear_cache()
        assert self.proxy.cache_size == 0

    def test_clear_cache_resets_hit_count(self):
        self.proxy.query("SELECT 1")
        self.proxy.query("SELECT 1")
        self.proxy.clear_cache()
        assert self.proxy.cache_hits == 0

    def test_after_clear_cache_real_db_is_called_again(self):
        self.proxy.query("SELECT 1")
        self.proxy.clear_cache()
        self.proxy.query("SELECT 1")
        assert len(self.real._query_log) == 2

    def test_is_database_subclass(self):
        assert issubclass(CachingDatabaseProxy, Database)

    def test_initial_cache_size_is_zero(self):
        assert self.proxy.cache_size == 0

    def test_initial_cache_hits_is_zero(self):
        assert self.proxy.cache_hits == 0


# ---------------------------------------------------------------------------
# LoggingDatabaseProxy
# ---------------------------------------------------------------------------

class TestLoggingDatabaseProxy:
    def setup_method(self):
        self.real = RealDatabase("sqlite://test.db")
        self.proxy = LoggingDatabaseProxy(self.real)

    def test_query_log_is_empty_initially(self):
        assert self.proxy.query_log == []

    def test_query_log_populated_after_single_query(self):
        self.proxy.query("SELECT name FROM products")
        assert "SELECT name FROM products" in self.proxy.query_log

    def test_query_log_records_all_queries(self):
        queries = ["SELECT 1", "SELECT 2", "SELECT 3"]
        for q in queries:
            self.proxy.query(q)
        assert self.proxy.query_log == queries

    def test_logging_proxy_delegates_to_real_database(self):
        result = self.proxy.query("SELECT 99")
        assert result == [{'result': 'SELECT 99'}]

    def test_logging_proxy_forwards_to_real_db(self):
        self.proxy.query("SELECT x")
        assert len(self.real._query_log) == 1

    def test_is_database_subclass(self):
        assert issubclass(LoggingDatabaseProxy, Database)

    def test_logging_wraps_caching_proxy(self):
        """LoggingProxy can wrap a CachingProxy (composability)."""
        cached = CachingDatabaseProxy(self.real)
        logged = LoggingDatabaseProxy(cached)
        result = logged.query("SELECT composed")
        assert result == [{'result': 'SELECT composed'}]
        assert "SELECT composed" in logged.query_log


# ---------------------------------------------------------------------------
# ProtectedDatabaseProxy
# ---------------------------------------------------------------------------

class TestProtectedDatabaseProxy:
    def setup_method(self):
        self.real = RealDatabase("sqlite://test.db")
        self.proxy = ProtectedDatabaseProxy(self.real, allowed_users=["alice", "bob"])

    def test_allowed_user_can_query(self):
        result = self.proxy.query("SELECT 1", user="alice")
        assert result == [{'result': 'SELECT 1'}]

    def test_second_allowed_user_can_query(self):
        result = self.proxy.query("SELECT 2", user="bob")
        assert result == [{'result': 'SELECT 2'}]

    def test_unauthorised_user_raises_permission_error(self):
        with pytest.raises(PermissionError):
            self.proxy.query("SELECT 1", user="eve")

    def test_empty_user_raises_permission_error(self):
        with pytest.raises(PermissionError):
            self.proxy.query("SELECT 1", user="")

    def test_allowed_user_result_forwarded_correctly(self):
        result = self.proxy.query("DROP TABLE secrets", user="alice")
        assert result == [{'result': 'DROP TABLE secrets'}]

    def test_real_db_not_called_for_unauthorised_user(self):
        try:
            self.proxy.query("SELECT 1", user="hacker")
        except PermissionError:
            pass
        assert len(self.real._query_log) == 0

    def test_is_database_subclass(self):
        assert issubclass(ProtectedDatabaseProxy, Database)

    def test_single_allowed_user_list(self):
        proxy = ProtectedDatabaseProxy(self.real, allowed_users=["only_one"])
        result = proxy.query("SELECT 1", user="only_one")
        assert result == [{'result': 'SELECT 1'}]
        with pytest.raises(PermissionError):
            proxy.query("SELECT 1", user="alice")


# ---------------------------------------------------------------------------
# Composition test
# ---------------------------------------------------------------------------

class TestProxyComposition:
    def test_protected_wrapping_logging_wrapping_caching_wrapping_real(self):
        """Full chain: Protected → Logging → Caching → Real."""
        real = RealDatabase("sqlite://test.db")
        cached = CachingDatabaseProxy(real)
        logged = LoggingDatabaseProxy(cached)
        protected = ProtectedDatabaseProxy(logged, allowed_users=["admin"])

        # First query — hits real DB
        r1 = protected.query("SELECT chain", user="admin")
        assert r1 == [{'result': 'SELECT chain'}]

        # Second identical query — served from cache
        r2 = protected.query("SELECT chain", user="admin")
        assert r2 == [{'result': 'SELECT chain'}]

        # Real DB was called only once despite two queries
        assert len(real._query_log) == 1

        # Log recorded both queries
        assert logged.query_log.count("SELECT chain") == 2

        # Unauthorised user still blocked
        with pytest.raises(PermissionError):
            protected.query("SELECT chain", user="intruder")
