# Change Record: CR-20261008-nginx-config-three-native-contracts

**Language:** English | [Deutsch](CR-20261008-nginx-config-three-native-contracts.de.md)

Focused Parent configuration orchestration change.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-config-three-native-contracts |
| Date (UTC) | 2026-10-08 |
| Base revision | `45754c0a0f0ae3dbd04f63a028d342bdac61220a` |

## Motivation and problem statement

Register three closed native configuration rejection operations: invalid_status and the two removed modsecurity_phase4_content_types_file cases. Removed API rejection must not masquerade as Engine MIME parsing.

## Acceptance criteria

Require exact rejection fragments, exit code, retained configuration line and byte-identical controlled regular fixtures; reject foreign configuration paths or modified fixture bytes. Preserve existing configtest operations.

## Implementation decision and rationale

Quote inline modsecurity_rules through JSON escaping. Retain bounded 0600 single-link regular MIME fixtures and their SHA256 only for the two explicit removed-API cases. Collector carries the closed fixture fields and requires retained fixture artifacts.

## Changed files

ci/runtime/lifecycle/run-nginx-configtest.py; ci/runtime/lifecycle/collect-no-crs-source.py; tests/test_nginx_migration_driver.py; tests/test_nginx_migration_collection.py; this EN/DE record pair.

## Commands executed

RTK-wrapped Parent .venv unittest of tests.test_nginx_configtest_driver, tests.test_nginx_migration_driver, tests.test_nginx_configtest_collection and tests.test_nginx_migration_collection passes 83 tests; external log stream-c-parent-config.log retains the result. In-memory compile passes all four changed Python files. ci/tools/new-change-record.py check, make check-bilingual-docs and make check-doc-links (explicit current Framework checkout) pass; diff whitespace is clean.

## Security impact

Controls bind parser diagnostics to exact retained inputs; regular fixture identity, type, ownership, permissions, bounds and content are checked. No validation or source authority is weakened.

## Runtime evidence

No fresh native runtime was run for this delivery. Controlled fake-host unit tests prove orchestration and rejection classification only.

## Known limitations

The removed directive is rejected by NGINX before reading its argument file. These cases do not establish wildcard MIME or Engine content-type behavior.

## Remaining risks

Fresh integrated configuration/runtime and canonical evidence remain coordinator-owned. Retained unit receipts alone cannot prove runtime coverage.

## Checks not run and rationale

No build, native runtime, E2E, remote CI, Sonar or push: prohibited by this bounded integration task.

## Final diff and review status

Reviewed focused Config3 slice and negative controls; separate commit only these four Python files and generated bilingual record. Concurrent slices remain unstaged.
