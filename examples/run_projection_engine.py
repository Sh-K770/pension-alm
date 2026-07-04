from dataclasses import dataclass
from pathlib import Path

from pension_alm.alm_report import ALMReport
from pension_alm.alternative_assets import Equity, RealEstate
from pension_alm.bonds import Bond
from pension_alm.infrastructure import Infrastructure
from pension_alm.portfolio import Portfolio
from pension_alm.projection_engine import ProjectionEngine
from pension_alm.scenario_loader import ScenarioLoader


@dataclass(frozen=True)
class SimpleLiability:
    value: float

    def present_value(self) -> float:
        return self.value


def main() -> None:
    # ---------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------

    portfolio = Portfolio()

    portfolio.add_asset(
        Bond(
            asset_id="BOND-001",
            market_value=100_000,
            book_value=95_000,
            face_value=100_000,
            coupon_rate=0.03,
            maturity_year=10,
            rating="A",
        )
    )

    portfolio.add_asset(
        Equity(
            asset_id="EQ-001",
            market_value=100_000,
            book_value=90_000,
            expected_return=0.06,
            dividend_yield=0.02,
        )
    )

    portfolio.add_asset(
        RealEstate(
            asset_id="RE-001",
            market_value=200_000,
            book_value=180_000,
            rental_yield=0.03,
            appreciation_rate=0.02,
        )
    )

    portfolio.add_asset(
        Infrastructure(
            asset_id="INFRA-001",
            market_value=150_000,
            book_value=140_000,
            bond_weight=0.5,
            equity_weight=0.5,
            bond_yield=0.03,
            equity_return=0.04,
            equity_dividend_yield=0.02,
        )
    )

    # ---------------------------------------------------------
    # Liability
    # ---------------------------------------------------------

    liability = SimpleLiability(
        value=420_000,
    )

    # ---------------------------------------------------------
    # Load Scenarios
    # ---------------------------------------------------------

    loader = ScenarioLoader()

    csv_file = (
            Path(__file__).parent
            / "data"
            / "sample_scenarios.csv"
    )

    scenario_sets = loader.load(csv_file)

    # ---------------------------------------------------------
    # Projection Engine
    # ---------------------------------------------------------

    engine = ProjectionEngine(
        portfolio=portfolio,
        liability=liability,
    )

    results = engine.run_all(scenario_sets)

    print("=" * 80)
    print("ASSET-LIABILITY MANAGEMENT PROJECTION")
    print("=" * 80)

    for scenario_id, snapshots in results.items():

        report = ALMReport(snapshots)

        print(f"\nScenario: {scenario_id}")
        print("-" * 80)

        for snapshot in snapshots:

            print(
                f"Year {snapshot.projection_year:2d} | "
                f"Assets MV: {snapshot.asset_market_value:12,.2f} | "
                f"Liability: {snapshot.pension_obligation:12,.2f} | "
                f"Funding Ratio: {snapshot.funding_ratio:7.2%}"
            )

        print("\nSummary")
        print("-" * 80)

        summary = report.summary()

        print(f"Projection Years      : {summary['number_of_years']}")
        print(f"Average Funding Ratio : {summary['average_funding_ratio']:.2%}")
        print(f"Minimum Funding Ratio : {summary['minimum_funding_ratio']:.2%}")
        print(f"Maximum Funding Ratio : {summary['maximum_funding_ratio']:.2%}")
        print(f"Average Hidden Reserve: {summary['average_hidden_reserves']:,.2f}")
        print(f"Final Market Equity   : {summary['final_market_equity']:,.2f}")
        print(f"Final Book Equity     : {summary['final_book_equity']:,.2f}")

        print()

    print("=" * 80)


if __name__ == "__main__":
    main()