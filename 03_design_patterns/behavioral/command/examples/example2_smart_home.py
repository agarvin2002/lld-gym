"""Command Pattern — Example 2: Smart Home with Macros.

Demonstrates macro commands (composite commands), scheduled execution,
and a remote control invoker that holds named command slots.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


# ── Command Interface ─────────────────────────────────────────────────────────

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

    def __str__(self) -> str:
        return self.__class__.__name__


# ── Receivers ─────────────────────────────────────────────────────────────────

class Light:
    def __init__(self, location: str) -> None:
        self.location = location
        self.is_on = False
        self.brightness = 100

    def on(self) -> None:
        self.is_on = True
        print(f"{self.location} light ON (brightness={self.brightness}%)")

    def off(self) -> None:
        self.is_on = False
        print(f"{self.location} light OFF")

    def set_brightness(self, level: int) -> None:
        self.brightness = level
        print(f"{self.location} light brightness → {level}%")


class Thermostat:
    def __init__(self) -> None:
        self.temperature = 22

    def set_temp(self, temp: int) -> None:
        print(f"Thermostat: {self.temperature}°C → {temp}°C")
        self.temperature = temp


# ── Concrete Commands ─────────────────────────────────────────────────────────

class LightOnCommand(Command):
    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> None:
        self._light.on()

    def undo(self) -> None:
        self._light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> None:
        self._light.off()

    def undo(self) -> None:
        self._light.on()


class DimLightCommand(Command):
    def __init__(self, light: Light, level: int) -> None:
        self._light = light
        self._new_level = level
        self._prev_level = light.brightness  # snapshot for undo

    def execute(self) -> None:
        self._prev_level = self._light.brightness
        self._light.set_brightness(self._new_level)

    def undo(self) -> None:
        self._light.set_brightness(self._prev_level)


class ThermostatCommand(Command):
    def __init__(self, thermostat: Thermostat, temp: int) -> None:
        self._thermostat = thermostat
        self._new_temp = temp
        self._prev_temp = thermostat.temperature

    def execute(self) -> None:
        self._prev_temp = self._thermostat.temperature
        self._thermostat.set_temp(self._new_temp)

    def undo(self) -> None:
        self._thermostat.set_temp(self._prev_temp)


# ── Macro Command (composite) ─────────────────────────────────────────────────

class MacroCommand(Command):
    """Executes a list of commands as a single atomic unit."""
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

    def __str__(self) -> str:
        return f"MacroCommand({self._name})"


# ── Invoker ───────────────────────────────────────────────────────────────────

class RemoteControl:
    """Holds named slots; each slot pairs an on-command with an off-command."""
    def __init__(self) -> None:
        self._slots: dict[str, Command] = {}
        self._history: list[Command] = []

    def set_command(self, slot: str, command: Command) -> None:
        self._slots[slot] = command

    def press(self, slot: str) -> None:
        if slot not in self._slots:
            print(f"No command in slot {slot!r}")
            return
        cmd = self._slots[slot]
        cmd.execute()
        self._history.append(cmd)

    def undo_last(self) -> None:
        if not self._history:
            print("Nothing to undo.")
            return
        self._history.pop().undo()


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    living_room = Light("Living Room")
    bedroom = Light("Bedroom")
    thermostat = Thermostat()

    remote = RemoteControl()
    remote.set_command("living_on",  LightOnCommand(living_room))
    remote.set_command("living_off", LightOffCommand(living_room))
    remote.set_command("dim_50",     DimLightCommand(living_room, 50))

    # "Movie mode" macro: dim living room + turn bedroom off + cool down
    movie_mode = MacroCommand("Movie Mode", [
        DimLightCommand(living_room, 30),
        LightOffCommand(bedroom),
        ThermostatCommand(thermostat, 20),
    ])
    remote.set_command("movie", movie_mode)

    print("=== Basic Commands ===")
    remote.press("living_on")
    remote.press("dim_50")
    remote.undo_last()          # restore brightness

    print("\n=== Movie Mode ===")
    remote.press("movie")

    print("\n=== Undo Movie Mode ===")
    remote.undo_last()
