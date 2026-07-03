from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class VasicekModel:
    """Vasicek short-rate model.

    dr_t = kappa * (theta - r_t) dt + sigma dW_t

    Parameters
    ----------
    kappa:
        Speed of mean reversion.
    theta:
        Long-term mean interest rate.
    sigma:
        Volatility of the short rate.
    r0:
        Initial short rate.
    """

    kappa: float
    theta: float
    sigma: float
    r0: float

    def simulate_path(
            self,
            years: int,
            steps_per_year: int = 1,
            seed: int | None = None,
    ) -> np.ndarray:
        """Simulate one short-rate path."""
        return self.simulate_paths(
            years=years,
            n_paths=1,
            steps_per_year=steps_per_year,
            seed=seed,
        )[0]

    def simulate_paths(
            self,
            years: int,
            n_paths: int,
            steps_per_year: int = 1,
            seed: int | None = None,
    ) -> np.ndarray:
        """Simulate multiple short-rate paths using Euler discretization."""
        if years <= 0:
            raise ValueError("years must be positive")
        if n_paths <= 0:
            raise ValueError("n_paths must be positive")
        if steps_per_year <= 0:
            raise ValueError("steps_per_year must be positive")

        n_steps = years * steps_per_year
        dt = 1.0 / steps_per_year

        rng = np.random.default_rng(seed)
        rates = np.empty((n_paths, n_steps + 1))
        rates[:, 0] = self.r0

        shocks = rng.normal(
            loc=0.0,
            scale=np.sqrt(dt),
            size=(n_paths, n_steps),
        )

        for t in range(n_steps):
            rates[:, t + 1] = (
                    rates[:, t]
                    + self.kappa * (self.theta - rates[:, t]) * dt
                    + self.sigma * shocks[:, t]
            )

        return rates