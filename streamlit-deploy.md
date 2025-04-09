# Anleitung zum Deployment auf Streamlit Cloud

Um die Signal Forge Elite App auf Streamlit Cloud zu deployen, folgen Sie bitte diesen Schritten:

## Voraussetzungen

1. Ein GitHub-Account
2. Ein Streamlit-Account (registrieren unter https://share.streamlit.io)

## Schritte zum Deployment

1. **Uploaden Sie Ihren Code auf GitHub:**
   - Erstellen Sie ein neues Repository
   - Laden Sie alle Projektdateien hoch

2. **Deployment auf Streamlit Cloud:**
   - Gehen Sie zu https://share.streamlit.io und melden Sie sich an
   - Klicken Sie auf "New app"
   - Wählen Sie Ihr GitHub-Repository und den Branch aus
   - Setzen Sie den Pfad zur Hauptdatei auf `app.py`
   - **Wichtig:** Unter "Advanced Settings" → "Python Version" wählen Sie "3.11"
   - Klicken Sie auf "Deploy!"

3. **Wichtige Hinweise für das Deployment:**
   - Die App enthält bereits eine `setup.sh` Datei, die bei der Installation der Abhängigkeiten hilft
   - pyperclip ist optional und die App funktioniert auch ohne dieses Modul
   - Falls das Deployment fehlschlägt, können Sie die Konfiguration weiter anpassen

## Fehlerbehebung bei "installer returned a non-zero exit code"

Wenn Sie den Fehler "installer returned a non-zero exit code" erhalten:

1. **Methode 1: Ohne .streamlit/config.toml deployen**
   - Entfernen Sie die .streamlit/config.toml und .streamlit/secrets.toml Dateien aus Ihrem Repository
   - Deployen Sie erneut - Streamlit Cloud wählt dann automatisch die Standard-Port-Konfiguration

2. **Methode 2: requirements.txt anpassen**
   - Erstellen Sie eine einfache requirements.txt mit nur den essentiellen Paketen:
     ```
     matplotlib
     numpy
     pandas
     plotly
     requests
     streamlit==1.32.0
     trafilatura
     ```
   - Entfernen Sie pyperclip aus der Liste

3. **Methode 3: Andere Python-Version wählen**
   - Versuchen Sie es mit Python 3.10 statt 3.11 in den Advanced Settings

## Lokales Testen

Zum lokalen Testen können Sie weiterhin `streamlit run app.py` verwenden. Der Port wird dann automatisch durch die lokale Streamlit-Installation bestimmt.