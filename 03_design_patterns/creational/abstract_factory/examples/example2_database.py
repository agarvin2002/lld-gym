"""
Abstract Factory Example 2: Database Families
===============================================

Two database families: PostgreSQL and SQLite.
Each family produces three coordinated components:
  - Connection  (connect, close)
  - QueryBuilder (select, where, build)
  - Migrator    (run)

The Repository client uses whichever DatabaseFactory it receives.
Swapping the factory switches the entire database backend.

Run: python example2_database.py
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract Products
# ---------------------------------------------------------------------------

class Connection(ABC):
    """Abstract database connection."""

    @abstractmethod
    def connect(self) -> str:
        """Open a database connection and return a status message."""
        ...

    @abstractmethod
    def close(self) -> str:
        """Close the database connection and return a status message."""
        ...


class QueryBuilder(ABC):
    """Abstract SQL query builder with a fluent interface."""

    @abstractmethod
    def select(self, table: str) -> "QueryBuilder":
        """Set the table to SELECT from."""
        ...

    @abstractmethod
    def where(self, condition: str) -> "QueryBuilder":
        """Add a WHERE clause to the query."""
        ...

    @abstractmethod
    def build(self) -> str:
        """Assemble and return the final SQL query string."""
        ...


class Migrator(ABC):
    """Abstract database migrator."""

    @abstractmethod
    def run(self, migration_name: str) -> str:
        """Run a named migration and return a status message."""
        ...


# ---------------------------------------------------------------------------
# Abstract Factory
# ---------------------------------------------------------------------------

class DatabaseFactory(ABC):
    """
    Abstract factory that produces a family of database components.

    A concrete factory ties together Connection, QueryBuilder, and Migrator
    implementations that are all compatible with the same database engine.
    """

    @abstractmethod
    def create_connection(self) -> Connection:
        """Create a database-engine-specific connection."""
        ...

    @abstractmethod
    def create_query_builder(self) -> QueryBuilder:
        """Create a database-engine-specific query builder."""
        ...

    @abstractmethod
    def create_migrator(self) -> Migrator:
        """Create a database-engine-specific migrator."""
        ...


# ---------------------------------------------------------------------------
# PostgreSQL Family — Concrete Products
# ---------------------------------------------------------------------------

class PostgreSQLConnection(Connection):
    def connect(self) -> str:
        return "PostgreSQL: opening connection via psycopg2 on port 5432"

    def close(self) -> str:
        return "PostgreSQL: closing connection and returning to pool"


class PostgreSQLQueryBuilder(QueryBuilder):
    def __init__(self) -> None:
        self._table: str = ""
        self._conditions: list[str] = []

    def select(self, table: str) -> "PostgreSQLQueryBuilder":
        self._table = table
        return self

    def where(self, condition: str) -> "PostgreSQLQueryBuilder":
        self._conditions.append(condition)
        return self

    def build(self) -> str:
        query = f"SELECT * FROM {self._table}"
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        query += ";"  # PostgreSQL style — semicolon-terminated
        return query


class PostgreSQLMigrator(Migrator):
    def run(self, migration_name: str) -> str:
        return (
            f"PostgreSQL: running migration '{migration_name}' "
            f"using pg_migrate with transaction support"
        )


# ---------------------------------------------------------------------------
# SQLite Family — Concrete Products
# ---------------------------------------------------------------------------

class SQLiteConnection(Connection):
    def connect(self) -> str:
        return "SQLite: opening connection to local file database.db"

    def close(self) -> str:
        return "SQLite: flushing WAL and closing file handle"


class SQLiteQueryBuilder(QueryBuilder):
    def __init__(self) -> None:
        self._table: str = ""
        self._conditions: list[str] = []

    def select(self, table: str) -> "SQLiteQueryBuilder":
        self._table = table
        return self

    def where(self, condition: str) -> "SQLiteQueryBuilder":
        self._conditions.append(condition)
        return self

    def build(self) -> str:
        # SQLite uses the same SQL syntax but no semicolon in some drivers
        query = f"SELECT * FROM {self._table}"
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        return query


class SQLiteMigrator(Migrator):
    def run(self, migration_name: str) -> str:
        return (
            f"SQLite: applying migration '{migration_name}' "
            f"via sqlite3 module (no transaction rollback support)"
        )


# ---------------------------------------------------------------------------
# Concrete Factories
# ---------------------------------------------------------------------------

class PostgreSQLFactory(DatabaseFactory):
    """Creates components targeting the PostgreSQL database engine."""

    def create_connection(self) -> Connection:
        return PostgreSQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return PostgreSQLQueryBuilder()

    def create_migrator(self) -> Migrator:
        return PostgreSQLMigrator()


class SQLiteFactory(DatabaseFactory):
    """Creates components targeting the SQLite embedded database."""

    def create_connection(self) -> Connection:
        return SQLiteConnection()

    def create_query_builder(self) -> QueryBuilder:
        return SQLiteQueryBuilder()

    def create_migrator(self) -> Migrator:
        return SQLiteMigrator()


# ---------------------------------------------------------------------------
# Client — Repository
# ---------------------------------------------------------------------------

class Repository:
    """
    A generic data-access repository that works with any database family.

    The Repository never imports PostgreSQLFactory or SQLiteFactory.
    It receives a DatabaseFactory and uses the components it produces.
    All components are guaranteed to be compatible with the same engine.
    """

    def __init__(self, factory: DatabaseFactory) -> None:
        self._connection = factory.create_connection()
        self._query_builder = factory.create_query_builder()
        self._migrator = factory.create_migrator()

    def initialise(self) -> list[str]:
        """Connect and run initial migrations. Returns a log of operations."""
        log = []
        log.append(self._connection.connect())
        log.append(self._migrator.run("create_users_table"))
        log.append(self._migrator.run("add_email_index"))
        return log

    def find_active_users(self) -> str:
        """Build and return a query for active users."""
        query = (
            self._query_builder
            .select("users")
            .where("active = TRUE")
            .where("deleted_at IS NULL")
            .build()
        )
        return query

    def shutdown(self) -> str:
        """Close the database connection."""
        return self._connection.close()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_repository(factory: DatabaseFactory, label: str) -> None:
    print(f"--- {label} ---")
    repo = Repository(factory)

    print("Initialising:")
    for step in repo.initialise():
        print(f"  {step}")

    print(f"Query: {repo.find_active_users()}")
    print(f"Shutdown: {repo.shutdown()}")
    print()


def main() -> None:
    demo_repository(PostgreSQLFactory(), "PostgreSQL Repository")
    demo_repository(SQLiteFactory(), "SQLite Repository")

    print("Key observation:")
    print("  Repository.find_active_users() and initialise() are")
    print("  identical code paths for both database families.")
    print("  Switching databases = swapping the factory argument.")


if __name__ == "__main__":
    main()
