# Advanced topic — Strategy pattern as the primary way to achieve OCP in Python
"""
OCP Fix: each discount type is a separate class.
Adding a new type means writing a new class — PriceCalculator never changes.
"""
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base. Each discount type is a subclass."""

    @abstractmethod
    def apply(self, price: float) -> float:
        """Apply discount to price and return new (lower) price."""
        ...

    def __repr__(self) -> str:
        return self.__class__.__name__


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
    """Second item free — effectively half price."""

    def apply(self, price: float) -> float:
        return price / 2


class SeasonalDiscount(DiscountStrategy):
    """Added as a NEW class — PriceCalculator was not touched."""

    def __init__(self, seasonal_percent: float) -> None:
        self.seasonal_percent = seasonal_percent

    def apply(self, price: float) -> float:
        return price * (1 - self.seasonal_percent / 100)


class PriceCalculator:
    """
    Calculates discounted price using any DiscountStrategy.
    Open for extension (new strategies), closed for modification.
    This class never changes when new discount types are added.
    """

    def __init__(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def calculate(self, original_price: float) -> float:
        return round(self._strategy.apply(original_price), 2)


if __name__ == "__main__":
    price = 100.0
    calc = PriceCalculator(NoDiscount())

    strategies = [
        NoDiscount(),
        PercentageDiscount(20),
        FixedDiscount(15),
        BuyOneGetOneDiscount(),
        SeasonalDiscount(30),
    ]

    print("=== OCP: PriceCalculator never changes ===\n")
    for strategy in strategies:
        calc.set_strategy(strategy)
        final = calc.calculate(price)
        print(f"  {strategy}: ${price:.2f} → ${final:.2f}")

    print("\nAdding SeasonalDiscount required only writing a new class.")
    print("PriceCalculator was not touched. That's OCP.")
