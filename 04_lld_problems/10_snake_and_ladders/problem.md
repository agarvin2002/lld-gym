# Problem 10: Snake and Ladders

## Problem Statement

Design a Snake and Ladders board game supporting 2–4 players with a configurable board.

---

## Rules

- Board: squares 1–100 (position 0 = off-board / start)
- Players take turns rolling a single 6-sided die (1–6)
- Moving beyond square 100 means the player stays in place (bounce rule)
- Landing on a **ladder base** → teleport to the **ladder top**
- Landing on a **snake head** → teleport to the **snake tail**
- First player to reach exactly square 100 wins
- Game status: `WAITING`, `IN_PROGRESS`, `FINISHED`

---

## API

```python
class Game:
    def __init__(self, board: Board) -> None
    def add_player(self, name: str) -> Player
    def start(self) -> None
    def roll_and_move(self) -> MoveResult        # current player rolls
    def current_player(self) -> Player
    def winner(self) -> Player | None
    def status(self) -> GameStatus

class Board:
    def __init__(self, size: int = 100) -> None
    def add_snake(self, head: int, tail: int) -> None
    def add_ladder(self, base: int, top: int) -> None
    def resolve(self, position: int) -> int      # apply snake/ladder if any

class Player:
    name: str
    position: int    # 0 = start, 100 = win

class MoveResult:
    player_name: str
    roll: int
    from_pos: int
    to_pos: int          # after snake/ladder resolution
    teleported_to: int | None   # if snake/ladder hit
    won: bool
```

---

## Constraints

- `add_player` is only allowed before `start()`
- `roll_and_move` is only allowed when game is `IN_PROGRESS`
- Minimum 2 players required to start
- Die rolls are random by default; injectable for testing: `Game(board, die=lambda: 4)`

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **Strategy** | Injectable die function — `die=lambda: 4` for deterministic tests |
| **State** | `GameStatus`: WAITING → IN_PROGRESS → FINISHED; guard clauses prevent invalid operations |
| **SRP** | `Board` resolves snakes/ladders; `Game` manages turn order; `Player` tracks position |

**See also:** Module 03 → [Strategy](../../03_design_patterns/behavioral/strategy/), [State](../../03_design_patterns/behavioral/state/)
