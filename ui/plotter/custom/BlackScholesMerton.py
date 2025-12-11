import streamlit as st
from ui.plotter.base.BasePlotter import BasePlotter

class BlackScholesMertonPlotter(BasePlotter):
    def __init__(self, asset_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.price = self.results
        self.asset_type = asset_type

    def explain(self):
        st.write(f"The Black-Scholes-Method Model gives the price:\n")
        _, _, col3, _, _ = st.columns(5)
        with col3:
            if st.session_state.params["call_option"]: 
                    st.success(f"**CALL Value**\n\n{round(self.price, 4)}€")
            else:
                st.error(f"**PUT Value**\n\n{round(self.price, 4)}€")
        st.write(f"Using the formula:")
        if self.asset_type in ["Stock", "Index"]:
            asset_yield = "q"
        elif self.asset_type == "Currency":
            asset_yield = "r_f"
        else:
            asset_yield = "r"
        if st.session_state.params["call_option"]:
            st.latex(r"""
                    c = S_0 e^{- %s T} N(d_1) - K e^{- r T} N(d_2)
                    """%(asset_yield))
        else:
            st.latex(r"""
                    p = K e^{- r T} N(- d_2) - S_0 e^{- %s T} N(- d_1)
                    """%(asset_yield))
        st.latex(r"""
                d_1 = \frac{\ln{\frac{S_0}{K}} + (r - %s + \sigma^2)T}{\sigma\sqrt{T}}
                """%(asset_yield))
        st.latex(r"""
                d_2 = \frac{\ln{\frac{S_0}{K}} + (r - %s - \sigma^2)T}{\sigma\sqrt{T}} = d_1 - \sigma\sqrt{T}
                """%(asset_yield))

    def generate_plot(self):
        return super().generate_plot()
