import numpy as np
from core.pricer.base.BasePricer import BasePricer
from typing import List, Tuple

class TrinomialTreePricer(BasePricer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.percentage_increase, self.percentage_decrease = (np.exp(self.volatility * np.sqrt(3 * self.timestep)),
                                                              np.exp(-self.volatility * np.sqrt(3 * self.timestep)))
        self.asset_yield = self._compute_asset_yield()
        self.increase_probability = np.sqrt(self.timestep / (12 * self.volatility ** 2)) * (self.asset_yield - self.volatility ** 2 / 2) + 1 / 6
        self.decrease_probability = - np.sqrt(self.timestep / (12 * self.volatility ** 2)) * (self.asset_yield - self.volatility ** 2 / 2) + 1 / 6
        self.sideways_probability = 2 / 3
        

    def run(self) -> Tuple[List[List[float]], List[float]]:
        self.asset_prices = self._compute_asset_prices()
        self.option_prices = self._compute_option_prices(self.asset_prices)
        return self.asset_prices, self.option_prices

    def compute_implied_volatility(self, option_price: float) -> None:
        super().compute_implied_volatility(option_price)

    def _compute_asset_yield(self) -> float: # type: ignore
        if self.asset_type in ["Stock", "Index"]:
            return self.dividend_yield
        if self.asset_type == "Currency":
            return self.foreign_risk_free_rate
        if self.asset_type == "Future":
            return self.risk_free_rate

    def _compute_asset_prices(self) -> List[List[float]]:
        asset_prices = [[self.start_price]]
        for i in range(self.n_steps):
            current_step = []
            for i, price in enumerate(asset_prices[-1]):
                if i == 0:
                    current_step.append(round(price * self.percentage_increase, 4))
                    current_step.append(round(price, 4))
                    current_step.append(round(price * self.percentage_decrease, 4))
                else:
                    current_step.append(round(price * self.percentage_decrease, 4))
            asset_prices.append(current_step)
        return asset_prices

    def _compute_option_prices(self, asset_prices: List[List[float]]) -> List[float]:
        option_prices = []
        reverse_asset_prices = asset_prices[::-1]
        call_option_coeff = 1 if self.call_option else -1
        for i, step in enumerate(reverse_asset_prices):
            current_option_prices = []
            if i == 0:
                for price in step:
                    f = max(call_option_coeff * (price - self.strike_price), 0)
                    current_option_prices.append(round(f, 4))
            else:
                for j, price in enumerate(step):
                    f_expected = self._compute_discounted_price_expectation(option_prices[-1][j],
                                                                             option_prices[-1][j + 1],
                                                                             option_prices[-1][j + 2])
                    if self.european_option:
                        f_payoff = f_expected
                    else:
                        f_payoff = max(call_option_coeff * (price - self.strike_price), 0)
                    f = max(f_expected, f_payoff)
                    current_option_prices.append(round(f, 4))
            option_prices.append(current_option_prices)
        return option_prices[::-1]          # Reverse the array to match the asset_prices arrays

    def _compute_discounted_price_expectation(self,
                                              previous_upper_price: float,
                                              previous_mid_price: float,
                                              previous_lower_price: float) -> float:
        p_up = self.increase_probability
        p_mid = self.sideways_probability
        p_down = self.decrease_probability
        r = self.risk_free_rate             # Interest rate
        dt = self.timestep                  # Timestep
        f_up = previous_upper_price
        f_mid = previous_mid_price
        f_down = previous_lower_price
        discounted_expectation = np.exp(-r * dt) * (p_up * f_up + p_mid * f_mid + p_down * f_down)
        return discounted_expectation
