import public

from asset import Asset


class Infrustruktur(Asset):
    def __init__(self, id: str, market_value: float, book_value: float, base_yield: float, inflation_rate: float,
                 bond_weight: float, equity_weight: float):
        super().__init__(id, market_value, book_value)
        self.base_yield = base_yield
        self.inflation_rate = inflation_rate
        self.bond_weight = bond_weight
        self.equity_weight = equity_weight

    def get_Cash_Flow(self, year: int, interest_rate: float) -> float:
        fixed_cf = self.market_value * self.base_yield * self.bond_weight
        index_cf = self.market_value * self.base_yield * (1 + self.inflation_rate) ** year

        return fixed_cf + index_cf

    def get_projected_value(self, year: int, interest_rate: float) -> float:
        blended_rate = self.bond_weight * self.inflation_rate + self.equity_weight * (
                self.inflation_rate + self.inflation_rate)

        return self.market_value * (1 + blended_rate) ** year

    def get_base_value(self) -> float:
        return self.base_yield

    def get_inflation_rate(self) -> float:
        return self.inflation_rate
