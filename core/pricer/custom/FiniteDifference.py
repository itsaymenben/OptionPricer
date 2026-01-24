import numpy as np
from core.pricer.base.BasePricer import BasePricer
from numpy.typing import NDArray

class FiniteDifference(BasePricer):
    def __init__(self,
                 finite_difference_method: str,
                 nb_time_steps: int,
                 nb_space_steps: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.finite_difference_method = finite_difference_method
        self.nb_time_steps = nb_time_steps
        self.nb_space_steps = nb_space_steps
        self.time_step = self.time_to_maturity / self.nb_time_steps
        self.max_price = 2 * self.start_price
        self.space_step = self.max_price / self.nb_space_steps
        self.asset_yield = self._compute_asset_yield()

    def run(self) -> NDArray:
        K = self.strike_price
        r = self.risk_free_rate
        q = self.asset_yield
        sigma = self.volatility
        dt = self.time_step
        dS = self.space_step
        N = self.nb_time_steps
        M = self.nb_space_steps
        call_option_coeff = 1 if self.call_option else -1
        if self.finite_difference_method == "EXPLICIT":
            price_array = np.zeros((M + 1, N + 1))
            price_array[:, N] = np.maximum(call_option_coeff * (np.arange(M + 1) * dS - K), 0)
            a = 1 / (1 + r * dt) * (- 1 / 2 * (r - q) * np.arange(1, M + 1) * dt + 1 / 2 * sigma ** 2 * np.arange(1, M + 1) ** 2 * dt)
            b = 1 / (1 + r * dt) * (1 - sigma ** 2 * np.arange(M + 1) ** 2 * dt)
            c = 1 / (1 + r * dt) * (1 / 2 * (r - q) * np.arange(M) * dt + 1 / 2 * sigma ** 2 * np.arange(M) ** 2 * dt)
            transition_matrix = np.diag(a, -1) + np.diag(b) + np.diag(c, 1)
            early_exercise = call_option_coeff * (np.arange(M + 1) * dS - K)
            for step in range(N - 1, -1, -1):
                price_array[:, step] = transition_matrix @ price_array[:, step + 1]
                if not self.european_option:
                    price_array[:, step] = np.maximum(early_exercise, price_array[:, step])
                price_array[0, step] = max(call_option_coeff * (0 * dS - K), 0)
                price_array[M, step] = max(call_option_coeff * (M * dS - K), 0)
            return price_array
        raise ValueError("Only 'EXPLICIT' finite difference method is implemented.")

    def _compute_asset_yield(self) -> float: # type: ignore
        if self.asset_type in ["Stock", "Index"]:
            return self.dividend_yield
        if self.asset_type == "Currency":
            return self.foreign_risk_free_rate
        if self.asset_type == "Future":
            return self.risk_free_rate