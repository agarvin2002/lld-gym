"""
Facade Pattern — Example 1: Home Theater System

Demonstrates how a HomeTheaterFacade simplifies the coordination of six
independent subsystem classes: Projector, Screen, SurroundSound, BluRayPlayer,
Lights, and StreamingBox.

Real-world use: Smart home apps (Google Home, Apple HomeKit) expose "scenes"
like "Movie Night" that coordinate lights, TV, and speakers with one tap —
exactly what this Facade does.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Subsystem classes
# ---------------------------------------------------------------------------

class Projector:
    def __init__(self, model: str = "Epson 4K") -> None:
        self._model = model
        self._on = False
        self._input: str | None = None

    def on(self) -> None:
        self._on = True
        print(f"[Projector:{self._model}] Powered ON.")

    def off(self) -> None:
        self._on = False
        print(f"[Projector:{self._model}] Powered OFF.")

    def set_input(self, source: str) -> None:
        self._input = source
        print(f"[Projector:{self._model}] Input set to '{source}'.")


class Screen:
    def __init__(self) -> None:
        self._position = "up"

    def down(self) -> None:
        self._position = "down"
        print("[Screen] Lowering screen...")

    def up(self) -> None:
        self._position = "up"
        print("[Screen] Raising screen...")


class SurroundSound:
    def __init__(self) -> None:
        self._on = False
        self._volume = 0

    def on(self) -> None:
        self._on = True
        print("[SurroundSound] Amplifier ON.")

    def off(self) -> None:
        self._on = False
        print("[SurroundSound] Amplifier OFF.")

    def set_volume(self, level: int) -> None:
        self._volume = level
        print(f"[SurroundSound] Volume set to {level}.")


class BluRayPlayer:
    def __init__(self) -> None:
        self._on = False
        self._playing: str | None = None

    def on(self) -> None:
        self._on = True
        print("[BluRay] Player ON.")

    def off(self) -> None:
        self._on = False
        print("[BluRay] Player OFF.")

    def play(self, title: str) -> None:
        self._playing = title
        print(f"[BluRay] Playing '{title}'.")

    def stop(self) -> None:
        self._playing = None
        print("[BluRay] Stopped.")


class Lights:
    def __init__(self, room: str = "Living Room") -> None:
        self._room = room
        self._dimmer = 100

    def on(self) -> None:
        self._dimmer = 100
        print(f"[Lights:{self._room}] Lights ON at full brightness.")

    def off(self) -> None:
        print(f"[Lights:{self._room}] Lights OFF.")

    def set_dimmer(self, level: int) -> None:
        self._dimmer = level
        print(f"[Lights:{self._room}] Dimmer set to {level}%.")


class StreamingBox:
    def __init__(self) -> None:
        self._on = False

    def on(self) -> None:
        self._on = True
        print("[StreamingBox] Apple TV ON.")

    def off(self) -> None:
        self._on = False
        print("[StreamingBox] Apple TV OFF.")


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

class HomeTheaterFacade:
    """
    Three high-level operations over six subsystems:
      - watch_movie   : physical disc via Blu-ray
      - end_movie     : shut everything down
      - stream_netflix: streaming via StreamingBox
    """

    def __init__(
        self,
        projector: Projector,
        screen: Screen,
        sound: SurroundSound,
        bluray: BluRayPlayer,
        lights: Lights,
        streaming_box: StreamingBox,
    ) -> None:
        self._projector = projector
        self._screen = screen
        self._sound = sound
        self._bluray = bluray
        self._lights = lights
        self._streaming_box = streaming_box

    def watch_movie(self, title: str) -> None:
        """Prepare the room and start a Blu-ray movie."""
        print(f"\n--- Getting ready to watch '{title}' ---")
        self._lights.set_dimmer(30)
        self._screen.down()
        self._projector.on()
        self._projector.set_input("HDMI")
        self._sound.on()
        self._sound.set_volume(30)
        self._bluray.on()
        self._bluray.play(title)
        print("--- Enjoy the movie! ---\n")

    def end_movie(self) -> None:
        """Stop playback and restore the room."""
        print("\n--- Shutting down the home theater ---")
        self._bluray.stop()
        self._bluray.off()
        self._projector.off()
        self._screen.up()
        self._sound.off()
        self._lights.on()
        print("--- Home theater off. ---\n")

    def stream_netflix(self, title: str) -> None:
        """Switch to streaming mode and start the given title."""
        print(f"\n--- Streaming '{title}' via Netflix ---")
        self._lights.set_dimmer(40)
        self._screen.down()
        self._projector.on()
        self._projector.set_input("Streaming")
        self._streaming_box.on()
        self._sound.on()
        self._sound.set_volume(25)
        print(f"--- Now streaming: '{title}' ---\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    theater = HomeTheaterFacade(
        Projector(), Screen(), SurroundSound(),
        BluRayPlayer(), Lights(), StreamingBox(),
    )

    # Scenario 1: Watch a Blu-ray movie
    theater.watch_movie("Interstellar")
    theater.end_movie()

    # Scenario 2: Stream something
    theater.stream_netflix("The Bear")
