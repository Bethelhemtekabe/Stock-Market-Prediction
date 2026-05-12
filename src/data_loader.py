
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


def ensure_column_types(df):
    """
    Ensure core stock columns are correctly typed:
    - Float for Open, High, Low, Close
    - Int64 for Volume (handles missing values safely)
    
    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    
    Returns:
    - pd.DataFrame: The DataFrame with strictly enforced column types.
    """
    # Create a copy to prevent modifying the original data unsafely
    df = df.copy()
    
    # 1. Define price columns to enforce as float
    price_columns = ['Open', 'High', 'Low', 'Close']
    
    for col in price_columns:
        if col in df.columns:
            # If the column is read as a string/object, clean up common artifacts like '$' or ','
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
            # Cast strictly to float
            df[col] = df[col].astype(float)
            
    # 2. Define volume column to enforce as an integer
    if 'Volume' in df.columns:
        if df['Volume'].dtype == 'object':
            df['Volume'] = df['Volume'].astype(str).str.replace(',', '', regex=False)
        # 'Int64' (capital I) allows pandas to keep integers even if there are NaN values
        df['Volume'] = df['Volume'].astype('Int64')
        
    return df

 

 