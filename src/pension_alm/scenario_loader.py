from pathlib import Path

import pandas as pd

from pension_alm.scenarios import EconomicScenario, ScenarioSet


class ScenarioLoader:
    """Load external scenarios from CSV files."""

    def load(self, file_path: str | Path) -> list[ScenarioSet]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() == ".csv":
            return self._load_csv(path)

        raise ValueError(f"Unsupported file format: {path.suffix}")

    def _load_csv(self, path: Path) -> list[ScenarioSet]:
        df = pd.read_csv(path)

        required_columns = {
            "scenario_id",
            "year",
            "interest_rate",
            "inflation_rate",
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        scenario_sets: list[ScenarioSet] = []

        for scenario_id, group in df.groupby("scenario_id"):
            scenarios = [
                EconomicScenario(
                    scenario_id=str(row.scenario_id),
                    year=int(row.year),
                    interest_rate=float(row.interest_rate),
                    inflation_rate=float(row.inflation_rate),
                )
                for row in group.sort_values("year").itertuples(index=False)
            ]

            scenario_sets.append(
                ScenarioSet(
                    scenario_id=str(scenario_id),
                    scenarios=scenarios,
                )
            )

        return scenario_sets