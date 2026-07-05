# traefik Connector

Dieser Connector ist Common-SDK-vorbereitet, bleibt aber bewusst `not_verified` / `connector-gap`.

- Common Config wird über `traefik_modsecurity_config_init()` auf `msconnector_config` initialisiert und mit Defaults versehen.
- Request- und Response-Mapper liegen unter `connectors/traefik/src/traefik_modsecurity_mapper.*` und validieren die Common Mapper Contracts auf Structure-/Compile-Ebene.
- Decisions verwenden Common-Modelle; Event-, TestResult- und Runtime-Artefakte bleiben bis zu echten Call-Sites Connector-Gap.
- Connector-spezifisch bleiben Host-API, Runtime-Lifecycle, Build-Glue sowie Protokoll-/Frame-Handling.
- Es gibt keine Produktions-, CRS-, Full-Matrix-, Runtime- oder RESPONSE_BODY-Verifikationsbehauptung.
