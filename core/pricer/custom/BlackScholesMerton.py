import numpy as np
from scipy.stats import norm
from core.pricer.base.BasePricer import BasePricer
from core.utilities.functions import derivative_cdf

class BlackScholesMertonPricer(BasePricer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_yield = self._compute_asset_yield()

    def run(self):
        delta = self._compute_delta(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity,
                                   self.call_option)
        gamma = self._compute_gamma(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity)
        theta = self._compute_theta(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity,
                                   self.call_option)
        vega = self._compute_vega(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity)
        rho = self._compute_rho(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity,
                                   self.call_option)
        price = self._compute_price(self.start_price,
                                   self.strike_price,
                                   self.risk_free_rate,
                                   self.asset_yield,
                                   self.volatility,
                                   self.time_to_maturity,
                                   self.call_option)
        return price, delta, gamma, theta, vega, rho

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

    def _compute_delta(self,
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
        delta_call = np.exp(- asset_yield * time_to_maturity) * norm.cdf(d1)
        delta_put = np.exp(- asset_yield * time_to_maturity) * (norm.cdf(d1) - 1)
        return delta_call if call_option else delta_put

    def _compute_gamma(self,
                       start_price,
                       strike_price,
                       risk_free_rate,
                       asset_yield,
                       volatility,
                       time_to_maturity):
        d1 = ((np.log(start_price / strike_price) 
              + (risk_free_rate - asset_yield + volatility ** 2 / 2) * time_to_maturity) 
              / (volatility * np.sqrt(time_to_maturity)))
        gamma = derivative_cdf(d1) * np.exp(- asset_yield * time_to_maturity) / (start_price * volatility * np.sqrt(time_to_maturity))
        return gamma

    def _compute_theta(self,
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
        theta_call = (- start_price * derivative_cdf(d1) * volatility * np.exp(- asset_yield * time_to_maturity) / (2 * np.sqrt(time_to_maturity))
                      + asset_yield * start_price * norm.cdf(d1) * np.exp(- asset_yield * time_to_maturity)
                      - risk_free_rate * strike_price * np.exp(- risk_free_rate * time_to_maturity) * norm.cdf(d2))
        theta_put = (- start_price * derivative_cdf(d1) * volatility * np.exp(- asset_yield * time_to_maturity) / (2 * np.sqrt(time_to_maturity))
                      - asset_yield * start_price * norm.cdf(- d1) * np.exp(- asset_yield * time_to_maturity)
                      + risk_free_rate * strike_price * np.exp(- risk_free_rate * time_to_maturity) * norm.cdf(- d2))
        return theta_call if call_option else theta_put

    def _compute_vega(self,
                       start_price,
                       strike_price,
                       risk_free_rate,
                       asset_yield,
                       volatility,
                       time_to_maturity):
        d1 = ((np.log(start_price / strike_price) 
              + (risk_free_rate - asset_yield + volatility ** 2 / 2) * time_to_maturity) 
              / (volatility * np.sqrt(time_to_maturity)))
        vega = start_price * np.sqrt(time_to_maturity) * derivative_cdf(d1) * np.exp(- asset_yield * time_to_maturity)
        return vega

    def _compute_rho(self,
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
        rho_call = strike_price * time_to_maturity * np.exp(- risk_free_rate * time_to_maturity) * norm.cdf(d2)
        rho_put = - strike_price * time_to_maturity * np.exp(- risk_free_rate * time_to_maturity) * norm.cdf(- d2)
        return rho_call if call_option else rho_put

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
