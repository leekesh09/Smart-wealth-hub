import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

from statsmodels.tsa.arima.model import ARIMA
from pages.utils.data_loader import load_stock_data

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Stock Prediction ")

today = datetime.date.today()

# ---------------- SESSION ----------------
if "pred_ticker" not in st.session_state:
    st.session_state.pred_ticker = "TSLA"

# ---------------- FORM ----------------
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        ticker = st.text_input("Stock Ticker", value=st.session_state.pred_ticker)

    with col2:
        start_date = st.date_input(
            "Start Date",
            datetime.date(today.year - 2, today.month, today.day)
        )

    with col3:
        end_date = st.date_input("End Date", today)

    forecast_days = st.slider("Forecast Days", 7, 60, 30)

    submitted = st.form_submit_button("Predict")

# ---------------- UPDATE STATE ----------------
if submitted:
    st.session_state.pred_ticker = ticker.upper().strip()

ticker = st.session_state.pred_ticker

# ---------------- LOAD DATA ----------------
data = load_stock_data(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No stock data found.")
    st.stop()

# ---------------- PREPARE DATA ----------------
close_data = data["Close"].dropna()

#  LOG TRANSFORM (fix trend issue)
log_data = np.log(close_data)

# ---------------- ARIMA MODEL ----------------
model = ARIMA(log_data, order=(2, 1, 2))
model_fit = model.fit()

# ---------------- FORECAST ----------------
forecast_log = model_fit.forecast(steps=forecast_days)
forecast = np.exp(forecast_log)

#  Add small randomness (realistic)
forecast = forecast * (1 + np.random.normal(0, 0.01, len(forecast)))

# Convert to numpy (fix error)
forecast = np.array(forecast)

# ---------------- FUTURE DATES ----------------
future_dates = pd.date_range(
    start=close_data.index[-1] + pd.Timedelta(days=1),
    periods=forecast_days
)


# ---------------- TABLE ----------------
forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted Close": forecast
})

st.write("### 📋 Forecast Data")
st.dataframe(forecast_df, use_container_width=True)
