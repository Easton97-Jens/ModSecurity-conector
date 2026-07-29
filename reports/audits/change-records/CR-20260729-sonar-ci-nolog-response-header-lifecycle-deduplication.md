# Change Record: Parent CI Nolog and response-header report-lifecycle deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication` |
| Date (UTC) | `2026-07-29` |
| Base revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Source revision assessed | Latest local task-working-tree diff from the base revision; Draft PR #188 exists, but this record does not claim a current exact head, hosted check, or merge. |
| Boundary | Only two Parent `ci/` evidence-report generators, their narrow Parent `ci/lib` helper, one direct Parent test, this English/German Change Record pair, and paired indexes. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Targets the current Nolog/response-header CPD cluster: the 13-line connector-work-queue Markdown lifecycle, 39-line phase-work regeneration, 19-line final report-output lifecycle, and the hosted 23-line `main()` residual that initially produced ten new duplicated lines. No scanner policy or issue disposition is changed. |

## Motivation and problem statement

The current Parent `ci/` inventory reports a 71-line Nolog/response-header
duplication cluster. The duplicated code generates fixed registered reports,
temporarily customizes the Framework phase-work callback, and writes report
pairs. It can be reduced only if each generator retains its own classification,
callback behavior, marker updates, safe-root setup, report identity, and
metadata.

## Implementation decision and rationale

`ci/lib/focused_analysis_utils.py` now owns four narrow report-lifecycle
helpers: fixed connector-work-queue Markdown regeneration, fixed phase-work
regeneration with a caller-owned direction callback, and the final generated
report-pair write, plus the fixed generator entrypoint lifecycle. The latter
continues to use the established registered-path and fail-closed safe-writer
controls.

The two generators retain their own classification and `full_run_evidence`
marker updates. Their `main()` functions delegate only fixed report identity,
metadata, builder, and renderer values to the entrypoint helper. That helper
retains the former parser, root-resolution, bounded-output, safe-root,
report-root, directory, analysis, and safe-writer order. It uses the internally
fixed `GENERATED_ROOT` and deliberately accepts no caller-supplied report root.
The phase helper temporarily replaces the imported
Framework callback only while building its payload and restores the original in
`finally`, including when payload generation fails. Nolog continues to use the
dynamically imported Framework module's `as_list()` behavior for its special
case; response-header retains its separate direction rules.

The patch deliberately does not centralize queue classification, accept dynamic
report roots, names, or paths, alter Framework scripts, loosen safe-root
controls, or change a scanner rule, Quality Gate, exclusion, suppression, or
coverage policy.

## Acceptance criteria

- The selected fixed report lifecycles, including the fixed entrypoint
  lifecycle, have parameterized Parent helpers while both generators retain
  their distinct report names, metadata, callback semantics, classifications,
  and marker updates.
- Tests prove fixed registered output paths, generated metadata, safe-root
  fail-closed behavior, phase payload output, callback restoration after
  success and failure, Nolog's Framework-specific list normalization, and a
  rejected outside output path before analysis or writing.
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
| Focused report-helper and conditional-remediation tests | passed: `29` tests after the fixed entrypoint lifecycle and outside-output controls were added. |
| Focused report-helper security-control test | passed: `20` tests in the final expanded security-control review. |
| Selected-file `py_compile` with a task-owned bytecode cache | passed. |
| Both generator `--help` contracts | passed; the three former CLI options remain unchanged. |
| `git diff --check` | passed. |
| Focused final source-security review | passed: the initially too-generic report-root parameter was removed; only the internal fixed `GENERATED_ROOT`, registered paths, safe writers, and `finally` callback restoration remain in force. |
| Focused final test-security review | passed: no test-boundary control regression; outside output is rejected before analysis/writing and leaves no artifact. |
| `make check-bilingual-docs` | blocked external dependency: the check reports only pre-existing missing Framework-submodule link targets, not a changed Change Record error; no checker or link policy was weakened. |
| Full `make lint` | blocked external dependency after shell syntax and all `ci/` Python compilation passed: `check-no-crs-source-normalization` cannot import the absent Framework submodule file `ci/checks/catalog/no_crs_baseline.py`; no check was weakened. |
| Full connector/Framework runtime | not run: the isolated task worktree has no initialized Framework checkout, and the focused temporary-root tests are the narrowest applicable control. |

## Security impact

The relevant boundary is report generation from CI evidence. New helpers accept
only source-authored report identifiers and fixed report keys; they do not
accept a report-root parameter, register a dynamic root, choose dynamic
framework scripts, or bypass `resolve_output_dir()`,
`report_path_from_root()`, and `write_text_file()`. The entrypoint helper
retains the former safe-root and report-root registration sequence internally.

The phase-work helper's temporary imported-module callback mutation is scoped
by `try`/`finally`. Focused tests prove that the original callback is restored
when the framework payload builder raises. The final source-security review
found no plausible diff-introduced candidate.

## Runtime evidence

Focused tests run the report-lifecycle helpers against temporary connector and
Framework roots. They prove the writer rejects use before safe roots are
configured, writes only the registered report paths afterward, preserves
metadata, restores the temporary callback after success and a controlled
failure, and rejects an external `--output-dir` before analysis, writing, or
artifact creation. The Nolog callback test also proves that its special path
uses the dynamically imported Framework list normalizer. No connector server,
networked preparation, Framework runtime matrix, or generated repository
artifact is claimed.

## Known limitations

- This record does not claim that the broader Parent `ci/` SonarQube Cloud
  backlog is exhausted. It records one non-overlapping CPD cluster only.
- The initial PR head measured ten new duplicated lines in the entrypoint
  residual. This record documents the locally validated fixed-root extraction;
  fresh hosted SonarQube Cloud evidence is still required.
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
