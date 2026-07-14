---
name: optional-prerequisite-ci
description: "Design or triage CI checks with optional prerequisites without hiding real failures. Use when a documented tool, host, feature, or environment may be absent; do not use to downgrade a genuine test failure, skip an in-scope check, or weaken a workflow."
---

# Optional prerequisite CI

Make a missing environment condition visible without turning it into either a
false pass or an unbounded failure.

## Required inputs

- The check's contract, owning path, required versus optional prerequisites,
  trigger, and expected evidence.
- The observed exit code or result and any relevant environment capability
  probe.
- The final SHA and whether the check applies to the changed scope.

## Repository boundary

Read the active `AGENTS.md`, command inventory, and CI/delivery policies.
Use only documented targets. Keep optional host, protocol, CRS/MRTS, and GitHub
feature conditions distinct from source or workflow errors.

## Workflow

1. Identify whether the missing prerequisite is mandatory for the in-scope
   contract.
2. Probe the condition deterministically before starting dependent work.
3. Preserve genuine command failures and their diagnostics.
4. Emit one explicit status with a concise non-secret reason.
5. Compare final-SHA CI behavior with `master` when triaging a remote run.

## Status model

Use exactly these outcomes for the decision:

- Missing mandatory prerequisite: `failed`.
- Missing optional relevant environment: `blocked`.
- Path outside the requested scope: `not_applicable`.
- Check never started: `not_executed`.
- Unavailable GitHub product capability: `blocked_feature_unavailable`.

Use `passed` only for an executed, successful check. Keep `unknown` visible
when neither applicability nor the cause is established.

## Expected result

Return the contract, prerequisite classification, probe, command and exit
status, exact SHA if remote, evidence location, and remaining uncertainty.

## Safety and stop conditions

Stop if the contract or optionality is undocumented. Do not use blanket
success paths, `continue-on-error`, or error-suppressing shell shortcuts to
hide a real failure. Do not fetch a large prerequisite merely to change a
status without authorization.

## Definition of done

Every missing condition is classified explicitly, genuine failures remain
failed, a non-applicable path has a scope reason, and the result does not
overstate execution or runtime evidence.

## References

- [Testing and evidence](../../../docs/testing-and-evidence.md)
- [Change traceability](../../../docs/change-traceability.md)
- [Repository concept](../../../docs/repository-concept.md)
