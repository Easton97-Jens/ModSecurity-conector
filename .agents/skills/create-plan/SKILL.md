---
name: create-plan
description: Create an evidence-based, repository-policy-compliant plan for a non-trivial ModSecurity-conector change.
---

# Create a repository plan

Use this repository-local adapter before a feature, bug fix, security remediation,
or infrastructure change whose scope is not already proven by local evidence.

## Trigger conditions

- The request needs a plan before implementation, especially when it affects a
  connector, lifecycle boundary, test evidence, documentation, or delivery.
- A non-trivial versioned implementation, multi-file change, security fix,
  dependency update, workflow change, architecture decision, large refactor,
  public API/compatibility change, release task, or Parent/Framework boundary
  is in scope.
- The task has multiple independent investigations or a material compatibility,
  security, or rollback decision.
- A reviewer asks for a concrete implementation and verification plan.

## Do not use when

- The request is a one-step factual answer that needs no repository change.
- A current, approved task plan already covers the requested work without a
  material scope change.
- The work is an already authorized one-line fix or an immediate task-owned CI
  lint correction with no material decision.
- The request is only to report the status of an active CI run.

## Local procedure

1. Read `AGENTS.md`, the applicable `.codex/context/` workflows, and the
   relevant product documentation before proposing changes.
2. Classify the task, record the baseline commit and worktree state, and state
   any assumption that could change compatibility, security, or architecture.
3. Split independent read-only investigation into bounded subagent work when
   that improves confidence. Keep all writes owned by the main agent.
4. Define explicit file scope, acceptance criteria, verification evidence,
   documentation language pairs, Change Record requirements, and delivery
   steps. Treat Parent and Framework work as separate scopes.
5. Use commands through `rtk`; keep temporary artifacts below `CODEX_TEMP_ROOT`.
6. Convert the plan into implementation only after material ambiguity is
   resolved from repository evidence or the user supplies the missing decision.

## Required plan format

Every required written plan must contain these fields:

- **Goal**
- **Scope**
- **Non-goals**
- **Acceptance criteria**
- **Files/components**
- **Security impact**
- **Test plan**
- **EN/DE impact**
- **Parent/Framework boundary**
- **Risks**
- **Open decisions**

When a material decision remains unresolved, record
`blocked_waiting_for_clarification`, explain the decision and trade-off, and
obtain the required direction before changing code. Planning itself must not
perform a code change.

## Safety boundary

Local system, user, repository, security, delivery, and storage policies take
priority over this adapter. Stage named task-owned paths only. Do not publish,
rewrite history, or automatically merge changes as part of planning.

## Provenance

This is an adapted, policy-constrained derivative of the historical
`create-plan` skill recorded in [UPSTREAM.md](UPSTREAM.md). No upstream scripts
or dependencies are included.
