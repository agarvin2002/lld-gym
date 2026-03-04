import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import SecuritySystem, Thermostat, LightingSystem, MusicSystem, SmartHomeFacade


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def home():
    return SmartHomeFacade(SecuritySystem(), Thermostat(), LightingSystem(), MusicSystem())


@pytest.fixture
def home_with_parts():
    """Returns (facade, security, thermostat, lighting, music) for state inspection."""
    security = SecuritySystem()
    thermostat = Thermostat()
    lighting = LightingSystem()
    music = MusicSystem()
    facade = SmartHomeFacade(security, thermostat, lighting, music)
    return facade, security, thermostat, lighting, music


# ---------------------------------------------------------------------------
# TestGoodMorning
# ---------------------------------------------------------------------------

class TestGoodMorning:
    def test_returns_list(self, home):
        result = home.good_morning()
        assert isinstance(result, list), "good_morning() must return a list"

    def test_returns_at_least_four_messages(self, home):
        result = home.good_morning()
        assert len(result) >= 4, "good_morning() must return at least 4 status messages"

    def test_security_is_disarmed(self, home_with_parts):
        facade, security, _, _, _ = home_with_parts
        facade.good_morning()
        assert security.is_armed is False, "Security should be disarmed after good_morning()"

    def test_thermostat_set_to_21(self, home_with_parts):
        facade, _, thermostat, _, _ = home_with_parts
        facade.good_morning()
        assert thermostat.current_temp == 21, "Thermostat should be set to 21 after good_morning()"

    def test_lighting_scene_is_bright(self, home_with_parts):
        facade, _, _, lighting, _ = home_with_parts
        facade.good_morning()
        assert lighting.current_scene == "bright", "Lighting scene should be 'bright' after good_morning()"

    def test_music_plays_morning_playlist(self, home_with_parts):
        facade, _, _, _, music = home_with_parts
        facade.good_morning()
        assert music.current_playlist == "Morning Playlist", \
            "Music should be playing 'Morning Playlist' after good_morning()"


# ---------------------------------------------------------------------------
# TestGoodNight
# ---------------------------------------------------------------------------

class TestGoodNight:
    def test_returns_list(self, home):
        result = home.good_night()
        assert isinstance(result, list), "good_night() must return a list"

    def test_returns_at_least_four_messages(self, home):
        result = home.good_night()
        assert len(result) >= 4, "good_night() must return at least 4 status messages"

    def test_security_is_armed(self, home_with_parts):
        facade, security, _, _, _ = home_with_parts
        facade.good_night()
        assert security.is_armed is True, "Security should be armed after good_night()"

    def test_thermostat_set_to_18(self, home_with_parts):
        facade, _, thermostat, _, _ = home_with_parts
        facade.good_night()
        assert thermostat.current_temp == 18, "Thermostat should be set to 18 after good_night()"

    def test_lighting_scene_is_off(self, home_with_parts):
        facade, _, _, lighting, _ = home_with_parts
        facade.good_night()
        assert lighting.current_scene == "off", "Lighting scene should be 'off' after good_night()"

    def test_music_is_stopped(self, home_with_parts):
        facade, _, _, _, music = home_with_parts
        # Start music first so we can verify it gets stopped
        music.play("Some Playlist")
        facade.good_night()
        assert music.current_playlist is None, "Music should be stopped (playlist None) after good_night()"


# ---------------------------------------------------------------------------
# TestMovieMode
# ---------------------------------------------------------------------------

class TestMovieMode:
    def test_returns_list(self, home):
        result = home.movie_mode()
        assert isinstance(result, list), "movie_mode() must return a list"

    def test_returns_at_least_four_messages(self, home):
        result = home.movie_mode()
        assert len(result) >= 4, "movie_mode() must return at least 4 status messages"

    def test_lighting_scene_is_dim(self, home_with_parts):
        facade, _, _, lighting, _ = home_with_parts
        facade.movie_mode()
        assert lighting.current_scene == "dim", "Lighting scene should be 'dim' after movie_mode()"

    def test_music_plays_movie_soundtrack(self, home_with_parts):
        facade, _, _, _, music = home_with_parts
        facade.movie_mode()
        assert music.current_playlist == "Movie Soundtrack", \
            "Music should be playing 'Movie Soundtrack' after movie_mode()"

    def test_security_is_disarmed(self, home_with_parts):
        facade, security, _, _, _ = home_with_parts
        security.arm()  # arm first
        facade.movie_mode()
        assert security.is_armed is False, "Security should be disarmed after movie_mode()"

    def test_thermostat_set_to_20(self, home_with_parts):
        facade, _, thermostat, _, _ = home_with_parts
        facade.movie_mode()
        assert thermostat.current_temp == 20, "Thermostat should be set to 20 after movie_mode()"


# ---------------------------------------------------------------------------
# TestAwayMode
# ---------------------------------------------------------------------------

class TestAwayMode:
    def test_returns_list(self, home):
        result = home.away_mode()
        assert isinstance(result, list), "away_mode() must return a list"

    def test_returns_at_least_four_messages(self, home):
        result = home.away_mode()
        assert len(result) >= 4, "away_mode() must return at least 4 status messages"

    def test_security_is_armed(self, home_with_parts):
        facade, security, _, _, _ = home_with_parts
        facade.away_mode()
        assert security.is_armed is True, "Security should be armed after away_mode()"

    def test_lighting_scene_is_off(self, home_with_parts):
        facade, _, _, lighting, _ = home_with_parts
        facade.away_mode()
        assert lighting.current_scene == "off", "Lighting scene should be 'off' after away_mode()"

    def test_music_is_stopped(self, home_with_parts):
        facade, _, _, _, music = home_with_parts
        music.play("Background Music")
        facade.away_mode()
        assert music.current_playlist is None, "Music should be stopped (playlist None) after away_mode()"

    def test_thermostat_set_to_16(self, home_with_parts):
        facade, _, thermostat, _, _ = home_with_parts
        facade.away_mode()
        assert thermostat.current_temp == 16, "Thermostat should be set to 16 after away_mode()"


# ---------------------------------------------------------------------------
# TestReturnValues
# ---------------------------------------------------------------------------

class TestReturnValues:
    def test_good_morning_returns_non_empty_strings(self, home):
        result = home.good_morning()
        for msg in result:
            assert isinstance(msg, str) and len(msg) > 0, \
                f"Each message in good_morning() result must be a non-empty string, got: {msg!r}"

    def test_good_night_returns_non_empty_strings(self, home):
        result = home.good_night()
        for msg in result:
            assert isinstance(msg, str) and len(msg) > 0, \
                f"Each message in good_night() result must be a non-empty string, got: {msg!r}"

    def test_movie_mode_returns_non_empty_strings(self, home):
        result = home.movie_mode()
        for msg in result:
            assert isinstance(msg, str) and len(msg) > 0, \
                f"Each message in movie_mode() result must be a non-empty string, got: {msg!r}"

    def test_away_mode_returns_non_empty_strings(self, home):
        result = home.away_mode()
        for msg in result:
            assert isinstance(msg, str) and len(msg) > 0, \
                f"Each message in away_mode() result must be a non-empty string, got: {msg!r}"
