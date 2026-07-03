import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.discount import DiscountEngine


def main() -> None:
    cash_flows = {
        1: 5.0,
        2: 5.0,
        3: 105.0,
    }

    engine = DiscountEngine(discount_rate=0.03)
    pv = engine.present_value(cash_flows)

    print("Discount Engine Example")
    print(f"Cash flows: {cash_flows}")
    print(f"Discount rate: {engine.discount_rate:.2%}")
    print(f"Present value: {pv:.2f}")


if __name__ == "__main__":
    main()