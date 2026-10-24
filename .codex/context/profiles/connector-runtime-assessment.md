# Connector Runtime Readiness Assessment Profile

## Trigger

Use when the user wants one connector/logical profile exercised through the real repository build/config/start/traffic/evidence chain without requesting a full deep-security discovery scan.

## Load

- `../command-execution-policy.md` for every local shell/project command;

- `../testing-and-evidence.md`
- `../resources-and-storage.md`
- `../architecture-and-boundaries.md`
- `../protocol-and-hardening.md`
- selected `../security/connectors/<connector>.md` for host boundaries
- `../security/checks/response-commit-phase4.md`
- `../security/checks/evidence-integrity.md`
- `../security/checks/runtime-failure-recovery.md`
- additional security checks only when the changed/runtime boundary requires them

## Runtime chain

For the selected logical profile evaluate, as applicable:

source/dependencies -> build -> binary/module/service identity -> config -> start -> readiness -> Allow -> rule-based Block -> P2 -> P3 -> P4 -> failure/recovery -> cleanup -> evidence validation.

Do not skip directly from build to a runtime claim. Do not promote compatibility/profile sibling evidence.

## Repetition and stability

Where safe and repository-native, include a small bounded repeat/keepalive sequence and a legitimate follow-up after a failure. Use the host-specific connector delta for relevant state/lifecycle hazards.

## Output

Produce a concise runtime matrix with actual commands/actions, evidence, reached stage, failures/blockers, profile identity, and claim boundary.
