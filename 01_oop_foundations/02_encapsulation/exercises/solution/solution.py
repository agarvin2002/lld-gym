"""
Solution: Temperature class with property-based encapsulation.
"""


class Temperature:
    """
    Represents a temperature with internal Celsius storage.
    Exposes Fahrenheit and Kelvin as computed read-only properties.
    """

    ABSOLUTE_ZERO_CELSIUS: float = -273.15

    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # uses the setter for validation

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < self.ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(
                f"Temperature {value}°C is below absolute zero ({self.ABSOLUTE_ZERO_CELSIUS}°C)"
            )
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15

    def __repr__(self) -> str:
        return (
            f"Temperature(celsius={self._celsius:.2f}, "
            f"fahrenheit={self.fahrenheit:.2f}, "
            f"kelvin={self.kelvin:.2f})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._celsius == other._celsius
