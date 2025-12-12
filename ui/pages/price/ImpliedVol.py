import streamlit as st
import plotly.graph_objects as go
from core.pricer.custom.Pricer import Pricer
from core.config.configFile import configData
from ui.plotter.custom.Plotter import Plotter 
from ui.utils.custom_widgets import slider_with_number_input

st.title("Implied Volatility")
st.set_page_config(layout="wide")


if "params" not in st.session_state:
    st.session_state.params = {}

time_to_maturity_granularity = {"Trading Days": 252,
                                "Days": 365,
                                "Weeks": 52,
                                "Months": 12,
                                "Years": 1}
def set_params():
    with st.sidebar:
        st.session_state.params["method"] = "BlackScholesMerton"
        st.session_state.params["asset_type"] = st.selectbox("Asset Category", configData["assettypes"])
        st.session_state.params["start_price"] = st.number_input("Current Asset Price", min_value=0.0, value=100.0)
        st.session_state.params["strike_price"] = st.number_input("Strike Price", min_value=0.0, value=100.0)
        st.session_state.params["option_price"] = st.number_input("Current Option Price", min_value=0.0, value=1.0)
        st.session_state.params["volatility"] = 10.0 / 100
        time_to_maturity_granularity_key = st.selectbox("Time to Maturity Granularity", time_to_maturity_granularity.keys())
        st.session_state.params["time_to_maturity"] = st.number_input("Time to Maturity", min_value=0.0, value=1.0, step=0.5) / time_to_maturity_granularity[time_to_maturity_granularity_key]
        st.session_state.params["risk_free_rate"] = slider_with_number_input("Risk Free Rate (%)", key="risk_free_rate", min_value=0.0, max_value=100.0, value=5.0, step=1.0) / 100
        if st.session_state.params["asset_type"] == "Currency":
            st.session_state.params["foreign_risk_free_rate"] = slider_with_number_input("Foreign Risk Free Rate (%)", key="foreign_risk_free_rate", min_value=0.0, max_value=100.0, value=0.0, step=1.0) / 100
        elif st.session_state.params["asset_type"] in ["Stock", "Index"]:
            st.session_state.params["dividend_yield"] = slider_with_number_input("Dividend Yield (%)", key="dividend_yield", min_value=0.0, max_value=100.0, value=0.0, step=1.0) / 100
        st.session_state.params["european_option"] = True
        st.session_state.params["call_option"] = st.radio(
                                                "Option Payoff Type",
                                                ["Call", "Put"],
                                            ) == "Call"
set_params()
pricer = Pricer(**st.session_state.params)
implied_vol = pricer.compute_implied_volatility(st.session_state.params["option_price"])
results = pricer.run()
plotter = Plotter(method=st.session_state.params["method"],
                    asset_type=st.session_state.params["asset_type"],
                    volatility=implied_vol,
                    results=results)
plotter.explain(type="ImpliedVol")
