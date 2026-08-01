# FND-GITHUB-0005 — Framework master governance and Actions defaults lack external enforcement

## Identity

| Field | Value |
| --- | --- |
| ID | FND-GITHUB-0005 |
| Title | Framework master governance and Actions defaults lack external enforcement |
| Category | github_governance |
| Repository | framework |
| Ownership | github_configuration |
| Priority | P1 |
| Severity | not_applicable |
| Confidence | validated |
| Status | accepted_risk |
| Feasibility | out_of_scope |
| Release blocker | true |
| Security relevance | true |

## Summary, observed behavior, and impact

The Framework PR #27 source correctly constrains pull-request CodeQL to an
exact, credentialless, read-only head without upload, and keeps the trusted
uploader outside pull-request triggering with only security-events write.
Those source controls are valid defense in depth, but they do not independently
force later master or workflow changes to retain the same declarations.

For Easton97-Jens/ModSecurity-test-Framework at exact reviewed head
2f635be02ede802024ec9e0ce2ed41e3030cbff2, the retained read-only GitHub
configuration receipt proves:

- classic master protection returns HTTP 404 Branch not protected;
- master reports protected=false and no required checks;
- repository rulesets and effective master rules are empty;
- Actions default_workflow_permissions is write; and
- one direct collaborator has admin, maintain, and push capabilities.

The result is a real GitHub-governance and master-integration control gap. A
privileged collaborator or compromised privileged credential can change master
or the workflow adjudicating a change without an evidenced independent PR,
review, or current-head check. No unauthenticated RCE, write-capable PR token,
secret exposure, Parent gitlink action, or MRTS action is claimed.

The completed attack-path analysis intentionally does not call this a
reportable security vulnerability: the only demonstrated attacker already has
privileged repository-write authority and no lower-privilege escalation is
proved. That policy result does not establish the missing hosted governance
control and does not make master delivery safe.

## Expected behavior, affected scope, preconditions, and reproduction

GitHub must independently enforce no-bypass master protection or rules,
current-head pull-request/review/required-check requirements, and
least-privilege Actions defaults. The present source-controlled workflow
permissions remain defense in depth rather than a substitute for that hosted
control.

Affected source context:

- .github/workflows/ci-security-codeql-pr.yml
- .github/workflows/ci-security-codeql.yml

The observed path requires a malicious privileged collaborator or compromised
privileged credential. No lower-privileged external or fork-PR path is
evidenced.

~~~bash
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master/protection
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rulesets
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rules/branches/master
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/actions/permissions/workflow
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/collaborators?affiliation=direct
~~~

## Evidence

- Run ID: 20260719T081017Z-framework-pr-resolution-20260719-840082e0
  - Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/framework-github-governance-readback-20260719T160637Z.md
  - Type: github_master_governance_read_only_configuration_receipt
  - SHA-256: 1cbdf30f5a0dfe329c354f753cce92f037067d92ba8ccd9435e6efe08ee1d354
  - Command: rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master/protection; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rulesets; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rules/branches/master; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/actions/permissions/workflow; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/collaborators?affiliation=direct
  - Working directory: /var/tmp/codex/worktrees/framework-ci-security; exit code: 0; observed at 2026-07-19T16:06:37Z; retention: retained_task_evidence.

The diff scan report is at /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/analysis/security-diff-pr27-final-sync/report.md. Its candidate CAND-PR27-GITHUB-GOVERNANCE-001 has discovery, validation, and attack-path receipts. The attack-path final policy is ignore because the demonstrated source is privileged-only; this finding preserves the distinct release-control disposition.

## Root cause, remediation, and acceptance criteria

The root cause is external GitHub control-plane configuration. The Framework
workflow source constrains the current PR, but GitHub does not independently
require future master or workflow changes to preserve its permissions,
exact-head checkout, or upload separation. Missing protection/effective rules
and a write Actions default are distinct from the current safe PR source.

Only an authorized GitHub repository owner or administrator may decide and
apply the remedy:

1. establish no-bypass master protection or rules;
2. require current-head PR, review, and required-check enforcement; and
3. set least-privilege default Actions workflow permissions.

Then reread the same endpoints and repeat exact-head PR #27 delivery
verification. Do not direct-push master, use an administrator bypass, weaken a
check, or infer risk acceptance from a merge request.

Acceptance criteria:

- A post-change read-only receipt proves no-bypass master protection or
  effective rules exist.
- The rule requires intended current-head PR, review, and required-check
  controls without a direct-push or administrator bypass.
- The Actions endpoint reports a least-privilege default instead of
  default_workflow_permissions=write.
- PR #27 is re-read at its exact current head and satisfies all delivery,
  review, thread, ruleset, and merge-method requirements.
- No Parent source/gitlink, MRTS content/gitlink, Framework source, security
  control, or SonarCloud result is weakened as a workaround.

## Validation, dependencies, blockers, related findings, residual risk, and history

Validation requires a fresh hash-addressed API readback, review of the
effective master rule and bypass settings, a re-run of exact-head PR #27
preflight, and confirmation that the existing PR and trusted CodeQL workflows
remain legitimate controls.

Dependencies: an explicit current-user decision authorizing the GitHub
configuration change, or an explicit acceptance of the precise residual
governance risk; plus a GitHub repository owner or administrator capable of
applying and rereading the configuration.

Blockers: this task has no explicit authority to change branch protection,
rulesets, bypass settings, or Actions defaults; the receipt proves the
prerequisites are absent. The current user's accepted-risk archive decision
does not remediate the remaining direct-master/check-bypass risk.

Related but distinct records are FND-GITHUB-0001, FND-GITHUB-0002,
FND-GITHUB-0004, FND-FRAMEWORK-0013, and FND-FRAMEWORK-0019.

Before the current user's 2026-07-26 archive decision, no risk was accepted.
Until an authorized configuration decision and endpoint reread occur, a
privileged collaborator or compromised privileged credential can bypass the
independently enforced master review/current-head-check boundary required for
safe integration. Current PR controls remain valid, but are not an external
no-bypass guarantee.

History:

- 2026-07-19T16:06:37Z: Read-only API evidence recorded the absent master
  protection/rules and write Actions default.
- 2026-07-19T16:35:35Z: CAND-PR27-GITHUB-GOVERNANCE-001 completed discovery,
  validation, and attack-path analysis. The security policy ignored it as
  privileged-only; the independent master-integration governance requirement
  remains blocked.

## Current user accepted-risk archive disposition — 2026-07-26

At `2026-07-26T14:18:25Z`, the current user explicitly accepted this exact
residual risk for local archival. Until an authorized GitHub configuration
decision and endpoint reread occur, a privileged collaborator or compromised
privileged credential can bypass the independently enforced master
review/current-head-check boundary. No rule, protection, bypass, or
Actions-default setting changed. This status is `accepted_risk`, not `closed`;
restore and revalidate the record before production, publication, or release
use.
