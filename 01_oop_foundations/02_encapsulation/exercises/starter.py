"""
WHAT YOU'RE BUILDING
--------------------
You are building a Temperature class.

A temperature can be read in three units: Celsius, Fahrenheit, and Kelvin.
You can only SET the temperature in Celsius.
If you try to set it below absolute zero (-273.15°C), it raises an error.

This is a great practice for @property — a key skill used in LLD problems.

HOW TO RUN TESTS
    pytest tests.py -v
"""


class Temperature:
    """
    Stores a temperature in Celsius internally.

    You can read it as Celsius, Fahrenheit, or Kelvin using properties.
    Only Celsius can be set. Setting below -273.15 raises ValueError.

    Usage:
        t = Temperature(100)
        t.celsius     # 100
        t.fahrenheit  # 212.0
        t.kelvin      # 373.15
        t.celsius = 0
        t.fahrenheit  # 32.0
    """

    ABSOLUTE_ZERO_CELSIUS: float = -273.15

    def __init__(self, celsius: float) -> None:
        # We call the setter here so validation runs automatically.
        # TIP: always validate in __init__ so your object starts in a valid state.
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        """Return temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """
        Set temperature in Celsius.

        Raises:
            ValueError: if value is below absolute zero (-273.15)
        """
        if value < Temperature.ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(
                f"Temperature cannot be below absolute zero "
                f"({Temperature.ABSOLUTE_ZERO_CELSIUS}°C), got {value}"
            )
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Return temperature in Fahrenheit. Formula: C × 9/5 + 32"""
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        """Return temperature in Kelvin. Formula: C + 273.15"""
        return self._celsius + 273.15

    def __repr__(self) -> str:
        """Return 'Temperature(celsius=X, fahrenheit=Y, kelvin=Z)'"""
        return (
            f"Temperature(celsius={self._celsius:.2f}, "
            f"fahrenheit={self.fahrenheit:.2f}, "
            f"kelvin={self.kelvin:.2f})"
        )

    def __eq__(self, other: object) -> bool:
        """Two Temperature objects are equal if their Celsius values match."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._celsius == other._celsius


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/02_encapsulation/exercises/tests.py -v
#
# Run all OOP exercises at once:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/ -v
# =============================================================================
