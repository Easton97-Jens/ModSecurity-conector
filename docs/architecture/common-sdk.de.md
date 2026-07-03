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

## Globale Adapter-Contracts für neue Connectoren

Common stellt jetzt auch connector-neutrale Contracts für zukünftige Host-Adapter bereit:

- `directive_adapter`: ein deterministischer Directive-Adapter-Katalog aus `directive_spec`. Er liefert zukünftigen Adaptern kanonische Namen, Host-Namen, Scopes und Argument-Policies, ohne Host-Direktiventypen zu erzeugen.
- `request_mapper_contract`: die minimalen Request-Felder und Limits, die ein Host-Mapper erfüllen muss, wenn er einen Server-Request in `msconnector_request` überführt.
- `response_mapper_contract`: der entsprechende Response-Contract für `msconnector_response`, inklusive HTTP-Statusprüfung und Header-/Body-Limits.
- `crs`: eine neutrale CRS-/Ruleset-Setup-Konvention für deaktivierte, externe Pfad-, gebündelte Pfad- und Test-Fixture-Konfigurationen.

Diese Contracts sind nur globale SDK-Oberfläche. Sie migrieren keine NGINX-, Apache-, HAProxy-, Envoy-, lighttpd- oder Traefik-Runtime und behaupten keine CRS-Runtime-Verifikation, Produktionsreife oder Full-Matrix-Abdeckung.

Host-spezifische APIs bleiben im Connector-Code. Beispiele sind `ngx_command_t`, `ngx_http_request_t`, `ngx_chain_t`, Apache `command_rec`, Apache `request_rec`, APR-Pools, Bucket Brigades und Server-Hooks/-Filter. NGINX und Apache können später dünne Mapper auf diesen Contracts implementieren; diese SDK-Schicht behauptet aber nicht, dass sie das bereits tun.

## Apache-Adoptionsgrenze

Apache nutzt jetzt das Common SDK für die übernommene semantische Schicht:
eingebettetes `msconnector_config`, Common-Parser, Directive-Spec/Adapter-
Lookup, Request-/Response-Mapper-Contracts und metadata-only Event-JSONL-
Primitive. Apache behält Apache-Server-APIs wie `request_rec`, `command_rec`,
Hooks, Filter, APR-Pools, Bucket Brigades, APLOG, Return-Codes und APXS-
Buildlogik. Das ist keine Aussage zu Produktionsreife, CRS, Full-Matrix oder
Runtime-Verifikation.
