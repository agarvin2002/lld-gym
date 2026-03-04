# Exercise: Drawing Canvas (Command Pattern)

## Problem

Implement a drawing canvas that supports undo/redo for all drawing operations.

## What to Build

### `Command` (ABC)
Abstract base with `execute()` and `undo()` methods.

### `Canvas`
The **receiver** — stores a list of `Shape` objects.

| Method | Description |
|--------|-------------|
| `add_shape(shape)` | Append a shape to the canvas |
| `remove_shape(shape)` | Remove a shape from the canvas |
| `move_shape(shape, dx, dy)` | Translate a shape's position |
| `shapes` | Property returning list of shapes |

### `Shape`
Simple dataclass: `name: str`, `x: float`, `y: float`.

### Concrete Commands

| Class | `execute()` | `undo()` |
|-------|-------------|----------|
| `AddShapeCommand` | Calls `canvas.add_shape(shape)` | Calls `canvas.remove_shape(shape)` |
| `RemoveShapeCommand` | Calls `canvas.remove_shape(shape)` | Calls `canvas.add_shape(shape)` |
| `MoveShapeCommand` | Moves by `(dx, dy)` | Moves by `(-dx, -dy)` |

### `DrawingApp` (Invoker)

| Method | Description |
|--------|-------------|
| `execute(command)` | Runs the command and pushes to undo stack; clears redo stack |
| `undo()` | Pops from undo stack, calls `undo()`, pushes to redo stack |
| `redo()` | Pops from redo stack, calls `execute()`, pushes to undo stack |
| `canvas` | Property returning the `Canvas` |

## Constraints
- `undo()` / `redo()` on an empty stack should be a no-op (no exception)
- After any new `execute()`, the redo stack must be cleared
- `MoveShapeCommand.undo()` must restore the shape to its exact original position

## Starter File
Edit `starter.py`. Run tests with:
```bash
pytest tests.py -v
```
