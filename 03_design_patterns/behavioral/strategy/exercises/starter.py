"""Strategy Pattern Exercise — Reference Solution."""
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, order_total: float) -> float: ...


class NoDiscount(DiscountStrategy):
    def apply(self, order_total: float) -> float:
        return order_total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError(f"percent must be 0–100, got {percent}")
        self._percent = percent

    def apply(self, order_total: float) -> float:
        return order_total * (1 - self._percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        if amount < 0:
            raise ValueError(f"amount must be >= 0, got {amount}")
        self._amount = amount

    def apply(self, order_total: float) -> float:
        return max(0.0, order_total - self._amount)


class BuyOneGetOneFree(DiscountStrategy):
    def apply(self, order_total: float) -> float:
        return order_total / 2


class LoyaltyDiscount(DiscountStrategy):
    _TIERS = {"silver": 5, "gold": 10, "platinum": 15}

    def __init__(self, tier: str) -> None:
        if tier not in self._TIERS:
            raise ValueError(f"Unknown tier: {tier!r}. Choose from {list(self._TIERS)}")
        self._percent = self._TIERS[tier]

    def apply(self, order_total: float) -> float:
        return order_total * (1 - self._percent / 100)


class Order:
    def __init__(self, total: float, discount: DiscountStrategy) -> None:
        if total <= 0:
            raise ValueError(f"total must be > 0, got {total}")
        self.total = total
        self._discount = discount

    def final_price(self) -> float:
        return self._discount.apply(self.total)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self._discount = discount
