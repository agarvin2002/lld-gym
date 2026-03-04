# Exercise: Smart Home Facade

## Goal

Build a `SmartHomeFacade` that simplifies controlling multiple smart home devices by wrapping four subsystems behind four named, high-level operations.

---

## Subsystems (already implemented in `starter.py`)

You do **not** need to implement these — they are provided. Read them to understand what each method does and what state they track.

### `SecuritySystem`
| Member | Description |
|---|---|
| `arm() -> str` | Arms the system; returns a status string |
| `disarm() -> str` | Disarms the system; returns a status string |
| `is_armed: bool` (property) | Current armed state |

### `Thermostat`
| Member | Description |
|---|---|
| `set_temperature(temp: int) -> str` | Sets target temperature; returns a status string |
| `current_temp: int` (property) | Currently set temperature (default: 22) |

### `LightingSystem`
| Member | Description |
|---|---|
| `set_scene(scene: str) -> str` | Sets the lighting scene (`"bright"`, `"dim"`, `"off"`); returns a status string |
| `current_scene: str` (property) | Currently active scene (default: `"off"`) |

### `MusicSystem`
| Member | Description |
|---|---|
| `play(playlist: str) -> str` | Starts a playlist; returns a status string |
| `stop() -> str` | Stops playback; returns a status string |
| `current_playlist: str | None` (property) | Name of the currently playing playlist, or `None` if stopped |

---

## Your Task: Implement `SmartHomeFacade`

### Constructor

```python
SmartHomeFacade(security, thermostat, lighting, music)
```

Accept the four subsystem instances and store them as private attributes.

### Methods

Each method must **call the relevant subsystem methods** (delegate, do not reimplement logic) and **return a `list[str]`** containing the status strings returned by each subsystem call, in order.

| Method | Actions |
|---|---|
| `good_morning() -> list[str]` | Disarm security, set temp to 21, set lighting to `"bright"`, play `"Morning Playlist"` |
| `good_night() -> list[str]` | Arm security, set temp to 18, set lighting to `"off"`, stop music |
| `movie_mode() -> list[str]` | Disarm security, set temp to 20, set lighting to `"dim"`, play `"Movie Soundtrack"` |
| `away_mode() -> list[str]` | Arm security, set temp to 16, set lighting to `"off"`, stop music |

---

## Example Usage

```python
security  = SecuritySystem()
thermostat = Thermostat()
lighting  = LightingSystem()
music     = MusicSystem()

home = SmartHomeFacade(security, thermostat, lighting, music)

msgs = home.good_morning()
# e.g. ["Security system disarmed.", "Thermostat set to 21°C.", "Lights set to bright.", "Playing 'Morning Playlist'."]

print(security.is_armed)      # False
print(thermostat.current_temp) # 21
print(lighting.current_scene)  # "bright"
print(music.current_playlist)  # "Morning Playlist"
```

---

## Constraints

- Each facade method must return a `list[str]` with **at least 4 elements**.
- Every element of the returned list must be a **non-empty string**.
- The facade must **not** reimplement subsystem logic — all state changes happen inside the subsystem objects.
- After calling `good_night()` or `away_mode()`, `music.current_playlist` must be `None`.

---

## Files

| File | Role |
|---|---|
| `starter.py` | Edit this — implement `SmartHomeFacade` |
| `tests.py` | Run these to check your work |
| `solution/solution.py` | Reference solution (peek only after attempting) |
| `solution/explanation.md` | Design notes explaining the choices made |

## Running the tests

```bash
/tmp/lld_venv/bin/pytest 03_design_patterns/structural/facade/exercises/tests.py -v
```
