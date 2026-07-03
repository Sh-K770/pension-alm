from dataclasses import dataclass
from collections.abc import Mapping


@dataclass(frozen=True)
class ValuationEngine:
    """Generic valuation engine for projected cash flows.

    The engine is intentionally independent of asset or liability types.
    It does not know whether the cash flows come from a bond, equity,
    infrastructure asset, real estate investment, or pension obligation.

    Version 1 implements a simple discounted-cash-flow valuation:

        value = sum(CF_t / (1 + r)^t)

    Later versions can support yield curves, scenario-dependent rates,
    credit spreads, liquidity premiums, or alternative valuation strategies.
    """

    discount_rate: float

    def __post_init__(self) -> None:
        if self.discount_rate <= -1:
            raise ValueError("discount_rate must be greater than -1")

    def discount_factor(self, year: int) -> float:
        """Return the discount factor for a projection year."""
        if year < 0:
            raise ValueError("year must be non-negative")

        return 1.0 / (1.0 + self.discount_rate) ** year

    def value(self, cash_flows: Mapping[int, float]) -> float:
        """Compute the present value of projected cash flows.

        Parameters
        ----------
        cash_flows:
            Mapping from projection year to cash-flow amount.

            Example:
                {1: 5.0, 2: 5.0, 3: 105.0}

        Notes
        -----
        Positive cash flows can represent asset inflows.
        Negative cash flows can represent liability payments.
        The engine treats both consistently.
        """
        return sum(
            amount * self.discount_factor(year)
            for year, amount in cash_flows.items()
        )