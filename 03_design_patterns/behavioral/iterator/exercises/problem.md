# Exercise: Playlist Iterator

## Problem Statement

You are building a simple music player library.  The core class is `Playlist`,
which stores a sequence of `Song` objects and must support three distinct ways
to iterate over them.

---

## Classes to Implement

### `Song` (dataclass — already provided in starter.py)

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Song title |
| `artist` | `str` | Artist name |
| `duration_seconds` | `int` | Length of the song in seconds |

No methods needed; `@dataclass` handles equality and `__repr__` automatically.

---

### `Playlist`

| Method / behaviour | Signature | Description |
|--------------------|-----------|-------------|
| Constructor | `__init__(self) -> None` | Creates an empty playlist |
| Add song | `add_song(self, song: Song) -> None` | Appends `song` to the end |
| Forward iteration | `__iter__(self)` | Yields songs in insertion order |
| Length | `__len__(self) -> int` | Returns number of songs |
| Reverse iteration | `reversed(self)` | Returns an iterable that yields songs in **reverse** insertion order |
| Shuffle | `shuffled(self)` | Returns an iterable that yields **all** songs in a random order |

---

## Requirements

1. `for song in playlist` must visit every song exactly once, in insertion order.
2. You must be able to iterate the playlist **multiple times** — iteration must not exhaust it.
3. `len(playlist)` must return the number of songs.
4. `playlist.reversed()` must return something you can pass to `list()` or use in a `for` loop, yielding songs in reverse order.
5. `playlist.shuffled()` must return something you can pass to `list()` or use in a `for` loop, yielding **all** songs in some order (not necessarily the same each call).
6. `shuffled()` must **not** modify the original playlist order — `list(playlist)` should still return insertion order after calling `shuffled()`.

---

## Example Usage

```python
from starter import Song, Playlist

s1 = Song("Bohemian Rhapsody", "Queen", 354)
s2 = Song("Hotel California", "Eagles", 391)
s3 = Song("Stairway to Heaven", "Led Zeppelin", 482)

pl = Playlist()
pl.add_song(s1)
pl.add_song(s2)
pl.add_song(s3)

print(len(pl))               # 3

for song in pl:
    print(song.title)        # Bohemian Rhapsody, Hotel California, Stairway to Heaven

print(list(pl.reversed()))   # [s3, s2, s1]

shuffled = list(pl.shuffled())
print(len(shuffled))         # 3  (all songs present, possibly different order)
print(list(pl))              # still [s1, s2, s3]  (original order preserved)
```

---

## Hints

- For forward iteration, `iter(self._songs)` is perfectly idiomatic — you do not need to write a custom iterator class.
- For reverse iteration, `reversed(self._songs)` works because `list` supports `__reversed__`.
- For `shuffled()`, copy the list first (`list(self._songs)`), shuffle the copy with `random.shuffle()`, then return an iterator over the copy.
- Think about the difference between an *iterable* (can be looped over, may be re-used) and an *iterator* (single-pass cursor).  Which one does `Playlist` need to be?

---

## What NOT to do

- Do not sort or alter `self._songs` inside `shuffled()` — always work on a copy.
- Do not store iteration state in `Playlist` itself — that would break multiple simultaneous loops.
