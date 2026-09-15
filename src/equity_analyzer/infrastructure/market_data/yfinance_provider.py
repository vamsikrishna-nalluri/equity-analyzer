## src/equity_analyzer/infrastructure/market_data/yfinance_provider.py
import logging
from typing import Any

import yfinance as yf

from equity_analyzer.application.exceptions import (
    MarketDataUnavailableException,
    StockNotFoundException,
)
from equity_analyzer.domain.ports.market_data_provider import (
    MarketDataProvider,
)


# Module-level logger.
# The application can configure the logging destination and log level centrally.
logger = logging.getLogger(__name__)


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
            # logger.exception() automatically includes the exception
            # traceback, making the original failure available in logs.
            logger.exception(
                "Failed to retrieve fundamental data for ticker '%s'.",
                ticker,
            )

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

    def get_price_history(
        self,
        ticker: str,
        period: str,
    ) -> Any:
        """Retrieve historical daily price data from yFinance."""

        try:
            history = yf.Ticker(ticker).history(period=period)

        except Exception as exc:
            # Log the original exception and full traceback for
            # operational troubleshooting.
            logger.exception(
                "Failed to retrieve price history for ticker '%s' "
                "for period '%s'.",
                ticker,
                period,
            )

            raise MarketDataUnavailableException(
                "Market data provider is temporarily unavailable."
            ) from exc

        if history.empty:
            raise StockNotFoundException(
                f"No historical market data found for ticker '{ticker}'."
            )

        return history