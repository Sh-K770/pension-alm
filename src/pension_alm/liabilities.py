from dataclasses import dataclass
from collections.abc import Iterable

from pension_alm.discount import DiscountEngine
from pension_alm.member import Member
from pension_alm.pension_projection import PensionCashFlowProjector


@dataclass(frozen=True)
class Liability:
    """Represents the total pension liability of a pension fund.

    The class aggregates member-level projected pension cash flows and
    computes their present value using a discount engine.
    """

    members: list[Member]
    projector: PensionCashFlowProjector
    discount_engine: DiscountEngine
    projection_horizon: int = 40

    def __post_init__(self) -> None:
        if self.projection_horizon <= 0:
            raise ValueError("projection_horizon must be positive")

    def number_of_members(self) -> int:
        """Return the number of members included in the liability model."""
        return len(self.members)

    def projection_years(self) -> Iterable[int]:
        """Return the projection years used for liability cash flows."""
        return range(1, self.projection_horizon + 1)

    def cash_flows(self) -> dict[int, float]:
        """Return aggregated projected pension cash flows for all members."""
        aggregated_cash_flows = {
            year: 0.0
            for year in self.projection_years()
        }

        for member in self.members:
            member_cash_flows = self.projector.project_member_cash_flows(
                member=member,
                years=self.projection_years(),
            )

            for year, amount in member_cash_flows.items():
                aggregated_cash_flows[year] += amount

        return aggregated_cash_flows

    def present_value(self) -> float:
        """Return the present value of projected pension liabilities."""
        return self.discount_engine.present_value(self.cash_flows())