<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Envoy build

**Language:** English | [Deutsch](build.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Build path and host version

`make build-envoy` and `make check-config-envoy` use the selected `ext_proc` host path.

The authoritative host version is the version of the current prepared runtime or its pinned provisioning input. A documented version is not support for every distribution, ABI, or operating environment.

## Toolchain and dependencies

Use the host-appropriate C/C++ or Go toolchain, libmodsecurity dependencies, and a writable build/cache root outside the checkout. Compiler, flags, and host revision are recorded as build provenance; this guide makes no universal compiler or Go-version claim.

## Cache-v2 and provenance

Cache-v2 reuse is identity-bound. Source URL, revision or digest, patchset, architecture, compiler, and configuration decide whether an entry is reusable. A cache hit is not a runtime PASS.

## Build, configuration, and runtime

Run `make build-envoy` and then `make check-config-envoy`. Start and runtime smokes exist only for the target families that provide them; the selected core run is `make full-lifecycle-envoy`. A successful build or config check is not a rule-engine PASS.

## Optional profiles and troubleshooting

Compatibility, CRS, extended-matrix, H2/H3, and Strict profiles remain separate from the selected core. Before changing configuration, check executable paths, ABI, module/service load, writable runtime roots, and pinned source/patch inputs.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `ENVOY_BIN` | Optional | executable Envoy path | Provisioning or caller | `<component-cache>/envoy/bin/envoy` |
| `ENVOY_CONFIG` | Generated | absolute runtime YAML path | Harness | `<build-root>/envoy.yaml` |
| `EXT_PROC_PORT` | Optional | local TCP port number | Harness/caller | `18083` |
| `NO_CRS_RULES_FILE` | Required for canonical rule runs | absolute rules-file path | Make default or caller | `/etc/modsecurity/no-crs-baseline.conf` |

See the [central variables reference](../../configuration/variables.md).
