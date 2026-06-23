# Compile / Prepare Envoy

## Purpose

Document the repository-supported build or prepare path for Envoy without adding unverified production claims. This guide is operator-facing and ties every build, runtime, and smoke statement to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Open connector runtime path under `connectors/envoy/` using Envoy `ext_authz`. Envoy is not built from source here. Production ready, full matrix ready, CRS complete, and response-body verified are all false.

## What This Builds / Prepares

a pinned Envoy runtime binary in the component cache plus generated smoke config/evidence when the framework runtime scripts are available.

## What This Does Not Prove

This does not prove production readiness, full CRS coverage, full matrix coverage, ext_proc, response-body support, or source compilation. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/envoy/src/`, `connectors/envoy/harness/`, `connectors/envoy/docs/`, `examples/envoy/`, `ci/`, and generated reports.

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

`ENVOY_BIN`, `ENVOY_DECISION_BACKEND`, `DECISION_BACKEND`, `CONNECTOR_COMPONENT_CACHE`, `SKIP_RUNTIME_COMPONENT_PREPARE`, `RUNTIME_COMPONENT_STRICT_VERIFY`, and `KEEP_RUNTIME_ARTIFACTS` are present in Makefile exports or harnesses. Version/checksum values are sourced from the framework `common.sh` when present. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

## Minimal Local Build

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
make smoke-envoy
```

The command is minimal for this repository's evidence path. It is not a global installation recipe.

## Manual Build Flow

Prepare the pinned Envoy binary with `make prepare-envoy-runtime`; do not document a source build. Run `make smoke-envoy`, `make smoke-envoy-modsecurity`, or CRS variants only when local Envoy, libmodsecurity, and optional CRS inputs are staged.

## Production / Production-Style Integration

This is production-style only, not production-ready. A comparable deployment would need the pinned Envoy binary, an `ext_authz` HTTP/gRPC authorization service or sidecar path, libmodsecurity for the libmodsecurity backend, ModSecurity rules and optional CRS, and Envoy access/error/admin logs plus sidecar decision/audit logs. Envoy sends authorization checks through `ext_authz`; the sidecar makes allow/deny decisions. Reload/restart depends on the operator process manager; config changes require Envoy validation/restart or hot-restart practice outside this repository.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Prepare the pinned runtime with `make prepare-envoy-runtime`, prepare libmodsecurity through `make prepare-runtime-components` when the libmodsecurity backend is used, prepare the ext_authz sidecar path, then run `make smoke-envoy` or `make smoke-envoy-modsecurity`/`make smoke-envoy-crs`. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/envoy/README.md](examples/envoy/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Test / Smoke Validation

Declared targets include `make smoke-envoy`, `make smoke-envoy-modsecurity`, `make smoke-envoy-crs`, and `make smoke-envoy-crs-secondary`. Use CRS variants only when CRS is prepared by the existing framework flow.

## Runtime Evidence Paths

Envoy result/log/runtime roots from framework `common.sh` when available and generated reports under `reports/testing/generated/`.

## Logs

Envoy access/admin/error logs when configured plus sidecar decision/audit logs for the libmodsecurity path. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

If the pinned binary, ext_authz service wiring, libmodsecurity, or CRS is absent, treat the run as blocked or runtime evidence only, not success.

## Common Failures

Missing local common.sh-managed Envoy binary, missing auth service wiring, missing libmodsecurity backend, or assuming source compilation exists.

## Related Docs / Examples

- [examples/envoy/README.md](examples/envoy/README.md)
- `connectors/envoy/README.md`
- `connectors/envoy/docs/build.md`
- `connectors/envoy/docs/validation.md`
- `reports/testing/generated/`
