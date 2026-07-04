from dataclasses import dataclass

from pension_alm.assets import Asset


@dataclass
class Equity(Asset):
    """Equity asset with simplified return and dividend assumptions."""

    expected_return: float = 0.06
    dividend_yield: float = 0.02

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.expected_return <= -1:
            raise ValueError("expected_return must be greater than -1")
        if not 0 <= self.dividend_yield <= 1:
            raise ValueError("dividend_yield must be between 0 and 1")

    def cash_flow(self, year: int, interest_rate: float) -> float:
        if year <= 0:
            raise ValueError("year must be positive")

        projected_value = self.projected_market_value(year - 1, interest_rate, 0.0)
        return projected_value * self.dividend_yield

    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        if year < 0:
            raise ValueError("year must be non-negative")

        return self.market_value * (1.0 + self.expected_return) ** year

    def projected_book_value(self, year: int, interest_rate: float) -> float:
        if year < 0:
            raise ValueError("year must be non-negative")

        return self.book_value

from dataclasses import dataclass

from pension_alm.assets import Asset


@dataclass
class RealEstate(Asset):
    """Real estate asset with rental income and inflation-linked growth."""

    rental_yield: float = 0.03
    appreciation_rate: float = 0.02

    def __post_init__(self) -> None:
        super().__post_init__()

        if not 0 <= self.rental_yield <= 1:
            raise ValueError("rental_yield must be between 0 and 1")
        if self.appreciation_rate <= -1:
            raise ValueError("appreciation_rate must be greater than -1")

    def cash_flow(self, year: int, interest_rate: float) -> float:
        if year <= 0:
            raise ValueError("year must be positive")

        projected_value = self.projected_market_value(year - 1, interest_rate, 0.0)
        return projected_value * self.rental_yield

    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        if year < 0:
            raise ValueError("year must be non-negative")

        effective_growth = self.appreciation_rate + inflation_rate
        return self.market_value * (1.0 + effective_growth) ** year

    def projected_book_value(self, year: int, interest_rate: float) -> float:
        if year < 0:
            raise ValueError("year must be non-negative")

        return self.book_value
@dataclass
class InfrastructureAsset(Asset):
    """Infrastructure asset modeled as 50% bond-like and 50% equity-like exposure."""

    bond_yield: float = 0.03
    equity_return: float = 0.06
    equity_dividend_yield: float = 0.02

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.bond_yield <= -1:
            raise ValueError("bond_yield must be greater than -1")
        if self.equity_return <= -1:
            raise ValueError("equity_return must be greater than -1")
        if not 0 <= self.equity_dividend_yield <= 1:
            raise ValueError("equity_dividend_yield must be between 0 and 1")

    def cash_flow(self, year: int, interest_rate: float) -> float:
        """Return infrastructure cash flow as 50% bond income + 50% equity dividend."""
        if year <= 0:
            raise ValueError("year must be positive")

        bond_part = 0.5 * self.market_value * self.bond_yield

        equity_base = 0.5 * self.market_value
        equity_value = equity_base * (1.0 + self.equity_return) ** (year - 1)
        equity_part = equity_value * self.equity_dividend_yield

        return bond_part + equity_part

    def projected_market_value(
            self,
            year: int,
            interest_rate: float,
            inflation_rate: float,
    ) -> float:
        """Project infrastructure market value as 50% bond-like + 50% equity-like."""
        if year < 0:
            raise ValueError("year must be non-negative")

        bond_part = 0.5 * self.market_value
        equity_part = 0.5 * self.market_value * (1.0 + self.equity_return) ** year

        return bond_part + equity_part

    def projected_book_value(self, year: int, interest_rate: float) -> float:
        """Project book value using a simplified stable book-value assumption."""
        if year < 0:
            raise ValueError("year must be non-negative")

        return self.book_value