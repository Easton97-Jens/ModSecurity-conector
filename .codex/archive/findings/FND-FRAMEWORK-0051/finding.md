# FND-FRAMEWORK-0051 — Framework PR #42 Ruff formatting check fails on CPython 3.14 transition files

## Identity

| Field | Value |
| --- | --- |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P1 / not_applicable / confirmed |
| Status / feasibility | verified / already_fixed |
| Release blocker / security relevant | false / false |
| Historical failed revision | e0564d219980d62bc37162ac6c11641f289f1b71 |
| Exact fixed revision | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Exact verified Framework master | 935cf14c676a24672be5c336e92cd13457cc35c8 |
| Pull request / check | #42 / python-ci-security-quality |

## Summary

Historical Framework PR #42 head e0564d219980d62bc37162ac6c11641f289f1b71
failed GitHub Actions Python-quality run 29956021568, job 89045175402.
Deterministic Ruff lint passed, but ruff format --check failed on exactly four
CPython 3.14 transition files. This is a confirmed mechanical formatting
failure and a P1 release blocker for the required quality gate, not evidence
of a runtime defect, dependency issue, or security vulnerability.

The repository-declared format correction is included in exact PR head
2930e04e1558b5b10bdeb87a76abb077a2085566. Its Python-quality run
29962792445/job 89067507532 passes after the Ruff stages; current OSV and
SonarQube Cloud checks pass, mergeability is clean, and there are no reviews
or inline comments. The retained verification receipt is
framework-pr42-2930e04-hosted-verification.md, SHA-256
4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
PR #42 was normally merged at 2026-07-23T07:41:13Z. Exact resulting Framework
master 935cf14c676a24672be5c336e92cd13457cc35c8 has bound CI security Python
quality workflow run 29989195066 completed `success`; its tree
5df6cce7d7385a041a817ff54fae777902645f1d equals the reviewed PR-head tree.
The retained postmerge receipt is framework-pr42-20260723-postmerge-
verification.md, SHA-256
0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
The original Ruff CI failure is therefore verified, not closed.

## Observed and expected behavior

The receipt records that run 29956021568/job 89045175402 passed deterministic
Ruff lint, then failed only ruff format --check for:

- ci/checks/security/check-ci-security-contract.py
- ci/checks/security/check-python-version.py
- ci/tools/update-python-version.py
- tests/ci_security/test_update_python_version.py

The existing Python-quality job must pass with current Ruff lint and formatter
contracts unchanged. These four files must format cleanly without a Ruff rule,
formatter configuration, baseline, exclusion, suppression, quality-gate scope,
or security/test-control change.

## Impact, root cause, and remediation

The historical e056 PR #42 head could not satisfy a required Python-quality gate.
The retained receipt establishes the outcome and exact file set but not a
source diff or raw formatter output. The supported root-cause statement is
limited to those files not satisfying the existing Ruff formatting contract at
e0564d219980d62bc37162ac6c11641f289f1b71.

The Framework follow-up applied only the repository-declared Ruff formatting
correction to the four named files. It changed no Ruff configuration,
exclusion, baseline, suppression, quality gate, or security/test behavior.

The exact resulting-master Python-quality workflow now succeeds, so this
repaired non-security defect is no longer a release blocker. This does not
weaken any Ruff, CI, test, security, or quality-gate control.

## Evidence and reproduction

| Field | Value |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-e056-hosted-ci-failures.md |
| Artifact type | task_owned_framework_pr42_e056_hosted_ruff_format_failure_receipt |
| SHA-256 | 5940246feb917a3d83a7372ef09f2f54673cf506ec24d457d5dec5dfeaa381be |
| Producer command | Not recorded in the retained receipt |
| Working directory | GitHub Actions hosted runner (external); receipt retained under the task-owned Parent run root |
| Exit code / observed at | 1 / 2026-07-22 |
| Retention status | task_owned_retained_evidence |

The receipt contains no producer command, raw formatter output, or more
precise observation time. This record does not invent any of them.

Reproduce by inspecting GitHub Actions run 29956021568/job 89045175402 for
exact head e0564d219980d62bc37162ac6c11641f289f1b71, verifying the retained
receipt hash, then running the repository-declared Ruff formatter in a
separately authorized Framework task with the selected Framework interpreter.

### Resulting-master evidence

