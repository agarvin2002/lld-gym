# Exercise: Game Asset Factory

## Background

A game studio is building two game genres: **RPG** and **Sci-Fi**. Each genre has its own visual style, and all assets within a genre must be visually consistent. Using Abstract Factory ensures you can never accidentally use an RPG character in a Sci-Fi scene.

---

## Your Task

Implement the Abstract Factory pattern to produce consistent game asset families.

---

## Product ABCs

Implement these three abstract base classes, each with one abstract method:

### `Character(ABC)`
- `describe(self) -> str` — returns a string describing the character

### `Weapon(ABC)`
- `describe(self) -> str` — returns a string describing the weapon

### `Environment(ABC)`
- `describe(self) -> str` — returns a string describing the environment

---

## Factory ABC

### `GameAssetFactory(ABC)`
- `create_character(self) -> Character`
- `create_weapon(self) -> Weapon`
- `create_environment(self) -> Environment`

---

## Concrete Families

### RPG Family

| Class | `describe()` return value |
|-------|--------------------------|
| `RPGCharacter(Character)` | `"Elven Ranger"` |
| `RPGWeapon(Weapon)` | `"Enchanted Bow"` |
| `RPGEnvironment(Environment)` | `"Enchanted Forest"` |

### Sci-Fi Family

| Class | `describe()` return value |
|-------|--------------------------|
| `SciFiCharacter(Character)` | `"Space Marine"` |
| `SciFiWeapon(Weapon)` | `"Plasma Rifle"` |
| `SciFiEnvironment(Environment)` | `"Space Station"` |

---

## Concrete Factories

### `RPGAssetFactory(GameAssetFactory)`
- `create_character()` returns `RPGCharacter()`
- `create_weapon()` returns `RPGWeapon()`
- `create_environment()` returns `RPGEnvironment()`

### `SciFiAssetFactory(GameAssetFactory)`
- `create_character()` returns `SciFiCharacter()`
- `create_weapon()` returns `SciFiWeapon()`
- `create_environment()` returns `SciFiEnvironment()`

---

## Client: `GameScene`

```python
class GameScene:
    def __init__(self, factory: GameAssetFactory) -> None: ...
    def render(self) -> str: ...
```

`__init__` receives a factory and uses it to create all three assets.

`render()` calls `describe()` on each asset and joins results with `" | "`:

```
"Elven Ranger | Enchanted Bow | Enchanted Forest"
```

---

## Constraints

- `GameScene` must **not** import or reference any concrete class (`RPGCharacter`, etc.)
- `GameScene` must work identically with both factories — no `if` statements checking factory type
- All abstract methods must be decorated with `@abstractmethod`

---

## Running the Tests

```bash
/tmp/lld_venv/bin/pytest exercises/tests.py -v
```

Expected output: all tests pass across `TestRPGFactory`, `TestSciFiFactory`, `TestGameScene`, and `TestFactorySubstitution`.
