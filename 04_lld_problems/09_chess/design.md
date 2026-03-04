# Chess — Design

## Class Diagram

```
Game
├── Board
│   └── dict[Position, Piece]
├── Player (white) ──────── Color.WHITE
├── Player (black) ──────── Color.BLACK
└── GameStatus (ACTIVE/WHITE_WINS/BLACK_WINS/STALEMATE)

Piece (ABC)
├── King
├── Queen
├── Rook
├── Bishop
├── Knight
└── Pawn

Position(row: int, col: int)
MoveResult(success, message, captured_piece)
```

## Coordinate System

```
row 0 = rank 8 (Black back rank)
row 7 = rank 1 (White back rank)
col 0 = file a, col 7 = file h

White pieces start at rows 6–7
Black pieces start at rows 0–1
```

## Move Validation Flow

```
make_move(from_pos, to_pos)
  1. Check game is ACTIVE
  2. Check it's this player's turn
  3. Check from_pos has a piece belonging to current player
  4. Check to_pos is in piece.get_valid_moves(board)
  5. Apply move tentatively
  6. Check if own King is in check → reject if yes
  7. Commit move
  8. Check if opponent is in checkmate or stalemate
  9. Advance turn
```

## Check Detection

```
is_in_check(color):
  find King of color on board
  for each enemy piece:
    if King.position in enemy_piece.get_valid_moves(board):
      return True
  return False
```

## Checkmate Detection

```
is_checkmate(color):
  is_in_check(color) AND no legal move exists for color
  (a legal move = one that, after being applied, doesn't leave own King in check)
```

## Piece Movement Rules

| Piece  | Moves |
|--------|-------|
| King   | 8 adjacent squares (1-step) |
| Queen  | All 8 directions, unlimited range, blocked by pieces |
| Rook   | 4 orthogonal directions, unlimited range, blocked |
| Bishop | 4 diagonal directions, unlimited range, blocked |
| Knight | 8 L-shapes, jumps over pieces |
| Pawn   | Forward 1 (or 2 from start row), captures diagonally |

## Scope Exclusions
- No castling, no en passant, no 50-move rule, no draw by repetition
- Pawn promotes to Queen automatically on reaching last rank
