---
name: dependency-security-update
description: "Safely plan and deliver a dependency update prompted by a validated security advisory or reachable vulnerability. Use for a focused dependency-security remediation; do not use for speculative upgrades, broad maintenance, or automatic package-manager fixes."
---

# Dependency security update

Treat advisory severity, reachability, compatibility, provenance, and license
changes as separate facts. An advisory alone does not prove that this repository
is affected.

## Required inputs

- Advisory identifier, affected dependency path, fixed-version range, and
  reachability evidence.
- Module or lockfile owner, current and minimum safe versions, compatibility
  constraints, and relevant license/provenance data.
- Scope-specific tests, security scanners, and required documentation.

## Repository boundary

Read the active `AGENTS.md`, source provenance, and security workflow first.
Keep repository dependency changes separate from unrelated changes. Do not
modify Framework dependencies from a Parent task or alter toolchain directives
without the required decision.

## Workflow

1. Validate the advisory against the current revision and dependency graph.
2. Establish reachability; use `govulncheck` for Go call-path evidence where
   applicable and keep OSV evidence complementary.
3. Select the smallest compatible secure version.
4. Review direct, indirect, license, provenance, and lockfile effects.
5. Make the isolated dependency change without an automatic fixer.
6. Run the affected module and security verification, then revalidate the
   original advisory path.
7. Record version delta, residual risk, and deferred major upgrades.

## Status model

Use `candidate`, `not_affected`, `affected_unreachable`,
`affected_reachable`, `update_pending`, `updated_verified`, or a
transparent block. Do not label an unreachable candidate as fixed.

## Expected result

Return the advisory, reachability and version evidence, selected minimum safe
version, dependency diff, actual tests, revalidation result, and any remaining
compatibility risk.

## Safety and stop conditions

Stop for an unclear module owner, a required major upgrade, an unexpected
dependency graph expansion, a new or changed toolchain/replace/exclude
directive, or missing compatibility evidence. Never run an automatic fix,
silently widen the dependency scope, or claim a scan alone closes the finding.

## Definition of done

The isolated update uses the smallest safe compatible version, actual affected
tests and scanners have run, the original path is revalidated, and the paired
record documents remaining risk.

## References

- [Operations and security](../../../docs/operations-and-security.md)
- [Change traceability](../../../docs/change-traceability.md)
- [Repository concept](../../../docs/repository-concept.md)
