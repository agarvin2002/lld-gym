"""
Adapter Pattern - Exercise Starter
===================================
Task: Adapt LegacyUserRepository to the UserStore interface.

Instructions:
1. Read problem.md for the full requirements.
2. Implement UserRepositoryAdapter below.
3. Run tests.py to verify your solution.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


# ---------------------------------------------------------------------------
# Domain model — do not modify
# ---------------------------------------------------------------------------

class User:
    def __init__(self, id: int, name: str, email: str, active: bool) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.active = active

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', active={self.active})"


# ---------------------------------------------------------------------------
# Legacy code — do not modify
# ---------------------------------------------------------------------------

class UserRepository:
    """Legacy data access object — DO NOT MODIFY."""

    def __init__(self) -> None:
        # Pre-populated in-memory store for the exercise
        self._users: dict[int, User] = {
            1: User(1, "Alice Smith",   "alice@example.com",  active=True),
            2: User(2, "Bob Jones",     "bob@example.com",    active=True),
            3: User(3, "Charlie Brown", "charlie@example.com", active=False),
            4: User(4, "Diana Prince",  "diana@example.com",  active=True),
            5: User(5, "Eve Adams",     "eve@example.com",    active=False),
        }

    def find_by_id(self, id: int) -> Optional[User]:
        """Returns a User by integer ID, or None if not found."""
        return self._users.get(id)

    def find_all_active(self) -> list[User]:
        """Returns all users whose active flag is True."""
        return [u for u in self._users.values() if u.active]

    def find_all(self) -> list[User]:
        """Returns every user regardless of active status."""
        return list(self._users.values())


# ---------------------------------------------------------------------------
# Target interface — do not modify
# ---------------------------------------------------------------------------

class UserStore(ABC):
    """New interface that the rest of the application depends on."""

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Fetch a single user by string ID.
        Returns None if not found or if user_id is invalid.
        """
        ...

    @abstractmethod
    def list_users(self, active_only: bool = True) -> list[User]:
        """
        Return a list of users.
        active_only=True  → active users only
        active_only=False → all users
        """
        ...


# ---------------------------------------------------------------------------
# TODO: Implement the Adapter below
# ---------------------------------------------------------------------------

class UserRepositoryAdapter(UserStore):
    """
    Adapt UserRepository to the UserStore interface.

    Requirements:
    - get_user(user_id: str) converts string ID to int, delegates to find_by_id
    - get_user returns None for invalid (non-numeric) IDs without raising
    - list_users(active_only=True) delegates to find_all_active()
    - list_users(active_only=False) delegates to find_all()
    """

    def __init__(self, repository: UserRepository) -> None:
        # TODO: store the repository
        pass

    def get_user(self, user_id: str) -> Optional[User]:
        # TODO: implement
        pass

    def list_users(self, active_only: bool = True) -> list[User]:
        # TODO: implement
        pass


# ---------------------------------------------------------------------------
# Quick manual test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    repo = UserRepository()
    store = UserRepositoryAdapter(repo)

    print("get_user('1'):", store.get_user("1"))
    print("get_user('3'):", store.get_user("3"))
    print("get_user('99'):", store.get_user("99"))
    print("get_user('abc'):", store.get_user("abc"))

    print("\nlist_users() [active only]:")
    for u in store.list_users():
        print(" ", u)

    print("\nlist_users(active_only=False) [all]:")
    for u in store.list_users(active_only=False):
        print(" ", u)
