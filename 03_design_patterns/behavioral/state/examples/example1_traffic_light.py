"""
State Pattern — Example 1: Traffic Light (Enum approach)
=========================================================
State stored as an Enum. Transitions defined in a dict.
Clean for simple state machines with few states.
"""
from enum import Enum, auto


class TrafficLightState(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()


class TrafficLight:
    _transitions = {
        TrafficLightState.RED:    TrafficLightState.GREEN,
        TrafficLightState.GREEN:  TrafficLightState.YELLOW,
        TrafficLightState.YELLOW: TrafficLightState.RED,
    }
    _actions = {
        TrafficLightState.RED:    "STOP  🔴",
        TrafficLightState.GREEN:  "GO    🟢",
        TrafficLightState.YELLOW: "SLOW  🟡",
    }

    def __init__(self) -> None:
        self.state = TrafficLightState.RED

    def change(self) -> None:
        self.state = self._transitions[self.state]

    def action(self) -> str:
        return self._actions[self.state]


if __name__ == "__main__":
    light = TrafficLight()
    for _ in range(6):
        print(f"{light.state.name:8} → {light.action()}")
        light.change()
