"""
Abstract Factory Example 1: UI Themes
======================================

Two UI families: LightTheme and DarkTheme.
Each family produces three coordinated widgets: Button, TextInput, Checkbox.

The Dialog client only knows about UIFactory and the abstract widget interfaces.
Swapping the factory switches the entire theme without any changes to Dialog.

Real-world use: Flipkart's app ships Light and Dark themes. Each theme is a
factory that produces matching nav bars, buttons, and input fields. The screen
components never import concrete theme classes — they accept a ThemeFactory.

Run: python example1_ui_themes.py
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract Products
# ---------------------------------------------------------------------------

class Button(ABC):
    """Abstract button widget."""

    @abstractmethod
    def render(self) -> str:
        """Return an HTML-like string representing the button."""
        ...


class TextInput(ABC):
    """Abstract text input widget."""

    @abstractmethod
    def render(self) -> str:
        """Return an HTML-like string representing the text input."""
        ...


class Checkbox(ABC):
    """Abstract checkbox widget."""

    @abstractmethod
    def render(self) -> str:
        """Return an HTML-like string representing the checkbox."""
        ...


# ---------------------------------------------------------------------------
# Abstract Factory
# ---------------------------------------------------------------------------

class UIFactory(ABC):
    """
    Abstract factory that produces a family of UI widgets.

    Concrete subclasses implement each create_* method to return widgets
    from a consistent visual theme.
    """

    @abstractmethod
    def create_button(self) -> Button:
        """Create a theme-appropriate button."""
        ...

    @abstractmethod
    def create_text_input(self) -> TextInput:
        """Create a theme-appropriate text input."""
        ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a theme-appropriate checkbox."""
        ...


# ---------------------------------------------------------------------------
# Light Theme — Concrete Products
# ---------------------------------------------------------------------------

class LightButton(Button):
    def render(self) -> str:
        return '<button style="background:#ffffff; color:#111111; border:1px solid #cccccc">Submit</button>'


class LightTextInput(TextInput):
    def render(self) -> str:
        return '<input type="text" style="background:#ffffff; color:#111111; border:1px solid #dddddd" placeholder="Enter text">'


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return '<input type="checkbox" style="accent-color:#0066cc"> Remember me'


# ---------------------------------------------------------------------------
# Dark Theme — Concrete Products
# ---------------------------------------------------------------------------

class DarkButton(Button):
    def render(self) -> str:
        return '<button style="background:#1e1e1e; color:#e0e0e0; border:1px solid #444444">Submit</button>'


class DarkTextInput(TextInput):
    def render(self) -> str:
        return '<input type="text" style="background:#2d2d2d; color:#e0e0e0; border:1px solid #555555" placeholder="Enter text">'


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return '<input type="checkbox" style="accent-color:#66aaff"> Remember me'


# ---------------------------------------------------------------------------
# Concrete Factories
# ---------------------------------------------------------------------------

class LightThemeFactory(UIFactory):
    """Creates widgets belonging to the Light visual theme."""

    def create_button(self) -> Button:
        return LightButton()

    def create_text_input(self) -> TextInput:
        return LightTextInput()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkThemeFactory(UIFactory):
    """Creates widgets belonging to the Dark visual theme."""

    def create_button(self) -> Button:
        return DarkButton()

    def create_text_input(self) -> TextInput:
        return DarkTextInput()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


# ---------------------------------------------------------------------------
# Client — Dialog
# ---------------------------------------------------------------------------

class Dialog:
    """
    A login dialog that renders its widgets using whatever UIFactory it receives.

    The Dialog never imports LightThemeFactory or DarkThemeFactory.
    Swapping the factory is the only change needed to switch themes.
    """

    def __init__(self, factory: UIFactory) -> None:
        # All three widgets are guaranteed to come from the same theme.
        self._button = factory.create_button()
        self._text_input = factory.create_text_input()
        self._checkbox = factory.create_checkbox()

    def render_login(self) -> str:
        """Compose all three widgets into a login form string."""
        lines = [
            "=== Login Form ===",
            f"Username: {self._text_input.render()}",
            f"Remember: {self._checkbox.render()}",
            f"Action:   {self._button.render()}",
            "==================",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("Light Theme Login Form")
    print("-" * 40)
    light_dialog = Dialog(LightThemeFactory())
    print(light_dialog.render_login())

    print()

    print("Dark Theme Login Form")
    print("-" * 40)
    dark_dialog = Dialog(DarkThemeFactory())
    print(dark_dialog.render_login())

    print()
    print("Key observation:")
    print("  Dialog code is identical for both themes.")
    print("  Only the factory argument changes.")


if __name__ == "__main__":
    main()
