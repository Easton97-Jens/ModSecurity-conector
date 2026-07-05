# Common-SDK-Adoptionsbericht für restliche Connectoren

Dieser Bericht erfasst Envoy, Traefik, lighttpd und den Repository-Template-Starter. Der Status bleibt bewusst **not_verified** / **connector-gap**: Die Änderung bereitet Common-SDK-Contracts und C-Standardprüfungen vor, behauptet aber keine Runtime-, CRS-, Produktions-, Full-Matrix- oder RESPONSE_BODY-Verifikation.

## Envoy

- Connector: `connectors/envoy`
- Current status: Bridge-Starter; native Envoy-SDK- und Runtime-Lifecycle-Anbindung fehlen.
- Common config mapping: `envoy_modsecurity_config_init()` initialisiert `msconnector_config` und setzt Defaults.
- Request mapper status: `envoy_modsecurity_map_request()` mappt Starter-Felder nach `msconnector_request` mit Host-Header-Priorität.
- Response mapper status: `envoy_modsecurity_map_response()` mappt Response-Metadaten nach `msconnector_response`; keine Body-Payloads werden geloggt.
- Decision/event status: Decision-Starter nutzt Common-Decision/Intervention; Event-JSONL bleibt Connector-Gap.
- C17 check status: durch `check-remaining-connectors-c17` abgedeckt; fehlende Header/Quellen liefern Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: Bridge-Selftest, künftige Envoy-API-Anbindung, Lifecycle, Build-Glue und Protokollhandling.
- Removed duplicate helpers: keine lokalen JSON-, Rule-ID-, Status-, Bool-, Phase4- oder Size-Parser-Duplikate.
- Remaining connector-gap work: Envoy-SDK-Typen, Callsites außerhalb der Mapper, libmodsecurity-Transaktionen, Runtime-Evidence, Event-Artefakte.

## Traefik

- Connector: `connectors/traefik`
- Current status: Decision-Service-Starter; keine Traefik-Plugin-/Traffic-Runtime-Anbindung.
- Common config mapping: `traefik_modsecurity_config_init()` initialisiert und defaultet `msconnector_config`.
- Request mapper status: `traefik_modsecurity_map_request()` mappt Starter-Fixture-Felder nach `msconnector_request` und validiert den Contract.
- Response mapper status: `traefik_modsecurity_map_response()` mappt Starter-Response-Felder nach `msconnector_response` und validiert den Contract.
- Decision/event status: Starter nutzt Common-Decision/Intervention; JSONL/Event-Ausgabe bleibt Connector-Gap.
- C17 check status: durch `check-remaining-connectors-c17` abgedeckt; fehlende Header/Quellen liefern Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: Decision-Service-Grenze, Runtime-Lifecycle, Build-Glue, künftiges Protokoll-/Frame-Handling.
- Removed duplicate helpers: keine lokalen JSON-, Rule-ID-, Sanitize-, Status-, Bool-, Phase4- oder Size-Parser-Duplikate.
- Remaining connector-gap work: Traefik-Middleware-Callsites, Body-Streaming-Policy, Runtime-Artefakte, libmodsecurity-Transaktionen.

## lighttpd

- Connector: `connectors/lighttpd`
- Current status: Decision-Service-Bridge-Starter; natives Modul und FastCGI/SCGI-Integration sind zurückgestellt.
- Common config mapping: `lighttpd_modsecurity_config_init()` initialisiert und defaultet `msconnector_config`.
- Request mapper status: `lighttpd_modsecurity_map_request()` mappt Starter-Fixture-Felder nach `msconnector_request` und validiert den Contract.
- Response mapper status: `lighttpd_modsecurity_map_response()` mappt Starter-Response-Felder nach `msconnector_response` und validiert den Contract.
- Decision/event status: Starter nutzt Common-Decision/Intervention; Event-/TestResult-Artefakte bleiben Connector-Gap.
- C17 check status: durch `check-remaining-connectors-c17` abgedeckt; fehlende Header/Quellen liefern Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: lighttpd-Modul-/FastCGI-/SCGI-Grenze, Runtime-Lifecycle, Build-Glue, Protokoll-/Frame-Handling.
- Removed duplicate helpers: keine lokalen JSON-, Rule-ID-, Sanitize-, Status-, Bool-, Phase4- oder Size-Parser-Duplikate.
- Remaining connector-gap work: echte lighttpd-Hooks, Request/Response-Callsites außerhalb der Mapper, libmodsecurity-Transaktionen, Runtime-Evidence.

## Template-Starter

`connectors/_template` bleibt reine Starter-Dokumentation und behauptet keine abgeschlossene Runtime-Fähigkeit.
