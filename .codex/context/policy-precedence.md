# Policy Precedence and Canonical Owners

## Binding order

Apply applicable instructions in this order:

1. system/platform safety and permissions;
2. current explicit user request;
3. active repository `AGENTS.override.md` when present;
4. active repository `AGENTS.md`;
5. task-specific primary Context policy;
6. supporting Context policy;
7. current repository-native contracts/conventions;
8. Codex defaults.

A lower layer may add detail but cannot weaken a higher-layer safety, security, read-only, repository, or authorization boundary.

The current user request defines the requested outcome. Policies constrain how to execute it safely; they must not silently substitute a different goal.

## Canonical-owner rule

Each rule should have one primary owner. Supporting policies should reference that owner instead of copying its full rule text.

Use `index.md` as the owner map. When two local policies duplicate a baseline rule, prefer the primary owner and reduce the other to a scoped delta/reference.

## Current state versus target state

Current product facts come from the current checkout and versioned documentation/evidence. A policy that intentionally defines a future migration or target semantic must be explicitly marked as target-state and must not be cited as proof that current code already implements it.

## Technical status vocabulary

Use these task-level technical statuses when applicable:

- `passed`: the scoped check actually succeeded;
- `failed`: the scoped check executed and failed/disproved the claim;
- `blocked`: a prerequisite, permission, environment, or safe path prevents execution;
- `not_run`: applicable but intentionally not executed;
- `not_applicable`: outside the scoped contract;
- `not_verified`: a claim exists but adequate technical proof was not obtained.

Never translate `blocked`, `not_run`, `not_applicable`, or `not_verified` into `passed`.
