from pension_alm.alternative_assets import Equity
from pension_alm.alternative_assets import RealEstate


def main() -> None:
    assets = [
        Equity(
            asset_id="EQ-001",
            market_value=100_000.0,
            book_value=90_000.0,
            expected_return=0.06,
            dividend_yield=0.02,
        ),
        RealEstate(
            asset_id="RE-001",
            market_value=200_000.0,
            book_value=180_000.0,
            rental_yield=0.03,
            appreciation_rate=0.02,
        ),
    ]

    print("Alternative Assets Example")
    print("-" * 40)

    for asset in assets:
        print(f"\nAsset: {asset.asset_id}")
        print(f"Market Value (t=0): {asset.market_value:,.2f}")
        print(f"Book Value   (t=0): {asset.book_value:,.2f}")
        print(f"Cash Flow    (t=1): {asset.cash_flow(1, interest_rate=0.03):,.2f}")
        print(
            f"Market Value (t=5): "
            f"{asset.projected_market_value(5, 0.03, 0.02):,.2f}"
        )


if __name__ == "__main__":
    main()