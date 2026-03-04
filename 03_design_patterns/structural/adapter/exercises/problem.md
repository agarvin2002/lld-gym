# Exercise: Adapter Pattern — Legacy User Repository

## Background

You have a legacy `UserRepository` class that your team has been using for years. It works fine,
but the new codebase expects a `UserStore` interface with different method names and signatures.

You **cannot modify** `UserRepository` — it is part of a library you do not own.

---

## The Legacy Code (do not modify)

```python
class User:
    def __init__(self, id: int, name: str, email: str, active: bool):
        self.id = id
        self.name = name
        self.email = email
        self.active = active

class UserRepository:
    """Legacy data access object — DO NOT MODIFY."""

    def find_by_id(self, id: int) -> User | None:
        """Returns a User by integer ID, or None if not found."""
        ...

    def find_all_active(self) -> list[User]:
        """Returns all users whose active flag is True."""
        ...

    def find_all(self) -> list[User]:
        """Returns every user regardless of active status."""
        ...
```

---

## The New Interface

```python
class UserStore(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> User | None:
        """
        Fetch a single user.
        user_id is a STRING (e.g., "42") — legacy uses int.
        Returns None if not found.
        """
        ...

    @abstractmethod
    def list_users(self, active_only: bool = True) -> list[User]:
        """
        Return users.
        If active_only=True  → return only active users.
        If active_only=False → return all users.
        """
        ...
```

---

## Your Task

1. Implement `UserRepositoryAdapter(UserStore)` that wraps a `UserRepository`.
2. `get_user(user_id: str)` must convert the string ID to int before calling legacy code.
3. `list_users(active_only=True)` must delegate to the right legacy method.
4. Do NOT modify `UserRepository` or `User`.

---

## Constraints

- `user_id` will always be a numeric string like `"1"`, `"42"`, `"100"`.
- If `user_id` cannot be converted to int, return `None` gracefully.
- The adapter must only call public methods on `UserRepository`.

---

## Expected Behaviour

```python
repo = UserRepository()  # pre-populated with test data
adapter = UserRepositoryAdapter(repo)

user = adapter.get_user("1")       # internally calls repo.find_by_id(1)
users = adapter.list_users()       # internally calls repo.find_all_active()
all_u = adapter.list_users(False)  # internally calls repo.find_all()
invalid = adapter.get_user("abc")  # returns None, no exception
```

---

## Files

- `starter.py` — skeleton code to fill in
- `tests.py` — run with `python tests.py` to check your solution
- `solution/solution.py` — reference solution (try yourself first!)
- `solution/explanation.md` — explains the design decisions
