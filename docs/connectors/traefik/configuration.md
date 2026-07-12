<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Traefik configuration

**Language:** English | [Deutsch](configuration.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Configuration model

The selected path uses an EntryPoint, Router, native Middleware, and local engine service. `forwardAuth` remains a compatibility example.

## Minimal, Safe, and Strict

The [annotated Traefik examples](../../../examples/traefik/README.md) are the complete local source. Replace every path, port, and endpoint for the target host. Minimal and Safe belong to the documented core; Strict is described only where the host and current evidence support it. Do not copy a compatibility configuration as the selected core path.

## Defaults, body scope, and logging

Only existing host directives and harness options are listed in the examples. Body and content-type behavior remain host- and profile-bound; no configuration permits a connector-owned full response buffer. Use payload-free connector/evidence logs and keep secrets out of rules, paths, and command lines.

## Validation

Run `make check-config-traefik` before starting a host. The core run `make full-lifecycle-traefik` needs writable runtime and evidence roots; always inspect its artifacts for the result.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `TRAEFIK_BIN` | Optional | executable Traefik path | Provisioning or caller | `<component-cache>/traefik/bin/traefik` |
| `TRAEFIK_ENGINE_SERVICE_BUILD_DIR` | Optional | absolute build directory | Build script or caller | `<build-root>/traefik-engine-service` |
| `TRAEFIK_ENGINE_SERVICE_BIN` | Optional | absolute engine-service executable | Build script or caller | `<build-root>/traefik-engine-service/traefik-engine-service` |
| `TRAEFIK_CONNECTOR_CONFIG` | Optional | absolute connector configuration | Start-smoke harness or caller | `config/traefik-forwardauth.conf` |

See the [central variables reference](../../configuration/variables.md).
