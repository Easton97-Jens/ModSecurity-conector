# Change Record: Parent CI verified-runtime-mismatch control-evidence deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-verified-runtime-mismatch-duplication` |
| Date (UTC) | `2026-07-29` |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Source revision assessed | Local task patch against the stated base revision |
| Boundary | Only Parent `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`, its direct Parent regression test, this English/German Change Record pair, and the paired indexes. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, SonarQube Cloud configuration, Quality Gate, exclusion, suppression, default-branch, or merge action is included. |
| SonarQube Cloud linkage | Removes one current same-file 20-line duplicate pair in the Parent CI generator. No scanner control is changed. |

## Motivation and problem statement

The current Parent CI generator contained two equivalent full-matrix control-
evidence loops. Their only intended difference was the fixed versus supplied
control-case name. The pair was a current SonarQube Cloud duplication target,
but it sits on a merge-readiness evidence boundary: a refactor must preserve
the fixed case, deterministic six-entry matrix, and all-pass classification
gates.

The focused security review also reproduced `FND-PARENT-0066`: an invalid
producer record could retain `status: pass` in the fallback after failing the
required `pass`/`403`/`403`/live predicate. Downstream classifiers gate on the
emitted status, so this could incorrectly allow an evidence-only
reclassification. The bounded correction belongs in the same helper because
it preserves the duplicate-removal contract while making the invalid fallback
fail closed.

## Acceptance criteria

- `full_matrix_control_evidence()` retains its API and fixed
  `ARGS_NAMES_CONTROL_CASE` behavior while delegating to the parameterized
  helper.
- A control is emitted as `pass` only for `status=pass`, expected `403`,
  actual-or-observed `403`, and `live_executed=true` together.
- `pass`/`403`/`403`/non-live and `pass`/`403`/`200`/live records are
  non-passing and cannot satisfy either downstream all-pass classifier.
- Valid Apache and NGINX live-403 controls, missing evidence, map ordering,
  evidence fields, safe-root behavior, and report output behavior remain
  compatible.
- The selected source/test diff has focused regression, syntax, whitespace,
  and security-review evidence. A later exact Draft-PR head must show zero
  new SonarQube Cloud issues and `0.0%` New-Code duplication without weakening
  scanner controls.

## Implementation decision and rationale

The fixed-case helper is now a compatibility wrapper around
`full_matrix_case_control_evidence(build_root, ARGS_NAMES_CONTROL_CASE)`.
The parameterized helper remains the sole loop and output implementation.

The success predicate itself remains explicit. Only the fallback changes: if
the producer says `pass` but the complete predicate has failed, its emitted
control state becomes `fail`. Existing producer states other than `pass` and
their evidence fields remain unchanged. This is intentionally narrower than
changing the downstream classifiers or report/readiness output logic.

The direct regression tests cover wrapper equivalence, valid live-403,
missing evidence, non-live evidence, an actual-200 false allow, the NGINX
`observed_status` compatibility path, and both classifier consumers.

## Security impact

The changed boundary consumes full-matrix summary JSON created by CI
producers, then feeds a collection-semantics classification which can affect
generated mismatch criticality and merge-readiness reporting. The repair is
fail closed: incomplete, stale, non-live, or false-allow evidence cannot
become a passing control merely because its producer status says `pass`.

The final local Codex Security diff scan covers the generator and direct test,
has complete worklist receipts, and contains zero reportable diff-induced
findings. Its retained report is
`/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/9f23ae2c5fe908cef38f203be03f93fda75a8dd7_20260729T090933Z/report.md`.
This is a CI-evidence integrity correction, not a claim of a request-path
enforcement bypass or an external hosted-CI attacker path.

## Changed files

- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `tests/test_report_conditional_remediation.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

### Tests and actual results

| Command or control | Result |
| --- | --- |
| Retained pre-fix targeted regression | failed as expected: a `pass`/`403`/`403`/non-live control was emitted as `pass`; retained SHA-256 `ef0876d194abe7258f5302263b0efa0a35f40a869cf84d2d00ad5d463427efe9`. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_report_conditional_remediation` | passed: 11 tests. |
| Selected `py_compile` for changed generator and test | passed. |
| `git diff --check origin/master` | passed after the versioned source, test, and Change Record edits. |
| Final local Codex Security diff scan | passed with complete coverage and zero reportable findings. |
| `make check-bilingual-docs` | `blocked_external_dependency`: the new record's required headings pass its validation; the isolated worktree lacks the Framework submodule targets referenced by existing repository documents. |
| `make check-doc-links` | `blocked_external_dependency`: every reported target is under the absent Framework submodule; no target from this Change Record pair is reported. |
| `make lint` | `blocked_external_dependency`: shell syntax and Parent Python compilation ran, then an existing no-CRS check could not import the absent Framework `ci/checks/catalog/no_crs_baseline.py`. |

## Runtime evidence

No connector runtime matrix, networked preparation, or report-generator run is
claimed. The direct tests exercise the pure evidence-classification contracts
without writing generated runtime reports. The normal matrix requires
generated evidence and unavailable Framework content, so it remains outside
this narrowly scoped CI source repair.

## Checks not run and rationale

- Full connector runtime matrix and report-generator execution were not run:
  they need generated evidence and the unavailable Framework content.
- Hosted GitHub Actions, SonarQube Cloud PR analysis, review, approval, merge,
  and master verification do not exist yet and are not inferred locally.

## Known limitations

The selected source repair is locally verified, but a later exact Draft-PR
head is still required for hosted checks and the requested zero-new-issue and
zero-new-duplication SonarQube Cloud measures. The task worktree intentionally
does not contain the Framework content needed by the normal runtime matrix.

## Remaining risks

The source-level fallback is now fail closed, but the final outcome remains
unverified on the hosted PR head and on current `master`. Any CI producer or
reporting behavior outside this helper's fixed source/test boundary remains
unchanged and is not claimed safe by this record.

## Final diff and review status

Local source, regression, syntax, whitespace, and complete security-diff
review evidence is present. The repository documentation and lint targets were
attempted and are blocked only by the intentionally absent Framework
submodule, as recorded above. The initial source record was pre-delivery; the
following update records the subsequently observed Draft-PR creation. No hosted
check, SonarQube Cloud PR result, approval, merge, or `master` change is
claimed.

Delivery update: [Draft PR #178](https://github.com/Easton97-Jens/ModSecurity-conector/pull/178)
was opened against `master` at `2026-07-29T09:39:18Z` from initial exact head
`7831e83b6385bd843b9320c59a34167fa1dd410a`, which equals the local and remote
task-branch commit at creation. This follow-up records the observed PR fact but
does not claim a hosted check, review, SonarQube Cloud result, approval, merge,
or `master` change. The next exact PR-head observation is required after this
Change Record follow-up is pushed.
