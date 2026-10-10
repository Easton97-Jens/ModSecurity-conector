# Change Record: CR-20261008-nginx-missing-rules-filename-quality

**Language:** English | [Deutsch](CR-20261008-nginx-missing-rules-filename-quality.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-missing-rules-filename-quality |
| Date (UTC) | 2026-10-08 |
| Base revision | `8004340da887d143bc5e850822ac122eb5ce8b59` |

## Motivation and problem statement

Historical Parent issue AaEa7bLqEJ_FL6Iil9V7, python:S1192, still matched three identical missing-rules.conf literals in the current configtest producer. Other quality refactors did not change this file. This separate slice addresses that remaining source duplication; remote resolution requires a new-revision scan.

## Acceptance criteria

Replace only those three producer literals with one constant, preserving exact configuration value, diagnostic fragments and absent fixture leaf/state. Existing config/collection/wiring guards remain unchanged. No validator, security, selection or runtime behavior changes.

## Implementation decision and rationale

Introduce MISSING_RULES_FILE_NAME and use it for the contract value, diagnostic fragment and CONFIGTEST_PATH_FIXTURES tuple. An existing driver test module gains one narrow characterization test with independent exact-string expectations. No helper extraction, suppression or broader refactor.

## Changed files

ci/runtime/lifecycle/run-nginx-configtest.py; tests/test_nginx_configtest_driver.py; this EN/DE record. Separate external source-quality-reconciliation.md was persisted before this implementation; the quality CSV is not edited.

## Commands executed

All commands RTK-wrapped with Parent-owning Python and external TMPDIR. New test-first test_missing_rules_constant_preserves_all_closed_contract_values ran1 test and exited1 because MISSING_RULES_FILE_NAME was absent. `rtk proxy env TMPDIR=<external-task-runs> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PARENT_TEST_FRAMEWORK_ROOT=<explicit-framework-root> python -m unittest tests.test_nginx_configtest_driver tests.test_nginx_configtest_collection tests.test_nginx_selected_configtest_wiring -q` passed51 tests, exit0, with no skips. `rtk proxy python ci/tools/new-change-record.py check` exited0 (structure only). Whitespace check exited0. AST characterization additionally requires exactly one producer literal.

## Security impact

Semantics-preserving filename naming only. Exact diagnostics, fixture absence/path authority, artifact containment, exit handling and acceptance checks remain unchanged.

## Runtime evidence

Controlled subprocess/unit tests only; no genuine NGINX invocation, canonical PASS or all-required completion claim.

## Known limitations

Stored Sonar readbacks still mark the historical issue OPEN. Source correction is not remote RESOLVED evidence.

## Remaining risks

Coordinator must integrate the separate normal commit and run the relevant fresh scan. No Framework/MRTS/Gitlink changes belong to this slice.

## Checks not run and rationale

Native build/runtime, full E2E, push and remote Sonar analysis are outside the bounded authority. No tool or dependency installation.

## Final diff and review status

Four owned files in a fresh isolated Parent worktree based exactly on the stated revision; unchanged literal values reviewed. Final focused results and normal commit handed to coordinator separately.
