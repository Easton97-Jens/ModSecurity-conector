---
name: connector-test-matrix
description: "Plan, run, or report the repository's connector test matrix while keeping H1/H2/H3 transport evidence separate from CRS/MRTS evidence. Use for connector, lifecycle, common-runtime, security, or test-matrix work; do not use to promote a source, build, or single-protocol result into runtime coverage."
---

# Connector test matrix

Treat connector, CRS/MRTS, test level, and transport protocol as independent
evidence dimensions.

## Required inputs

- Changed component, affected connector(s), selected host profile, and test
  level.
- Available documented targets, CRS/MRTS prerequisites, and H1/H2/H3
  environment.
- Commit, Framework revision, run ID, evidence root, and resource constraints.

## Repository boundary

Read the active `AGENTS.md`, the current command inventory, connector guide,
and test/evidence documentation. Keep reusable Framework cases and runners in
the Framework. Use only documented targets and isolated paths under
`CODEX_TEMP_ROOT`.

## Workflow

1. Determine whether the scope affects one connector, all six connectors, or
   no connector behavior.
2. Disposition each independent CRS/MRTS row:
   `no_crs_no_mrts`, `with_crs_no_mrts`, `no_crs_with_mrts`, and
   `with_crs_with_mrts`.
3. Record H1, H2, and H3 separately from every matrix disposition.
4. Use only the actually reached `contract`, `build`, `configuration`,
   `smoke`, `runtime`, or `full_lifecycle` level.
5. Preserve connector/profile-specific evidence and report missing prerequisites
   without inferring unsupported behavior.

## Status model

Each matrix and protocol row is exactly one of `passed`, `failed`,
`blocked`, `not_executed`, `not_applicable`, `unsupported`, or
`unknown`. Do not treat `unknown` as success.

## Expected result

Provide one table per affected connector with matrix ID, profile, CRS/MRTS,
test level, command, protocol, status, and evidence or reason. Include a
separate H1/H2/H3 disposition and a scoped non-applicability statement for
documentation-only work.

## Safety and stop conditions

Stop before an undocumented target, an unapproved large download, unclear
Framework ownership, or a missing security-critical prerequisite. Never use a
No-CRS result as a CRS result, an H1 result as H2/H3 evidence, or a build as
runtime proof.

## Definition of done

Every in-scope combination and transport dimension has a concrete status,
evidence is isolated and non-secret, and any unrun or blocked path states its
reason and remaining unknown.

## References

- [Testing and evidence](../../../docs/testing-and-evidence.md)
- [Repository concept](../../../docs/repository-concept.md)
- [Operations and security](../../../docs/operations-and-security.md)
