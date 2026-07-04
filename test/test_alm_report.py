import pytest

from pension_alm.alm_report import ALMReport
from pension_alm.balance_sheet import BalanceSheetSnapshot


@pytest.fixture
def snapshots():

    return [

        BalanceSheetSnapshot(
            scenario_id="BASE",
            projection_year=1,
            asset_market_value=1000,
            asset_book_value=900,
            pension_obligation=800,
            interest_rate=0.03,
            inflation_rate=0.02,
        ),

        BalanceSheetSnapshot(
            scenario_id="BASE",
            projection_year=2,
            asset_market_value=1100,
            asset_book_value=920,
            pension_obligation=790,
            interest_rate=0.03,
            inflation_rate=0.02,
        ),

        BalanceSheetSnapshot(
            scenario_id="BASE",
            projection_year=3,
            asset_market_value=1200,
            asset_book_value=940,
            pension_obligation=780,
            interest_rate=0.03,
            inflation_rate=0.02,
        ),
    ]


def test_number_of_years(snapshots):

    report = ALMReport(snapshots)

    assert report.number_of_years() == 3


def test_first_snapshot(snapshots):

    report = ALMReport(snapshots)

    assert report.first_snapshot().projection_year == 1


def test_final_snapshot(snapshots):

    report = ALMReport(snapshots)

    assert report.final_snapshot().projection_year == 3


def test_average_funding_ratio(snapshots):

    report = ALMReport(snapshots)

    assert report.average_funding_ratio() > 1


def test_minimum_funding_ratio(snapshots):

    report = ALMReport(snapshots)

    assert report.minimum_funding_ratio() == min(report.funding_ratios())


def test_maximum_funding_ratio(snapshots):

    report = ALMReport(snapshots)

    assert report.maximum_funding_ratio() == max(report.funding_ratios())


def test_average_hidden_reserves(snapshots):

    report = ALMReport(snapshots)

    assert report.average_hidden_reserves() > 0


def test_summary(snapshots):

    report = ALMReport(snapshots)

    summary = report.summary()

    assert summary["scenario_id"] == "BASE"
    assert summary["number_of_years"] == 3


def test_empty_report():

    with pytest.raises(ValueError):

        ALMReport([])