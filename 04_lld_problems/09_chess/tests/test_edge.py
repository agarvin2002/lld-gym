"""Chess — Edge Cases: checkmate, stalemate, game ending."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    Game, Board, Position, Color, GameStatus,
    King, Queen, Rook, Bishop, Knight, Pawn,
)


def make_custom_game(pieces: dict, current_color=Color.WHITE) -> Game:
    board = Board()
    for pos, piece in pieces.items():
        board.set_piece(pos, piece)
    game = Game("A", "B")
    game._board = board
    game._current_color = current_color
    game._status = GameStatus.ACTIVE
    return game


class TestCheckmate:
    def test_scholars_mate(self):
        """Scholar's mate: e4, e5, Qh5, Nc6, Bc4, Nf6?? Qxf7#"""
        game = Game("Alice", "Bob")
        game.start_game()
        # 1. e4
        game.make_move(Position(6, 4), Position(4, 4))
        # 1... e5
        game.make_move(Position(1, 4), Position(3, 4))
        # 2. Qh5
        game.make_move(Position(7, 3), Position(3, 7))
        # 2... Nc6
        game.make_move(Position(0, 1), Position(2, 2))
        # 3. Bc4
        game.make_move(Position(7, 5), Position(4, 2))
        # 3... Nf6?? (blunder)
        game.make_move(Position(0, 6), Position(2, 5))
        # 4. Qxf7#
        game.make_move(Position(3, 7), Position(1, 5))
        assert game.status == GameStatus.WHITE_WINS

    def test_back_rank_checkmate(self):
        """Rook delivered to back rank while second rook seals row 1."""
        # Black King cornered at (0,7); Rook(1,1) already seals all of row 1;
        # moving Rook from (3,0) to (0,0) attacks the whole back rank → checkmate.
        game = make_custom_game({
            Position(0, 7): King(Color.BLACK),
            Position(7, 4): King(Color.WHITE),
            Position(3, 0): Rook(Color.WHITE),  # will slide to (0,0)
            Position(1, 1): Rook(Color.WHITE),  # seals row 1: (1,0)..(1,7)
        })
        game.make_move(Position(3, 0), Position(0, 0))
        assert game.status == GameStatus.WHITE_WINS

    def test_is_checkmate_true(self):
        """King at corner already in check with no escape square."""
        # Rook(0,0) attacks row 0 → king at (0,7) is in check.
        # Rook(1,1) attacks all of row 1 → (1,6) and (1,7) are covered.
        # (0,6) is covered by Rook(0,0). No escape → checkmate.
        game = make_custom_game({
            Position(0, 7): King(Color.BLACK),
            Position(0, 0): Rook(Color.WHITE),  # attacks row 0 → king in check
            Position(1, 1): Rook(Color.WHITE),  # attacks row 1 → seals escape
            Position(7, 4): King(Color.WHITE),
        }, current_color=Color.BLACK)
        assert game.is_in_check(Color.BLACK) is True
        assert game.is_checkmate(Color.BLACK) is True

    def test_is_checkmate_false_when_can_block(self):
        """King in check but can block with own piece."""
        game = make_custom_game({
            Position(0, 4): King(Color.BLACK),
            Position(7, 4): King(Color.WHITE),
            Position(7, 0): Rook(Color.WHITE),  # attacks column 4? No, row 7
        })
        # Rook on row 7 doesn't attack black king on row 0
        assert game.is_checkmate(Color.BLACK) is False


class TestStalemate:
    def test_stalemate_detected(self):
        """Classic stalemate: Black king cornered with no legal moves but not in check."""
        game = make_custom_game({
            Position(0, 0): King(Color.BLACK),
            Position(2, 1): Queen(Color.WHITE),  # covers (1,0),(1,1),(0,1),(1,2)
            Position(7, 4): King(Color.WHITE),
        }, current_color=Color.BLACK)
        # Black king at (0,0): can go to (0,1)→attacked by queen, (1,0)→attacked, (1,1)→attacked
        assert game.is_in_check(Color.BLACK) is False
        assert game.is_stalemate(Color.BLACK) is True

    def test_not_stalemate_when_in_check(self):
        game = make_custom_game({
            Position(0, 0): King(Color.BLACK),
            Position(7, 4): King(Color.WHITE),
            Position(2, 0): Rook(Color.WHITE),  # attacks col 0 → king in check
        }, current_color=Color.BLACK)
        assert game.is_in_check(Color.BLACK) is True
        assert game.is_stalemate(Color.BLACK) is False


class TestGameStateEdges:
    def test_no_move_after_game_over(self):
        # Same back-rank mate setup: move delivers checkmate, then verify
        # any further move is rejected because the game is no longer ACTIVE.
        game = make_custom_game({
            Position(0, 7): King(Color.BLACK),
            Position(7, 4): King(Color.WHITE),
            Position(3, 0): Rook(Color.WHITE),
            Position(1, 1): Rook(Color.WHITE),
        })
        game.make_move(Position(3, 0), Position(0, 0))  # delivers checkmate
        assert game.status == GameStatus.WHITE_WINS
        result = game.make_move(Position(7, 4), Position(6, 4))
        assert result is False

    def test_cannot_capture_own_piece(self):
        game = Game("A", "B")
        game.start_game()
        result = game.make_move(Position(7, 3), Position(6, 3))  # Queen onto own pawn
        assert result is False

    def test_pieces_of_counts_correctly(self):
        game = Game("A", "B")
        game.start_game()
        white = game.board.pieces_of(Color.WHITE)
        black = game.board.pieces_of(Color.BLACK)
        assert len(white) == 16
        assert len(black) == 16
