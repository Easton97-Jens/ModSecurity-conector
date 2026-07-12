<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Traefik build

**Language:** English | [Deutsch](build.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Build path and host version

`make build-traefik` and `make check-config-traefik` prepare the native middleware path.

The authoritative host version is the version of the current prepared runtime or its pinned provisioning input. A documented version is not support for every distribution, ABI, or operating environment.

## Toolchain and dependencies

Use the host-appropriate C/C++ or Go toolchain, libmodsecurity dependencies, and a writable build/cache root outside the checkout. Compiler, flags, and host revision are recorded as build provenance; this guide makes no universal compiler or Go-version claim.

## Cache-v2 and provenance

Cache-v2 reuse is identity-bound. Source URL, revision or digest, patchset, architecture, compiler, and configuration decide whether an entry is reusable. A cache hit is not a runtime PASS.

## Build, configuration, and runtime

Run `make build-traefik` and then `make check-config-traefik`. Start and runtime smokes exist only for the target families that provide them; the selected core run is `make full-lifecycle-traefik`. A successful build or config check is not a rule-engine PASS.

## Optional profiles and troubleshooting

Compatibility, CRS, extended-matrix, H2/H3, and Strict profiles remain separate from the selected core. Before changing configuration, check executable paths, ABI, module/service load, writable runtime roots, and pinned source/patch inputs.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `TRAEFIK_BIN` | Optional | executable Traefik path | Provisioning or caller | `<component-cache>/traefik/bin/traefik` |
| `TRAEFIK_ENGINE_SERVICE_BUILD_DIR` | Optional | absolute build directory | Build script or caller | `<build-root>/traefik-engine-service` |
| `TRAEFIK_ENGINE_SERVICE_BIN` | Optional | absolute engine-service executable | Build script or caller | `<build-root>/traefik-engine-service/traefik-engine-service` |
| `TRAEFIK_CONNECTOR_CONFIG` | Optional | absolute connector configuration | Start-smoke harness or caller | `config/traefik-forwardauth.conf` |

See the [central variables reference](../../configuration/variables.md).
