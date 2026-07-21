# Change Record: GitHub Actions setup-python v7 immutable-lock synchronization

**Language:** English | [Deutsch](CR-20260721-actions-setup-python-v7-lock.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-actions-setup-python-v7-lock |
| Date (UTC) | 2026-07-21 |
| Base revision | 1fa024ca6ec97023ea5b6f7dff5215e43f10b74c |
| Boundary | Parent GitHub Actions CI security and traceability only; Framework, MRTS, gitlinks, connector source, and historical Change Records remain unchanged. |

## Motivation and problem statement

Dependabot PR #67 updated all actions/setup-python workflow references from
v6.3.0 to v7.0.0 but did not update the matching reviewed entry in
ci/tooling/security-tools.lock.yml. The immutable-action contract correctly
rejected the otherwise fully pinned official SHA. This replacement carries the
same current workflow update and its one matching lock entry atomically.

## Acceptance criteria

- Every Parent actions/setup-python reference resolves to full commit
  5fda3b95a4ea91299a34e894583c3862153e4b97 with its v7.0.0 comment.
- ci/tooling/security-tools.lock.yml records the same v7.0.0 commit for
  actions/setup-python.
- No v6.3.0 setup-python reference, mutable Action tag, unexpected action
  source, permission change, trigger change, matrix change, or weakened
  immutable-pin control remains in the scoped workflow diff.
- Focused local contracts and resulting exact replacement-PR and master checks
  pass before protected delivery is finalized.

## Implementation decision and rationale

The official actions/setup-python tag API maps v7.0.0 to commit
5fda3b95a4ea91299a34e894583c3862153e4b97. The 25 current workflow references
in 19 Parent workflow files and the single matching lock entry move together.
A lock-only correction was rejected: the contract builds one set of all
recorded lock SHAs, so removing the old SHA while current workflows still used
it would correctly fail closed.

The replacement deliberately excludes two historical Change Records altered on
the stale Dependabot branch. Those documents contain delivery facts unrelated
to this Action update and must retain their already observed history.

## Changed files

- Nineteen scoped Parent files under .github/workflows/, containing the 25
  actions/setup-python references.
- ci/tooling/security-tools.lock.yml
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- This English/German Change Record pair.

## Commands executed

| Command or evidence | Result |
| --- | --- |
| Official GitHub tag API readback for actions/setup-python v7.0.0 | passed: official commit is 5fda3b95a4ea91299a34e894583c3862153e4b97. |
| gh run view 29806178964 --repo Easton97-Jens/ModSecurity-conector --log-failed | passed as evidence retrieval: exact Dependabot #67 head reproduced only the immutable-lock-membership failure. |
| Exact source-head check for #67 | passed: fetched head was d09a47e19cbe2888dfaca83267513a8ba7722068; its workflow substitutions were reviewed before reapplying only their current Parent workflow scope. |
| git diff --check 1fa024ca6ec97023ea5b6f7dff5215e43f10b74c FETCH_HEAD | passed for the fetched Dependabot diff. |
| Retained preflight receipt | passed: action-pin-lock-preflight-20260721T072315Z.json, SHA-256 01e11033d3ccbe1c3a9aa0f60e99e28116d35ae232970520997bd1913fc30e33. |
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
