# Compile / Prepare Open Connectors

## Purpose

This guide is the shared local preparation entry point for the open connector
runtime components:

- Envoy
- Traefik
- Lighttpd

Envoy and Traefik are runtime-staged, not source-compiled. Lighttpd is built
locally from a pinned source tarball. All three use common.sh-managed runtime
roots and evidence contracts.

## Common Runtime Rules

- `modules/ModSecurity-test-Framework/ci/common.sh` is the source of truth for
  versions, URLs, checksums, component roots, binary paths, runtime roots, log
  roots, and result roots.
- Runtime components are not installed globally.
- Downloads require explicit `ALLOW_RUNTIME_DOWNLOADS=1`.
- Builds require explicit `ALLOW_RUNTIME_BUILDS=1`.
- Staging stays under `$CONNECTOR_COMPONENT_CACHE`.
- Runtime evidence is written under `$VERIFIED_RUN_ROOT` or a
  `TMPDIR=/tmp` verified root.
- Global system paths and global `PATH` fallbacks are rejected for runtime
  proof.
- Missing dependencies should produce Exit 77/BLOCKED evidence, not synthetic
  PASS rows.

## Full Local Preparation

```sh
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
```

Envoy stages a pinned runtime binary. Traefik stages the expected binary from a
pinned release archive. Lighttpd stages pinned source and builds a local binary
under `$LIGHTTPD_COMPONENT_ROOT`.

## Simple Runtime Smokes

```sh
TMPDIR=/tmp make smoke-envoy
TMPDIR=/tmp make smoke-traefik
TMPDIR=/tmp make smoke-lighttpd
```

## Targeted ModSecurity Smokes

```sh
TMPDIR=/tmp make smoke-envoy-modsecurity
TMPDIR=/tmp make smoke-traefik-modsecurity
TMPDIR=/tmp make smoke-lighttpd-modsecurity
```

These use the targeted local libmodsecurity rule `1000001`. They do not prove
CRS completeness.

## Minimal CRS Smokes

```sh
TMPDIR=/tmp make smoke-envoy-crs
TMPDIR=/tmp make smoke-traefik-crs
TMPDIR=/tmp make smoke-lighttpd-crs
TMPDIR=/tmp make smoke-open-connectors-crs
```

The minimal CRS smoke uses the existing SQLi anomaly probe and may set
`crs_minimal_smoke_verified=true` only with local CRS/libmodsecurity/runtime
evidence.

## Secondary CRS Smokes

```sh
TMPDIR=/tmp make smoke-envoy-crs-secondary
TMPDIR=/tmp make smoke-traefik-crs-secondary
TMPDIR=/tmp make smoke-lighttpd-crs-secondary
TMPDIR=/tmp make smoke-open-connectors-crs-secondary
```

The secondary CRS smoke is available. It uses `CRS_SMOKE_CASE=secondary` and a
separate XSS probe. It may set `crs_secondary_smoke_verified=true` only with
local CRS/libmodsecurity/runtime evidence and an observed CRS rule ID/message.

## Status Matrix

| Connector | Prepare | Build | Runtime Smoke | ModSecurity Smoke | Minimal CRS Smoke | Secondary CRS Smoke | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Envoy | PASS: pinned binary staging target available | Not applicable; no source compile | PASS | PASS | PASS | PASS | `ext_authz`; runtime binary only |
| Traefik | PASS: pinned release archive staging target available | Not applicable; no source compile | PASS | PASS | PASS | PASS | `forwardAuth`; release archive extraction only |
| Lighttpd | PASS: pinned source staging target available | PASS: local source build with opt-in | PASS | PASS | PASS | PASS | Phase 1 `sidecar_proxy`, not native module |

PASS means the repository target exists and has local evidence when required
runtime dependencies are present. It does not mean production readiness.

## Evidence Roots

With `TMPDIR=/tmp`, typical result and log roots are:

| Connector | Result root | Log root |
| --- | --- | --- |
| Envoy | `/tmp/ModSecurity-conector-verified/envoy-smoke/` | `/tmp/ModSecurity-conector-verified/logs/envoy-smoke/` |
| Traefik | `/tmp/ModSecurity-conector-verified/traefik-smoke/` | `/tmp/ModSecurity-conector-verified/logs/traefik-smoke/` |
| Lighttpd | `/tmp/ModSecurity-conector-verified/lighttpd-smoke/` | `/tmp/ModSecurity-conector-verified/logs/lighttpd-smoke/` |

Inventory can be inspected with:

```sh
TMPDIR=/tmp make runtime-components-inventory
TMPDIR=/tmp make runtime-components-sources
```

## Claims Not Allowed

Open connector evidence must not claim:

- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `response_body_verified=true`

Lighttpd Phase 1 evidence must also not claim a native Lighttpd module.

## Per-Connector Guides

- `COMPILE_ENVOY.md`
- `COMPILE_TRAEFIK.md`
- `COMPILE_LIGHTTPD.md`
