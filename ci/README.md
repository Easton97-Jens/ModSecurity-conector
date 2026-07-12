# CI tooling

**Language:** English | [Deutsch](README.de.md)

This tree contains connector-repository orchestration, contracts, and evidence tools. The Framework owns the reusable case catalog; this repository owns connector integration through `FRAMEWORK_ROOT`.

## Layout

| Area | Responsibility | Invocation |
| --- | --- | --- |
| `checks/common/` | Common SDK, build, flow, memory, directive, and adapter contracts | matching `make check-*` target |
| `checks/connectors/` | Connector and aggregate adoption contracts | `make check-<connector>-*` |
| `checks/documentation/` | Language, links, generated-layout, path, and variable checks | `make check-doc-links` |
| `checks/evidence/` | Lifecycle, fixture, capability, and core-completion checks | evidence targets |
| `checks/security/` | Runtime-path and artifact safety | `make check-runtime-path-policy` |
| `runtime/common/` | Shared path, process, port, and fixture helpers | runner support only |
| `runtime/lifecycle/` | Canonical runners, normalizers, and artifact writers | lifecycle Make targets |
| `provisioning/` | Cache-v2, component, and toolchain preparation | `make prepare-runtime-components` |
| `evidence/collectors/` | Capability collection | `make capabilities-*` |
| `evidence/reports/` | Report generators and refresh orchestration | `make refresh-all-reports` |
| `lib/` | Common imported Python helpers | not a standalone entry point |
| `tools/` | Small maintenance inputs | documented caller only |

Python files use `snake_case.py`; established shell names retain their `kebab-case.sh` form. Do not rename a stable file merely for cosmetics.

## Entry points and inputs

Use Make targets rather than nested files from an arbitrary working directory. They set repository-relative roots and verify the Framework.

| Target | Purpose | Inputs | Artifacts |
| --- | --- | --- | --- |
| `make quick-check` | Fast contracts, syntax, and documentation checks | `PYTHON`, `FRAMEWORK_ROOT` | No canonical runtime evidence |
| `make prepare-runtime-components` | Materializes or reuses Cache-v2 inputs | `BUILD_ROOT`, `CACHE_ROOT`, `CONNECTOR_COMPONENT_CACHE` | Component manifest and local snapshot |
| `make full-lifecycle-<connector>` | Runs one selected native HTTP/1.1 core profile | `<connector>` = `apache`, `nginx`, `haproxy`, `envoy`, `traefik`, or `lighttpd`; `NO_CRS_RUN_ID` | Connector evidence |
| `make full-lifecycle-all-connectors` | Runs all six selected profiles | `NO_CRS_RUN_ID`, writable runtime/evidence roots | Six result sets |
| `make check-six-connector-core-completion` | Validates aggregate evidence | Same run id and evidence root | Aggregate PASS/FAIL |

`NO_CRS_RUN_ID` is a filesystem-safe run identifier, for example `repository-cleanup-core-20260712T164725Z`. Do not use secrets, user names, or ticket text. See the [variables reference](../docs/configuration/variables.md).

## Evidence flow

1. Make resolves repository, build, cache, runtime, and evidence roots.
2. `provisioning/` prepares one identity-bound Cache-v2 entry.
3. `runtime/lifecycle/` runs a host profile and writes payload-free local data.
4. The Framework and `evidence/collectors/` normalize and validate that data.
5. `checks/evidence/` decides whether it supports the selected claim.
6. `evidence/reports/` regenerates tracked reports; never edit generated output.

Exit `0` means technical completion, not that every catalog case is `PASS`. `1` is a general error, `2` is commonly a validation/aggregate error, and `77` means a declared missing optional prerequisite. See [test levels](../docs/testing/test-levels.md) for status semantics.

## Adding a file

Place a new file with its responsibility, update its Make/workflow caller, and use `Path(__file__).resolve()` or a `SCRIPT_DIR` derived from `dirname -- "$0"` for location discovery. Do not add workspace-specific paths, duplicate a `lib/` helper, or introduce a runtime capability in this organizational change.
