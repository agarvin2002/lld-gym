"""Snake and Ladders — Extended Tests."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import Board, Game, GameStatus


class TestSnakesAndLadders:
    def _game_with_fixtures(self, die_value):
        board = Board(100)
        board.add_snake(50, 20)
        board.add_ladder(10, 60)
        return Game(board, die=lambda: die_value), board

    def test_snake_teleports_player(self):
        board = Board(100)
        board.add_snake(30, 5)
        game = Game(board, die=lambda: 30)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        result = game.roll_and_move()
        assert result.teleported_to == 5
        assert alice.position == 5

    def test_ladder_teleports_player(self):
        board = Board(100)
        board.add_ladder(6, 80)
        game = Game(board, die=lambda: 6)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        result = game.roll_and_move()
        assert result.teleported_to == 80
        assert alice.position == 80

    def test_no_teleport_on_plain_square(self):
        board = Board(100)
        board.add_snake(50, 20)
        game = Game(board, die=lambda: 3)
        game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        result = game.roll_and_move()
        assert result.teleported_to is None

    def test_four_players_round_robin(self):
        board = Board(100)
        names = ["A", "B", "C", "D"]
        game = Game(board, die=lambda: 1)
        players = [game.add_player(n) for n in names]
        game.start()
        for i in range(4):
            assert game.current_player() is players[i]
            game.roll_and_move()
        # After full round, back to first player
        assert game.current_player() is players[0]


class TestWinCondition:
    def test_win_at_exactly_100(self):
        board = Board(100)
        game = Game(board, die=lambda: 4)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        alice.position = 96
        result = game.roll_and_move()
        assert result.won is True
        assert alice.position == 100
        assert game.status == GameStatus.FINISHED
        assert game.winner() is alice

    def test_no_roll_after_win(self):
        board = Board(100)
        game = Game(board, die=lambda: 4)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        alice.position = 96
        game.roll_and_move()
        with pytest.raises(ValueError):
            game.roll_and_move()

    def test_winner_is_none_during_game(self):
        board = Board(100)
        game = Game(board, die=lambda: 2)
        game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        assert game.winner() is None

    def test_bounce_does_not_win(self):
        board = Board(100)
        game = Game(board, die=lambda: 6)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        alice.position = 98
        result = game.roll_and_move()
        assert result.won is False
        assert alice.position == 98  # bounce, not win

    def test_land_on_snake_after_near_win(self):
        """Landing exactly on a snake head even near 100 sends player down."""
        board = Board(100)
        board.add_snake(99, 50)
        game = Game(board, die=lambda: 5)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        alice.position = 94
        result = game.roll_and_move()  # 94 + 5 = 99 → snake to 50
        assert alice.position == 50
        assert result.won is False
