# Change Record: CR-20261008-nginx-native-operation-collection

**Language:** English | [Deutsch](CR-20261008-nginx-native-operation-collection.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-operation-collection |
| Date (UTC) | 2026-10-08 |
| Base revision | `63d2f9a38c506e5122ace9ba36927add7f47e377` |

## Motivation and problem statement

The generic collector drops native wrappers and may interpret or scrub referenced event logs. Native records need a separate closed route before generic status, event and alias handling.

## Acceptance criteria

Preserve original bounded native wrapper/identity/revision/actual-exit fields under explicit caller authority; produce no canonical events or PASS. Missing/foreign authority, unsafe paths, unknown fields, duplicate identities and malformed exit values fail closed. Preserve existing configuration and harness collection.

## Implementation decision and rationale

`--allowed-native-operation-root` defaults to None and is never inferred from a row. `case_row_observations` and `case_observations` accept the optional `allowed_native_operation_root` parameter. `nginx_native_collection.collect_native_row` checks the existing closed 42-case dispatch mapping and reference safety; Framework remains responsible for canonical/runtime proof. Zero actual exit preserves NOT_EXECUTED; nonzero actual exit is retained and marked FAIL. Both routes return no native events or aliases.

## Changed files

`ci/runtime/lifecycle/collect-no-crs-source.py`, new `ci/runtime/lifecycle/nginx_native_collection.py`, new `tests/test_nginx_native_operation_collection.py`, and this EN/DE record. Existing configuration receipt constants/helpers and host/baseline wrappers are not changed; Root's separate Config3 changes must be preserved during integration.

## Commands executed

`rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_native_operation_collection` initially exited 1 (missing CLI/API and absent authority rejection), then passed all 13 focused tests. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PARENT_TEST_FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_nginx_native_operation_collection tests.test_collect_no_crs_source tests.test_collect_no_crs_source_helpers tests.test_nginx_configtest_collection tests.test_nginx_native_operation_dispatch -v` passed 91 tests, exit 0, with three Gitlink-trust skips. The broader selected-runner wiring suite had two existing missing Apache-submodule-fixture failures; it is not claimed green. Three changed Python files parsed with `ast.parse`; `rtk git diff --check` passed. Parent archive and pair checks validate documentation structure, not runtime proof.

## Security impact

Authority and bundle paths must be absolute external children of `/var/tmp/codex/ModSecurity-conector`, owned and nonwritable by others, with no checkout or followed symlink. Original receipts must be bounded, owner-only, regular, single-link files matching wrapper hashes. E parent/child paths and seals are closed. Native raw logs/captures remain unchanged; native paths are rejected from generic source-event and consumed-event lists before scrubbing.

## Runtime evidence

Only controlled collection/fixture tests ran. No NGINX build, live native request, canonical Required-case PASS or Exact-Head proof is claimed.

## Known limitations

This layer validates safe collection references, not actual engine callbacks, final artifact authority, or canonical case semantics. Three Framework checks skipped because the supplied Framework HEAD differs from the Parent Gitlink.

## Remaining risks

Root must wire the explicit authority through host/baseline orchestration and integrate Framework strict proof/retention. Required source-hash closure must account for the new collection helper when applicable. No missing authority or nonzero exit can be promoted.

## Checks not run and rationale

Native build/runtime, full E2E, wrapper/baseline wiring and canonical proof validation were not run or changed because they are outside this bounded collection slice. No packages were installed; Ruff was unavailable and not installed.

## Final diff and review status

Reviewed only the collector seam, owned helper/tests and paired record. Raw evidence stays original; config/harness behavior remains separate. Fresh focused and collector regression results support this slice, while runtime and isolated-submodule gaps remain explicit.
