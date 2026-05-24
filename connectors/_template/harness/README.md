# Harness – Connector Template

Dieses Verzeichnis beschreibt die erwartete Harness-Struktur für einen neuen
Connector. Es enthält absichtlich **keine** lauffähige Implementierung.

## Erwartete Hooks (noch zu implementieren)

- `prepare()`
- `start()`
- `stop()`
- `reload()` (falls vom Zielserver unterstützt)
- `apply_rules()`
- `materialize_case()`
- `send_request()`
- `collect_logs()`
- `summarize_results()`
- `cleanup()`

## Hinweise

- Die Hook-Semantik ist server-spezifisch auszugestalten.
- Jede Implementierung muss echte Runtime-Evidenz liefern.
- Fehlende Hooks oder eingeschränkte Serverfähigkeiten sind explizit als
  "noch zu prüfen" oder "unsupported" zu dokumentieren.
