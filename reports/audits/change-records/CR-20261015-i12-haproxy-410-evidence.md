# Change Record: CR-20261015-i12-haproxy-410-evidence

**Language:** English | [Deutsch](CR-20261015-i12-haproxy-410-evidence.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-haproxy-410-evidence |
| Date (UTC) | 2026-10-15 |
| Base revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation and problem statement

Existing #410 evidence qualifies nine HAProxy lifecycle cases. The three separate route inventories contain 112/94/72 required IDs and 48/44/32 original oracles; 43/41/31 original oracles remain open at the starting ledger. This change improves independently measured coverage without converting HTTP-only observations into lifecycle PASS.

## Acceptance criteria

Retain separate native HTX, SPOP request and companion verdicts; bind changed original-oracle predicates to source and fixture behavior; retain host/native/config/frame/client/backend/sink/finish/free evidence, exact argv, exits and hashes. Keep product, central matrix, shared captures, generators and other connectors unchanged. Deliver an authorized draft against `work/pr382-i12-host-evidence-20261011`; unresolved cases remain explicitly open.

## Implementation decision and rationale

Add task-specific HAProxy harnesses and fixtures while using the existing three immutable capture variants in disposable copies. Separate observation assertions from lifecycle qualification and source-oracle resolution. Correct only the stale HAProxy-specific SPOP test caller contract. Distinguish logical commit from positive client transport; preserve native disruptive outcomes even when Safe mode sends the original response.

## Changed files

- `connectors/haproxy/harness/i12_native_cases.py`
- `connectors/haproxy/harness/i12_native_observe.py`
- `connectors/haproxy/harness/i12_spop_host.py`
- `connectors/haproxy/harness/i12_spop_sink_capture.py`
- `connectors/haproxy/harness/i12_spop_wire.py`
- `connectors/haproxy/harness/i12_companion_host.py`
- `tests/test_haproxy_i12_native_cases.py`
- `tests/test_haproxy_i12_spop_samples.py`
- `tests/test_haproxy_i12_spop_wire.py`
- `tests/test_haproxy_i12_companion_host.py`
- `tests/haproxy_spop_request_target_test.c`
- `docs/pr-410-i12-haproxy-20261015.md`
- `docs/pr-410-i12-haproxy-20261015.de.md`
- `reports/testing/i12-haproxy-410-20261015.json`
- `reports/audits/change-records/CR-20261015-i12-haproxy-410-evidence.md`
- `reports/audits/change-records/CR-20261015-i12-haproxy-410-evidence.de.md`

## Commands executed

All shell commands use RTK. Fresh receipt-backed commands include `rtk proxy make check-haproxy-c17`, `rtk proxy make check-haproxy-htx-overlay`, `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify`, and capture mutation unittests. Full argv, build-root/Python parameters, stdout/stderr hashes and exits are retained under `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-410-20261015/verification/summary.json`. Native and host drivers retain additional exact argv and exits in their own receipts. The Change Record pair was created with `rtk proxy python3 ci/tools/new-change-record.py create --name i12-haproxy-410-evidence --base-revision f27eb59b53beff6f65384fc2e5037881a3052c01 --date 2026-10-15`.

Change Record archive structure and both EN/DE structural parity checks pass. `rtk git diff --check` passes. `rtk make check-bilingual-docs` and `rtk make check-doc-links` fail on absent Framework-submodule link targets; the task JSON links now resolve.

## Security impact

No production security control changes. Tests examine fail-closed bounded SPOP samples, corrupt framing, sink failures, transaction cleanup and response authorization ordering. Unknown/chunked framing and unsupported HTTP/2 mappings remain outside full-inspection qualification. A green request ACK cannot establish companion security. Product discrepancies are retained for separate #382 follow-up.

## Runtime evidence

Fresh host builds use HAProxy `3.2.25` and libModSecurity `3.0.14`. Task raw root: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-410-20261015`. [Task report](../../../docs/pr-410-i12-haproxy-20261015.md) explains each route and the observation limits; [JSON evidence](../../testing/i12-haproxy-410-20261015.json) carries reviewed per-run dispositions. Native request-only SPOP completion returns `-3` with phase mask `3`, yielding ACK/client `503` and zero backend requests; a separate combined request reaches mask `15`, finish `0`, ACK `200` and one backend request. The native response Reject limit observes disruptive `403` while Safe client transport delivers `200` and 27 bytes. Neither discrepancy is rewritten as a successful full lifecycle.

The real HTTP/2 Content-Length sample sends `http_version=2.0` and receives ACK `200`/one backend request, but native audit records `HTTP/1.1`. The request-only finish and HTTP-version discrepancies are reported in [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194176740). A separate companion P3-deny host run records `1→2→8→7`, client `403`, no COMMIT/BODY/EOS and one native free per transaction; the independent Safe run records `1→2→5→3→4→8→7`, `log_only`, client `200` and 33 body bytes. Expired correlation returns CLAIM→RESULT error/client `503`; two idempotent Common cleanup calls with one native cleanup do not prove double free.

The accepted Strict branch attempts abort after P4 deny `403`, yet the measured buffered 33-byte response reaches the client completely as HTTP `200` with TLS close. Source trace `companion/strict-transport-cause.json` confirms asynchronous `stream_shutdown` plus positive `http_end` permits queued output before task shutdown; the subsequent positive `SSL_write` is 210 bytes with client SHA-256 `9b6e9773ad3ed4e42cfc54373d5769e9d393f634124bf5667b54be2cc8ab8176`. This scoped product mismatch needs #382 correction. The malformed NOTIFY initial no-ACK expectation was a `HARNESS_DEFECT`: actual ACK `400`/`block=true`, client `503`, backend zero are preserved and corrected only in source-bound offline evaluation without fresh host credit. Phase-four diagnostics and file-named payload fixtures do not establish catalog-ID or native file-API coverage.

Root review accepts 22 fresh native runs including two baseline retakes: 20 new qualified IDs, current native lifecycle `25/112`, 87 unqualified required IDs, and `25/48` original oracles resolved with 23 open. SPOP stays at lifecycle `3/94`, 91 unqualified required IDs; four source-only oracle resolutions yield `7/44` resolved and 37 open without new lifecycle credit. The independent V7 `NEED-client-response-bytes` companion run passes unchanged original-oracle and lifecycle-ledger gates: current companion lifecycle `2/72`, 70 unqualified required IDs and 30/32 original oracles open. Overall results are 30/278 full lifecycle PASS (+21), 248 unqualified required IDs, and 34/124 original oracles resolved with 90 open (baseline 115 open). The 23 fresh qualified attempts are 22 native runs including two baseline retakes plus one independent companion run with distinct nonces; no request is tripled. SPOP has 13 valid private host runs; the final mismatch retry exits controller `0` with ACK/client `503`, zero backend requests and zero native allocations. Read-only storage finalization passes with approximately 0.475 GiB retained and 184 GiB free. The 25 new HAProxy unittests pass.

V8 parallel controller exit `0` does not qualify the case: 16 clients produce four complete `200`, one truncated `200`, two `503` and nine `502`. Zero live mappings/pending calls and eight native frees support only the cleanup observation. Failed V4/controller-`77` attempts remain retained alongside later retries. Native snapshot v2 strengthens explicit 16-byte `ProcessPartial` scope while preserving old immutable artifacts. The task-private controller changes only the RUN-root literal. The Strict product finding is reported separately in [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194270431).

## Known limitations

The broad existing suite executes 256 tests: two stale workflow upload-pin failures, one Unix-socket-path error and 12 skips. The socket case passes with a shorter task-owned temporary path. The stale workflow pins remain unchanged. All 31 plain pytest-style functions pass via a minimal adapter, including ASAN/UBSAN paths after correcting the stale SPOP test caller. The ordinary pytest command fails because pytest is absent; no dependency is installed. C17, HTX overlay, capture registry and mutation checks pass. Complete qualification is limited to evidence actually reviewed.

## Remaining risks

Unresolved original oracles, unsupported H2/framing, missing physical CommonAllow sink evidence and unqualified companion ordering remain open. Native audit/debug output is not a substitute for a missing CommonAllow sink event. No claim of exhaustive 278-ID coverage or three independent runs from a shared request is made.

## Checks not run and rationale

Pytest itself was not run successfully because it is not installed; a separate minimal adapter executed the 31 functions. No cross-connector, Framework or MRTS changes/tests are part of this scope. Hosted final-head CI/review/Sonar results and draft publication must be recorded from actual delivery observations; they are not inferred from local checks.

## Final diff and review status

Local documentation preserves bilingual scope, results and limits. The requested branch is `codex/i12-haproxy-410-20261015`, based on `f27eb59b53beff6f65384fc2e5037881a3052c01`; the requested draft title is `test(i12/haproxy): complete HTX SPOP and companion lifecycle evidence`. This record does not assert a published PR number, completed hosted checks, merge, force-push or product fix. Final qualification is recorded above; authorized draft delivery and hosted review remain separate observed lifecycle facts.
