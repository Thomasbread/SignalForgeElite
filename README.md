# Signal Forge Elite

Die ultimative Signal-basierte Forex-Trading-Plattform, die Ihnen qualitativ hochwertige Handelssignale mit Einstiegspunkten, Stop-Loss und Take-Profit-Levels liefert.

## Installation und Start

### Benötigte Pakete
```
streamlit
numpy
pandas
plotly
requests
pyperclip (optional, wird für die Kopier-Funktionalität verwendet)
```

### Installation
```bash
pip install streamlit numpy pandas plotly requests
pip install pyperclip  # Optional
```

### Starten der App
```bash
streamlit run app.py
```

## Features

- **Echtzeit-Kursdaten**: Automatischer Abruf der aktuellen Marktpreise von Yahoo Finance
- **Trading-Signale**: Hochwertige Kauf- und Verkaufssignale basierend auf der "Profit Pulse Precision"-Strategie
- **Multiple Währungspaare**: Unterstützt traditionelle Forex-Paare und Kryptowährungen
- **Signalverlauf**: Speichert und zeigt die letzten 3 Tage an Signalen
- **Visualisierung**: Interaktive Kerzendiagramme mit klaren Einstiegs-, Stop-Loss- und Take-Profit-Markierungen
- **MT5-Integration**: Vorbereitet für die Integration mit MetaTrader 5 (in dieser Version simuliert)

## Hinweise

- Die App ist für Deployment auf Streamlit Cloud optimiert und läuft auch lokal einwandfrei
- Die Signalgenerierung ist bewusst sehr selektiv, um nur qualitativ hochwertige Signale zu liefern
- Alle Kurse werden von Yahoo Finance abgerufen, um die höchste Genauigkeit zu gewährleisten

## Haftungsausschluss

Diese Anwendung bietet keine Finanzberatung. Der Handel birgt Risiken.