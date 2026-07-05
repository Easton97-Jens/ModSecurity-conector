# Common SDK

Envoy, Traefik und lighttpd besitzen lokale Common-SDK-Mapper-Gerüste für `msconnector_config`, `msconnector_request` und `msconnector_response`. Dies ist nur ein Structure-/Compile-Contract. Host-API-Glue, Runtime-Lifecycle, Build-Glue, Protokoll-/Frame-Handling, Event-Artefakt-Callsites und libmodsecurity-Transaktionsbesitz bleiben Connector-spezifische Arbeit. Diese Connectoren bleiben `not_verified` / `connector-gap`, bis echte Runtime-Evidence vorhanden ist.
