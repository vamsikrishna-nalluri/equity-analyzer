class ApplicationException(Exception):
    """Base exception for application-level failures."""


class StockNotFoundException(ApplicationException):
    """Raised when market data cannot be found for a ticker."""


class MarketDataUnavailableException(ApplicationException):
    """
    Raised when the external market-data provider is unavailable
    or fails while retrieving data.
    """


class InvalidTickerException(ApplicationException):
    """Raised when a ticker fails application-level validation."""