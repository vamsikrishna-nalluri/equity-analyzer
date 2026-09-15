## src/equity_analyzer/domain/indicators/technical_indicator.py

from abc import ABC, abstractmethod
from typing import Any


class TechnicalIndicator(ABC):
    """
    Port/interface for technical-indicator calculations.

    The domain layer defines what a technical indicator must do,
    without knowing how market data is obtained.
    """

    @abstractmethod
    def calculate(self, history: Any) -> float | None:
        """Calculate the indicator from historical market data."""
        ...