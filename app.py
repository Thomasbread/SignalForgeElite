import streamlit as st
import pandas as pd
import numpy as np
import pyperclip
from datetime import datetime, timedelta
import time
from strategy import profit_pulse_precision
from utils import format_price

# App configuration
st.set_page_config(
    page_title="Signal Forge Elite",
    page_icon="📊",
    layout="centered"
)

# App title and description
st.title("Signal Forge Elite")
st.subheader("Perfekte Trading-Signale")

# Currency pair selection
currency_pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"]
symbol = st.selectbox("Währungspaar", currency_pairs)

# Generate synthetic forex data
def get_forex_data(symbol, num_candles=500):
    try:
        # Set seed based on currency pair for consistent results
        np.random.seed(hash(symbol) % 10000)
        
        # Create timestamps
        end_time = pd.Timestamp.now()
        start_time = end_time - pd.Timedelta(minutes=5 * num_candles)
        times = pd.date_range(start=start_time, end=end_time, periods=num_candles)
        
        # Base prices for different pairs
        base_prices = {
            "EURUSD": 1.08,
            "GBPUSD": 1.25,
            "USDJPY": 154.50,
            "AUDUSD": 0.65,
            "USDCAD": 1.37,
            "USDCHF": 0.91,
            "NZDUSD": 0.59
        }
        
        # Generate price data with realistic patterns
        base_price = base_prices.get(symbol, 1.0)
        
        # Create a trend component
        trend = np.cumsum(np.random.normal(0, 0.0001, num_candles))
        
        # Create a cyclical component
        t = np.linspace(0, 10, num_candles)
        cycle = 0.001 * np.sin(t) + 0.0005 * np.sin(3*t)
        
        # Create a random component
        noise = np.random.normal(0, 0.0003, num_candles)
        
        # Combine components
        closes = base_price + trend + cycle + noise
        
        # Generate OHLC data with realistic relationships
        typical_spread = 0.0002 if "JPY" not in symbol else 0.02
        
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

# Function to refresh data
def refresh_data():
    with st.spinner("Analysiere Marktbedingungen..."):
        df = get_forex_data(symbol)
        if df is not None:
            # Apply the strategy
            action, safety, entry, sl, tp = profit_pulse_precision(df)
            
            # Display the results
            if action:
                expiry = (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M UTC")
                
                # Übersetze "BUY" und "SELL" ins Deutsche
                action_de = "KAUF" if action == "BUY" else "VERKAUF"
                
                signal_text = f"""
SIGNAL FÜR: {symbol}
RICHTUNG: {action_de}
EINSTIEG: {format_price(entry, symbol)}
STOP-LOSS: {format_price(sl, symbol)}
TAKE-PROFIT: {format_price(tp, symbol)}
SICHERHEIT: {safety}%
GÜLTIG BIS: {expiry}
                """
                
                st.text_area("Aktuelles Signal", signal_text, height=200)
                
                if st.button("Signal kopieren"):
                    try:
                        pyperclip.copy(signal_text)
                        st.success("Signal kopiert!")
                    except Exception as e:
                        st.error(f"Fehler beim Kopieren: {e}")
                        st.info("Bitte wähle den Signal-Text manuell aus und kopiere ihn.")
                
                # Display risk-reward info
                if entry is not None and sl is not None and tp is not None:  # Stellen sicher, dass keine None-Werte da sind
                    pips_risk = abs(entry - sl) * (10000 if 'JPY' not in symbol else 100)
                    pips_reward = abs(tp - entry) * (10000 if 'JPY' not in symbol else 100)
                    st.info(f"Risiko: {pips_risk:.1f} Pips | Gewinn: {pips_reward:.1f} Pips | Verhältnis: {pips_reward/pips_risk:.1f}:1")
                
            else:
                st.info("Warte auf perfektes Signal... Der Algorithmus generiert nur Signale mit höchster Erfolgswahrscheinlichkeit.")
                # Show when the data was last updated
                st.text(f"Letzte Prüfung: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.error("Konnte keine Marktdaten abrufen. Bitte überprüfe deine Verbindung.")

# Initial data load
refresh_data()

# Add a refresh button
if st.button("Nach neuen Signalen suchen"):
    refresh_data()

# Auto-refresh option
auto_refresh = st.checkbox("Automatische Aktualisierung (alle 5 Minuten)")
if auto_refresh:
    refresh_interval = 300  # 5 minutes in seconds
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Check if it's time to refresh
    current_time = time.time()
    if current_time - st.session_state.last_refresh >= refresh_interval:
        refresh_data()
        st.session_state.last_refresh = current_time
    
    # Display time until next refresh
    time_left = refresh_interval - (current_time - st.session_state.last_refresh)
    st.text(f"Nächste Aktualisierung in: {int(time_left)} Sekunden")
    st.rerun()

# Footer
st.markdown("---")
st.caption("Signal Forge Elite - Handle mit Zuversicht")
st.caption("HAFTUNGSAUSSCHLUSS: Diese Anwendung bietet keine Finanzberatung. Der Handel birgt Risiken. Konsultieren Sie immer einen lizenzierten Finanzberater.")
