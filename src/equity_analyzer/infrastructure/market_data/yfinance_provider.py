from typing import Any

import yfinance as yf

from equity_analyzer.application.exceptions import (
    MarketDataUnavailableException,
    StockNotFoundException,
)
from equity_analyzer.domain.ports.market_data_provider import (
    MarketDataProvider,
)


class YFinanceMarketDataProvider(MarketDataProvider):
    """
    yFinance implementation of the MarketDataProvider port.

    This adapter isolates the rest of the application from
    yFinance-specific APIs and exceptions.
    """

    def get_fundamentals(self, ticker: str) -> dict[str, Any]:
        """Retrieve fundamental metrics from yFinance."""

        try:
            info = yf.Ticker(ticker).info

        except Exception as exc:
            # Do not expose yFinance/network implementation details
            # to the API consumer.
            raise MarketDataUnavailableException(
                "Market data provider is temporarily unavailable."
            ) from exc

        if not info or info.get("regularMarketPrice") is None:
            raise StockNotFoundException(
                f"No market data found for ticker '{ticker}'."
            )

        return {
            "price": info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "dividend_yield": info.get("dividendYield"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        }

    def get_price_history(self, ticker: str, period: str) -> Any:
        """Retrieve historical daily price data from yFinance."""

        try:
            history = yf.Ticker(ticker).history(period=period)

        except Exception as exc:
            raise MarketDataUnavailableException(
                "Market data provider is temporarily unavailable."
            ) from exc

        if history.empty:
            raise StockNotFoundException(
                f"No historical market data found for ticker '{ticker}'."
            )

        return history