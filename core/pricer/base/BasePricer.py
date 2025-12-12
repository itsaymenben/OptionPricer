from core.config.configFile import configData

class BasePricer:
    def __init__(self,
                 start_price: float,                    # S0
                 time_to_maturity: float,               # T
                 volatility: float,                     # sigma
                 risk_free_rate: float,                 # r
                 asset_type: str,
                 european_option: bool,
                 call_option: bool,
                 strike_price: float,                   # K
                 n_steps: int = 1,                      # n
                 dividend_yield: float = 0,             # q
                 foreign_risk_free_rate: float = 0,     # rf
                 *args,
                 **kwargs,
                 ):

        self.start_price = start_price
        self.time_to_maturity = time_to_maturity
        self.n_steps = n_steps
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
        self.asset_type = asset_type
        self.european_option = european_option
        self.call_option = call_option
        self.strike_price = strike_price
        self.dividend_yield = dividend_yield
        self.foreign_risk_free_rate = foreign_risk_free_rate

        # Type and Value validation
        if not (isinstance(self.start_price, float) or isinstance(self.start_price, int)) or self.start_price <= 0:
            raise ValueError(f"'start_price' must be a posititve {float} or {int}.")

        for name in ["time_to_maturity", "volatility"]:
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"{name} must be a positive {float}.")

        if not isinstance(self.n_steps, int) or self.n_steps < 1:
            raise ValueError(f"'n_steps' must be an {int} superior to 1.")

        if not isinstance(self.risk_free_rate, (int, float)):
            raise TypeError(f"'risk_free_rate' must be of type {float}.")

        if not isinstance(self.dividend_yield, (int, float)):
            raise TypeError(f"'risk_free_rate' must be of type {float}.")

        if not isinstance(self.foreign_risk_free_rate, (int, float)):
            raise TypeError(f"'risk_free_rate' must be of type {float}.")

        if not isinstance(self.asset_type, str):
            raise TypeError(f"'asset_type' must be of type {str}.")
        if self.asset_type not in configData["assettypes"]:
            raise KeyError(f"'asset_type' used should be in {configData["assettypes"]}")

        if not isinstance(self.european_option, bool):
            raise TypeError(f"'european_option' must be of type {bool}.")

        if not isinstance(self.call_option, bool):
            raise TypeError(f"'call_option' must be of type {bool}.")

        if not (isinstance(self.strike_price, float) or isinstance(self.strike_price, int)) or self.strike_price <= 0:
            raise ValueError(f"'strike_price' must be a posititve {float} or {int}.")

        self.timestep = self.time_to_maturity / self.n_steps

    def run(self):
        raise NotImplementedError("Method not implemented yet.")

    def compute_implied_volatility(self, option_price):
        raise NotImplementedError("Method not implemented yet.")
