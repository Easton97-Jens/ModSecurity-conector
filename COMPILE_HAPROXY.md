# Compile HAProxy

## Purpose

Document the repository-supported build or prepare path for Haproxy without adding unverified production claims. This guide is operator-facing and ties every build, runtime, and smoke statement to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

SPOE/SPOP path using HAProxy plus `haproxy-modsecurity-spoa` and libmodsecurity. Default evidence reports 55/55 PASS; force-all evidence contains FAIL and NOT_EXECUTABLE rows. RESPONSE_BODY is not promoted.

## What This Builds / Prepares

a local HAProxy binary, `haproxy-modsecurity-spoa`, libmodsecurity binding/self-test pieces, SPOE config, decisions, audit logs, and smoke summaries under runtime roots.

## What This Does Not Prove

This does not prove OS-wide installation, every HAProxy build option, full RESPONSE_BODY support, or production support for force-all FAIL rows. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/haproxy/src/`, `connectors/haproxy/harness/`, `connectors/haproxy/docs/`, `connectors/haproxy/poc/spoe/`, `examples/haproxy/`, `ci/`, and `reports/testing/generated/`.

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

`HAPROXY_VERSION`, `HAPROXY_SOURCE_URL`, `HAPROXY_SHA256`, `HAPROXY_RUNTIME_DIR`, `HAPROXY_BIN`, `BUILD_ROOT`, `SOURCE_ROOT`, `LOG_ROOT`, and `RESULTS_DIR` are exported by the Makefile or preparation scripts. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

## Minimal Local Build

```sh
make smoke-haproxy
```

The command is minimal for this repository's evidence path. It is not a global installation recipe.

## Manual Build Flow

Run `make prepare-runtime-components`, optionally `make -C connectors/haproxy build-spoa-runtime` for the SPOA runtime, then `make smoke-haproxy` or `connectors/haproxy/harness/run_haproxy_smoke.sh`.

## Production / Production-Style Integration

A production-style HAProxy deployment needs HAProxy, a running `haproxy-modsecurity-spoa` process, libmodsecurity accessible to that process, SPOE config loaded by HAProxy, a SPOA agent config pointing at ModSecurity rules, and writable decision/audit/agent logs. End-to-end: HAProxy starts, the SPOE filter sends request metadata to the SPOP backend, the SPOA runtime calls libmodsecurity, the agent writes decision/audit evidence, and HAProxy allows, denies, redirects, or drops according to returned transaction variables. Response-header checks are a separate path; RESPONSE_BODY remains bounded runtime evidence only. Reload HAProxy after HAProxy/SPOE changes; restart the SPOA service after agent config, rules, binary, or library changes.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Fetch components with `make prepare-runtime-components`, build/prepare libmodsecurity, build/prepare HAProxy and `haproxy-modsecurity-spoa`, then run `make smoke-haproxy`. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/haproxy/README.md](examples/haproxy/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Test / Smoke Validation

`make smoke-haproxy`, `make test-haproxy-no-crs`, `make test-haproxy-with-crs`, and `make verified-haproxy-case CASE=<case> CRS=<no-crs|with-crs> MRTS=<no-mrts|with-mrts>` are declared targets. Use CRS variants only when CRS is prepared by the existing framework flow.

## Runtime Evidence Paths

HAProxy summaries under `BUILD_ROOT/results/.../haproxy`, SPOA `decision.jsonl`, audit logs, harness logs, and generated reports under `reports/testing/generated/`.

## Logs

HAProxy logs, SPOA agent logs, `decision.jsonl`, and ModSecurity audit logs. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

Check SPOP backend reachability, SPOE config syntax, frame/body limits, libmodsecurity library paths, writable log directories, and request/response phase assumptions.

## Common Failures

SPOE backend unavailable, HAProxy config validation failure, agent cannot open rules/logs, or phase-4 expectations exceeding non-promoted evidence.

## Related Docs / Examples

- [examples/haproxy/README.md](examples/haproxy/README.md)
- `connectors/haproxy/README.md`
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
- `reports/testing/generated/`
