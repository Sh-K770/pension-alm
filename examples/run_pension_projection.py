import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.member import Member, MemberStatus, Sex
from pension_alm.mortality import GompertzMortality
from pension_alm.pension_projection import PensionCashFlowProjector


def main() -> None:
    member = Member(
        member_id="MEMBER-001",
        age=67,
        sex=Sex.FEMALE,
        status=MemberStatus.RETIRED,
        annual_pension=24_000.0,
        retirement_age=65,
    )

    mortality = GompertzMortality()
    projector = PensionCashFlowProjector(
        mortality_model=mortality,
        inflation_rate=0.02,
    )

    cash_flows = projector.project_member_cash_flows(
        member=member,
        years=range(1, 11),
    )

    print("Pension Cash Flow Projection Example")
    for year, cash_flow in cash_flows.items():
        print(f"Year {year}: {cash_flow:,.2f}")


if __name__ == "__main__":
    main()