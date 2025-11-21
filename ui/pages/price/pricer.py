import streamlit as st
import plotly.graph_objects as go
from core.pricer.custom.Pricer import Pricer
from core.config.configFile import configData
from ui.plotter.custom.Plotter import Plotter 
from ui.utils.custom_widgets import slider_with_number_input

st.title("Option Pricer")
st.set_page_config(layout="wide")


if "params" not in st.session_state:
    st.session_state.params = {}

def set_params():
    with st.sidebar:
        st.session_state.params["method"] = st.selectbox("Pricing Method", configData["methods"])
        if st.session_state.params["method"] == "BinomialTree":
            st.session_state.params["asset_type"] = st.selectbox("Asset Category", configData["assettypes"])
        st.session_state.params["start_price"] = st.number_input("Current Asset Price", min_value=0.0, value=100.0)
        st.session_state.params["strike_price"] = st.number_input("Strike Price", min_value=0.0, value=100.0)
        st.session_state.params["time_to_maturity"] = st.number_input("Time to Maturity (Years)", min_value=0.0, value=1.0)
        if st.session_state.params["method"] == "BinomialTree":
            st.session_state.params["n_steps"] = slider_with_number_input("Number of Steps", key="n_steps", min_value=0, max_value=30, value=2, step=1)
            # st.session_state.params["n_steps"] = st.number_input("Number of Steps", min_value=0, value=1)
        st.session_state.params["volatility"] = slider_with_number_input("Volatility (%)", key="volatility", min_value=0.0, max_value=100.0, value=10.0, step=1.0) / 100
        st.session_state.params["risk_free_rate"] = slider_with_number_input("Risk Free Rate (%)", key="risk_free_rate", min_value=0.0, max_value=100.0, value=5.0, step=1.0) / 100
        if st.session_state.params["method"] == "BinomialTree":
            if st.session_state.params["asset_type"] == "Currency":
                st.session_state.params["foreign_risk_free_rate"] = slider_with_number_input("Foreign Risk Free Rate (%)", key="foreign_risk_free_rate", min_value=0.0, max_value=100.0, value=0.0, step=1.0) / 100
            else:
                st.session_state.params["dividend_yield"] = slider_with_number_input("Dividend Yield (%)", key="dividend_yield", min_value=0.0, max_value=100.0, value=0.0, step=1.0) / 100
        st.session_state.params["european_option"] = st.radio(
                                                "Option Exercise Style",
                                                ["European", "American"],
                                            ) == "European"
        st.session_state.params["call_option"] = st.radio(
                                                "Option Payoff Type",
                                                ["Call", "Put"],
                                            ) == "Call"
set_params()
pricer = Pricer(**st.session_state.params)
results = pricer.run()
if st.session_state.params["method"] == "BinomialTree":
    asset_prices, option_prices = results
    plotter = Plotter(method=st.session_state.params["method"],
                      n_steps=st.session_state.params["n_steps"],
                      results=results)
    fig = plotter.generate_plot()
    st.plotly_chart(fig, width="stretch")

elif st.session_state.params["method"] == "BlackScholesMerton":
    price = results
    st.write(f"The price given the Black-Scholes-Method Model is {round(price, 4)}")
