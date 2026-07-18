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
| `tools/` | Small CI-status and maintenance inputs | documented caller only |

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

`NO_CRS_RUN_ID` is a filesystem-safe run identifier, for example `repository-cleanup-core-20260712T164725Z`. Do not use secrets, user names, or ticket text. See the [variables reference](../docs/reference/variables.md).

## Evidence flow

1. Make resolves repository, build, cache, runtime, and evidence roots.
2. `provisioning/` prepares one identity-bound Cache-v2 entry.
3. `runtime/lifecycle/` runs a host profile and writes payload-free local data.
4. The Framework and `evidence/collectors/` normalize and validate that data.
5. `checks/evidence/` decides whether it supports the selected claim.
6. `evidence/reports/` regenerates tracked reports; never edit generated output.

Exit `0` means technical completion, not that every catalog case is `PASS`. `1` is a general error, `2` is commonly a validation/aggregate error, and `77` means a declared missing optional prerequisite. A recursive GNU Make invocation can report its failed recipe as `2` even when the direct child returned `77`; callers must not infer the original status from that recursive exit code. See [test levels](../docs/testing-and-evidence.md) for status semantics.

## Optional-prerequisite status records

`ci/tools/run-check-status.py` runs one direct child command, writes a
payload-free JSON record, and emits a `CHECK_STATUS` JSON line before Make can
replace the child's exit code. The persisted record is the status channel: its
`schema_version` is `2` and `status_source` is either `child_exit_code`,
`parent_preflight`, or `parent_explicit`. Child `stdout` and `stderr` are
forwarded only for diagnostics; neither stream can supply a reason or
authorize a workflow result. Its records use this lowercase status model:

| Status | Meaning | Default workflow result |
| --- | --- | --- |
| `passed` | The direct check ran and succeeded. | success |
| `failed` | The direct check returned an error other than the declared blocked code. | failure |
| `blocked` | The check is relevant but a declared prerequisite is unavailable. | failure unless this runner's `parent_preflight` records an allowed structured reason |
| `not_applicable` | The caller explicitly records that the check is outside this job's scope. | failure unless its caller explicitly allows it |
| `not_executed` | The check was deliberately not started and has no valid disposition. | failure |

The runner derives a fixed filename from its validated `--check` identifier
under `$(BUILD_ROOT)/check-status`; for the Apache cleanup check this is
`apache-request-transaction-cleanup.json`. It accepts no caller-selected
status-file path. `BUILD_ROOT` must be an absolute, canonical, invocation-owned
external path. The runner rejects checkout-local, noncanonical, and symlinked roots or status
files before writing. It opens the validated status directory before starting
the child command and uses that directory handle for the temporary file and
final replacement. These records are CI-control evidence, not canonical runtime
evidence.

`make check-apache-request-transaction-cleanup` remains strict: its Python
source contract and native Apache/APR harness must both complete, and a missing
prerequisite remains nonzero. In contrast,
`make check-apache-request-transaction-cleanup-lint` keeps the same mandatory
Python source contract but uses the parent-owned
`--blocked-if-missing-apache-development` preflight. Before the child starts,
the runner resolves `APXS_BIN`, then `APXS`, then
`CI_APXS_BIN_CANDIDATES` (or `apxs`/`apxs2`), and requires an executable APXS
whose `-q INCLUDEDIR` result is an absolute directory containing `httpd.h`.
Only when that preflight fails does the runner record the structured
`apache_development_prerequisite` `blocked` result and allow it for this lint
target. If the preflight passes, the child runs; every child `77`, including a
copied or forged `CHECK_STATUS_REASON` string in either output stream, remains
an unclassified nonzero result. The five documented Push workflows reach this
one subcheck through `make lint` or `make quick-check`; no other target,
Common check, or connector check inherits the allowance.

## Adding a file

Place a new file with its responsibility, update its Make/workflow caller, and use `Path(__file__).resolve()` or a `SCRIPT_DIR` derived from `dirname -- "$0"` for location discovery. Do not add workspace-specific paths, duplicate a `lib/` helper, or introduce a runtime capability in this organizational change.
