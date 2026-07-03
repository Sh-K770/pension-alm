from dataclasses import dataclass, field
from collections.abc import Iterable

from pension_alm.assets import Asset


@dataclass
class Portfolio:
    """Portfolio of pension fund assets.

    The portfolio aggregates asset-level information such as market value,
    book value, hidden reserves ("Stille Reserven"), and projected cash flows.
    """

    assets: list[Asset] = field(default_factory=list)

    def add_asset(self, asset: Asset) -> None:
        """Add an asset to the portfolio."""
        self.assets.append(asset)

    def market_value(self) -> float:
        """Return total market value of all assets."""
        return sum(asset.market_value for asset in self.assets)

    def book_value(self) -> float:
        """Return total book value of all assets."""
        return sum(asset.book_value for asset in self.assets)

    def hidden_reserves(self) -> float:
        """Return hidden reserves ("Stille Reserven").

        Hidden reserves are defined as:

            market value - book value
        """
        return self.market_value() - self.book_value()

    def cash_flows(
            self,
            years: Iterable[int],
            interest_rate: float,
    ) -> dict[int, float]:
        """Aggregate projected cash flows from all assets."""
        aggregated_cash_flows: dict[int, float] = {}

        for year in years:
            aggregated_cash_flows[year] = sum(
                asset.cash_flow(year=year, interest_rate=interest_rate)
                for asset in self.assets
            )

        return aggregated_cash_flows

    def allocation(self) -> dict[str, float]:
        """Return asset allocation by class name based on market value."""
        total_market_value = self.market_value()

        if total_market_value == 0:
            return {}

        allocation: dict[str, float] = {}

        for asset in self.assets:
            asset_type = asset.__class__.__name__
            allocation[asset_type] = allocation.get(asset_type, 0.0) + asset.market_value

        return {
            asset_type: value / total_market_value
            for asset_type, value in allocation.items()
        }

    def __len__(self) -> int:
        return len(self.assets)

    def __iter__(self):
        return iter(self.assets)