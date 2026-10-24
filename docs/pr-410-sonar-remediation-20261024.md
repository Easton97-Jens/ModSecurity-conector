# PR #410 Sonar remediation and final verification

**Language:** English | [Deutsch](pr-410-sonar-remediation-20261024.de.md)

## Outcome at the versioned checkpoint

The concrete Sonar causes on the starting PR head were addressed in the patch without a
Quality Gate exclusion, rule suppression, accepted-issue disposition, or
historical-result rewrite. The patch keeps the reduced I12 closeout intact and
does not change the Framework or MRTS Gitlink.

The one authorized local functional run was executed exactly once and **failed**.
It ran 39 unittest methods representing 79 predeclared expanded active scenarios;
65 expanded scenarios passed, five failed during a common C++ helper build, one
errored at an Envoy fixture-root boundary, and eight later companion variants
were not reached after the method aborted. No retry was run and executable
behavior was not changed afterward. Consequently this checkpoint is
`remediation_required`, not `verified_pr`, regardless of any later green scanner
result.

The exact published commit and automatic CI/Sonar readback are recorded in the
PR after the single final push; this static document does not self-assert a
future commit or provider result.

## Starting Sonar inventory

The complete baseline is machine-readable in
[sonar-baseline.json](../reports/testing/pr410-sonar-remediation-20261024/sonar-baseline.json).
It is bound to PR head `30d50a181278904a552e295d9a2c1ae1265e8b87`, analysis
`e18acebb-7e6c-4727-a572-afe02105a43b`, compute task
`AaFrW5KKk-m4lzyjl55H`, and analysis time `2026-10-24T00:39:09Z`.

| Category | Baseline |
| --- | ---: |
| Open issues | 231 |
| Vulnerabilities / code smells / bugs | 90 / 141 / 0 |
| Blocker / critical / major / minor | 5 / 121 / 76 / 29 |
| Open security hotspots / accepted issues | 0 / 0 |
| New duplicated blocks / lines | 21 / 851 |
| New duplicated-line density | 0.20824055087089086 |
| PR coverage measurements | unavailable |
| Quality Gate | `ERROR`: new Security Rating E (5), required A (1) |

All 231 open issues, every duplication-positive file and block, all reported
measures, the compute task, and all 50 GitHub annotations were read. The 50
annotations were therefore only a presentation subset, not a vulnerability
count. Sonar reported one reliability issue, 90 security issues, and 140
maintainability issues. Its three configuration warnings concerned the Python
version, missing test classification, and unspecified encoding; the tracked
local inventory contained only ASCII, UTF-8, or binary files.

## Root causes and remediation

| Cause and affected findings | Remediation and preserved boundary |
| --- | --- |
| 125 findings and 19 of 21 duplicate-block occurrences came from source-suffixed files under `ci/runtime/lifecycle/i12/objects/text/**`. These are immutable, hash-bound historical records, not maintained programs. | 61 plain-text objects and one historical observer repository snapshot were changed to the existing lossless `text_lines` JSON data representation. All 346,634 reconstructed bytes and every SHA-256 identity remain exact. `capture_sources.py` now rejects source-suffixed plain-text objects. Historical results, deltas, profiles, and revisions were not edited. |
| Envoy still imported or exposed historical helpers transitively; the archived host-log parser also carried the sole reliability rule `python:S8786`. | Maintained `host_log_observations.py` and `grpc_stream_observations.py` are normal reviewed modules. Historical helpers remain authenticated provenance data and cannot replace current parser identities or enter the helper-directory import path. Parsing is bounded and linear. |
| Live Python security flows accepted evidence paths or publication targets without one common read/write boundary. | `ci/lib/i12_path_safety.py` centralizes canonical roots, traversal/symlink/private-path/unsafe-mode/checkout rejection, bounded descriptor-pinned reads, and create-versus-replace semantics. Apache, HAProxy, Traefik, lighttpd, Envoy, and report producers use this boundary. Existing `CODEX_PROJECT_STATE` compatibility remains explicit. |
| Evidence generators contained repeated unbounded parsing/publication logic and high cognitive complexity. | The current report, lifecycle ledger, and Oracle reconciliation generators use the shared bounded I/O contract and smaller linear parsing helpers while preserving historical-result and qualification separation. |
| NGINX acceptance/qualification and native observer code mixed independent validations in large functions; the native observer test duplicated the same compile fixture. | NGINX validation was decomposed without weakening identity, provenance, physical-producer, or negative-event checks. Native C finalization uses named helpers/state, and the tests share one compile fixture while retaining distinct runtime and companion scenario sets. |
| Automatic analysis lacked explicit Python and test-source configuration. | `.sonarcloud.properties` declares Python 3.14 and classifies `tests/**/*.py`, `**/test_*.py`, and `**/*_test.py` as tests. It contains no source, issue, coverage, duplication, or rule exclusion. |

