#!/bin/bash

# Dieses Skript wird auf Streamlit Cloud während des Deployments ausgeführt
# Es hilft, Probleme mit Abhängigkeiten zu beheben

echo "Installiere Abhängigkeiten..."
pip install matplotlib numpy pandas plotly requests streamlit trafilatura

# Versuche, pyperclip zu installieren, aber ignoriere Fehler
echo "Versuche pyperclip zu installieren (optional)..."
pip install pyperclip || echo "pyperclip konnte nicht installiert werden, aber das ist in Ordnung."

echo "Setup abgeschlossen!"