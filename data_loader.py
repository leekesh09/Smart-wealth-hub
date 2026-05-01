import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data(ttl=600, show_spinner=False)
def load_stock_info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}


@st.cache_data(ttl=600, show_spinner=False)
def load_stock_data(ticker: str, start=None, end=None) -> pd.DataFrame:
    try:
        data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
        if isinstance(data, pd.DataFrame):
            return data
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600, show_spinner=False)
def load_stock_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    try:
        data = yf.Ticker(ticker).history(period=period, auto_adjust=False)
        if isinstance(data, pd.DataFrame):
            return data
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600, show_spinner=False)
def load_multiple_data(tickers, start=None, end=None) -> pd.DataFrame:
    try:
        data = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=False)
        if isinstance(data, pd.DataFrame):
            return data
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()