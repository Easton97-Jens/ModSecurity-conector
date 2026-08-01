# FND-FRAMEWORK-0014 — CRS version-pinning check used predictable temporary files and lossy pathname iteration

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0014` |
| Category | `security_hardening` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P2` / `medium` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary

The CRS version-pinning shell validator wrote scan output to a predictable
shared `/tmp` filename and enumerated shell paths with word splitting, allowing
same-host interference and a whitespace filename coverage gap.

## Evidence and remediation

`ci/checks/catalog/check-crs-version-pinning.sh` now validates its runner-
temporary root, applies `umask 077`, uses private `mktemp` files, cleans them
with a trap, checks grep failures, and passes NUL-delimited paths through a
recursive `--check-path` mode. The committed remediation is
`768a06b5b734547f8213cc6918c26ef4a8ef9f67`. Exact local head validation
passed `make lint`, shell syntax, the CRS pinning contract test, and whitespace
checks; retained artifact SHA-256 is
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`.

## Acceptance criteria

- No predictable global temporary filename is used.
- Shell filenames containing whitespace are checked exactly once.
- Failures to enumerate or scan paths fail the validator.
- Exact final PR-head CI confirms the committed behavior.

## Residual risk and history

The local fix is verified; remote exact-head CI and review evidence are pending.
`2026-07-18T15:18:00Z`: created and locally fixed with retained evidence.
