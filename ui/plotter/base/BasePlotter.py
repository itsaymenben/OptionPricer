class BasePlotter:
    def __init__(self,
                 results,
                 volatility):
        self.results = results
        self.volatility = volatility

    def generate_plot(self):
        raise NotImplementedError("Method not implemented yet.")

    def explain(self, type: str):
        raise NotImplementedError("Method not implemented yet.")
