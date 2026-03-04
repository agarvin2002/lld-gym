"""
Abstract Factory Exercise - Solution
======================================

Game Asset Factory: produces consistent visual families for RPG and Sci-Fi genres.

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
        return "Elven Ranger"


class RPGWeapon(Weapon):
    def describe(self) -> str:
        return "Enchanted Bow"


class RPGEnvironment(Environment):
    def describe(self) -> str:
        return "Enchanted Forest"


# ---------------------------------------------------------------------------
# Sci-Fi Family — Concrete Products
# ---------------------------------------------------------------------------

class SciFiCharacter(Character):
    def describe(self) -> str:
        return "Space Marine"


class SciFiWeapon(Weapon):
    def describe(self) -> str:
        return "Plasma Rifle"


class SciFiEnvironment(Environment):
    def describe(self) -> str:
        return "Space Station"


# ---------------------------------------------------------------------------
# Concrete Factories
# ---------------------------------------------------------------------------

class RPGAssetFactory(GameAssetFactory):
    def create_character(self) -> Character:
        return RPGCharacter()

    def create_weapon(self) -> Weapon:
        return RPGWeapon()

    def create_environment(self) -> Environment:
        return RPGEnvironment()


class SciFiAssetFactory(GameAssetFactory):
    def create_character(self) -> Character:
        return SciFiCharacter()

    def create_weapon(self) -> Weapon:
        return SciFiWeapon()

    def create_environment(self) -> Environment:
        return SciFiEnvironment()


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class GameScene:
    """
    Renders a game scene using assets produced by a GameAssetFactory.

    The scene is completely decoupled from concrete product classes.
    It only ever calls describe() on the abstract product interfaces.
    """

    def __init__(self, factory: GameAssetFactory) -> None:
        self._character = factory.create_character()
        self._weapon = factory.create_weapon()
        self._environment = factory.create_environment()

    def render(self) -> str:
        return " | ".join([
            self._character.describe(),
            self._weapon.describe(),
            self._environment.describe(),
        ])


# ---------------------------------------------------------------------------
# Manual smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    for label, factory in [("RPG", RPGAssetFactory()), ("Sci-Fi", SciFiAssetFactory())]:
        scene = GameScene(factory)
        print(f"{label}: {scene.render()}")
