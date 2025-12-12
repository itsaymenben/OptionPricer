from core.config.configFile import configData
from core.pricer.custom.BinomialTree import BinomialTreePricer
from core.pricer.custom.BlackScholesMerton import BlackScholesMertonPricer

class Pricer:
    def __init__(self,
                 method: str,
                 *args,
                 **kwargs):
        if not isinstance(method, str):
            raise TypeError(f"'method' argument should be of {str} type.")
        if not method in configData["methods"]:
            raise KeyError(f"'method' should be in {configData["methods"]}")
        if method == "BinomialTree":
            self.pricer = BinomialTreePricer(*args, **kwargs)
        elif method == "BlackScholesMerton":
            self.pricer = BlackScholesMertonPricer(*args, **kwargs)

    def run(self):
        return self.pricer.run()

    def compute_implied_volatility(self, option_price):
        return self.pricer.compute_implied_volatility(option_price)
