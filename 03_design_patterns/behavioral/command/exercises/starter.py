"""
WHAT YOU'RE BUILDING
====================
A drawing canvas that supports undo and redo.

The canvas holds a list of shapes. Three command classes wrap each action:
- AddShapeCommand  — adds a shape to the canvas
- RemoveShapeCommand — removes a shape from the canvas
- MoveShapeCommand — moves a shape by (dx, dy)

The DrawingApp (invoker) keeps an undo stack and a redo stack.
Calling execute() runs a command and pushes it onto the undo stack.
Calling undo() pops the last command and reverses it.
Calling redo() re-executes the last undone command.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


@dataclass
class Shape:
    name: str
    x: float
    y: float


class Canvas:
    def __init__(self) -> None:
        self._shapes: list[Shape] = []

    def add_shape(self, shape: Shape) -> None:
        # TODO: Append shape to self._shapes
        pass

    def remove_shape(self, shape: Shape) -> None:
        # TODO: Remove shape from self._shapes
        pass

    def move_shape(self, shape: Shape, dx: float, dy: float) -> None:
        # TODO: Add dx to shape.x and dy to shape.y
        pass

    @property
    def shapes(self) -> list[Shape]:
        # TODO: Return a copy of self._shapes (so callers can't mutate it)
        pass


class AddShapeCommand(Command):
    def __init__(self, canvas: Canvas, shape: Shape) -> None:
        self._canvas = canvas
        self._shape = shape

    def execute(self) -> None:
        # TODO: Call canvas.add_shape with the stored shape
        pass

    def undo(self) -> None:
        # TODO: Call canvas.remove_shape to reverse the add
        pass


class RemoveShapeCommand(Command):
    def __init__(self, canvas: Canvas, shape: Shape) -> None:
        self._canvas = canvas
        self._shape = shape

    def execute(self) -> None:
        # TODO: Call canvas.remove_shape with the stored shape
        pass

    def undo(self) -> None:
        # TODO: Call canvas.add_shape to restore the removed shape
        pass


class MoveShapeCommand(Command):
    def __init__(self, canvas: Canvas, shape: Shape, dx: float, dy: float) -> None:
        self._canvas = canvas
        self._shape = shape
        self._dx = dx
        self._dy = dy

    def execute(self) -> None:
        # TODO: Call canvas.move_shape(shape, dx, dy)
        pass

    def undo(self) -> None:
        # HINT: To reverse a move of (dx, dy), move by (-dx, -dy)
        # TODO: Call canvas.move_shape with negated dx and dy
        pass


class DrawingApp:
    def __init__(self) -> None:
        self._canvas = Canvas()
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        # HINT: Run the command, add it to the undo stack, and clear the redo stack.
        #       Clearing the redo stack is important: a new action invalidates future redos.
        # TODO: call command.execute(), append to _undo_stack, clear _redo_stack
        pass

    def undo(self) -> None:
        # HINT: Pop from _undo_stack, call undo() on it, push onto _redo_stack.
        #       Do nothing if the stack is empty.
        # TODO: implement undo
        pass

    def redo(self) -> None:
        # HINT: Pop from _redo_stack, call execute() on it, push onto _undo_stack.
        #       Do nothing if the stack is empty.
        # TODO: implement redo
        pass

    @property
    def canvas(self) -> Canvas:
        return self._canvas


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/behavioral/command/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
