import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.balance_sheet_builder import BalanceSheetBuilder
from pension_alm.bonds import Bond
from pension_alm.discount import DiscountEngine
from pension_alm.liabilities import Liability
from pension_alm.member import Member, MemberStatus, Sex
from pension_alm.mortality import GompertzMortality
from pension_alm.pension_projection import PensionCashFlowProjector
from pension_alm.portfolio import Portfolio


def main() -> None:
    portfolio = Portfolio()

    portfolio.add_asset(
        Bond(
            asset_id="BOND-001",
            market_value=160_000.0,
            book_value=150_000.0,
            face_value=150_000.0,
            coupon_rate=0.03,
            maturity_year=5,
            rating="AA",
        )
    )

    members = [
        Member(
            member_id="M001",
            age=67,
            sex=Sex.FEMALE,
            status=MemberStatus.RETIRED,
            annual_pension=24_000,
            retirement_age=65,
        )
    ]

    mortality = GompertzMortality()

    projector = PensionCashFlowProjector(
        mortality_model=mortality,
        inflation_rate=0.02,
    )

    discount_engine = DiscountEngine(discount_rate=0.03)

    liability = Liability(
        members=members,
        projector=projector,
        discount_engine=discount_engine,
        projection_horizon=40,
    )

    builder = BalanceSheetBuilder(
        portfolio=portfolio,
        liability=liability,
        interest_rate=0.03,
        inflation_rate=0.02,
    )

    snapshot = builder.build(projection_year=1)

    print("Balance Sheet Builder Example")
    print("-" * 50)
    print(f"Projection Year   : {snapshot.projection_year}")
    print(f"Market Value      : {snapshot.asset_market_value:,.2f}")
    print(f"Book Value        : {snapshot.asset_book_value:,.2f}")
    print(f"Pension Liability : {snapshot.pension_obligation:,.2f}")
    print(f"Hidden Reserves   : {snapshot.hidden_reserves:,.2f}")
    print(f"Market Equity     : {snapshot.equity_market:,.2f}")
    print(f"Book Equity       : {snapshot.equity_book:,.2f}")
    print(f"Funding Ratio     : {snapshot.funding_ratio:.2%}")
    print(f"Balanced          : {snapshot.is_balanced()}")


if __name__ == "__main__":
    main()