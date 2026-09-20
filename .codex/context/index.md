# Parent Context Index

Load only the policies needed for the current task. `AGENTS.md` is the concise entry point. This index routes each decision domain to one primary owner.

## Core policies

| Task or decision | Primary owner |
| --- | --- |
| Instruction conflicts / canonical ownership | `policy-precedence.md` |
| Task contract, prompt requirements, questions, assumptions, planning | `task-workflow.md` |
| Feasibility / prerequisites / execution go-no-go | `feasibility-policy.md` |
| Parent/Common/connector/Framework ownership | `architecture-and-boundaries.md` |
| Feature, bugfix, refactor, behavior change | `change-workflow.md` |
| Tests, command selection, evidence meaning | `testing-and-evidence.md` |
| Shell/project command execution and RTK | `command-execution-policy.md` |
| Storage, CPU, memory, worktrees, caches | `resources-and-storage.md` |
| Security-sensitive work | `security-policy.md` |
| Native NGINX/Envoy security runtime preflight | `security-runtime-preflight.md` |
| Git state, branches, staging, remotes | `git-policy.md` |
| Commit/push/PR/CI to `verified_pr` | `delivery-and-ci.md` |
| PR feedback / CI remediation | `pr-remediation.md` |
| Explicit Parent `master` integration | `master-integration.md` |
| Worktree/branch cleanup and Parent restoration | `cleanup-and-restoration.md` |
| Parent/Framework/MRTS orchestration | `framework-orchestration.md` |
| EN/DE docs, Change Records, lifecycle evidence | `documentation-and-traceability.md` |
| C/C++/Go/Shell/CLI/tool selection | `tooling-and-language.md` |
| Python environments, dependencies, external Python CLIs | `python-policy.md` |
| Subagents and background commands | `subagents-and-background.md` |
| Findings, evidence retention, remediation | `findings-policy.md` |
| CRS/MRTS connector matrix | `connector-matrix.md` |
| H1/H2/H3, hardening, sanitizers, static analysis | `protocol-and-hardening.md` |
| SonarQube local access and Cloud Quality Gate | `sonarqube-policy.md` |
| Phase-4 migration target semantics | `phase4-target-semantics.md` |
| Final completion decision | `definition-of-done.md` |

## Assessment profiles

| Request | Load |
| --- | --- |
| Deep security assessment of one connector | `profiles/connector-security-assessment.md` + `security/connectors/<connector>.md` |
| Deep security assessment of all six host families | `profiles/all-connectors-security-assessment.md` + all six connector deltas |
| Runtime readiness of one connector/profile | `profiles/connector-runtime-assessment.md` + selected connector delta |
| Runtime readiness across all connectors | `profiles/all-connectors-runtime-assessment.md` |
| CI / dependency / supply-chain assessment | `profiles/ci-supply-chain-assessment.md` |
| Strict all-applicable-target completeness overlay | `profiles/strict-completeness-assessment.md` + owning assessment profile |
| Full repository security/quality/readiness assessment | `profiles/full-repository-assessment.md` |
| Phase-4 target migration assessment | `profiles/phase4-migration-assessment.md` |
| Evidence/claim integrity audit | `profiles/evidence-integrity-assessment.md` |

## Security module routing

Connector deltas list the common security checks they require. Do not load every check module automatically.

Common modules live under `security/checks/`. Connector-specific deltas live under `security/connectors/`.

The six host families are Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd. Their ten logical profiles are listed in `security/connectors/README.md` and remain separate evidence claims.

## Repository-native authority

Do not maintain a second static Parent command catalog here. Current root `Makefile`, component build files, current versioned connector/testing docs, `ci/README.md`, and `tests/README.md` are the command/test sources of truth.

Old MRTS-specific `commands.md`, `testing.md`, and `storage-policy.md` are not Parent-wide primary owners.

## Historical audit material

Policy-consistency reports, historical runtime reports, generated analysis snapshots, and coverage snapshots are evidence/history, not operational primary policies. Keep them outside the normal routing path under `.codex/audit/` or run-specific evidence roots.
