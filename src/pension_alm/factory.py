from pension_alm.bonds import Bond
from pension_alm.portfolio import Portfolio


class PortfolioFactory:
    """Factory for building portfolios from raw asset records.

    This class separates data input from the portfolio domain model.

    In production-like systems, asset data may come from SQL, CSV, Excel,
    or an external data provider. The Portfolio itself should not know
    where the data came from.
    """

    @staticmethod
    def from_records(records: list[dict]) -> Portfolio:
        """Build a Portfolio from a list of asset records."""
        portfolio = Portfolio()

        for record in records:
            asset_type = record["type"].lower()

            if asset_type == "bond":
                asset = Bond(
                    asset_id=record["asset_id"],
                    market_value=record["market_value"],
                    book_value=record["book_value"],
                    coupon_rate=record["coupon_rate"],
                    face_value=record["face_value"],
                    maturity_year=record["maturity_year"],
                    rating=record.get("rating", "Investment Grade"),
                    default_probability=record.get("default_probability", 0.0),
                    recovery_rate=record.get("recovery_rate", 0.4),
                )
            else:
                raise ValueError(f"Unsupported asset type: {asset_type}")

            portfolio.add_asset(asset)

        return portfolio