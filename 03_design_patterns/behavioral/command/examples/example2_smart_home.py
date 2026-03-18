# Advanced topic — MacroCommand: grouping multiple commands into one undoable unit.
"""Command Pattern — Example 2: Macro Commands.

A MacroCommand holds a list of commands and executes them as a single unit.
Undo reverses all of them in reverse order.

Real-world use: "Movie Mode" on a smart home app — one button dims lights
and turns others off. One undo button reverses all of them.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...


class Light:
    def __init__(self, location: str) -> None:
        self.location = location
        self.is_on = False

    def on(self) -> None:
        self.is_on = True
        print(f"{self.location} light ON")

    def off(self) -> None:
        self.is_on = False
        print(f"{self.location} light OFF")


class LightOnCommand(Command):
    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> None: self._light.on()
    def undo(self)    -> None: self._light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> None: self._light.off()
    def undo(self)    -> None: self._light.on()


class MacroCommand(Command):
    """Executes a list of commands as one atomic unit; undoes in reverse."""
    def __init__(self, name: str, commands: list[Command]) -> None:
        self._name = name
        self._commands = commands

    def execute(self) -> None:
        print(f"--- Macro: {self._name} ---")
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        print(f"--- Undo Macro: {self._name} ---")
        for cmd in reversed(self._commands):
            cmd.undo()


if __name__ == "__main__":
    living_room = Light("Living Room")
    bedroom     = Light("Bedroom")
    hallway     = Light("Hallway")

    movie_mode = MacroCommand("Movie Mode", [
        LightOffCommand(living_room),
        LightOffCommand(bedroom),
        LightOffCommand(hallway),
    ])

    print("=== Activate Movie Mode ===")
    movie_mode.execute()

    print("\n=== Undo Movie Mode ===")
    movie_mode.undo()
