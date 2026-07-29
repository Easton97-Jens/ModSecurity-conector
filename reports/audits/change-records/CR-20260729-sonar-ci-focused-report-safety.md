# Change Record: Parent CI focused-report helper deduplication and request-body path containment

**Language:** English | [Deutsch](CR-20260729-sonar-ci-focused-report-safety.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-focused-report-safety` |
| Date (UTC) | `2026-07-29` |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Source revision assessed | Local working-tree diff from the base revision. The sealed initial focused source/test snapshot is `codex-security-snapshot/v1:sha256:c18a44b023c66ffc8ae6489f0735941d7d95ab635d055e9e1543525badd8ce8b`; the final diff also has a supplemental Nolog import-only review. |
| Boundary | Only the four listed Parent `ci/` report generators, `ci/lib/focused_analysis_utils.py`, their direct Parent test, this English/German Change Record pair, and paired indexes. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Targets two current `python:S1192` body-processor literals and the exact `action_value`/`log_paths` duplication blocks selected from Parent `ci/`; no scanner policy or issue disposition is changed. |

## Motivation and problem statement

The current Parent `ci/` inventory contains two body-processor `python:S1192`
literal findings and duplicate parsing/path-selection helpers across the
selected focused report generators. These are safe to reduce only when the helpers keep
their former first-match, ordering, and safe-root behavior exactly.

During the required security review, a separate pre-existing defect was
reproduced through the real body-processor report boundary: an
artifact-derived traversal-shaped `case_id` selected an out-of-root
`conf/request-body.bin`, whose bytes, preview, and SHA-256 propagated into the
generated record. The canonical local finding is `FND-PARENT-0065`; this
Change Record does not close it or claim hosted verification.

## Implementation decision and rationale

`ci/lib/focused_analysis_utils.py` now owns the behaviorally identical
`action_value()` and `log_paths()` helpers. The four affected report generators
import the helper they use directly: `action_value()` is shared by all four,
and `log_paths()` by the three evidence-log consumers. The exact body-processor literals `multipart/form-data` and
`conf/modsecurity-smoke.conf` are owned by named constants, preserving every
prior comparison and generated path.

The narrow security repair is at the derived request-body read boundary.
`generated_body_length()` and `request_body_bytes()` now call the existing
`safe_existing_file()` control before using the candidate. That preserves an
ordinary in-root generated body, while traversal or a symlink resolving outside
registered roots follows the pre-existing request-body fallback instead of
reading the candidate.

The patch deliberately does not reject all case-ID text globally, alter
safe-root registration, change evidence/output roots, centralize unrelated
report behavior, alter subprocess/import paths, or weaken a validation control.

## Acceptance criteria

- The four former `action_value()` implementations retain case-insensitive,
  first-match value selection and the `"-"` fallback.
- The former `log_paths()` behavior retains evidence insertion order, accepted
  keys, and the `safe_existing_file()` gate.
- The two selected literals retain their exact strings and existing output
  behavior.
- A traversal-derived request-body path and an in-root symlink resolving
  outside safe roots cannot disclose the outside sentinel through the report.
- An ordinary in-root generated request body remains available.
- The exact future PR head must show zero new SonarQube Cloud issues and
  `0.0%` New-Code duplication, with no rule, Quality Gate, exclusion,
  suppression, or coverage-policy change.

## Changed files

- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/lib/focused_analysis_utils.py`
- `tests/test_focused_analysis_utils.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-focused-report-safety.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-focused-report-safety.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Pre-fix focused regression | passed as a reproducer: the test failed exactly because `outside-root-sentinel` reached the body preview. |
| Controlled pre-fix path probe | passed as a reproducer: `vulnerability_reproduced` was `true`; the out-of-root sentinel hash equaled the generated record hash, while an in-root control remained readable. |
| Focused utility regression/control suite | passed: `14` tests, including traversal, symlink, and legitimate in-root controls. |
| Conditional-remediation report suite | passed: `9` tests. |
| Presentation-literal report suite | passed: `3` tests. |
| Controlled post-fix path probe | passed: `vulnerability_reproduced` is `false`; traversal and symlink both use `fallback-body`, and the in-root body remains readable. |
| Selected-file `py_compile` with task-owned bytecode cache | passed. |
| `git diff --check origin/master` | passed. |
| Formal Codex Security final diff review | passed: the initial five-file review and the supplemental Nolog import-only review found no diff-introduced candidate. |
| Full `make lint` | blocked before changed-source execution because the isolated task worktree lacks the Framework submodule file `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`; no check was weakened. |

## Security impact

The relevant invariant is that artifact-derived paths may reach a read only
after canonical safe-root validation. Before the change,
`request_body_bytes()` bypassed that control and read the derived candidate
directly. The local patch restores the existing control at the narrowest
read/byte-sink boundary.

The combined final and supplemental security review found no newly introduced candidate. The current
repository-wide safe-file model still has its documented ordinary TOCTOU
assumption for trusted artifact roots; that condition predates this patch and
was neither broadened nor presented as fixed here.

## Runtime evidence

No connector runtime, networked preparation, or full host matrix is claimed.
The retained probes exercise the actual report-generator metadata boundary in
a temporary, safe-root-constrained filesystem without writing generated report
artifacts. The formal final source-security report is retained outside the
repository in the task-owned security-scan evidence directory.

## Known limitations

- The isolated task worktree has no initialized Framework checkout, so full
  `make lint` is blocked before the changed source; focused owning checks are
  retained separately.
- This Change Record does not claim that the broad current Parent `ci/`
  backlog is exhausted; it records only this non-overlapping CI-A cluster.

## Delivery-status reconciliation

PR #175 was created from this scoped change after its initial local-evidence
snapshot. This record retains that local evidence only; current exact-head
GitHub Actions, SonarQube Cloud, review, thread, and merge evidence is retained
by the controlled-integration task and must be rechecked after every head
update. It does not claim that a hosted result completed for an earlier head is
still valid for a later one.

## Remaining risks

`FND-PARENT-0065` remains `validated` until its lifecycle receives the
required exact-head delivery evidence. Local tests and probes prove that the
current working-tree patch closes the recorded reproduction, but this record
does not by itself assert current exact-head commit, push, PR, hosted-check,
hosted SonarQube Cloud, review, thread, or merge status. The pre-existing
trusted-artifact-root TOCTOU assumption also remains outside this narrow patch.

## Checks not run and rationale

- Hosted GitHub Actions, exact-head SonarQube Cloud issue/duplication results,
  review, thread, and merge status were not performed at the initial local
  snapshot stage; the controlled-integration task rechecks them against the
  current exact PR head.
- No connector runtime, networked preparation, or full host matrix was run:
  the source change is a focused CI evidence/report repair, and the retained
  real-boundary probes are the narrowest relevant runtime evidence.

## Final diff and review status

The working-tree diff is locally validated and has a completed combined
security review with zero reportable diff findings. The task-owned PR now exists;
its current exact committed head must be rechecked for current master base,
GitHub Actions, SonarQube Cloud, reviews, threads, and mergeability. No
default-branch action is authorized or implied.
