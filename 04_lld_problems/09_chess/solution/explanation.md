# Chess — Solution Explanation

## Core Architecture

```
Piece (ABC) — polymorphic get_valid_moves()
Board       — dict[Position, Piece]; no game logic
Game        — orchestrates turns, check, checkmate, promotion
```

## `get_valid_moves` vs legal moves

`get_valid_moves` returns "pseudo-legal" moves — moves that are geometrically valid but may leave the king in check. `get_valid_moves` is used inside `is_in_check` (checking what the opponent threatens), so it must NOT filter for check there (infinite recursion).

`Game.get_valid_moves` wraps `piece.get_valid_moves` and filters out moves that leave the own king in check by simulating each move and calling `is_in_check`.

## Simulate-and-check pattern

```python
captured = board.get_piece(target)
board.set_piece(target, piece)
board.set_piece(pos, None)
if not is_in_check(piece.color):
    legal.append(target)
board.set_piece(pos, piece)    # undo
board.set_piece(target, captured)
```

No move objects needed — we directly mutate the board dict and undo. This is the simplest correct approach.

## `_slide` helper eliminates duplication

Queen, Rook, and Bishop all use ray-casting in different direction sets. `_slide` handles: continue while empty, stop at enemy (capture), stop before friendly. Three pieces share this 15-line method.

## Pawn promotion: auto-Queen

```python
if isinstance(piece, Pawn):
    last_rank = 0 if piece.color == Color.WHITE else 7
    if to_pos.row == last_rank:
        self._board.set_piece(to_pos, Queen(piece.color))
```

Auto-promotion to Queen is the simplest correct rule. A complete implementation would let the player choose (underpromotion).

## Check vs Checkmate vs Stalemate

| State | In check | Has legal moves | Result |
|-------|----------|-----------------|--------|
| Normal | No | Yes | Continue |
| Check | Yes | Yes | Must resolve check |
| Checkmate | Yes | No | Loser |
| Stalemate | No | No | Draw |

## Scope exclusions

**Castling** requires: neither piece has moved, no pieces between them, king not in check, king doesn't pass through check. Complex but mechanical to add via `has_moved` flag on King/Rook.

**En passant** requires tracking the last double-pawn move. Implementable with a `last_move` field on `Game`.

Both are documented in `design.md` as intentional exclusions to keep scope manageable.
