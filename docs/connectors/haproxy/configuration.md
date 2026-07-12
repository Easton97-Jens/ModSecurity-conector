<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# HAProxy configuration

**Language:** English | [Deutsch](configuration.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Configuration model

The selected full-lifecycle path is the native HTX filter. It is not the historical SPOE/SPOP compatibility example.

## Minimal, Safe, and Strict

The [annotated HAProxy examples](../../../examples/haproxy/README.md) are the complete local source. Replace every path, port, and endpoint for the target host. Minimal and Safe belong to the documented core; Strict is described only where the host and current evidence support it. Do not copy a compatibility configuration as the selected core path.

## Defaults, body scope, and logging

Only existing host directives and harness options are listed in the examples. Body and content-type behavior remain host- and profile-bound; no configuration permits a connector-owned full response buffer. Use payload-free connector/evidence logs and keep secrets out of rules, paths, and command lines.

## Validation

Run `make check-config-haproxy` before starting a host. The core run `make full-lifecycle-haproxy` needs writable runtime and evidence roots; always inspect its artifacts for the result.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `HAPROXY_VERSION` | Optional | selected host version | Framework/provider pin or caller | `the current provider pin` |
| `HAPROXY_SOURCE_URL` | Optional | HTTPS archive URL | Framework/provider pin or caller | `pinned source URL` |
| `HAPROXY_SHA256` | Optional | 64-character SHA-256 | Framework/provider pin or caller | `pinned digest` |
| `HAPROXY_RUNTIME_BUILD_DIR` | Optional | absolute build directory | Provisioning | `<build-root>/haproxy-runtime` |

See the [central variables reference](../../configuration/variables.md).
