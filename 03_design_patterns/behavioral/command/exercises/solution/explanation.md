# Explanation: Command Pattern — Drawing Canvas

## Core Roles

| Role | Class | Responsibility |
|------|-------|----------------|
| Command (interface) | `Command` ABC | Defines `execute()` + `undo()` |
| Receiver | `Canvas` | Knows how to actually do the work |
| Concrete Commands | `AddShapeCommand` etc. | Delegate to Canvas; store undo data |
| Invoker | `DrawingApp` | Manages stacks; knows nothing about shapes |

## Why the Invoker knows nothing about shapes

`DrawingApp.execute()` accepts any `Command` — it doesn't care if it's an add, remove, or move. Adding a new operation (e.g., `ResizeShapeCommand`) requires **zero changes** to `DrawingApp`. This is the Open/Closed Principle in action.

## The undo stack loop

```
execute(cmd) → cmd.execute() → push undo_stack → clear redo_stack
undo()       → pop undo_stack → cmd.undo()    → push redo_stack
redo()       → pop redo_stack → cmd.execute() → push undo_stack
```

Why clear redo on `execute()`? If the user undoes two steps then makes a new edit, the future they "undid toward" no longer exists. Clearing prevents stale redos.

## MoveShapeCommand: storing state vs reversing math

Two valid approaches:

1. **Reverse math** (used here): `undo()` moves by `(-dx, -dy)`. Simple, no extra storage.
2. **Snapshot**: store `_prev_x, _prev_y` before `execute()`. Safer if the shape could be moved by other means between execute and undo.

For this exercise where commands are the only way to mutate shapes, reverse math is correct and simpler.

## DeleteCommand pattern: capture before deleting

`RemoveShapeCommand` just holds a reference to the shape object. The shape object isn't destroyed — Python keeps it alive via the reference in the command. `undo()` simply re-adds the same object. No need to copy or serialize.

## Redo stack clears correctly

The test `test_new_execute_clears_redo_stack` verifies: after undo → new execute → redo, the redo is a no-op. The new execute represents a branch in the edit history; the old redo branch is discarded.
