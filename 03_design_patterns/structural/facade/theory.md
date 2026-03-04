# Facade Pattern

## What Is Facade?

The **Facade** pattern provides a simplified interface to a complex subsystem. Instead of forcing clients to interact with multiple classes, methods, and sequences of calls, a Facade exposes a single, high-level interface that hides the underlying complexity.

The name comes from architecture: a building's facade is the front-facing surface presented to the public, hiding the internal structure of walls, wiring, and plumbing behind it.

---

## Real-World Analogy: Car Ignition

When you turn a car key (or press a button), you trigger:

1. The fuel pump pressurising the fuel line
2. The starter motor cranking the engine
3. The ignition coil firing spark plugs in sequence
4. The ECU monitoring sensor feedback
5. The throttle body adjusting air intake

You do not coordinate any of this manually. The ignition system is a Facade over these subsystems. You interact with a single interface — turn the key — and the subsystem coordinates itself.

The same idea appears everywhere:
- A **TV remote** is a facade over tuner, display, audio amplifier, and HDMI switching.
- A **web browser** is a facade over DNS resolution, TCP/IP, HTTP, HTML parsing, and rendering.
- A **bank's mobile app** is a facade over account services, fraud detection, notifications, and ledger systems.

---

## Why It Matters

Without a Facade, client code must:
- Know the internal structure of the subsystem
- Understand the correct sequence of calls
- Handle coordination and error recovery across multiple classes
- Be updated whenever subsystem internals change

With a Facade:
- Clients depend on one class, not many
- Coupling between client and subsystem is reduced
- The subsystem can evolve without breaking clients
- Common workflows are named and documented in one place

---

## Python Specifics

Python has no special syntax for Facade. It is simply a class that holds references to subsystem objects and delegates to them:

```python
class HomeTheaterFacade:
    def __init__(self, projector, screen, sound, bluray, lights):
        self._projector = projector
        self._screen = screen
        self._sound = sound
        self._bluray = bluray
        self._lights = lights

    def watch_movie(self, title: str) -> None:
        self._lights.set_dimmer(30)
        self._screen.down()
        self._projector.on()
        self._projector.set_input("HDMI")
        self._sound.on()
        self._sound.set_volume(30)
        self._bluray.play(title)
```

Notice: the Facade does **not** contain business logic. Every line is a delegation. The logic lives in the subsystems.

---

## When to Use Facade

- **Wrapping legacy systems**: provide a clean modern interface over old, tangled code.
- **Complex third-party libraries**: shield your application from a library's verbose API.
- **Layered architecture**: define the public API of a layer (e.g., a service layer Facade over repositories and domain objects).
- **Simplifying test setup**: a Facade can reduce the boilerplate needed to put a subsystem into a usable state.
- **Reducing coupling**: when many parts of your app talk to the same subsystem, centralise the coordination in one place.

---

## When to Avoid Facade

- **Do not hide complexity that clients genuinely need.** If callers require fine-grained control (e.g., a video editor needs individual audio track control), a Facade that forces a one-size-fits-all workflow is an obstacle.
- **Do not use Facade as a dumping ground.** If the Facade starts containing conditional logic, data transformation, or domain rules, it is becoming a service class — give it a different name and rethink the design.
- **Do not couple subsystems through the Facade.** Subsystems should remain independent of each other; only the Facade knows about all of them.

---

## Common Mistakes

1. **Facade doing too much logic.** The Facade should delegate, not implement. If you find yourself writing if/else or calculations inside a Facade method, move that logic into the appropriate subsystem.

2. **Preventing access to subsystems.** A Facade simplifies; it does not lock clients out. Subsystems should still be usable directly when needed.

3. **One giant God Facade.** If a system is very large, consider multiple focused Facades (e.g., `OrderFacade`, `ReportingFacade`) rather than one class that wraps everything.

4. **Confusing Facade with Adapter.** Adapter converts one interface to another (makes incompatible things compatible). Facade simplifies many interfaces into one (reduces complexity). The intent is different even if the mechanics look similar.

5. **Confusing Facade with Mediator.** Mediator coordinates two-way communication between objects (they know the mediator). Facade is a one-directional simplification — subsystems do not know the Facade exists.

---

## Summary

| Property | Detail |
|---|---|
| Category | Structural |
| Intent | Provide a unified, simplified interface to a set of interfaces in a subsystem |
| Participants | Facade, Subsystem classes, Client |
| Key benefit | Reduced coupling between client and subsystem |
| Python mechanism | Plain class with constructor injection of subsystem references |
| Risk | Over-simplification, or Facade growing into a God object |
