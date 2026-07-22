# Change Record: GitHub Actions checkout v7.0.1 immutable-lock synchronization

**Language:** English | [Deutsch](CR-20260721-actions-checkout-v7-lock.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-actions-checkout-v7-lock |
| Date (UTC) | 2026-07-21 |
| Base revision | 5c26ffb698a892ffe83b7aa1749a456eae10b956 |
| Boundary | Parent GitHub Actions CI security and traceability only; Framework, MRTS, gitlinks, connector source, and historical Change Records remain unchanged. |

## Motivation and problem statement

Dependabot PR #68 updated all actions/checkout workflow references to v7.0.1
but did not update the matching reviewed entry in ci/tooling/security-tools.lock.yml.
The immutable-action contract correctly rejected the otherwise fully pinned
official SHA. This replacement carries the current bot workflow update and its
one matching lock entry atomically.

## Acceptance criteria

- Every Parent actions/checkout reference resolves to full commit
  3d3c42e5aac5ba805825da76410c181273ba90b1 with its v7 comment.
- ci/tooling/security-tools.lock.yml records the same v7.0.1 commit for
  actions/checkout.
- No older checkout SHA, mutable Action tag, unexpected action source,
  permission change, trigger change, matrix change, or weakened immutable-pin
  control remains in the scoped workflow diff.
- Focused local contracts and resulting exact replacement-PR and master checks
  pass before protected delivery is finalized.

## Implementation decision and rationale

The official actions/checkout tag API maps v7.0.1 to commit
3d3c42e5aac5ba805825da76410c181273ba90b1. The 36 current workflow references
in 23 Parent workflow files and the single matching lock entry move together.
A lock-only correction was rejected: the contract builds one set of all
recorded lock SHAs, so removing the old SHA while current workflows still used
it would correctly fail closed.

After #67 was safely merged, Dependabot refreshed #68 onto that resulting
master. The current bot head is d7ceb21aed63e7ca7257a5f247825bb02c826b30 and
its current diff contains only the intended checkout pin substitutions. The
original bot PR remains retained; its unmodifiable branch is not used for this
correction.

## Changed files

- Twenty-three scoped Parent files under .github/workflows/, containing the 36
  actions/checkout references.
- ci/tooling/security-tools.lock.yml
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- This English/German Change Record pair.

## Commands executed

| Command or evidence | Result |
| --- | --- |
| Official GitHub tag API readback for actions/checkout v7.0.1 | passed: official commit is 3d3c42e5aac5ba805825da76410c181273ba90b1. |
| gh run view 29811489361 --repo Easton97-Jens/ModSecurity-conector --log-failed | passed as evidence retrieval: exact Dependabot #68 head reproduced only the immutable-lock-membership failure. |
| Exact source-head check for #68 | passed: fetched current head was d7ceb21aed63e7ca7257a5f247825bb02c826b30; its diff contains only 36 checkout substitutions in 23 workflow files. |
| git diff --check 5c26ffb698a892ffe83b7aa1749a456eae10b956 FETCH_HEAD | passed for the fetched current Dependabot diff. |
| Retained preflight receipt | passed: pr68-current-head-lock-preflight-20260721T074704Z.json, SHA-256 52e4b85a142f2d850cbdb4b6ba552a1538c7f386296ce1728bb9f89e78338f5a. |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract | passed: all 15 CI-security workflow tests and the actionlint, zizmor, and gitleaks lock-record validations passed. |
| git diff --check on the replacement worktree | passed. |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs | blocked_environment: the intentionally unpopulated Framework gitlink caused only pre-existing missing-link reports; no new Change Record schema or parity failure was reported. |

The focused local CI-security contract and scoped diff check passed. The
full-tree documentation check is environment-blocked only by pre-existing
Framework links. Exact replacement-PR, review, SonarQube Cloud,
protected-merge, and resulting-master checks remain pending and are not
represented as passed.

## Security impact

This is a CI supply-chain integrity change. Every affected Action remains an
official full immutable commit, and the reviewed lock preserves the allowlist
relationship enforced by the existing CI-security test. Existing permissions,
triggers, action sources, scanners, branch protections, and Quality Gates are
unchanged. No security control is weakened and no risk is accepted.

## Runtime evidence

No connector runtime behavior changes. The exact failed Dependabot run proves
the legitimate block control: an unreviewed workflow SHA is rejected even when
the SHA is immutable. The paired lock update is required to permit the
officially verified release under that unchanged control.

## Known limitations

The task-owned worktree intentionally has an unpopulated Framework gitlink.
Full-tree documentation link checks may therefore be blocked only by existing
Framework links; no Framework content, gitlink, or MRTS path is part of this
change.

## Remaining risks

Pinning a verified official upstream commit does not eliminate upstream Action
risk. Immutable pinning, retained tag evidence, the reviewed lock, exact-head
CI, and protected delivery bound that dependency risk. No risk is accepted.

## Checks not run and rationale

Exact replacement-PR checks, review/thread state, SonarQube Cloud evidence,
protected squash merge, and resulting-master workflows have not yet occurred.
They remain required; no check will be bypassed. Broad connector-runtime checks
are not applicable to a workflow-pin and lock-only change. The full-tree
bilingual/documentation check is blocked_environment solely by the intentionally
unpopulated Framework gitlink.

## Final diff and review status

This is an in-progress traceability record. The scoped source decision,
official tag mapping, original failure, focused local CI-security contract, and
scoped diff review have been retained. Remote validation, protected delivery,
update of the existing FND-PARENT-0018 evidence history, and safe
Parent-workspace reconciliation remain pending.
