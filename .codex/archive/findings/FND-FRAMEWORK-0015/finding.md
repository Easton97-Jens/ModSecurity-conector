# FND-FRAMEWORK-0015 — OSV evidence validation did not require complete vulnerability-group coverage

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0015` |
| Category | `evidence_gap` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P2` / `not_applicable` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `blocked_external_dependency` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary

OSV comparison evidence could be structurally valid JSON while omitting,
duplicating, or inconsistently grouping vulnerability identifiers.

## Evidence and remediation

The OSV report schema and comparator now fail closed for malformed reports,
incomplete or overlapping groups, duplicate IDs, and untrusted or symlinked
evidence paths. Alias enrichment remains a legitimate non-new group. The
remediation is in `768a06b5b734547f8213cc6918c26ef4a8ef9f67`; exact local HEAD
passed 64 CI-security tests and `make lint`. Retained artifact SHA-256:
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`.

On exact Framework PR #50 head
`b0f3e745075d57ee727bdfcd61f6258d488d4dc1`, the hosted OSV
`pull-request-head` job reached its bounded base/head comparison but the OSV
Scanner returned `service unavailable` while resolving the unchanged trusted
base manifest. The job exited `127` before producing trustworthy comparison
evidence. This is an external verification blocker, not evidence that the
fixed schema/comparator control regressed; the fail-closed workflow was not
weakened. Receipt: [run 30204914941, job 89801198064](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/30204914941/job/89801198064).

## Acceptance criteria

- Every reported vulnerability ID belongs to exactly one validated group.
- Alias-only enrichment does not create a false new group.
- Malformed, incomplete, overlapping, oversized, or untrusted evidence fails.
- Exact final PR-head OSV CI confirms the committed control.

## Residual risk and history

Local remediation remains fixed, but remote exact-head OSV verification is
`blocked_external_dependency` until the scanner service recovers and a fresh
PR #50 run succeeds. `2026-07-18T15:18:00Z`: created and locally fixed.
`2026-07-26T13:52:18Z`: exact PR #50 OSV run blocked by external service.
