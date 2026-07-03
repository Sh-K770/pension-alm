from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Asset(ABC):
    """Abstract base class for pension fund assets.

    Each asset has a market value and a book value. Subclasses implement
    asset-specific cash-flow and projection logic.
    """

    asset_id: str
    market_value: float
    book_value: float

    def __post_init__(self) -> None:
        if self.market_value < 0:
            raise ValueError("market_value must be non-negative")
        if self.book_value < 0:
            raise ValueError("book_value must be non-negative")

    @property
    def hidden_reserve(self) -> float:
        """Difference between market value and book value."""
        return self.market_value - self.book_value

    @abstractmethod
    def cash_flow(self, year: int, interest_rate: float) -> float:
        """Return the asset cash flow in a given projection year."""
        raise NotImplementedError

    @abstractmethod
    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        """Return the projected market value in a given projection year."""
        raise NotImplementedError

    @abstractmethod
    def projected_book_value(
            self,
            year: int,
            interest_rate: float,
    ) -> float:
        """Return the projected book value in a given projection year."""
        raise NotImplementedError