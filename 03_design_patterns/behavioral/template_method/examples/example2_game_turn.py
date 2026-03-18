# Advanced topic — overriding the optional _next_player hook to support more than two players
"""
Template Method Pattern — Example 2: Turn-Based Game Engine
============================================================
A Game base class defines the turn sequence:
    setup → take_turns (loop) → print_winner

The base class controls the flow; subclasses control the content.
The optional _next_player hook can be overridden for games with >2 players.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import random


class Game(ABC):
    """Template Method: play() is the game loop skeleton."""

    def __init__(self) -> None:
        self._current_player: int = 0
        self._turn_count: int = 0

    def play(self) -> None:
        """TEMPLATE METHOD — runs a complete game from start to finish."""
        print(f"\n{'='*40}")
        print(f"  Starting: {self.__class__.__name__}")
        print(f"{'='*40}")
        self.initialize()
        while not self.has_winner():
            self._turn_count += 1
            print(f"\n--- Turn {self._turn_count} | Player {self._current_player + 1} ---")
            self.take_turn()
            self._current_player = self._next_player()
        self.print_winner()
        print(f"  (Game ended in {self._turn_count} turns)")

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def has_winner(self) -> bool: ...

    @abstractmethod
    def take_turn(self) -> None: ...

    @abstractmethod
    def print_winner(self) -> None: ...

    def _next_player(self) -> int:
        """Optional hook — default alternates two players; override for more."""
        return (self._current_player + 1) % 2


class NumberGuessingGame(Game):
    """Two players alternately guess a secret number between 1 and 20."""

    def __init__(self, players: list[str]) -> None:
        super().__init__()
        self._players = players
        self._secret: int = 0
        self._winner: str | None = None

    def initialize(self) -> None:
        self._secret = random.randint(1, 20)
        print("  Secret number chosen (between 1 and 20).")

    def has_winner(self) -> bool:
        return self._winner is not None

    def take_turn(self) -> None:
        name = self._players[self._current_player]
        guess = random.randint(1, 20)
        print(f"  {name} guesses {guess} ", end="")
        if guess == self._secret:
            print("— CORRECT!")
            self._winner = name
        elif guess < self._secret:
            print("— too low")
        else:
            print("— too high")

    def print_winner(self) -> None:
        print(f"\n  WINNER: {self._winner} (secret was {self._secret})")


class DiceRace(Game):
    """Three players roll a die; first to reach 20 wins. Overrides _next_player."""

    def __init__(self, players: list[str]) -> None:
        super().__init__()
        self._players = players
        self._positions: list[int] = [0] * len(players)
        self._goal = 20
        self._winner_idx: int | None = None

    def initialize(self) -> None:
        self._positions = [0] * len(self._players)
        print(f"  {len(self._players)} players race to position {self._goal}.")

    def has_winner(self) -> bool:
        return self._winner_idx is not None

    def take_turn(self) -> None:
        roll = random.randint(1, 6)
        self._positions[self._current_player] += roll
        pos = self._positions[self._current_player]
        name = self._players[self._current_player]
        print(f"  {name} rolls {roll} → position {pos}")
        if pos >= self._goal:
            self._winner_idx = self._current_player

    def print_winner(self) -> None:
        print(f"\n  WINNER: {self._players[self._winner_idx]}")  # type: ignore[index]

    def _next_player(self) -> int:
        """Cycle through all players, not just two."""
        return (self._current_player + 1) % len(self._players)


if __name__ == "__main__":
    random.seed(42)
    for game in [NumberGuessingGame(["Alice", "Bob"]),
                 DiceRace(["Alice", "Bob", "Carol"])]:
        game.play()
