# Compile Lighttpd

## Purpose

This guide documents the repository-supported Lighttpd source-build and Phase 1
`sidecar_proxy` smoke path. Lighttpd is prepared from a pinned source tarball
and built locally under the common.sh-managed component cache. The current
runtime proof is a sidecar/proxy integration, not a native Lighttpd
ModSecurity module.

Use this file when you need to stage Lighttpd source, build the local runtime
binary, run the open-connector smokes, or locate Lighttpd evidence artifacts.

## Current Connector Status

- Connector: `connectors/lighttpd/`.
- Integration mode: `sidecar_proxy`.
- Local source build: PASS when `ALLOW_RUNTIME_BUILDS=1` is used with the
  pinned source.
- Simple runtime smoke: PASS when a local common.sh-managed Lighttpd binary is
  resolved.
- Targeted libmodsecurity smoke: PASS when local common.sh-managed
  libmodsecurity headers/libraries are available.
- Minimal CRS smoke: PASS when local common.sh-managed CRS and libmodsecurity
  are available.
- Secondary CRS smoke: PASS when local common.sh-managed CRS and
  libmodsecurity block the secondary CRS probe.
- Native Lighttpd module: not implemented.
- FastCGI/SCGI: not implemented.
- mod_magnet/Lua: not implemented.
- Production ready: false.
- Full matrix ready: false.
- CRS complete: false.
- Response body verified: false.

## What This Builds

- A pinned Lighttpd source tarball staged under `LIGHTTPD_COMPONENT_ROOT`.
- A local Lighttpd build workspace under `LIGHTTPD_COMPONENT_ROOT`.
- The final Lighttpd executable at `LIGHTTPD_BIN`.
- Local generated Lighttpd and sidecar smoke artifacts under the verified
  runtime roots.

It does not install Lighttpd globally, write system paths, require root, or
claim a native Lighttpd connector.

## Source / Version

The source of truth is
`modules/ModSecurity-test-Framework/ci/common.sh`.

| Variable | Current default |
| --- | --- |
| `LIGHTTPD_VERSION` | `1.4.84` |
| `LIGHTTPD_SOURCE_URL` | `https://download.lighttpd.net/lighttpd/releases-1.4.x/` |
| `LIGHTTPD_RELEASE_INDEX_URL` | `$LIGHTTPD_SOURCE_URL` |
| `LIGHTTPD_LATEST_URL` | `https://download.lighttpd.net/lighttpd/releases-1.4.x/latest.txt` |
| `LIGHTTPD_DOWNLOAD_URL` | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$LIGHTTPD_VERSION.tar.xz` |
| `LIGHTTPD_SHA256` | `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70` |
| `LIGHTTPD_SHA256_URL` | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$LIGHTTPD_VERSION.sha256sum` |
| `LIGHTTPD_COMPONENT_ROOT` | `$CONNECTOR_COMPONENT_CACHE/lighttpd` |
| `LIGHTTPD_BIN` | `$LIGHTTPD_COMPONENT_ROOT/bin/lighttpd` |

## Local Build / Runtime Paths

| Path | Meaning |
| --- | --- |
| `$LIGHTTPD_COMPONENT_ROOT` | Lighttpd source/build/install component root |
| `$LIGHTTPD_BIN` | Staged Lighttpd executable used by smokes |
| `$LIGHTTPD_RUNTIME_ROOT` | Lighttpd runtime smoke root |
| `$LIGHTTPD_CONFIG_ROOT` | Generated Lighttpd config root |
| `$LIGHTTPD_LOG_ROOT` | Lighttpd smoke and prepare logs |
| `$LIGHTTPD_RESULT_ROOT` | Lighttpd smoke result JSON |

The prepare helper also uses:

- `$LIGHTTPD_COMPONENT_ROOT/src/lighttpd-$LIGHTTPD_VERSION`
- `$LIGHTTPD_COMPONENT_ROOT/build/lighttpd-$LIGHTTPD_VERSION`
- `$LIGHTTPD_LOG_ROOT/prepare-runtime`

By default these roots are under
`${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified`. In
restricted sandboxes, prefer `TMPDIR=/tmp`.

## Prepare Source

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-lighttpd-runtime
```

This downloads the pinned source tarball only after explicit opt-in, verifies
the pinned SHA256, and stages source under `$LIGHTTPD_COMPONENT_ROOT/src`.
Without `ALLOW_RUNTIME_BUILDS=1`, it stops after source staging and reports
77/BLOCKED if no runtime binary is already available.

## Build Runtime Binary

Build from already staged source:

```sh
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime
```

Download and build in one command:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime
```

