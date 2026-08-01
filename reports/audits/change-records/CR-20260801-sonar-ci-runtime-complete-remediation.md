# Change Record: Parent CI runtime complete SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-ci-runtime-complete-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-runtime-complete-remediation` |
| Date (UTC) | `2026-08-01` |
| Base revision | `a7e2e70f307c91bc3da702b7240a1c4218cb2b79` |
| Goal | Remediate the current Parent `ci/runtime` SonarQube Cloud inventory with source-native controls and a focused security review, then publish one verifiable Draft PR. |
| Boundary | Parent `ci/runtime/**`, the directly required Parent `ci/lib/runtime_path_utils.py`, direct Parent tests, and this English/German Change Record pair plus their indexes. Framework, MRTS, Gitlinks, scanner configuration, Quality Gate, exclusions, suppressions, workflows, and `master` are not changed. |

## Motivation and problem statement

The exact `master` SonarQube Cloud analysis at the base revision reported 64
open items in `ci/runtime`: 33 vulnerabilities and 31 Code Smells, with zero
duplicated lines. The affected lifecycle tools accept runtime paths, select
subprocess arguments, emit evidence, and orchestrate bounded jobs. Those are
security-relevant boundaries as well as maintainability hotspots.

The work therefore removes duplicated shell literals and backtracking-prone
regular expressions, decomposes high-complexity lifecycle decisions, and
constrains runtime-derived input and output paths to either a private,
descriptor-validated runtime root or an existing regular source file below a
canonical checked-out Parent/Framework root.

## Acceptance criteria

- Source fixes retain fail-closed root ownership, mode, no-follow, and
  containment controls before runtime artifact access.
- Lifecycle child commands use allow-listed matrix tokens and canonical source
  roots; timeouts continue to prefer a completed host job record.
- Existing source-compatible report, status, event, and evidence semantics are
  preserved by focused regression tests.
- No `NOSONAR`, false-positive change, suppression, scanner configuration,
  Quality-Gate change, or Gitlink update is used.
- The eventual exact PR head must receive a fresh GitHub Actions and
  SonarQube Cloud readback. New-Code acceptance remains zero new issues and
  `0.0%` duplication; no current issue is claimed resolved until that analysis
  has observed the final head.

## Implementation decision and rationale

`runtime_artifact_path()` remains the central private-runtime guard. A new
companion recognizes only regular, non-symlink source files under the canonical
Parent/Framework roots for lifecycle inputs that must hash checked-in rules or
capabilities. All other input and output paths remain below the private runtime
root. This avoids widening read authority to arbitrary host paths.

The collector now decomposes metadata coercion, first-byte validation, raw
event rejection, and case outcome evaluation into bounded helpers. Matrix and
native runners now isolate canonical-context, child-environment, timeout, and
result-classification steps. These changes preserve the established contracts
while reducing decision nesting and repeated literals.

## Known non-applicable S5332 lead

The current `python:S5332` row in
`ci/runtime/common/response-header-test-backend.py` is not a remotely reachable
product HTTP service: it binds only to `127.0.0.1` for connector fixtures and
does not accept an endpoint from an untrusted party. It is already tracked in
`FND-SONAR-0001` as `not_actionable` with high confidence. This change neither
marks it false-positive nor risk-accepts it in SonarQube Cloud; an external
issue-state change would require a separate current explicit authorization.

## Changed files

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/common/resolve-runtime-paths.py`
- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `ci/runtime/lifecycle/resolve-full-lifecycle-profile.py`
- `ci/runtime/lifecycle/run-full-matrix-job.py`
- `ci/runtime/lifecycle/run-full-matrix-resume.py`
- `ci/runtime/lifecycle/run-mrts-native-full.sh`
- `ci/runtime/lifecycle/run-native-case-comparison.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/runtime/lifecycle/run-verified-case.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `ci/runtime/lifecycle/sanitize-full-lifecycle-log.py`
- `ci/runtime/lifecycle/write-*.py` lifecycle writers
- focused `tests/test_*runtime*`, resolver, engine-artifact, and profile tests
- this Change Record pair and indexes

## Commands executed

