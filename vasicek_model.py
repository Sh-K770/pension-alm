import random


class VesicekModel():

    def __init__(self, kappa: float, theta: float, sigma: float, r0: float):
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.r0 = r0

    def simulation_path(self, years: int) -> list:
        rates = [0.0] * (years + 1)
        rates[0] = self.r0

        for t in range(1, years + 1):
            dw = random.gauss(0, 1)
            rates[t] = rates[t - 1] + self.kappa * (self.theta - rates[t - 1]) + self.sigma * dw
        return rates

    def simulation_multiple_paths(self, years: int, numPaths: int) -> list:
        paths = []
        for i in range(0, numPaths):
            paths.append(self.simulation_path(years))
        return paths
