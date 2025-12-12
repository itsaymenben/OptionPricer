import numpy as np
from scipy.stats import norm
from core.pricer.base.BasePricer import BasePricer

class BlackScholesMertonPricer(BasePricer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_yield = self._compute_asset_yield()

    def run(self):
        return self._compute_price(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity,
                                   self.call_option)

    def compute_implied_volatility(self, option_price, tol=1e-4, max_iter=1000):
        upper_sigma = 3
        lower_sigma = 0.001
        computed_option_price = - np.inf
        iter_count = 0
        while abs(option_price - computed_option_price) > tol and iter_count < max_iter:
            sigma = (upper_sigma + lower_sigma) / 2
            computed_option_price = self._compute_price(self.start_price,
                                                        self.strike_price,
                                                        self.risk_free_rate,
                                                        self.asset_yield,
                                                        sigma,
                                                        self.time_to_maturity,
                                                        self.call_option)
            if computed_option_price <= option_price:
                lower_sigma = sigma
            else:
                upper_sigma = sigma
            iter_count += 1
        self.volatility = sigma
        return round(sigma * 100, 4)

    def _compute_price(self,
                       start_price,
                       strike_price,
                       risk_free_rate,
                       asset_yield,
                       volatility,
                       time_to_maturity,
                       call_option):
        d1 = ((np.log(start_price / strike_price) 
              + (risk_free_rate - asset_yield + volatility ** 2 / 2) * time_to_maturity) 
              / (volatility * np.sqrt(time_to_maturity)))
        d2 = d1 - volatility * np.sqrt(time_to_maturity)
        if call_option:
            return self._compute_call_price(d1, d2)
        return self._compute_put_price(d1, d2)

    def _compute_asset_yield(self):
        if self.asset_type in ["Stock", "Index"]:
            return self.dividend_yield
        if self.asset_type == "Currency":
            return self.foreign_risk_free_rate
        return self.risk_free_rate  # asset_type = 'Future'

    def _compute_call_price(self, d1, d2):
        return self.start_price * np.exp(- self.asset_yield * self.time_to_maturity) * norm.cdf(d1) - self.strike_price * np.exp(- self.risk_free_rate * self.time_to_maturity) * norm.cdf(d2)

    def _compute_put_price(self, d1, d2):
        return self.strike_price * np.exp(- self.risk_free_rate * self.time_to_maturity) * norm.cdf(- d2) - self.start_price * np.exp(- self.asset_yield * self.time_to_maturity) * norm.cdf(- d1)
