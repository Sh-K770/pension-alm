from abc import ABC, abstractmethod


class InterestRateModel(ABC):

    @abstractmethod
    def next_rate(
            self,
            current_rate: float,
    ) -> float:
        pass