# Advanced topic — swapping an entire database backend (PostgreSQL vs SQLite) by changing one factory argument.
"""
Abstract Factory Example 2: Database Families

Two families — PostgreSQL and SQLite — each produce a matching
Connection, QueryBuilder, and Migrator. The Repository client
accepts any DatabaseFactory and works identically for both.

Real-world use: Django's database backend system — changing DATABASE ENGINE
in settings.py swaps the whole family of connection, schema editor, and
query compiler without touching application code.

Run: python example2_database.py
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def connect(self) -> str: ...
    @abstractmethod
    def close(self) -> str: ...

class QueryBuilder(ABC):
    @abstractmethod
    def select(self, table: str) -> "QueryBuilder": ...
    @abstractmethod
    def where(self, condition: str) -> "QueryBuilder": ...
    @abstractmethod
    def build(self) -> str: ...

class Migrator(ABC):
    @abstractmethod
    def run(self, name: str) -> str: ...

class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection: ...
    @abstractmethod
    def create_query_builder(self) -> QueryBuilder: ...
    @abstractmethod
    def create_migrator(self) -> Migrator: ...


# PostgreSQL family
class PGConnection(Connection):
    def connect(self) -> str: return "PG: connected on port 5432"
    def close(self) -> str:   return "PG: connection returned to pool"

class PGQueryBuilder(QueryBuilder):
    def __init__(self) -> None:
        self._table = ""; self._conds: list[str] = []
    def select(self, t: str) -> "PGQueryBuilder":
        self._table = t; return self
    def where(self, c: str) -> "PGQueryBuilder":
        self._conds.append(c); return self
    def build(self) -> str:
        q = f"SELECT * FROM {self._table}"
        if self._conds: q += " WHERE " + " AND ".join(self._conds)
        return q + ";"  # PG style: semicolon-terminated

class PGMigrator(Migrator):
    def run(self, name: str) -> str: return f"PG: running '{name}' via pg_migrate"

class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self)    -> Connection:   return PGConnection()
    def create_query_builder(self) -> QueryBuilder: return PGQueryBuilder()
    def create_migrator(self)      -> Migrator:     return PGMigrator()


# SQLite family
class SQLiteConnection(Connection):
    def connect(self) -> str: return "SQLite: opened database.db"
    def close(self)   -> str: return "SQLite: flushed WAL and closed"

class SQLiteQueryBuilder(QueryBuilder):
    def __init__(self) -> None:
        self._table = ""; self._conds: list[str] = []
    def select(self, t: str) -> "SQLiteQueryBuilder":
        self._table = t; return self
    def where(self, c: str) -> "SQLiteQueryBuilder":
        self._conds.append(c); return self
    def build(self) -> str:
        q = f"SELECT * FROM {self._table}"
        if self._conds: q += " WHERE " + " AND ".join(self._conds)
        return q  # SQLite: no trailing semicolon

class SQLiteMigrator(Migrator):
    def run(self, name: str) -> str: return f"SQLite: applying '{name}' via sqlite3"

class SQLiteFactory(DatabaseFactory):
    def create_connection(self)    -> Connection:   return SQLiteConnection()
    def create_query_builder(self) -> QueryBuilder: return SQLiteQueryBuilder()
    def create_migrator(self)      -> Migrator:     return SQLiteMigrator()


# Client — identical code, works with any DatabaseFactory
class Repository:
    def __init__(self, factory: DatabaseFactory) -> None:
        self._conn    = factory.create_connection()
        self._qb      = factory.create_query_builder()
        self._migrate = factory.create_migrator()

    def setup(self) -> list[str]:
        return [self._conn.connect(), self._migrate.run("create_users_table")]

    def find_active_users(self) -> str:
        return self._qb.select("users").where("active = TRUE").build()


if __name__ == "__main__":
    for factory, label in [(PostgreSQLFactory(), "PostgreSQL"), (SQLiteFactory(), "SQLite")]:
        repo = Repository(factory)
        print(f"--- {label} ---")
        for step in repo.setup(): print(f"  {step}")
        print(f"  {repo.find_active_users()}\n")
    print("Same Repository code runs against both engines — only the factory changes.")
