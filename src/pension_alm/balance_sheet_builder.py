from dataclasses import dataclass

from pension_alm.balance_sheet import BalanceSheetSnapshot
from pension_alm.liabilities import Liability
from pension_alm.portfolio import Portfolio


@dataclass(frozen=True)
class BalanceSheetBuilder:
    """Build balance-sheet snapshots from portfolio, liability, and scenario data."""

    portfolio: Portfolio
    liability: Liability

    def build(
            self,
            scenario_id: str,
            projection_year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> BalanceSheetSnapshot:
        if projection_year <= 0:
            raise ValueError("projection_year must be positive")

        return BalanceSheetSnapshot(
            scenario_id=scenario_id,
            projection_year=projection_year,
            asset_market_value=self.portfolio.projected_market_value(
                year=projection_year,
                interest_rate=interest_rate,
                inflation_rate=inflation_rate,
            ),
            asset_book_value=self.portfolio.projected_book_value(
                year=projection_year,
                interest_rate=interest_rate,
            ),
            pension_obligation=self.liability.present_value(),
            interest_rate=interest_rate,
            inflation_rate=inflation_rate,
        )