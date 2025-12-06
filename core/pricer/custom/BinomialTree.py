import numpy as np
from core.pricer.base.BasePricer import BasePricer

class BinomialTreePricer(BasePricer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.percentage_increase, self.percentage_decrease = (np.exp(self.volatility * np.sqrt(self.timestep)),
                                                              np.exp(-self.volatility * np.sqrt(self.timestep)))
        self.risk_free_adjustment = self._compute_risk_free_adjustment()
        self.increase_probability = ((self.risk_free_adjustment - self.percentage_decrease) 
                                     / (self.percentage_increase - self.percentage_decrease))

    def run(self):
        self.asset_prices = self._compute_asset_prices()
        self.option_prices = self._compute_option_prices(self.asset_prices)
        return self.asset_prices, self.option_prices

    def _compute_risk_free_adjustment(self):
        if self.asset_type in ["Stock", "Index"]:
            return np.exp((self.risk_free_rate - self.dividend_yield) * self.timestep)
        if self.asset_type == "Currency":
            return np.exp((self.risk_free_rate - self.foreign_risk_free_rate) * self.timestep)
        return 1

    def _compute_asset_prices(self):
        asset_prices = [[self.start_price]]
        for i in range(self.n_steps):
            current_step = []
            for i, price in enumerate(asset_prices[-1]):
                if i == 0:
                    current_step.append(round(price * self.percentage_increase, 4))
                    current_step.append(round(price * self.percentage_decrease, 4))
                else:
                    current_step.append(round(price * self.percentage_decrease, 4))
            asset_prices.append(current_step)
        return asset_prices

    def _compute_option_prices(self, asset_prices):
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
                                                                             option_prices[-1][j + 1])
                    if self.european_option:
                        f_payoff = f_expected
                    else:
                        f_payoff = max(call_option_coeff * (price - self.strike_price), 0)
                    f = max(f_expected, f_payoff)
                    current_option_prices.append(round(f, 4))
            option_prices.append(current_option_prices)
        return option_prices[::-1]          # Reverse the array to match the asset_prices arrays

    def _compute_discounted_price_expectation(self, previous_upper_price, previous_lower_price):
        p = self.increase_probability       # Risk-neutral probability
        r = self.risk_free_rate             # Interest rate
        dt = self.timestep                  # Timestep
        f_up = previous_upper_price
        f_down = previous_lower_price
        discounted_expectation = np.exp(-r * dt) * (p * f_up + (1 - p) * f_down)
        return discounted_expectation
