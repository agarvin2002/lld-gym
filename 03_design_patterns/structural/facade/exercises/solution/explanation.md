# Explanation: Facade Pattern — Smart Home

## Core insight: orchestration, not logic

`SmartHomeFacade` contains **no business logic of its own**. Every method is a sequence of delegated calls to subsystems. The facade knows *the order* and *which* subsystems to call — that's it.

```python
def good_morning(self) -> list[str]:
    return [
        self._security.disarm(),
        self._thermostat.set_temperature(21),
        self._lighting.set_scene("bright"),
        self._music.play("Morning Playlist"),
    ]
```

Compare the client code without vs with the facade:

```python
# Without facade — 4+ lines, client must know all subsystems
security.disarm()
thermostat.set_temperature(21)
lighting.set_scene("bright")
music.play("Morning Playlist")

# With facade — 1 line, client knows nothing about subsystems
home.good_morning()
```

## Dependency injection via constructor

```python
def __init__(self, security, thermostat, lighting, music):
```

Injecting subsystems (rather than creating them inside the facade) makes each subsystem independently testable and replaceable. Tests can pass in any implementation that has the right methods.

## Facade vs Adapter

| Pattern | Purpose |
|---------|---------|
| Adapter | Convert one interface to another (mismatch fix) |
| Facade | Simplify a complex subsystem (complexity hiding) |

Adapter is about *compatibility*; Facade is about *simplicity*.

## Facade vs Mediator

Both coordinate multiple objects. The difference:
- **Facade**: one-way simplification — clients call the facade, which calls subsystems; subsystems don't know the facade exists
- **Mediator**: two-way coordination — objects communicate *through* the mediator and may also be notified by it

## The "layer boundary" role

In layered architectures, the Facade defines the public API of an internal layer. Code in higher layers depends only on the Facade, not on any individual subsystem class. This makes the subsystem layer refactorable without touching higher layers.

## Return values list

Returning `list[str]` (response messages from each subsystem) lets callers log or display what happened without coupling to internals. A production system might return structured events or status codes instead.
