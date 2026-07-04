import pytest

from pension_alm.infrastructure import Infrastructure


def test_infrastructure_can_be_created():
    infrastructure = Infrastructure(
        asset_id="INFRA-001",
        market_value=150_000.0,
        book_value=140_000.0,
        bond_weight=0.5,
        equity_weight=0.5,
        bond_yield=0.03,
        equity_return=0.04,
        equity_dividend_yield=0.02,
    )

    assert infrastructure.asset_id == "INFRA-001"
    assert infrastructure.market_value == 150_000.0
    assert infrastructure.book_value == 140_000.0


def test_infrastructure_invalid_weights():
    with pytest.raises(ValueError):
        Infrastructure(
            asset_id="INFRA-001",
            market_value=150_000.0,
            book_value=140_000.0,
            bond_weight=0.7,
            equity_weight=0.5,
        )