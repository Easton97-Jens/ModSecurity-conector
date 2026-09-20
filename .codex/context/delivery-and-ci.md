# Parent Delivery and CI Policy

## Scope

This policy governs eligible non-trivial versioned Parent product work through `verified_pr`. It does not authorize merge to `master`.

A current user instruction such as `do not commit`, `do not push`, `local only`, or `do not create a PR` disables that action.

## Delivery states

Use as applicable:

`delivery_not_applicable`, `local_complete`, `committed`, `pushed`, `pr_open`, `checks_pending`, `remediation_required`, `verified_pr`, `blocked`, `failed`.

`verified_pr` is the highest standing-delivery state without explicit master integration authorization.

## Preconditions

Before commit/push/PR:

- local applicable Definition of Done is satisfied;
- final scoped diff is reviewed;
- `git diff --check` is clean;
- required EN/DE docs and Change Record are current;
- no secrets/local artifacts are staged;
- repository boundaries are respected;
- required local checks have truthful terminal statuses;
- resource/process cleanup requirements are satisfied;
- Parent remote preflight passes.

## Commit and push

Create an atomic task-owned commit. After first push, do not amend/rebase/force-push; remediation uses focused follow-up commits.

Push only the task branch and verify local/remote SHA equality.

## PR

Create/update the task-owned Draft PR. Its description must reflect final behavior, actual tests/results, security/compatibility effects, limitations, and Change Record.

After every push verify:

`local HEAD = remote task branch = PR head SHA`

Only current-head checks/reviews/Quality Gates are evidence.

## verified_pr

Enter `verified_pr` only when required current-SHA GitHub checks passed, applicable SonarQube Cloud Quality Gate passed, no required task-owned check is pending/cancelled/unknown, actionable task-owned review feedback is resolved, PR/Change Record match the final diff, and no task-owned monitor/process remains active.

Do not merge automatically. Read `master-integration.md` only when the current prompt explicitly requests Parent master integration.
