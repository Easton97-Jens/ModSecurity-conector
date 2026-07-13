# Envoy-Anschlusskabelbaum

**Sprache:** [English](README.md) | Deutsch

Status: C17-`ext_authz`-Dienst mit getrennten Start- und Runtime-Smokes.
Connector-Metadaten sind `minimal_runtime_smoke` / `connector-gap` für das Ziel
Nur Pfad für Anforderungsheader 200/403.

## Einstiegspunkte

- `serve_envoy_connector.sh` materialisiert eine konkrete Connector-Konfiguration und führt sie aus
  der gebaute Service im Vordergrund.
- `start_envoy_connector.sh` validiert Connector- und Envoy-Konfigurationen und startet beide
  Envoy und der Dienst überprüfen beide Prozesse und stoppen sie ohne Aufforderung.
- `run_envoy_connector_runtime.sh` validiert eine temporäre Envoy YAML-Konfiguration,
  startet einen lokalen Upstream, den Connector-Dienst und Envoy und überprüft dann einen
  erlaubt HTTP 200 und ein regelgestütztes HTTP 403 über `ext_authz`.
- `run_envoy_smoke.sh` ist der Framework-bezogene Kompatibilitätseinstiegspunkt für
  derselbe reale Connector-Laufzeitpfad.
- `envoy_smoke_helper.py` bietet nur den abhängigkeitsfreien Upstream und HTTP
  Sonde; Es trifft keine Sicherheitsentscheidungen.

Für den Laufzeitrauch sind `ENVOY_BIN` und der separat gebaute Connector erforderlich
Dienst. Fehlende Binärdateien geben Exit 77/BLOCKED zurück. Ungültige Konfiguration, früher Prozess
Exit, Anforderungsfehler, falscher Status oder fehlende Ereignisnachweise geben FAIL zurück.
Jeder gestartete Prozess wird bei Erfolg, Fehler oder Signal gestoppt.

Der Smoke zeichnet nur Metadaten-Entscheidungsereignisse auf und protokolliert keine Anfragen oder
Reaktionsorgane. `ext_authz` gilt nur für die Anforderungsphase; Überprüfung des Antworttextes
bleibt falsch.

Der Full-Lifecycle-Dispatcher verwendet den Laufzeiteinstiegspunkt `ext_authz` nicht wieder.
Es ruft `runtime-smoke-envoy-ext-proc` auf
`full-lifecycle-envoy-ext-proc`, der einen echten Envoy-Hörer startet, den Go
`ext_proc` CGo/Common-Dienst und ein lokaler Upstream. Der ausgewählte Dienst verwendet
eine echte Common/libmodsecurity-Transaktion pro ext_proc-Stream und schreibt Rohdaten
Gemeinsames JSONL unter dem Run-Root; seine Vervollständigung JSONL bleibt ergänzend.
Der Smoke überprüft das begrenzte Regel-/Aktionsverhalten von HTTP/1.1 P1/P2/P3/P4, einschließlich
Vom Host bestätigte Ablehnungs-, Umleitungs- und sichere Nur-Protokoll-Ergebnisse nach erfolgreichem gRPC
sendet. Dieser Connector-lokale Beweis wird nicht gefördert und kann nicht nachgewiesen werden
Reset-, Timeout-, HTTP/2-, Client-Byte-, Canonical-Result- oder Produktionsansprüche.
