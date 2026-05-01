import streamlit as st
import pandas as pd

from pages.utils.data_loader import load_stock_data
from pages.utils.risk_models import calculate_returns, calculate_beta, calculate_capm_return

st.set_page_config(
    page_title="CAPM Return",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: #f8fafc;
}
h1, h2, h3 {
    color: #38bdf8 !important;
}
p, div, label, span {
    color: #e2e8f0 !important;
}
div[data-baseweb="input"] input, div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("CAPM Return")

col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")

with col2:
    market_index = st.selectbox("Market Benchmark", ["S&P 500 (^GSPC)", "NASDAQ (^IXIC)", "DOW JONES (^DJI)"])

index_map = {
    "S&P 500 (^GSPC)": "^GSPC",
    "NASDAQ (^IXIC)": "^IXIC",
    "DOW JONES (^DJI)": "^DJI"
}
index_ticker = index_map[market_index]

stock_data = load_stock_data(ticker, start="2020-01-01")
market_data = load_stock_data(index_ticker, start="2020-01-01")

if stock_data.empty or market_data.empty:
    st.error("Unable to fetch stock or market data.")
    st.stop()

stock_returns = calculate_returns(stock_data["Close"].squeeze())
market_returns = calculate_returns(market_data["Close"].squeeze())

beta = round(calculate_beta(stock_returns, market_returns), 2)
expected_return = round(calculate_capm_return(beta), 2)

result_df = pd.DataFrame({
    "Metric": ["Beta", "Risk Free Rate", "Market Return", "Expected Return"],
    "Value": [beta, "4.2%", "10.8%", f"{expected_return}%"]
})

st.write("### CAPM Return Result")
st.dataframe(result_df, use_container_width=True)

st.info(f"The expected return of {ticker.upper()} based on CAPM is {expected_return}%.")