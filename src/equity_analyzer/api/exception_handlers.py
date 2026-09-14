from fastapi import Request
from fastapi.responses import JSONResponse

from equity_analyzer.application.exceptions import (
    InvalidTickerException,
    MarketDataUnavailableException,
    StockNotFoundException,
)


async def stock_not_found_handler(
    request: Request,
    exc: StockNotFoundException,
) -> JSONResponse:
    """Convert StockNotFoundException into HTTP 404."""

    return JSONResponse(
        status_code=404,
        content={
            "errorCode": "STOCK_NOT_FOUND",
            "errorDescription": str(exc),
        },
    )


async def invalid_ticker_handler(
    request: Request,
    exc: InvalidTickerException,
) -> JSONResponse:
    """Convert InvalidTickerException into HTTP 400."""

    return JSONResponse(
        status_code=400,
        content={
            "errorCode": "INVALID_TICKER",
            "errorDescription": str(exc),
        },
    )


async def market_data_unavailable_handler(
    request: Request,
    exc: MarketDataUnavailableException,
) -> JSONResponse:
    """Convert provider failures into HTTP 503."""

    return JSONResponse(
        status_code=503,
        content={
            "errorCode": "MARKET_DATA_UNAVAILABLE",
            "errorDescription": str(exc),
        },
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Prevent unexpected internal exceptions from leaking
    implementation details to API consumers.
    """

    return JSONResponse(
        status_code=500,
        content={
            "errorCode": "INTERNAL_SERVER_ERROR",
            "errorDescription": "An unexpected internal error occurred.",
        },
    )