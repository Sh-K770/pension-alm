import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.balance_sheet import BalanceSheetSnapshot


def main() -> None:

    balance_sheet = BalanceSheetSnapshot(
        projection_year=1,
        asset_market_value=203.0,
        asset_book_value=200.0,
        pension_obligation=180.0,
        interest_rate=0.03,
        inflation_rate=0.02,
    )

    print("Balance Sheet Snapshot Example")
    print("-" * 50)

    print(f"Projection year : {balance_sheet.projection_year}")

    print(f"Market value    : {balance_sheet.asset_market_value:.2f}")
    print(f"Book value      : {balance_sheet.asset_book_value:.2f}")

    print(f"Pension liability : {balance_sheet.pension_obligation:.2f}")

    print()

    print(f"Hidden reserves : {balance_sheet.hidden_reserves:.2f}")
    print(f"Market equity   : {balance_sheet.equity_market:.2f}")
    print(f"Book equity     : {balance_sheet.equity_book:.2f}")

    print()

    print(f"Funding ratio   : {balance_sheet.funding_ratio:.2%}")

    print()

    print(f"Balanced        : {balance_sheet.is_balanced()}")


if __name__ == "__main__":
    main()