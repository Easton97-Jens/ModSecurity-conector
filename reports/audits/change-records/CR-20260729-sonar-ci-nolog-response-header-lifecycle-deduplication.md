# Change Record: Parent CI Nolog and response-header report-lifecycle deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication` |
| Date (UTC) | `2026-07-29` |
| Base revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Source revision assessed | Local task-working-tree diff from the base revision; no commit, push, pull request, hosted check, or merge is claimed at record creation. |
| Boundary | Only two Parent `ci/` evidence-report generators, their narrow Parent `ci/lib` helper, one direct Parent test, this English/German Change Record pair, and paired indexes. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Targets the current Nolog/response-header CPD cluster: the 13-line connector-work-queue Markdown lifecycle, 39-line phase-work regeneration, and 19-line final report-output lifecycle. No scanner policy or issue disposition is changed. |

## Motivation and problem statement

The current Parent `ci/` inventory reports a 71-line Nolog/response-header
duplication cluster. The duplicated code generates fixed registered reports,
temporarily customizes the Framework phase-work callback, and writes report
pairs. It can be reduced only if each generator retains its own classification,
callback behavior, marker updates, safe-root setup, report identity, and
metadata.

## Implementation decision and rationale

`ci/lib/focused_analysis_utils.py` now owns three narrow report-lifecycle
helpers: fixed connector-work-queue Markdown regeneration, fixed phase-work
regeneration with a caller-owned direction callback, and the final generated
report-pair write. The latter continues to use the established registered-path
and fail-closed safe-writer controls.

The two generators retain their own classification and `full_run_evidence`
marker updates. Their CLI entry points still configure output and report roots
before invoking any helper. The phase helper temporarily replaces the imported
Framework callback only while building its payload and restores the original in
`finally`, including when payload generation fails. Nolog continues to use the
dynamically imported Framework module's `as_list()` behavior for its special
case; response-header retains its separate direction rules.

The patch deliberately does not centralize queue classification or CLI setup,
accept dynamic report names or paths, alter Framework scripts, loosen safe-root
controls, or change a scanner rule, Quality Gate, exclusion, suppression, or
coverage policy.

## Acceptance criteria

- The selected fixed report lifecycles have one parameterized Parent helper
  each, while both generators retain their distinct report names, metadata,
  callback semantics, classifications, marker updates, and safe-root setup.
- Tests prove fixed registered output paths, generated metadata, safe-root
  fail-closed behavior, phase payload output, callback restoration after
  success and failure, and Nolog's Framework-specific list normalization.
- The exact future pull-request head must report zero new SonarQube Cloud
  issues, zero new duplicated lines, and `0.0%` New-Code duplication without
  changing scanner policy.
- No default-branch integration occurs without separate explicit user
  authorization.

## Changed files

- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/lib/focused_analysis_utils.py`
- `tests/test_focused_analysis_utils.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused report-helper and conditional-remediation tests | passed: `27` tests. |
| Focused report-helper security-control test | passed: `18` tests after the Nolog-specific callback control was added. |
| Selected-file `py_compile` with a task-owned bytecode cache | passed. |
| `git diff --check` | passed. |
| Focused final source-security review | passed: no plausible diff-introduced security finding; fixed registered paths, safe writers, local root setup, and `finally` callback restoration remain in force. |
| Focused final test-security review | passed: no test-boundary control regression; the Nolog-specific callback control is isolated and does not write files. |
| `make check-bilingual-docs` | blocked external dependency: the check reports only pre-existing missing Framework-submodule link targets, not a changed Change Record error; no checker or link policy was weakened. |
| Full `make lint` | blocked external dependency after shell syntax and all `ci/` Python compilation passed: `check-no-crs-source-normalization` cannot import the absent Framework submodule file `ci/checks/catalog/no_crs_baseline.py`; no check was weakened. |
| Full connector/Framework runtime | not run: the isolated task worktree has no initialized Framework checkout, and the focused temporary-root tests are the narrowest applicable control. |

## Security impact

The relevant boundary is report generation from CI evidence. New helpers accept
only source-authored report identifiers and fixed report keys; they do not
register roots, choose dynamic framework scripts, or bypass
`report_path_from_root()` and `write_text_file()`. The callers retain their
existing `resolve_output_dir()`, `add_safe_roots()`, and `add_report_roots()`
sequence.

The phase-work helper's temporary imported-module callback mutation is scoped
by `try`/`finally`. Focused tests prove that the original callback is restored
when the framework payload builder raises. The final source-security review
found no plausible diff-introduced candidate.

## Runtime evidence

Focused tests run the report-lifecycle helpers against temporary connector and
Framework roots. They prove the writer rejects use before safe roots are
configured, writes only the registered report paths afterward, preserves
metadata, and restores the temporary callback both after success and after a
controlled failure. The Nolog callback test also proves that its special path
uses the dynamically imported Framework list normalizer. No connector server,
networked preparation, Framework runtime matrix, or generated repository
artifact is claimed.

## Known limitations

- This record does not claim that the broader Parent `ci/` SonarQube Cloud
  backlog is exhausted. It records one non-overlapping CPD cluster only.
- The safety-preserving entry-point portion of the reported CPD remains a
  separately evaluated future candidate; moving CLI root setup merely to force
  a larger deduplication is intentionally out of scope.
- Hosted GitHub Actions and SonarQube Cloud evidence must be re-read at the
  exact pull-request head after every head update.

## Delivery-status reconciliation

Draft PR [#188](https://github.com/Easton97-Jens/ModSecurity-conector/pull/188)
was created from the initial task commit
`ed06eb84a07b0d50988dc308087e85da589311e1`. This documentation-only follow-up
advances that PR head, so its final exact local/remote/PR head equality and
fresh hosted evidence must be re-read before any integration decision. No
hosted check, review, thread, mergeability result, or merge is claimed here.

## Remaining risks

The shared-helper boundary depends on the existing trusted Parent and Framework
report roots. This patch neither broadens those roots nor claims to remove the
repository-wide trusted-artifact-root TOCTOU assumption. The current
SonarQube Cloud report is a selection input, not proof of the future PR's
exact-head result.

## Checks not run and rationale

- A complete Framework runtime was not run because the isolated task worktree
  lacks the initialized Framework checkout required by existing repository
  checks. No check was weakened; direct owner tests, compilation, whitespace,
  and focused security review were used instead.
- Hosted GitHub Actions, SonarQube Cloud, review, thread, mergeability, and
  merge checks cannot be claimed until a committed exact PR head exists.

## Final diff and review status

The local diff has focused tests, compilation, whitespace validation, completed
source/test security reviews with no reportable candidate, and a bilingual
documentation check that is blocked only by pre-existing absent Framework
submodule targets. Task-owned Draft PR #188 exists; its final exact committed
head and hosted checks remain pending. No default-branch action is authorized
or implied.
