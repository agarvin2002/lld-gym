"""
WHAT YOU'RE BUILDING
====================
A Playlist class that holds Song objects and supports three ways to iterate:

1. Forward iteration (default for-loop) — songs in the order they were added
2. Reversed iteration  — songs from last to first
3. Shuffled iteration  — songs in a random order each time

The Playlist must be re-usable: looping over it twice should work fine.
"""

from __future__ import annotations
from dataclasses import dataclass
import random


@dataclass
class Song:
    title: str
    artist: str
    duration_seconds: int


class Playlist:
    def __init__(self) -> None:
        # TODO: Create self._songs as an empty list to store Song objects
        pass

    def add_song(self, song: Song) -> None:
        # TODO: Append the song to self._songs
        pass

    def __iter__(self):
        # HINT: Use iter(self._songs) — Python's built-in iter() returns a
        #       fresh list iterator each call, so the playlist stays reusable.
        # TODO: Return iter(self._songs)
        pass

    def __len__(self) -> int:
        # TODO: Return the number of songs
        pass

    def reversed(self):
        # HINT: Use reversed(self._songs) — returns a reverse iterator without
        #       modifying self._songs at all.
        # TODO: Return reversed(self._songs)
        pass

    def shuffled(self):
        # HINT: Copy self._songs first (list(self._songs)), then call
        #       random.shuffle() on the copy, then return iter(copy).
        #       Never shuffle self._songs directly — that would change the
        #       original order permanently.
        # TODO: Shuffle a copy and return an iterator over the copy
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/behavioral/iterator/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
