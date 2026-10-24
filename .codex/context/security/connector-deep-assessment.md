# Generic Deep Connector Security Assessment

## Mode

`analysis_only`

This contract does not authorize product fixes, normal test changes, delivery, dependency changes, capability promotion, or Git writes.

## Scope discipline

The selected connector delta defines the direct product scope, logical profiles, host-specific boundaries, and required common check modules.

Parent, Framework, and MRTS remain separate ownership/Git boundaries. Supporting Framework/MRTS material is read-only unless a separate current user authorization selects that repository for writable work.

## Run storage

Use the configured external roots from `.codex/config.toml`.

Recommended run root:

`$CODEX_RUN_ROOT/security/<connector>/<RUN_ID>/`

Large builds, caches, runtime state, scanner work, logs, and temporary artifacts stay in `$BUILD_ROOT`, `$CACHE_ROOT`, `$TMP_ROOT`, `$ANALYSIS_ROOT`, `$LOG_ROOT`, and `$EVIDENCE_ROOT` or run-local descendants.

Do not create large runtime trees under the checkout.

## Required sequence

1. resolve active policies and connector delta;
2. inventory Parent/Framework/MRTS revisions and cleanliness;
3. inventory the selected host/toolchain and current repository-native targets;
4. build the execution contract and feasibility decision;
5. create repository and connector threat models;
6. inventory attack surfaces and trust boundaries;
7. perform current advisory seed research when permitted;
8. conduct multi-pass finding discovery;
9. deduplicate candidates by root cause while retaining independently reachable instances;
10. validate plausible candidates using source/control/sink analysis plus the strongest safe local execution available;
11. analyze attack paths and counterevidence;
12. calibrate severity/confidence/reportability;
13. produce hardening recommendations without implementing them;
14. reconcile coverage, evidence, cleanup, and repository integrity.

## Threat model minimum

Model relevant attacker classes such as:

- unauthenticated external client;
- authenticated low-privilege client;
- malicious or compromised upstream/downstream component;
- malicious reverse proxy or compatibility service;
- attacker controlling request target, headers, body, framing, timing, or connection lifecycle;
- attacker controlling allowed runtime/config/rule inputs;
- local attacker with another UID;
- local attacker with the same UID where IPC/filesystem boundaries rely on ownership;
- attacker seeking parser differential, request desynchronization, state confusion, resource exhaustion, logging disclosure, or supply-chain compromise.

Connector deltas may add host-specific attacker classes.

## Candidate contract

Every candidate records:

- stable candidate ID;
- connector and logical profile;
- affected path/file/function;
- attacker-controlled source/precondition;
- trust boundary and next intended control;
- sink or broken control;
- root cause;
- impact;
- legitimate control case;
- strongest counterevidence;
- validation method and evidence;
- confidence and finding status;
- cross-cutting affected repositories/connectors where applicable.

A common helper does not close independently reachable call sites, phases, routes, filters, companions, observers, or host actions.

## Validation

Prefer current repository-native builds/tests/harnesses. For plausible security candidates, use the relevant check modules and, when safe and permitted, focused negative tests, legitimate controls, alternate bypasses, sanitizers, race tools, fuzzing, fault injection, or non-interactive debugging.

Do not change product source or normal test suites to make validation possible during `analysis_only`.

A scanner or AI result is a candidate until validated against current source and evidence.

## Result truth

Individual existing checks use the repository status model from `testing-and-evidence.md`.

For assessment coverage, an applicable target that never reached execution remains an explicit coverage gap; do not invent a target-test result merely because a prerequisite failed.

Build success is not runtime evidence. Rule match is not host action. Requested intervention is not client-visible result. Service/self-test success is not host traffic evidence.

## Required retained artifacts

Create only artifacts with real content. Minimum durable set:

- `execution-contract.md`
- `policy-resolution.md`
- `repository-inventory.json`
- `tool-inventory.json`
- `threat-model.md`
- `attack-surface-ledger.jsonl`
- `coverage-ledger.jsonl`
- `candidates.jsonl`
- `findings.json`
- `validation-summary.md`
- `hardening-roadmap.md`
- `command-log.tsv`
- `cleanup-manifest.json`
- `final-report.md`

Finding-specific evidence may live under `findings/<finding-id>/`.

## Completion

A complete assessment requires policy resolution, inventory, threat model, attack-surface coverage, candidate disposition, required validation, truthful gaps, cleanup reconciliation, and final repository-integrity comparison.

A complete assessment may contain product failures and security findings. Completeness describes the assessment, not product approval.

Every final report states: **Diese Analyse ist keine Produktionsfreigabe.**
