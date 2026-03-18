"""
Composite Pattern — Example 1: File System

A file system is the canonical Composite example.

- FileSystemItem  — shared ABC (Component)
- File            — Leaf: stores its own size
- Directory       — Composite: delegates size() to children

Key insight: directory.size() works the same whether the directory contains
files, sub-directories, or a mixture — no isinstance() checks required.

Real-world use: Cloud storage dashboards (Google Drive, Dropbox) calculate
folder sizes by recursively summing all nested files using this same pattern.
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
        return self._size_bytes   # base case: return own value

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
        """Add a child item. Returns self for fluent chaining."""
        self._children.append(item)
        return self

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    def size(self) -> int:
        """Recursive sum — each child handles its own subtree."""
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
    docs     = Directory("docs").add(File("resume.pdf", 120_000)).add(File("cover_letter.docx", 45_000))
    vacation = Directory("vacation").add(File("beach.jpg", 800_000)).add(File("sunset.jpg", 650_000))
    pictures = Directory("pictures").add(vacation).add(File("profile.png", 200_000))
    home     = Directory("home").add(docs).add(pictures).add(File("notes.txt", 2_000))
    return home


if __name__ == "__main__":
    home = build_sample_tree()

    print("=== File System Tree ===")
    print(home.display())

    print()

    # Same size() call works on directory or file — no isinstance() needed
    items: list[FileSystemItem] = [
        home,
        home._children[0],           # docs/
        home._children[0]._children[0],  # resume.pdf
    ]
    print("=== Sizes (uniform interface) ===")
    for item in items:
        print(f"  {item.name:25s}  {item.size():>10,} B")

    expected = 120_000 + 45_000 + 800_000 + 650_000 + 200_000 + 2_000
    assert home.size() == expected, f"Expected {expected}, got {home.size()}"
    print(f"\nhome.size() == {home.size():,} B  ✓")
