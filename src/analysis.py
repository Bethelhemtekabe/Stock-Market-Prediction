def compute_sma(series, window):
    """Compute the Simple Moving Average over a given number of days."""
    return series.rolling(window=window).mean()

def get_daily_return(close):
    """Calculate the daily percentage change in closing price."""
    return close.pct_change() * 100