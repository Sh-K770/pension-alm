from dataclasses import dataclass, field
from collections.abc import Iterator


@dataclass(frozen=True)
class EconomicScenario:
    """External economic scenario for one projection year."""

    scenario_id: str
    year: int
    interest_rate: float
    inflation_rate: float

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("scenario_id must not be empty")
        if self.year <= 0:
            raise ValueError("year must be positive")
        if self.interest_rate <= -1:
            raise ValueError("interest_rate must be greater than -1")
        if self.inflation_rate <= -1:
            raise ValueError("inflation_rate must be greater than -1")


@dataclass(frozen=True)
class ScenarioSet:
    """One economic scenario path over the projection horizon."""

    scenario_id: str
    scenarios: list[EconomicScenario] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("scenario_id must not be empty")

        scenario_ids = {scenario.scenario_id for scenario in self.scenarios}

        if scenario_ids and scenario_ids != {self.scenario_id}:
            raise ValueError(
                "All EconomicScenario objects must have the same scenario_id"
            )

    def years(self) -> list[int]:
        """Return projection years available in the scenario path."""
        return [scenario.year for scenario in self.scenarios]

    def get_by_year(self, year: int) -> EconomicScenario:
        """Return the economic scenario for a given projection year."""
        if year <= 0:
            raise ValueError("year must be positive")

        for scenario in self.scenarios:
            if scenario.year == year:
                return scenario

        raise ValueError(f"No scenario data found for year {year}")

    def __len__(self) -> int:
        return len(self.scenarios)

    def __iter__(self) -> Iterator[EconomicScenario]:
        return iter(self.scenarios)