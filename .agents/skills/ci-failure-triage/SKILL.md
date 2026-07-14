---
name: ci-failure-triage
description: "Classify and investigate a failed GitHub Actions run for this repository using the final commit SHA and a master comparison. Use for a concrete failed, pending, skipped, or permission-limited CI result; do not use to change workflow behavior preemptively or to treat an older run as evidence."
---

# CI failure triage

Start from one named workflow run and its exact head SHA. Inspect logs without
copying secrets, raw request data, or hidden environment values into artifacts.

## Required inputs

- Final local and remote commit SHA, branch, workflow URL or run ID, and event.
- The failed job, sanitized error excerpt, and the comparable `master` run.
- Whether the run is required, optional, scheduled, PR-only, or push-only.

## Repository boundary

Read the active `AGENTS.md` and relevant CI/delivery policies first. Keep the
Parent and Framework run histories separate. Do not retry, alter protection, or
change a workflow unless the task authorizes a scoped remediation.

## Workflow

1. Confirm that `headSha` equals the final pushed SHA.
2. Identify the workflow trigger and whether a run should exist for that SHA.
3. Inspect the exact failed job and classify the evidence.
4. Compare the same target on `master` or another unaffected final SHA.
5. Reproduce only a suspected `own_change_failure` locally when safe.
6. Make the smallest complete follow-up only for an owned failure, then restart
   exact-SHA verification.

## Status model

Classify each failure as exactly one of:

- `own_change_failure`
- `unrelated_repository_failure`
- `infrastructure_failure`
- `flaky_or_transient_failure`
- `permissions_or_secrets_failure`
- `workflow_configuration_failure`
- `unknown_failure`

When an owned workflow has a syntax, schema, expression, permission, action
reference, or configuration defect, classify it as
`workflow_configuration_failure`; record ownership separately rather than
also using `own_change_failure`. Reserve `own_change_failure` for an owned
product, test, or integration failure that is not itself workflow
configuration.

Keep `ci_pending`, `blocked_github_permissions`, and
`blocked_feature_unavailable` distinct from passed evidence. A missing
optional run is not a passed check.

## Expected result

Return the exact SHA, run and job identifiers, trigger, classification,
comparison evidence, remediation scope, retry decision, and the delivery
status supported by those facts.

## Safety and stop conditions

Stop when the compared run is not equivalent, a secret could be exposed, a
branch-protection change is proposed, or the failure cannot be separated from
another task. Never weaken a test, add a blanket success path, or classify an
unknown result as unrelated.

## Definition of done

The result is tied to the final SHA, has one evidence-backed classification,
compares the relevant `master` state, preserves independent failures, and
records any retry or owned fix accurately.

## References

- [Change traceability](../../../docs/change-traceability.md)
- [Repository concept](../../../docs/repository-concept.md)
- [Change Record index](../../../reports/audits/change-records/README.md)
