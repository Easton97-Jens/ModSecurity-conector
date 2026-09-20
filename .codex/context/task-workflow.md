# Task Workflow

## Mandatory sequence

For every task:

1. read active instructions;
2. read completely `/root/.agents/skills/goal-driven-execution/SKILL.md`;
3. parse the exact current prompt;
4. create a requirement inventory;
5. determine repository/ownership scope;
6. load only applicable primary policies from `index.md`;
7. perform feasibility assessment;
8. create the execution contract and validation plan;
9. ask only material questions that evidence cannot safely resolve;
10. perform the work within scope;
11. validate changed behavior and requested deliverables;
12. reconcile every prompt requirement before reporting completion.

## Compact execution contract

Record, in the task conversation or task-owned plan:

- Goal
- Exact user request
- Deliverables
- Non-goals
- Repository/ownership scope
- Constraints/prohibited actions
- Assumptions
- Open material decisions
- Acceptance criteria
- Plan
- Validation plan
- Delivery authorization

Trivial work may use a short contract, but it still needs a goal, acceptance criteria, and a plan.

## Requirement inventory

For each concrete prompt requirement track:

- exact requirement;
- scope;
- required output;
- prohibited action if any;
- acceptance evidence;
- status: `pending`, `in_progress`, `satisfied`, `blocked`, `not_applicable`, or `superseded_by_user`.

Do not silently add, remove, or reinterpret a material user requirement.

## Questions and assumptions

Investigate repository evidence before asking. Ask only when the missing decision materially changes product behavior, compatibility, security posture, repository ownership, destructive actions, delivery/merge authority, dependencies/toolchains, external cost/service use, or evidence validity.

Do not ask for information the user already provided.

A low-risk assumption is allowed only when it is reversible, repository-native, outside security/data-loss/delivery boundaries, and has no public semantic effect. Record the assumption and how to reverse it.

## Final reconciliation

Before reporting completion, map every current prompt requirement to its disposition and evidence. A mandatory `pending`, `in_progress`, or `blocked` item prevents `complete`.
