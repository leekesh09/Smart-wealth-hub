import pandas as pd


def add_moving_average(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df = df.copy()
    df[f"MA_{window}"] = df["Close"].rolling(window=window).mean()
    return df


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["RSI"] = df["RSI"].fillna(0)
    return df


def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["Histogram"] = df["MACD"] - df["Signal"]
    return df


def filter_period(df: pd.DataFrame, period: str) -> pd.DataFrame:
    if df.empty:
        return df

    period_map = {
        "5d": 5,
        "1mo": 30,
        "6mo": 180,
        "1y": 365,
        "5y": 365 * 5
    }

    if period == "max":
        return df
    if period == "ytd":
        current_year = df.index.max().year
        return df[df.index.year == current_year]

    days = period_map.get(period, 365)
    return df[df.index >= (df.index.max() - pd.Timedelta(days=days))]