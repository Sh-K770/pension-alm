from dataclasses import dataclass
import math


@dataclass(frozen=True)
class GompertzMortality:
    """Gompertz mortality model.

    The model approximates age-dependent mortality using:

        q(x) = 1 - exp(-B * c^x)

    where q(x) is the one-year mortality probability at age x.

    This is a simplified research implementation, not an official actuarial
    mortality table.
    """

    B: float = 0.00022
    c: float = 1.095

    def __post_init__(self) -> None:
        if self.B <= 0:
            raise ValueError("B must be positive")
        if self.c <= 1:
            raise ValueError("c must be greater than 1")

    def mortality_rate(self, age: int) -> float:
        """Return one-year mortality probability at a given age."""
        if age < 0:
            raise ValueError("age must be non-negative")

        return 1.0 - math.exp(-self.B * self.c**age)

    def survival_probability(self, current_age: int, years: int) -> float:
        """Return survival probability from current_age over a number of years.

        This computes:

            product_{t=0}^{years-1} (1 - q(current_age + t))
        """
        if current_age < 0:
            raise ValueError("current_age must be non-negative")
        if years < 0:
            raise ValueError("years must be non-negative")

        survival = 1.0

        for t in range(years):
            age = current_age + t
            # Assume independence of yearly survival events.
            survival *= 1.0 - self.mortality_rate(age)

        return survival

    def death_probability(self, current_age: int, years: int) -> float:
     """Probability of dying within the next `years` years."""
     return 1.0 - self.survival_probability(current_age, years)