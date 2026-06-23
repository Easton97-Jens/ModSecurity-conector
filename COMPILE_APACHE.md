# Compile Apache

## Purpose

Document the repository-supported build or prepare path for Apache without adding unverified production claims. This guide is operator-facing and ties every build, runtime, and smoke statement to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Adapter-owned Apache module under `connectors/apache/`; request phases are the production-style baseline. Default generated evidence currently reports 54/54 PASS, while force-all evidence still contains FAIL and NOT_EXECUTABLE rows and must not be promoted.

## What This Builds / Prepares

libmodsecurity v3, an Apache/APXS toolchain when `BUILD_HTTPD_FROM_SOURCE=1` or a module against explicit matching `APXS`/`APACHE_HTTPD`, and `mod_security3.so` from `connectors/apache/`.

## What This Does Not Prove

This does not prove every distribution Apache package, MPM combination, module mix, CRS deployment, or complete RESPONSE_BODY support. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/apache/src/` (module source), `connectors/apache/harness/` (smoke harness), `connectors/apache/docs/`, `examples/apache/`, `common/`, `ci/`, and `reports/testing/generated/`.

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

`BUILD_HTTPD_FROM_SOURCE`, `APXS`, `APACHE_HTTPD`, `MODSECURITY_APACHE_SOURCE_DIR`, `MODSECURITY_V3_SOURCE_DIR`, `MODSECURITY_V3_ROOT`, `BUILD_ROOT`, `SOURCE_ROOT`, `LOG_ROOT`, `RESULTS_DIR`, `MODSECURITY_TEST_VARIANT`, and `MODSECURITY_MRTS_VARIANT` are present in the Makefile or preparation scripts. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

## Minimal Local Build

```sh
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

The command is minimal for this repository's evidence path. It is not a global installation recipe.

## Manual Build Flow

Run `make prepare-runtime-components` to prepare libmodsecurity and runtime inputs, then use the Apache harness path through `make smoke-apache` or `connectors/apache/harness/run_apache_smoke.sh` with matching `APXS` and `APACHE_HTTPD` if supplying an external Apache.

## Production / Production-Style Integration

A production-style Apache deployment needs libmodsecurity v3 libraries, a `mod_security3.so` built for the exact Apache/APXS ABI, Apache config that loads the module, a ModSecurity rules file under an operator-chosen config directory such as `/etc/modsecurity`, optional CRS includes, and writable audit/error log locations. APXS and the Apache binary must come from the same Apache build or package family; this repository does not prove arbitrary distro/APXS/MPM combinations. After rule/config changes, run an Apache config test and graceful reload; after replacing the module or libmodsecurity, restart Apache according to site policy. Production-style paths shown in examples include an Apache module directory, `/etc/modsecurity`, CRS includes, ModSecurity audit logs, and Apache access/error logs, but they are examples rather than mandatory global install claims.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Fetch components with `make prepare-runtime-components`, build/prepare libmodsecurity through that target, build the Apache module with the prepared APXS flow, and run `make smoke-apache` for integrated evidence. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/apache/README.md](examples/apache/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Test / Smoke Validation

`make smoke-apache`, `make test-no-crs`, `make test-with-crs`, and targeted `make verified-apache-case CASE=<case> CRS=<no-crs|with-crs> MRTS=<no-mrts|with-mrts>` are declared targets. Use CRS variants only when CRS is prepared by the existing framework flow.

## Runtime Evidence Paths

`BUILD_ROOT/results/.../apache`, `LOG_ROOT`, Apache runtime logs, audit logs, and generated report files under `reports/testing/generated/`.

## Logs

Apache access/error logs from the harness runtime plus ModSecurity audit logs when enabled. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

Check missing submodule, APXS/httpd mismatch, unwritable runtime roots, missing libmodsecurity headers/libraries, CRS include paths, and response-body tests that are intentionally non-promoted.

## Common Failures

Missing framework returns a blocked preflight; APXS from one Apache and httpd from another can produce an unusable module; force-all rows may fail without changing production support status.

## Related Docs / Examples

- [examples/apache/README.md](examples/apache/README.md)
- `connectors/apache/README.md`
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
- `reports/testing/generated/`
