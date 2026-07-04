from dataclasses import dataclass
import random

from pension_alm.scenarios import EconomicScenario, ScenarioSet


@dataclass(frozen=True)
class MonteCarloScenarioGenerator:
    """Generate stochastic economic scenarios."""

    projection_horizon: int
    number_of_paths: int

    initial_interest_rate: float
    initial_inflation_rate: float

    interest_rate_volatility: float = 0.01
    inflation_volatility: float = 0.005

    random_seed: int | None = None

    def __post_init__(self) -> None:

        if self.projection_horizon <= 0:
            raise ValueError("projection_horizon must be positive")

        if self.number_of_paths <= 0:
            raise ValueError("number_of_paths must be positive")

        if self.random_seed is not None:
            random.seed(self.random_seed)

    def generate(self) -> list[ScenarioSet]:

        scenario_sets: list[ScenarioSet] = []

        for path in range(1, self.number_of_paths + 1):

            interest_rate = self.initial_interest_rate
            inflation_rate = self.initial_inflation_rate

            scenarios: list[EconomicScenario] = []

            for year in range(1, self.projection_horizon + 1):

                interest_rate += random.gauss(
                    0.0,
                    self.interest_rate_volatility,
                )

                inflation_rate += random.gauss(
                    0.0,
                    self.inflation_volatility,
                )

                scenarios.append(
                    EconomicScenario(
                        scenario_id=f"MC-{path:05d}",
                        year=year,
                        interest_rate=interest_rate,
                        inflation_rate=inflation_rate,
                    )
                )

            scenario_sets.append(
                ScenarioSet(
                    scenario_id=f"MC-{path:05d}",
                    scenarios=scenarios,
                )
            )

        return scenario_sets