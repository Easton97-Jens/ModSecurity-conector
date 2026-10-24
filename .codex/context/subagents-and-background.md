# Subagents and Background Work

## Main-agent responsibility

Subagents/background commands are bounded helpers for the active task. The main agent remains responsible for scope, evidence, integration, validation, Git/delivery decisions, and final completion.

No helper/process may continue after the task is reported complete.

## Delegation

Use subagents only when independent bounded work improves coverage/speed enough to justify coordination. Prefer read-only investigation. Do not delegate a material user decision or use agents to evade repository/security/authorization boundaries.

Every assignment records role, repository root, mode (`read_only` or tightly bounded write), goal, read/write scope, temporary root, prohibited actions, required evidence, and completion criteria.

Parallel writes require disjoint file ownership; shared files are integrated by the main agent.

## Background commands

Before launch record owner, purpose, working directory, process reference, log/output path, timeout, resource estimate, cancellation condition, and completion condition.

Run concurrently only when ports, mutable state, build/cache/output/evidence paths, logs, and resource budgets are disjoint.

Monitor progress, CPU/memory/disk/log growth, scope violations, and exit status. Stop work that crosses resource limits, writes outside scope, conflicts with another process, or loses observable progress.

Before completion, wait for/terminate all mandatory processes/agents, collect terminal statuses, finalize evidence, and clean only eligible task-owned temporary data.
