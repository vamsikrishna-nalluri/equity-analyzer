# src/equity_analyzer/main.py
from fastapi import FastAPI

from equity_analyzer.api.exception_handlers import (
    invalid_ticker_handler,
    market_data_unavailable_handler,
    stock_not_found_handler,
    unexpected_exception_handler,
)
from equity_analyzer.api.v1.stock_router import router as stock_router
from equity_analyzer.application.exceptions import (
    InvalidTickerException,
    MarketDataUnavailableException,
    StockNotFoundException,
)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title="Equity Analyzer",
        description="Equity analysis API",
        version="1.0.0",
    )

    # API routes.
    application.include_router(
        stock_router,
        prefix="/api/v1",
    )

    # Centralized application-exception → HTTP-response mapping.
    application.add_exception_handler(
        StockNotFoundException,
        stock_not_found_handler,
    )

    application.add_exception_handler(
        InvalidTickerException,
        invalid_ticker_handler,
    )

    application.add_exception_handler(
        MarketDataUnavailableException,
        market_data_unavailable_handler,
    )

    # Last-resort protection against leaking unexpected exceptions.
    application.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )

    return application


app = create_application()