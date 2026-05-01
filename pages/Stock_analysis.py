import streamlit as st
import pandas as pd
import datetime
from pages.utils.data_loader import load_stock_data, load_stock_history, load_stock_info
from pages.utils.plotly_figure import plotly_table, candlestick, close_chart, Moving_average, RSI, MACD
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: #f8fafc;
}
h1, h2, h3, h4 {
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
div[data-baseweb="input"] {
    background-color: #1e293b !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}
button[kind="secondary"] {
    background-color: #1e293b !important;
    color: #38bdf8 !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 18px;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

st.title("Stock Analysis")

today = datetime.date.today()

if "ticker" not in st.session_state:
    st.session_state.ticker = "TSLA"
if "num_period" not in st.session_state:
    st.session_state.num_period = "1y"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Candle"
if "indicator" not in st.session_state:
    st.session_state.indicator = "RSI"
if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.date(today.year - 1, today.month, today.day)
if "end_date" not in st.session_state:
    st.session_state.end_date = today

with st.form("stock_analysis_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        ticker_input = st.text_input("Stock Ticker", value=st.session_state.ticker)

    with col2:
        start_date = st.date_input("Choose Start Date", value=st.session_state.start_date)

    with col3:
        end_date = st.date_input("Choose End Date", value=st.session_state.end_date)

    submitted = st.form_submit_button("Analyze")

if submitted or st.session_state.ticker:
    st.session_state.ticker = ticker_input.upper().strip()
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

ticker = st.session_state.ticker
start_date = st.session_state.start_date
end_date = st.session_state.end_date

st.subheader(ticker)

stock_info = load_stock_info(ticker)

st.write(stock_info.get("longBusinessSummary", "No business summary available"))
st.write("**Sector:**", stock_info.get("sector", "N/A"))
st.write("**Full Time Employees:**", stock_info.get("fullTimeEmployees", "N/A"))
st.write("**Website:**", stock_info.get("website", "N/A"))

col1, col2 = st.columns(2)

with col1:
    df1 = pd.DataFrame(index=["Market Cap", "Beta", "EPS", "PE Ratio"])
    df1[""] = [
        stock_info.get("marketCap", "N/A"),
        stock_info.get("beta", "N/A"),
        stock_info.get("trailingEps", "N/A"),
        stock_info.get("trailingPE", "N/A")
    ]
    st.plotly_chart(plotly_table(df1), use_container_width=True)

with col2:
    df2 = pd.DataFrame(index=[
        "Quick Ratio",
        "Revenue per share",
        "Profit Margins",
        "Debt to Equity",
        "Return on Equity"
    ])
    df2[""] = [
        stock_info.get("quickRatio", "N/A"),
        stock_info.get("revenuePerShare", "N/A"),
        stock_info.get("profitMargins", "N/A"),
        stock_info.get("debtToEquity", "N/A"),
        stock_info.get("returnOnEquity", "N/A")
    ]
    st.plotly_chart(plotly_table(df2), use_container_width=True)

data = load_stock_data(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No stock data found. Please check the ticker symbol.")
    st.stop()

col1, col2, col3 = st.columns(3)
close_series = data["Close"].squeeze()

live_price = stock_info.get("currentPrice") or stock_info.get("regularMarketPrice")
previous_close = float(close_series.iloc[-1]) if len(close_series) > 0 else 0.0

if live_price is None:
    live_price = previous_close

daily_change = live_price - previous_close

col1.metric("Live Price", f"{live_price:.2f}", f"{daily_change:+.2f}")

last_10_df = data.tail(10).sort_index(ascending=False).round(2)
st.write("### Last 10 Days Stock Data")
st.plotly_chart(plotly_table(last_10_df), use_container_width=True)

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    if st.button("5D"):
        st.session_state.num_period = "5d"
with c2:
    if st.button("1M"):
        st.session_state.num_period = "1mo"
with c3:
    if st.button("6M"):
        st.session_state.num_period = "6mo"
with c4:
    if st.button("YTD"):
        st.session_state.num_period = "ytd"
with c5:
    if st.button("1Y"):
        st.session_state.num_period = "1y"
with c6:
    if st.button("5Y"):
        st.session_state.num_period = "5y"
with c7:
    if st.button("MAX"):
        st.session_state.num_period = "max"

num_period = st.session_state.num_period

col1, col2, col3 = st.columns([1, 1, 4])

chart_options = ("Candle", "Line")
line_indicators = ("RSI", "Moving Average", "MACD")
candle_indicators = ("RSI", "MACD")

with col1:
    chart_type = st.selectbox("", chart_options, index=chart_options.index(st.session_state.chart_type))
    st.session_state.chart_type = chart_type

with col2:
    if chart_type == "Candle":
        default_indicator = st.session_state.indicator if st.session_state.indicator in candle_indicators else "RSI"
        indicators = st.selectbox("", candle_indicators, index=candle_indicators.index(default_indicator))
    else:
        default_indicator = st.session_state.indicator if st.session_state.indicator in line_indicators else "RSI"
        indicators = st.selectbox("", line_indicators, index=line_indicators.index(default_indicator))
    st.session_state.indicator = indicators

history_data = load_stock_history(ticker, period="5y")

if history_data.empty:
    st.warning("Unable to load chart data.")
    st.stop()

if chart_type == "Candle" and indicators == "RSI":
    st.plotly_chart(candlestick(history_data, num_period), use_container_width=True)
    st.plotly_chart(RSI(history_data, num_period), use_container_width=True)
elif chart_type == "Candle" and indicators == "MACD":
    st.plotly_chart(candlestick(history_data, num_period), use_container_width=True)
    st.plotly_chart(MACD(history_data, num_period), use_container_width=True)
elif chart_type == "Line" and indicators == "RSI":
    st.plotly_chart(close_chart(history_data, num_period), use_container_width=True)
    st.plotly_chart(RSI(history_data, num_period), use_container_width=True)
elif chart_type == "Line" and indicators == "Moving Average":
    st.plotly_chart(Moving_average(history_data, num_period), use_container_width=True)
elif chart_type == "Line" and indicators == "MACD":
    st.plotly_chart(close_chart(history_data, num_period), use_container_width=True)
    st.plotly_chart(MACD(history_data, num_period), use_container_width=True)