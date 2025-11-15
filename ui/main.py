import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pages = {
    "Home": [
        st.Page("pages/home/home.py", title="Home", icon=":material/home:"),
    ],
    "Pricing": [
        st.Page(
            "pages/price/pricer.py",
            title="Option Pricer",
            url_path="option_pricer",
            icon=":material/analytics:"
        ),
    ],
}

pg = st.navigation(pages)
pg.run()
