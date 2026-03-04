"""
Abstract Factory Exercise - Test Suite
========================================

Tests for the Game Asset Factory exercise.

Run with:
    /tmp/lld_venv/bin/pytest exercises/tests.py -v
"""

import sys
import os
import pytest

# ---------------------------------------------------------------------------
# Critical: pop 'starter' from sys.modules before importing to prevent
# cross-directory module cache collisions when pytest collects all tests.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    RPGCharacter, RPGWeapon, RPGEnvironment,
    SciFiCharacter, SciFiWeapon, SciFiEnvironment,
    RPGAssetFactory, SciFiAssetFactory,
    GameScene,
)


# ---------------------------------------------------------------------------
# TestRPGFactory
# ---------------------------------------------------------------------------

class TestRPGFactory:
    """RPGAssetFactory returns correctly-typed RPG product instances."""

    def test_create_character_returns_rpg_character(self):
        factory = RPGAssetFactory()
        character = factory.create_character()
        assert isinstance(character, RPGCharacter), (
            "RPGAssetFactory.create_character() must return an RPGCharacter instance"
        )

    def test_create_weapon_returns_rpg_weapon(self):
        factory = RPGAssetFactory()
        weapon = factory.create_weapon()
        assert isinstance(weapon, RPGWeapon), (
            "RPGAssetFactory.create_weapon() must return an RPGWeapon instance"
        )

    def test_create_environment_returns_rpg_environment(self):
        factory = RPGAssetFactory()
        env = factory.create_environment()
        assert isinstance(env, RPGEnvironment), (
            "RPGAssetFactory.create_environment() must return an RPGEnvironment instance"
        )

    def test_factory_produces_new_instances_each_time(self):
        """Each call to create_character() should produce a fresh object."""
        factory = RPGAssetFactory()
        c1 = factory.create_character()
        c2 = factory.create_character()
        assert c1 is not c2, (
            "Each create_character() call should return a new instance"
        )


# ---------------------------------------------------------------------------
# TestSciFiFactory
# ---------------------------------------------------------------------------

class TestSciFiFactory:
    """SciFiAssetFactory returns correctly-typed Sci-Fi product instances."""

    def test_create_character_returns_scifi_character(self):
        factory = SciFiAssetFactory()
        character = factory.create_character()
        assert isinstance(character, SciFiCharacter), (
            "SciFiAssetFactory.create_character() must return a SciFiCharacter instance"
        )

    def test_create_weapon_returns_scifi_weapon(self):
        factory = SciFiAssetFactory()
        weapon = factory.create_weapon()
        assert isinstance(weapon, SciFiWeapon), (
            "SciFiAssetFactory.create_weapon() must return a SciFiWeapon instance"
        )

    def test_create_environment_returns_scifi_environment(self):
        factory = SciFiAssetFactory()
        env = factory.create_environment()
        assert isinstance(env, SciFiEnvironment), (
            "SciFiAssetFactory.create_environment() must return a SciFiEnvironment instance"
        )

    def test_factory_produces_new_instances_each_time(self):
        """Each call to create_character() should produce a fresh object."""
        factory = SciFiAssetFactory()
        c1 = factory.create_character()
        c2 = factory.create_character()
        assert c1 is not c2, (
            "Each create_character() call should return a new instance"
        )


# ---------------------------------------------------------------------------
# TestGameScene
# ---------------------------------------------------------------------------

