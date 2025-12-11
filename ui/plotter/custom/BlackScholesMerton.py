import streamlit as st
from ui.plotter.base.BasePlotter import BasePlotter

class BlackScholesMertonPlotter(BasePlotter):
    def __init__(self, results):
        super().__init__(results)
        self.price = results

    def explain(self):
        st.write(f"The Black-Scholes-Method Model gives the price:\n")
        _, _, col3, _, _ = st.columns(5)
        with col3:
            if st.session_state.params["call_option"]: 
                    st.success(f"**CALL Value**\n\n{round(self.price, 4)}€")
            else:
                st.error(f"**PUT Value**\n\n{round(self.price, 4)}€")
        st.write(f"Using the formula:")
        if st.session_state.params["call_option"]:
            st.latex(r"""
                    c = S_0 N(d_1) - K e^{- r T} N(d_2)
                    """)
        else:
            st.latex(r"""
                    p = K e^{- r T} N(- d_2) - S_0 N(- d_1)
                    """)
        st.latex(r"""
                d_1 = \frac{\ln{\frac{S_0}{K}} + (r + \sigma^2)T}{\sigma\sqrt{T}}
                """)
        st.latex(r"""
                d_2 = \frac{\ln{\frac{S_0}{K}} + (r - \sigma^2)T}{\sigma\sqrt{T}} = d_1 - \sigma\sqrt{T}
                """)

    def generate_plot(self):
        return super().generate_plot()
