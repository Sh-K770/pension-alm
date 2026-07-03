import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.factory import PortfolioFactory


def main() -> None:
    asset_records = [
        {
            "type": "bond",
            "asset_id": "BOND-001",
            "market_value": 105.0,
            "book_value": 100.0,
            "coupon_rate": 0.05,
            "face_value": 100.0,
            "maturity_year": 3,
            "rating": "AA",
        },
        {
            "type": "bond",
            "asset_id": "BOND-002",
            "market_value": 98.0,
            "book_value": 100.0,
            "coupon_rate": 0.03,
            "face_value": 100.0,
            "maturity_year": 5,
            "rating": "A",
        },
    ]

    portfolio = PortfolioFactory.from_records(asset_records)

    print("Portfolio Factory Example")
    print(f"Number of assets: {len(portfolio)}")
    print(f"Market value: {portfolio.market_value():,.2f}")
    print(f"Book value: {portfolio.book_value():,.2f}")
    print(f"Hidden reserves: {portfolio.hidden_reserves():,.2f}")
    print(f"Allocation: {portfolio.allocation()}")


if __name__ == "__main__":
    main()