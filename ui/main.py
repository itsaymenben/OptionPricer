import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pages = {
    "Home": [
        st.Page("pages/home/home.py", title="Home", icon=":material/home:"),
    ],
    "Pricing Models": [
        st.Page(
            "pages/price/Pricer.py",
            title="Option Pricer",
            url_path="option_pricer",
            icon=":material/analytics:"
        ),
        st.Page(
            "pages/price/ImpliedVol.py",
            title="Implied Volatility",
            url_path="implied_volatility",
            icon=":material/analytics:"
        ),
    ],
}

pg = st.navigation(pages)
pg.run()
