"""Command Pattern Exercise — Drawing Canvas Reference Solution."""
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
        self._shapes.append(shape)

    def remove_shape(self, shape: Shape) -> None:
        self._shapes.remove(shape)

    def move_shape(self, shape: Shape, dx: float, dy: float) -> None:
        shape.x += dx
        shape.y += dy

    @property
    def shapes(self) -> list[Shape]:
        return list(self._shapes)


class AddShapeCommand(Command):
    def __init__(self, canvas: Canvas, shape: Shape) -> None:
        self._canvas = canvas
        self._shape = shape

    def execute(self) -> None:
        self._canvas.add_shape(self._shape)

    def undo(self) -> None:
        self._canvas.remove_shape(self._shape)


class RemoveShapeCommand(Command):
    def __init__(self, canvas: Canvas, shape: Shape) -> None:
        self._canvas = canvas
        self._shape = shape

    def execute(self) -> None:
        self._canvas.remove_shape(self._shape)

    def undo(self) -> None:
        self._canvas.add_shape(self._shape)


class MoveShapeCommand(Command):
    def __init__(self, canvas: Canvas, shape: Shape, dx: float, dy: float) -> None:
        self._canvas = canvas
        self._shape = shape
        self._dx = dx
        self._dy = dy

    def execute(self) -> None:
        self._canvas.move_shape(self._shape, self._dx, self._dy)

    def undo(self) -> None:
        self._canvas.move_shape(self._shape, -self._dx, -self._dy)


class DrawingApp:
    def __init__(self) -> None:
        self._canvas = Canvas()
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        if not self._undo_stack:
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)

    @property
    def canvas(self) -> Canvas:
        return self._canvas
