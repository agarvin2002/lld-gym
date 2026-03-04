"""
Tests for the Adapter exercise.

Run with:
    python tests.py

Imports UserRepositoryAdapter from starter.py (or solution.py if you want
to test the reference solution directly).
"""

import sys
import os
import unittest

# Allow importing from the same directory (starter.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)

from starter import UserRepository, UserRepositoryAdapter, User


class TestUserRepositoryAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = UserRepository()
        self.store = UserRepositoryAdapter(self.repo)

    # --- get_user ---

    def test_get_user_valid_id_returns_user(self) -> None:
        user = self.store.get_user("1")
        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Alice Smith")

    def test_get_user_returns_correct_user_for_each_id(self) -> None:
        user2 = self.store.get_user("2")
        self.assertIsNotNone(user2)
        self.assertEqual(user2.id, 2)
        self.assertEqual(user2.name, "Bob Jones")

        user3 = self.store.get_user("3")
        self.assertIsNotNone(user3)
        self.assertEqual(user3.id, 3)
        self.assertEqual(user3.name, "Charlie Brown")

    def test_get_user_nonexistent_id_returns_none(self) -> None:
        result = self.store.get_user("999")
        self.assertIsNone(result)

    def test_get_user_invalid_string_returns_none(self) -> None:
        result = self.store.get_user("abc")
        self.assertIsNone(result)

    def test_get_user_empty_string_returns_none(self) -> None:
        result = self.store.get_user("")
        self.assertIsNone(result)

    def test_get_user_float_string_returns_none(self) -> None:
        # "1.5" is not a valid int ID
        result = self.store.get_user("1.5")
        self.assertIsNone(result)

    def test_get_user_string_is_converted_to_int(self) -> None:
        # Passing "4" (string) should find user with id=4
        user = self.store.get_user("4")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, 4)

    # --- list_users ---

    def test_list_users_default_returns_active_only(self) -> None:
        users = self.store.list_users()
        self.assertIsInstance(users, list)
        # Active users: 1 (Alice), 2 (Bob), 4 (Diana) = 3 users
        self.assertEqual(len(users), 3)
        for u in users:
            self.assertTrue(u.active, f"Expected active user, got inactive: {u}")

    def test_list_users_active_only_true(self) -> None:
        users = self.store.list_users(active_only=True)
        self.assertEqual(len(users), 3)
        ids = {u.id for u in users}
        self.assertEqual(ids, {1, 2, 4})

    def test_list_users_active_only_false_returns_all(self) -> None:
        users = self.store.list_users(active_only=False)
        self.assertEqual(len(users), 5)
        ids = {u.id for u in users}
        self.assertEqual(ids, {1, 2, 3, 4, 5})

    def test_list_users_returns_list_type(self) -> None:
        result = self.store.list_users()
        self.assertIsInstance(result, list)

    def test_list_users_all_elements_are_user_instances(self) -> None:
        for u in self.store.list_users(active_only=False):
            self.assertIsInstance(u, User)

    # --- adapter delegates correctly ---

    def test_adapter_calls_find_by_id_with_int(self) -> None:
        """Verify delegation — the result should match direct repo call."""
        expected = self.repo.find_by_id(1)
        result = self.store.get_user("1")
        self.assertIs(result, expected)

    def test_adapter_active_list_matches_repo(self) -> None:
        expected = set(u.id for u in self.repo.find_all_active())
        result = set(u.id for u in self.store.list_users(active_only=True))
        self.assertEqual(result, expected)

    def test_adapter_all_list_matches_repo(self) -> None:
        expected = set(u.id for u in self.repo.find_all())
        result = set(u.id for u in self.store.list_users(active_only=False))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
