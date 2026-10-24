# Change Record: CR-20261015-haproxy-current-host-fixtures

**Language:** English | [Deutsch](CR-20261015-haproxy-current-host-fixtures.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-haproxy-current-host-fixtures |
| Date (UTC) | 2026-10-15 |
| Base revision | `1b4e1dc041a9080cd84cd8c70ba053cd77c3fa3f` |

## Motivation and problem statement

Prepare fresh HAProxy acceptance fixtures after product integration while preserving every original requirement and historical result. Simplify and harden the HAProxy harness paths identified by the current Sonar analysis; local edits do not establish server-side issue closure.

## Acceptance criteria

Bind all 278 original HAProxy IDs and selected contracts to immutable snapshot hashes; prepare 80 native and 49 companion capture-ready fixtures, retaining explicit gaps. Preserve observation/qualification boundaries and existing capture definitions. Run focused regression tests; make no new host or lifecycle-PASS claim.

## Implementation decision and rationale

Add source-bound native and companion fixture planners; extract focused helpers from complex harness paths. Validate admitted physical paths and reject symlink/traversal inputs; record actual relay forwarding and terminal states. Keep source-oracle values, actual measurements and qualification separate. No product, shared capture, central matrix, generator, Framework/MRTS or other connector change.

Continuation on 2026-10-18 aligns native v6 and companion v5 fixture behavior: negative rules, malformed framing, client cancellation and MRC faults target only the main transaction; healthy neighbors retain clean small responses. Comparators require actual Content-Length framing and independent transport-abort observations; a timeout or incomplete body alone does not establish a reset. MRC wire protocol version `2` is checked against the primary product C header, and client transport aliases preserve the same measured facts. Earlier v3/v4 attempts that failed before host execution remain recorded as `HARNESS_DEFECT`.

## Changed files

`connectors/haproxy/harness/i12_companion_host.py`, `i12_native_cases.py`, `i12_native_observe.py`, `i12_spop_host.py`, `i12_spop_wire.py`; new `connectors/haproxy/harness/i12_companion_cases.py` and `i12_native_contracts.py`; `tests/test_haproxy_i12_companion_host.py`, `tests/test_haproxy_i12_native_cases.py`, `tests/test_haproxy_i12_spop_wire.py`; this EN/DE Change Record pair. The separate work-in-progress `i12_current_capture.py`, `i12_request_scope_observer.c`, `test_haproxy_i12_current_capture.py` and new oracle artifacts are excluded from this initial harness commit.

## Commands executed

Worker evidence reports 45 focused unittests passing under CPython 3.14.4. Local Sonar-remediation regression evidence reports 28 passing tests; these are overlapping focused suites, not additional host runs. Historical Root evidence independently reran the earlier focused harness suite under CPython 3.14.7: 45 tests and 41 subtests passed, exit 0. Older 45-/53-test receipts remain historical evidence and do not validate the latest changes. Exact argv, cwd and output hashes are retained in external run `i12-haproxy-415-acceptance-20261015/commands/current-haproxy-harness-pytest-v1.json` and its stdout. The fresh combined Root CPython 3.14.7 run on 2026-10-18 passes 55 tests and 56 subtests, exit 0. Exact wrapped argv, cwd, times and output hashes are retained in `i12-haproxy-415-acceptance-20261015/commands/current-haproxy-harness-20261018-v1.json`; its stdout SHA-256 is `4bb12b1d51dfbcfea2713684101f77b80ed6f4ef127fc98ea8d1ffc2a64e2c96`. This is harness regression evidence, not host acceptance. Record creation used `rtk proxy python3 ci/tools/new-change-record.py create --name haproxy-current-host-fixtures --base-revision 1b4e1dc041a9080cd84cd8c70ba053cd77c3fa3f --date 2026-10-15`.

## Security impact

No production security control changes. Physical-path admission, source identity binding, relay shutdown and malformed frame handling remain fail closed at their tested harness layer. Fixtures do not authorize missing sink, timeout, native file API or host-fault evidence to pass.

## Runtime evidence

No new host execution or lifecycle PASS is claimed by this fixture/remediation change. The 80 native and 49 companion fixtures are capture-ready preparations only. Independent integrated builds, native engine mappings, physical sink logs, wire/client/backend measurements and root qualification remain required. Historical results are unchanged.

## Known limitations

Original requirements without executable source-bound contracts remain explicit gaps. The complete 278-ID snapshot is immutable, including unresolved original expectations. Capture readiness is not completion of an oracle, transport check or lifecycle.

## Remaining risks

Actual host behavior after the product rebuild and all remaining evidence gaps require separate execution. The Sonar server analysis reports 41 baseline findings; it has not been rerun for these local changes, so no new server Quality Gate or issue-resolution claim is made.

## Checks not run and rationale

Fresh private host acceptance and final server Sonar analysis are not part of this local fixture validation. The Root CPython 3.14.7 result is separate receipt-backed evidence, not inferred from worker results.

## Final diff and review status

This record describes harness/test/fixture preparation and local remediation only. No final I12 acceptance, all-green Sonar result or delivery/merge outcome is asserted. The English and German records preserve the same scope, counts and limitations.
