"""
Proxy Pattern — Example 1: Virtual (Lazy) Proxy

A VirtualProxy defers creating an expensive object until the first time it is
actually needed. The caller never notices — the interface is identical.

Real-world use: Django's SimpleLazyObject defers loading request.user from
the database until the view first accesses it, saving a DB query on routes
that never check the user.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Subject interface
# ---------------------------------------------------------------------------

class Image(ABC):
    """Common interface for real and proxy images."""

    @abstractmethod
    def display(self) -> str:
        """Render the image and return a description string."""
        ...

    @abstractmethod
    def dimensions(self) -> tuple[int, int]:
        """Return (width, height) in pixels."""
        ...


# ---------------------------------------------------------------------------
# Real Subject — expensive to create
# ---------------------------------------------------------------------------

class HighResImage(Image):
    """Simulates loading a large image file from disk."""

    def __init__(self, filename: str) -> None:
        self._filename = filename
        print(f"  [HighResImage] Loading '{filename}' from disk … (slow)")
        # In real life: PIL.Image.open(filename)
        self._width = 4096
        self._height = 3072

    def display(self) -> str:
        return f"Displaying {self._filename} at {self._width}×{self._height}"

    def dimensions(self) -> tuple[int, int]:
        return (self._width, self._height)


# ---------------------------------------------------------------------------
# Virtual Proxy — defers construction of HighResImage
# ---------------------------------------------------------------------------

class LazyImageProxy(Image):
    """
    Holds only the filename at construction time.
    Creates the real HighResImage on the first call to display() or dimensions().
    """

    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._real: HighResImage | None = None  # not yet loaded
        print(f"  [LazyImageProxy] Registered '{filename}' (not yet loaded)")

    def _load(self) -> None:
        """Trigger real object creation on first access."""
        if self._real is None:
            print(f"  [LazyImageProxy] First access — triggering load …")
            self._real = HighResImage(self._filename)

    def display(self) -> str:
        self._load()
        return self._real.display()  # type: ignore[union-attr]

    def dimensions(self) -> tuple[int, int]:
        self._load()
        return self._real.dimensions()  # type: ignore[union-attr]

    @property
    def is_loaded(self) -> bool:
        """Useful for diagnostics and testing."""
        return self._real is not None


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def render_gallery(images: list[Image]) -> None:
    """Simulates a gallery that renders every visible image."""
    for img in images:
        print(f"  → {img.display()}")


if __name__ == "__main__":
    print("=== Building gallery (no images loaded yet) ===")
    gallery: list[Image] = [
        LazyImageProxy("photo_paris.raw"),
        LazyImageProxy("photo_tokyo.raw"),
        LazyImageProxy("photo_sydney.raw"),
    ]

    print("\n=== Rendering only the first image ===")
    print(gallery[0].display())

    print("\n=== Checking load state ===")
    for i, img in enumerate(gallery):
        if isinstance(img, LazyImageProxy):
            print(f"  gallery[{i}] loaded: {img.is_loaded}")

    print("\n=== Rendering full gallery ===")
    render_gallery(gallery)

    print("\n=== Dimensions of first image (already loaded — no reload) ===")
    print(f"  {gallery[0].dimensions()}")
