# FND-FRAMEWORK-0055 — Framework policy auditor could omit the active Git policy while reporting broad control-plane coverage

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0055` |
| Category | `security_hardening` |
| Repository | `framework` |
| Ownership | `framework` |
| Priority | `P2` |
| Severity | `low` |
| Confidence | `verified` |
| Status | `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevance | `true` |

## Summary and behavior

The Framework local policy auditor built its read set from `DOMAIN_SPECS` but did not include active `git-policy.md`. A direct-master-push weakening written only there could be omitted from the `all_text` forbidden-language scan while the audit reported broad coverage.

The security review confirmed that `DOMAIN_SPECS` omitted `git-policy.md`; the forbidden weakening loop therefore did not read that Git authority. A local governance change could weaken Git safety and produce misleading audit evidence. No automated delivery sink consumed the audit result, so this is low-severity control-coverage hardening rather than a demonstrated exploit.

## Expected behavior and scope

A Framework policy audit that claims delivery/Git safety coverage must read active `git-policy.md` and reject forbidden weakening there, while retaining its structural-only proof boundary.

Affected files: `modules/ModSecurity-test-Framework/.codex/bin/audit-policies`, `modules/ModSecurity-test-Framework/.codex/tests/test_audit_policies.py`, and `modules/ModSecurity-test-Framework/.codex/context/git-policy.md`. Affected symbols: `DOMAIN_SPECS.delivery`, `FORBIDDEN_PATTERNS`, and `test_git_policy_weakening_is_not_omitted_from_audit`.

## Preconditions and reproduction

The precondition is a Framework control-plane change that modifies `git-policy.md` with prohibited Git weakening language while a task relies on the old audit consistency result. Inspect the retained scan report and pre-fix inventory. Run the new fixture appending `Direct push to master is permitted.` only to `git-policy.md` and confirm `forbidden_weakening_language` becomes conflicting. Run the normal Framework audit to confirm the valid control plane remains consistent.

## Evidence

- Run ID: `20260724T170026Z-worktree-cleanup-governance`
  - Path: `/var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-conector/30ee953b_20260724T170026Z-worktree-cleanup-governance/report.md`
  - Type: `scoped_governance_security_scan_final_report`
  - SHA-256: `83f0006b91b2831ce0b8067c07e3af13b7be55fb82af957bdd2eba6465c5d914`
  - Command: RTK-wrapped scoped Codex Security review of Framework audit source, policy authority, and focused test coverage
  - Working directory: `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework`
  - Exit code: `0`; observed: `2026-07-24T17:00:26Z`; retention: `external_retained_task_evidence`

The audit is intentionally a local structural consistency tool. Its passing result does not prove runtime Git, GitHub, access-control, or sandbox enforcement.

## Root cause and remediation

The delivery domain enumerated `delivery-and-ci-policy.md` but not `git-policy.md`; its forbidden-pattern scan only examined text loaded through declared domains.

The local remediation includes `git-policy.md` and `fork-and-upstream-policy.md` in the delivery-domain file inventory, then adds fixtures proving a direct-master-push weakening in `git-policy.md` is detected and a missing `git-policy.md` makes delivery coverage missing.

## Acceptance and validation

- `DOMAIN_SPECS` reads `git-policy.md` as delivery coverage.
- A forbidden direct-master-push phrase in that file produces conflicting `forbidden_weakening_language`.
- Removing that file produces missing delivery coverage.
- The normal Framework audit and focused tests pass without weakening the structural-only scope statement.

Completed validation: Framework audit passed with all domains covered, and 22 focused tests passed including `test_git_policy_weakening_is_not_omitted_from_audit` and `test_missing_git_policy_is_missing_delivery_coverage`. Legitimate controls were the complete valid fixture and the ordinary Framework control-plane audit.

## Dependencies, residual risk, and history

Dependencies and blockers: none. Related finding: `FND-CROSS-0007`. The audit now reads active Git authority but remains a textual consistency check; a future task still requires real worktree, remote, PR, and Gitlink evidence before delivery/deletion.

- `2026-07-24T17:00:26Z` — `scoped_governance_scan_validated_audit_omission`: the deterministic review recorded this audit omission.
- `2026-07-24T18:15:00Z` — `audit_inventory_and_negative_regressions_added`: the delivery domain reads Git/fork policy and the new negative fixtures plus ordinary audit passed.

Final disposition: `fixed_local_audit_coverage_pending_future_delivery_context`.
