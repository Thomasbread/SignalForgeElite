# Anleitung zum Deployment auf Streamlit Cloud

Um die Signal Forge Elite App auf Streamlit Cloud zu deployen, folgen Sie bitte diesen Schritten:

## Voraussetzungen

1. Ein GitHub-Account
2. Ein Streamlit-Account (registrieren unter https://share.streamlit.io)

## Schritte zum Deployment

1. **Uploaden Sie Ihren Code auf GitHub:**
   - Erstellen Sie ein neues Repository
   - Laden Sie alle Projektdateien hoch (achten Sie darauf, dass die .streamlit/config.toml Datei mit hochgeladen wird)

2. **Deployment auf Streamlit Cloud:**
   - Gehen Sie zu https://share.streamlit.io und melden Sie sich an
   - Klicken Sie auf "New app"
   - Wählen Sie Ihr GitHub-Repository und den Branch aus
   - Setzen Sie den Pfad zur Hauptdatei auf `app.py`
   - Klicken Sie auf "Deploy!"

3. **Wichtige Hinweise für das Deployment:**
   - Die App verwendet Port 8501 für Streamlit Cloud (dies ist in der .streamlit/config.toml Datei konfiguriert)
   - Alle Abhängigkeiten werden automatisch installiert
   - pyperclip ist optional und die App funktioniert auch ohne dieses Modul

## Fehlerbehebung

Falls der Fehler "connection refused" weiterhin auftritt:

1. Stellen Sie sicher, dass die Datei `.streamlit/config.toml` im Repository enthalten ist und mit deployt wurde
2. Überprüfen Sie, dass die Port-Einstellung auf 8501 steht
3. Versuchen Sie, die App neu zu deployen
4. Falls der Fehler bestehen bleibt, können Sie alternativ die `config.toml` Datei entfernen und Streamlit die Standard-Port-Konfiguration verwenden lassen

## Lokales Testen

Zum lokalen Testen können Sie weiterhin `streamlit run app.py` verwenden. Der Port wird dann automatisch durch die lokale Streamlit-Installation bestimmt.