import pandas as pd
import numpy as np

def profit_pulse_precision(df):
    """
    Implements the "Profit Pulse Precision" strategy for trading signals.
    
    Parameters:
    df (DataFrame): DataFrame containing OHLC price data
    
    Returns:
    tuple: (action, safety, entry_price, stop_loss, take_profit) or (None, None, None, None, None) if no signal
    """
    # Calculate technical indicators
    df = calculate_indicators(df)
    
    # Get the current price
    curr_price = df['close'].iloc[-1]
    
    # Check for buy signal
    if is_buy_signal(df):
        # Calculate stop loss and take profit for buy
        sl = curr_price - calculate_stop_loss(df, 'buy')
        tp = curr_price + calculate_take_profit(df, 'buy')
        return "BUY", 98, curr_price, sl, tp
    
    # Check for sell signal
    elif is_sell_signal(df):
        # Calculate stop loss and take profit for sell
        sl = curr_price + calculate_stop_loss(df, 'sell')
        tp = curr_price - calculate_take_profit(df, 'sell')
        return "SELL", 98, curr_price, sl, tp
    
    # No signal
    return None, None, None, None, None

def calculate_indicators(df):
    """Calculate all technical indicators needed for the strategy"""
    # Exponential Moving Averages
    df['ema10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    
    # Average True Range (ATR)
    df['tr'] = calculate_true_range(df)
    df['atr'] = df['tr'].rolling(14).mean()
    
    # Average Directional Index (ADX)
    # This is a simplified ADX calculation for the purpose of this strategy
    df['plus_dm'] = calculate_directional_movement(df, 'plus')
    df['minus_dm'] = calculate_directional_movement(df, 'minus')
    df['plus_di'] = 100 * (df['plus_dm'].rolling(14).mean() / df['atr'])
    df['minus_di'] = 100 * (df['minus_dm'].rolling(14).mean() / df['atr'])
    df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
    df['adx'] = df['dx'].rolling(14).mean()
    
    # Relative Strength Index (RSI)
    df['price_change'] = df['close'].diff()
    df['gain'] = df['price_change'].clip(lower=0)
    df['loss'] = -df['price_change'].clip(upper=0)
    df['avg_gain'] = df['gain'].rolling(7).mean()
    df['avg_loss'] = df['loss'].rolling(7).mean()
    df['rs'] = df['avg_gain'] / df['avg_loss'].replace(0, 0.00001)  # Avoid division by zero
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    
    return df

def calculate_true_range(df):
    """Calculate the True Range"""
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    
    # Create a DataFrame with the three components
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    
    # Return the maximum of the three components
    return ranges.max(axis=1)

def calculate_directional_movement(df, direction):
    """Calculate Directional Movement for ADX"""
    if direction == 'plus':
        # +DM
        up_move = df['high'] - df['high'].shift(1)
        down_move = df['low'].shift(1) - df['low']
        return pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0), index=df.index)
    else:
        # -DM
        up_move = df['high'] - df['high'].shift(1)
        down_move = df['low'].shift(1) - df['low']
        return pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0), index=df.index)

def is_buy_signal(df):
    """Check if current conditions match buy signal criteria"""
    # Get the last two rows for checking crossover
    ema10_last = df['ema10'].iloc[-1]
    ema10_prev = df['ema10'].iloc[-2]
    ema50_last = df['ema50'].iloc[-1]
    ema50_prev = df['ema50'].iloc[-2]
    
    # Get other indicators' values
    adx = df['adx'].iloc[-1]
    atr = df['atr'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    
    # Convert ATR to pips (assuming 4-digit forex pair)
    atr_pips = atr * 10000  # For JPY pairs, would be * 100
    
    # Check EMA crossover (10 crosses above 50)
    ema_crossover = ema10_last > ema50_last and ema10_prev <= ema50_prev
    
    # Check all conditions for buy signal
    return (ema_crossover and 
            adx > 25 and  # Strong trend
            atr_pips < 15 and  # Low volatility (less than 15 pips)
            40 < rsi < 60)  # RSI in neutral zone

def is_sell_signal(df):
    """Check if current conditions match sell signal criteria"""
    # Get the last two rows for checking crossover
    ema10_last = df['ema10'].iloc[-1]
    ema10_prev = df['ema10'].iloc[-2]
    ema50_last = df['ema50'].iloc[-1]
    ema50_prev = df['ema50'].iloc[-2]
    
    # Get other indicators' values
    adx = df['adx'].iloc[-1]
    atr = df['atr'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    
    # Convert ATR to pips (assuming 4-digit forex pair)
    atr_pips = atr * 10000  # For JPY pairs, would be * 100
    
    # Check EMA crossover (10 crosses below 50)
    ema_crossover = ema10_last < ema50_last and ema10_prev >= ema50_prev
    
    # Check all conditions for sell signal
    return (ema_crossover and 
            adx > 25 and  # Strong trend
            atr_pips < 15 and  # Low volatility (less than 15 pips)
            40 < rsi < 60)  # RSI in neutral zone

def calculate_stop_loss(df, direction):
    """Calculate stop loss distance based on ATR"""
    # Use ATR to determine stop loss (ATR/2 or about 8 pips)
    atr = df['atr'].iloc[-1]
    
    # Base SL on ATR, but ensure it's at least 8 pips (0.0008)
    sl_distance = max(atr / 2, 0.0008)
    
    return sl_distance

def calculate_take_profit(df, direction):
    """Calculate take profit based on 3:1 risk-reward ratio"""
    # Get the stop loss distance
    sl_distance = calculate_stop_loss(df, direction)
    
    # TP is 3 times the SL distance
    tp_distance = sl_distance * 3.0
    
    return tp_distance
