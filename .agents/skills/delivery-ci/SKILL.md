---
name: delivery-ci
description: "Deliver a completed versioned Parent-repository change through scoped staging, an atomic commit, push, draft pull request, and exact-SHA CI verification. Use after local verification is complete; do not use for read-only analysis, local-only Codex files, incomplete work, or Framework changes awaiting their own delivery."
---

# Delivery CI

Deliver only a finished, scoped Parent change. Preserve unrelated work and
ensure local Codex configuration remains outside the commit.

## Required inputs

- Final intended diff, Change Record, local checks, branch, base branch, and
  unambiguous `origin`.
- A list of task-owned files and deliberately excluded local or unrelated files.
- The final local SHA, pushed SHA, draft PR, and required workflow results.

## Repository boundary

Read the active `AGENTS.md` and delivery policy before staging. Framework
work is delivered in its own repository first; never use this skill to update a
Framework Gitlink implicitly. Exclude `AGENTS.md`, `RTK.md`, `.codex/`,
`.rtk/`, secrets, caches, build trees, and raw evidence.

## Workflow

1. Reconcile the final diff, Change Record, source boundary, and actual local
   verification.
2. Stage only named task-owned files and inspect the complete cached diff.
3. Create an atomic, imperative commit.
4. Push the task branch without rewriting published history.
5. Compare the local and remote final SHA.
6. Open or update one draft PR against `master`; do not merge or enable
   auto-merge.
7. Observe only workflow runs whose `headSha` equals the final SHA.
8. Close an owned CI failure with a new follow-up commit, then repeat SHA
   verification.

## Status model

Use the repository delivery status supported by the evidence:
`delivery_complete`, `committed_not_pushed`, `blocked_git_remote`,
`blocked_github_auth`, `blocked_branch_policy`,
`blocked_pull_request_required`, `blocked_possible_secret`, `push_failed`,
`ci_pending`, `ci_failed_own_change`, `ci_blocked_unrelated_failure`,
`ci_blocked_infrastructure`, `blocked_github_permissions`, or
`delivery_not_applicable`.

## Expected result

Report the branch, base and final SHA, task-owned and excluded files, commits,
push comparison, draft PR, each exact-SHA run, actual outcomes, and final
delivery status.

## Safety and stop conditions

Stop for an unclear remote or target branch, a possible secret, a non-separable
unrelated change, a direct default-branch push, or any history rewrite. Never
stage a broad path, overwrite another task, or claim delivery from a
branch-level or earlier-commit run.

## Definition of done

The final diff and Change Record agree, only task-owned files are committed,
the remote SHA equals the local SHA, the draft PR is unmerged, and required
checks for that SHA are green or an evidence-backed blocking status is present.

## References

- [Change traceability](../../../docs/change-traceability.md)
- [Repository concept](../../../docs/repository-concept.md)
- [Change Record index](../../../reports/audits/change-records/README.md)
