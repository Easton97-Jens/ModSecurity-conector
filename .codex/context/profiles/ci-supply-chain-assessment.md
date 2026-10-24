# CI and Supply-Chain Assessment Profile

## Scope

Assess GitHub workflows, permissions, untrusted-input boundaries, action/image/tool provenance, dependency pins/locks, download/extraction paths, build caches, artifacts, scanner/tool provisioning, host/library/toolchain compatibility, and read-only current remote CI state.

## Load

- `../command-execution-policy.md` for every local shell/project command;

- `../security/checks/supply-chain.md`
- `../security/checks/config-injection.md`
- `../security/checks/logging-disclosure.md`
- `../security/checks/evidence-integrity.md`
- `../security/checks/advisory-research.md`
- `../tooling-and-language.md`
- `../python-policy.md`
- `../testing-and-evidence.md`
- `../sonarqube-policy.md` when applicable

## Rules

Do not trigger delivery workflows merely to assess them. Remote CI inspection is read-only unless the current user separately authorizes an action. Treat moving versions, unverified downloads, credential exposure, artifact/cache confusion, and unsafe workflow expression-to-shell/file sinks as candidate risks requiring concrete repository evidence.
