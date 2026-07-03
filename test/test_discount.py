import pytest

from pension_alm.discount import DiscountEngine


def test_discount_factor_year_1():
    engine = DiscountEngine(discount_rate=0.03)

    assert engine.discount_factor(1) == pytest.approx(1 / 1.03)


def test_present_value():
    engine = DiscountEngine(discount_rate=0.03)

    cash_flows = {
        1: 100.0,
        2: 100.0,
    }

    expected = 100 / 1.03 + 100 / (1.03 ** 2)

    assert engine.present_value(cash_flows) == pytest.approx(expected)


def test_invalid_discount_rate():
    with pytest.raises(ValueError):
        DiscountEngine(discount_rate=-1.0)