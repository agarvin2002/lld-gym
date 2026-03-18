"""
Template Method Pattern — Example 1: Data Pipeline
===================================================
A DataPipeline base class owns the fixed sequence:
    connect → extract → validate → transform → load → disconnect

Each concrete pipeline fills in what those steps mean for its data source.
The base class calls the subclass's methods, never the reverse.

Real-world use: Aadhaar data ingestion pipelines follow the same
ETL skeleton; only the connector and transformer differ per data source.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Template (abstract base class)
# ---------------------------------------------------------------------------

class DataPipeline(ABC):
    """
    Template Method: run() defines the fixed ETL sequence.

    Subclasses implement the abstract hooks; they must never override run()
    itself (the algorithm skeleton).
    """

    def run(self) -> dict:
        """
        Execute the full pipeline and return a summary.
        This is the TEMPLATE METHOD — do not override in subclasses.
        """
        print(f"\n[{self.__class__.__name__}] Starting pipeline …")
        conn = self._connect()
        try:
            raw = self._extract(conn)
            print(f"  Extracted {len(raw)} records")

            valid = self._validate(raw)
            print(f"  Validated: {len(valid)} passed, {len(raw)-len(valid)} rejected")

            transformed = self._transform(valid)
            print(f"  Transformed {len(transformed)} records")

            self._load(transformed)
            print(f"  Loaded {len(transformed)} records")
        finally:
            self._disconnect(conn)
            print(f"[{self.__class__.__name__}] Pipeline complete.")

        return {"extracted": len(raw), "loaded": len(transformed)}

    # ------------------------------------------------------------------
    # Abstract primitive operations — subclasses MUST implement these
    # ------------------------------------------------------------------

    @abstractmethod
    def _connect(self) -> object:
        """Open a connection to the data source. Return a connection handle."""
        ...

    @abstractmethod
    def _extract(self, conn: object) -> list[dict]:
        """Read raw records from the source. Return a list of dicts."""
        ...

    @abstractmethod
    def _transform(self, data: list[dict]) -> list[dict]:
        """Convert validated records into the target schema."""
        ...

    @abstractmethod
    def _load(self, data: list[dict]) -> None:
        """Write transformed records to the destination."""
        ...

    # ------------------------------------------------------------------
    # Optional hooks — subclasses MAY override, defaults provided
    # ------------------------------------------------------------------

    def _validate(self, data: list[dict]) -> list[dict]:
        """Default: accept all records. Override to add validation rules."""
        return data

    def _disconnect(self, conn: object) -> None:
        """Default: no-op. Override if the connection needs explicit closing."""
        pass


# ---------------------------------------------------------------------------
# Concrete pipeline 1: CSV → In-memory store
# ---------------------------------------------------------------------------

class CSVToMemoryPipeline(DataPipeline):
    """Reads product records from an in-memory CSV string."""

    _CSV_DATA = (
        "name,category,price\n"
        "Widget,Hardware,9.99\n"
        "Gadget,Electronics,49.99\n"
        "Doodad,Hardware,-5.00\n"   # invalid price — will be rejected
        "Thingamajig,Software,0.00\n"  # invalid price — will be rejected
    )

    def __init__(self) -> None:
        self._store: list[dict] = []

    def _connect(self) -> object:
        """Return a 'connection' — here just the CSV string split into lines."""
        print("  Connecting to CSV source …")
        return iter(self._CSV_DATA.strip().splitlines())

    def _extract(self, conn) -> list[dict]:
        """Parse CSV lines into dicts."""
        lines = list(conn)
        headers = lines[0].split(",")
        return [dict(zip(headers, line.split(","))) for line in lines[1:]]

    def _validate(self, data: list[dict]) -> list[dict]:
        """Reject rows where price <= 0."""
        return [r for r in data if float(r["price"]) > 0]

    def _transform(self, data: list[dict]) -> list[dict]:
        """Convert price to float."""
        return [
            {"name": r["name"], "category": r["category"], "price": float(r["price"])}
            for r in data
        ]

    def _load(self, data: list[dict]) -> None:
        """Store records in memory."""
        self._store.extend(data)

    def _disconnect(self, conn) -> None:
        """CSV is in memory — nothing to close."""
        print("  Closing CSV source …")

    @property
    def records(self) -> list[dict]:
        return list(self._store)


# ---------------------------------------------------------------------------
# Concrete pipeline 2: JSON → In-memory store
# ---------------------------------------------------------------------------

import json

class JSONToMemoryPipeline(DataPipeline):
    """Reads user records from a JSON string."""

    _JSON_DATA = json.dumps([
        {"id": 1, "username": "alice", "email": "alice@example.com", "active": True},
        {"id": 2, "username": "bob",   "email": "bob@example.com",   "active": False},
        {"id": 3, "username": "carol", "email": "carol@example.com", "active": True},
        {"id": 4, "username": "",      "email": "broken@example.com","active": True},
    ])

    def __init__(self) -> None:
        self._store: list[dict] = []

    def _connect(self) -> object:
        print("  Connecting to JSON source …")
        return self._JSON_DATA

    def _extract(self, conn) -> list[dict]:
        return json.loads(conn)

    def _validate(self, data: list[dict]) -> list[dict]:
        """Reject records with empty username."""
        return [r for r in data if r.get("username")]

    def _transform(self, data: list[dict]) -> list[dict]:
        """Keep only active users; drop the 'active' flag from output."""
        return [
            {"id": r["id"], "username": r["username"], "email": r["email"]}
            for r in data
            if r["active"]
        ]

    def _load(self, data: list[dict]) -> None:
        self._store.extend(data)

    @property
    def records(self) -> list[dict]:
        return list(self._store)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("Pipeline 1: CSV → Memory")
    print("=" * 55)
    csv_pipeline = CSVToMemoryPipeline()
    summary = csv_pipeline.run()
    print(f"\nSummary: {summary}")
    print("Stored records:")
    for r in csv_pipeline.records:
        print(f"  {r}")

    print("\n" + "=" * 55)
    print("Pipeline 2: JSON → Memory")
    print("=" * 55)
    json_pipeline = JSONToMemoryPipeline()
    summary = json_pipeline.run()
    print(f"\nSummary: {summary}")
    print("Stored records:")
    for r in json_pipeline.records:
        print(f"  {r}")
