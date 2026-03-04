"""Snake and Ladders — Reference Solution."""
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
    teleported_to: int | None
    won: bool


class Board:
    def __init__(self, size: int = 100) -> None:
        self._size = size
        self._snakes: dict[int, int] = {}   # head → tail
        self._ladders: dict[int, int] = {}  # base → top

    def add_snake(self, head: int, tail: int) -> None:
        if head <= tail:
            raise ValueError("Snake head must be above tail.")
        self._snakes[head] = tail

    def add_ladder(self, base: int, top: int) -> None:
        if base >= top:
            raise ValueError("Ladder top must be above base.")
        self._ladders[base] = top

    def resolve(self, position: int) -> int:
        if position in self._snakes:
            return self._snakes[position]
        if position in self._ladders:
            return self._ladders[position]
        return position

    @property
    def size(self) -> int:
        return self._size


class Game:
    def __init__(self, board: Board, die: Callable[[], int] | None = None) -> None:
        self._board = board
        self._die = die or (lambda: random.randint(1, 6))
        self._players: list[Player] = []
        self._status = GameStatus.WAITING
        self._current_index = 0
        self._winner: Player | None = None

    def add_player(self, name: str) -> Player:
        if self._status != GameStatus.WAITING:
            raise ValueError("Cannot add players after the game has started.")
        player = Player(name=name)
        self._players.append(player)
        return player

    def start(self) -> None:
        if len(self._players) < 2:
            raise ValueError("Need at least 2 players to start.")
        self._status = GameStatus.IN_PROGRESS

    def roll_and_move(self) -> MoveResult:
        if self._status != GameStatus.IN_PROGRESS:
            raise ValueError("Game is not in progress.")
        player = self._players[self._current_index]
        roll = self._die()
        from_pos = player.position
        new_pos = player.position + roll

        # Bounce rule: cannot go beyond the board
        if new_pos > self._board.size:
            new_pos = player.position

        resolved = self._board.resolve(new_pos)
        teleported_to = resolved if resolved != new_pos else None
        player.position = resolved

        won = player.position == self._board.size
        if won:
            self._winner = player
            self._status = GameStatus.FINISHED
        else:
            self._current_index = (self._current_index + 1) % len(self._players)

        return MoveResult(
            player_name=player.name,
            roll=roll,
            from_pos=from_pos,
            to_pos=resolved,
            teleported_to=teleported_to,
            won=won,
        )

    def current_player(self) -> Player:
        return self._players[self._current_index]

    def winner(self) -> Player | None:
        return self._winner

    @property
    def status(self) -> GameStatus:
        return self._status
