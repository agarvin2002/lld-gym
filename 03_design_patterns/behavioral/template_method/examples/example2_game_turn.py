"""
Template Method Pattern — Example 2: Turn-Based Game Engine
============================================================
A Game base class defines the turn sequence:
    setup → take_turns (loop) → print_winner

Each game (Chess, NumberGuessing) fills in how turns are played,
how to check if the game is over, and how to determine the winner.

The base class controls the *flow*; subclasses control the *content*.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import random


# ---------------------------------------------------------------------------
# Template (abstract base class)
# ---------------------------------------------------------------------------

class Game(ABC):
    """
    Template Method: play() is the game loop skeleton.

    Subclasses must implement:
      - initialize()    — set up board / state
      - has_winner()    — True when the game is over
      - take_turn()     — one player takes their turn
      - print_winner()  — announce the outcome
    """

    def __init__(self) -> None:
        self._current_player: int = 0
        self._turn_count: int = 0

    def play(self) -> None:
        """
        TEMPLATE METHOD.
        Runs a complete game from start to finish.
        """
        print(f"\n{'='*50}")
        print(f"  Starting: {self.__class__.__name__}")
        print(f"{'='*50}")

        self.initialize()

        while not self.has_winner():
            self._turn_count += 1
            print(f"\n--- Turn {self._turn_count} | Player {self._current_player + 1} ---")
            self.take_turn()
            self._current_player = self._next_player()

        self.print_winner()
        print(f"  (Game ended in {self._turn_count} turns)")

    # ------------------------------------------------------------------
    # Abstract hooks — MUST override
    # ------------------------------------------------------------------

    @abstractmethod
    def initialize(self) -> None:
        """Set up the initial game state."""
        ...

    @abstractmethod
    def has_winner(self) -> bool:
        """Return True when the game is over."""
        ...

    @abstractmethod
    def take_turn(self) -> None:
        """Execute the current player's turn."""
        ...

    @abstractmethod
    def print_winner(self) -> None:
        """Announce the result."""
        ...

    # ------------------------------------------------------------------
    # Optional hook — MAY override
    # ------------------------------------------------------------------

    def _next_player(self) -> int:
        """Default: alternate between two players. Override for >2 players."""
        return (self._current_player + 1) % 2


# ---------------------------------------------------------------------------
# Concrete Game 1: Number Guessing
# ---------------------------------------------------------------------------

class NumberGuessingGame(Game):
    """Two players alternately guess a secret number between 1 and 20."""

    def __init__(self, players: list[str]) -> None:
        super().__init__()
        self._players = players
        self._secret: int = 0
        self._winner: str | None = None

    def initialize(self) -> None:
        self._secret = random.randint(1, 20)
        print(f"  Secret number chosen (between 1 and 20).")

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


# ---------------------------------------------------------------------------
# Concrete Game 2: Simplified Chess (just captures)
# ---------------------------------------------------------------------------

class SimplifiedChess(Game):
    """
    Stripped-down chess: each player starts with 5 pieces; each turn they
    randomly capture 0 or 1 of the opponent's pieces.  Game ends when a
    player has no pieces left.
    """

    def __init__(self) -> None:
        super().__init__()
        self._pieces = [5, 5]   # pieces[0] = player 1, pieces[1] = player 2

    def initialize(self) -> None:
        self._pieces = [5, 5]
        print("  Board set up: each player has 5 pieces.")

    def has_winner(self) -> bool:
        return any(p == 0 for p in self._pieces)

    def take_turn(self) -> None:
        opponent = (self._current_player + 1) % 2
        capture = random.randint(0, 1)
        self._pieces[opponent] = max(0, self._pieces[opponent] - capture)
        action = "captures a piece" if capture else "moves without capturing"
        print(
            f"  Player {self._current_player+1} {action}. "
            f"Pieces: P1={self._pieces[0]}, P2={self._pieces[1]}"
        )

    def print_winner(self) -> None:
        loser = next(i for i, p in enumerate(self._pieces) if p == 0)
        winner = (loser + 1) % 2
        print(f"\n  WINNER: Player {winner+1}  "
              f"(Player {loser+1} ran out of pieces)")


# ---------------------------------------------------------------------------
# Concrete Game 3: Three-Player Dice Race
# ---------------------------------------------------------------------------

class DiceRace(Game):
    """
    Three players roll a die each turn; first to reach 20 wins.
    Overrides _next_player() to cycle through three players.
    """

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


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)

    games: list[Game] = [
        NumberGuessingGame(["Alice", "Bob"]),
        SimplifiedChess(),
        DiceRace(["Alice", "Bob", "Carol"]),
    ]

    for game in games:
        game.play()
