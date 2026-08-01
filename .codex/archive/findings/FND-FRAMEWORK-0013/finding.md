# FND-FRAMEWORK-0013 — Framework workflows do not consistently enforce least-privilege tokens, canonical permissions, and safe PR checkout

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0013` |
| Category | `security_hardening` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P2` / `medium` |
| Confidence / status | `validated` / `verified` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Current scope and observation

## 2026-07-26 current-master verification

The pre-fix statements below are retained as historical reproduction evidence.
They are superseded by the current disposition: Framework master
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0` passes the strict workflow
checker, focused CI-security/permission/action-pin controls, and current
master checks. PR #27 exact-head and resulting-master hosted checks were also
observed successful. No permission invariant or strict checker was weakened.

This finding is reopened. The reconciled Framework PR #27 workflow set again
violates the least-privilege permission invariant: the untrusted
`pull_request` CodeQL `analyze` job grants `security-events: write`, and
`cleanup-artifacts` does not express the required top-level permissions as the
canonical `contents: read` mapping. The historical exact-checkout remediation
remains retained evidence, but does not establish that the current reconciled
workflow composition is safe.

The retained pre-fix checker exited `1` and reported both diagnostics:

```text
.github/workflows/ci-security-codeql.yml: job 'analyze' grants a write permission in a pull_request workflow
.github/workflows/cleanup-artifacts.yml: top-level permissions must be exactly '{contents: read}'
```

Affected paths are `.github/workflows/ci-security-codeql.yml`,
`.github/workflows/cleanup-artifacts.yml`,
`ci/checks/security/check-github-actions-workflows.py`, and
`tests/ci_security/test_framework_ci_security_contract.py`. The relevant
symbols and invariants are `pull_request`, `analyze`, `security-events: write`,
top-level `permissions`, `cleanup-artifacts`, and
`check-github-actions-workflows.py --check all`.

## Evidence and reproduction

The current retained pre-fix evidence is:

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

The condition was captured after normal reconciliation of Framework
`origin/master` `7a12073c28e62a67492dd501b6513b9914fe5df8` into
`agent/expand-framework-ci-security`, after merge-conflict resolution and
before the #27-owned compatibility repair. No Parent or MRTS path changed.

Historical evidence remains intact rather than being relabeled as current:
`20260718T084030Z-expand-framework-ci-security-be8fb24d`, artifact
`final-framework-ci-security-local-validation.md`, SHA-256
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`,
recorded a local exit `0` at source commit
`768a06b5b734547f8213cc6918c26ef4a8ef9f67`. It proves only the earlier
exact-checkout and scan-range remediation, not the later reconciled workflow
composition.

## Root cause, impact, and remediation

The prior remediation established exact checkout and scan-range controls, but
the reconciled workflow set still combined an untrusted `pull_request` CodeQL
analysis path with `security-events: write` and retained a cleanup permission
expression that violates the later canonical strict checker. An attacker-
controlled pull request could therefore execute CodeQL with a write-capable
token. The noncanonical cleanup model also defeats the reviewable permission
contract and risks future permissive drift.

The #27-owned repair must leave the strict checker unchanged. It must split
CodeQL into a read-only, no-upload untrusted `pull_request` path and a trusted
non-`pull_request` upload path, convert `cleanup-artifacts` to the canonical
block mapping with top-level `contents: read`, and preserve the existing exact
PR-head checkout and scan-range controls.

## Acceptance criteria and validation plan

- No `pull_request`-triggered job grants any write permission.
- The CodeQL `pull_request` path is read-only and does not upload security
  events; any `security-events: write` upload is confined to a trusted
  non-`pull_request` path.
- `cleanup-artifacts` declares exactly the canonical top-level `contents: read`
  permission mapping in block syntax.
- The strict workflow checker and focused regression tests pass on the final
  #27 exact head without weakening `ci/checks/security/check-github-actions-workflows.py`.
- The negative controls reject a PR write permission and a noncanonical cleanup
  model; the legitimate controls accept the trusted upload path, intended
  cleanup mapping, and default-branch `github.sha` behavior.
- Fresh exact-head PR checks and review state are observed, then the original
  reproduction and legitimate controls are rerun on the resulting Framework
  master before lifecycle advancement.

## Dependencies, relationships, residual risk, and history

Dependencies are the #27-owned workflow compatibility repair, fresh exact-head
PR checks/reviews, and the resulting-master rerun. This record is related to
`FND-FRAMEWORK-0012`, the distinct YAML-contract compatibility finding
`FND-FRAMEWORK-0019`, and `FND-SONAR-0005`.

The current reconciled #27 pre-fix tree demonstrably fails the strict checker.
There is no post-fix local result, exact-head remote result, or
resulting-master verification yet. No permission invariant, strict YAML rule,
or security control is waived.

`2026-07-18T15:18:00Z`: earlier local exact-PR-head remediation was recorded
as fixed at `768a06b`; that evidence remains historical. `2026-07-19T15:35:21Z`:
the current condition was reproduced and the finding was reopened from `fixed`
to `in_progress`; no current implementation is claimed fixed.
