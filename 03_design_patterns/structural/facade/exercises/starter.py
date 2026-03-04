"""
Facade Pattern — Exercise Solution: Smart Home Facade
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Subsystem classes
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
# Facade
# ---------------------------------------------------------------------------

class SmartHomeFacade:
    """
    Facade over SecuritySystem, Thermostat, LightingSystem, and MusicSystem.

    Each method delegates to the subsystems in the correct order and returns a
    list of the status strings each subsystem call produces. The Facade contains
    no logic of its own — it only coordinates.
    """

    def __init__(
        self,
        security: SecuritySystem,
        thermostat: Thermostat,
        lighting: LightingSystem,
        music: MusicSystem,
    ) -> None:
        self._security = security
        self._thermostat = thermostat
        self._lighting = lighting
        self._music = music

    def good_morning(self) -> list[str]:
        """Disarm security, set temp to 21, bright lights, play Morning Playlist."""
        return [
            self._security.disarm(),
            self._thermostat.set_temperature(21),
            self._lighting.set_scene("bright"),
            self._music.play("Morning Playlist"),
        ]

    def good_night(self) -> list[str]:
        """Arm security, set temp to 18, lights off, stop music."""
        return [
            self._security.arm(),
            self._thermostat.set_temperature(18),
            self._lighting.set_scene("off"),
            self._music.stop(),
        ]

    def movie_mode(self) -> list[str]:
        """Disarm security, set temp to 20, dim lights, play Movie Soundtrack."""
        return [
            self._security.disarm(),
            self._thermostat.set_temperature(20),
            self._lighting.set_scene("dim"),
            self._music.play("Movie Soundtrack"),
        ]

    def away_mode(self) -> list[str]:
        """Arm security, set temp to 16, lights off, stop music."""
        return [
            self._security.arm(),
            self._thermostat.set_temperature(16),
            self._lighting.set_scene("off"),
            self._music.stop(),
        ]
