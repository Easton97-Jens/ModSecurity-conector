# CI tooling

**Language:** English | [Deutsch](README.de.md)

This tree contains connector-repository orchestration, contracts, and evidence tools. The Framework owns the reusable case catalog; this repository owns connector integration through `FRAMEWORK_ROOT`.

## Automatic behavioral selection

[config/testing/active-cases.json](../config/testing/active-cases.json) remains the only selector authority for normal local, CI and scheduled checks.

The user explicitly authorized additional offline Python units outside the 100-case core ceiling. Schema 2 of the same inventory now declares **934 expanded cases across 540 executions**: 100 core cases / 80 executions (including the original eight offline cases) plus 834 explicitly source-bound `offline_unit_exceptions` / 460 executions. Every independent variant is counted. The runner validates both sections and enforces the core ceiling before every child; 101 core cases still fail. Exception selectors are Python-only, and their isolated child installs a guard against process creation and network access before importing tests. Package-level `tests.load_tests` defers offline test imports to that child. Raw `unittest discover -s tests` first imports each module in the parent to find its hook; those top levels were reviewed for absence of eager process/host activity, and test execution then occurs only in the guarded child. These counts describe the current selection, not final acceptance. This exception does not authorize native/Go/host scenarios outside the core budget.

Coverage currently selects 898 cases / 518 executions. One active offline timing case runs separately in Sonar CI without instrumentation: its unchanged one-second assertion failed under tracing (2.551 s) and passed without tracing (0.034 s). It remains selected and asserted; this changes measurement only, with no case removal, source exclusion or gate relaxation. Child tracing filters fixture line callbacks and retains only real positive hits for Parent MAIN sources.


`make check-active-inventory` checks the complete inventory without starting tests; `make test` and `make test-active` execute its admitted selection. Group/case/module filters apply only after full admission. Unknown or empty selections and changed source bindings fail; selection is never truncated. Functional build/lint callers use this same authority. Static compilation, CodeQL, actionlint, zizmor, OSV and secret scanning retain substantive independent gates.

Root/component defaults, standard CI, scheduled contracts and maintenance
candidate validation use this same selection. No-CRS plans must match the
Parent's exact declared case IDs before host execution. The fixed five-profile
CRS cells retain their actual selected requests and fail-closed evidence /
cleanup checks. NGINX remains its protected exact-head boundary with the two
separately counted callback On/Off cases. Readiness must not introduce a hidden
extra request scenario. Profile-specific results cannot qualify sibling routes.

Full matrix, broad smoke, MRTS, full-lifecycle, historical I12 and random fuzz
campaigns remain specialist work. Their retained commands require explicit
<code>ON_DEMAND_TESTS=1</code> and a current request for that assessment; manual
specialist workflows additionally require their closed <code>on_demand</code>
input where exposed. The flag is not permission to restart closed I12 work or
weaken privilege/source/artifact boundaries. Do not export it globally or set
it on standard CI/schedules. See the [archive and lost coverage](../docs/testing-and-evidence.md)
and [test entry points](../tests/README.md).

## Layout

| Area | Responsibility | Invocation |
| --- | --- | --- |
| `checks/common/` | Common SDK, build, flow, memory, directive, and adapter contracts | matching `make check-*` target |
| `checks/connectors/` | Connector and aggregate adoption contracts | `make check-<connector>-*` |
| `checks/documentation/` | Language, links, generated-layout, path, and variable checks | `make check-doc-links` |
| `checks/evidence/` | Lifecycle, fixture, capability, and core-completion checks | evidence targets |
| `checks/security/` | Runtime-path and artifact safety | `make check-runtime-path-policy` |
| `runtime/common/` | Shared path, process, port, and fixture helpers | runner support only |
| `runtime/contracts/` | Parent-owned canonical runtime-observation schema, semantic validator, and strict CLI | `validate-runtime-observation.py` |
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
| `make quick-check` | Static contracts, syntax and documentation plus the admitted functional subset | `PYTHON`, `FRAMEWORK_ROOT` | No canonical runtime evidence |
| `make prepare-runtime-components` | Materializes or reuses Cache-v2 inputs | `BUILD_ROOT`, `CACHE_ROOT`, `CONNECTOR_COMPONENT_CACHE` | Component manifest and local snapshot |
| `ON_DEMAND_TESTS=1 make full-lifecycle-<connector>` | Runs one selected native HTTP/1.1 core profile | `<connector>` = `apache`, `nginx`, `haproxy`, `envoy`, `traefik`, or `lighttpd`; `NO_CRS_RUN_ID` | Connector evidence |
| `ON_DEMAND_TESTS=1 make full-lifecycle-all-connectors` | Runs all six selected profiles | `NO_CRS_RUN_ID`, writable runtime/evidence roots | Six result sets |
| `make check-six-connector-core-completion` | Validates aggregate evidence | Same run id and evidence root | Aggregate PASS/FAIL |

`NO_CRS_RUN_ID` is a filesystem-safe run identifier, for example `repository-cleanup-core-20260712T164725Z`. Do not use secrets, user names, or ticket text. See the [variables reference](../docs/reference/variables.md).

The six-connector lifecycle commands above are retained on-demand orchestration
examples, not default validation or the scheduled/manual CI baseline. That baseline is the closed
<code>no-crs</code> profile in
<code>.github/workflows/reusable-five-connectors-profile.yml</code>, called by
<code>all-connectors-no-crs.yml</code>. It selects only Apache, HAProxy, Envoy,
Traefik, and lighttpd, rejects unknown profiles and connector rows, and
aggregates only the five bound result/receipt pairs. It makes no NGINX, CRS,
MRTS, full-matrix, or hosted-runtime-pass claim.

## Evidence flow

