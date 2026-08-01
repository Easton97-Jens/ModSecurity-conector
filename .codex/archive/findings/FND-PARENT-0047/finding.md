# FND-PARENT-0047 — Go CodeQL version-contract checker allowed YAML-equivalent literal selectors

Category: security_hardening\
Repository / ownership: parent / parent\
Priority / severity / confidence: P2 / low / reproduced\
Status: closed\
Release blocker: false\
Security relevant: true\
Protocol: GitHub Actions CodeQL Go toolchain-selection contract\
Delivery state: verified_exact_head_ci_and_sonarqube_cloud_passed

## Summary

The static Go version contract is a defense-in-depth admission control for
untrusted pull-request workflow changes. Its former partial line checks accepted
a with mapping that retained go-version-file: .go-version but added a
YAML-equivalent literal go-version selector. The immutable actions/setup-go v7
source warns when both inputs are present and resolves literal go-version before
go-version-file, so the central authority could be bypassed while the checker
reported success.

The condition is low impact because a workflow edit still needs the repository
pull-request/review path. It is nonetheless a reproducible broken CodeQL
workflow control and is task-owned by PR #90, although it predates the local
Sonar-remediation follow-up from d99eafd76d9fdbef5b63a19d084fd2d7caff6c08.

## Affected files, preconditions, and reproduction

Affected files are ci/checks/common/check-go-version-contract.py and
tests/test_go_version_contract.py. The entry point is the Parent CodeQL
workflow's envoy-go and traefik-go actions/setup-go steps.

A proposed workflow needs to reach the static contract checker and contain both
the central-file input and a semantically equivalent literal key. Before the
remediation, each of these variants returned an empty violation list:

- go-version : '1.26.5'
- 'go-version': '1.26.5'
- "go-version": "1.26.5"
- ? go-version followed by : '1.26.5'

The retained reproduction and post-fix rerun are in
go-contract-literal-selector-remediation.txt (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/go-contract-literal-selector-remediation.txt`)
with SHA-256 1d924a16b3c724861070bafe652c487c6bcaf0f512a415dc1ae10a9fa7c32fcc.

## Root cause, impact, and remediation

The former checker accepted required lines independently and rejected only one
exact bare go-version: spelling. YAML permits equivalent mapping keys, so the
text-level control did not enforce one unambiguous selector.

The immutable v7 action source at
[actions/setup-go b7ad1dad31e06c5925ef5d2fc7ad053ef454303e](https://raw.githubusercontent.com/actions/setup-go/b7ad1dad31e06c5925ef5d2fc7ad053ef454303e/src/main.ts)
prefers go-version when both inputs are supplied. A reviewed workflow could
therefore select a literal Go version instead of .go-version, weakening
toolchain reproducibility and confidence in CodeQL's centrally reviewed
compiler/runtime.

The local repair requires the complete setup-go with body to equal exactly:

    with:
      go-version-file: .go-version
      check-latest: false

Any additional, alternate, quoted, whitespace-variant, explicit-mapping,
anchor/merge, or malformed input shape fails closed. The immutable action pin,
expected job inventory, central file, and filesystem checks are unchanged.

## Acceptance, validation, and controls

Acceptance requires all four original variants to be rejected; the checked-in
workflow to pass with the exact mapping; action pin and job inventory to remain
exact; and focused tests, checker target, CI-security tests, final security
review, and exact-head hosted checks to pass before verification.

Passed locally:

- tests.test_go_version_contract: 6 tests, including the four bypass classes
  and the valid central-selector control.
- make check-go-version-contract.
- Python syntax compilation for checker and test.
- git diff --check.

Wrong action pins, literal selectors, unlisted Go jobs, and symlinked
.go-version files remain rejected.

The subsequent complete remediation validation passed 100 focused tests, all
static contracts, syntax compilation, safe CLI-help smokes, and `git diff
--check`. The final security-diff scan reported zero findings:
report.md (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/tmp/codex-security-scans/ModSecurity-conector/d99eafd76d9_20260722T221118Z/report.md`)
(SHA-256 `12df4f3ed8d6f850feaf644a512d7bd1de0c3b41b6fffb5e99e021e21a25e1b4`).

## Dependencies, blockers, residual risk, and history

Exact head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` completed its ordinary
GitHub checks successfully or skipped and passed the SonarQube Cloud Quality
Gate. The finding is verified; no risk is accepted. Related finding
FND-SONAR-0010 owns the former hosted Quality Gate failure.

- 2026-07-22T22:18:00Z: reproduced four bypass variants and inspected the
  immutable action input precedence.
- 2026-07-22T22:28:04Z: implemented the exact-body rule; focused tests,
  checker target, syntax compilation, and whitespace validation passed.
- 2026-07-22T22:47:54Z: complete local remediation validation passed (100
  focused tests, contracts, syntax, safe CLI-help, and diff validation); the
  complete security-diff scan reported zero findings. Hosted proof remains
  pending.
- 2026-07-22T23:02:27Z: exact head `06a4e71` passed ordinary hosted checks and
  SonarQube Cloud Quality Gate; the selector-control repair is verified.

## Closed disposition — 2026-08-01

[PR #90](https://github.com/Easton97-Jens/ModSecurity-conector/pull/90) merged
normally as `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3`, reachable from current
`origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`. The current checker
still requires `go-version-file: .go-version` and rejects the equivalent
literal selector; the affected scope has not changed since the merged fix.
Exact PR checks, including CodeQL and SonarCloud, passed.
