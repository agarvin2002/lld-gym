# Problem 09: Chess Game

## Problem Statement

Design a two-player chess game with full move validation, check detection, and checkmate detection. The system must enforce all standard movement rules for every piece type.

---

## Functional Requirements

1. **Board**
   - 8×8 grid of cells
   - Standard starting layout (all 32 pieces in their canonical positions)

2. **Pieces** — each has correct movement rules:
   | Piece  | Movement Rules                                                    |
   |--------|-------------------------------------------------------------------|
   | King   | 1 square in any direction                                         |
   | Queen  | Any number of squares in any direction (ranks, files, diagonals)  |
   | Rook   | Any number of squares along rank or file                          |
   | Bishop | Any number of squares diagonally                                  |
   | Knight | L-shape: (±1,±2) or (±2,±1), jumps over pieces                   |
   | Pawn   | Forward 1 (or 2 from start), captures diagonally; promotion on rank 8/1 |

3. **Players**
   - White and Black; White moves first
   - Player has a name and color

4. **Game Operations**
   - `start_game()` → initializes board with standard setup
   - `make_move(from_pos, to_pos)` → `bool` (True if successful)
   - `get_valid_moves(pos)` → `List[Position]`

5. **Rules**
   - A player cannot make a move that leaves their own King in check
   - `is_in_check(color)` → `bool`
   - `is_checkmate(color)` → `bool` (no legal moves AND in check)
   - Invalid moves are rejected (return False)
   - Pawn promotion: auto-promote to Queen on reaching last rank

6. **Game Status**
   - `ACTIVE`, `WHITE_WINS`, `BLACK_WINS`, `STALEMATE`

---

## Scope Exclusions (mention in explanation.md as extensibility)

- No castling
- No en passant
- No draw by repetition or 50-move rule

---

## Example Usage

```python
game = Game("Alice", "Bob")
game.start_game()

# e2 → e4 (White pawn double advance)
result = game.make_move(Position(6, 4), Position(4, 4))  # row 6 = rank 2 (0-indexed from top)
assert result is True

# e7 → e5 (Black pawn double advance)
result = game.make_move(Position(1, 4), Position(3, 4))
assert result is True
```

---

## Coordinate System

```
     a   b   c   d   e   f   g   h
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
8 │ ♜ │ ♞ │ ♝ │ ♛ │ ♚ │ ♝ │ ♞ │ ♜ │  row=0
  ├───┼───┼───┼───┼───┼───┼───┼───┤
7 │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │  row=1
  ├───┼───┼───┼───┼───┼───┼───┼───┤
  ...
  ├───┼───┼───┼───┼───┼───┼───┼───┤
2 │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │  row=6
  ├───┼───┼───┼───┼───┼───┼───┼───┤
1 │ ♖ │ ♘ │ ♗ │ ♕ │ ♔ │ ♗ │ ♘ │ ♖ │  row=7
  └───┴───┴───┴───┴───┴───┴───┴───┘
col:  0   1   2   3   4   5   6   7

Position(row, col) — row 0 = rank 8 (Black back rank), row 7 = rank 1 (White back rank)
```
