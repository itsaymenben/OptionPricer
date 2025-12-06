import numpy as np
from scipy.stats import norm
from core.pricer.base.BasePricer import BasePricer

class BlackScholesMertonPricer(BasePricer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_yield = self._compute_asset_yield()

    def run(self):
        d1 = ((np.log(self.start_price / self.strike_price) 
              + (self.risk_free_rate - self.asset_yield + self.volatility ** 2 / 2) * self.time_to_maturity) 
              / (self.volatility * np.sqrt(self.time_to_maturity)))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        if self.call_option:
            return self._compute_call_price(d1, d2)
        return self._compute_put_price(d1, d2)

    def _compute_asset_yield(self):
        if self.asset_type in ["Stock", "Index"]:
            return self.dividend_yield
        if self.asset_type == "Currency":
            return self.foreign_risk_free_rate
        return 0

    def _compute_call_price(self, d1, d2):
        return self.start_price * np.exp(- self.asset_yield * self.time_to_maturity) * norm.cdf(d1) - self.strike_price * np.exp(- self.risk_free_rate * self.time_to_maturity) * norm.cdf(d2)

    def _compute_put_price(self, d1, d2):
        return self.strike_price * np.exp(- self.risk_free_rate * self.time_to_maturity) * norm.cdf(- d2) - self.start_price * np.exp(- self.asset_yield * self.time_to_maturity) * norm.cdf(- d1)
