"""
Snake and Ladders — Starter File
===================================
Your task: Implement a Snake and Ladders board game.

Read problem.md and design.md before starting.

Design decisions:
  - Board holds dicts for snakes (head→tail) and ladders (base→top)
  - Board.resolve(position) applies any snake or ladder at that position
  - Game manages player order, turn tracking, and win detection
  - Bounce rule: if roll would take player past board size, they stay put
  - Die is injected as a callable (default: random.randint(1, 6)) for testability
  - add_player() only works before start(); start() requires >= 2 players
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
import random
from typing import Callable


class GameStatus(Enum):
    WAITING     = auto()
    IN_PROGRESS = auto()
    FINISHED    = auto()


@dataclass
class Player:
    name: str
    position: int = 0


@dataclass
class MoveResult:
    player_name: str
    roll: int
    from_pos: int
    to_pos: int
    teleported_to: int | None   # final position if snake/ladder applied, else None
    won: bool


class Board:
    def __init__(self, size: int = 100) -> None:
        # TODO: Store _size, create _snakes: dict[int, int] = {}, _ladders: dict[int, int] = {}
        pass

    def add_snake(self, head: int, tail: int) -> None:
        """Register a snake from head down to tail.

        TODO:
            - Raise ValueError if head <= tail (snake must go downward)
            - Store in _snakes
        """
        pass

    def add_ladder(self, base: int, top: int) -> None:
        """Register a ladder from base up to top.

        TODO:
            - Raise ValueError if base >= top (ladder must go upward)
            - Store in _ladders
        """
        pass

    def resolve(self, position: int) -> int:
        """Return final position after applying any snake or ladder.

        TODO:
            - If position is a snake head: return the tail
            - If position is a ladder base: return the top
            - Otherwise return position unchanged
        """
        pass

    @property
    def size(self) -> int:
        # TODO: Return _size
        pass


class Game:
    def __init__(self, board: Board, die: Callable[[], int] | None = None) -> None:
        # TODO: Store _board and _die (default: lambda: random.randint(1, 6))
        # TODO: Create _players: list[Player] = []
        # TODO: Set _status = GameStatus.WAITING
        # TODO: Set _current_index = 0 and _winner = None
        pass

    def add_player(self, name: str) -> Player:
        """Add a player to the game (only valid before start).

        TODO:
            - Raise ValueError if game status is not WAITING
            - Create Player(name=name), append to _players
            - Return the player
        """
        pass

    def start(self) -> None:
        """Start the game.

        TODO:
            - Raise ValueError if fewer than 2 players
            - Set status to IN_PROGRESS
        """
        pass

    def roll_and_move(self) -> MoveResult:
        """Roll the die and move the current player.

        TODO:
            - Raise ValueError if status is not IN_PROGRESS
            - Roll the die; compute new_pos = current_position + roll
            - Apply bounce rule: if new_pos > board.size, stay at current position
            - Apply board.resolve(new_pos) for snakes/ladders
            - Set teleported_to = resolved if resolved != new_pos, else None
            - Update player.position = resolved
            - If player.position == board.size: set winner, status = FINISHED; return
            - Otherwise: advance _current_index to next player (circular)
            - Return MoveResult with all relevant info
        """
        pass

    def current_player(self) -> Player:
        # TODO: Return _players[_current_index]
        pass

    def winner(self) -> Player | None:
        # TODO: Return _winner
        pass

    @property
    def status(self) -> GameStatus:
        return self._status