The patch addresses all baseline cause groups. Actual issue closure and
duplication removal remain claims of the automatic analysis of the published
head, not of the source diff alone.

## Duplication and coverage effect

Fourteen historical object paths accounted for 19 duplicated-block occurrences;
their data conversion removes the false maintained-code relationship without
changing a byte of reconstructed history. The remaining two occurrences were a
genuine duplicate in `tests/test_native_lifecycle_observer.py`; one shared
fixture compiler now serves the runtime and companion checks while their
separate parameters, ownership failures, EOS variants, and assertions remain.

No test was deleted to obtain a pass. Sonar supplied no PR coverage measure, so
this work does not claim a coverage percentage. The scanner now receives an
explicit test classification so a later analysis can report the layer
correctly.

## Frozen test budget and the single run

The immutable plan is
[test-plan.json](../reports/testing/pr410-sonar-remediation-20261024/test-plan.json)
and the result is
[run-result.json](../reports/testing/pr410-sonar-remediation-20261024/run-result.json).
An import-free preflight resolved every selector from source and enforces
rejection above the shared limit.

| Item | Count/status |
| --- | ---: |
| Historical frozen reserve, not re-executed | 21 |
| Selected active scenarios | 79 |
| Combined project budget | 100 / 100 |
| Exact selectors / unittest methods | 30 / 39 |
| Local commands / retries | 1 / 0 |
| Expanded PASS / FAIL / ERROR / not reached | 65 / 5 / 1 / 8 |
| unittest summary | `FAILED (failures=5, errors=1)` in 11.431 s |

The retained 21 historical cases consume the same project-wide budget but were
not run. The 79 selected scenarios were unit, contract, synthetic-evidence, and
local compiled C/APR/SDK controls; they did not start a host, network, protocol
matrix, or historical I12 campaign.

The error and failures were:

- Envoy's historical-helper control wrote a temporary fixture below the run
  root, but the maintained transport reference used `evidence_io.DEFAULT_ROOTS`
  fixed at module import rather than the test's patched storage root. Admission
  stopped before the no-transitive-import assertion.
- Five native expanded scenarios reached the same C++ SDK-helper prerequisite.
  Its `-isystem /usr/include` argument caused GCC 15 libstdc++
  `#include_next <stdlib.h>` resolution to fail before runtime assertions.
- The companion method's first compile failure prevented its remaining eight
  sequential variants from running.

The full read-only log is retained outside the checkout at
`/var/tmp/codex/ModSecurity-conector/pr410-sonar-final-20261024.0T0N9T/functional-run.log`
(SHA-256 `4015acc961e1af01a1d88884a2960ae349230f44a001c4d93841521ea6fcdaa3`,
21,256 bytes). No second local run is permitted for this task.

## Other verification

- The static archive/integration verifier passed for 62 conversions, 346,634
  reconstructed bytes, every archive/delta hash, the allowed manifest
  transitions, current pins, 64 JSON files, 61 changed Python AST/symbol-table
  files, and the unchanged Framework Gitlink.
- `git diff --check` passed.
- Strict `-std=c17 -Wall -Wextra -Werror -fsyntax-only` checks passed for the
  changed native lifecycle observer and Apache header-semantics probe.
- One focused defensive patch review found no remaining actionable security
  issue. It was static and is not a runtime or scanner substitute.

## Boundaries and delivery status

The existing I12 frozen selection, archive disposition, historical PASS/FAIL
bindings, and `I12_COMPLETE=false` boundary remain unchanged. No Framework or
MRTS repository, Gitlink, historical Oracle, host run, or matrix was changed or
executed.

The repository's automatic default test paths are still not all wired to one
authoritative inventory and technical pre-execution cap. Only this task's
selection had a verified 79+21 guard. Global automatic cap enforcement remains
`not_verified` and requires separately authorized migration.

Because the only local run failed and part of the selected behavior was not
reached, current-head runtime acceptance and final local verification are
missing. PR #410 must remain Draft/`remediation_required`; a green automatic CI
or Sonar result cannot retroactively turn this local result into a pass.
