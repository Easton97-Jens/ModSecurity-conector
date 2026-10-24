# Change Record: CR-20261008-nginx-pointer-protocol-cleanup-selection

**Language:** English | [Deutsch](CR-20261008-nginx-pointer-protocol-cleanup-selection.de.md)

Bounded event projection; original raw bytes retained.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-pointer-protocol-cleanup-selection |
| Date (UTC) | 2026-10-08 |
| Base revision | `bcb02b6b20c2e0697be3c0cd8013ce9b28aa1afa` |

## Motivation and problem statement

New native post-return cleanup evidence shares the P1 JSONL sink. Feeding all rows to the strict one-protocol-error helper incorrectly includes cleanup.

## Acceptance criteria

Select only actual source-bound own P1 protocol_error; preserve original JSONL and hashes including cleanup; retain strict wrong-TX/phase/URI and duplicate negatives. No native run/build.

## Implementation decision and rationale

select_protocol_events(rows,transaction,path) requires exact native nginx connector/mode, protocol_error/MSCONN_EVENT_PROTOCOL_ERROR, request_headers, same transaction, POST and exact URI. It filters without editing records; zero/multiple or malformed selected errors remain rejected by the unchanged strict Framework helper. Full raw phase1-events.jsonl hash/capture remains unchanged.

## Changed files

Parent ci/runtime/lifecycle/run-nginx-common-input-fault.py, tests/test_nginx_common_input_fault_driver.py and this paired record only. Root module/Framework helper read-only.

## Commands executed

RTK-wrapped focused Parent unittest with explicit FRAMEWORK_ROOT: first exit1 absent selector, final exit0/three tests with no skips. Pure mixed JSONL file bytes and SHA stay identical. Framework strict helper is standard-library-only and loaded read-only from explicit boundary. Portable command: `rtk proxy env FRAMEWORK_ROOT="${FRAMEWORK_ROOT}" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p test_nginx_common_input_fault_driver.py`. Native record scaffold created exit0; final checks in handoff.

## Security impact

No fabricated events or raw rewrites. Selector narrows to actual own request identity without weakening downstream status/action/rule/error checks. Wrong TX/phase/URI/method/connector/mode and duplicate-valid rows fail strict helper.

## Runtime evidence

No runtime/build performed. Read-only current Root cleanup source calls Common cleanup, then native void cleanup, then emits its logging event; pure tests model only coexistence, not native cleanup PASS.

## Known limitations

Pure tests are not live pointer injection evidence. When Framework helper is absent, the extra helper integration test explicitly skips; this task's actual command supplied FRAMEWORK_ROOT and observed zero skips.

## Remaining risks

Root must integrate updated driver/source hashes and perform exact native runtime validation. Existing reader guide MIME-scope/content_type_not_in_scope sentence is stale relative to source-only late intervention resolution; flagged to Root, not edited.

## Checks not run and rationale

No native runtime/build, Framework mutation/tests, MRTS, scanner, push or main integration. Scoped Parent pure checks only; broader integrated checks remain Root-owned.

## Final diff and review status

Scoped review confirms full original raw hash loop retained and only observed event projection changed. Commit and final validation delivered separately; no runtime promotion claimed.
