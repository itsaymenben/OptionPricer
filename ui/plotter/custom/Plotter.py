from core.config.configFile import configData
from ui.plotter.custom.BinomialTree import BinomialTreePlotter
from ui.plotter.custom.BlackScholesMerton import BlackScholesMertonPlotter

class Plotter:
    def __init__(self,
                 method: str,
                 *args,
                 **kwargs):
        if not isinstance(method, str):
            raise TypeError(f"'method' argument should be of {str} type.")
        if not method in configData["methods"]:
            raise KeyError(f"'method' should be in {configData["methods"]}")
        if method == "BinomialTree":
            self.plotter = BinomialTreePlotter(*args, **kwargs)
        elif method == "BlackScholesMerton":
            self.plotter = BlackScholesMertonPlotter(*args, **kwargs)

    def generate_plot(self):
        return self.plotter.generate_plot()

    def explain(self):
        return self.plotter.explain()
