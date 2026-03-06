# Design — Snake and Ladders

## Clarifying Questions (Interview Simulation)

Before drawing any class diagram, ask these in an interview:

1. How big is the board? → Configurable, default 100.
2. How many players? → At least 2, no hard upper limit.
3. What happens when a player rolls past the end? → Bounce: stay at current position.
4. Can snakes and ladders overlap? → No, each cell has at most one.
5. How is the die rolled? → Random 1-6; but should be injectable for testing.
6. What data does a move return? → Player name, roll, from/to positions, snake/ladder effect, won flag.
7. Is this turn-based? → Yes, strictly round-robin.
8. What happens after someone wins? → Game is FINISHED; no more moves allowed.

---

## Core Entities

### 1. Player (Data Class)
Holds player name and current position (starts at 0). Position 0 = before the board.
Winning condition: position equals board.size (e.g., 100).

### 2. MoveResult (Data Class)
Immutable record of what happened during a turn: roll value, from/to positions,
whether a snake/ladder was triggered (teleported_to), and whether the player won.

### 3. Board
Encapsulates the board rules: size, snakes dict (head→tail), ladders dict (base→top).
`resolve(position)` applies any snake or ladder and returns the final position.
Validates snake/ladder placement on registration.

### 4. Game
Central coordinator: manages player list, turn order, status, die injection.
`add_player()` — only before start. `start()` — requires ≥ 2 players.
`roll_and_move()` — performs a full turn and returns MoveResult.

---

## Class Diagram (ASCII)

```
+---------------------+
|        Game         |
+---------------------+
| - _board: Board     |------>  Board
| - _die: Callable    |
| - _players: list    |------>  Player (1..*)
| - _status: Enum     |
| - _current_index    |
| - _winner: Player?  |
+---------------------+
| + add_player(name)  |
| + start()           |
| + roll_and_move()   |------>  MoveResult
| + current_player()  |
| + winner()          |
+---------------------+

+------------------------+        +------------------+
|         Board          |        |     Player       |
+------------------------+        +------------------+
| - _size: int           |        | name: str        |
| - _snakes: dict[int,int]|       | position: int    |
| - _ladders: dict[int,int]|      +------------------+
+------------------------+
| + add_snake(head, tail)|        +---------------------------+
| + add_ladder(base, top)|        |        MoveResult         |
| + resolve(pos) -> int  |        +---------------------------+
| + size: int (property) |        | player_name: str          |
+------------------------+        | roll: int                 |
                                  | from_pos: int             |
                                  | to_pos: int               |
                                  | teleported_to: int | None |
                                  | won: bool                 |
                                  +---------------------------+
```

---

## Game Status State Machine

```
 WAITING ──start()──> IN_PROGRESS ──(winner)──> FINISHED
```

---

## Turn Flow

```
roll_and_move():
    1. Raise ValueError if not IN_PROGRESS
    2. Roll die → roll = self._die()
    3. raw_pos = player.position + roll
    4. If raw_pos > board.size: stay (bounce rule)
    5. resolved = board.resolve(raw_pos)
    6. teleported_to = resolved if resolved != raw_pos else None
    7. player.position = resolved
    8. If player.position == board.size: WINNER → status = FINISHED
    9. Else: advance current_index (circular)
    10. Return MoveResult
```

---

## Key Design Decisions

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Injected die (Callable) | Fully testable without randomness | Callers must pass `lambda: 4` in tests |
| Board.resolve() as pure function | Stateless — easy to test in isolation | |
| MoveResult dataclass | Rich return type — no need to query state after each move | Slightly more verbose |
| Circular _current_index | Simple round-robin without removing players from list | |
| Bounce rule | Standard Snake & Ladders rule | Some variants allow exceeding |

---

## Extensibility

**Add multiple dice:**
- Change `die: Callable[[], int]` to accept a list of callables and sum results.

**Add power-ups or special cells:**
- Add a `special_cells: dict[int, Callable[[Player], None]]` dict to Board.
- Call in `resolve()` or separately in `roll_and_move()`.

**Add undo/replay:**
- Store move history as a `list[MoveResult]`.
- Snapshot player positions at each turn.
