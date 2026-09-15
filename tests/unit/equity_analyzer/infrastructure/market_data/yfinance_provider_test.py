from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from equity_analyzer.application.exceptions import (
    MarketDataUnavailableException,
    StockNotFoundException,
)
from equity_analyzer.infrastructure.market_data.yfinance_provider import (
    YFinanceMarketDataProvider,
)


YFINANCE_TICKER_PATH = (
    "equity_analyzer.infrastructure.market_data.yfinance_provider.yf.Ticker"
)


# --- get_fundamentals: success path --------------------------------------


@patch(YFINANCE_TICKER_PATH)
def test_get_fundamentals_with_valid_ticker_returns_mapped_dict(mock_ticker):
    mock_ticker.return_value.info = {
        "regularMarketPrice": 150.0,
        "marketCap": 2_500_000_000_000,
        "trailingPE": 28.5,
        "trailingEps": 5.26,
        "dividendYield": 0.005,
        "fiftyTwoWeekHigh": 199.0,
        "fiftyTwoWeekLow": 120.0,
    }

    provider = YFinanceMarketDataProvider()
    result = provider.get_fundamentals("AAPL")

    assert result["price"] == 150.0
    assert result["pe_ratio"] == 28.5


@patch(YFINANCE_TICKER_PATH)
def test_get_fundamentals_maps_missing_optional_fields_to_none(mock_ticker):
    mock_ticker.return_value.info = {"regularMarketPrice": 150.0}

    provider = YFinanceMarketDataProvider()
    result = provider.get_fundamentals("AAPL")

    assert result["dividend_yield"] is None
    assert result["eps"] is None


# --- get_fundamentals: negative / edge cases -----------------------------


@patch(YFINANCE_TICKER_PATH)
def test_get_fundamentals_with_empty_info_raises_stock_not_found_exception(
    mock_ticker,
):
    mock_ticker.return_value.info = {}

    provider = YFinanceMarketDataProvider()

    with pytest.raises(StockNotFoundException):
        provider.get_fundamentals("ZZZZ")


@patch(YFINANCE_TICKER_PATH)
def test_get_fundamentals_with_missing_market_price_raises_stock_not_found_exception(
    mock_ticker,
):
    mock_ticker.return_value.info = {"marketCap": 1000}

    provider = YFinanceMarketDataProvider()

    with pytest.raises(StockNotFoundException):
        provider.get_fundamentals("ZZZZ")


@patch(YFINANCE_TICKER_PATH)
def test_get_fundamentals_when_yfinance_raises_returns_market_data_unavailable_exception(
    mock_ticker,
):
    mock_ticker.side_effect = ConnectionError("network unreachable")

    provider = YFinanceMarketDataProvider()

    with pytest.raises(MarketDataUnavailableException):
        provider.get_fundamentals("AAPL")


# --- get_price_history: success path --------------------------------------


@patch(YFINANCE_TICKER_PATH)
def test_get_price_history_with_valid_ticker_returns_history_dataframe(mock_ticker):
    history = pd.DataFrame({"Close": [100.0, 101.0, 102.0]})
    mock_ticker.return_value.history.return_value = history

    provider = YFinanceMarketDataProvider()
    result = provider.get_price_history("AAPL", period="3mo")

    assert result.equals(history)


# --- get_price_history: negative / edge cases ------------------------------


@patch(YFINANCE_TICKER_PATH)
def test_get_price_history_with_empty_history_raises_stock_not_found_exception(
    mock_ticker,
):
    mock_ticker.return_value.history.return_value = pd.DataFrame()

    provider = YFinanceMarketDataProvider()

    with pytest.raises(StockNotFoundException):
        provider.get_price_history("ZZZZ", period="3mo")


@patch(YFINANCE_TICKER_PATH)
def test_get_price_history_when_yfinance_raises_returns_market_data_unavailable_exception(
    mock_ticker,
):
    mock_ticker.side_effect = TimeoutError("request timed out")

    provider = YFinanceMarketDataProvider()

    with pytest.raises(MarketDataUnavailableException):
        provider.get_price_history("AAPL", period="3mo")