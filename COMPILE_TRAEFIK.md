# Compile / Prepare Traefik

## Purpose

This guide documents the repository-supported Traefik runtime-prepare and smoke
path. Traefik is not compiled from source by this repository. The supported
flow downloads a pinned Traefik release archive, extracts the expected binary,
stages it into the common.sh-managed component cache, and then runs local
runtime evidence through the Traefik `forwardAuth` path.

Use this file when you need to prepare the Traefik runtime component, run the
open-connector smokes, or locate Traefik evidence artifacts.

## Current Connector Status

- Connector: `connectors/traefik/`.
- Integration mode: `forwardAuth`.
- Runtime component: pinned Traefik release archive containing the Traefik
  binary.
- Source compile: not performed by this repository.
- Simple runtime smoke: PASS when a local common.sh-managed Traefik binary is
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

- A pinned Traefik Linux amd64 release archive.
- The extracted Traefik binary under `TRAEFIK_COMPONENT_ROOT`.
- Local generated Traefik smoke configuration under `TRAEFIK_CONFIG_ROOT`.
- Runtime evidence under `TRAEFIK_RESULT_ROOT` and `TRAEFIK_LOG_ROOT`.

It does not build Traefik from source, install Traefik globally, or accept a
global `PATH` fallback as runtime proof.

## Source / Version

The source of truth is
`modules/ModSecurity-test-Framework/ci/common.sh`.

| Variable | Current default |
| --- | --- |
| `TRAEFIK_VERSION` | `3.7.5` |
| `TRAEFIK_SOURCE_URL` | `https://github.com/traefik/traefik/releases` |
| `TRAEFIK_INSTALL_DOCS_URL` | `https://doc.traefik.io/traefik/getting-started/install-traefik/` |
| `TRAEFIK_DOWNLOAD_URL` | `https://github.com/traefik/traefik/releases/download/v$TRAEFIK_VERSION/traefik_v${TRAEFIK_VERSION}_linux_amd64.tar.gz` |
| `TRAEFIK_SHA256` | `9da81a928fde965c2c4678698bbc28bc3f600223b14c32b35bd480bf5ec863dc` |
| `TRAEFIK_SHA256_URL` | `https://github.com/traefik/traefik/releases/download/v$TRAEFIK_VERSION/traefik_v${TRAEFIK_VERSION}_checksums.txt` |
| `TRAEFIK_COMPONENT_ROOT` | `$CONNECTOR_COMPONENT_CACHE/traefik` |
| `TRAEFIK_BIN` | `$TRAEFIK_COMPONENT_ROOT/bin/traefik` |

## Local Runtime Paths

| Path | Meaning |
| --- | --- |
| `$TRAEFIK_COMPONENT_ROOT` | Pinned Traefik runtime component cache |
| `$TRAEFIK_BIN` | Staged Traefik executable used by smokes |
| `$TRAEFIK_RUNTIME_ROOT` | Traefik runtime smoke root |
| `$TRAEFIK_CONFIG_ROOT` | Generated Traefik config root |
| `$TRAEFIK_LOG_ROOT` | Traefik smoke logs |
| `$TRAEFIK_RESULT_ROOT` | Traefik smoke result JSON |

By default these roots are under
`${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified`. In
restricted sandboxes, prefer `TMPDIR=/tmp`.

## Prepare Runtime Component

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
```

The prepare helper:

- downloads only after explicit `ALLOW_RUNTIME_DOWNLOADS=1`;
- verifies the pinned SHA256 before extraction;
- extracts only the expected `traefik` binary from the archive;
- writes only under `$CONNECTOR_COMPONENT_CACHE`;
- stages the binary at `$TRAEFIK_BIN`;
- does not install global files;
- rejects global system paths and global `PATH` fallback.

Without download opt-in, the target reports the expected binary path and exits
77/BLOCKED when the binary is not already staged.

## Smoke Commands

```sh
TMPDIR=/tmp make smoke-traefik
TMPDIR=/tmp make smoke-traefik-modsecurity
TMPDIR=/tmp make smoke-traefik-crs
TMPDIR=/tmp make smoke-traefik-crs-secondary
```

The secondary CRS target is available and selects
`CRS_SMOKE_CASE=secondary`. It is separate from the minimal CRS SQLi probe.

## Evidence

Typical evidence paths with `TMPDIR=/tmp`:

| Evidence | Path |
| --- | --- |
| Current result | `/tmp/ModSecurity-conector-verified/traefik-smoke/result.json` |
| Simple runtime result | `/tmp/ModSecurity-conector-verified/traefik-smoke/runtime-result.json` |
| Targeted ModSecurity result | `/tmp/ModSecurity-conector-verified/traefik-smoke/targeted-result.json` |
| Minimal CRS result | `/tmp/ModSecurity-conector-verified/traefik-smoke/crs-result.json` |
| Secondary CRS result | `/tmp/ModSecurity-conector-verified/traefik-smoke/crs-secondary-result.json` |
| Logs | `/tmp/ModSecurity-conector-verified/logs/traefik-smoke/` |

Variable equivalents:

- `$TRAEFIK_RESULT_ROOT/result.json`
- `$TRAEFIK_LOG_ROOT/`

Secondary CRS evidence includes `crs-secondary-decision.log` and
`crs-secondary-audit.log`.

## Claims Not Allowed

Traefik open-connector evidence must not claim:

- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `response_body_verified=true`

`crs_secondary_smoke_verified=true` is allowed only when the secondary CRS
smoke has local CRS/libmodsecurity/runtime evidence and an observed CRS rule
ID/message.

## Troubleshooting

- Missing binary: run `ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime`
  or set `TRAEFIK_BIN` to an executable local common.sh-managed path.
- Missing download opt-in: prepare exits 77/BLOCKED until
  `ALLOW_RUNTIME_DOWNLOADS=1` is set.
- SHA256 mismatch: the pinned archive is rejected; check `TRAEFIK_SHA256`,
  `TRAEFIK_SHA256_URL`, and the downloaded archive.
- Read-only `/var/tmp`: run with `TMPDIR=/tmp`.
- Missing libmodsecurity dependencies: targeted and CRS smokes exit
  77/BLOCKED until local common.sh-managed headers and libraries are available.
- Missing CRS checkout: CRS smokes exit 77/BLOCKED; run the repository CRS
  preparation flow or stage CRS under common.sh-managed roots.
- Port conflict: rerun with a clean runtime root or adjust the smoke port
  environment if needed.

## Related Docs

- `connectors/traefik/README.md`
- `connectors/traefik/docs/validation.md`
- `common/docs/design.md`
- `reports/connector-parallel-runtime-smoke-plan.md`
