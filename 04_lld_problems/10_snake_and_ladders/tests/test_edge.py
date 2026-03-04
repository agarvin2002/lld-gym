"""Snake and Ladders — Edge Cases."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import Board, Game, GameStatus


class TestBoardEdgeCases:
    def test_snake_at_99(self):
        b = Board()
        b.add_snake(99, 1)
        assert b.resolve(99) == 1

    def test_ladder_from_1_to_100(self):
        b = Board()
        b.add_ladder(1, 100)
        assert b.resolve(1) == 100

    def test_multiple_snakes(self):
        b = Board()
        b.add_snake(80, 10)
        b.add_snake(60, 5)
        assert b.resolve(80) == 10
        assert b.resolve(60) == 5
        assert b.resolve(70) == 70

    def test_snake_priority_over_ladder(self):
        """Same square can't be both, but resolve checks snakes first."""
        b = Board()
        b.add_snake(50, 20)
        assert b.resolve(50) == 20


class TestGameEdgeCases:
    def test_exact_win_no_bounce(self):
        board = Board(size=10)
        game = Game(board, die=lambda: 4)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        alice.position = 6
        result = game.roll_and_move()
        assert alice.position == 10
        assert result.won is True

    def test_three_players_turn_order(self):
        board = Board(100)
        game = Game(board, die=lambda: 1)
        players = [game.add_player(n) for n in ["A", "B", "C"]]
        game.start()
        for _ in range(9):
            game.roll_and_move()
        # After 9 moves (3 rounds), back to A
        assert game.current_player() is players[0]

    def test_game_with_die_injection(self):
        """Die injection ensures deterministic tests."""
        rolls = iter([3, 5, 2, 6])
        board = Board(100)
        game = Game(board, die=lambda: next(rolls))
        alice = game.add_player("Alice")
        bob = game.add_player("Bob")
        game.start()
        game.roll_and_move()   # Alice: 0+3=3
        game.roll_and_move()   # Bob: 0+5=5
        assert alice.position == 3
        assert bob.position == 5

    def test_winner_stays_after_game_ends(self):
        board = Board(10)
        game = Game(board, die=lambda: 10)
        alice = game.add_player("Alice")
        game.add_player("Bob")
        game.start()
        game.roll_and_move()
        assert game.winner() is alice
        assert game.status == GameStatus.FINISHED
