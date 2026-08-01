# FND-CROSS-0007 — Parent and Framework task delivery did not bind origin effective push destination to the expected user repository

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-CROSS-0007` |
| Category | `security_hardening` |
| Repository | `parent_and_framework` |
| Ownership | `cross_repository` |
| Priority | `P2` |
| Severity | `low` |
| Confidence | `validated` |
| Status | `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevance | `true` |

## Summary, observed behavior, and impact

The normal Parent and Framework task-branch delivery path displayed remote
configuration but did not require both origin fetch and effective push URL,
expected GitHub identity, writable permission, archive state, and default
branch before branch creation, push, PR, or remote deletion. A mismatched
`origin.pushurl` could therefore evade a display-only preflight.

The scoped governance scan found display-only `git remote` evidence before
`git push -u origin` and PR creation, without an invariant that the effective
push URL resolves to the expected `Easton97-Jens` repository. A local operator
error or hostile local Git configuration could therefore redirect task-branch
delivery/deletion. No attacker-controlled delivery sink or outbound misuse was
demonstrated: this is low-severity governance hardening, not a runtime exploit.

## Expected behavior and affected boundary

Before every delivery-branch creation, push, PR action, or remote-branch
deletion, the owning repository must verify origin fetch and effective push
URLs against the exact expected user repository, GitHub identity, non-archived
writable state, and default branch, and stop as `blocked_remote_mismatch` on
any mismatch.

Affected paths are `AGENTS.md`, `.codex/context/git-policy.md`,
`.codex/context/fork-and-upstream-policy.md`,
`.codex/context/delivery-and-ci-policy.md`, and their Framework equivalents
under `modules/ModSecurity-test-Framework/`. Affected controls are the
Parent/Framework delivery destination preflight, origin effective push URL,
and `blocked_remote_mismatch`.

## Preconditions and safe reproduction

This applies when an authorized Parent/Framework delivery action is about to
create a branch, push, create/update a PR, or delete a remote branch and an
origin fetch URL, `origin.pushurl`/effective push URL, or GitHub identity
differs from the expected repository while the task relies only on display
evidence.

Inspect the retained scan report and pre-fix delivery policies. Then run the
focused audits and Framework negative fixture after the patch: a direct-master
weakening in `git-policy.md` is now read by the audit and remote-preflight text
requires both URLs and GitHub identity. Do not mutate a remote or perform an
outbound/malicious push merely to demonstrate this governance control.

## Evidence

- Run ID: `20260724T170026Z-worktree-cleanup-governance`
  - Path: `/var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-conector/30ee953b_20260724T170026Z-worktree-cleanup-governance/report.md`
  - Type: `scoped_governance_security_scan_final_report`
  - SHA-256: `83f0006b91b2831ce0b8067c07e3af13b7be55fb82af957bdd2eba6465c5d914`
  - Command: RTK-wrapped scoped Codex Security review of the 35 governance
    paths; final report and deterministic work ledger
  - Working directory: `/root/git/ModSecurity-conector`
  - Exit code: `0`; observed: `2026-07-24T17:00:26Z`
  - Retention: `external_retained_task_evidence`

The review deliberately did not mutate `origin.pushurl`, push to a remote, or
claim runtime enforcement. It proves the previous policy omission and the
current local policy/audit remediation only.

## Root cause and proposed remediation

The Parent policy mislabeled its Git authority and referenced missing routes;
Parent and Framework delivery treated remote display as sufficient evidence
rather than binding the effective push destination and GitHub repository
identity at each remote-action boundary.

The local remediation adds repository-local fork-and-upstream policies with
accepted HTTPS/SSH URLs, effective-push URL and GitHub
identity/permission/default-branch preflight, routes AGENTS/Git/delivery/
restoration through them, and requires `blocked_remote_mismatch` on any
discrepancy. It preserves normal task-branch origin delivery and prohibits
upstream delivery/deletion.

## Acceptance criteria and validation

- Parent and Framework instructions require exact origin fetch/effective-push
  URLs plus GitHub identity, permission, archive, and default-branch readback
  before a delivery branch, push, PR action, or remote deletion.
- A mismatch is blocked without remote rewrite, fallback push, PR creation, or
  remote deletion.
- MRTS retains its stricter `Easton97-Jens/MRTS` origin-only rule; no policy
  grants upstream push/delete or Gitlink update.
- Parent and Framework local policy audits and focused tests pass.

Completed validation: Parent audit `all` and 57 focused audit tests passed;
Framework audit and 22 focused audit tests passed, including the
`git-policy.md` weakening fixture. Regression tests are Parent
`.codex/tests/test_audit_policies.py`, Framework
`.codex/tests/test_audit_policies.py::test_git_policy_weakening_is_not_omitted_from_audit`,
and Framework
`.codex/tests/test_audit_policies.py::test_missing_git_policy_is_missing_delivery_coverage`.

Legitimate controls showed expected Parent, Framework, and MRTS origin
fetch/effective-push URLs at preflight and a valid Framework fixture that
remains consistent while a direct-master weakening is detected.

## Dependencies, residual risk, and history

Dependencies and blockers: none. Related finding: `FND-FRAMEWORK-0055`.
The policies/audits are governance controls, not host-side interceptors. A
future authorized delivery must still retain live remote/GitHub readback; no
remote rewrite, upstream push, or default-branch push occurred here.

- `2026-07-24T17:00:26Z` — `scoped_governance_scan_validated_control_gap`:
  the deterministic 35-path security review recorded this low-severity gap.
- `2026-07-24T18:15:00Z` — `local_policy_remediation_and_audit_passed`:
  Parent/Framework fork, Git, delivery, restoration, cleanup, and routing
  controls were updated; audits/tests passed without remote-state change.

Final disposition: `fixed_local_governance_controls_pending_future_live_delivery_proof`.
