# Change Record: CR-20261008-selected-nginx-native-operations

**Language:** English | [Deutsch](CR-20261008-selected-nginx-native-operations.de.md)

Closed Parent dispatcher and source adapter; no runtime promotion.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-selected-nginx-native-operations |
| Date (UTC) | 2026-10-08 |
| Base revision | `4a28d86fa0d052397e74f0843ca6931e3dd17cae` |

## Motivation and problem statement

Route the new 42 selected native NGINX invocations to real closed host drivers without changing the existing 52-case collector or three configuration operations.

## Acceptance criteria

Exactly five groups/42 strict catalog descriptors, shared selection variable, fresh external output/projections, true source SHAs/Gitlink, required fault fixtures, actual exits, original receipt seals and NOT_EXECUTED output. No native process/build/E2E for this slice.

## Implementation decision and rationale

The dispatcher accepts only exact native_invocations.nginx descriptors including the two aliases and nine closed overrides; catalog commands are never executable. It uses NO_CRS_SELECTED_CASE_IDS, BUILD_ROOT, RESULTS_DIR, NGINX_PREFIX, FRAMEWORK_ROOT and NO_CRS_RUN_ID. Output is BUILD_ROOT/host-runtime/native-operations-<run>/<case>, with fresh projection parents per case and independent E child projection roots. The source adapter preserves original source receipts and emits status/canonical_status NOT_EXECUTED. native_operation_receipt carries schema_version1/case/run/operation/native mode/absolute bundle_root/optional source_record_id, invocations main|at|over with relative receipt_path and SHA256, mandatory namespaced source_sha256 from Framework required_source_paths(case_id), and an E parent receipt path/hash. True Parent/Framework/MRTS SHAs and Parent Framework Gitlink remain separately recorded.

## Changed files

New ci/runtime/lifecycle/run-selected-nginx-native-operations.py, nginx-native-operation-source.py, tests/test_nginx_native_operation_dispatch.py, and this paired record. No existing collector, wrapper, driver, Framework, MRTS or Root integration file edited.

## Commands executed

RTK-wrapped native scaffold create; focused `rtk proxy "${PARENT_PYTHON}" -m unittest discover -s tests -p test_nginx_native_operation_dispatch.py`: initial exit1 missing new implementation, final exit0/eight tests (no native processes). A second failing orchestration check exposed protected placeholder .git directories; repository-native actual checkout detection fixed it. Exact C catalog descriptor comparison: 42, exit0. AST parse of three files: exit0. `rtk proxy "${PARENT_PYTHON}" -m ruff --version`: exit1, unavailable. Required env-presence probe: all five false, no values printed. Final record/pair/diff checks recorded at handoff.

## Security impact

Closed command/case routing; strict duplicate selection/catalog refusal; external fresh state; all receipt path components NOFOLLOW, bounded owner-only regular single-link leaves; safe append preserves existing rows, rejects selected duplicates and uses an exclusive nonblocking lock. Source hashes use the reader-owned closed namespace list, never receipt-chosen arbitrary paths. Required native fault libraries fail closed.

## Runtime evidence

No native runtime/build executed. Mocked subprocess receipts prove only dispatcher orchestration and preserve driver exit7/0 as NOT_EXECUTED, not Engine/host PASS. Root owns integrated runtime slot and canonical promotion.

## Known limitations

Depends on the integrated actual drivers and Framework nginx_native_operation_bundle.py required_source_paths API; not copied or cherry-picked into this isolated Parent slice. Event child names at/over map original at255/over256 directories and run suffixes; metadata main maps long-query. Original parent envelope remains sealed. Missing receipts fail closed rather than fabricate evidence.

## Remaining risks

Root must wire collector/wrapper and export actual NGX_NATIVE_INPUT_FAULT_LIBRARY, NGX_NATIVE_BEGIN_FAULT_LIBRARY, NGX_NATIVE_WRITE_FAULT_LIBRARY, NGX_NATIVE_FINISH_FAULT_LIBRARY and NGX_NATIVE_ENGINE_BUDGET_FAULT_LIBRARY for their exact cases. No fallback to no-fault execution. Full integrated reader/driver/runtime verification remains outstanding.

## Checks not run and rationale

No native runtime, build, full E2E, Framework/MRTS tests, publication or push per scope. Parent Ruff unavailable; no package installed. Integrated bilingual link check requires Root's materialized Framework boundary; isolated worktree has 22 known existing missing targets.

## Final diff and review status

Scoped local review covers only five new files; final validation results and local commit SHA are handed to Root. No existing52/config3 mutation or shared file edit; no external delivery claimed.
