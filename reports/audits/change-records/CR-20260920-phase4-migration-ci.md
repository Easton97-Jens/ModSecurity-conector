# Phase-4 migration consistency and pre-merge verification

**Language:** English | [Deutsch](CR-20260920-phase4-migration-ci.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260920-phase4-migration-ci` |
| Date (UTC) | `2026-09-20` |
| Base revision | `0819bd819bf6f699149adb8fcdd067895abd0862` |

## Motivation and problem statement

PR #380 contained only part of the migration from minimal/safe/strict to
off/safe/strict with engine-owned MIME selection. Obsolete source-contract
tests, incomplete example moves, stale generated documentation, and PR steps
that skipped the actual lint run concealed failures until after merge.

## Acceptance criteria

The existing PR retains its changes and additionally contains consistent
off profiles, source-backed EN/DE references and capability declarations.
NGINX mutation tests reject unreachable body appends and ignored errors.
The same lint/quick-check commands run before and after merge. No protection
or runtime enforcement is weakened to obtain a passing check.

## Implementation decision and rationale

Retain bounded body processing, native off behavior, and safe/strict behavior.
Replace tests of the removed MIME loader with absence/engine-ownership guards.
Restore the full direct chain-call/error-return contract, rather than counting
a matching string. Move the remaining HAProxy SPOE/SPOP companion files into
off and keep host/agent socket paths identical. Regenerate references through
their source generators. Preserve historical evidence and capability states.

## Changed files

The change covers the five lint/structure workflows, the NGINX adoption checker
and its three regression suites, the new Phase-4 migration guard, configuration
and guide generators with their tests, the Common event metadata comment,
current connector capability descriptions, active off examples and paired
READMEs, generated configuration references/inventory, and this EN/DE record.
Generated capability catalogs are refreshed from manifests without runtime
promotion. Framework and MRTS source/pins are unchanged.

## Commands executed

Local checks used Python APIs on an authenticated tracked-source archive:
33 migration/native/upstream security tests, 96 checker mutation tests,
20 configuration/guide tests, and 34 workflow regression tests passed.
The 21 configuration-reference outputs and the full reference semantic checker
passed, as did the six-manifest capability validator and NGINX adoption checker.

Supplemental capability/wiring tests ran 38 tests with no failures/errors and
three Framework-dependent skips. Runtime-evidence tests ran 58 tests with one
failure, two errors, and three skips caused by the absent Git checkout/Framework
catalog in the archive. These results are not reported as full-suite passes.
Hosted runs use the actual Git checkout, recursive pinned submodules, and the
repository's Python version for authoritative pre-merge validation.

## Security impact

No runtime fail-closed branch, resource bound, logging-file guard, rule loading
policy, CI requirement, or branch protection is relaxed. Regression coverage
is strengthened for call reachability and error propagation. CI execution uses
read-only repository permissions; publishing is separate from test execution.

## Runtime evidence

No new client-visible NGINX/Apache/other host result is asserted. Source,
generator, and mutation tests do not establish runtime response blocking.

## Known limitations

The local archive lacks Git metadata, submodule contents, and native host build
prerequisites. Hosted checks remain the authority for their own test layers.

## Remaining risks

Host-specific response commitment and supported abort behavior still require
the selected native runtime profiles. Old dated reports remain historical and
must not be interpreted as verification of the current head.

## Checks not run and rationale

No local full native build or six-connector runtime matrix was performed.
No merge, release, dependency upgrade, or external deployment was requested.

## Final diff and review status

Source changes and generated-reference differences were reviewed together.
This record documents local evidence; final hosted job results are attached
to the exact PR head rather than inferred from a skipped or earlier green job.
The PR is not automatically merged.
