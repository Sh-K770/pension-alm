from dataclasses import dataclass
from statistics import mean

from pension_alm.balance_sheet import BalanceSheetSnapshot


@dataclass(frozen=True)
class ALMReport:
    """Analytical summary of ALM projection results."""

    snapshots: list[BalanceSheetSnapshot]

    def __post_init__(self) -> None:
        if not self.snapshots:
            raise ValueError("snapshots must not be empty")

    def number_of_years(self) -> int:
        return len(self.snapshots)

    def first_snapshot(self) -> BalanceSheetSnapshot:
        return self.snapshots[0]

    def final_snapshot(self) -> BalanceSheetSnapshot:
        return self.snapshots[-1]

    def funding_ratios(self) -> list[float]:
        return [snapshot.funding_ratio for snapshot in self.snapshots]

    def average_funding_ratio(self) -> float:
        return mean(self.funding_ratios())

    def minimum_funding_ratio(self) -> float:
        return min(self.funding_ratios())

    def maximum_funding_ratio(self) -> float:
        return max(self.funding_ratios())

    def average_hidden_reserves(self) -> float:
        return mean(snapshot.hidden_reserves for snapshot in self.snapshots)

    def final_market_equity(self) -> float:
        return self.final_snapshot().equity_market

    def final_book_equity(self) -> float:
        return self.final_snapshot().equity_book

    def summary(self) -> dict[str, float | int | str]:
        final = self.final_snapshot()

        return {
            "scenario_id": final.scenario_id,
            "number_of_years": self.number_of_years(),
            "average_funding_ratio": self.average_funding_ratio(),
            "minimum_funding_ratio": self.minimum_funding_ratio(),
            "maximum_funding_ratio": self.maximum_funding_ratio(),
            "average_hidden_reserves": self.average_hidden_reserves(),
            "final_market_equity": self.final_market_equity(),
            "final_book_equity": self.final_book_equity(),
        }