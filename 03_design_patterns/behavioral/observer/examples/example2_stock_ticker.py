# Advanced topic — ABC-based Observer: using abstract classes to enforce the update() contract.
"""
Observer Pattern — Example 2: Stock Market Ticker

Classic GoF Observer with a Subject class and a StockObserver ABC.
Use this structure when you want the compiler / type checker to enforce
that every observer implements update().

Real-world use: Zerodha Kite's live price feed notifies dashboards,
alert services, and trading bots whenever a stock price changes.
"""
from abc import ABC, abstractmethod


class StockObserver(ABC):
    @abstractmethod
    def update(self, symbol: str, price: float) -> None: ...


class StockMarket:
    """Subject: tracks prices and notifies all observers on each change."""

    def __init__(self) -> None:
        self._observers: list[StockObserver] = []
        self._prices: dict[str, float] = {}

    def subscribe(self, observer: StockObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: StockObserver) -> None:
        self._observers.remove(observer)

    def set_price(self, symbol: str, price: float) -> None:
        self._prices[symbol] = price
        for obs in self._observers:
            obs.update(symbol, price)

    def get_price(self, symbol: str) -> float | None:
        return self._prices.get(symbol)


class StockDisplay(StockObserver):
    """Displays the latest price for every symbol it receives."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.current_prices: dict[str, float] = {}

    def update(self, symbol: str, price: float) -> None:
        self.current_prices[symbol] = price
        print(f"[{self.name}] {symbol}: ₹{price:.2f}")


class PriceAlert(StockObserver):
    """Fires once when a symbol crosses a threshold."""

    def __init__(self, symbol: str, threshold: float) -> None:
        self.symbol = symbol
        self.threshold = threshold
        self.triggered = False

    def update(self, symbol: str, price: float) -> None:
        if symbol == self.symbol and price >= self.threshold and not self.triggered:
            print(f"ALERT: {symbol} crossed ₹{self.threshold:.2f} (now ₹{price:.2f})")
            self.triggered = True


if __name__ == "__main__":
    market = StockMarket()
    display = StockDisplay("Main Board")
    alert   = PriceAlert("INFY", threshold=1800.0)

    market.subscribe(display)
    market.subscribe(alert)

    market.set_price("INFY", 1750.00)
    market.set_price("INFY", 1810.00)  # alert fires here
    market.set_price("INFY", 1820.00)  # alert already triggered — no duplicate
