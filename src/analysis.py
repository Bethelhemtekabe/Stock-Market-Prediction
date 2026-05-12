# def compute_sma(series, window):
#     """Compute the Simple Moving Average over a given number of days."""
#     return series.rolling(window=window).mean()

# def get_daily_return(close):
#     """Calculate the daily percentage change in closing price."""
#     return close.pct_change() * 100

import pandas as pd
import talib
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import quantstats as qs

def compute_sma(series, window):
    """Compute the Simple Moving Average (SMA) over a given number of days."""
    # We can use TA-Lib's optimized C implementation
    return pd.Series(talib.SMA(series.values, timeperiod=window), index=series.index)


def compute_ema(series, window):
    """Compute the Exponential Moving Average (EMA) over a given number of days."""
    return pd.Series(talib.EMA(series.values, timeperiod=window), index=series.index)


def compute_rsi(series, window=14):
    """
    Compute the Relative Strength Index (RSI).
    Standard window is 14 days. Returns values between 0 and 100.
    """
    return pd.Series(talib.RSI(series.values, timeperiod=window), index=series.index)


def compute_macd(series, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    Compute MACD (Moving Average Convergence Divergence).
    Returns a DataFrame containing:
    - macd: The difference between fast and slow EMAs.
    - macdsignal: The EMA of the MACD line.
    - macdhist: The MACD histogram (macd - macdsignal).
    """
    macd, macdsignal, macdhist = talib.MACD(
        series.values, 
        fastperiod=fastperiod, 
        slowperiod=slowperiod, 
        signalperiod=signalperiod
    )
    
    return pd.DataFrame({
        'MACD': macd,
        'MACD_Signal': macdsignal,
        'MACD_Hist': macdhist
    }, index=series.index)
















import pandas as pd

def backtest_bollinger_breakout(df):
    """
    Calculates the cumulative returns for both a Buy & Hold market strategy 
    and a Bollinger Band breakout strategy.
    
    Parameters:
    - df (pd.DataFrame): Must contain 'Close' and 'upper_band' columns.
    
    Returns:
    - pd.DataFrame: A new DataFrame containing 'Market_Cum' and 'Strategy_Cum'.
    """
    # Create a clean working copy to prevent setting-with-copy warnings
    backtest_df = df.copy()
    
    # 1. Calculate underlying asset daily returns
    backtest_df['Returns'] = backtest_df['Close'].pct_change()
    
    # 2. Generate Bollinger Breakout Signal (1 = Invested, 0 = In Cash)
    backtest_df['Signal'] = 0
    backtest_df.loc[backtest_df['Close'] > backtest_df['upper_band'], 'Signal'] = 1
    
    # 3. Strategy returns use yesterday's signal to trade today's returns
    backtest_df['Strategy_Returns'] = backtest_df['Signal'].shift(1) * backtest_df['Returns']
    
    # 4. Compute compound cumulative performance
    results = pd.DataFrame(index=backtest_df.index)
    results['Market_Cum'] = (1 + backtest_df['Returns']).cumprod()
    results['Strategy_Cum'] = (1 + backtest_df['Strategy_Returns'].fillna(0)).cumprod()
    
    return results











# Extend pandas with QuantStats methods
qs.extend_pandas()

# ==========================================
# 1. QUANTITATIVE ANALYSIS & BACKTESTING
# ==========================================

def backtest_bollinger_breakout(df, plot=True):
    """
    Backtest a Bollinger Band breakout strategy on a single local dataset.
    
    Parameters:
    - df (pd.DataFrame): Must contain 'Close' and 'upper_band' columns.
    - plot (bool): If True, plots the cumulative strategy vs. market returns.
    """
    # Create a copy to avoid modifying your original DataFrame in place
    df = df.copy()
    
    # Calculate daily percent change
    df['Returns'] = df['Close'].pct_change()

    # Simple Strategy: Buy (1) when Close > Upper Band, otherwise flat (0)
    df['Signal'] = 0
    df.loc[df['Close'] > df['upper_band'], 'Signal'] = 1
    
    # Shift signals by 1 day to execute on the next day's returns
    df['Strategy_Returns'] = df['Signal'].shift(1) * df['Returns']

    # Compute compounding cumulative returns
    df['Cumulative_Market'] = (1 + df['Returns']).cumprod()
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns'].fillna(0)).cumprod()

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(df['Cumulative_Market'], label='Market (Buy & Hold)', color='gray', alpha=0.7)
        plt.plot(df['Cumulative_Strategy'], label='Strategy (Bollinger Breakout)', color='green')
        plt.title("Single-Asset Strategy Backtesting")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Growth")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()

    return df


# ==========================================
# 2. FUNDAMENTAL SNAPSHOT
# ==========================================

def print_fundamental_snapshot(ticker_symbol):
    """
    Look up and print key fundamental metrics for a single stock ticker.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        company_name = info.get('longName', 'N/A')
        market_cap = info.get('marketCap')
        trailing_pe = info.get('trailingPE', 'N/A')
        
        # Format the market cap nicely with commas
        market_cap_str = f"${market_cap:,}" if isinstance(market_cap, (int, float)) else "N/A"
        
        print(f"--- Fundamental Snapshot: {ticker_symbol.upper()} ---")
        print(f"Company: {company_name}")
        print(f"Market Cap: {market_cap_str}")
        print(f"Trailing PE: {trailing_pe}")
        print("-" * 40)
        
    except Exception as e:
        print(f"Could not retrieve fundamentals for '{ticker_symbol}': {e}")


# ==========================================
# 3. ADVANCED PERFORMANCE REPORTING
# ==========================================

def generate_performance_report(close_series):
    """
    Calculate and print QuantStats performance metrics for a single price series.
    """
    # Calculate daily returns
    returns = close_series.pct_change().dropna()
    
    # Calculate metrics
    sharpe = qs.stats.sharpe(returns)
    max_dd = qs.stats.max_drawdown(returns) * 100
    
    print("--- Single-Asset Performance Snapshot ---")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {max_dd:.2f}%")
    print("-" * 41)
    
    return {"sharpe": sharpe, "max_drawdown": max_dd}