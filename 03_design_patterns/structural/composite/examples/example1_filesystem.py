"""
Composite Pattern — Example 1: File System
==========================================

A file system is the canonical Composite example.

- FileSystemItem  — shared ABC (Component)
- File            — Leaf: stores its own size
- Directory       — Composite: delegates size() to children

Key insight: directory.size() works the same whether the directory contains
files, sub-directories, or a mixture — no isinstance() checks required.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component (abstract base)
# ---------------------------------------------------------------------------

class FileSystemItem(ABC):
    """Shared interface for both files and directories."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def size(self) -> int:
        """Return total size in bytes."""
        ...

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Return a human-readable tree representation."""
        ...


# ---------------------------------------------------------------------------
# Leaf
# ---------------------------------------------------------------------------

class File(FileSystemItem):
    """A leaf node — stores its own size, has no children."""

    def __init__(self, name: str, size_bytes: int) -> None:
        self._name = name
        self._size_bytes = size_bytes

    @property
    def name(self) -> str:
        return self._name

    def size(self) -> int:
        return self._size_bytes

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}{self._name}  ({self._size_bytes:,} B)"


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------

class Directory(FileSystemItem):
    """A composite node — delegates size() and display() to children."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._children: list[FileSystemItem] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, item: FileSystemItem) -> "Directory":
        """Add a child item (fluent — returns self for chaining)."""
        self._children.append(item)
        return self

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    def size(self) -> int:
        """Recursively sum the sizes of all children."""
        return sum(child.size() for child in self._children)

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}[{self._name}/]  ({self.size():,} B total)"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def build_sample_tree() -> Directory:
    """
    /home/
    ├── docs/
    │   ├── resume.pdf         (120 000 B)
    │   └── cover_letter.docx  ( 45 000 B)
    ├── pictures/
    │   ├── vacation/
    │   │   ├── beach.jpg      (800 000 B)
    │   │   └── sunset.jpg     (650 000 B)
    │   └── profile.png        (200 000 B)
    └── notes.txt              (  2 000 B)
    """
    resume        = File("resume.pdf",         120_000)
    cover_letter  = File("cover_letter.docx",   45_000)
    docs          = Directory("docs").add(resume).add(cover_letter)

    beach         = File("beach.jpg",          800_000)
    sunset        = File("sunset.jpg",         650_000)
    vacation      = Directory("vacation").add(beach).add(sunset)

    profile       = File("profile.png",        200_000)
    pictures      = Directory("pictures").add(vacation).add(profile)

    notes         = File("notes.txt",            2_000)

    home          = Directory("home").add(docs).add(pictures).add(notes)
    return home


if __name__ == "__main__":
    home = build_sample_tree()

    print("=== File System Tree ===")
    print(home.display())

    print()

    # Demonstrate uniform treatment
    items: list[FileSystemItem] = [
        home,
        home._children[0],  # docs/
        home._children[0]._children[0],  # resume.pdf
    ]
    print("=== Sizes (uniform interface) ===")
    for item in items:
        print(f"  {item.name:25s}  {item.size():>10,} B")

    print()

    # Verify arithmetic
    expected = 120_000 + 45_000 + 800_000 + 650_000 + 200_000 + 2_000
    assert home.size() == expected, f"Expected {expected}, got {home.size()}"
    print(f"home.size() == {home.size():,} B  (verified correct)")
