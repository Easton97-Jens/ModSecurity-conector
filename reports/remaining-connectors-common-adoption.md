# Remaining connectors Common SDK adoption report

This report covers Envoy, Traefik, lighttpd, and the repository template starter. The status is intentionally **not_verified** / **connector-gap**: the work prepares Common SDK contracts, the generic mapper helper, and C standard checks but does not claim runtime, CRS, production, full-matrix, or response-body verification.

## Envoy

- Connector: `connectors/envoy`
- Current status: bridge starter; native Envoy SDK and runtime lifecycle are absent.
- Common config mapping: `envoy_modsecurity_config_init()` initializes `msconnector_config`, applies defaults, and leaves directive parsing to future Envoy glue.
- Request mapper status: header alias to `msconnector_generic_map_request`; the duplicated Envoy mapper source was removed and Host fallback lives in Common.
- Response mapper status: header alias to `msconnector_generic_map_response`; the duplicated Envoy mapper source was removed and body payloads are not logged.
- Decision/event status: existing decision starter uses Common decision/intervention types; event JSONL remains connector-gap until a runtime callsite exists.
- C17 check status: covered by `check-remaining-connectors-c17`; missing source/header inputs return Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: bridge self-test, future Envoy API glue, lifecycle, build glue, and protocol handling.
- Removed duplicate helpers: no connector-local JSON escape, rule-id, status, bool, phase4, or size parser duplicate is retained.
- Remaining connector-gap work: Envoy SDK types, callsites outside mapper files, libmodsecurity transaction lifecycle, runtime evidence, and event artifact emission.

## Traefik

- Connector: `connectors/traefik`
- Current status: decision-service starter; no Traefik plugin/runtime traffic integration.
- Common config mapping: `traefik_modsecurity_config_init()` initializes and defaults `msconnector_config`.
- Request mapper status: header alias to `msconnector_generic_map_request`; the duplicated Traefik mapper source was removed and validation lives in Common.
- Response mapper status: header alias to `msconnector_generic_map_response`; the duplicated Traefik mapper source was removed and validation lives in Common.
- Decision/event status: existing starter uses Common decision/intervention types; JSONL/event output is documented as connector-gap.
- C17 check status: covered by `check-remaining-connectors-c17`; missing source/header inputs return Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: decision service API boundary, runtime lifecycle, build glue, and future protocol/frame handling.
- Removed duplicate helpers: no connector-local JSON escape, rule-id, sanitize, status, bool, phase4, or size parser duplicate is retained.
- Remaining connector-gap work: Traefik middleware callsites, body streaming policy, runtime artifacts, and libmodsecurity transaction lifecycle.

## lighttpd

- Connector: `connectors/lighttpd`
- Current status: decision-service bridge starter; native module and FastCGI/SCGI integration are deferred.
- Common config mapping: `lighttpd_modsecurity_config_init()` initializes and defaults `msconnector_config`.
- Request mapper status: header alias to `msconnector_generic_map_request`; the duplicated lighttpd mapper source was removed and validation lives in Common.
- Response mapper status: header alias to `msconnector_generic_map_response`; the duplicated lighttpd mapper source was removed and validation lives in Common.
- Decision/event status: starter uses Common decision/intervention types; event/test-result artifact output is connector-gap.
- C17 check status: covered by `check-remaining-connectors-c17`; missing source/header inputs return Exit 77.
- Runtime verification status: `runtime_status=not_verified`, `verification_status=connector-gap`.
- Kept connector-specific code: lighttpd module/FastCGI/SCGI boundary, runtime lifecycle, build glue, protocol/frame handling.
- Removed duplicate helpers: no connector-local JSON escape, rule-id, sanitize, status, bool, phase4, or size parser duplicate is retained.
- Remaining connector-gap work: real lighttpd hooks, request/response callsites outside mapper files, libmodsecurity transaction lifecycle, and runtime evidence.

## Template starter

`connectors/_template` remains starter-only documentation. It is captured as a starter scaffold and does not claim completed runtime capability.