1. Make resolves repository, build, cache, runtime, and evidence roots.
2. `provisioning/` prepares one identity-bound Cache-v2 entry.
3. `runtime/lifecycle/` runs a host profile and writes payload-free local data.
4. `runtime/contracts/` validates the identity-bound, payload-free Parent runtime observation.
5. The Framework and `evidence/collectors/` normalize and validate reusable catalog data.
6. `checks/evidence/` decides whether it supports the selected claim.
7. `evidence/reports/` regenerates tracked reports; never edit generated output.

Exit `0` means technical completion, not that every catalog case is `PASS`. `1` is a general error, `2` is commonly a validation/aggregate error, and `77` means a declared missing optional prerequisite. A recursive GNU Make invocation can report its failed recipe as `2` even when the direct child returned `77`; callers must not infer the original status from that recursive exit code. See [test levels](../docs/testing-and-evidence.md) for status semantics.

## Canonical runtime-observation contract

`runtime/contracts/` is the Parent-owned boundary for canonical runtime
observations. `runtime-observation.schema.json` defines the transport shape;
`runtime_observation.py` is the single semantic validator and secure-file
reader. The contract is identity-bound to connector, profile, run ID, Parent
commit, Framework commit, and MRTS commit for every profile. It is
payload-free and permits only safe relative evidence references, so raw
requests, logs, secrets, and absolute runner paths do not become report
metadata.

The strict entry point is:

```sh
"$PYTHON" ci/runtime/contracts/validate-runtime-observation.py \
  --observation "<private-evidence-root>/runtime-observation.json" \
  --evidence-root "<private-evidence-root>" \
  --connector envoy --profile with-crs-no-mrts \
  --run-id RUN_ID --parent-sha PARENT_SHA --framework-sha FRAMEWORK_SHA \
  --mrts-sha MRTS_SHA \
  --policy strict
```

The default `--policy strict` emits payload-free JSON and exits `0` only for
`PASS`; unsafe input, identity mismatches, missing evidence, or
semantic mismatches emit `VALIDATION_FAILED` and exit `2`. `--policy partial`
reports `PARTIAL` for incomplete evidence but remains non-passing. A `PASS`
requires matching typed expectations and observations, a live selected and
executed Framework case, zero failure/mismatch counts, and zero cleanup
residue. No-MRTS profiles must contain only negative MRTS-isolation facts
while still binding the selected lowercase full `mrts_commit`; they must not
invoke an MRTS runner, load its inventory, start its process, create a
listener, or use an MRTS artifact. `--mrts-sha` is required for every profile.

The reader requires the current UID to own the evidence root and every
descendant directory, each at exact mode 0700, and regular evidence files at
exact mode 0600. It rejects symlinks and hard links, bounds observations to
1 MiB, and rejects duplicate JSON keys and non-strict UTF-8. Envoy, lighttpd,
and Traefik have live producer adapters. Apache and HAProxy expose interfaces
only. NGINX remains a protected separate boundary: the common validator
accepts only its approved protected producer and protected-runtime evidence,
while this PR neither invokes nor changes the broker production path. The
contract tests prove validator behavior, not a hosted runtime result.

## Optional NGINX worker self-map capture

The closed Common-input-fault and lifecycle-sequence drivers normally read the
actual nobody worker's `/proc/<pid>/maps`; a denied read remains a failure.
An explicitly selected test-only `--worker-self-map-library` (or
`NGX_NATIVE_WORKER_SELF_MAP_LIBRARY`) instead lets that same worker read
`/proc/self/maps` immediately after its real successful transition to UID/GID
65534. It adds no process-inspection capability. The Root parent opens a fresh
0600, single-link, regular `O_APPEND` file and passes its private descriptor to
the exact native launch. The helper binds the descriptor's device/inode and
captures only its original master's own child.

Before sending traffic, the parent requires complete bounded raw bytes,
matching worker PID, parent PID, UID/GID and process start time, and actual
maps entries for the selected native module and every loaded fixture library.
Missing, unsafe, incomplete or mismatched capture fails closed. Raw bytes and
the helper artifact hash remain in the run receipt; no master maps substitute
for worker maps. This channel proves loaded mappings only. It supplies no
host EOS, MIME decision, native/Common ID join or full lifecycle PASS.

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

With explicit <code>ON_DEMAND_TESTS=1</code>,
`make check-apache-request-transaction-cleanup` retains its strict specialist
Python source contract and native Apache/APR harness; both must complete and a
missing prerequisite remains nonzero. In that same specialist mode,
`make check-apache-request-transaction-cleanup-lint` keeps the Python source
contract but uses the parent-owned
`--blocked-if-missing-apache-development` preflight. Before the child starts,
the runner resolves `APXS_BIN`, then `APXS`, then
`CI_APXS_BIN_CANDIDATES` (or `apxs`/`apxs2`), and requires an executable APXS
whose `-q INCLUDEDIR` result is an absolute directory containing `httpd.h`.
Only when that preflight fails does the runner record the structured
`apache_development_prerequisite` `blocked` result and allow it for this lint
target. If the preflight passes, the child runs; every child `77`, including a
copied or forged `CHECK_STATUS_REASON` string in either output stream, remains
an unclassified nonzero result. Without <code>ON_DEMAND_TESTS=1</code>, both Make aliases select the admitted
Apache group instead of this archived native harness. The specialist allowance
does not authorize success for another target, Common check or connector check.

## Adding a file

Place a new file with its responsibility, update its Make/workflow caller, and use `Path(__file__).resolve()` or a `SCRIPT_DIR` derived from `dirname -- "$0"` for location discovery. Do not add workspace-specific paths, duplicate a `lib/` helper, or introduce a runtime capability in this organizational change.
