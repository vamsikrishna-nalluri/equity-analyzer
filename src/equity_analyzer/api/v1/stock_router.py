from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from equity_analyzer.api.dependencies import get_stock_service
from equity_analyzer.application.stock_service import StockAnalysisService
from equity_analyzer.domain.models.stock import StockAnalysis


router = APIRouter(
    prefix="/stock",
    tags=["Stock"],
)


class FundamentalsResponse(BaseModel):
    """
    HTTP representation of fundamental stock metrics.

    Monetary values are expressed in the stock's trading currency.
    """

    price: float | None
    market_cap: float | None
    pe_ratio: float | None
    eps: float | None
    dividend_yield: float | None
    fifty_two_week_high: float | None
    fifty_two_week_low: float | None


class TechnicalResponse(BaseModel):
    """
    HTTP representation of calculated technical indicators.
    """

    sma_20: float | None


class StockResponse(BaseModel):
    """Public API response returned by the stock endpoint."""

    ticker: str
    fundamentals: FundamentalsResponse
    technical: TechnicalResponse


StockServiceDependency = Annotated[
    StockAnalysisService,
    Depends(get_stock_service),
]


@router.get(
    "/{ticker}",
    response_model=StockResponse,
)
def read_stock(
    ticker: str,
    service: StockServiceDependency,
) -> StockResponse:
    """
    Analyze a stock and return its fundamental and technical data.

    Application exceptions are translated into HTTP responses
    by the centralized exception handlers.
    """

    analysis: StockAnalysis = service.analyze(ticker)

    return StockResponse(
        ticker=analysis.ticker,
        fundamentals=FundamentalsResponse(
            price=analysis.fundamentals.price,
            market_cap=analysis.fundamentals.market_cap,
            pe_ratio=analysis.fundamentals.pe_ratio,
            eps=analysis.fundamentals.eps,
            dividend_yield=analysis.fundamentals.dividend_yield,
            fifty_two_week_high=analysis.fundamentals.fifty_two_week_high,
            fifty_two_week_low=analysis.fundamentals.fifty_two_week_low,
        ),
        technical=TechnicalResponse(
            sma_20=analysis.technical.sma_20,
        ),
    )