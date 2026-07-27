# Change Record: Parent analysis-helper unused-parameter cleanup for SonarQube Cloud S1172

**Language:** English | [Deutsch](CR-20260727-sonar-parent-analysis-unused-parameters.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-parent-analysis-unused-parameters |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1172` Code Smells AZ7b3dfYcO69wzd-_jHm, AZ7b3dfYcO69wzd-_jHn, AZ7b3dfYcO69wzd-_jHo, AZ7POyVcBW70q7L2nMJV, and AZ7POyVcBW70q7L2nMJX. |
| Boundary | Parent runtime/evidence analysis source, a Parent-only focused test, this English/German Change Record pair, and their indexes. Framework/MRTS repository content and Gitlinks, report semantics, path-validation controls, scanner configuration, Quality Gates, suppressions, external Sonar state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

Five analysis-helper parameters are accepted but never read. They make the
helper contracts look broader than their real data dependencies and cause five
SonarQube Cloud `python:S1172` Code Smells. Two helpers only produce a fixed
tool inventory or derive a variant from a path; the other two use their
remaining inputs for report metadata, paths, or incomplete-job rows.

## Acceptance criteria

- Remove only the five unused parameters and adjust every direct Parent call.
- Preserve `framework_root` use for native-summary metadata, report fields,
  variant derivation, incomplete-job classification, and output paths.
- Retain the immutable-commit `label` parameter, which is currently used in
  diagnostics and is not part of this change.
- Pass focused mocked Parent output coverage plus no-write syntax, signature,
  parameter-use, and direct-call arity checks.
- Maintain this complete English/German Change Record pair and indexes, then
  run applicable documentation and diff-hygiene checks.

## Implementation decision and rationale

`inventory(...)` has no runtime input dependency, so its unused connector and
Framework parameters were removed. `write_summary_report(...)` keeps its
connector and Framework roots for metadata but no longer accepts unused
`build_root`. In the verified-runtime mismatch generator, `connector` is not
needed to derive a path variant and `connector_root` is not needed to classify
incomplete jobs; their direct call sites now pass only the remaining inputs.
The focused test writes only temporary mocked report output and a synthetic job
record, then confirms the retained tool inventory, summary output, incomplete
row, and path-derived variant. No native runtime, Framework checkout, or MRTS
data is consumed.

## Changed files

- `ci/runtime/lifecycle/run-native-case-comparison.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <dynamic imports and
  baseline pure helper outputs>` passed before the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <AST baseline signature and unused-body predicate>` passed
  before the edit.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v
  tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_native_summary_and_mismatch_helpers_keep_outputs_with_reduced_context_parameters`
  passed after the edit: 1 test in 0.006s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <post-edit syntax, signatures, parameter-use, and direct-call
  arity AST predicate>` passed.
- The documentation-pair validator, `tests.test_bilingual_docs`, and
  `rtk proxy git diff --check` are run after this pair is added; this record
  asserts no unobserved CI, runtime, review, or delivery result.

## Security impact

`not_applicable` to the product diff: this is a signature-only cleanup. The
retained code continues to derive paths from its prior roots, passes the
Framework root to report metadata, and classifies incomplete jobs from the
same job records. The focused test avoids real Framework/MRTS inputs and does
not weaken validation, ownership, symlink, publication, or supply-chain
controls.

## Runtime evidence

No connector, NGINX, CRS, MRTS, native libmodsecurity, or report-generation
runtime was executed. The focused test uses temporary mocked serialization and
a synthetic Parent job file only; it verifies helper output contracts rather
than claiming production runtime evidence.

## Known limitations

The local interpreter is Python 3.14.4 while the CI version-file contract is
Python 3.14.6, so the focused result is same-minor local evidence. The test
does not execute real metadata serialization or a native runtime. This batch
covers five current Code Smells; the public project endpoint still reports
1,125 `OPEN` issues, and this uncommitted candidate changes no external Sonar
state.

## Remaining risks

An unobserved external caller could still expect an old helper signature. The
repository source reference and AST checks found and validated every direct
Parent call, while the focused test executes all four reduced helper contracts.
An exact delivered-head Sonar analysis remains necessary before the listed
keys can be treated as resolved externally.

## Checks not run and rationale

- Full report generation, native runtime, connector builds, NGINX/CRS/MRTS
  matrices, and Framework/MRTS checks are not run because this is a signature-
  only Parent cleanup and they would consume unrelated runtime inputs.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The B16 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
