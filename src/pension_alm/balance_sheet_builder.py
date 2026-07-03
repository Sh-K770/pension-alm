from dataclasses import dataclass

from pension_alm.balance_sheet import BalanceSheetSnapshot
from pension_alm.liabilities import Liability
from pension_alm.portfolio import Portfolio


@dataclass(frozen=True)
class BalanceSheetBuilder:
    """Builds balance-sheet snapshots from portfolio and liability models."""

    portfolio: Portfolio
    liability: Liability
    interest_rate: float
    inflation_rate: float

    def build(self, projection_year: int) -> BalanceSheetSnapshot:
        """Build a balance-sheet snapshot for a projection year."""

        if projection_year <= 0:
            raise ValueError("projection_year must be positive")

        return BalanceSheetSnapshot(
            projection_year=projection_year,
            asset_market_value=self.portfolio.market_value(),
            asset_book_value=self.portfolio.book_value(),
            pension_obligation=abs(self.liability.present_value()),
            interest_rate=self.interest_rate,
            inflation_rate=self.inflation_rate,
        )