| Command or control | Result |
| --- | --- |
| `python3 -m py_compile` for all changed Python production modules and focused tests | passed. |
| `python3 tests/test_runtime_artifact_utils.py` | passed: 9 tests. |
| `python3 tests/test_runtime_path_security.py` | passed: 21 tests, including symlink-swap, normalized parent-traversal rejection, generated-report component allowlisting, and decimal-only child timeout rendering. |
| `python3 tests/test_resolve_runtime_paths.py` | passed: 8 tests. |
| `python3 tests/test_engine_lifecycle_artifacts.py` | passed: 5 tests. |
| `python3 tests/test_full_lifecycle_profiles.py` | passed: 5 tests. |
| `python3 tests/test_full_lifecycle_evidence.py` | passed: 19 tests, including the restored same-directory sanitizer compatibility path and rejection of cross-directory use without a named runtime root. |
| `python3 tests/test_collect_no_crs_source_helpers.py` | passed: 3 Framework-independent collector helper tests. |
| `python3 tests/test_bilingual_docs.py` | passed: 22 documentation-checker unit tests. |
| `sh -n ci/runtime/lifecycle/run-no-crs-baseline.sh` and `sh -n ci/runtime/lifecycle/run-mrts-native-full.sh` | passed. |
| `git diff --check` | passed at the recorded local revision before delivery. |
| `python3 tests/test_collect_no_crs_source.py` | blocked before tests: the Parent-pinned Framework checkout lacks `ci/checks/catalog/no_crs_baseline.py`. |
| `python3 ci/checks/documentation/check-bilingual-docs.py` | blocked only by pre-existing links into the absent Parent-pinned Framework checkout; it reported no Change Record error. |

## Security impact

Changed paths cover CLI/environment-derived filesystem artifacts, source rule
files, shell subprocess arguments, evidence streams, and timeout cleanup. The
closest control is the descriptor-based private-runtime validator, now applied
before the changed writers read or create artifacts. Legitimate private roots,
canonical checked-in source files, and normal job-token selections remain
valid; symlinked, outside-root, and normalized traversal destinations are
rejected before product mutations.

No credential, scanner, test, Quality Gate, repository setting, or workflow
permission is changed. The reviewed loopback HTTP fixture is not altered.

The initial exact-head PR analysis reported five new findings: four taint
paths (`pythonsecurity:S2083`, two `pythonsecurity:S8707`, and
`pythonsecurity:S8705`) and `python:S1172`. This follow-up replaces the
sanitizer's direct path write with the existing atomic descriptor-based writer,
positively bounds persisted diagnostics and labels, validates relative report
components before construction, and renders the child timeout only after a
numeric bound check with `shell=False`. The new exact-head SonarQube Cloud
analysis remains the required verification; no issue state was changed.

## Compatibility and generated artifacts

No generated artifact is committed. Existing launcher options and normal
private runtime locations remain supported. Invalid paths that previously
reached a writer may now fail earlier, which is the intentional safety change.

## Documentation status

The paired Change Record and both indexes were added. The focused bilingual
checker unit suite passed; the repository-wide checker reached the records and
reported only existing missing Framework-link targets.

## Runtime evidence

The focused evidence is limited to the direct Python and shell controls listed
above. It proves private-root, symlink, and lexical traversal rejection as well
as normal source/runtime artifact handling; it is not connector-matrix or
host-runtime evidence.

## Known limitations

The complete collector test module and the Framework-dependent transport
integration cannot load from this fresh Parent worktree because its pinned
Framework content lacks a required catalog helper. This task neither initializes
nor modifies Framework or its Gitlink. Full connector matrices, host setup,
package installation, and live multi-user races are not claimed.

## Remaining risks

The exact final PR head still requires hosted security, review, and SonarQube
Cloud evidence. The known loopback-only `S5332` lead remains a separate,
tracked non-applicable item until an authorized external disposition changes.

Exact-head hosted checks, SonarQube Cloud result, review, and PR delivery facts
are pending until the task branch is committed and published. No merge or
direct `master` change is authorized by this record.

## Checks not run and rationale

- `tests/test_collect_no_crs_source.py` and its Framework-backed integration
  cases cannot import because `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`
  is absent at the Parent-pinned revision; changing that repository or Gitlink
  is outside the task boundary.
- Full connector/runtime matrices, host provisioning, package installation,
  generated-report refresh, and live cross-user race tests require unavailable
  native dependencies or exceed this focused source remediation scope.
- GitHub Actions, pull-request Secret Scanning, review, and SonarQube Cloud
  require the final exact PR head and are not inferred from local checks.

## Delivery status

At record authoring the task worktree is rebased onto
`a7e2e70f307c91bc3da702b7240a1c4218cb2b79`. No remote branch,
PR, hosted check, SonarQube Cloud analysis, review, or merge is claimed. Before
delivery, local, remote, and PR heads must be verified equal and hosted results
must be read for that exact head.

## Final diff and review status

The source and direct-test diff is under active focused security and final-diff
review. It is not ready to claim a verified PR until that review, documentation
validation, commit, publication, and exact-head hosted readback are complete.
