import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.mortality import GompertzMortality


def main() -> None:
    mortality = GompertzMortality()

    current_age = 67

    print("Mortality Example")
    print(f"Mortality rate at age {current_age}: {mortality.mortality_rate(current_age):.4%}")
    ages = [40, 50, 60, 70, 80, 90]

    for age in ages:
     print(age, mortality.mortality_rate(age))

    for years in [1, 5, 10, 20]:
        survival = mortality.survival_probability(
            current_age=current_age,
            years=years,
        )
        print(f"Survival probability over {years} years: {survival:.4%}")



if __name__ == "__main__":
    main()