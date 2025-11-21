class BasePlotter:
    def __init__(self,
                 results):
        self.results = results

    def generate_plot(self):
        raise NotImplementedError("Method not implemented yet.")
