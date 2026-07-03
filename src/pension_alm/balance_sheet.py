from dataclasses import dataclass


@dataclass(frozen=True)
class BalanceSheetSnapshot:
    """
    Represents the balance sheet of a pension fund at a single
    projection year.

    The balance sheet is reported using both market values and
    book values.

    Terminology
    -----------
    Pension obligation:
        Present value of future pension payments
        (German: Deckungsrückstellung, DRS)
    """

    projection_year: int

    asset_market_value: float
    asset_book_value: float

    pension_obligation: float

    interest_rate: float
    inflation_rate: float

    @property
    def hidden_reserves(self) -> float:
        """Return hidden reserves (German: Stille Reserven)."""
        return self.asset_market_value - self.asset_book_value

    @property
    def equity_market(self) -> float:
        """Return economic equity based on market values."""
        return (
                self.asset_market_value
                - self.pension_obligation
                - self.hidden_reserves
        )

    @property
    def equity_book(self) -> float:
        """Return accounting equity based on book values."""
        return (
                self.asset_book_value
                - self.pension_obligation
        )

    @property
    def funding_ratio(self) -> float:
        """Return funding ratio (German: Deckungsgrad)."""

        if self.pension_obligation <= 0:
            return 0.0

        return (
                self.asset_market_value
                / self.pension_obligation
        )

    def is_balanced(self) -> bool:
        """
        Verify that the balance sheet is internally consistent.
        """

        market_assets = self.asset_market_value

        market_liabilities = (
                self.pension_obligation
                + self.hidden_reserves
                + self.equity_market
        )

        book_assets = self.asset_book_value

        book_liabilities = (
                self.pension_obligation
                + self.equity_book
        )

        tolerance = 1e-6

        return (
                abs(market_assets - market_liabilities) < tolerance
                and
                abs(book_assets - book_liabilities) < tolerance
        )