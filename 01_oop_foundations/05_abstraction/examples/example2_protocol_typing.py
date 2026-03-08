"""
example2_protocol_typing.py
----------------------------
Advanced topic — introduces typing.Protocol, Python's structural typing system.

What is typing.Protocol?
  - Another way to define an interface in Python (Python 3.8+).
  - A class satisfies a Protocol if it has the right methods — no inheritance needed.
  - This is called "structural typing" or "duck typing with type hints".

How it differs from ABC:

  Use ABC when:
    - You are designing the classes yourself
    - You want Python to enforce that subclasses implement the methods

  Use Protocol when:
    - You are working with third-party classes you cannot modify
    - You want to describe what shape an object needs to have, without requiring inheritance

Example:

    from typing import Protocol

    class Drawable(Protocol):
        def draw(self) -> None: ...   # any class with draw() satisfies this

    class Circle:                     # does NOT inherit from Drawable
        def draw(self) -> None:
            print("Drawing a circle")

    def render(shape: Drawable) -> None:
        shape.draw()                  # works — Circle has draw()

    render(Circle())   # works fine

See example1_abc_module.py for the ABC approach, which is more common in
practice when you own the code.
"""

# Nothing to run here — this file is a reference guide.
print("This file is a reference guide for typing.Protocol.")
print("See example1_abc_module.py for the ABC approach.")
