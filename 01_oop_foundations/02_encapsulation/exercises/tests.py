"""
Tests for the Temperature exercise.
Run: pytest tests.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import Temperature


class TestTemperatureCreation:
    def test_celsius_stored_correctly(self):
        t = Temperature(100)
        assert t.celsius == 100

    def test_negative_celsius_stored_correctly(self):
        t = Temperature(-40)
        assert t.celsius == -40

    def test_zero_celsius(self):
        t = Temperature(0)
        assert t.celsius == 0


class TestConversions:
    def test_fahrenheit_at_boiling_point(self):
        t = Temperature(100)
        assert t.fahrenheit == pytest.approx(212.0)

    def test_fahrenheit_at_freezing_point(self):
        t = Temperature(0)
        assert t.fahrenheit == pytest.approx(32.0)

    def test_fahrenheit_at_body_temperature(self):
        t = Temperature(37)
        assert t.fahrenheit == pytest.approx(98.6, rel=1e-3)

    def test_kelvin_at_boiling_point(self):
        t = Temperature(100)
        assert t.kelvin == pytest.approx(373.15)

    def test_kelvin_at_freezing_point(self):
        t = Temperature(0)
        assert t.kelvin == pytest.approx(273.15)


class TestCelsiusSetter:
    def test_setter_updates_value(self):
        t = Temperature(0)
        t.celsius = 50
        assert t.celsius == 50

    def test_setter_updates_all_conversions(self):
        t = Temperature(0)
        t.celsius = 100
        assert t.fahrenheit == pytest.approx(212.0)
        assert t.kelvin == pytest.approx(373.15)

    def test_raises_below_absolute_zero(self):
        with pytest.raises(ValueError):
            Temperature(-300)

    def test_raises_on_setter_below_absolute_zero(self):
        t = Temperature(0)
        with pytest.raises(ValueError):
            t.celsius = -300

    def test_exact_absolute_zero_is_valid(self):
        t = Temperature(-273.15)
        assert t.celsius == pytest.approx(-273.15)


class TestDunderMethods:
    def test_repr_contains_celsius(self):
        t = Temperature(100)
        assert "celsius" in repr(t)

    def test_repr_contains_fahrenheit(self):
        t = Temperature(100)
        assert "fahrenheit" in repr(t)

    def test_repr_contains_kelvin(self):
        t = Temperature(100)
        assert "kelvin" in repr(t)

    def test_equality_same_celsius(self):
        assert Temperature(100) == Temperature(100)

    def test_equality_different_celsius(self):
        assert Temperature(0) != Temperature(100)

    def test_equality_non_temperature(self):
        assert Temperature(100) != 100
