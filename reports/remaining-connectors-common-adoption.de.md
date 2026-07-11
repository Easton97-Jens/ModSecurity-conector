# Archivierter Common-SDK-Adoptionsbericht vor der Host-Integration

**Sprache:** [English](remaining-connectors-common-adoption.md) | Deutsch

> **Historisches Archiv — kein aktueller Capability- oder Runtime-Bericht.**
>
> Dieses Dokument beschreibt die frühere Starter-only-Adoption. Seine Aussagen,
> dass Envoy, Traefik und lighttpd keine Host-Integration, keinen Common-Runtime-
> Lifecycle oder keine Event-Pfade hätten, sind abgelöst. Der nachfolgende Text
> darf nicht zur Klassifizierung aktueller Connector-Unterstützung oder Evidence
> verwendet werden.
>
> Die aktuellen Host-Grenzen und Evidence-Zustände werden aus
> `connectors/<name>/capabilities.json` in der
> [kanonischen Capability-Matrix](testing/generated/canonical/connector-capabilities.generated.de.md)
> erzeugt. Der zugehörige [No-CRS-Gesamtsnapshot](all-connectors-no-crs-baseline.de.md)
> ist die maßgebliche Sicht auf Ergebnisstatus; vorhandener Quellcode ist kein
> PASS.

Dieser Bericht erfasst Envoy, Traefik, lighttpd und den Repository-Template-Starter. Der Status bleibt bewusst **not_verified** / **connector-gap**: Die Änderung bereitet Common-SDK-Contracts und C-Standardprüfungen vor, behauptet aber keine Runtime-, CRS-, Produktions-, Full-Matrix- oder RESPONSE_BODY-Verifikation.

## Envoy

- Connector: `connectors/envoy`
- Current status: Bridge-Starter; native Envoy-SDK- und Runtime-Lifecycle-Anbindung fehlen.
- Common config mapping: `envoy_modsecurity_config_init()` initialisiert `msconnector_config`, ohne Defaults vor einem Merge anzuwenden.
- Request mapper status: Header-Alias auf `msconnector_generic_map_request`; es gab in diesem Baum keine vorherige connector-lokale Mapper-Implementierung; der PR vermeidet neue duplizierte Mapper-Quellen und delegiert gemeinsame Hostname-/Serveradress-Fallback-Logik an den Common Generic Mapper.
- Response mapper status: Header-Alias auf `msconnector_generic_map_response`; es gab in diesem Baum keine vorherige connector-lokale Mapper-Implementierung; der PR vermeidet neue duplizierte Mapper-Quellen; keine Body-Payloads werden geloggt.
- Decision/event status: Decision-Starter nutzt Common-Decision/Intervention; Event-JSONL bleibt Connector-Gap.
- C17 check status: durch `check-remaining-connectors-c17` abgedeckt; fehlende Header/Quellen liefern Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: Bridge-Selftest, künftige Envoy-API-Anbindung, Lifecycle, Build-Glue und Protokollhandling.
- Removed duplicate helpers: keine lokalen JSON-, Rule-ID-, Status-, Bool-, Phase4- oder Size-Parser-Duplikate.
- Remaining connector-gap work: Envoy-SDK-Typen, Callsites außerhalb der Mapper, libmodsecurity-Transaktionen, Runtime-Evidence, Event-Artefakte.

## Traefik

- Connector: `connectors/traefik`
- Current status: Decision-Service-Starter; keine Traefik-Plugin-/Traffic-Runtime-Anbindung.
- Common config mapping: `traefik_modsecurity_config_init()` initialisiert `msconnector_config`, ohne Defaults vor einem Merge anzuwenden.
- Request mapper status: Header-Alias auf `msconnector_generic_map_request`; es gab in diesem Baum keine vorherige connector-lokale Mapper-Implementierung; der PR vermeidet neue duplizierte Mapper-Quellen und delegiert Validierung an Common.
- Response mapper status: Header-Alias auf `msconnector_generic_map_response`; es gab in diesem Baum keine vorherige connector-lokale Mapper-Implementierung; der PR vermeidet neue duplizierte Mapper-Quellen und delegiert Validierung an Common.
- Decision/event status: Starter nutzt Common-Decision/Intervention; JSONL/Event-Ausgabe bleibt Connector-Gap.
- C17 check status: durch `check-remaining-connectors-c17` abgedeckt; fehlende Header/Quellen liefern Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: Decision-Service-Grenze, Runtime-Lifecycle, Build-Glue, künftiges Protokoll-/Frame-Handling.
- Removed duplicate helpers: keine lokalen JSON-, Rule-ID-, Sanitize-, Status-, Bool-, Phase4- oder Size-Parser-Duplikate.
- Remaining connector-gap work: Traefik-Middleware-Callsites, Body-Streaming-Policy, Runtime-Artefakte, libmodsecurity-Transaktionen.

## lighttpd

- Connector: `connectors/lighttpd`
- Current status: Decision-Service-Bridge-Starter; natives Modul und FastCGI/SCGI-Integration sind zurückgestellt.
- Common config mapping: `lighttpd_modsecurity_config_init()` initialisiert `msconnector_config`, ohne Defaults vor einem Merge anzuwenden.
- Request mapper status: Header-Alias auf `msconnector_generic_map_request`; es gab in diesem Baum keine vorherige connector-lokale Mapper-Implementierung; der PR vermeidet neue duplizierte Mapper-Quellen und delegiert Validierung an Common.
- Response mapper status: Header-Alias auf `msconnector_generic_map_response`; es gab in diesem Baum keine vorherige connector-lokale Mapper-Implementierung; der PR vermeidet neue duplizierte Mapper-Quellen und delegiert Validierung an Common.
- Decision/event status: Starter nutzt Common-Decision/Intervention; Event-/TestResult-Artefakte bleiben Connector-Gap.
- C17 check status: durch `check-remaining-connectors-c17` abgedeckt; fehlende Header/Quellen liefern Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: lighttpd-Modul-/FastCGI-/SCGI-Grenze, Runtime-Lifecycle, Build-Glue, Protokoll-/Frame-Handling.
- Removed duplicate helpers: keine lokalen JSON-, Rule-ID-, Sanitize-, Status-, Bool-, Phase4- oder Size-Parser-Duplikate.
- Remaining connector-gap work: echte lighttpd-Hooks, Request/Response-Callsites außerhalb der Mapper, libmodsecurity-Transaktionen, Runtime-Evidence.

## Template-Starter

`connectors/_template` bleibt reine Starter-Dokumentation und behauptet keine abgeschlossene Runtime-Fähigkeit.
