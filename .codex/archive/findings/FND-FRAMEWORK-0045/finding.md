# FND-FRAMEWORK-0045 — Framework PR #37 Change Record retains stale no-merge delivery instruction

- Category: `documentation_drift`
- Repository / ownership: `framework` / `framework`
- Priority / severity / confidence: `P1` / `not_applicable` / `confirmed`
- Status: `verified`
- Release blocker / security relevance: `false` / `true`

## Summary

The versioned English and German Change Records in Framework PR #37 originally said that
no `master` merge is allowed, a normal commit/push remains, and PR #37 must
remain unmerged. After their source correction, the GitHub PR description also
still named the old head, called the PR Draft, denied a merge, and said checks
were running. The exact head is already pushed and the current user has
expressly authorized Framework-only integration of PR #37. The corrected head
was normally merged as Framework master
`f73f8842f45318e2df8aff1d31855eeb7c20a22f`; this is a truthfulness and
release-readiness defect, not a product exploit.

## Observed and expected behavior

At `c1523a8f51b2647228dea44284fa8d4a7ac38710`, both
`reports/audits/change-records/20260720-03-reconcile-codex-cloud-framework-security.md`
and its German companion prohibit merging. The expected record retains the
historical Draft-PR context, preserves the direct-`master`-push prohibition,
and states that a merge is possible only through the current explicitly
authorized PR workflow after fresh exact-head validation. The GitHub PR
description must equally name current head
`1e9fa0d22639517193d450b05eb7b07193e41257`, current completed checks, and
that same conditional delivery model. On resulting master
`f73f8842f45318e2df8aff1d31855eeb7c20a22f`, the original stale phrases
(`Allow no master merge` / `the PR must remain unmerged` and their German
equivalents) are absent, while the direct-`master`-push prohibition remains.

## Impact, root cause, and remediation

This was a P1 Framework release blocker because it would make a protected,
authorized integration contradict the versioned traceability evidence. The
root cause was a historical Draft-PR restriction retained as a permanent rule.
The focused remediation updated only the paired Change Record wording and
passed documentation, security, exact-head hosted, protected-merge, and
post-merge wording checks. The independent default-branch SonarCloud Quality
Gate failure is tracked separately as `FND-SONAR-0002`.

## Evidence and reproduction

- Run: `20260721T060210Z-framework-pr-37-master-integration-6be553a4`
- Evidence: `analysis/pr37-stale-change-record-evidence.md` and
  `analysis/pr37-stale-pr-description-evidence.md`
- SHA-256: `9c6c842aa3a1658733ffc7ba4154478233690b07c4fb00c8bff5b6adb15208d4` and
  `b10f04784dba50f3c9a99b79615d7a3126107b8069cb2d10c6f78285baf205b7`
- Command: RTK-wrapped GitHub PR metadata/check review and exact-head
  Change-Record inspection, exit `0`.
- Post-merge evidence:
  `analysis/postmerge-master-sonar-triage.md`, SHA-256
  `a9a312f1ba760030ceb45644ced6b0d533fe01b9a4d2f8e19c1e832dc54b5830`.
- It records normal merge of exact source `1e9fa0d…` as master `f73f884…`,
  successful PR-head documentation/security/hosted controls, absent original
  stale wording on master, and retained direct-push protection.

Inspect the paired records at the recorded revision and the pre-correction PR
description, then compare their no-merge wording with the current user
request. The retained evidence contains the exact affected statements and
observed delivery state.

## Acceptance and validation

- English and German delivery statements remain equivalent and truthful.
- The GitHub PR description names the current head and accurately reports the
  scope, completed checks, and conditional protected-delivery rule.
- Direct `master` pushes stay prohibited; the record itself is never merge
  authority.
- The normal merge used fresh exact-head checks, Sonar, reviews, and the
  current explicit user authorization.
- Documentation and whitespace checks, the focused Framework security/
  regression set, exact-head hosted checks, and resulting-master wording
  verification passed.

The legitimate control is that the revised record still forbids direct
`master` pushes and bypasses. The bypass review confirms the wording neither
weakens protections nor self-authorizes delivery. No dependency, Parent change,
or MRTS action is required.

## Residual risk and history

This finding is verified and no longer a release blocker. `FND-SONAR-0002`
remains the separate P1 default-branch SonarCloud blocker: its master-only
failure does not reproduce the stale Change-Record defect or reopen this
finding.

- `2026-07-21T06:02:10Z`: `delivery_record_drift_confirmed` — paired PR #37
  records conflict with current Framework-only master authorization.
- `2026-07-21T07:01:09Z`: `delivery_metadata_drift_confirmed_and_corrected` —
  the stale PR description was replaced without changing the PR source head.
- `2026-07-21T07:28:49Z`: `verified_after_pr37_normal_merge_and_scoped_reproduction` —
  exact source `1e9fa0d…` merged normally as `f73f884…`; the original stale
  phrases are absent on master and the direct-push control remains present.