The convenience build target is also available:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
```

The build helper:

- builds only under `$LIGHTTPD_COMPONENT_ROOT`;
- writes no global installation files;
- uses no system install prefix;
- requires no root privileges;
- writes build logs under `$LIGHTTPD_LOG_ROOT/prepare-runtime`;
- stages the final binary at `$LIGHTTPD_BIN`.

## Smoke Commands

```sh
TMPDIR=/tmp make smoke-lighttpd
TMPDIR=/tmp make smoke-lighttpd-modsecurity
TMPDIR=/tmp make smoke-lighttpd-crs
TMPDIR=/tmp make smoke-lighttpd-crs-secondary
```

The secondary CRS target is available and selects
`CRS_SMOKE_CASE=secondary`. It is separate from the minimal CRS SQLi probe.

## Evidence

Typical evidence paths with `TMPDIR=/tmp`:

| Evidence | Path |
| --- | --- |
| Current result | `/tmp/ModSecurity-conector-verified/lighttpd-smoke/result.json` |
| Simple runtime result | `/tmp/ModSecurity-conector-verified/lighttpd-smoke/runtime-result.json` |
| Targeted ModSecurity result | `/tmp/ModSecurity-conector-verified/lighttpd-smoke/targeted-result.json` |
| Minimal CRS result | `/tmp/ModSecurity-conector-verified/lighttpd-smoke/crs-result.json` |
| Secondary CRS result | `/tmp/ModSecurity-conector-verified/lighttpd-smoke/crs-secondary-result.json` |
| Logs | `/tmp/ModSecurity-conector-verified/logs/lighttpd-smoke/` |

Variable equivalents:

- `$LIGHTTPD_RESULT_ROOT/result.json`
- `$LIGHTTPD_LOG_ROOT/`

Secondary CRS evidence includes `crs-secondary-decision.log`,
`crs-secondary-audit.log`, and `crs-secondary-request-transcript.jsonl`.

## Phase-1 Scope

- `sidecar_proxy` is Phase 1.
- This is not a native Lighttpd ModSecurity connector.
- Native module, FastCGI/SCGI, and mod_magnet/Lua paths remain later options.
- No production claim is made.
- No full-matrix claim is made.
- No CRS-complete claim is made.
- No response-body claim is made.

## Claims Not Allowed

Lighttpd Phase 1 evidence must not claim:

- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `response_body_verified=true`

`crs_secondary_smoke_verified=true` is allowed only when the secondary CRS
smoke has local CRS/libmodsecurity/runtime evidence and an observed CRS rule
ID/message.

## Troubleshooting

- Missing download opt-in: source staging exits 77/BLOCKED until
  `ALLOW_RUNTIME_DOWNLOADS=1` is set.
- Missing build opt-in: source may be staged, but building requires
  `ALLOW_RUNTIME_BUILDS=1`.
- Missing compiler: install or expose a local `cc`, `gcc`, or `clang`.
- Missing `make`: install or expose `make`.
- Missing build dependencies: check
  `$LIGHTTPD_LOG_ROOT/prepare-runtime/build-dependencies.missing`.
- SHA256 mismatch: the pinned source tarball is rejected; check
  `LIGHTTPD_SHA256`, `LIGHTTPD_SHA256_URL`, and the downloaded tarball.
- `$LIGHTTPD_BIN` missing: run the build target or set `LIGHTTPD_BIN` to an
  executable local common.sh-managed path.
- Read-only `/var/tmp`: run with `TMPDIR=/tmp`.
- Missing libmodsecurity dependencies: targeted and CRS smokes exit
  77/BLOCKED until local common.sh-managed headers and libraries are available.
- Missing CRS checkout: CRS smokes exit 77/BLOCKED; run the repository CRS
  preparation flow or stage CRS under common.sh-managed roots.
- Port conflict: rerun with a clean runtime root or adjust the smoke port
  environment if needed.

## Related Docs

- `connectors/lighttpd/README.md`
- `connectors/lighttpd/docs/architecture.md`
- `connectors/lighttpd/docs/validation.md`
- `common/docs/design.md`
- `reports/connector-parallel-runtime-smoke-plan.md`
