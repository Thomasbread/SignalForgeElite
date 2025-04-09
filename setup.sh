#!/bin/bash

# Dieses Skript wird auf Streamlit Cloud während des Deployments ausgeführt
# Es hilft, Probleme mit Abhängigkeiten zu beheben

echo "Installiere Abhängigkeiten mit spezifischen Versionen..."
pip install matplotlib==3.7.1 numpy==1.24.3 pandas==2.0.3 plotly==5.15.0 requests==2.31.0 streamlit==1.24.0 trafilatura==1.6.0

echo "Setup abgeschlossen!"