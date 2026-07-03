import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.vasicek import VasicekModel


def main() -> None:
    model = VasicekModel(
        kappa=0.25,
        theta=0.035,
        sigma=0.01,
        r0=0.03,
    )

    rates = model.simulate_paths(
        years=30,
        n_paths=1_000,
        steps_per_year=1,
        seed=42,
    )

    final_rates = rates[:, -1]

    print("Vasicek Monte Carlo simulation")
    print(f"Number of paths: {rates.shape[0]}")
    print(f"Horizon: {rates.shape[1] - 1} years")
    print(f"Mean final rate: {np.mean(final_rates):.4%}")
    print(f"5th percentile: {np.percentile(final_rates, 5):.4%}")
    print(f"95th percentile: {np.percentile(final_rates, 95):.4%}")


if __name__ == "__main__":
    main()