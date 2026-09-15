from unittest.mock import Mock

import pytest
import pandas as pd

from equity_analyzer.application.exceptions import (
    InvalidTickerException,
    MarketDataUnavailableException,
    StockNotFoundException,
)
from equity_analyzer.application.stock_service import StockAnalysisService
from equity_analyzer.domain.models.stock import StockAnalysis
from equity_analyzer.domain.indicators.sma import SimpleMovingAverage


FUNDAMENTALS_DATA = {
    "price": 150.0,
    "market_cap": 2_500_000_000_000,
    "pe_ratio": 28.5,
    "eps": 5.26,
    "dividend_yield": 0.005,
    "fifty_two_week_high": 199.0,
    "fifty_two_week_low": 120.0,
}


def make_service(provider=None, sma=None) -> StockAnalysisService:
    return StockAnalysisService(
        market_data_provider=provider or Mock(),
        sma=sma or Mock(),
    )


# --- _validate_ticker: valid formats -----------------------------------


def test_validate_ticker_with_plain_ticker_returns_uppercased():
    assert StockAnalysisService._validate_ticker("aapl") == "AAPL"


def test_validate_ticker_with_surrounding_whitespace_returns_stripped():
    assert StockAnalysisService._validate_ticker("  AAPL  ") == "AAPL"


def test_validate_ticker_with_exchange_suffix_returns_normalized():
    assert StockAnalysisService._validate_ticker("lt.ns") == "LT.NS"


def test_validate_ticker_with_share_class_suffix_returns_normalized():
    assert StockAnalysisService._validate_ticker("brk-b") == "BRK-B"


# --- _validate_ticker: negative / edge cases ----------------------------


def test_validate_ticker_with_empty_string_raises_invalid_ticker_exception():
    with pytest.raises(InvalidTickerException):
        StockAnalysisService._validate_ticker("")


def test_validate_ticker_with_whitespace_only_raises_invalid_ticker_exception():
    with pytest.raises(InvalidTickerException):
        StockAnalysisService._validate_ticker("   ")


def test_validate_ticker_with_invalid_characters_raises_invalid_ticker_exception():
    with pytest.raises(InvalidTickerException):
        StockAnalysisService._validate_ticker("???")


def test_validate_ticker_with_leading_separator_raises_invalid_ticker_exception():
    with pytest.raises(InvalidTickerException):
        StockAnalysisService._validate_ticker(".AAPL")


def test_validate_ticker_with_trailing_separator_raises_invalid_ticker_exception():
    with pytest.raises(InvalidTickerException):
        StockAnalysisService._validate_ticker("AAPL.")


def test_validate_ticker_with_consecutive_separators_raises_invalid_ticker_exception():
    with pytest.raises(InvalidTickerException):
        StockAnalysisService._validate_ticker("AAPL..NS")


# --- analyze: success path ----------------------------------------------


def test_analyze_with_valid_ticker_returns_stock_analysis():
    provider = Mock()
    provider.get_fundamentals.return_value = FUNDAMENTALS_DATA
    provider.get_price_history.return_value = Mock()

    sma = Mock()
    sma.calculate.return_value = 145.32

    service = make_service(provider=provider, sma=sma)

    result = service.analyze("aapl")

    assert isinstance(result, StockAnalysis)
    assert result.ticker == "AAPL"
    assert result.fundamentals.price == 150.0
    assert result.technical.sma_20 == 145.32


def test_analyze_normalizes_ticker_before_calling_provider():
    provider = Mock()
    provider.get_fundamentals.return_value = FUNDAMENTALS_DATA
    provider.get_price_history.return_value = Mock()

    service = make_service(provider=provider)

    service.analyze("  aapl  ")

    provider.get_fundamentals.assert_called_once_with("AAPL")


def test_analyze_passes_three_month_period_to_price_history():
    provider = Mock()
    provider.get_fundamentals.return_value = FUNDAMENTALS_DATA
    provider.get_price_history.return_value = Mock()

    service = make_service(provider=provider)

    service.analyze("AAPL")

    provider.get_price_history.assert_called_once_with("AAPL", period="3mo")


def test_analyze_with_insufficient_history_returns_none_sma():
    provider = Mock()
    provider.get_fundamentals.return_value = FUNDAMENTALS_DATA
    provider.get_price_history.return_value = Mock()

    sma = Mock()
    sma.calculate.return_value = None

    service = make_service(provider=provider, sma=sma)

    result = service.analyze("AAPL")

    assert result.technical.sma_20 is None


# --- analyze: negative / edge cases --------------------------------------


def test_analyze_with_invalid_ticker_raises_before_calling_provider():
    provider = Mock()
    service = make_service(provider=provider)

    with pytest.raises(InvalidTickerException):
        service.analyze("???")

    provider.get_fundamentals.assert_not_called()
    provider.get_price_history.assert_not_called()


def test_analyze_propagates_stock_not_found_exception_from_provider():
    provider = Mock()
    provider.get_fundamentals.side_effect = StockNotFoundException(
        "No market data found for ticker 'ZZZZ'."
    )

    service = make_service(provider=provider)

    with pytest.raises(StockNotFoundException):
        service.analyze("ZZZZ")


def test_analyze_propagates_market_data_unavailable_exception_from_provider():
    provider = Mock()
    provider.get_fundamentals.side_effect = MarketDataUnavailableException(
        "Market data provider is temporarily unavailable."
    )

    service = make_service(provider=provider)

    with pytest.raises(MarketDataUnavailableException):
        service.analyze("AAPL")

def test_calculates_sma_when_exactly_window_size():
    history = pd.DataFrame({
        "Close": list(range(1, 21))
    })

    sma = SimpleMovingAverage(window=20)

    result = sma.calculate(history)

    assert result == 10.5