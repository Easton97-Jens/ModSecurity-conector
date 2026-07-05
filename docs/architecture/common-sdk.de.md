# Common SDK

Envoy, Traefik und lighttpd besitzen lokale Common-SDK-Mapper-Gerüste für `msconnector_config`, `msconnector_request` und `msconnector_response`. Dies ist nur ein Structure-/Compile-Contract. Host-API-Glue, Runtime-Lifecycle, Build-Glue, Protokoll-/Frame-Handling, Event-Artefakt-Callsites und libmodsecurity-Transaktionsbesitz bleiben Connector-spezifische Arbeit. Diese Connectoren bleiben `not_verified` / `connector-gap`, bis echte Runtime-Evidence vorhanden ist.

## Generic mapper helper

The Common SDK includes `msconnector_generic_map_request()` and `msconnector_generic_map_response()` for starter connectors that already have connector-neutral request and response fields. Envoy, Traefik, and lighttpd use this helper through thin local adapters. The helper does not take ownership of headers or body bytes, does not log body payloads, and does not change their `not_verified` / `connector-gap` status.
The remaining starter connectors now avoid connector-local mapper source copies by aliasing their map entry points to the connector-neutral generic mapper; this keeps duplicated Host lookup, validation, and body metadata assignment in one Common implementation only.

Generic mapper callers must pass `hostname` as a NUL-terminated string when it is set; header value slices are never exposed as C-string hostnames. Nonzero body sizes require non-NULL body data and remain metadata-only unless the caller owns safe body bytes.
