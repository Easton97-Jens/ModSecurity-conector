# Compile NGINX

## Purpose

Document the repository-supported build or prepare path for Nginx without adding unverified production claims. This guide is operator-facing and ties every build, runtime, and smoke statement to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Adapter-owned NGINX dynamic module under `connectors/nginx/`; request phases are the production-style baseline. Default generated evidence currently reports 60/60 PASS, while force-all evidence still contains FAIL and NOT_EXECUTABLE rows and must not be promoted.

## What This Builds / Prepares

libmodsecurity v3, a local NGINX runtime/module when `BUILD_NGINX_FROM_SOURCE=1`, and `ngx_http_modsecurity_module.so` from `connectors/nginx/`.

## What This Does Not Prove

This does not prove every NGINX release, distro build, module ABI, packaging layout, or complete RESPONSE_BODY support. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/nginx/src/`, `connectors/nginx/config`, `connectors/nginx/harness/`, `connectors/nginx/docs/`, `examples/nginx/`, `common/`, `ci/`, and `reports/testing/generated/`.

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

`BUILD_NGINX_FROM_SOURCE`, `NGINX_BINARY`, `NGINX_MODULE`, `NGINX_PREFIX`, `NGINX_BUILD_DIR`, `NGINX_SOURCE_DIR`, `MODSECURITY_NGINX_SOURCE_DIR`, `MRTS_NATIVE_NGINX_BIN`, and `MRTS_NATIVE_NGINX_MODULE_DIR` are present in the Makefile or preparation scripts. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

## Minimal Local Build

```sh
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

The command is minimal for this repository's evidence path. It is not a global installation recipe.

## Manual Build Flow

Run `make prepare-runtime-components` to prepare libmodsecurity and NGINX inputs, then use `make smoke-nginx` or `connectors/nginx/harness/run_nginx_smoke.sh`. If supplying an external NGINX, use a module compiled against compatible NGINX source/configure arguments.

## Production / Production-Style Integration

A production-style NGINX deployment needs libmodsecurity v3 libraries, `ngx_http_modsecurity_module.so` compiled for the deployed NGINX ABI, a top-level `load_module` directive, NGINX `modsecurity on;` and `modsecurity_rules_file` directives in the intended scope, optional CRS includes, and writable NGINX/ModSecurity logs. The dynamic-module flow loads the module at master startup with `load_module modules/ngx_http_modsecurity_module.so;`; config/rule changes can use `nginx -t` followed by reload, while replacing the binary module requires a restart/reload sequence compatible with the deployed NGINX package. The repository does not prove every NGINX version or distro build.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Fetch components with `make prepare-runtime-components`, build/prepare libmodsecurity through that target, build the dynamic module, then run `make smoke-nginx` for integrated evidence. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/nginx/README.md](examples/nginx/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Test / Smoke Validation

`make smoke-nginx`, `make test-no-crs`, `make test-with-crs`, and targeted `make verified-nginx-case CASE=<case> CRS=<no-crs|with-crs> MRTS=<no-mrts|with-mrts>` are declared targets. Use CRS variants only when CRS is prepared by the existing framework flow.

## Runtime Evidence Paths

`BUILD_ROOT/results/.../nginx`, `NGINX_HARNESS_PARENT`, `LOG_ROOT`, NGINX runtime logs, audit logs, and generated report files under `reports/testing/generated/`.

## Logs

NGINX access/error logs from the harness runtime plus ModSecurity audit logs when enabled. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

Check missing submodule, NGINX module ABI mismatch, worker traversal permissions for runtime roots, missing libmodsecurity libraries, CRS include paths, and non-promoted phase-4 rows.

## Common Failures

NGINX worker permissions can block generated docroots; a module built for a different NGINX can fail to load; force-all rows may fail without changing production support status.

## Related Docs / Examples

- [examples/nginx/README.md](examples/nginx/README.md)
- `connectors/nginx/README.md`
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`
- `reports/testing/generated/`
