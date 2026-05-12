# ==========================================
# 4. TECHNICAL ANALYSIS PLOTTING (UPDATED)
# ==========================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 

def plot_technical_analysis(df, save_path=None):
    """
    Generate a 3-panel chart showing:
    1. Close Price overlaid with Moving Averages (SMA_20, EMA_20, SMA_50, EMA_50).
    2. Relative Strength Index (RSI_14) with overbought/oversold levels.
    3. MACD line, Signal line, and color-coded momentum Histogram.
    
    All panels share the same X-axis (Dates) for perfect chronological alignment.
    """
    # Create aligned subplots (height ratio 2:1:1 gives the price chart primary focus)
    fig, axes = plt.subplots(
        3, 1, 
        figsize=(14, 10), 
        sharex=True, 
        gridspec_kw={'height_ratios': [2, 1, 1]}
    )
    
    # --- PANEL 1: Close Price & Moving Averages ---
    axes[0].plot(df.index, df["Close"], label="Close Price", color="black", linewidth=1.5)
    
    # Plot 20-Day Moving Averages if they exist
    if "SMA_20" in df.columns:
        axes[0].plot(df.index, df["SMA_20"], label="SMA 20", color="blue", linestyle="--", alpha=0.8)
    if "EMA_20" in df.columns:
        axes[0].plot(df.index, df["EMA_20"], label="EMA 20", color="orange", linestyle=":", alpha=0.8)
        
    # Plot 50-Day Moving Averages if they exist (NEW ADDITIONS)
    if "SMA_50" in df.columns:
        axes[0].plot(df.index, df["SMA_50"], label="SMA 50", color="red", linestyle="--", alpha=0.8)
    if "EMA_50" in df.columns:
        axes[0].plot(df.index, df["EMA_50"], label="EMA 50", color="magenta", linestyle=":", alpha=0.8)
            
    axes[0].set_title("Close Price & Moving Averages", fontsize=14, fontweight='bold')
    axes[0].set_ylabel("Price ($)", fontsize=11)
    axes[0].legend(loc="upper left")
    axes[0].grid(True, linestyle="--", alpha=0.4)


    
    # --- PANEL 2: Relative Strength Index (RSI) ---
    if "RSI_14" in df.columns:
        axes[1].plot(df.index, df["RSI_14"], label="RSI (14)", color="purple", linewidth=1.2)
        axes[1].axhline(70, color="red", linestyle="--", alpha=0.6, label="Overbought (70)")
        axes[1].axhline(30, color="green", linestyle="--", alpha=0.6, label="Oversold (30)")
        axes[1].fill_between(df.index, 70, 100, color="red", alpha=0.05)
        axes[1].fill_between(df.index, 0, 30, color="green", alpha=0.05)
        axes[1].set_ylabel("RSI Value", fontsize=11)
        axes[1].set_ylim(10, 90)
        axes[1].set_title("Relative Strength Index (RSI)", fontsize=12, fontweight='bold')
        axes[1].legend(loc="upper left")
        axes[1].grid(True, linestyle="--", alpha=0.4)
        
    # --- PANEL 3: MACD Momentum ---
    if "MACD" in df.columns and "MACD_Signal" in df.columns:
        axes[2].plot(df.index, df["MACD"], label="MACD", color="blue", linewidth=1.2)
        axes[2].plot(df.index, df["MACD_Signal"], label="Signal Line", color="orange", linewidth=1.2)
        
        if "MACD_Hist" in df.columns:
            positive_hist = df["MACD_Hist"] > 0
            bar_colors = np.where(positive_hist, "green", "red")
            axes[2].bar(df.index, df["MACD_Hist"], label="Histogram", color=bar_colors, alpha=0.5, width=1.0)
            
        axes[2].set_ylabel("MACD / Signal", fontsize=11)
        axes[2].set_xlabel("Date", fontsize=11)
        axes[2].set_title("MACD (Moving Average Convergence Divergence)", fontsize=12, fontweight='bold')
        axes[2].legend(loc="upper left")
        axes[2].grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Chart saved successfully to '{save_path}'")
        
    plt.show()