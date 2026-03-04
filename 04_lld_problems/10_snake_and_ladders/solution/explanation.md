# Snake and Ladders — Solution Explanation

## Key Design Decisions

### Board is responsible for resolution
`Board.resolve(position)` encapsulates the snake/ladder lookup. The `Game` never directly touches the snake or ladder dictionaries — this is the **single responsibility principle** in action. If you wanted to add a "wormhole" (teleport to random square), you'd only change `Board.resolve`.

### Dependency injection for the die
```python
die: Callable[[], int] | None = None
self._die = die or (lambda: random.randint(1, 6))
```
Injecting the die makes the game fully deterministic in tests without mocking. `Game(board, die=lambda: 4)` always rolls 4. This is cleaner than patching `random.randint`.

### Bounce rule: stay in place
```python
if new_pos > self._board.size:
    new_pos = player.position
```
Standard rule: cannot exceed 100. The alternative (exact roll required to win) is a common variant — the problem.md specifies stay-in-place.

### Turn advancement only on non-winning move
```python
if won:
    self._winner = player
    self._status = GameStatus.FINISHED
else:
    self._current_index = (self._current_index + 1) % len(self._players)
```
The winner's turn doesn't advance — the game is simply over. Attempting to `roll_and_move` after `FINISHED` raises `ValueError`, preventing stale state.

### MoveResult captures full context
`MoveResult` is a snapshot of what happened on a turn: `from_pos`, `to_pos`, `teleported_to`, `won`. This makes it easy to build a game log, replay moves, or display a UI without keeping extra state.

### `teleported_to` is None vs. the destination
```python
teleported_to = resolved if resolved != new_pos else None
```
`None` means "landed on a plain square". A non-None value means a snake or ladder was triggered. This distinction matters for UI (show animation vs. don't).
