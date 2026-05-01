import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pages.utils.data_loader import load_stock_data
from pages.utils.plotly_figure import plotly_table
from pages.utils.risk_models import (
    calculate_returns,
    calculate_beta,
    calculate_capm_return,
    annualized_return,
    annualized_volatility,
    rolling_beta
)

st.set_page_config(
    page_title="CAPM Beta",
    page_icon="⚡",
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
    font-weight: 700;
}
p, div, label, span {
    color: #e2e8f0 !important;
}
div[data-baseweb="input"] input {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}
[data-testid="stInfo"] {
    background-color: rgba(56, 189, 248, 0.12) !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 12px !important;
}
[data-testid="stWarning"] {
    background-color: rgba(250, 204, 21, 0.12) !important;
    border: 1px solid #facc15 !important;
    border-radius: 12px !important;
}
[data-testid="stError"] {
    background-color: rgba(248, 113, 113, 0.12) !important;
    border: 1px solid #f87171 !important;
    border-radius: 12px !important;
}
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #38bdf8, transparent);
    margin-top: 10px;
    margin-bottom: 10px;
}
[data-testid="stSpinner"] {
    color: #38bdf8 !important;
}
.katex {
    color: #f8fafc !important;
}
</style>
""", unsafe_allow_html=True)

st.title("CAPM Beta ⚡")
st.write("Calculates Beta and Expected Return for Individual Stocks. Beta measures a stock's volatility relative to the market.")

st.markdown("---")

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

st.markdown("---")
st.markdown("### 💡 Beta Formula")
st.latex(r"\beta = \frac{Cov(R_s,\ R_m)}{Var(R_m)}")
st.markdown("---")
st.write("### 🔍 Beta Interpretation Guide")

col1, col2 = st.columns(2)

with col1:
    interpretation_df = pd.DataFrame({
        "Beta Range": ["β < 0", "β = 0", "0 < β < 1", "β = 1", "β > 1"],
        "Interpretation": [
            "Moves inversely to market (e.g. gold in crash)",
            "No correlation with market",
            "Less volatile than market",
            "Moves exactly with market",
            "More volatile than market"
        ],
        "Risk": ["Special", "None", "Low", "Market", "High"]
    })
    fig_guide = plotly_table(interpretation_df.set_index("Beta Range"))
    st.plotly_chart(fig_guide, use_container_width=True)

with col2:
    st.write("")
    st.info("**Low Beta (< 1):** Defensive stocks like utilities or consumer staples. Good for conservative investors.")
    st.warning("**Beta = 1:** Stock moves in line with the overall market. Average market risk.")
    st.error("**High Beta (> 1):** Aggressive stocks like tech or EV companies. Higher risk, higher reward.")

st.markdown("---")

with st.spinner(f"Calculating Beta for {ticker.upper()} against {market_index}..."):
    stock_data = load_stock_data(ticker, start="2020-01-01")
    market_data = load_stock_data(index_ticker, start="2020-01-01")

    if stock_data.empty or market_data.empty:
        st.error("Error fetching data. Please check the ticker symbol and try again.")
        st.stop()

    stock_returns = calculate_returns(stock_data["Close"].squeeze())
    market_returns = calculate_returns(market_data["Close"].squeeze())

    combined = pd.concat([stock_returns, market_returns], axis=1).dropna()
    combined.columns = ["Stock", "Market"]

    beta = round(calculate_beta(stock_returns, market_returns), 2)
    expected_return = round(calculate_capm_return(beta), 2)
    annual_stock_return = round(annualized_return(combined["Stock"]), 2)
    annual_market_return = round(annualized_return(combined["Market"]), 2)
    stock_volatility = round(annualized_volatility(combined["Stock"]), 2)

    st.write(f"### 📈 Results for {ticker.upper()}")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Beta (β)", beta, "High Risk" if beta > 1.5 else "Medium Risk" if beta > 1 else "Low Risk")
    m2.metric("Expected Return (CAPM)", f"{expected_return}%")
    m3.metric("Annual Stock Return", f"{annual_stock_return}%")
    m4.metric("Stock Volatility", f"{stock_volatility}%")

    st.markdown("---")
    st.write("### 📊 Rolling 30-Day Beta")

    rolling_beta_series = rolling_beta(stock_returns, market_returns, window=30)

    fig_rolling = go.Figure()
    fig_rolling.add_trace(go.Scatter(
        x=rolling_beta_series.index,
        y=rolling_beta_series.values,
        mode="lines",
        name="Rolling Beta",
        line=dict(width=2, color="#38bdf8")
    ))

    fig_rolling.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Market Beta = 1", annotation_position="top right")
    fig_rolling.add_hline(y=beta, line_dash="dot", line_color="green", annotation_text=f"Avg Beta = {beta}", annotation_position="bottom right")

    fig_rolling.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        yaxis_title="Beta",
        xaxis_title="Date"
    )
    fig_rolling.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig_rolling, use_container_width=True)

    st.markdown("---")
    st.write("### 📊 Stock Returns vs Market Returns")

    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=combined["Market"],
        y=combined["Stock"],
        mode="markers",
        name="Daily Returns",
        marker=dict(color="#38bdf8", size=4, opacity=0.5)
    ))

    x_line = np.linspace(combined["Market"].min(), combined["Market"].max(), 100)
    y_line = beta * x_line

    fig_scatter.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        name=f"Beta Line (β={beta})",
        line=dict(color="red", width=2, dash="dash")
    ))

    fig_scatter.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        xaxis_title="Market Returns",
        yaxis_title=f"{ticker.upper()} Returns"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)