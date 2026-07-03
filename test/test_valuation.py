import pytest

from pension_alm.valuation import ValuationEngine


def test_value_cash_flows():
    engine = ValuationEngine(discount_rate=0.05)

    cash_flows = {
        1: 105.0,
        2: 110.0,
    }

    expected = 105 / 1.05 + 110 / (1.05 ** 2)

    assert engine.value(cash_flows) == pytest.approx(expected)


def test_invalid_discount_rate():
    with pytest.raises(ValueError):
        ValuationEngine(discount_rate=-1.0)