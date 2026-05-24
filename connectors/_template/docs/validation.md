# Validation – Connector Template

## Grundsatz

Ein Strukturcheck allein reicht nicht aus. Ein Connector gilt erst dann als
technisch belastbar, wenn echte Runtime-Evidenz aus realen Serverläufen
vorliegt.

## Mindestanforderungen für Runtime-Validierung

Für einen neuen Connector sind mindestens folgende Nachweise erforderlich:

1. **Smoke-Test**
   - Basiskonfiguration lädt Connector und Regeln ohne offensichtliche
     Initialisierungsfehler.
2. **Start/Stop-Test**
   - Serverprozess startet/stopt reproduzierbar ohne hängende Listener.
3. **Request-Test**
   - Reale HTTP-Requests werden durch den Connectorpfad verarbeitet.
4. **Intervention-Test**
   - Block-/Allow-Verhalten ist für definierte Regeln nachweisbar.
5. **Logging-Test**
   - Relevante Logs (server/connector/audit/access) sind erzeugt und
     auswertbar.
6. **Report-Output**
   - Ergebnisberichte/JSON im erwarteten Schema sind vorhanden.

## Ergänzende Evidenz (noch zu prüfen)

- Verhalten bei Fehlkonfigurationen
- Verhalten bei größeren Bodies/Streaming
- Stabilität über mehrere Durchläufe
- Connector-spezifische Gap- und XFAIL-Einordnung

## Nicht ausreichend

- Nur Datei-/Ordner-Existenz
- Nur statische Lints ohne Runtime
- Nur behauptete Kompatibilität ohne reproduzierbare Logs/Reports
