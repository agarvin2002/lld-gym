"""Tests for Command Pattern — Drawing Canvas."""
import sys, os
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import Canvas, Shape, AddShapeCommand, RemoveShapeCommand, MoveShapeCommand, DrawingApp


def make_app():
    return DrawingApp()


def make_shape(name="Circle", x=0.0, y=0.0):
    return Shape(name=name, x=x, y=y)


# ── Canvas direct tests ────────────────────────────────────────────────────────

class TestCanvas:
    def test_starts_empty(self):
        c = Canvas()
        assert c.shapes == []

    def test_add_shape(self):
        c = Canvas()
        s = make_shape()
        c.add_shape(s)
        assert s in c.shapes

    def test_remove_shape(self):
        c = Canvas()
        s = make_shape()
        c.add_shape(s)
        c.remove_shape(s)
        assert s not in c.shapes

    def test_move_shape(self):
        c = Canvas()
        s = make_shape(x=1.0, y=2.0)
        c.add_shape(s)
        c.move_shape(s, 3.0, 4.0)
        assert s.x == pytest.approx(4.0)
        assert s.y == pytest.approx(6.0)

    def test_shapes_returns_copy(self):
        c = Canvas()
        s = make_shape()
        c.add_shape(s)
        snapshot = c.shapes
        c.remove_shape(s)
        assert s in snapshot          # snapshot not affected by later changes


# ── AddShapeCommand ────────────────────────────────────────────────────────────

class TestAddShapeCommand:
    def test_execute_adds_shape(self):
        c = Canvas()
        s = make_shape()
        cmd = AddShapeCommand(c, s)
        cmd.execute()
        assert s in c.shapes

    def test_undo_removes_shape(self):
        c = Canvas()
        s = make_shape()
        cmd = AddShapeCommand(c, s)
        cmd.execute()
        cmd.undo()
        assert s not in c.shapes


# ── RemoveShapeCommand ────────────────────────────────────────────────────────

class TestRemoveShapeCommand:
    def test_execute_removes_shape(self):
        c = Canvas()
        s = make_shape()
        c.add_shape(s)
        cmd = RemoveShapeCommand(c, s)
        cmd.execute()
        assert s not in c.shapes

    def test_undo_restores_shape(self):
        c = Canvas()
        s = make_shape()
        c.add_shape(s)
        cmd = RemoveShapeCommand(c, s)
        cmd.execute()
        cmd.undo()
        assert s in c.shapes


# ── MoveShapeCommand ──────────────────────────────────────────────────────────

class TestMoveShapeCommand:
    def test_execute_moves_shape(self):
        c = Canvas()
        s = make_shape(x=0.0, y=0.0)
        c.add_shape(s)
        cmd = MoveShapeCommand(c, s, 5.0, 3.0)
        cmd.execute()
        assert s.x == pytest.approx(5.0)
        assert s.y == pytest.approx(3.0)

    def test_undo_restores_position(self):
        c = Canvas()
        s = make_shape(x=1.0, y=2.0)
        c.add_shape(s)
        cmd = MoveShapeCommand(c, s, 10.0, 20.0)
        cmd.execute()
        cmd.undo()
        assert s.x == pytest.approx(1.0)
        assert s.y == pytest.approx(2.0)


# ── DrawingApp (Invoker) ──────────────────────────────────────────────────────

class TestDrawingApp:
    def test_execute_adds_shape_to_canvas(self):
        app = make_app()
        s = make_shape()
        app.execute(AddShapeCommand(app.canvas, s))
        assert s in app.canvas.shapes

    def test_undo_reverses_add(self):
        app = make_app()
        s = make_shape()
        app.execute(AddShapeCommand(app.canvas, s))
        app.undo()
        assert s not in app.canvas.shapes

    def test_redo_reapplies_add(self):
        app = make_app()
        s = make_shape()
        app.execute(AddShapeCommand(app.canvas, s))
        app.undo()
        app.redo()
        assert s in app.canvas.shapes

    def test_undo_empty_stack_is_noop(self):
        app = make_app()
        app.undo()  # should not raise

    def test_redo_empty_stack_is_noop(self):
        app = make_app()
        app.redo()  # should not raise

    def test_new_execute_clears_redo_stack(self):
        app = make_app()
        s1 = make_shape("A")
        s2 = make_shape("B")
        app.execute(AddShapeCommand(app.canvas, s1))
        app.undo()                              # s1 removed; s1 on redo stack
        app.execute(AddShapeCommand(app.canvas, s2))  # clears redo stack
        app.redo()                              # no-op (redo stack cleared)
        assert s1 not in app.canvas.shapes      # redo for s1 was lost

    def test_multiple_undo_redo(self):
        app = make_app()
        s1 = make_shape("A", 0, 0)
        s2 = make_shape("B", 5, 5)
        app.execute(AddShapeCommand(app.canvas, s1))
        app.execute(AddShapeCommand(app.canvas, s2))
        app.undo()   # removes s2
        app.undo()   # removes s1
        assert app.canvas.shapes == []
        app.redo()   # re-adds s1
        app.redo()   # re-adds s2
        assert s1 in app.canvas.shapes
        assert s2 in app.canvas.shapes

    def test_move_undo_redo(self):
        app = make_app()
        s = make_shape(x=0.0, y=0.0)
        app.execute(AddShapeCommand(app.canvas, s))
        app.execute(MoveShapeCommand(app.canvas, s, 10.0, 5.0))
        assert s.x == pytest.approx(10.0)
        app.undo()
        assert s.x == pytest.approx(0.0)
        app.redo()
        assert s.x == pytest.approx(10.0)
