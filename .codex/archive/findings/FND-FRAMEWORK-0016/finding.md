# FND-FRAMEWORK-0016 — Security-tool downloader accepted an unconfined lock-file path

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0016` |
| Category | `security_hardening` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P2` / `medium` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary

The generic `--lock` CLI boundary in the security-tool downloader accepted a
regular non-symlink lock file outside the Framework root. The checked-in
workflow invocation was trusted, but the generic CLI confinement was too broad.

## Evidence and remediation

`ci/tools/fetch-security-tool.py` now resolves relative locks from the
Framework root and rejects out-of-root absolute/traversal paths, symlink
components, symlink leaves, and nonregular files before YAML parsing. Focused
regressions accept the real Framework lock and reject external, traversal, and
symlink paths. The remediation is committed in
`768a06b5b734547f8213cc6918c26ef4a8ef9f67`; exact local `make lint` and 64
CI-security tests passed. Retained artifact SHA-256:
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`.

## Acceptance criteria

- `--lock` is confined to the Framework root before lock parsing.
- Legitimate relative and absolute in-root lock paths remain accepted.
- External, traversal, symlink, and nonregular paths fail before YAML access.
- Exact final PR-head CI confirms the committed downloader behavior.

## Residual risk and history

The actual workflow lock was trusted before the repair, but generic CLI callers
now have fail-closed confinement. Remote exact-head evidence remains pending.
`2026-07-18T15:18:00Z`: created and locally fixed.
