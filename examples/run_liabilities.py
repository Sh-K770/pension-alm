import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.discount import DiscountEngine
from pension_alm.liabilities import Liability
from pension_alm.member import Member, MemberStatus, Sex
from pension_alm.mortality import GompertzMortality
from pension_alm.pension_projection import PensionCashFlowProjector


def main() -> None:

    members = [

        Member(
            member_id="M001",
            age=67,
            sex=Sex.FEMALE,
            status=MemberStatus.RETIRED,
            annual_pension=24_000,
            retirement_age=65,
        ),

        Member(
            member_id="M002",
            age=70,
            sex=Sex.MALE,
            status=MemberStatus.RETIRED,
            annual_pension=18_000,
            retirement_age=65,
        ),

    ]

    mortality = GompertzMortality()

    projector = PensionCashFlowProjector(
        mortality_model=mortality,
        inflation_rate=0.02,
    )

    discount_engine = DiscountEngine(
        discount_rate=0.03,
    )

    liability = Liability(
        members=members,
        projector=projector,
        discount_engine=discount_engine,
        projection_horizon=40,
    )

    print("Liability Example")
    print("-" * 50)

    print(f"Number of members: {liability.number_of_members()}")

    print("\nProjected Cash Flows")

    cash_flows = liability.cash_flows()

    for year, amount in cash_flows.items():
        print(f"Year {year:2d}: {amount:,.2f}")

    print("\nPresent Value")

    print(f"{liability.present_value():,.2f}")


if __name__ == "__main__":
    main()