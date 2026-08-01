# FND-FRAMEWORK-0019 — Framework CI-security workflows are incompatible with the canonical strict YAML workflow-security contract

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0019` |
| Category | `security_hardening` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P2` / `medium` |
| Confidence / status | `validated` / `verified` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary and distinct boundary

## 2026-07-26 current-master verification

The retained #27/#29 pre-fix syntax diagnostics below are historical. Framework
master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` now passes the strict
fail-closed checker, focused flow-style negative controls, and legitimate
block-mapping/action-pin controls. PR #27 exact-head and resulting-master
hosted checks were observed successful; the strict YAML rule was not waived or
weakened.

After PR #27 was reconciled with the #29 workflow checker, its CI-security
workflows retained flow-style YAML collections. The canonical checker
deliberately rejects those collections fail-closed because canonical block
mappings keep workflow permissions and action pins reviewable. This is a
distinct syntax-contract boundary: it is not the `FND-FRAMEWORK-0013`
least-privilege permission invariant and it is not the
`FND-FRAMEWORK-0016` downloader-locking boundary.

The scope includes `.github/workflows/ci-security-codeql.yml`,
`ci-security-dependency-review.yml`, `ci-security-osv.yml`,
`ci-security-quality.yml`, `ci-security-scorecard.yml`,
`ci-security-secrets.yml`, and `ci-security-workflow-lint.yml`; the same
diagnostic also records the related flow-style collection in
`.github/workflows/cleanup-artifacts.yml`. The checker and its focused
contract tests are `ci/checks/security/check-github-actions-workflows.py` and
`tests/ci_security/test_framework_ci_security_contract.py`.

## Evidence and reproduction

The retained pre-fix evidence is:

- Run ID: `20260719T081017Z-framework-pr-resolution-20260719-840082e0`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr27-pre-fix-workflow-contract-diagnostics.md`
- Type: `pre_fix_pr27_workflow_contract_diagnostics`
- SHA-256:
  `95237ba7fd80715e4fb9086298d4eb6e814d2cf575bc45ccfe4fd58489ab2c61`
- Working directory: `/var/tmp/codex/worktrees/framework-ci-security`
- Command:
  `rtk env PYTHONDONTWRITEBYTECODE=1 python3 ci/checks/security/check-github-actions-workflows.py --check all`
- Exit status: `1`; observed `2026-07-19T15:xxZ` (the supplied receipt did not
  retain the exact minute); retention: `retained_task_evidence`.

The canonical check reported flow-style YAML collections at CodeQL lines 5, 7,
and 30; dependency-review line 5; OSV line 5; quality line 5; Scorecard lines
5 and 7; secrets line 5; workflow-lint line 5; and cleanup-artifacts line 8.
It was captured after the ten textual merge conflicts were resolved in the
normal reconciliation with Framework `origin/master`
`7a12073c28e62a67492dd501b6513b9914fe5df8`, before the #27-owned compatibility
repair. No Parent or MRTS path changed.

## Root cause, impact, and remediation

PR #27's CI-security syntax predates or was not fully reconciled to the #29
canonical strict checker. Flow-style mappings survived the normal branch
reconciliation, creating a deterministic contract failure rather than a reason
to loosen the checker. Such syntax obscures permission and action-pin review
boundaries; permitting it would weaken a security control.

The #27-owned repair must convert every listed flow-style collection to the
canonical equivalent block mapping. It must preserve scanner coverage, pinned
action identities, the strict checker, and the separate
`FND-FRAMEWORK-0013` permission remediation. No exception or broadened accepted
syntax is permitted.

## Acceptance criteria and validation plan

- Every listed workflow has no flow-style YAML collection covered by the strict
  workflow-security contract.
- The canonical checker remains fail-closed and passes `--check all` on the
  final #27 exact head.
- Focused negative regressions continue to reject flow-style mappings.
- Legitimate canonical block-mapped permissions and SHA-pinned action
  definitions remain accepted.
- Applicable local workflow/lint checks, fresh exact-head PR checks/review,
  and the resulting-master original-reproduction and legitimate-control rerun
  verify the repaired workflow set.

## Dependencies, relationships, residual risk, and history

This work depends on the #27-owned YAML compatibility repair, the separate
`FND-FRAMEWORK-0013` permission remediation, fresh exact-head PR checks/review,
and resulting-master validation. It is related to `FND-FRAMEWORK-0013`,
`FND-FRAMEWORK-0016`, and `FND-SONAR-0005`.

The current reconciled #27 pre-fix workflow set fails the strict syntax
contract. There is no post-fix local, exact-head remote, or resulting-master
evidence yet. The strict checker is deliberately neither waived nor weakened.

`2026-07-19T15:35:21Z`: created as a validated, distinct pre-fix #27/#29
workflow-contract incompatibility record; no current remediation or remote
verification is claimed.
