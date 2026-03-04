"""Chess Game — Reference Solution."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

    def opponent(self) -> Color:
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
        return 0 <= self.row <= 7 and 0 <= self.col <= 7


@dataclass
class MoveResult:
    success: bool
    message: str
    captured_piece: Optional[Piece] = None


class Piece(ABC):
    def __init__(self, color: Color) -> None:
        self.color = color
        self.has_moved = False

    @abstractmethod
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        """Return all squares this piece can move to (ignoring check)."""

    def _slide(self, board: Board, pos: Position, directions: list[tuple[int, int]]) -> list[Position]:
        """Generate all squares in given directions until blocked."""
        moves = []
        for dr, dc in directions:
            r, c = pos.row + dr, pos.col + dc
            while 0 <= r <= 7 and 0 <= c <= 7:
                target = Position(r, c)
                occupant = board.get_piece(target)
                if occupant is None:
                    moves.append(target)
                elif occupant.color != self.color:
                    moves.append(target)  # capture
                    break
                else:
                    break  # blocked by own piece
                r += dr
                c += dc
        return moves


class King(Piece):
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                target = Position(position.row + dr, position.col + dc)
                if not target.is_valid():
                    continue
                occupant = board.get_piece(target)
                if occupant is None or occupant.color != self.color:
                    moves.append(target)
        return moves


class Queen(Piece):
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        return self._slide(board, position, [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1),
        ])


class Rook(Piece):
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        return self._slide(board, position, [(-1, 0), (1, 0), (0, -1), (0, 1)])


class Bishop(Piece):
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        return self._slide(board, position, [(-1, -1), (-1, 1), (1, -1), (1, 1)])


class Knight(Piece):
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        moves = []
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            target = Position(position.row + dr, position.col + dc)
            if not target.is_valid():
                continue
            occupant = board.get_piece(target)
            if occupant is None or occupant.color != self.color:
                moves.append(target)
        return moves


class Pawn(Piece):
    def get_valid_moves(self, board: Board, position: Position) -> list[Position]:
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1

        # Single forward step
        fwd = Position(position.row + direction, position.col)
        if fwd.is_valid() and board.get_piece(fwd) is None:
            moves.append(fwd)
            # Double step from starting row
            if position.row == start_row:
                fwd2 = Position(position.row + 2 * direction, position.col)
                if board.get_piece(fwd2) is None:
                    moves.append(fwd2)

        # Diagonal captures
        for dc in (-1, 1):
            cap = Position(position.row + direction, position.col + dc)
            if cap.is_valid():
                occupant = board.get_piece(cap)
                if occupant is not None and occupant.color != self.color:
                    moves.append(cap)

        return moves


class Board:
    def __init__(self) -> None:
        self._grid: dict[Position, Piece] = {}

    def get_piece(self, pos: Position) -> Optional[Piece]:
        return self._grid.get(pos)

    def set_piece(self, pos: Position, piece: Optional[Piece]) -> None:
        if piece is None:
            self._grid.pop(pos, None)
        else:
            self._grid[pos] = piece

    def find_king(self, color: Color) -> Optional[Position]:
        for pos, piece in self._grid.items():
            if isinstance(piece, King) and piece.color == color:
                return pos
        return None

    def pieces_of(self, color: Color) -> list[tuple[Position, Piece]]:
        return [(pos, p) for pos, p in self._grid.items() if p.color == color]

    def setup_standard(self) -> None:
        """Place all 32 pieces in their starting positions."""
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, cls in enumerate(back_rank):
            self.set_piece(Position(0, col), cls(Color.BLACK))
            self.set_piece(Position(7, col), cls(Color.WHITE))
        for col in range(8):
            self.set_piece(Position(1, col), Pawn(Color.BLACK))
            self.set_piece(Position(6, col), Pawn(Color.WHITE))


@dataclass
class Player:
    name: str
    color: Color


class Game:
    def __init__(self, white_name: str, black_name: str) -> None:
        self._white = Player(white_name, Color.WHITE)
        self._black = Player(black_name, Color.BLACK)
        self._board = Board()
        self._current_color = Color.WHITE
        self._status = GameStatus.ACTIVE

    def start_game(self) -> None:
        self._board.setup_standard()

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        if self._status != GameStatus.ACTIVE:
            return False

        piece = self._board.get_piece(from_pos)
        if piece is None or piece.color != self._current_color:
            return False

        valid_moves = piece.get_valid_moves(self._board, from_pos)
        if to_pos not in valid_moves:
            return False

        # Apply tentatively
        captured = self._board.get_piece(to_pos)
        self._board.set_piece(to_pos, piece)
        self._board.set_piece(from_pos, None)

        # Pawn promotion
        if isinstance(piece, Pawn):
            last_rank = 0 if piece.color == Color.WHITE else 7
            if to_pos.row == last_rank:
                self._board.set_piece(to_pos, Queen(piece.color))

        # Reject if own king left in check
        if self.is_in_check(self._current_color):
            # Undo
            self._board.set_piece(from_pos, piece)
            self._board.set_piece(to_pos, captured)
            return False

        piece.has_moved = True

        # Switch turns
        self._current_color = self._current_color.opponent()

        # Check game-ending conditions for the opponent
        opp = self._current_color
        if self.is_checkmate(opp):
            self._status = (
                GameStatus.WHITE_WINS if opp == Color.BLACK else GameStatus.BLACK_WINS
            )
        elif self.is_stalemate(opp):
            self._status = GameStatus.STALEMATE

        return True

    def get_valid_moves(self, pos: Position) -> list[Position]:
        piece = self._board.get_piece(pos)
        if piece is None:
            return []
        raw_moves = piece.get_valid_moves(self._board, pos)
        legal = []
        for target in raw_moves:
            captured = self._board.get_piece(target)
            self._board.set_piece(target, piece)
            self._board.set_piece(pos, None)
            if not self.is_in_check(piece.color):
                legal.append(target)
            self._board.set_piece(pos, piece)
            self._board.set_piece(target, captured)
        return legal

    def is_in_check(self, color: Color) -> bool:
        king_pos = self._board.find_king(color)
        if king_pos is None:
            return False
        for pos, piece in self._board.pieces_of(color.opponent()):
            if king_pos in piece.get_valid_moves(self._board, pos):
                return True
        return False

    def is_checkmate(self, color: Color) -> bool:
        if not self.is_in_check(color):
            return False
        return not self._has_any_legal_move(color)

    def is_stalemate(self, color: Color) -> bool:
        if self.is_in_check(color):
            return False
        return not self._has_any_legal_move(color)

    def _has_any_legal_move(self, color: Color) -> bool:
        for pos, piece in self._board.pieces_of(color):
            if self.get_valid_moves(pos):
                return True
        return False

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def current_color(self) -> Color:
        return self._current_color

    @property
    def board(self) -> Board:
        return self._board
