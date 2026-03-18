"""
WHAT YOU'RE BUILDING
=====================
A Game Asset Factory that produces consistent visual families for a game engine.

There are two genres: RPG and Sci-Fi. Each genre is a "family" with three assets:
  - Character  (e.g. "Elven Ranger" or "Space Marine")
  - Weapon     (e.g. "Enchanted Bow" or "Plasma Rifle")
  - Environment (e.g. "Enchanted Forest" or "Space Station")

A GameScene accepts any GameAssetFactory and renders all three assets joined by " | ".
The scene never knows which genre it's running — only the factory knows.

Pattern roles:
    Abstract Products:   Character, Weapon, Environment
    Abstract Factory:    GameAssetFactory
    Concrete Products:   RPGCharacter, RPGWeapon, RPGEnvironment,
                         SciFiCharacter, SciFiWeapon, SciFiEnvironment
    Concrete Factories:  RPGAssetFactory, SciFiAssetFactory
    Client:              GameScene
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract Products
# ---------------------------------------------------------------------------

class Character(ABC):
    @abstractmethod
    def describe(self) -> str: ...


class Weapon(ABC):
    @abstractmethod
    def describe(self) -> str: ...


class Environment(ABC):
    @abstractmethod
    def describe(self) -> str: ...


# ---------------------------------------------------------------------------
# Abstract Factory
# ---------------------------------------------------------------------------

class GameAssetFactory(ABC):
    # TIP: Each method here returns one abstract product type.
    # The concrete factory decides which concrete class to instantiate.

    @abstractmethod
    def create_character(self) -> Character: ...

    @abstractmethod
    def create_weapon(self) -> Weapon: ...

    @abstractmethod
    def create_environment(self) -> Environment: ...


# ---------------------------------------------------------------------------
# RPG Family — Concrete Products
# ---------------------------------------------------------------------------

class RPGCharacter(Character):
    def describe(self) -> str:
        # TODO: Return the string "Elven Ranger"
        pass


class RPGWeapon(Weapon):
    def describe(self) -> str:
        # TODO: Return the string "Enchanted Bow"
        pass


class RPGEnvironment(Environment):
    def describe(self) -> str:
        # TODO: Return the string "Enchanted Forest"
        pass


# ---------------------------------------------------------------------------
# Sci-Fi Family — Concrete Products
# ---------------------------------------------------------------------------

class SciFiCharacter(Character):
    def describe(self) -> str:
        # TODO: Return the string "Space Marine"
        pass


class SciFiWeapon(Weapon):
    def describe(self) -> str:
        # TODO: Return the string "Plasma Rifle"
        pass


class SciFiEnvironment(Environment):
    def describe(self) -> str:
        # TODO: Return the string "Space Station"
        pass


# ---------------------------------------------------------------------------
# Concrete Factories
# ---------------------------------------------------------------------------

class RPGAssetFactory(GameAssetFactory):
    # HINT: Each method should return a new instance of the matching RPG concrete class.

    def create_character(self) -> Character:
        # TODO: Return a new RPGCharacter()
        pass

    def create_weapon(self) -> Weapon:
        # TODO: Return a new RPGWeapon()
        pass

    def create_environment(self) -> Environment:
        # TODO: Return a new RPGEnvironment()
        pass


class SciFiAssetFactory(GameAssetFactory):
    # HINT: Mirror RPGAssetFactory but return SciFi concrete classes instead.

    def create_character(self) -> Character:
        # TODO: Return a new SciFiCharacter()
        pass

    def create_weapon(self) -> Weapon:
        # TODO: Return a new SciFiWeapon()
        pass

    def create_environment(self) -> Environment:
        # TODO: Return a new SciFiEnvironment()
        pass


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class GameScene:
    """Renders a game scene using assets from any GameAssetFactory."""

    def __init__(self, factory: GameAssetFactory) -> None:
        # HINT: Call all three factory methods here and store the results.
        # This ensures every asset in the scene comes from the same genre.
        self._character = factory.create_character()
        self._weapon = factory.create_weapon()
        self._environment = factory.create_environment()

    def render(self) -> str:
        # TODO: Return the three describe() results joined by " | "
        # Expected RPG output: "Elven Ranger | Enchanted Bow | Enchanted Forest"
        # HINT: call .describe() on each stored asset, then join with " | "
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/creational/abstract_factory/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
