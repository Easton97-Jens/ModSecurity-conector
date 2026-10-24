# Findings and Remediation Policy

Use the local finding system for significant defects, blockers, security observations, evidence gaps, runtime/CI/Sonar/governance/hardening limitations, and release-readiness issues when durable tracking is warranted.

## Principles

- one stable finding ID per independently remediable technical cause/boundary;
- concrete evidence, ownership, priority, confidence, status, acceptance criteria, validation plan, and residual risk;
- Parent/Framework/MRTS evidence and ownership remain separate;
- a code change, commit, PR, merge, or unrelated green check does not automatically close a finding;
- `accepted_risk` requires a current explicit user decision.

## Evidence

Retained finding evidence must be bounded, secret-safe, regular-file content with enough provenance to reproduce or explain the observation. Do not retain tokens, raw confidential payloads, full inherited environments, unsafe filesystem objects, or oversized/unreviewed artifacts.

## Lifecycle

A significant finding normally progresses through evidence-backed discovery/triage/validation/planning/fix/verification/closure. `fixed` means a change exists; `verified` means the original failure/strongest evidence no longer reproduces and legitimate control behavior passes.

For security findings also apply `security-policy.md`.
