# Compile / Prepare Envoy

## Purpose

This guide documents the repository-supported Envoy runtime-prepare and smoke
path. Envoy is not compiled from source by this repository. The supported flow
stages a pinned Envoy runtime binary into the common.sh-managed component cache
and then runs local runtime evidence through the Envoy `ext_authz` path.

Use this file when you need to prepare the Envoy runtime component, run the
open-connector smokes, or locate Envoy evidence artifacts.

## Current Connector Status

- Connector: `connectors/envoy/`.
- Integration mode: `ext_authz`.
- Runtime component: pinned Envoy binary.
- Source compile: not performed by this repository.
- Simple runtime smoke: PASS when a local common.sh-managed Envoy binary is
  resolved.
- Targeted libmodsecurity smoke: PASS when local common.sh-managed
  libmodsecurity headers/libraries are available.
- Minimal CRS smoke: PASS when local common.sh-managed CRS and libmodsecurity
  are available.
- Secondary CRS smoke: PASS when local common.sh-managed CRS and
  libmodsecurity block the secondary CRS probe.
- Production ready: false.
- Full matrix ready: false.
- CRS complete: false.
- Response body verified: false.

## What This Prepares

- A pinned Envoy Linux x86_64 runtime binary under `ENVOY_COMPONENT_ROOT`.
- Local generated Envoy smoke configuration under `ENVOY_CONFIG_ROOT`.
- Runtime evidence under `ENVOY_RESULT_ROOT` and `ENVOY_LOG_ROOT`.

It does not build Envoy from source, install Envoy globally, or accept a global
`PATH` fallback as runtime proof.

## Source / Version

The source of truth is
`modules/ModSecurity-test-Framework/ci/common.sh`.

| Variable | Current default |
| --- | --- |
| `ENVOY_VERSION` | `1.38.2` |
| `ENVOY_SOURCE_URL` | `https://github.com/envoyproxy/envoy/releases` |
| `ENVOY_INSTALL_DOCS_URL` | `https://www.envoyproxy.io/docs/envoy/latest/start/install` |
| `ENVOY_DOWNLOAD_URL` | `https://github.com/envoyproxy/envoy/releases/download/v$ENVOY_VERSION/envoy-$ENVOY_VERSION-linux-x86_64` |
| `ENVOY_SHA256` | `87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899` |
| `ENVOY_SHA256_URL` | `https://github.com/envoyproxy/envoy/releases/download/v$ENVOY_VERSION/checksums.txt.asc` |
| `ENVOY_COMPONENT_ROOT` | `$CONNECTOR_COMPONENT_CACHE/envoy` |
| `ENVOY_BIN` | `$ENVOY_COMPONENT_ROOT/bin/envoy` |

## Local Runtime Paths

| Path | Meaning |
| --- | --- |
| `$ENVOY_COMPONENT_ROOT` | Pinned Envoy runtime component cache |
| `$ENVOY_BIN` | Staged Envoy executable used by smokes |
| `$ENVOY_RUNTIME_ROOT` | Envoy runtime smoke root |
| `$ENVOY_CONFIG_ROOT` | Generated Envoy config root |
| `$ENVOY_LOG_ROOT` | Envoy smoke logs |
| `$ENVOY_RESULT_ROOT` | Envoy smoke result JSON |

By default these roots are under
`${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified`. In
restricted sandboxes, prefer `TMPDIR=/tmp`.

## Prepare Runtime Component

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
```

The prepare helper:

- downloads only after explicit `ALLOW_RUNTIME_DOWNLOADS=1`;
- verifies the pinned SHA256 before staging;
- writes only under `$CONNECTOR_COMPONENT_CACHE`;
- stages the binary at `$ENVOY_BIN`;
- does not install global files;
- rejects global system paths and global `PATH` fallback.

Without download opt-in, the target reports the expected binary path and exits
77/BLOCKED when the binary is not already staged.

## Smoke Commands

```sh
TMPDIR=/tmp make smoke-envoy
TMPDIR=/tmp make smoke-envoy-modsecurity
TMPDIR=/tmp make smoke-envoy-crs
TMPDIR=/tmp make smoke-envoy-crs-secondary
```

The secondary CRS target is available and selects
`CRS_SMOKE_CASE=secondary`. It is separate from the minimal CRS SQLi probe.

## Evidence

Typical evidence paths with `TMPDIR=/tmp`:

| Evidence | Path |
| --- | --- |
| Current result | `/tmp/ModSecurity-conector-verified/envoy-smoke/result.json` |
| Simple runtime result | `/tmp/ModSecurity-conector-verified/envoy-smoke/runtime-result.json` |
| Targeted ModSecurity result | `/tmp/ModSecurity-conector-verified/envoy-smoke/targeted-result.json` |
| Minimal CRS result | `/tmp/ModSecurity-conector-verified/envoy-smoke/crs-result.json` |
| Secondary CRS result | `/tmp/ModSecurity-conector-verified/envoy-smoke/crs-secondary-result.json` |
| Logs | `/tmp/ModSecurity-conector-verified/logs/envoy-smoke/` |

Variable equivalents:

- `$ENVOY_RESULT_ROOT/result.json`
- `$ENVOY_LOG_ROOT/`

Secondary CRS evidence includes `crs-secondary-decision.log` and
`crs-secondary-audit.log`.

## Claims Not Allowed

Envoy open-connector evidence must not claim:

- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `response_body_verified=true`

`crs_secondary_smoke_verified=true` is allowed only when the secondary CRS
smoke has local CRS/libmodsecurity/runtime evidence and an observed CRS rule
ID/message.

## Troubleshooting

- Missing binary: run `ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime` or
  set `ENVOY_BIN` to an executable local common.sh-managed path.
- Missing download opt-in: prepare exits 77/BLOCKED until
  `ALLOW_RUNTIME_DOWNLOADS=1` is set.
- SHA256 mismatch: the pinned artifact is rejected; check `ENVOY_SHA256`,
  `ENVOY_SHA256_URL`, and the downloaded artifact.
- Read-only `/var/tmp`: run with `TMPDIR=/tmp`.
- Missing libmodsecurity dependencies: targeted and CRS smokes exit
  77/BLOCKED until local common.sh-managed headers and libraries are available.
- Missing CRS checkout: CRS smokes exit 77/BLOCKED; run the repository CRS
  preparation flow or stage CRS under common.sh-managed roots.
- Port conflict: rerun with a clean runtime root or adjust the smoke port
  environment if needed.

## Related Docs

- `connectors/envoy/README.md`
- `connectors/envoy/docs/validation.md`
- `common/docs/design.md`
- `reports/connector-parallel-runtime-smoke-plan.md`
