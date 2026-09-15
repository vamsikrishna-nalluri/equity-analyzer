## src/equity_analyzer/domain/indicators/sma.py
from typing import Any

from equity_analyzer.domain.indicators.technical_indicator import (
    TechnicalIndicator,
)


class SimpleMovingAverage(TechnicalIndicator):
    """
    Calculate a Simple Moving Average (SMA).

    The window represents the number of observations used in
    the calculation. For daily stock data, a window of 20
    represents 20 trading days.
    """

    def __init__(self, window: int):
        if window <= 0:
            raise ValueError("SMA window must be greater than zero")

        self._window = window

    def calculate(self, history: Any) -> float | None:
        """
        Calculate SMA using closing prices.

        Returns None when insufficient historical data is available.
        """

        if history.empty or len(history) < self._window:
            return None

        return round(
            history["Close"].tail(self._window).mean(),
            2,
        )