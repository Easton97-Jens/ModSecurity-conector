# Parent Master Integration Authorization

## Authorization

Integration into Parent `master` is allowed only when the current user prompt unambiguously requests merge/integration of the current task-owned PR scope or explicitly named PR(s) into Parent `master`.

Commit/push/PR creation, “make it green”, “prepare merge”, or general delivery wording is not merge authorization.

Authorization is task-scoped, revocable by a newer user instruction, repository-scoped, and limited to the selected PR inventory.

## Preconditions

Before merge, establish for the current head SHA:

- PR is open, non-draft, and targets `master`;
- ownership/selection is clear;
- final diff and PR description are current;
- required local checks and current-SHA GitHub checks pass;
- required reviews/conversations are satisfied;
- applicable SonarQube Cloud Quality Gate passes;
- no actionable task-owned feedback remains;
- repository protections/rulesets/deployment requirements are satisfied;
- no task-owned process/subagent remains active;
- allowed merge method is determined from current repository settings/convention and current user instruction.

Do not hard-code a merge method in local policy when GitHub can be queried. Never use admin bypass, direct `master` push, force-push, or optional auto-merge as a shortcut.

## Exact-head merge

Immediately before merge, resolve the PR head again and bind the operation to that exact head (`--match-head-commit` or equivalent). If the head changes, stop and repeat the final verification round.

## Cross-repository order

When Parent integration depends on a separately authorized Framework PR, verify/merge Framework first, resolve the exact Framework `master` SHA, then update the Parent gitlink through a separate authorized Parent change and PR.

A Framework merge never authorizes the Parent gitlink. MRTS is never implicitly included.

## Post-merge

Confirm authoritative PR `MERGED` state and resulting Parent `master` SHA, verify applicable master workflows for that SHA, then apply `cleanup-and-restoration.md`.

`master_integration_complete` requires verified merge result, current master evidence, required master checks, safe Parent restoration, and no active task-owned process.
