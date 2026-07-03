**Sprache:** [English](README.md) | Deutsch

# Apache-Connector

Status: Apache-adaptereigene Common-SDK-Adoption für Konfiguration,
Direktiven, Mapper-Contracts und metadata-only Events.

Der Apache-Connector bettet jetzt `msconnector_config` für
connector-neutrale Konfigurationswerte ein, nutzt Common-Direktivennamen und
Common-Parser für die übernommenen Direktiven und stellt Apache-eigene dünne
Mapper von `request_rec` zu `msconnector_request` sowie von Apache-Response-
Metadaten zu `msconnector_response` bereit. Die Mapper validieren gegen die
Common `request_mapper_contract`- und `response_mapper_contract`-Modelle.

Apache-spezifisch bleiben `command_rec`-Registrierung, `request_rec`-Zugriff,
Hooks, Filter, APR-Pools, Bucket Brigades, APLOG-Logging, Apache-Return-Codes
und APXS/autotools-Buildlogik.

Phase-4-Ereignisse verwenden den Common `msconnector_event`-/JSONL-Pfad für
Metadaten. Request- und Response-Body-Payloads werden nicht in diese Events
oder Logs geschrieben.

Diese Änderung behauptet keine Produktionsreife, keine CRS-Abdeckung, keine
Full-Matrix-Abdeckung und keine neue Runtime-Verifikation.
