"""
Solution: Playlist Iterator
============================
Demonstrates how Python's built-in iterator protocol makes most of the work
trivial — `list` already knows how to iterate, reverse, and copy itself.
"""

from __future__ import annotations
from dataclasses import dataclass
import random


# ---------------------------------------------------------------------------
# Song — same definition as starter.py
# ---------------------------------------------------------------------------

@dataclass
class Song:
    title: str
    artist: str
    duration_seconds: int


# ---------------------------------------------------------------------------
# Playlist
# ---------------------------------------------------------------------------

class Playlist:
    """
    A sequence of Songs with forward, reverse, and shuffled iteration.

    Design decisions:
    - `Playlist` is an *iterable*, not an *iterator*.  This means `__iter__`
      returns a fresh iterator object each call, allowing multiple independent
      loops over the same playlist.
    - We delegate to Python's built-in list iterator (`iter()`), list reversal
      (`reversed()`), and a shuffled copy — no custom iterator class is needed.
    - `shuffled()` works on a copy to avoid mutating `_songs`.
    """

    def __init__(self) -> None:
        self._songs: list[Song] = []

    def add_song(self, song: Song) -> None:
        """Append `song` to the end of the playlist."""
        self._songs.append(song)

    def __iter__(self):
        """Return a fresh iterator over songs in insertion order."""
        return iter(self._songs)

    def __len__(self) -> int:
        """Return the number of songs."""
        return len(self._songs)

    def reversed(self):
        """
        Return an iterable that yields songs in reverse insertion order.

        `reversed()` on a list returns a `list_reverseiterator` — a single-pass
        iterator.  Calling `playlist.reversed()` multiple times each produces a
        fresh iterator, so the playlist remains reusable.
        """
        return reversed(self._songs)

    def shuffled(self):
        """
        Return an iterable that yields all songs in a random order.

        We copy `_songs` first so the original order is never disturbed.
        `random.shuffle()` shuffles in-place, then we return an iterator over
        the shuffled copy.
        """
        songs_copy = list(self._songs)
        random.shuffle(songs_copy)
        return iter(songs_copy)
