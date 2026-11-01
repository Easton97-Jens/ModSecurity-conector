# Envoy source

**Language:** English | [Deutsch](README.de.md)

The C `ext_authz` service and the separate Go `ext_proc` service are distinct
connector profiles. Source presence and compilation are not host runtime proof.

- `envoy_ext_authz_service_main.c` selects the connector-owned host profile and
  the shared HTTP authorization service in `common/runtime/`.
- `envoy_modsecurity_mapper.h` / `.c` adapt request, response and configuration
  metadata to the Common mapper contracts.
- `envoy_bridge.h` / `.c` retain the historical local decision model.
- `envoy_bridge_main.c` provides the starter metadata command `--describe`.

The bridge starter does not call Envoy or libmodsecurity. Its regression
assertions now belong to the pinned Framework under
`connector_native_tests/connectors/envoy/src/envoy_bridge.inc`. Run them from the
Connector root with `make -C connectors/envoy self-test ON_DEMAND_TESTS=1`.
The starter binary no longer accepts `--self-test`; this does not expand default
selection or claim hosted enforcement.

Production launchers remain Connector-owned under `../scripts/`:
`serve_envoy_connector.sh` and `serve_envoy_ext_proc.sh`. Supply an explicit
product `RULES_FILE` or `MSCONNECTOR_RULES_FILE` to configuration/serve commands;
`serve-envoy-ext-proc` also accepts `EXT_PROC_RULES_FILE`. Product configuration
has no implicit Framework fixture fallback. Named smoke targets select their
Framework rules explicitly and their harnesses live under
`connector_suite/adapters/envoy/` in the Framework. Test outputs must be external.
