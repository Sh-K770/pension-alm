from dataclasses import dataclass

from pension_alm.assets import Asset


@dataclass
class Bond(Asset):
    """Fixed-income asset with simplified credit-risk assumptions."""

    face_value: float
    coupon_rate: float
    maturity_year: int
    rating: str
    default_probability: float = 0.0
    recovery_rate: float = 0.4

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.face_value <= 0:
            raise ValueError("face_value must be positive")
        if not 0 <= self.coupon_rate <= 1:
            raise ValueError("coupon_rate must be between 0 and 1")
        if self.maturity_year <= 0:
            raise ValueError("maturity_year must be positive")
        if not 0 <= self.default_probability <= 1:
            raise ValueError("default_probability must be between 0 and 1")
        if not 0 <= self.recovery_rate <= 1:
            raise ValueError("recovery_rate must be between 0 and 1")

    def cash_flow(self, year: int, interest_rate: float) -> float:
        """Return expected bond cash flow for a projection year."""
        if year <= 0:
            raise ValueError("year must be positive")

        survival_probability = 1.0 - self.default_probability
        expected_coupon = self.face_value * self.coupon_rate * survival_probability
        expected_recovery = self.face_value * self.recovery_rate * self.default_probability

        if year < self.maturity_year:
            return expected_coupon + expected_recovery

        if year == self.maturity_year:
            expected_principal = self.face_value * survival_probability
            return expected_coupon + expected_principal + expected_recovery

        return 0.0

    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        """Project bond market value using simplified discounting."""
        if year >= self.maturity_year:
            return 0.0

        remaining_years = self.maturity_year - year
        coupon = self.face_value * self.coupon_rate

        discounted_coupons = sum(
            coupon / (1 + interest_rate) ** t
            for t in range(1, remaining_years + 1)
        )
        discounted_principal = self.face_value / (1 + interest_rate) ** remaining_years

        credit_adjustment = 1.0 - self.default_probability

        return (discounted_coupons + discounted_principal) * credit_adjustment

    def projected_book_value(
            self,
            year: int,
            interest_rate: float,
    ) -> float:
        """Project book value with a simple hold-to-maturity assumption."""
        if year >= self.maturity_year:
            return 0.0

        return self.book_value