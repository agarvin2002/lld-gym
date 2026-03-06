"""
Chess Game — Starter File
===========================
Your task: Implement a two-player chess game.

Read problem.md and design.md before starting.

Design decisions:
  - Piece is an ABC with get_valid_moves() per piece type
  - _slide() helper in Piece handles Rook/Bishop/Queen movement
  - Board uses a dict[Position, Piece] — sparse grid (only stores occupied squares)
  - Position is a frozen dataclass (hashable) — check is_valid() before using
  - Game enforces turn order and detects check, checkmate, stalemate
  - make_move() tentatively applies a move, reverts it if it leaves own king in check
  - Pawn promotes to Queen automatically on reaching the back rank
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

    def opponent(self) -> "Color":
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class GameStatus(Enum):
    ACTIVE      = auto()
    WHITE_WINS  = auto()
    BLACK_WINS  = auto()
    STALEMATE   = auto()


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def is_valid(self) -> bool:
        # TODO: Return True if row and col are both in range [0, 7]
        pass


@dataclass
class MoveResult:
    success: bool
    message: str
    captured_piece: Optional["Piece"] = None


class Piece(ABC):
    def __init__(self, color: Color) -> None:
        # TODO: Store color and set has_moved = False
        pass

    @abstractmethod
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        """Return all squares this piece can move to (ignoring check rules)."""

    def _slide(self, board: "Board", pos: Position, directions: list[tuple[int, int]]) -> list[Position]:
        """Generate all squares in given directions until blocked.

        TODO:
            - For each direction (dr, dc), extend from pos one step at a time
            - If square is empty: add it, keep going
            - If square has an enemy piece: add it (capture), stop
            - If square has a friendly piece: stop (don't add)
            - Stop at board boundary (row/col outside 0-7)
        """
        pass


class King(Piece):
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        """King moves one square in any of 8 directions.

        TODO:
            - For each (dr, dc) in all 8 adjacent directions:
              - Compute target = Position(row+dr, col+dc)
              - Skip if not valid or occupied by friendly piece
              - Add to moves list
        """
        pass


class Queen(Piece):
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        # TODO: Use _slide() with all 8 directions (straight + diagonal)
        pass


class Rook(Piece):
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        # TODO: Use _slide() with 4 straight directions: up, down, left, right
        pass


class Bishop(Piece):
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        # TODO: Use _slide() with 4 diagonal directions
        pass


class Knight(Piece):
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        """Knight moves in L-shapes (8 possible offsets).

        TODO:
            - Try all 8 knight offsets: (-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)
            - Skip if target is not valid or occupied by friendly piece
        """
        pass


class Pawn(Piece):
    def get_valid_moves(self, board: "Board", position: Position) -> list[Position]:
        """Pawn movement rules:
          - WHITE moves UP (row decreases), starts at row 6
          - BLACK moves DOWN (row increases), starts at row 1
          - Can move forward 1 square if empty
          - Can move forward 2 squares from starting row if both squares empty
          - Can capture diagonally forward (only if enemy piece present)

        TODO: Implement these rules correctly.
        """
        pass


class Board:
    def __init__(self) -> None:
        # TODO: Create _grid: dict[Position, Piece] = {}
        pass

    def get_piece(self, pos: Position) -> Optional[Piece]:
        # TODO: Return piece at pos or None
        pass

    def set_piece(self, pos: Position, piece: Optional[Piece]) -> None:
        # TODO: If piece is None: remove pos from _grid (pop with default)
        # TODO: If piece is not None: set _grid[pos] = piece
        pass

    def find_king(self, color: Color) -> Optional[Position]:
        # TODO: Scan _grid for a King with the given color; return its Position or None
        pass

    def pieces_of(self, color: Color) -> list[tuple[Position, Piece]]:
        # TODO: Return list of (pos, piece) for all pieces of the given color
        pass

    def setup_standard(self) -> None:
        """Place all 32 pieces in starting positions.

        Back rank order: [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        Black back rank: row 0, White back rank: row 7
        Black pawns: row 1, White pawns: row 6

        TODO: Implement this standard chess setup.
        """
        pass


@dataclass
class Player:
    name: str
    color: Color


class Game:
    def __init__(self, white_name: str, black_name: str) -> None:
        # TODO: Create Player objects for white and black
        # TODO: Create a Board (don't set up pieces yet — that's start_game())
        # TODO: Set _current_color = Color.WHITE
        # TODO: Set _status = GameStatus.ACTIVE
        pass

    def start_game(self) -> None:
        # TODO: Call self._board.setup_standard()
        pass

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        """Attempt to move the piece at from_pos to to_pos.

        TODO:
            - Return False if game is not ACTIVE
            - Return False if no piece at from_pos or it's the wrong color's turn
            - Return False if to_pos not in piece's valid moves
            - Apply move tentatively (move piece on board)
            - Handle pawn promotion: if pawn reaches back rank, replace with Queen
            - If own king is in check after move: UNDO the move, return False
            - Set piece.has_moved = True
            - Switch _current_color to opponent
            - Check for checkmate or stalemate against the opponent
              - Update _status accordingly
            - Return True
        """
        pass

    def get_valid_moves(self, pos: Position) -> list[Position]:
        """Return legal moves for the piece at pos (filters moves that leave king in check).

        TODO:
            - Get raw moves from piece.get_valid_moves()
            - For each target: tentatively apply, check if own king is in check, undo
            - Return only moves that don't leave own king in check
        """
        pass

    def is_in_check(self, color: Color) -> bool:
        """Return True if the king of the given color is under attack.

        TODO:
            - Find king position via board.find_king(color)
            - For each enemy piece, check if king_pos is in its valid moves
        """
        pass

    def is_checkmate(self, color: Color) -> bool:
        # TODO: Return True if in check AND has no legal moves
        pass

    def is_stalemate(self, color: Color) -> bool:
        # TODO: Return True if NOT in check AND has no legal moves
        pass

    def _has_any_legal_move(self, color: Color) -> bool:
        # TODO: Return True if any piece of color has at least one legal move
        pass

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def current_color(self) -> Color:
        return self._current_color

    @property
    def board(self) -> Board:
        return self._board
