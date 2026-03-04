"""Snake and Ladders — Basic Tests."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import Board, Game, Player, MoveResult, GameStatus


def make_game(die_value=None):
    board = Board(size=100)
    die = (lambda: die_value) if die_value else None
    return Game(board, die=die)


class TestBoard:
    def test_size_default(self):
        b = Board()
        assert b.size == 100

    def test_resolve_no_special(self):
        b = Board()
        assert b.resolve(50) == 50

    def test_snake_sends_down(self):
        b = Board()
        b.add_snake(50, 10)
        assert b.resolve(50) == 10

    def test_ladder_sends_up(self):
        b = Board()
        b.add_ladder(10, 50)
        assert b.resolve(10) == 50

    def test_resolve_unrelated_square(self):
        b = Board()
        b.add_snake(50, 10)
        b.add_ladder(20, 80)
        assert b.resolve(30) == 30

    def test_snake_validation(self):
        b = Board()
        with pytest.raises(ValueError):
            b.add_snake(10, 50)  # head must be above tail

    def test_ladder_validation(self):
        b = Board()
        with pytest.raises(ValueError):
            b.add_ladder(80, 10)  # top must be above base


class TestGameSetup:
    def test_initial_status_waiting(self):
        g = make_game()
        assert g.status == GameStatus.WAITING

    def test_add_player_returns_player(self):
        g = make_game()
        p = g.add_player("Alice")
        assert isinstance(p, Player)
        assert p.name == "Alice"

    def test_player_starts_at_zero(self):
        g = make_game()
        p = g.add_player("Alice")
        assert p.position == 0

    def test_cannot_add_player_after_start(self):
        g = make_game(die_value=3)
        g.add_player("Alice")
        g.add_player("Bob")
        g.start()
        with pytest.raises(ValueError):
            g.add_player("Charlie")

    def test_start_requires_two_players(self):
        g = make_game()
        g.add_player("Solo")
        with pytest.raises(ValueError):
            g.start()

    def test_status_in_progress_after_start(self):
        g = make_game(die_value=3)
        g.add_player("Alice")
        g.add_player("Bob")
        g.start()
        assert g.status == GameStatus.IN_PROGRESS


class TestRollAndMove:
    def test_player_advances(self):
        g = make_game(die_value=5)
        alice = g.add_player("Alice")
        g.add_player("Bob")
        g.start()
        result = g.roll_and_move()
        assert result.roll == 5
        assert alice.position == 5

    def test_move_result_fields(self):
        g = make_game(die_value=3)
        g.add_player("Alice")
        g.add_player("Bob")
        g.start()
        r = g.roll_and_move()
        assert r.player_name == "Alice"
        assert r.roll == 3
        assert r.from_pos == 0
        assert r.to_pos == 3
        assert r.won is False
        assert r.teleported_to is None

    def test_turn_alternates(self):
        g = make_game(die_value=2)
        alice = g.add_player("Alice")
        bob = g.add_player("Bob")
        g.start()
        g.roll_and_move()  # Alice moves
        assert g.current_player() is bob
        g.roll_and_move()  # Bob moves
        assert g.current_player() is alice

    def test_cannot_roll_before_start(self):
        g = make_game(die_value=3)
        g.add_player("Alice")
        g.add_player("Bob")
        with pytest.raises(ValueError):
            g.roll_and_move()

    def test_bounce_rule(self):
        board = Board(size=100)
        g = Game(board, die=lambda: 6)
        alice = g.add_player("Alice")
        g.add_player("Bob")
        g.start()
        # Move alice to 98 manually
        alice.position = 98
        result = g.roll_and_move()  # 98 + 6 = 104 > 100 → stay at 98
        assert alice.position == 98
        assert result.to_pos == 98
