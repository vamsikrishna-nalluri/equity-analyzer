## src/equity_analyzer/domain/models/stock.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Fundamentals:
    """Fundamental metrics for a stock."""

    price: float | None
    market_cap: float | None
    pe_ratio: float | None
    eps: float | None
    dividend_yield: float | None
    fifty_two_week_high: float | None
    fifty_two_week_low: float | None


@dataclass(frozen=True)
class TechnicalIndicators:
    """Technical indicators calculated for a stock."""

    sma_20: float | None


@dataclass(frozen=True)
class StockAnalysis:
    """
    Domain result representing the complete stock analysis.
    """

    ticker: str
    fundamentals: Fundamentals
    technical: TechnicalIndicators