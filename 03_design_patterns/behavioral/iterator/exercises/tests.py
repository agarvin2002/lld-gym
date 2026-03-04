"""
Tests for the Playlist Iterator exercise.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import Song, Playlist

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def songs():
    return [
        Song("Bohemian Rhapsody", "Queen", 354),
        Song("Hotel California", "Eagles", 391),
        Song("Stairway to Heaven", "Led Zeppelin", 482),
    ]


@pytest.fixture
def playlist(songs):
    pl = Playlist()
    for s in songs:
        pl.add_song(s)
    return pl


# ---------------------------------------------------------------------------
# TestPlaylistBasic
# ---------------------------------------------------------------------------

class TestPlaylistBasic:
    def test_empty_playlist_len_is_zero(self):
        pl = Playlist()
        assert len(pl) == 0

    def test_add_song_increments_len(self, songs):
        pl = Playlist()
        for i, song in enumerate(songs, start=1):
            pl.add_song(song)
            assert len(pl) == i

    def test_list_returns_songs_in_insertion_order(self, playlist, songs):
        assert list(playlist) == songs

    def test_single_song_playlist(self):
        pl = Playlist()
        s = Song("Only One", "Solo Artist", 200)
        pl.add_song(s)
        assert len(pl) == 1
        assert list(pl) == [s]


# ---------------------------------------------------------------------------
# TestPlaylistIteration
# ---------------------------------------------------------------------------

class TestPlaylistIteration:
    def test_for_loop_visits_all_songs(self, playlist, songs):
        visited = []
        for song in playlist:
            visited.append(song)
        assert visited == songs

    def test_iteration_does_not_exhaust_playlist(self, playlist, songs):
        first_pass = list(playlist)
        second_pass = list(playlist)
        assert first_pass == songs
        assert second_pass == songs

    def test_iteration_order_matches_insertion_order(self, songs):
        pl = Playlist()
        # Add in a specific order
        for s in songs:
            pl.add_song(s)
        result = list(pl)
        assert result == songs

    def test_empty_playlist_iteration(self):
        pl = Playlist()
        assert list(pl) == []

    def test_for_loop_on_empty_playlist_does_not_execute(self):
        pl = Playlist()
        count = 0
        for _ in pl:
            count += 1
        assert count == 0


# ---------------------------------------------------------------------------
# TestPlaylistReversed
# ---------------------------------------------------------------------------

class TestPlaylistReversed:
    def test_reversed_gives_reverse_of_forward(self, playlist, songs):
        forward = list(playlist)
        backward = list(playlist.reversed())
        assert backward == list(reversed(forward))

    def test_reversed_exact_order(self, playlist, songs):
        backward = list(playlist.reversed())
        assert backward == [songs[2], songs[1], songs[0]]

    def test_reversed_empty_playlist(self):
        pl = Playlist()
        assert list(pl.reversed()) == []

    def test_reversed_single_song(self):
        pl = Playlist()
        s = Song("Solo", "Artist", 100)
        pl.add_song(s)
        assert list(pl.reversed()) == [s]

    def test_reversed_does_not_modify_original_order(self, playlist, songs):
        list(playlist.reversed())           # consume the reverse iterable
        assert list(playlist) == songs      # original still in insertion order

    def test_can_reverse_multiple_times(self, playlist, songs):
        rev1 = list(playlist.reversed())
        rev2 = list(playlist.reversed())
        assert rev1 == rev2 == list(reversed(songs))


# ---------------------------------------------------------------------------
# TestPlaylistShuffled
# ---------------------------------------------------------------------------

class TestPlaylistShuffled:
    def test_shuffled_contains_all_songs(self, playlist, songs):
        shuffled = list(playlist.shuffled())
        assert len(shuffled) == len(songs)
        # Same songs by title, regardless of order
        assert {s.title for s in shuffled} == {s.title for s in songs}

    def test_shuffled_does_not_modify_original_order(self, playlist, songs):
        list(playlist.shuffled())           # consume the shuffled iterable
        assert list(playlist) == songs

    def test_shuffled_result_is_iterable(self, playlist):
        result = playlist.shuffled()
        # Must be usable in a for loop
        count = 0
        for _ in result:
            count += 1
        assert count == len(playlist)

    def test_shuffled_empty_playlist(self):
        pl = Playlist()
        assert list(pl.shuffled()) == []

    def test_shuffled_single_song(self):
        pl = Playlist()
        s = Song("Only", "One", 99)
        pl.add_song(s)
        assert list(pl.shuffled()) == [s]

    def test_shuffled_twice_may_differ(self, songs):
        """
        Probabilistic test: with >= 2 songs, two shuffles are unlikely to
        always produce the same order.  We run 10 attempts and accept if at
        least one differs.  Skip for playlists smaller than 2.
        """
        pl = Playlist()
        for s in songs:
            pl.add_song(s)

        if len(pl) < 2:
            pytest.skip("Need at least 2 songs for this test")

        found_difference = False
        for _ in range(10):
            if list(pl.shuffled()) != list(pl.shuffled()):
                found_difference = True
                break

        # With 3 songs there are 6 permutations; probability both are the
        # same in 10 tries is (1/6)^10 ≈ 1.65e-8 — effectively impossible.
        assert found_difference, (
            "shuffled() returned the same order every time — "
            "is random.shuffle() being called?"
        )

    def test_shuffled_all_songs_present_as_objects(self, playlist, songs):
        """Shuffled result must contain the exact Song objects, not copies."""
        shuffled = list(playlist.shuffled())
        for song in songs:
            assert song in shuffled
