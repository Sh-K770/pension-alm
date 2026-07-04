from dataclasses import dataclass

from pension_alm.alternative_assets import Equity
from pension_alm.portfolio import Portfolio
from pension_alm.projection_engine import ProjectionEngine
from pension_alm.scenarios import EconomicScenario, ScenarioSet


@dataclass(frozen=True)
class SimpleLiability:
    value: float

    def present_value(self) -> float:
        return self.value


def test_projection_engine():

    portfolio = Portfolio()

    portfolio.add_asset(
        Equity(
            asset_id="EQ-001",
            market_value=1000,
            book_value=900,
            expected_return=0.06,
            dividend_yield=0.02,
        )
    )

    liability = SimpleLiability(800)

    scenario = ScenarioSet(
        scenario_id="BASE",
        scenarios=[
            EconomicScenario(
                scenario_id="BASE",
                year=1,
                interest_rate=0.03,
                inflation_rate=0.02,
            ),
            EconomicScenario(
                scenario_id="BASE",
                year=2,
                interest_rate=0.035,
                inflation_rate=0.02,
            ),
        ],
    )

    engine = ProjectionEngine(
        portfolio=portfolio,
        liability=liability,
    )

    snapshots = engine.run(scenario)

    assert len(snapshots) == 2
    assert snapshots[0].projection_year == 1
    assert snapshots[1].projection_year == 2
    assert snapshots[0].scenario_id == "BASE"


def test_projection_engine_run_all():

    portfolio = Portfolio()

    portfolio.add_asset(
        Equity(
            asset_id="EQ-001",
            market_value=1000,
            book_value=900,
            expected_return=0.06,
            dividend_yield=0.02,
        )
    )

    liability = SimpleLiability(800)

    scenario = ScenarioSet(
        scenario_id="BASE",
        scenarios=[
            EconomicScenario(
                scenario_id="BASE",
                year=1,
                interest_rate=0.03,
                inflation_rate=0.02,
            )
        ],
    )

    engine = ProjectionEngine(
        portfolio=portfolio,
        liability=liability,
    )

    results = engine.run_all([scenario])

    assert "BASE" in results
    assert len(results["BASE"]) == 1