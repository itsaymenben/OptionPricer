from core.config.configFile import configData
from core.pricer.custom.BinomialTree import BinomialTreePricer
from core.pricer.custom.BlackScholesMerton import BlackScholesMertonPricer

class Pricer:
    def __init__(self,
                 method: str,
                 **kwargs):
        if not isinstance(method, str):
            raise TypeError(f"'method' argument should be of {str} type.")
        if not method in configData["Methods"]:
            raise KeyError(f"'method' should be in {configData["Methods"]}")
        if method == "BinomialTree":
            self.pricer = BinomialTreePricer(**kwargs)
        elif method == "BlackScholesMerton":
            self.pricer = BlackScholesMertonPricer(**kwargs)

    def run(self):
        return self.pricer.run()
