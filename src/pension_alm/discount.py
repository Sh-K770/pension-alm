from dataclasses import dataclass
from collections.abc import Mapping


@dataclass(frozen=True)
class DiscountEngine:
    """Discount engine for present-value calculations."""

    discount_rate: float

    def __post_init__(self) -> None:
        if self.discount_rate <= -1:
            raise ValueError("discount_rate must be greater than -1")

    def discount_factor(self, year: int) -> float:
        """Return discount factor for a given projection year."""
        if year < 0:
            raise ValueError("year must be non-negative")

        return 1.0 / (1.0 + self.discount_rate) ** year

    def present_value(self, cash_flows: Mapping[int, float]) -> float:
        """Compute present value of annual cash flows.

        Parameters
        ----------
        cash_flows:
            Mapping from projection year to cash-flow amount.
            Example: {1: 5.0, 2: 5.0, 3: 105.0}
        """
        return sum(
            amount * self.discount_factor(year)
            for year, amount in cash_flows.items()
        )