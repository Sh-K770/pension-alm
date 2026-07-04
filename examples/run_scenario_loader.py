from pension_alm.scenario_loader import ScenarioLoader


def main() -> None:

    loader = ScenarioLoader()
    from pathlib import Path

    print("Current working directory:", Path.cwd())

    from pathlib import Path

    csv_file = Path(__file__).parent / "data" / "sample_scenarios.csv"

    scenarios = loader.load(csv_file)

    print(f"Loaded {len(scenarios)} scenario paths.\n")

    for scenario_set in scenarios:

        print(f"Scenario: {scenario_set.scenario_id}")

        for scenario in scenario_set:
            print(
                f"Year {scenario.year:2d} | "
                f"Interest = {scenario.interest_rate:.2%} | "
                f"Inflation = {scenario.inflation_rate:.2%}"
            )

        print()


if __name__ == "__main__":
    main()