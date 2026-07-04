import pytest

from pension_alm.alternative_assets import Equity
from pension_alm.alternative_assets import RealEstate
from pension_alm.infrastructure import Infrastructure

def test_equity_cash_flow():
    equity = Equity(
        asset_id="EQ-001",
        market_value=100_000,
        book_value=90_000,
        expected_return=0.06,
        dividend_yield=0.02,
    )

    assert equity.cash_flow(1, 0.03) == pytest.approx(2000.0)


def test_equity_market_value_projection():
    equity = Equity(
        asset_id="EQ-001",
        market_value=100_000,
        book_value=90_000,
        expected_return=0.06,
        dividend_yield=0.02,
    )

    expected = 100_000 * (1.06) ** 5

    assert equity.projected_market_value(5, 0.03, 0.00) == pytest.approx(expected)


def test_real_estate_cash_flow():
    real_estate = RealEstate(
        asset_id="RE-001",
        market_value=200_000,
        book_value=180_000,
        rental_yield=0.03,
        appreciation_rate=0.02,
    )

    assert real_estate.cash_flow(1, 0.03) == pytest.approx(6000.0)


def test_real_estate_market_value_projection():
    real_estate = RealEstate(
        asset_id="RE-001",
        market_value=200_000,
        book_value=180_000,
        rental_yield=0.03,
        appreciation_rate=0.02,
    )

    expected = 200_000 * (1.04) ** 5

    assert real_estate.projected_market_value(
        5,
        interest_rate=0.03,
        inflation_rate=0.02,
    ) == pytest.approx(expected)


def test_equity_invalid_dividend():
    with pytest.raises(ValueError):
        Equity(
            asset_id="EQ",
            market_value=100,
            book_value=100,
            dividend_yield=1.5,
        )
def test_real_estate_invalid_rental_yield():
    with pytest.raises(ValueError):
        RealEstate(
            asset_id="RE",
            market_value=100,
            book_value=100,
            rental_yield=-0.1,
        )
