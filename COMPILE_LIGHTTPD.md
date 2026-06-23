# Compile Lighttpd

## Purpose

Document the repository-supported build or prepare path for Lighttpd without adding unverified production claims. This guide is operator-facing and ties every build, runtime, and smoke statement to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Open connector runtime path under `connectors/lighttpd/` using Phase 1 `sidecar_proxy`. Lighttpd is built locally from a pinned source tarball when runtime builds are allowed. There is no native Lighttpd ModSecurity connector. Production ready, full matrix ready, CRS complete, and response-body verified are all false.

## What This Builds / Prepares

a pinned Lighttpd source tarball/build/install under the component cache and generated sidecar_proxy smoke artifacts.

## What This Does Not Prove

This does not prove a native Lighttpd module, FastCGI/SCGI/mod_magnet/Lua integration, production readiness, full CRS coverage, full matrix coverage, or response-body support. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/lighttpd/src/`, `connectors/lighttpd/harness/`, `connectors/lighttpd/docs/`, `examples/lighttpd/`, `ci/`, and generated reports.

## Prerequisites

POSIX shell, `make`, Python 3, Git, C/C++ build tools where a native build is performed, network only when explicitly fetching pinned sources/runtime components, and writable runtime roots outside the checkout.

## Required Submodules

```sh
git submodule update --init --recursive
make setup-dev
```

`FRAMEWORK_ROOT` defaults to `modules/ModSecurity-test-Framework`. If the submodule is absent, targets that require `check-framework` block before runtime work starts.

## Rebuild / Refresh

Use `REFRESH=1` only when intentionally recreating fetched/generated source or runtime state. Runtime roots default below `${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified`; override `VERIFIED_RUN_ROOT`, `BUILD_ROOT`, `SOURCE_ROOT`, `TMP_ROOT`, and `LOG_ROOT` when an operator needs isolated workspaces.

## Generated Artifacts

Do not hand-edit generated reports. Refresh them through repository targets such as `make refresh-connector-reports`, `make refresh-all-reports`, `make generate-test-matrix`, or `make check-test-matrix` when the change actually requires regenerated evidence.

## Cleanup

The repository Makefile writes runtime/build state under `VERIFIED_RUN_ROOT` and related roots, not global install prefixes. Remove the chosen run root only after preserving any logs or JSON summaries needed for evidence.

## Best Practices

- Keep build and runtime artifacts outside the git checkout.
- Pin source/runtime versions through the existing framework variables; do not introduce undocumented versions in operator docs.
- Treat force-all FAIL rows as evidence of boundaries, not production support.
- Keep request-only operation as the conservative baseline unless a generated report proves a more specific behavior.

## Build / Prepare Variables

`LIGHTTPD_BIN`, `LIGHTTPD_DECISION_BACKEND`, `DECISION_BACKEND`, `ALLOW_RUNTIME_BUILDS`, `CONNECTOR_COMPONENT_CACHE`, `SKIP_RUNTIME_COMPONENT_PREPARE`, `RUNTIME_COMPONENT_STRICT_VERIFY`, and `KEEP_RUNTIME_ARTIFACTS` are present in Makefile exports or harnesses. Version/checksum values are sourced from framework `common.sh` when present. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

## Minimal Local Build

```sh
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
```

The command is minimal for this repository's evidence path. It is not a global installation recipe.

## Manual Build Flow

Prepare/build the pinned Lighttpd tarball with `ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build`; then run `make smoke-lighttpd`, `make smoke-lighttpd-modsecurity`, or CRS variants only when local Lighttpd, libmodsecurity, and optional CRS inputs are staged.

## Production / Production-Style Integration

This is production-style only, not production-ready. The current path places Lighttpd in front of or beside a ModSecurity sidecar/proxy; it does not load a native Lighttpd module. A comparable deployment would need the staged Lighttpd binary, proxy configuration, a reachable ModSecurity sidecar/decision backend, libmodsecurity for that backend, rules and optional CRS, and Lighttpd plus sidecar logs. Reload/restart follows Lighttpd config validation and operator process-manager practice. Native module, FastCGI/SCGI, and mod_magnet/Lua paths are not implemented here and must be treated only as deferred options when mentioned.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Build/stage the pinned Lighttpd runtime with `ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build`, prepare libmodsecurity through `make prepare-runtime-components` when the libmodsecurity backend is used, prepare the sidecar_proxy path, then run `make smoke-lighttpd` or `make smoke-lighttpd-modsecurity`/`make smoke-lighttpd-crs`. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/lighttpd/README.md](examples/lighttpd/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Test / Smoke Validation

Declared targets include `make smoke-lighttpd`, `make smoke-lighttpd-modsecurity`, `make smoke-lighttpd-crs`, and `make smoke-lighttpd-crs-secondary`. Use CRS variants only when CRS is prepared by the existing framework flow.

## Runtime Evidence Paths

Lighttpd result/log/runtime roots from framework `common.sh` when available and generated reports under `reports/testing/generated/`.

## Logs

Lighttpd access/error logs when configured plus sidecar decision/audit logs. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

If the pinned source build, sidecar_proxy service, libmodsecurity, or CRS is absent, treat the run as blocked or runtime evidence only, not success.

## Common Failures

Missing runtime build permission, missing local Lighttpd binary, missing sidecar wiring, missing libmodsecurity backend, or assuming a native connector exists.

## Related Docs / Examples

- [examples/lighttpd/README.md](examples/lighttpd/README.md)
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
- `reports/testing/generated/`