class TestGameScene:
    """GameScene.render() produces correct output for each theme."""

    def test_rpg_scene_render_contains_elven_ranger(self):
        scene = GameScene(RPGAssetFactory())
        result = scene.render()
        assert "Elven Ranger" in result, (
            f"RPG scene render must contain 'Elven Ranger', got: {result!r}"
        )

    def test_rpg_scene_render_contains_enchanted_bow(self):
        scene = GameScene(RPGAssetFactory())
        result = scene.render()
        assert "Enchanted Bow" in result, (
            f"RPG scene render must contain 'Enchanted Bow', got: {result!r}"
        )

    def test_rpg_scene_render_contains_enchanted_forest(self):
        scene = GameScene(RPGAssetFactory())
        result = scene.render()
        assert "Enchanted Forest" in result, (
            f"RPG scene render must contain 'Enchanted Forest', got: {result!r}"
        )

    def test_scifi_scene_render_contains_space_marine(self):
        scene = GameScene(SciFiAssetFactory())
        result = scene.render()
        assert "Space Marine" in result, (
            f"Sci-Fi scene render must contain 'Space Marine', got: {result!r}"
        )

    def test_scifi_scene_render_contains_plasma_rifle(self):
        scene = GameScene(SciFiAssetFactory())
        result = scene.render()
        assert "Plasma Rifle" in result, (
            f"Sci-Fi scene render must contain 'Plasma Rifle', got: {result!r}"
        )

    def test_scifi_scene_render_contains_space_station(self):
        scene = GameScene(SciFiAssetFactory())
        result = scene.render()
        assert "Space Station" in result, (
            f"Sci-Fi scene render must contain 'Space Station', got: {result!r}"
        )

    def test_render_returns_a_string(self):
        for factory in [RPGAssetFactory(), SciFiAssetFactory()]:
            scene = GameScene(factory)
            result = scene.render()
            assert isinstance(result, str), (
                f"GameScene.render() must return a str, got {type(result).__name__}"
            )

    def test_rpg_render_format_uses_pipe_separator(self):
        """The render string must join assets with ' | '."""
        scene = GameScene(RPGAssetFactory())
        result = scene.render()
        assert "|" in result, (
            "GameScene.render() must join asset descriptions with ' | '"
        )

    def test_rpg_render_exact_format(self):
        """Full render string must match exact expected value."""
        scene = GameScene(RPGAssetFactory())
        expected = "Elven Ranger | Enchanted Bow | Enchanted Forest"
        assert scene.render() == expected, (
            f"RPG render expected {expected!r}, got {scene.render()!r}"
        )

    def test_scifi_render_exact_format(self):
        """Full render string must match exact expected value."""
        scene = GameScene(SciFiAssetFactory())
        expected = "Space Marine | Plasma Rifle | Space Station"
        assert scene.render() == expected, (
            f"Sci-Fi render expected {expected!r}, got {scene.render()!r}"
        )


# ---------------------------------------------------------------------------
# TestFactorySubstitution
# ---------------------------------------------------------------------------

class TestFactorySubstitution:
    """
    The same GameScene code must work with either factory.
    This tests the core Abstract Factory substitutability guarantee.
    """

    def _render_with(self, factory) -> str:
        """Helper: create a scene with the given factory and render it."""
        scene = GameScene(factory)
        return scene.render()

    def test_rpg_factory_substitution(self):
        result = self._render_with(RPGAssetFactory())
        assert isinstance(result, str)
        assert len(result) > 0

    def test_scifi_factory_substitution(self):
        result = self._render_with(SciFiAssetFactory())
        assert isinstance(result, str)
        assert len(result) > 0

    def test_factories_produce_different_output(self):
        """The two factories must produce distinct scene renders."""
        rpg_result = self._render_with(RPGAssetFactory())
        scifi_result = self._render_with(SciFiAssetFactory())
        assert rpg_result != scifi_result, (
            "RPG and Sci-Fi factories must produce different render output"
        )

    def test_same_function_works_with_both_factories(self):
        """
        A single function that accepts a factory should return valid output
        for both RPGAssetFactory and SciFiAssetFactory — no branching needed.
        """
        def build_scene_description(factory) -> str:
            return GameScene(factory).render()

        rpg_desc = build_scene_description(RPGAssetFactory())
        scifi_desc = build_scene_description(SciFiAssetFactory())

        assert "Elven Ranger" in rpg_desc
        assert "Space Marine" in scifi_desc

    def test_rpg_assets_are_not_scifi_instances(self):
        """Cross-family type check: RPG products must not be SciFi instances."""
        factory = RPGAssetFactory()
        character = factory.create_character()
        weapon = factory.create_weapon()
        env = factory.create_environment()

        assert not isinstance(character, SciFiCharacter)
        assert not isinstance(weapon, SciFiWeapon)
        assert not isinstance(env, SciFiEnvironment)

    def test_scifi_assets_are_not_rpg_instances(self):
        """Cross-family type check: SciFi products must not be RPG instances."""
        factory = SciFiAssetFactory()
        character = factory.create_character()
        weapon = factory.create_weapon()
        env = factory.create_environment()

        assert not isinstance(character, RPGCharacter)
        assert not isinstance(weapon, RPGWeapon)
        assert not isinstance(env, RPGEnvironment)
