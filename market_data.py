import requests
import json
import re
import random
from datetime import datetime
import time


def get_yahoo_finance_data(symbol):
    """
    Holt Kursdaten von Yahoo Finance für das angegebene Symbol
    """
    # Yahoo Finance Symbol-Mapping
    yahoo_symbols = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "JPY=X",  # Umgekehrte Notation bei Yahoo
        "AUDUSD": "AUDUSD=X",
        "USDCAD": "CAD=X",  # Umgekehrte Notation bei Yahoo
        "USDCHF": "CHF=X",  # Umgekehrte Notation bei Yahoo
        "NZDUSD": "NZDUSD=X",
        "BTCUSD": "BTC-USD",
        "SOLUSD": "SOL-USD",
        "ETHUSD": "ETH-USD",
        "XRPUSD": "XRP-USD",
        "ADAUSD": "ADA-USD"
    }
    
    if symbol not in yahoo_symbols:
        return None
    
    yahoo_symbol = yahoo_symbols[symbol]
    
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
        params = {
            "interval": "1m",
            "range": "1d"
        }
        headers = {
            "User-Agent": "Mozilla/5.0"  # Yahoo erfordert manchmal einen User-Agent
        }
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            if "meta" in result and "regularMarketPrice" in result["meta"]:
                price = result["meta"]["regularMarketPrice"]
                
                # Bei umgekehrten Notationen (wie JPY=X) müssen wir den Kehrwert nehmen
                if symbol in ["USDJPY", "USDCAD", "USDCHF"]:
                    return 1.0 / price
                return price
    
    except Exception as e:
        print(f"Fehler beim Abrufen der Yahoo Finance Daten für {symbol}: {e}")
    
    return None


def get_forex_data_from_source():
    """
    Versucht, aktuelle Marktdaten von Yahoo Finance abzurufen.
    Im Fehlerfall werden Fallback-Daten zurückgegeben.
    """
    # Aktuelle Forex-Daten (Fallback)
    forex_data = {
        "EURUSD": 1.0757,
        "GBPUSD": 1.2732,
        "USDJPY": 149.28,
        "AUDUSD": 0.6628,
        "USDCAD": 1.3484,
        "USDCHF": 0.8980,
        "NZDUSD": 0.6062,
        "BTCUSD": 70090.0,
        "SOLUSD": 147.42,
        "ETHUSD": 3502.0,
        "XRPUSD": 0.5032,
        "ADAUSD": 0.4463
    }
    
    # Holt alle Kurse von Yahoo Finance
    symbols = list(forex_data.keys())
    updated_data = {}
    
    # Kurse nacheinander abrufen mit kurzer Pause, um Rate-Limits zu vermeiden
    for symbol in symbols:
        price = get_yahoo_finance_data(symbol)
        if price is not None:
            updated_data[symbol] = price
        time.sleep(0.2)  # Kurze Pause zwischen Anfragen
    
    # Fallback-Daten mit aktuellen Daten aktualisieren
    forex_data.update(updated_data)
    
    return forex_data


def get_variation(base_price, symbol=""):
    """
    Generiert eine minimale realistische Variation für den angegebenen Basispreis
    Variation drastisch reduziert, um bei kurzen Zeitabständen realistischer zu sein
    """
    # Kleinere Variation für Forex-Paare
    if any(crypto in symbol for crypto in ['BTC', 'SOL', 'ETH', 'XRP', 'ADA']):
        # Kleinere Variation für Krypto (0.05-0.1%)
        percent = random.uniform(0.00005, 0.0001)
    elif 'JPY' in symbol:
        # Spezielle Variation für JPY-Paare
        percent = random.uniform(0.00001, 0.00005)
    else:
        # Standard-Forex-Paare (0.005-0.01%)
        percent = random.uniform(0.00001, 0.00005)
        
    # Zufällige Richtung (positiv oder negativ)
    direction = 1 if random.random() > 0.5 else -1
    variation = base_price * percent * direction
    
    return variation


def get_current_forex_price(symbol, add_variation=False):
    """
    Gibt den aktuellen Preis für das angegebene Währungspaar zurück
    add_variation=False, um exakt den von Yahoo Finance abgerufenen Preis zu verwenden
    """
    forex_data = get_forex_data_from_source()
    
    if symbol in forex_data:
        base_price = forex_data[symbol]
        if add_variation:
            # Füge minimale Variation hinzu, um "live" zu erscheinen
            variation = get_variation(base_price, symbol)
            return base_price + variation
        return base_price
    
    # Fallback für unbekannte Symbole
    return None