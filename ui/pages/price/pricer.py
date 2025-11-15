import streamlit as st
import plotly.graph_objects as go
from core.pricer.custom.Pricer import Pricer
from core.config.configFile import configData

st.title("Option Pricer")
st.set_page_config(layout="wide")

if "params" not in st.session_state:
    st.session_state.params = {}

def set_params():
    with st.sidebar:
        st.session_state.params["method"] = st.selectbox("Pricing Method", configData["methods"])
        st.session_state.params["asset_type"] = st.selectbox("Asset Category", configData["assettypes"])
        st.session_state.params["start_price"] = st.number_input("Current Asset Price", min_value=0, value=100)
        st.session_state.params["strike_price"] = st.number_input("Strike Price", min_value=0, value=100)
        st.session_state.params["time_to_maturity"] = st.number_input("Time to Maturity (Years)", min_value=0.0, value=1.0)
        st.session_state.params["n_steps"] = st.number_input("Number of Steps", min_value=0, value=1)
        st.session_state.params["volatility"] = st.number_input("Volatility (%)", min_value=0.0, value=10.0, step=1.0) / 100
        st.session_state.params["risk_free_rate"] = st.number_input("Risk Free Rate (%)", min_value=0.0, value=5.0, step=1.0) / 100
        if st.session_state.params["asset_type"] == "Currency":
            st.session_state.params["foreign_risk_free_rate"] = st.number_input("Foreign Risk Free Rate (%)", min_value=0.0, value=0.0, step=1.0) / 100
        else:
            st.session_state.params["dividend_yield"] = st.number_input("Dividend Yield (%)", min_value=0.0, value=0.0, step=1.0) / 100
        st.session_state.params["european_option"] = st.radio(
                                                "Option Exercise Style",
                                                ["European", "American"],
                                            ) is "European"
        st.session_state.params["call_option"] = st.radio(
                                                "Option Payoff Type",
                                                ["Call", "Put"],
                                            ) is "Call"
set_params()
binom_tree = Pricer(**st.session_state.params)
asset_prices, option_prices = binom_tree.run()

# Build binomial tree
asset_prices_nodes = []
option_prices_nodes = []
edges = []

for i in range(st.session_state.params["n_steps"] + 1):
    for j in range(i + 1):
        asset_prices_nodes.append((i, j, asset_prices[i][i - j]))
        option_prices_nodes.append((i, j, option_prices[i][i - j]))
        if i > 0:
            if j > 0:
                edges.append(((i - 1, j - 1), (i, j)))
            if j < i:
                edges.append(((i - 1, j), (i, j)))

# Convert nodes to coordinates
x = [i for (i, j, S) in asset_prices_nodes]
y = [j - i / 2 + 0.15 for (i, j, S) in asset_prices_nodes]
yprime = [j - i / 2 - 0.1 for (i, j, S) in asset_prices_nodes]
text = [f"Step {i}<br>Up {j}<br>S={S:.2f}" for (i, j, S) in asset_prices_nodes]

# Create edges for Plotly
edge_x = []
edge_y = []
for ((i1, j1), (i2, j2)) in edges:
    edge_x += [i1 + 0.2, i2 - 0.2, None]
    edge_y += [j1 - i1 / 2, j2 - i2 / 2, None]

shapes = []

node_width = 0.38   # horizontal size of rectangles
node_height = 0.28  # vertical size of rectangles

for (i, j, S) in asset_prices_nodes:
    x_center = i
    y_center = j - i/2 + 0.15

    shapes.append(dict(
        type="rect",
        x0=x_center - node_width/2,
        x1=x_center + node_width/2,
        y0=y_center - node_height/2,
        y1=y_center + node_height/2,
        line=dict(color="black", width=2),
        fillcolor="white",
        layer="below"
    ))

for (i, j, C) in option_prices_nodes:
    x_center = i
    y_center = j - i/2 - 0.1

    shapes.append(dict(
        type="rect",
        x0=x_center - node_width/2,
        x1=x_center + node_width/2,
        y0=y_center - node_height/2,
        y1=y_center + node_height/2,
        line=dict(color="black", width=2),
        fillcolor="lightgray",
        layer="below"
    ))

# Plot
fig = go.Figure()

# Add edges
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines',
    line=dict(color='lightgray', width=2),
    text=[f"edge" for (i, j) in edges],
    hoverinfo='none'
))

# Asset price values
fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='text',
    text=[f"{S:.2f}" for (_, _, S) in asset_prices_nodes],
    textposition='middle center',
    hovertext=text,
    hoverinfo='text',
    textfont=dict(color="black")
))

# Option prices
fig.add_trace(go.Scatter(
    x=x, y=yprime,
    mode='text',
    text=[f"{S:.2f}" for (_, _, S) in option_prices_nodes],
    textposition='middle center',
    hovertext=text,
    hoverinfo='text',
    textfont=dict(color="black", weight='bold')
))

fig.update_layout(
    title='Binomial Tree for Option Pricing',
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor=None,
    margin=dict(l=0, r=0, t=50, b=0),
    height=max(60 * st.session_state.params["n_steps"], 600),
    width=max(120 * st.session_state.params["n_steps"], 1450),
    shapes=shapes,
)

st.plotly_chart(fig, width="stretch")