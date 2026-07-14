---
name: security-finding-lifecycle
description: "Validate, reproduce, remediate, and revalidate a reported security finding in this Parent repository. Use for a concrete vulnerability report, scanner candidate, or reachability question that may require a fix; do not use for a generic repository scan, an unvalidated theory, or routine CI triage."
---

# Security finding lifecycle

Use this skill only after identifying a concrete candidate, report, or alert.
Treat a scanner alert as a candidate until reachability and impact are proven.

## Required inputs

- The candidate's source, affected revision, component, and stated impact.
- The relevant trust boundary, deployment assumptions, and available reproducer.
- The intended Parent or Framework scope, plus the acceptable verification level.

## Repository boundary

Read the active `AGENTS.md` and its applicable local policies before acting.
Keep reusable runner, case, and normalizer changes in the Framework; do not
change its Gitlink until that repository has completed its own delivery.
Keep payloads, credentials, cookies, bodies, and private paths out of findings,
tests, logs, and records.

## Workflow

1. Capture the candidate without promoting it to a confirmed finding.
2. Validate the current revision and ownership boundary.
3. Trace reachability and the source-to-sink attack path.
4. Build a minimal, non-secret reproducer or record why one is unavailable.
5. Establish the smallest complete remediation that preserves legitimate
   behavior.
6. Add a regression test or another reproducible proof of the original cause.
7. Re-run the reproducer, the regression test, and the relevant legitimate
   behavior checks.
8. Revalidate the finding on the final revision and record residual risk.

Use a verified, currently available Codex Security skill only by its surfaced
name and documented workflow. Do not invent plugin commands or use a scanner
result as a replacement for validation.

## Status model

Use `candidate`, `validated`, `not_reproducible`, `fix_in_progress`,
`regression_verified`, `closed`, or a transparent blocking status. A
`closed` finding includes final-revision revalidation; a `not_reproducible`
candidate is not silently treated as safe.

## Expected result

Produce a concise finding record containing the affected boundary, attack
preconditions, reachability evidence, reproducer status, smallest fix,
regression and legitimate-behavior results, final revision, and residual risk.

## Safety and stop conditions

Stop and request a decision when the security boundary, fail-open/fail-closed
contract, deployment assumption, or compatibility impact is unknown. Do not
rotate, delete, disclose, or paste a suspected secret. Do not change
dependencies, Framework code, public contracts, or workflow permissions merely
to make a scanner green.

## Definition of done

The final revision has a validated attack-path disposition, a bounded fix when
needed, regression and legitimate-behavior evidence, paired documentation and
Change Record updates when versioned work occurred, and an explicit residual
risk.

## References

- [Change traceability](../../../docs/change-traceability.md)
- [Repository concept](../../../docs/repository-concept.md)
- [Operations and security](../../../docs/operations-and-security.md)
- [Change Record index](../../../reports/audits/change-records/README.md)
