import pytest

from pension_alm.balance_sheet_builder import BalanceSheetBuilder
from pension_alm.bonds import Bond
from pension_alm.discount import DiscountEngine
from pension_alm.liabilities import Liability
from pension_alm.member import Member, MemberStatus, Sex
from pension_alm.mortality import GompertzMortality
from pension_alm.pension_projection import PensionCashFlowProjector
from pension_alm.portfolio import Portfolio


def test_balance_sheet_builder_creates_valid_snapshot():
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

    member = Member(
        member_id="M001",
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

    discount_engine = DiscountEngine(discount_rate=0.03)

    liability = Liability(
        members=[member],
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

    assert snapshot.asset_market_value == pytest.approx(160_000.0)
    assert snapshot.asset_book_value == pytest.approx(150_000.0)
    assert snapshot.hidden_reserves == pytest.approx(10_000.0)
    assert snapshot.funding_ratio > 1.0
    assert snapshot.is_balanced()