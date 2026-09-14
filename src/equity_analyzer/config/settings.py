from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationSettings:
    """Application configuration."""

    sma_window: int = 20