from dataclasses import dataclass, field
from collections.abc import Iterable, Iterator

from pension_alm.assets import Asset


@dataclass
class Portfolio:
    """Portfolio of pension fund assets."""

    assets: list[Asset] = field(default_factory=list)

    def add_asset(self, asset: Asset) -> None:
        self.assets.append(asset)

    def market_value(self) -> float:
        return sum(asset.market_value for asset in self.assets)

    def book_value(self) -> float:
        return sum(asset.book_value for asset in self.assets)

    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        return sum(
            asset.projected_market_value(year, interest_rate, inflation_rate)
            for asset in self.assets
        )

    def projected_book_value(
            self,
            year: int,
            interest_rate: float,
    ) -> float:
        return sum(
            asset.projected_book_value(year, interest_rate)
            for asset in self.assets
        )

    def hidden_reserves(self) -> float:
        return self.market_value() - self.book_value()

    def cash_flows(
            self,
            years: Iterable[int],
            interest_rate: float,
    ) -> dict[int, float]:
        return {
            year: sum(
                asset.cash_flow(year=year, interest_rate=interest_rate)
                for asset in self.assets
            )
            for year in years
        }

    def allocation(self) -> dict[str, float]:
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

    def __iter__(self) -> Iterator[Asset]:
        return iter(self.assets)