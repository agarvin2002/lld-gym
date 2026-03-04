# Solution Explanation: UserRepositoryAdapter

## What the Adapter Does

The `UserRepositoryAdapter` is a classic **object adapter** (composition over inheritance). It:

1. Holds a reference to `UserRepository` (the adaptee)
2. Implements `UserStore` (the target interface)
3. Translates each method call from the new interface to the legacy interface

---

## Method-by-Method Breakdown

### `get_user(user_id: str) -> Optional[User]`

```python
def get_user(self, user_id: str) -> Optional[User]:
    try:
        int_id = int(user_id)
    except (ValueError, TypeError):
        return None
    return self._repo.find_by_id(int_id)
```

**Translation**: `str` → `int`

The new interface accepts string IDs (because REST APIs, URLs, and form data always deal in strings).
The legacy code expects `int`. The adapter converts with `int(user_id)`.

Importantly, if conversion fails (e.g., `"abc"`, `""`, `"1.5"`), we return `None` rather than
letting a `ValueError` propagate — this is part of the contract in `problem.md`.

### `list_users(active_only: bool = True) -> list[User]`

```python
def list_users(self, active_only: bool = True) -> list[User]:
    if active_only:
        return self._repo.find_all_active()
    return self._repo.find_all()
```

**Translation**: `active_only` flag → different legacy method calls

The legacy API chose different method names (`find_all_active` vs `find_all`).
The new interface parameterises this into a single method with a flag.
The adapter picks the right legacy method based on the flag.

---

## Why Composition Instead of Inheritance?

```python
# We did NOT do this:
class UserRepositoryAdapter(UserStore, UserRepository): ...
```

**Object adapter (composition) is preferred because**:
- We don't need to inherit legacy implementation details
- We can wrap any `UserRepository` instance — including subclasses or mocks
- Avoids MRO (Method Resolution Order) confusion from multiple inheritance
- `UserRepository` might not be designed to be subclassed

---

## Key Design Decisions

| Decision | Why |
|---|---|
| `try/except` on int conversion | The contract says return `None`, not raise, for bad IDs |
| Delegate fully, don't copy data | The adapter is a thin wrapper — no business logic |
| Accept `UserRepository` in `__init__` | Dependency injection — easy to test with custom repos |
| Keep `UserStore` as ABC | Allows multiple implementations (adapter, mock, real DB) |

---

## What This Pattern Lets You Do

- Replace `UserRepository` with a different backend later — the adapter hides it
- Test client code using a `MockUserStore` without touching the legacy layer
- Migrate incrementally: old code uses `UserRepository` directly, new code uses `UserStore`

---

## Common Mistakes to Avoid

1. **Modifying the adaptee**: The whole point is you leave legacy code alone.
2. **Adding business logic to the adapter**: Adapters translate; they don't decide.
3. **Forgetting error handling on type conversion**: Always guard against invalid input at the seam.
4. **Using class adapter when you don't need to**: Composition keeps things loose.
