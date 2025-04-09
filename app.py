import streamlit as st
import pandas as pd
import numpy as np
import pyperclip
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from strategy import profit_pulse_precision
from utils import format_price, save_signal, get_signals_history, get_mt5_connection_status

# App configuration
st.set_page_config(
    page_title="Signal Forge Elite",
    page_icon="📊",
    layout="wide"  # Use wide layout for better display
)

# Custom CSS for a more epic look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(to bottom, #0e1117, #1e2130);
    }
    h1, h2, h3 {
        color: #4CAF50 !important;
        font-weight: bold !important;
    }
    .stTextArea textarea {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 5px !important;
        font-family: monospace !important;
    }
    .signal-card {
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: rgba(30, 33, 48, 0.8);
    }
    .buy-signal {
        border-left: 5px solid #4CAF50;
    }
    .sell-signal {
        border-left: 5px solid #FF5252;
    }
    .stButton button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    .stButton button:hover {
        background-color: #45a049 !important;
        box-shadow: 0 0 10px #4CAF50 !important;
    }
    .signal-header {
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 10px;
        color: white;
    }
    .signal-details {
        font-family: monospace;
        font-size: 0.9em;
        color: #b0b0b0;
    }
    .signal-price {
        font-weight: bold;
        font-size: 1.1em;
        color: white;
    }
    .crypto-icon {
        font-size: 1.5em;
        margin-right: 10px;
    }
    .stInfo {
        background-color: rgba(30, 33, 48, 0.8) !important;
        color: white !important;
        border: 1px solid #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

# App header with epic styling
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3em; margin-bottom: 0;">⚡ SIGNAL FORGE ELITE ⚡</h1>
    <p style="font-size: 1.2em; color: #b0b0b0;">Die ultimative Signal-basierte Trading-Plattform</p>
</div>
""", unsafe_allow_html=True)

# MT5 Connection Status in Sidebar
st.sidebar.title("MT5 Verbindung")
mt5_status = get_mt5_connection_status()

if mt5_status['connected']:
    st.sidebar.success("MT5 verbunden")
else:
    st.sidebar.warning(mt5_status['message'])
    if st.sidebar.button("Mit MT5 verbinden"):
        st.sidebar.info("Versuche, die MT5-Verbindung herzustellen...")
        # In a real implementation, this would attempt to connect to MT5

# Currency pairs with cryptos
currency_pairs = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD",
    "BTCUSD", "SOLUSD", "ETHUSD", "XRPUSD", "ADAUSD"
]

# Base prices for different pairs including crypto
base_prices = {
    "EURUSD": 1.08,
    "GBPUSD": 1.25,
    "USDJPY": 154.50,
    "AUDUSD": 0.65,
    "USDCAD": 1.37,
    "USDCHF": 0.91,
    "NZDUSD": 0.59,
    "BTCUSD": 63500.0,
    "SOLUSD": 145.75,
    "ETHUSD": 3080.0,
    "XRPUSD": 0.52,
    "ADAUSD": 0.45
}

# Generate synthetic forex data
def get_forex_data(symbol, num_candles=500):
    try:
        # Set seed based on currency pair for consistent results
        np.random.seed(hash(symbol) % 10000)
        
        # Create timestamps
        end_time = pd.Timestamp.now()
        start_time = end_time - pd.Timedelta(minutes=5 * num_candles)
        times = pd.date_range(start=start_time, end=end_time, periods=num_candles)
        
        # Generate price data with realistic patterns
        base_price = base_prices.get(symbol, 1.0)
        
        # Create a trend component
        trend = np.cumsum(np.random.normal(0, 0.0001 * base_price, num_candles))
        
        # Create a cyclical component
        t = np.linspace(0, 10, num_candles)
        cycle_amplitude = 0.001 * base_price
        cycle = cycle_amplitude * np.sin(t) + 0.0005 * base_price * np.sin(3*t)
        
        # Create a random component
        noise_level = 0.0003 * base_price
        noise = np.random.normal(0, noise_level, num_candles)
        
        # Combine components
        closes = base_price + trend + cycle + noise
        
        # Generate OHLC data with realistic relationships
        typical_spread = 0.0002 * base_price if "JPY" not in symbol else 0.02
        if any(crypto in symbol for crypto in ['BTC', 'SOL', 'ETH', 'XRP', 'ADA']):
            typical_spread = 0.001 * base_price  # Higher spread for crypto
        
        # Close-to-close changes
        changes = np.diff(closes, prepend=closes[0])
        
        # Generate high, low, open based on close and typical volatility
        highs = closes + np.abs(np.random.normal(typical_spread, typical_spread*2, num_candles))
        lows = closes - np.abs(np.random.normal(typical_spread, typical_spread*2, num_candles))
        opens = np.roll(closes, 1)
        opens[0] = closes[0] - changes[0]/2
        
        # Ensure high >= close >= low for all candles
        for i in range(num_candles):
            highs[i] = max(highs[i], closes[i], opens[i])
            lows[i] = min(lows[i], closes[i], opens[i])
        
        # Create DataFrame
        df = pd.DataFrame({
            'time': times,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'tick_volume': np.random.randint(100, 1000, num_candles),
            'spread': np.random.randint(1, 5, num_candles),
            'real_volume': np.random.randint(1000, 10000, num_candles)
        })
        
        return df
    except Exception as e:
        st.error(f"Error generating data: {e}")
        return None

# Function to create a candlestick chart
def create_candlestick_chart(df, symbol, action=None, entry=None, sl=None, tp=None):
    # Create figure
    fig = go.Figure()
    
    # Add candlestick trace
    fig.add_trace(go.Candlestick(
        x=df['time'].tail(100),
        open=df['open'].tail(100),
        high=df['high'].tail(100),
        low=df['low'].tail(100),
        close=df['close'].tail(100),
        name='Candlesticks',
        increasing_line_color='#4CAF50',
        decreasing_line_color='#FF5252'
    ))
    
    # Add EMA lines
    if 'ema10' in df.columns and 'ema50' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['time'].tail(100),
            y=df['ema10'].tail(100),
            line=dict(color='#FFD700', width=1),
            name='EMA 10'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['time'].tail(100),
            y=df['ema50'].tail(100),
            line=dict(color='#00A3FF', width=1),
            name='EMA 50'
        ))
    
    # Add horizontal lines for entry, SL, TP if available
    last_time = df['time'].iloc[-1]
    first_time = df['time'].tail(100).iloc[0]
    if action and entry and sl and tp:
        # Entry line
        fig.add_trace(go.Scatter(
            x=[first_time, last_time],
            y=[entry, entry],
            line=dict(color='white', width=1, dash='dash'),
            name='Einstieg'
        ))
        
        # Stop Loss line
        fig.add_trace(go.Scatter(
            x=[first_time, last_time],
            y=[sl, sl],
            line=dict(color='#FF5252', width=1, dash='dash'),
            name='Stop Loss'
        ))
        
        # Take Profit line
        fig.add_trace(go.Scatter(
            x=[first_time, last_time],
            y=[tp, tp],
            line=dict(color='#4CAF50', width=1, dash='dash'),
            name='Take Profit'
        ))
    
    # Update layout
    fig.update_layout(
        title=f'{symbol} Chart',
        xaxis_title='Zeit',
        yaxis_title='Preis',
        height=500,
        template='plotly_dark',
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_rangeslider_visible=False
    )
    
    return fig

# Function to refresh data for a single pair
def analyze_pair(symbol):
    df = get_forex_data(symbol)
    if df is not None:
        # Apply the strategy
        action, safety, entry, sl, tp = profit_pulse_precision(df)
        
        if action:
            expiry = (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M UTC")
            # Save the signal to history
            save_signal(symbol, action, entry, sl, tp, safety, expiry)
            
            return {
                'symbol': symbol,
                'action': action,
                'entry': entry,
                'sl': sl,
                'tp': tp,
                'safety': safety,
                'expiry': expiry,
                'df': df
            }
    
    return None

# Function to refresh data for all pairs
def refresh_all_pairs():
    with st.spinner("Analysiere alle Währungspaare nach perfekten Signalen..."):
        new_signals = []
        
        # Process all currency pairs
        for pair in currency_pairs:
            signal = analyze_pair(pair)
            if signal:
                new_signals.append(signal)
        
        return new_signals

# Display a single signal
def display_signal(signal, is_current=False):
    symbol = signal['symbol']
    action = signal['action']
    entry = signal['entry']
    sl = signal['sl']
    tp = signal['tp']
    safety = signal['safety']
    expiry = signal['expiry']
    
    # Übersetze "BUY" und "SELL" ins Deutsche
    action_de = "KAUF" if action == "BUY" else "VERKAUF"
    
    # Choose icon based on currency pair
    icon = "💹"  # Default icon
    if "BTC" in symbol:
        icon = "₿"
    elif "SOL" in symbol:
        icon = "☀️"
    elif "ETH" in symbol:
        icon = "Ξ"
    elif "XRP" in symbol:
        icon = "✘"
    elif "ADA" in symbol:
        icon = "₳"
    
    # Create signal card with custom styling based on action
    signal_class = "buy-signal" if action == "BUY" else "sell-signal"
    
    # Format the signal
    signal_text = f"""
SIGNAL FÜR: {symbol}
RICHTUNG: {action_de}
EINSTIEG: {format_price(entry, symbol)}
STOP-LOSS: {format_price(sl, symbol)}
TAKE-PROFIT: {format_price(tp, symbol)}
SICHERHEIT: {safety}%
GÜLTIG BIS: {expiry}
    """
    
    st.markdown(f"""
    <div class="signal-card {signal_class}">
        <div class="signal-header">
            <span class="crypto-icon">{icon}</span> {symbol} - {action_de}
        </div>
        <div class="signal-details">
            Sicherheit: {safety}% | Gültig bis: {expiry}
        </div>
        <div class="signal-price">
            Einstieg: {format_price(entry, symbol)} | SL: {format_price(sl, symbol)} | TP: {format_price(tp, symbol)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # For the current signal, display extended options
    if is_current and 'df' in signal:
        # Display the chart
        st.plotly_chart(create_candlestick_chart(signal['df'], symbol, action, entry, sl, tp), use_container_width=True)
        
        # Display risk-reward info
        if entry is not None and sl is not None and tp is not None:
            multiplier = 10000 if 'JPY' not in symbol else 100
            if any(crypto in symbol for crypto in ['BTC', 'SOL', 'ETH', 'XRP', 'ADA']):
                multiplier = 1  # Use dollars directly for crypto
            
            pips_risk = abs(entry - sl) * multiplier
            pips_reward = abs(tp - entry) * multiplier
            
            risk_unit = "Pips" if multiplier > 1 else "$"
            st.info(f"Risiko: {pips_risk:.1f} {risk_unit} | Gewinn: {pips_reward:.1f} {risk_unit} | Verhältnis: {pips_reward/pips_risk:.1f}:1")
        
        # Copy button for the signal
        if st.button("Signal kopieren", key=f"copy_{symbol}"):
            try:
                pyperclip.copy(signal_text)
                st.success("Signal kopiert!")
            except Exception as e:
                st.error(f"Fehler beim Kopieren: {e}")
                st.info("Bitte wähle den Signal-Text manuell aus und kopiere ihn.")

# Main app layout
tab1, tab2, tab3 = st.tabs(["Aktuelle Signale", "Signalverlauf", "MT5 Verbindung"])

with tab1:
    # Check if "current_signals" exists in session state
    if "current_signals" not in st.session_state:
        st.session_state.current_signals = []
        st.session_state.last_refresh = time.time()
    
    # Refresh button at the top
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Nach neuen Signalen suchen", use_container_width=True):
            st.session_state.current_signals = refresh_all_pairs()
            st.session_state.last_refresh = time.time()
    
    with col1:
        # Auto-refresh option
        auto_refresh = st.checkbox("Automatische Aktualisierung (alle 5 Minuten)")
        if auto_refresh:
            refresh_interval = 300  # 5 minutes in seconds
            
            # Check if it's time to refresh
            current_time = time.time()
            if current_time - st.session_state.last_refresh >= refresh_interval:
                st.session_state.current_signals = refresh_all_pairs()
                st.session_state.last_refresh = current_time
            
            # Display time until next refresh
            time_left = refresh_interval - (current_time - st.session_state.last_refresh)
            st.text(f"Nächste Aktualisierung in: {int(time_left)} Sekunden")
            st.rerun()
    
    # Display the signals
    if st.session_state.current_signals:
        st.markdown("## Aktuelle Trading-Signale")
        for signal in st.session_state.current_signals:
            display_signal(signal, is_current=True)
    else:
        st.info("Keine perfekten Signale gefunden. Der Algorithmus generiert nur Signale mit höchster Erfolgswahrscheinlichkeit.")
        st.text(f"Letzte Prüfung: {datetime.now().strftime('%H:%M:%S')}")

with tab2:
    st.markdown("## Signalverlauf (letzte 3 Tage)")
    
    # Get signal history
    signal_history = get_signals_history(days=3)
    
    if not signal_history.empty:
        for _, row in signal_history.iterrows():
            # Convert row to signal format
            signal = {
                'symbol': row['symbol'],
                'action': row['action'],
                'entry': row['entry'],
                'sl': row['sl'],
                'tp': row['tp'],
                'safety': row['safety'],
                'expiry': row['expiry']
            }
            
            # Display the signal (but not as current)
            display_signal(signal, is_current=False)
    else:
        st.info("Keine Signale im Verlauf gefunden.")

with tab3:
    st.markdown("## MetaTrader 5 Verbindung")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Verbindungseinstellungen")
        mt5_path = st.text_input("MT5 Installationspfad", placeholder="C:\\Program Files\\MetaTrader 5")
        login = st.text_input("Login ID (optional)")
        password = st.text_input("Passwort (optional)", type="password")
        server = st.text_input("Server (optional)", placeholder="MetaQuotes-Demo")
        
        if st.button("Verbinden"):
            st.info("Versuche, Verbindung herzustellen... In einer echten Implementierung würde dies MT5 verbinden.")
    
    with col2:
        st.markdown("### Status")
        st.warning("MT5 nicht verbunden")
        st.markdown("""
        **Hinweis:** Die MT5-Verbindung erlaubt:
        - Abrufen von Live-Kursdaten
        - Direktes Platzieren von Trades
        - Automatisches Handeln mit Signalen
        
        In der aktuellen Demo-Version werden simulierte Daten verwendet.
        """)

# Footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.caption("Signal Forge Elite - Handle mit Zuversicht")
with col2:
    st.caption("HAFTUNGSAUSSCHLUSS: Diese Anwendung bietet keine Finanzberatung. Der Handel birgt Risiken.")
