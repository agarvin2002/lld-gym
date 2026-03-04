"""
Example 2: Open/Closed Principle — Refactored with Strategy Pattern

Shows how to add new discount types without modifying existing code.
Contrast this with example1_violation.py where every new type requires
modifying the central PriceCalculator.
"""
from abc import ABC, abstractmethod


# ─── Abstraction: The DiscountStrategy interface ──────────────────

class DiscountStrategy(ABC):
    """Each discount type is a separate class. To add a new type: add a new class."""

    @abstractmethod
    def apply(self, price: float) -> float:
        """Apply discount to price and return new price."""
        ...

    def __repr__(self) -> str:
        return self.__class__.__name__


# ─── Concrete Strategies ─────────────────────────────────────────

class NoDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise ValueError(f"Percent must be 0-100, got {percent}")
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, price: float) -> float:
        return max(0.0, price - self.amount)


class BuyOneGetOneDiscount(DiscountStrategy):
    """Second item is free — effectively half price."""

    def apply(self, price: float) -> float:
        return price / 2


class SeasonalDiscount(DiscountStrategy):
    """Example of a NEW strategy added WITHOUT changing PriceCalculator."""

    def __init__(self, seasonal_percent: float) -> None:
        self.seasonal_percent = seasonal_percent

    def apply(self, price: float) -> float:
        return price * (1 - self.seasonal_percent / 100)


# ─── Closed for modification: PriceCalculator never changes ──────

class PriceCalculator:
    """
    Calculates discounted price using any DiscountStrategy.
    NEVER needs to change when new discount types are added.
    Open for extension (new strategies), closed for modification.
    """

    def __init__(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def calculate(self, original_price: float) -> float:
        discounted = self._strategy.apply(original_price)
        return round(discounted, 2)

    def show_savings(self, original_price: float) -> None:
        final = self.calculate(original_price)
        savings = original_price - final
        print(
            f"Strategy: {self._strategy} | "
            f"Original: ${original_price:.2f} | "
            f"Final: ${final:.2f} | "
            f"Savings: ${savings:.2f}"
        )


if __name__ == "__main__":
    price = 100.0

    strategies = [
        NoDiscount(),
        PercentageDiscount(20),
        FixedDiscount(15),
        BuyOneGetOneDiscount(),
        SeasonalDiscount(30),  # added without touching PriceCalculator
    ]

    calc = PriceCalculator(NoDiscount())

    print("=== OCP Demo: PriceCalculator never changes ===\n")
    for strategy in strategies:
        calc.set_strategy(strategy)
        calc.show_savings(price)

    print("\n=== Key insight ===")
    print("Adding SeasonalDiscount required ONLY writing a new class.")
    print("PriceCalculator was not touched. That's OCP.")
