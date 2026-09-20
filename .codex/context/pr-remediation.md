# PR Feedback and CI Remediation

After first push, keep a task-owned PR in the remediation cycle until `verified_pr`, `blocked`, or `failed`.

## Failed checks

For each current-head failure, identify the exact run/job/SHA and classify the cause as task-owned, pre-existing baseline, infrastructure/flaky, or external/unrelated.

Fix clear task-owned failures with the smallest scoped correction, run focused local validation, commit/push normally, then restart the current-SHA verification cycle.

Do not rerun failures repeatedly to erase evidence. An evidenced flaky/infrastructure failure may be rerun when justified; recurrence needs root-cause evidence or a truthful blocker.

## Review threads

Classify visible feedback as actionable, informational, already resolved, outdated, duplicate, conflicting, ambiguous, or unrelated. Fix clear task-owned actionable feedback. Resolve a thread only after the correction is verified.

Do not auto-resolve product-decision, security-risk-acceptance, ambiguous, or unverified feedback.

## Fresh final round

Immediately before any separately authorized merge, re-read the complete final diff and current PR state; verify exact current head SHA, checks, reviews, conversations, SonarQube, base freshness/mergeability, repository protections, and absence of active task processes/agents.

Any new push/base update/conflict resolution invalidates stale head-bound evidence and restarts the round.
