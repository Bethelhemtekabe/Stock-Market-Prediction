
import pandas as pd

def load_data(filepath):
    """Load a stock CSV file and return a clean, date-indexed DataFrame."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df.sort_index()
    print(f"Loaded {len(df)} rows from '{filepath}'")
    return df

def remove_nulls(df):
    """Remove rows that have any missing values. Print a summary."""
    before = len(df)
    df = df.dropna()
    print(f"Removed {before - len(df)} row(s). {len(df)} rows remaining.")
    return df