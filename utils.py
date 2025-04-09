import pandas as pd
from datetime import datetime, timedelta

def format_price(price, pair=""):
    """
    Format price according to currency pair
    
    Parameters:
    price (float): The price to format
    pair (str): The currency pair (optional)
    
    Returns:
    str: Formatted price
    """
    if price is None:
        return "N/A"
        
    if 'JPY' in pair:
        # JPY pairs typically have 2 decimal places
        return f"{price:.2f}"
    elif any(crypto in pair for crypto in ['BTC', 'SOL', 'ETH']):
        # Crypto prices with more precision
        if 'BTC' in pair:
            return f"{price:.1f}"
        else:
            return f"{price:.2f}"
    else:
        # Most forex pairs have 4 or 5 decimal places
        return f"{price:.5f}"

def save_signal(symbol, action, entry, sl, tp, safety, expiry_time):
    """
    Save signal to the signals history
    
    Parameters:
    symbol (str): Currency pair
    action (str): BUY or SELL
    entry (float): Entry price
    sl (float): Stop loss price
    tp (float): Take profit price
    safety (int): Signal confidence
    expiry_time (str): Signal expiry time
    """
    # Create a new signal record
    new_signal = {
        'timestamp': datetime.now(),
        'symbol': symbol,
        'action': action,
        'entry': entry,
        'sl': sl,
        'tp': tp,
        'safety': safety,
        'expiry': expiry_time
    }
    
    try:
        # Try to load existing signals
        signals_df = pd.read_csv('signals_history.csv', parse_dates=['timestamp'])
    except:
        # If file doesn't exist, create a new DataFrame
        signals_df = pd.DataFrame(columns=[
            'timestamp', 'symbol', 'action', 'entry', 'sl', 'tp', 'safety', 'expiry'
        ])
    
    # Append new signal
    signals_df = pd.concat([signals_df, pd.DataFrame([new_signal])], ignore_index=True)
    
    # Keep only the last 3 days of signals
    cutoff_date = datetime.now() - timedelta(days=3)
    signals_df = signals_df[signals_df['timestamp'] >= cutoff_date]
    
    # Save updated signals
    signals_df.to_csv('signals_history.csv', index=False)
    
def get_signals_history(days=3):
    """
    Get signals history for the specified number of days
    
    Parameters:
    days (int): Number of days to look back
    
    Returns:
    DataFrame: Signals history
    """
    try:
        # Try to load existing signals
        signals_df = pd.read_csv('signals_history.csv', parse_dates=['timestamp'])
        
        # Filter for the last X days
        cutoff_date = datetime.now() - timedelta(days=days)
        signals_df = signals_df[signals_df['timestamp'] >= cutoff_date]
        
        # Sort by timestamp (newest first)
        signals_df = signals_df.sort_values('timestamp', ascending=False)
        
        return signals_df
    except:
        # If file doesn't exist or other error, return empty DataFrame
        return pd.DataFrame(columns=[
            'timestamp', 'symbol', 'action', 'entry', 'sl', 'tp', 'safety', 'expiry'
        ])

def get_mt5_connection_status():
    """
    Get MT5 connection status message
    """
    # In a real implementation, we would check if MT5 is connected
    # For now, we'll just return a placeholder message
    return {
        'connected': False,
        'message': "MT5 nicht verbunden. Bitte starten Sie MT5 und verbinden Sie es."
    }
