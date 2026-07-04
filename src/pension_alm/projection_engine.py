from dataclasses import dataclass
from collections.abc import Iterable

from pension_alm.balance_sheet import BalanceSheetSnapshot
from pension_alm.balance_sheet_builder import BalanceSheetBuilder
from pension_alm.liabilities import Liability
from pension_alm.portfolio import Portfolio
from pension_alm.scenarios import ScenarioSet


@dataclass(frozen=True)
class ProjectionEngine:
    """Run scenario-based ALM balance-sheet projections."""

    portfolio: Portfolio
    liability: Liability

    def run(self, scenario: ScenarioSet) -> list[BalanceSheetSnapshot]:
        builder = BalanceSheetBuilder(
            portfolio=self.portfolio,
            liability=self.liability,
        )

        snapshots: list[BalanceSheetSnapshot] = []

        for scenario_year in scenario:
            snapshots.append(
                builder.build(
                    scenario_id=scenario.scenario_id,
                    projection_year=scenario_year.year,
                    interest_rate=scenario_year.interest_rate,
                    inflation_rate=scenario_year.inflation_rate,
                )
            )

        return snapshots

    def run_all(
            self,
            scenarios: Iterable[ScenarioSet],
    ) -> dict[str, list[BalanceSheetSnapshot]]:
        """Run projections for multiple scenario paths."""
        return {
            scenario.scenario_id: self.run(scenario)
            for scenario in scenarios
        }