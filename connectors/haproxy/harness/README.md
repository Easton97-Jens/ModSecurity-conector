# HAProxy Harness Scaffold

Dieses Verzeichnis beschreibt erwartete Harness-Aufgaben für einen zukünftigen
HAProxy-Connector. Es enthält keine Implementierung.

## Erwartete Aufgaben (noch zu prüfen)

- `prepare`: Voraussetzungen prüfen, Arbeitsverzeichnisse unter `BUILD_ROOT` vorbereiten
- `start`: HAProxy und ggf. Connector-Komponente starten
- `stop`: Prozesse sauber stoppen
- `send_request`: Reale Test-Requests ausführen
- `collect_logs`: Relevante Log-Artefakte sammeln
- `cleanup`: Laufzeitartefakte isolieren/entfernen

## Hinweis

Die konkrete Ausgestaltung ist server- und integrationsmodellabhängig und noch
zu prüfen.
