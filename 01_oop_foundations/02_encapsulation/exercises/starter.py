"""
Exercise: Temperature class with property-based encapsulation.

Fill in the TODOs to complete the implementation.
Run tests with: pytest tests.py -v
"""


class Temperature:
    """
    Represents a temperature with internal Celsius storage.

    Supports reading temperature in Celsius, Fahrenheit, and Kelvin.
    Only Celsius can be set directly. Setting below absolute zero
    (-273.15°C) raises ValueError.

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
        # TODO: assign via the property setter (not directly to _celsius)
        # This ensures validation runs on construction too
        pass

    @property
    def celsius(self) -> float:
        """Return temperature in Celsius."""
        # TODO: return the private attribute
        pass

    @celsius.setter
    def celsius(self, value: float) -> None:
        """
        Set temperature in Celsius.

        Raises:
            ValueError: if value is below absolute zero (-273.15)
        """
        # TODO: validate value >= ABSOLUTE_ZERO_CELSIUS, raise ValueError if not
        # TODO: store in self._celsius
        pass

    @property
    def fahrenheit(self) -> float:
        """Return temperature in Fahrenheit. Formula: C × 9/5 + 32"""
        # TODO: compute and return fahrenheit
        pass

    @property
    def kelvin(self) -> float:
        """Return temperature in Kelvin. Formula: C + 273.15"""
        # TODO: compute and return kelvin
        pass

    def __repr__(self) -> str:
        """Return 'Temperature(celsius=X, fahrenheit=Y, kelvin=Z)'"""
        # TODO: format all three values to 2 decimal places
        pass

    def __eq__(self, other: object) -> bool:
        """Two Temperature objects are equal if their Celsius values match."""
        # TODO: return True if other is Temperature and celsius values are equal
        pass
