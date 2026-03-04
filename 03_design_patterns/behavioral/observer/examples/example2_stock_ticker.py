"""
Observer Pattern Example 2: Stock Market Ticker

Classic GoF Observer implementation with Subject/Observer ABCs.
"""
from abc import ABC, abstractmethod


class StockObserver(ABC):
    @abstractmethod
    def update(self, symbol: str, price: float) -> None: ...


class StockMarket:
    """Subject: maintains stock prices and notifies observers on changes."""

    def __init__(self) -> None:
        self._observers: list[StockObserver] = []
        self._prices: dict[str, float] = {}

    def subscribe(self, observer: StockObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: StockObserver) -> None:
        self._observers.remove(observer)

    def set_price(self, symbol: str, price: float) -> None:
        self._prices[symbol] = price
        self._notify(symbol, price)

    def get_price(self, symbol: str) -> float | None:
        return self._prices.get(symbol)

    def _notify(self, symbol: str, price: float) -> None:
        for observer in self._observers:
            observer.update(symbol, price)


class StockDisplay(StockObserver):
    """Displays current prices in a grid."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.current_prices: dict[str, float] = {}

    def update(self, symbol: str, price: float) -> None:
        self.current_prices[symbol] = price
        print(f"[{self.name}] {symbol}: ${price:.2f}")


class PriceAlert(StockObserver):
    """Triggers alert when price crosses a threshold."""

    def __init__(self, symbol: str, threshold: float, above: bool = True) -> None:
        self.symbol = symbol
        self.threshold = threshold
        self.above = above  # True = alert when above threshold
        self.triggered = False

    def update(self, symbol: str, price: float) -> None:
        if symbol != self.symbol:
            return
        crossed = (price >= self.threshold) if self.above else (price <= self.threshold)
        if crossed and not self.triggered:
            direction = "above" if self.above else "below"
            print(f"🚨 ALERT: {symbol} is {direction} ${self.threshold:.2f} (current: ${price:.2f})")
            self.triggered = True


class TradeBot(StockObserver):
    """Simulates a trading bot that reacts to price changes."""

    def __init__(self, buy_threshold: float, sell_threshold: float) -> None:
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.portfolio: dict[str, int] = {}

    def update(self, symbol: str, price: float) -> None:
        if price <= self.buy_threshold:
            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + 10
            print(f"[TradeBot] BUY 10 {symbol} @ ${price:.2f}")
        elif price >= self.sell_threshold and self.portfolio.get(symbol, 0) > 0:
            self.portfolio[symbol] = 0
            print(f"[TradeBot] SELL all {symbol} @ ${price:.2f}")


if __name__ == "__main__":
    market = StockMarket()

    display = StockDisplay("Main Board")
    alert = PriceAlert("AAPL", threshold=180.0, above=True)
    bot = TradeBot(buy_threshold=150.0, sell_threshold=175.0)

    market.subscribe(display)
    market.subscribe(alert)
    market.subscribe(bot)

    print("=== Market Opening ===")
    market.set_price("AAPL", 155.00)
    market.set_price("GOOG", 2800.00)
    market.set_price("AAPL", 148.50)  # bot buys here
    market.set_price("AAPL", 177.00)  # bot sells here
    market.set_price("AAPL", 182.00)  # alert triggers here

    print(f"\nBot portfolio: {bot.portfolio}")
