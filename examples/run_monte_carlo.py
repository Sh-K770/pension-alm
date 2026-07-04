from pension_alm.monte_carlo import MonteCarloScenarioGenerator


def main() -> None:

    generator = MonteCarloScenarioGenerator(
        projection_horizon=10,
        number_of_paths=5,
        initial_interest_rate=0.03,
        initial_inflation_rate=0.02,
        interest_rate_volatility=0.01,
        inflation_volatility=0.005,
        random_seed=42,
    )

    scenario_sets = generator.generate()

    print("=" * 70)
    print("MONTE CARLO ECONOMIC SCENARIOS")
    print("=" * 70)

    for scenario in scenario_sets:

        print(f"\nScenario {scenario.scenario_id}")

        for year in scenario:

            print(
                f"Year {year.year:2d}"
                f" | Interest = {year.interest_rate:.4f}"
                f" | Inflation = {year.inflation_rate:.4f}"
            )


if __name__ == "__main__":
    main()