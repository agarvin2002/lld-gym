"""
Adapter Pattern - Exercise Solution
=====================================
Adapts UserRepository (legacy) to the UserStore interface (new system).
"""

from __future__ import annotations
import sys
import os

# Import shared definitions from starter.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from starter import User, UserRepository, UserStore
from typing import Optional


class UserRepositoryAdapter(UserStore):
    """
    Adapts the legacy UserRepository to the new UserStore interface.

    Key translations:
    - user_id: str  →  id: int   (get_user)
    - list_users(active_only=True)  →  find_all_active()
    - list_users(active_only=False) →  find_all()
    - Invalid string IDs → return None (no exception propagation)
    """

    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Convert string ID to int, then delegate to legacy find_by_id().
        Returns None for non-numeric strings rather than raising ValueError.
        """
        try:
            int_id = int(user_id)
        except (ValueError, TypeError):
            return None
        return self._repo.find_by_id(int_id)

    def list_users(self, active_only: bool = True) -> list[User]:
        """
        Delegate to the appropriate legacy method based on active_only flag.
        """
        if active_only:
            return self._repo.find_all_active()
        return self._repo.find_all()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    repo = UserRepository()
    store = UserRepositoryAdapter(repo)

    print("=== UserRepositoryAdapter Demo ===\n")

    print("get_user('1')  →", store.get_user("1"))
    print("get_user('3')  →", store.get_user("3"))
    print("get_user('99') →", store.get_user("99"))
    print("get_user('abc')→", store.get_user("abc"))
    print("get_user('')   →", store.get_user(""))

    print("\nActive users (default):")
    for u in store.list_users():
        print(f"  {u}")

    print("\nAll users (active_only=False):")
    for u in store.list_users(active_only=False):
        print(f"  {u}")