| Field | Value |
| --- | --- |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Artifact type | task_owned_framework_pr42_resulting_master_verification_receipt |
| SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Commands | RTK-wrapped GitHub PR/ref/commit/workflow/check-suite, SonarQube Cloud, and boundary-state readback; exact commands are retained in the receipt |
| Working directory / exit code / observed at | /root/git/ModSecurity-conector / 0 / 2026-07-23T07:51:09Z |
| Retention status | task_owned_retained_evidence |

The receipt records the normal `merge` of PR #42, exact master
935cf14c676a24672be5c336e92cd13457cc35c8, and successful CI security Python
quality workflow run 29989195066. It is the resulting-master evidence for the
verified transition; it does not claim separate SonarQube or Cloudflare
delivery conditions are passing.

## Acceptance criteria and validation plan

1. Only the four named files receive repository-declared Ruff formatter output;
   rules, configuration, baselines, scope, suppressions, quality gates, and
   security/test semantics remain unchanged.
2. The declared Ruff lint and ruff format --check controls pass for the
   affected scope using the selected Framework interpreter.
3. Exact PR #42 head 2930e04e1558b5b10bdeb87a76abb077a2085566 passes
   python-ci-security-quality, including the Ruff formatter stage. Historical
   failed e056 run 29956021568 is not replacement evidence.
4. PR #42 is normally merged and exact resulting-master evidence records a
   successful CI security Python quality workflow before the verified
   transition; closure is outside this update's scope.

The focused formatter diff, declared Ruff lint/format checks, affected
contracts, and fresh hosted result are recorded for the fixed exact head.

## Regression and legitimate-control tests

Regression tests:

- Repository-declared ruff format --check for the four listed files.
- Repository-declared Ruff lint for the same scope.
- GitHub Actions python-ci-security-quality on a new exact Framework PR #42
  head.

Legitimate controls:

- Deterministic Ruff lint remains passing under unchanged configuration.
- Existing CI-security contracts and Python-version behavior stay covered
  without a formatter exclusion, suppression, or quality-gate change.

## Dependencies, blockers, related findings, and residual risk

- Dependencies: none for this verified finding; closure is intentionally out
  of scope for this update.
- Blockers: none for this repaired Ruff defect.
- Related findings: FND-FRAMEWORK-0044, FND-FRAMEWORK-0046,
  FND-FRAMEWORK-0049, FND-FRAMEWORK-0050, FND-SONAR-0002, and
  FND-GITHUB-0007.

No risk is accepted for this Ruff defect. The successful resulting-master
Python-quality workflow verifies the original failure. FND-SONAR-0002 and
FND-GITHUB-0007 are separate accepted PR #42 delivery limitations; their global
records remain separately blocked, and neither limitation blocks, closes, or
otherwise alters this repaired finding. No formatter, lint, test, security, or
gate control may be weakened.

## History

- 2026-07-23T07:51:09Z — framework_pr42_resulting_master_ruff_verified:
  PR #42 was normally merged at 2026-07-23T07:41:13Z. Exact resulting Framework
  master 935cf14c676a24672be5c336e92cd13457cc35c8, whose tree
  5df6cce7d7385a041a817ff54fae777902645f1d equals the reviewed PR-head tree,
  has successful CI security Python quality run 29989195066. Retained postmerge
  verification receipt SHA-256 is
  0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
  FND-SONAR-0002 and FND-GITHUB-0007 remain separate accepted PR #42 delivery
  limitations and do not block this repaired Ruff defect.
- 2026-07-22T22:35:46Z — framework_pr42_2930_exact_head_ruff_fixed:
  exact head 2930e04e1558b5b10bdeb87a76abb077a2085566 passed Python-quality
  run 29962792445/job 89067507532 after the repaired Ruff stages. The retained
  receipt SHA-256 is
  4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
  Status is fixed only; no master merge, resulting-master evidence, Parent
  gitlink action, or MRTS action occurred.
- 2026-07-22T21:23:05Z —
  framework_pr42_e056_hosted_ruff_format_failure_tracked: after receipt review
  and deduplication, this distinct finding recorded exact head
  e0564d219980d62bc37162ac6c11641f289f1b71, run 29956021568/job
  89045175402, deterministic Ruff lint passed, and the four-file ruff format
  --check failure. No source, Git, GitHub, Parent, Framework, or MRTS action is
  claimed.
