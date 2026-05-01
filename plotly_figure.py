import pandas as pd
import plotly.graph_objects as go
from pages.utils.indicators import add_moving_average, add_rsi, add_macd, filter_period


def plotly_table(df: pd.DataFrame):
    df_display = df.copy()
    df_display = df_display.reset_index()

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df_display.columns),
            fill_color="#1d4ed8",
            font=dict(color="white", size=14),
            align="center"
        ),
        cells=dict(
            values=[df_display[col] for col in df_display.columns],
            fill_color="#0f172a",
            font=dict(color="white", size=13),
            align="center"
        )
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="#1e293b",
        plot_bgcolor="#1e293b",
        height=350
    )
    return fig


def filter_data(df: pd.DataFrame, period: str):
    return filter_period(df, period)


def candlestick(df: pd.DataFrame, period: str):
    df = filter_period(df, period)

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    )])

    fig.update_layout(
        title="Candlestick Chart",
        height=500,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        xaxis_rangeslider_visible=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig


def close_chart(df: pd.DataFrame, period: str):
    df = filter_period(df, period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price"
    ))

    fig.update_layout(
        title="Closing Price Chart",
        height=500,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig


def Moving_average(df: pd.DataFrame, period: str):
    df = filter_period(df, period)
    df = add_moving_average(df, 20)
    df = add_moving_average(df, 50)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close"))
    fig.add_trace(go.Scatter(x=df.index, y=df["MA_20"], mode="lines", name="MA 20"))
    fig.add_trace(go.Scatter(x=df.index, y=df["MA_50"], mode="lines", name="MA 50"))

    fig.update_layout(
        title="Moving Average Chart",
        height=500,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig


def RSI(df: pd.DataFrame, period: str):
    df = filter_period(df, period)
    df = add_rsi(df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI"))

    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")

    fig.update_layout(
        title="RSI Indicator",
        height=300,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        yaxis_title="RSI",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig


def MACD(df: pd.DataFrame, period: str):
    df = filter_period(df, period)
    df = add_macd(df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode="lines", name="MACD"))
    fig.add_trace(go.Scatter(x=df.index, y=df["Signal"], mode="lines", name="Signal"))

    fig.update_layout(
        title="MACD Indicator",
        height=300,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#1e293b",
        font=dict(color="#f8fafc"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig