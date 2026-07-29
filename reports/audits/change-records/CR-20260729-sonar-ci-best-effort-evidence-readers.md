# Change Record: Parent CI best-effort evidence-reader deduplication for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260729-sonar-ci-best-effort-evidence-readers.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-best-effort-evidence-readers` |
| Date (UTC) | `2026-07-29` |
| Base revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Source revision assessed | `b9008be7fc416d5e58a2305ab21dfacc4c7cef5f` |
| Boundary | Only Parent `ci/lib/best_effort_evidence_readers.py`, its four direct Parent `ci/` consumers, this English/German Change Record pair, and paired indexes. No `.github/`, test source, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Targets the leading current Parent `ci/` duplicate-reader cluster; no rule, Quality Gate, exclusion, or suppression is changed. |

## Motivation and problem statement

Four CI evidence/lifecycle scripts contained byte-identical best-effort JSON
object and JSONL object readers. The leading current `ci/` duplication cluster
was therefore safe to reduce only if parsing remains non-authoritative and all
caller-specific path, receipt, and status controls remain intact.

## Implementation decision and rationale

`ci/lib/best_effort_evidence_readers.py` now owns exactly two helpers:
`read_json_object()` and `read_jsonl_objects()`. The four callers import them
under their existing `read_json` and `read_jsonl` names. The helpers retain the
former behavior exactly:

- JSON is UTF-8 decoded and yields an object only; unreadable, malformed, or
  non-object input yields `{}`.
- JSONL uses UTF-8 replacement decoding; blank, malformed, and non-object
  rows are skipped, while valid object rows retain source order.

The change deliberately does not centralize path resolution, root
registration, symlink policy, receipt validation, raw-line counting, status
classification, output writes, or runtime command construction. In
particular, `report_path_safety` and `verified_full_matrix_receipt` are
stricter controls and are not replacements for this compatibility helper.

## Acceptance criteria

- The four former readers retain identical JSON/JSONL return behavior.
- The lifecycle runner's raw nonblank-line count remains independent from
  parsed-object rows.
- Missing or malformed evidence remains incomplete, partial, `UNKNOWN`, or
  otherwise non-authoritative according to each unchanged caller; it cannot
  create a successful full-matrix or merge-readiness claim.
- No path root, receipt, write, subprocess, token, workflow, Framework, MRTS,
  Gitlink, SonarQube Cloud setting, or test-source behavior changes.
- A future exact PR head must show zero new SonarQube Cloud issues and `0.0%`
  New-Code duplication without weakening any control.

## Changed files

- `ci/lib/best_effort_evidence_readers.py`
- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-best-effort-evidence-readers.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-best-effort-evidence-readers.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Selected-file `py_compile` with task-owned bytecode cache | passed. |
| Direct external master-parity harness | passed: valid, missing, malformed, scalar/list JSON; mixed JSONL; lifecycle raw-line count; and full-matrix JSONL fallback. |
| Four focused existing test modules | 107 tests passed; one snapshot integration test is `blocked_external_dependency` because the isolated Parent worktree intentionally lacks Framework `ci/lib/common.sh`. The other eight snapshot contract tests passed separately. |
| `git diff --check` | passed. |
| Formal Codex Security diff scan of the five exact source files | passed: all five worklist rows received full-file receipts; no reportable finding. |

## Security impact and residual risk

The changed code processes mutable runtime/report evidence that can influence
generated readiness outputs. Its security-relevant invariant is that permissive
parsing alone must not establish trust in a path, receipt, or successful
runtime state. The helper remains deliberately non-authoritative; each caller
retains the prior run-ID, runtime-root, output-root, fixed-matrix, strict
aggregate-receipt, and fail-closed status controls.

The security scan found no diff-introduced candidate. Existing permissive
evidence readers and caller-specific path behavior are not broadened by this
deduplication. This record does not claim to fix, suppress, or close any
unrelated security observation.

## Runtime evidence

No connector runtime, networked preparation, or full host matrix is claimed.
The direct parity harness and focused import/status tests verify the changed
reader contract without writing generated report evidence. Full runtime-matrix
execution remains outside this narrow duplicate-removal refactor.

## Known limitations

- The full connector runtime matrix requires Framework content and generated
  evidence; it was not run for this source-only compatibility refactor.
- One existing snapshot integration test cannot run in the intentionally
  unpopulated task worktree because Framework `ci/lib/common.sh` is absent.
  This is an external dependency limitation, not a changed test outcome.
- The exact hosted PR head remains required evidence for the selected
  SonarQube Cloud metrics and GitHub checks.

## Remaining risks

The source refactor still requires an exact hosted PR-head analysis to prove
that it creates no new SonarQube Cloud issue or New-Code duplication. The
missing Framework content also prevents the one existing snapshot integration
test and a full runtime matrix in this isolated worktree; neither limitation
is hidden as a passing result.

## Checks not run and rationale

- No `.github/`, Framework, MRTS, Gitlink, or unrelated Parent source was
  changed or exercised because the user restricted remediation to Parent
  `ci/` and `scripts/`.
- No package installation, networked connector build, or runtime matrix was
  run: the source change is a behavior-preserving evidence-parser extraction
  and the direct contract controls are the narrowest valid checks.
- Hosted SonarQube Cloud, GitHub Actions, review, and merge evidence are not
  inferred locally and require the eventual exact PR head.

## Final diff and review status

This record deliberately makes no claim about a push, pull request, hosted
check, review, SonarQube Cloud analysis, or merge. Those facts must be
observed at the eventual exact PR head. The formal source-security report is
retained outside the repository with the task-owned scan evidence.
