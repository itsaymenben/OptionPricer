from core.pricer.base.BasePricer import BasePricer

class BlackScholesMertonPricer(BasePricer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
