# Parent Codex Working Agreement

<!-- codex-control-plane-routing:parent -->

## Scope

This file governs Codex work started from the Parent repository:

`/root/git/ModSecurity-conector`

Keep this file concise. Detailed operational rules live in `.codex/context/` and are loaded only when their domain applies.

## Product authority

For current product facts, route identity, commands, build/test behavior, configuration semantics, and runtime claims, prefer the current checkout in this order:

1. product source and checked-in contracts;
2. root `Makefile` and component-native build files;
3. current versioned architecture/connector/testing documentation;
4. current tests, CI workflows, and run-scoped evidence;
5. local Codex policies.

A local policy may define a future target contract, but it must say so explicitly. Never turn target-state policy into a claim about current implementation.

## Mandatory task start

Before task-changing work:

1. read active instructions and then read completely `/root/.agents/skills/goal-driven-execution/SKILL.md`;
2. parse the current user request exactly;
3. read `.codex/context/index.md` and only the routed policies/profiles;
4. establish repository ownership, feasibility, security relevance, and resource needs;
5. create the execution contract and plan under `task-workflow.md`;
6. identify validation before implementation.

A bounded read-only inspection may precede the full plan only to locate instructions, repository boundaries, and relevant evidence.

## Repository boundaries

Parent, Framework, and MRTS are separate Git, ownership, test, evidence, and delivery boundaries.

- Parent: `/root/git/ModSecurity-conector`
- Framework: `modules/ModSecurity-test-Framework`
- MRTS: `modules/ModSecurity-test-Framework/tools/MRTS`

The Parent owns connector product source, `common/`, connector integration, Parent build/runtime orchestration, Parent tests, and Parent evidence producers/consumers.

The Framework owns reusable test cases, schemas, runners, normalizers, reusable matrix/report logic, and Framework documentation.

MRTS is read-only by default during Parent or Framework tasks. MRTS write/Git/delivery work requires a current explicit user selection of MRTS and permitted action classes.

Before Framework work, load `framework-orchestration.md`, then the active Framework instructions and applicable Framework-local policies.

## Resources

Heavy task data belongs under the external roots exported by the active project `.codex/config.toml`, especially `/var/tmp/codex/ModSecurity-conector`.

Do not use the source checkout, `/tmp`, `$HOME`, or the smaller source filesystem as overflow storage for builds, caches, runtime data, logs, downloads, matrices, analysis, or evidence.

Numeric storage limits come only from `.codex/config.toml`. Use all available logical CPUs for parallel-safe CPU-bound work when memory and target semantics permit. Agent concurrency and build concurrency are separate controls.

## Commands and tools

Prefer current repository-native `make` targets and checked-in scripts. Discover target names from the current checkout; never invent a target because an old report or policy mentions it.

Before issuing local project commands, read `command-execution-policy.md`. RTK is the mandatory shell-command execution proxy; repository-native execution remains RTK-wrapped. Tool-specific authentication wrappers remain separate mandatory controls and no wrapper may bypass another policy boundary.

Do not install packages, change system services, introduce toolchains, or mutate dependency files unless the current task and applicable policy authorize it.

## Security

Assess security relevance for every non-trivial task. For a deep connector scan, load `profiles/connector-security-assessment.md` plus the selected connector delta under `security/connectors/`. For all-connector or repository-wide assessment, load the corresponding profile under `.codex/context/profiles/`.

Never weaken validation, authentication, authorization, isolation, redaction, compiler warnings, tests, CI requirements, branch protection, or Quality Gates to obtain a pass.

## Git and delivery

Preserve unrelated user changes. No destructive cleanup, broad staging, force-push, history rewriting, direct `master` push, or merge without the routed authority.

Commit/push/PR authority never implies merge authority. Parent `master` integration requires current explicit authorization under `master-integration.md`.

## Documentation and evidence

Versioned reader-facing technical documentation follows the repository EN/DE companion convention. Generated documentation/reports must be changed through their generator/source contract.

A build, config load, source wiring, capability declaration, generated report, scanner result, or client-only probe proves only its own layer. Runtime claims require the applicable host/profile/run evidence.

## Completion

Before reporting completion, apply `definition-of-done.md`, reconcile every current-prompt requirement, report all relevant checks truthfully, stop task-owned processes/agents, and retain or clean task-owned artifacts safely.

## Routing

`.codex/context/index.md` is the routing table. Load only the primary owner(s), selected assessment profile, selected connector delta, and explicitly referenced check modules needed for the task.
