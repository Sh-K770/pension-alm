from dataclasses import dataclass


@dataclass(frozen=True)
class BalanceSheetSnapshot:
    """Balance sheet of a pension fund for one scenario and projection year."""

    scenario_id: str
    projection_year: int

    asset_market_value: float
    asset_book_value: float
    pension_obligation: float

    interest_rate: float
    inflation_rate: float

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("scenario_id must not be empty")
        if self.projection_year <= 0:
            raise ValueError("projection_year must be positive")
        if self.asset_market_value < 0:
            raise ValueError("asset_market_value must be non-negative")
        if self.asset_book_value < 0:
            raise ValueError("asset_book_value must be non-negative")
        if self.pension_obligation < 0:
            raise ValueError("pension_obligation must be non-negative")
        if self.interest_rate <= -1:
            raise ValueError("interest_rate must be greater than -1")
        if self.inflation_rate <= -1:
            raise ValueError("inflation_rate must be greater than -1")

    @property
    def hidden_reserves(self) -> float:
        """Return hidden reserves (market value minus book value)."""
        return self.asset_market_value - self.asset_book_value

    @property
    def equity_market(self) -> float:
        """Return economic equity based on market values."""
        return self.asset_market_value - self.pension_obligation

    @property
    def equity_book(self) -> float:
        """Return accounting equity based on book values."""
        return self.asset_book_value - self.pension_obligation

    @property
    def funding_ratio(self) -> float:
        """Return funding ratio based on market values."""
        if self.pension_obligation <= 0:
            return 0.0

        return self.asset_market_value / self.pension_obligation

    def is_balanced(self) -> bool:
        """Verify internal consistency of market and book balance sheets."""
        tolerance = 1e-6

        market_assets = self.asset_market_value
        market_liabilities = self.pension_obligation + self.equity_market

        book_assets = self.asset_book_value
        book_liabilities = self.pension_obligation + self.equity_book

        return (
                abs(market_assets - market_liabilities) < tolerance
                and abs(book_assets - book_liabilities) < tolerance
        )