# Abstract Factory

## What is it?
Abstract Factory creates a family of related objects together. You ask the factory for a button, an input field, and a checkbox — and they all come from the same visual theme. The client never names a concrete class; it just calls the factory.

## Analogy
Think of ordering a Zomato Pro subscription vs a regular order. Each tier bundles a matching set of perks — delivery discount, priority support, cashback — all from one "membership factory." You switch tiers and the whole bundle swaps. You never pick perks individually from different tiers.

## Minimal code
```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...

class TextField(ABC):
    @abstractmethod
    def render(self) -> str: ...

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...
    @abstractmethod
    def create_text_field(self) -> TextField: ...

# Light family — every product belongs to the same theme
class LightButton(Button):
    def render(self) -> str: return "<button style='light'>OK</button>"

class LightTextField(TextField):
    def render(self) -> str: return "<input style='light' />"

class LightThemeFactory(UIFactory):
    def create_button(self)    -> Button:    return LightButton()
    def create_text_field(self) -> TextField: return LightTextField()

# Swap one factory → the whole family swaps together
def build_form(factory: UIFactory) -> None:
    print(factory.create_button().render())
    print(factory.create_text_field().render())

build_form(LightThemeFactory())  # both components are Light-themed
```

## Real-world uses
- Payment SDKs: Razorpay vs Paytm each provide a matching set of Button, QR, UPI components
- App themes: Light / Dark / High-Contrast modes produce matching widgets from one factory
- Database drivers: PostgreSQL vs SQLite each supply a matching Connection, QueryBuilder, and Migrator

## One mistake
Hardcoding the concrete factory inside the client defeats the whole pattern.
```python
# Wrong — client is locked to one theme
class Dialog:
    def __init__(self):
        self.factory = LightThemeFactory()  # hardcoded

# Right — inject the factory so it can be swapped
class Dialog:
    def __init__(self, factory: UIFactory) -> None:
        self.factory = factory
```

## What to do next
- Read `examples/example1_ui_themes.py` — two UI families (Light / Dark) sharing one `Dialog` client.
- Read `examples/example2_database.py` — PostgreSQL vs SQLite families, same `Repository` client.
- Open `exercises/starter.py` and build the Game Asset Factory for RPG and Sci-Fi genres.
