from dataclasses import dataclass

from pension_alm.assets import Asset
from pension_alm.bonds import Bond
from pension_alm.alternative_assets import Equity


@dataclass
class Infrastructure(Asset):
    """Infrastructure asset modeled as a combination of bond-like and equity-like exposure."""

    bond_weight: float = 0.5
    equity_weight: float = 0.5
    bond_yield: float = 0.03
    equity_return: float = 0.04
    equity_dividend_yield: float = 0.02

    def __post_init__(self) -> None:
        super().__post_init__()

        if not 0 <= self.bond_weight <= 1:
            raise ValueError("bond_weight must be between 0 and 1")
        if not 0 <= self.equity_weight <= 1:
            raise ValueError("equity_weight must be between 0 and 1")
        if abs((self.bond_weight + self.equity_weight) - 1.0) > 1e-8:
            raise ValueError("bond_weight and equity_weight must sum to 1")

        self._bond_component = Bond(
            asset_id=f"{self.asset_id}-BOND",
            market_value=self.market_value * self.bond_weight,
            book_value=self.book_value * self.bond_weight,
            face_value=self.market_value * self.bond_weight,
            coupon_rate=self.bond_yield,
            maturity_year=30,
            rating="A",
        )

        self._equity_component = Equity(
            asset_id=f"{self.asset_id}-EQUITY",
            market_value=self.market_value * self.equity_weight,
            book_value=self.book_value * self.equity_weight,
            expected_return=self.equity_return,
            dividend_yield=self.equity_dividend_yield,
        )

    def cash_flow(self, year: int, interest_rate: float) -> float:
        if year <= 0:
            raise ValueError("year must be positive")

        return (
                self._bond_component.cash_flow(year, interest_rate)
                + self._equity_component.cash_flow(year, interest_rate)
        )

    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        if year < 0:
            raise ValueError("year must be non-negative")

        return (
                self._bond_component.projected_market_value(
                    year,
                    interest_rate,
                    inflation_rate,
                )
                + self._equity_component.projected_market_value(
            year,
            interest_rate,
            inflation_rate,
        )
        )

    def projected_book_value(self, year: int, interest_rate: float) -> float:
        if year < 0:
            raise ValueError("year must be non-negative")

        return (
                self._bond_component.projected_book_value(year, interest_rate)
                + self._equity_component.projected_book_value(year, interest_rate)
        )