# PR #382: review and merge-decision closeout

**Language:** English | [Deutsch](pr-382-merge-readiness.de.md)

## Scope and revision binding

This is the leading status document for the separately authorized 2026-10-25 inventory/runner/coverage migration. Its base is `d510d21dba7eab3c9f0ccbe579fbc9c105eb3da1`, where #410 was already integrated. The historical [checklist](pr-382-checklist.md), [handoff](pr-382-i12-handoff.md), [remaining matrix](pr-382-i09-i12-rest-matrix.md) and [reduced I12 closure](pr-410-i12-closeout-20261024.md) retain their original revisions and results; their old work instructions are superseded. No new `I12_COMPLETE` or historical host qualification follows.

This document records the implemented selection and measurement contract. Final exact-head local/remote/PR identity, checks, coverage import/metrics and Ready state must be read from the [PR description and checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382). Earlier successful CI/Sonar at the base does not verify a follow-up commit.

## One active selection

`config/testing/active-cases.json` is the only active selector authority. Every execution explicitly enumerates stable behavioral case IDs, requirements and logical profiles, including independent parameters inside collectors. The runner validates the entire expanded inventory against its literal ceiling of 100 before any selected child; group, case, execution and Go-module filters do not create separate budgets. A selected collector always includes all its declared variants. Unknown/empty selections, source drift and alternate executable inventories fail; selection is never truncated.

The reviewed inventory contains 100 unique expanded cases across 81 executions. Static review includes nested Make/build/scheduled selectors and confirms original assertions in the 436 pre-existing hook-manifest sources were preserved. The initial 21 migration/report controls passed, including rejection of 101 synthetic cases before a sentinel child starts. Those controls consume the same budget. A repeat locally or in CI is execution cost, not another distinct active case.

Default entry points are `make test`, `make lint` and `python3 ci/tools/run-active-tests.py`; all automatic workflows and nested functional build/lint checks must use the same inventory. Python discovery is bound at package and module boundaries; direct specialist catalogs require explicit opt-in. Static builds, lint, dependency/secret scanners and actual configuration validation retain their own substantive gates.

The generated specialist disposition `reports/testing/test-selection-archive.generated.json` is owned by `ci/tools/update-test-archive.py`. It is non-executable and counts definitions, not fully expanded archived scenarios. Retained specialist sources provide no new PASS. Explicit specialist work requires `ON_DEMAND_TESTS=1` and its documented specific command; this is outside automatic default selection.

## Retained and lost automatic coverage

The generated archive retains specialist definitions and source hashes; it currently records 5930 on-demand Python/Go definitions, not expanded scenarios. This is deliberate lost automatic coverage, not a claim that all removed cases were duplicates. Retained automatic security intents include real memory wiping/allocation limits, HTTP header/body deadlines and recovery, Parent APR-util pin policy/current Framework provenance, peer ownership, report identity and source-bound admission.

Archived requirements include full redirect/option/capacity/parser parameter matrices, I09/I10/I12 fault and lifecycle campaigns, full scaffold/validator corpora, randomized fuzzing, full H2/H3 preflight, NGINX inheritance/override/reload/error-page/body-buffer campaigns, broad MRTS catalogs and the omitted installer/admission/header/phase variants. In particular, unknown/empty group controls and the installer private-root positive control are retained on demand; their production guards remain enforced. No sibling profile inherits proof: HAProxy SPOE differs from HTX; Envoy ext_authz differs from ext_proc; Traefik forwardAuth differs from native; lighttpd compatibility differs from stock/patched-native. See the [testing guide](testing-and-evidence.md) and [source roles](sonar-source-roles.md).

The planned acceptance union is 56 coverage cases, two additional shell path cases, four scanner fixtures, one stock-sidecar case, three strict peer cases, 21 No-CRS config/start/allow/deny cases, 11 CRS cases and two NGINX callback cases. Repeating an ID in lint, local coverage or Hosted CI does not add an independent case. Local and Hosted outcomes are recorded separately; unexecuted or blocked cases are never reported as passed.

## Coverage and evidence limits

Previous Sonar Automatic Analysis did not import coverage: coverage measures were absent, while `new_lines_to_cover` was zero. This was not a measured 0% result. CI-based analysis collects reports during real inventory-selected execution. Python uses actual stdlib line tracing, the four Go modules retain native `go test` profiles, and GCC/gcov measures actual linked C and C++ sources. Extracted temporary native fixture text is not attributed to original production source. Eligible same-prefix/UID Python children are traced without changing isolation flags. Isolated, clean-environment, other-prefix/UID or killed children and unexecuted host paths may remain unmeasured. These are line measurements, without branch observations.

The report manifest binds source revision, dirty/clean state, inventory digest, selected case IDs, source/report hashes, toolchain, actual SDK identity and source-role/scanner configuration hashes. Both properties must match the reviewed source-role contract before collection/import. Scanner import requires clean exact-published source. Report generation, successful import and final total/new-code server metrics are separate claims; each still requires observed evidence. Existing Quality Gate conditions, production scope and New Code baseline remain unchanged. The existing gate requires `new_coverage >= 80`; its earlier project-status result omitted that condition because coverage measures were absent. The threshold is retained.

## Later maintenance operation

Only a separate authorized master integration enables default-branch live proof. Check trusted resolver, validator and publisher results for Go/Python/Actions; inspect an actual allowed candidate and genuinely generated maintenance PR, author/base/head/diff and downstream required CI. A no-update run does not prove PR creation. Go uses `github.token`; inspect any approval-required PR-triggered workflow before claiming unattended execution. Dependabot covers weekly pip and the four Parent Go directories with a seven-day Go cooldown; its configured five-PR limit is not asserted as a global cap. No default-branch publication is performed by this task.

## Traceability

[Change Record](../reports/audits/change-records/CR-20261025-pr382-global-inventory-coverage.md). Framework/MRTS sources, repositories and gitlinks remain outside the write scope. No master merge, release or deployment is authorized.
