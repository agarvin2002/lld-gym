"""
WHAT YOU'RE BUILDING
====================
A SmartHomeFacade that controls four subsystems with one method call each:
  - SecuritySystem  — arm or disarm the house alarm
  - Thermostat      — set the target temperature
  - LightingSystem  — switch between named lighting scenes
  - MusicSystem     — play a named playlist or stop music

You need to implement four "scene" methods on SmartHomeFacade:
  good_morning() — disarm, 21°C, bright lights, Morning Playlist
  good_night()   — arm, 18°C, lights off, stop music
  movie_mode()   — disarm, 20°C, dim lights, Movie Soundtrack
  away_mode()    — arm, 16°C, lights off, stop music

Each method must return a list of the strings that the subsystem calls return.
The subsystems are already complete — you only need to implement SmartHomeFacade.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Subsystem classes — DO NOT MODIFY
# ---------------------------------------------------------------------------

class SecuritySystem:
    def __init__(self) -> None:
        self._armed = False

    def arm(self) -> str:
        self._armed = True
        return "Security system armed."

    def disarm(self) -> str:
        self._armed = False
        return "Security system disarmed."

    @property
    def is_armed(self) -> bool:
        return self._armed


class Thermostat:
    def __init__(self) -> None:
        self._temp = 22

    def set_temperature(self, temp: int) -> str:
        self._temp = temp
        return f"Thermostat set to {temp}\u00b0C."

    @property
    def current_temp(self) -> int:
        return self._temp


class LightingSystem:
    def __init__(self) -> None:
        self._scene = "off"

    def set_scene(self, scene: str) -> str:
        self._scene = scene
        return f"Lights set to {scene}."

    @property
    def current_scene(self) -> str:
        return self._scene


class MusicSystem:
    def __init__(self) -> None:
        self._playlist: str | None = None

    def play(self, playlist: str) -> str:
        self._playlist = playlist
        return f"Playing '{playlist}'."

    def stop(self) -> str:
        self._playlist = None
        return "Music stopped."

    @property
    def current_playlist(self) -> str | None:
        return self._playlist


# ---------------------------------------------------------------------------
# Facade — implement this class
# ---------------------------------------------------------------------------

class SmartHomeFacade:
    """Facade over SecuritySystem, Thermostat, LightingSystem, and MusicSystem."""

    def __init__(
        self,
        security: SecuritySystem,
        thermostat: Thermostat,
        lighting: LightingSystem,
        music: MusicSystem,
    ) -> None:
        # TODO: Store each subsystem as an instance variable (e.g. self._security = security)
        pass

    def good_morning(self) -> list[str]:
        """Disarm security, set temp to 21, bright lights, play Morning Playlist."""
        # TODO: Call the four subsystems in order and collect their return values.
        # HINT: Each subsystem method returns a string — build a list of those strings.
        # Example first step: self._security.disarm()
        pass

    def good_night(self) -> list[str]:
        """Arm security, set temp to 18, lights off, stop music."""
        # TODO: Call arm(), set_temperature(18), set_scene("off"), stop()
        # HINT: Return a list of all four return values.
        pass

    def movie_mode(self) -> list[str]:
        """Disarm security, set temp to 20, dim lights, play Movie Soundtrack."""
        # TODO: Use "dim" for the lighting scene and "Movie Soundtrack" as the playlist.
        # HINT: Disarm first so the alarm doesn't trigger during the movie.
        pass

    def away_mode(self) -> list[str]:
        """Arm security, set temp to 16, lights off, stop music."""
        # TODO: Call arm(), set_temperature(16), set_scene("off"), stop()
        # HINT: Same structure as good_night() but with a different temperature.
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/structural/facade/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
