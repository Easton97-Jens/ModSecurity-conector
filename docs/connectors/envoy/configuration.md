<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Envoy configuration

**Language:** English | [Deutsch](configuration.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Configuration model

The selected configuration streams request and response processing through an `ext_proc` gRPC service. `ext_authz` is kept only as a compatibility example.

## Minimal, Safe, and Strict

The [annotated Envoy examples](../../../examples/envoy/README.md) are the complete local source. Replace every path, port, and endpoint for the target host. Minimal and Safe belong to the documented core; Strict is described only where the host and current evidence support it. Do not copy a compatibility configuration as the selected core path.

## Defaults, body scope, and logging

Only existing host directives and harness options are listed in the examples. Body and content-type behavior remain host- and profile-bound; no configuration permits a connector-owned full response buffer. Use payload-free connector/evidence logs and keep secrets out of rules, paths, and command lines.

## Validation

Run `make check-config-envoy` before starting a host. The core run `make full-lifecycle-envoy` needs writable runtime and evidence roots; always inspect its artifacts for the result.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `ENVOY_BIN` | Optional | executable Envoy path | Provisioning or caller | `<component-cache>/envoy/bin/envoy` |
| `ENVOY_CONFIG` | Generated | absolute runtime YAML path | Harness | `<build-root>/envoy.yaml` |
| `EXT_PROC_PORT` | Optional | local TCP port number | Harness/caller | `18083` |
| `NO_CRS_RULES_FILE` | Required for canonical rule runs | absolute rules-file path | Make default or caller | `/etc/modsecurity/no-crs-baseline.conf` |

See the [central variables reference](../../configuration/variables.md).
