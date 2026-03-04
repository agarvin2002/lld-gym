"""Chess — Basic Tests: board setup, piece moves, basic game flow."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    Game, Board, Position, Color, GameStatus,
    King, Queen, Rook, Bishop, Knight, Pawn,
)


@pytest.fixture
def game():
    g = Game("Alice", "Bob")
    g.start_game()
    return g


class TestBoardSetup:
    def test_white_king_position(self, game):
        king_pos = game.board.find_king(Color.WHITE)
        assert king_pos == Position(7, 4)

    def test_black_king_position(self, game):
        king_pos = game.board.find_king(Color.BLACK)
        assert king_pos == Position(0, 4)

    def test_white_pawn_row(self, game):
        for col in range(8):
            piece = game.board.get_piece(Position(6, col))
            assert isinstance(piece, Pawn)
            assert piece.color == Color.WHITE

    def test_black_pawn_row(self, game):
        for col in range(8):
            piece = game.board.get_piece(Position(1, col))
            assert isinstance(piece, Pawn)
            assert piece.color == Color.BLACK

    def test_empty_middle_squares(self, game):
        for row in range(2, 6):
            for col in range(8):
                assert game.board.get_piece(Position(row, col)) is None

    def test_32_pieces_on_board(self, game):
        count = sum(1 for r in range(8) for c in range(8)
                    if game.board.get_piece(Position(r, c)) is not None)
        assert count == 32


class TestPieceMoves:
    def test_pawn_can_move_one_forward(self, game):
        moves = game.get_valid_moves(Position(6, 4))  # e2 pawn
        assert Position(5, 4) in moves

    def test_pawn_can_move_two_forward_from_start(self, game):
        moves = game.get_valid_moves(Position(6, 4))
        assert Position(4, 4) in moves

    def test_knight_moves_from_start(self, game):
        moves = game.get_valid_moves(Position(7, 1))  # b1 knight
        assert Position(5, 0) in moves
        assert Position(5, 2) in moves

    def test_no_moves_for_empty_square(self, game):
        moves = game.get_valid_moves(Position(4, 4))
        assert moves == []

    def test_no_moves_for_blocked_pawn(self):
        board = Board()
        board.set_piece(Position(4, 4), Pawn(Color.WHITE))
        board.set_piece(Position(3, 4), Pawn(Color.BLACK))  # blocked
        board.set_piece(Position(7, 4), King(Color.WHITE))
        board.set_piece(Position(0, 4), King(Color.BLACK))
        game = Game("A", "B")
        game._board = board
        game._current_color = Color.WHITE
        game._status = GameStatus.ACTIVE
        moves = game.get_valid_moves(Position(4, 4))
        assert Position(3, 4) not in moves


class TestMakeMove:
    def test_white_pawn_advance(self, game):
        result = game.make_move(Position(6, 4), Position(4, 4))  # e2→e4
        assert result is True

    def test_white_moves_first(self, game):
        assert game.current_color == Color.WHITE

    def test_color_alternates(self, game):
        game.make_move(Position(6, 4), Position(4, 4))
        assert game.current_color == Color.BLACK

    def test_invalid_move_wrong_color(self, game):
        result = game.make_move(Position(1, 4), Position(3, 4))  # Black pawn, White's turn
        assert result is False

    def test_invalid_destination(self, game):
        result = game.make_move(Position(6, 4), Position(3, 4))  # 3-step pawn
        assert result is False

    def test_move_updates_board(self, game):
        game.make_move(Position(6, 4), Position(4, 4))
        assert game.board.get_piece(Position(6, 4)) is None
        assert game.board.get_piece(Position(4, 4)) is not None

    def test_game_starts_active(self, game):
        assert game.status == GameStatus.ACTIVE
