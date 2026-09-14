import re

from equity_analyzer.application.exceptions import InvalidTickerException
from equity_analyzer.domain.indicators.technical_indicator import (
    TechnicalIndicator,
)
from equity_analyzer.domain.models.stock import (
    Fundamentals,
    StockAnalysis,
    TechnicalIndicators,
)
from equity_analyzer.domain.ports.market_data_provider import (
    MarketDataProvider,
)


class StockAnalysisService:
    """
    Application service responsible for orchestrating stock analysis.

    This class coordinates market-data retrieval and technical
    indicator calculations.

    It does not know whether the data comes from yFinance,
    Bloomberg, a database, or another provider.
    """

    def __init__(
        self,
        market_data_provider: MarketDataProvider,
        sma: TechnicalIndicator,
    ):
        self._market_data_provider = market_data_provider
        self._sma = sma

    def analyze(self, ticker: str) -> StockAnalysis:
        """
        Analyze a stock and return its fundamental and technical data.
        """

        ticker = self._validate_ticker(ticker)

        fundamentals_data = (
            self._market_data_provider.get_fundamentals(ticker)
        )

        history = self._market_data_provider.get_price_history(
            ticker,
            period="3mo",
        )

        fundamentals = Fundamentals(
            **fundamentals_data,
        )

        technical = TechnicalIndicators(
            sma_20=self._sma.calculate(history),
        )

        return StockAnalysis(
            ticker=ticker,
            fundamentals=fundamentals,
            technical=technical,
        )

    @staticmethod
    def _validate_ticker(ticker: str) -> str:
        """
        Validate and normalize the ticker before calling the
        external market-data provider.

        Examples:
            AAPL   -> valid
            LT.NS  -> valid
            ???    -> invalid
            ""     -> invalid
            "   "  -> invalid
        """

        normalized_ticker = ticker.strip().upper()

        if not normalized_ticker:
            raise InvalidTickerException(
                "Ticker must not be empty."
            )

        # Allows common ticker formats such as:
        # AAPL
        # LT.NS
        # BRK-B
        #
        # This is intentionally conservative. The allowed format
        # can be expanded if additional markets require it.
        if not re.fullmatch(
            r"[A-Z0-9]+([.-][A-Z0-9]+)*",
            normalized_ticker,
        ):
            raise InvalidTickerException(
                f"Invalid ticker '{ticker}'."
            )

        return normalized_ticker