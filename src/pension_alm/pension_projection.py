from dataclasses import dataclass
from collections.abc import Iterable

from pension_alm.member import Member
from pension_alm.mortality import GompertzMortality


@dataclass(frozen=True)
class PensionCashFlowProjector:
    """Projects expected pension cash flows for pension scheme members.

    Version 1 uses a simplified liability model:

    expected payment =
        annual pension
        × inflation adjustment
        × survival probability

    The output is an annual cash-flow table that can later be passed to
    the ValuationEngine.
    """

    mortality_model: GompertzMortality
    inflation_rate: float = 0.02

    def __post_init__(self) -> None:
        if self.inflation_rate < -1:
            raise ValueError("inflation_rate must be greater than -1")

    def project_member_cash_flows(
            self,
            member: Member,
            years: Iterable[int],
    ) -> dict[int, float]:
        """Project expected annual pension payments for one member."""
        cash_flows: dict[int, float] = {}

        for year in years:
            if year <= 0:
                raise ValueError("projection years must be positive")

            member_age = member.age + year

            if member_age < member.retirement_age:
                cash_flows[year] = 0.0
                continue

            years_since_start = year
            survival_probability = self.mortality_model.survival_probability(
                current_age=member.age,
                years=year,
            )

            inflation_factor = (1.0 + self.inflation_rate) ** years_since_start

            expected_payment = (
                    member.annual_pension
                    * inflation_factor
                    * survival_probability
            )

            cash_flows[year] = -expected_payment

        return cash_flows