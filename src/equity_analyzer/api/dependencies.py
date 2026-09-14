from equity_analyzer.application.stock_service import StockAnalysisService
from equity_analyzer.config.settings import ApplicationSettings
from equity_analyzer.domain.indicators.sma import SimpleMovingAverage
from equity_analyzer.infrastructure.market_data.yfinance_provider import (
    YFinanceMarketDataProvider,
)


def get_stock_service() -> StockAnalysisService:
    """
    Construct the application service and its dependencies.

    FastAPI calls this function when an endpoint requests
    StockAnalysisService through Depends().
    """

    settings = ApplicationSettings()

    market_data_provider = YFinanceMarketDataProvider()

    sma = SimpleMovingAverage(
        window=settings.sma_window,
    )

    return StockAnalysisService(
        market_data_provider=market_data_provider,
        sma=sma,
    )