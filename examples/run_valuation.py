import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from pension_alm.valuation import ValuationEngine


def main() -> None:
    bond_cash_flows = {
        1: 5.0,
        2: 5.0,
        3: 105.0,
    }

    pension_cash_flows = {
        1: -120_000.0,
        2: -125_000.0,
        3: -130_000.0,
    }

    asset_engine = ValuationEngine(discount_rate=0.03)
    liability_engine = ValuationEngine(discount_rate=0.025)

    bond_value = asset_engine.value(bond_cash_flows)
    pension_value = liability_engine.value(pension_cash_flows)

    print("Valuation Engine Example")
    print(f"Bond present value: {bond_value:,.2f}")
    print(f"Pension obligation present value: {pension_value:,.2f}")


if __name__ == "__main__":
    main()
