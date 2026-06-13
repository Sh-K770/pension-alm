from abc import ABC, abstractmethod

class Asset(ABC):
     def __init__(self, id : str, market_value : float, book_value : float):
         self.id = id
         self.market_value = market_value
         self.book_value = book_value

     def get_stelle_reserve(self) -> float:
         return self.market_value-self.book_value

     @abstractmethod
     def get_Cash_Flow(self, year : int, intrest_rate : float) -> float:
         pass

     @abstractmethod
     def get_projected_value(self, year : int, interest_rate : float) -> float:
         pass




