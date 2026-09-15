## src/equity_analyzer/domain/ports/market_data_provider.py

from abc import ABC, abstractmethod
from typing import Any


class MarketDataProvider(ABC):
    """
    Port defining the market-data operations required by the
    application.

    The application depends on this abstraction rather than
    directly depending on yFinance, Bloomberg, Refinitiv, etc.
    """

    @abstractmethod
    def get_fundamentals(self, ticker: str) -> dict[str, Any]:
        """Retrieve fundamental metrics for a ticker."""
        ...

    @abstractmethod
    def get_price_history(self, ticker: str, period: str) -> Any:
        """Retrieve historical price data for a ticker."""
        ...