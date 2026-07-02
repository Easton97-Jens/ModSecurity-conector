**Sprache:** [English](common-sdk.md) | Deutsch

# Common-Connector-SDK-Scaffolding

`common/` enthält connector-neutrale C-Modelle und Hilfsfunktionen für spätere Integrationen. Diese APIs ändern keine Laufzeitpfade von NGINX, Apache, HAProxy, Envoy, Traefik oder lighttpd und behaupten keine Produktionsreife.

## Module und Infrastruktur

Das SDK enthält gemeinsame Metadaten für Konfiguration, Header, HTTP-Status, Entscheidungen, Fehler, Ereignisse, JSONL-Ereigniszeilen, Adapter, Adapter-Verträge, Capability-Test-Zuordnung, Artefaktlayout und Laufzeitpfade. Die Helfer sind nur Common-SDK-Infrastruktur.

## Header-Richtlinie

Header-Helfer suchen case-insensitiv, entfernen führende optionale Leerzeichen bei Content-Type-Vergleichen, lehnen ungültige Suffixe ab und kombinieren Set-Cookie, Cookie, Content-Length und Host nicht blind per Komma. Log-Sanitizing ersetzt Steuerzeichen; es ist keine Redaktion.

## Ereignis- und JSONL-Modell

Das Ereignismodell ist connector-neutrale Metadaten. Es enthält keine Request- oder Response-Bodies. JSONL-Helfer schreiben eine einzelne Ereigniszeile und melden Trunkierung sichtbar.

## Artefakte und Pfade

Das Artefaktlayout definiert Namen wie `result.json`, `decision.jsonl`, `audit.log` und `error.log`. Laufzeitpfad-Helfer lehnen absolute Namen, Windows-absolute/UNC-Namen und Parent-Traversal ab.

## Integrationsstatus

Connector-Integration ist zukünftige Arbeit. Diese Dokumentation behauptet keine Connector-Fähigkeit, keine Laufzeitunterstützung, keine Full-Matrix-Bereitschaft und keine Produktionsreife.

## Weitere Paket-Helfer

Das Common-SDK-Paket enthält jetzt außerdem Konfigurationsparser,
Request-/Response-Validierung, Rule-Collection-Merge-Helfer,
Rule-Error-/Event-Helfer, Test-Result-JSON, Connector-Manifeste,
Runtime-Report-Skelette, Origin-Governance, Build-Contract-Targets,
C++-Header-Wrapper, zentrale Ressourcenlimits, Rule-ID-Extraktion,
Log-Sanitizing und Body-Snippet-Redaktion. Diese Bausteine sind nur
connector-neutrales Scaffolding und migrieren oder verifizieren keinen
Connector. Sie fügen keine echte libmodsecurity-Bindung hinzu und behaupten
keine Produktionsreife oder Full-Matrix-Bereitschaft.
