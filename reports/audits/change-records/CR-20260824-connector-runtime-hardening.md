# Change Record

**Language:** English | [Deutsch](CR-20260824-connector-runtime-hardening.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260824-connector-runtime-hardening |
| Date (UTC) | 2026-08-24 |
| Base revision | 5d71be74369123257851eb5ec612d7523a6b061d |
| Repository boundary | Parent only; Framework, MRTS, Gitlink, CI, branch rules, rulesets, and required checks unchanged |
| Evidence | Earlier retained runtime evidence plus final local validation `/root/git/ModSecurity-conector/.codex/runs/20260825T161923Z-connector-runtime-hardening-final/evidence/final-local-validation.md` (SHA-256 `61b9abdb709104e538e1d56d06afd374b459b0e5d06b5b2735d2863262f10765`) and sealed security review report (SHA-256 `974516d3bb25d102892091e9492b03935acbe1e99bf0d8c62ba07a0637876b42`) |
| Delivery status | Draft PR [#346](https://github.com/Easton97-Jens/ModSecurity-conector/pull/346) open; initial head `aef7ebfad18d90b6efda2e3cc4ad4a0816e9ae7c`; no merge performed or authorized |

## Motivation and problem statement

The task required one explicit failure, availability, and cleanup model for Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy `ext_authz`, Envoy `ext_proc`, Traefik `forwardAuth`, Traefik Native UDS, lighttpd Stock, and lighttpd Patched. A malformed or unavailable engine, peer, backend, client, stream, body, or handshake must not silently terminate a long-lived connector, permanently block later work, retain unbounded resources, or leave processes, ports, UDS files, streams, or transaction state behind.

## Acceptance criteria

- Direct libmodsecurity C API calls treat exactly `1` as success and fail closed on `0` or negative returns in the covered Apache, NGINX, HAProxy, and shared runtime paths.
- HAProxy SPOE/SPOP writes are signal-safe and evaluated; peer reset/EPIPE, incomplete or slow HELLO, parallel peers, follow-up HELLO, and Allow/Block controls have bounded, isolated outcomes. A lost stateful response transaction is an explicit closed `deny`/`503`, never a silent `pass`/`200`.
- HAProxy SPOP rejects a positive unsupported `response-body-timeout` rather than claiming an unenforced stream deadline; self-test metadata is atomically invocation-owned and cleaned without altering caller-owned paths.
- HAProxy SPOP rejects every response-phase activation before production startup until an owner-preserving bounded P3/P4 bridge exists; request-only configuration remains the legitimate control.
- Common HTTP authorization for Envoy `ext_authz` and Traefik `forwardAuth` bounds worker admission, survives malformed-peer close, and permits subsequent Allow and Block requests.
- Envoy `ext_proc` separates engine timeout from stream idle timeout, defines activity per complete request, bounds concurrent streams, propagates cancellation, and releases state.
- Traefik Native UDS bounds worker/socket tracking, applies a separate monotonic 30-second peer-output write deadline, handles reset and shutdown, and uses a defined controlled restart path if an uninterruptible engine worker cannot drain.
- lighttpd Stock and Patched compile and pass baseline, Block, event, and listener/cleanup smokes; the Stock ABI records only `native-lighttpd-plugin` and the patched ABI only `patched-native-lighttpd`.
- Patched lighttpd advances the response-hook record by `sizeof(*plfd)`; benign/P2-marker request TCP RSTs survive, and only the exact raw disruptive request-body-limit signature maps `403` to `413`.
- No CI workflow, branch rule, ruleset, required check, Framework source, MRTS source, or Parent gitlink is changed.

## Implementation decision and rationale

- Malformed, incomplete, timed-out, reset, or cancelled engine/protocol state fails closed where authorization is undecidable; a legitimate follow-up request is admitted after peer-local cleanup. Host action, status, event, cleanup, and operator impact are recorded in the paired runtime policy and retained evidence.
- Signal safety is local to each socket write (`MSG_NOSIGNAL`, with platform fallback where available); no global SIGPIPE ignore is used.
- Admission and shutdown are bounded. Cleanup is idempotent or ownership-isolated; state is not freed while an uninterruptible worker still owns it.
- The project-supplied HAProxy closed-default SPOE configuration omits `option continue-on-error`: that HAProxy opt-in is incompatible with `fail-mode=closed` because an agent failure can otherwise become an Allow. An admission close without an ACK is a closed SPOP transport failure; a failure ACK maps to `503`. The exact native-HAProxy client status for an unacknowledged admission close remains `NOT_EXECUTED`, while peer-local admission/HELLO isolation is retained.
- A response-side SPOP cache correlation miss remains separately fail-closed in the source-level response path, even when an operator selected ordinary engine-error `fail-mode=open`: bounded eviction can remain an availability limit, but a later response NOTIFY emits `deny`/`503`, `disruptive=1`, and `stateful_response_transaction_missing_closed` rather than silently skipping response enforcement. The production boundary rejects response-phase startup, and its peer-local guard rejects an incompatible response NOTIFY before cache processing with `response_phase_disabled_closed`.
- The selected SPOP response path has no response-body stream. Positive `response-body-timeout` is therefore rejected at parsing with exit `2`; zero/default and per-frame `spoe-timeout` remain separate. PID, ready, and port metadata use `O_CREAT|O_EXCL` (and `O_NOFOLLOW` where available), then ownership-masked cleanup, so a collision cannot overwrite or unlink a caller-owned path.
- The production SPOP boundary rejects `response-body-limit > 0`, `enable-response-headers`, and `response-phases` before listener or worker startup because the current request-side protocol has no bounded owner-preserving P3/P4 EOS bridge. This is a closed configuration failure, never an implied partial response-enforcement mode; a valid request-only start remains supported.
- `ext_proc` activity resets only after a complete processing request and its response/engine work. The general engine timeout is not a stream-idle timeout.
- The ext_proc follow-up fixture asserts `pendingReceives == 0` after the idle handler returns; mutex and forced-stop waits are deadline-bounded. An already-running uninterruptible native C destructor uses a controlled nonzero restart path, not an in-process cancellation claim.
- Native UDS RESULT writes use one `CLOCK_MONOTONIC` peer deadline with `poll(POLLOUT)` and nonblocking `MSG_NOSIGNAL | MSG_DONTWAIT`. Expiry closes only that peer and releases its worker; it is not an engine-operation or receive timeout.
- Stock lighttpd response-start helpers are compiled outside the patched-host ABI guard so both host variants use the same cleanup-safe path.
- lighttpd raw event identity is chosen at that same compile-time ABI boundary: stock headers select `native-lighttpd-plugin`, while streaming-hook headers select `patched-native-lighttpd`. A Stock run can therefore not masquerade as patched-host evidence.
- Patched lighttpd uses `resp_fn_step += sizeof(*plfd)`, not a one-byte increment. The Common Runtime changes only the exact raw disruptive request-body intervention (`403`, no redirect, exact body-limit log) to `413`; ordinary same-wording `403` and `451` rules retain their explicit status.

## Security impact

The changes harden trust-boundary transitions between hosts, clients, peers, engines, sockets, protocol streams, and transaction state. They reduce crash, deadlock, resource-exhaustion, request-stall, stale-listener, and ambiguous-authorization outcomes. Allow and Block controls remain available and were rechecked after malformed-peer and timeout/cancel cases. This is local source, service, connector, and host-smoke evidence, not proof of every production host, HTTP/2/HTTP/3, reload, or external deployment combination.

## Changed files

- `common/runtime/msconnector_runtime.c` — exact libmodsecurity transaction success checks and narrow request-body-limit `413` normalization.
- `common/runtime/http_authorization_service.c` — signal-safe writes, bounded worker admission, and bounded shutdown ownership.
- Apache: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c` — fail-closed transaction and response/body checks.
- NGINX: `connectors/nginx/src/ngx_http_modsecurity_access.c`, `ngx_http_modsecurity_body_filter.c`, `ngx_http_modsecurity_header_filter.c`, `ngx_http_modsecurity_module.c` — exact C API result handling.
- HAProxy: `connectors/haproxy/src/haproxy_modsecurity_binding.c`, `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh`, `examples/haproxy/compatibility-spoe/modsecurity-agent.conf` — HTX checks, isolated signal-safe SPOE/SPOP handling, a request-only response-phase guard control, retained source-level cache-miss fail-closed behavior, parser rejection of an unsupported response-body timeout, and ownership-safe self-test metadata cleanup.
- Envoy: `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`, `connectors/envoy/ext_proc/internal/processor/config.go`, `processor.go`, `processor_test.go`, `connectors/envoy/config/envoy-ext-proc-service.json`, `examples/envoy/minimal/envoy-ext-proc-service.json`, `examples/envoy/safe/envoy-ext-proc-service.json` — idle/admission/cancellation/shutdown controls and config.
- Traefik: `connectors/traefik/src/traefik_engine_service.c`, `connectors/traefik/build/test-engine-service-runtime.sh` — bounded Native UDS drain, controlled restart, and unread-peer write-deadline runtime regression.
- lighttpd: `connectors/lighttpd/module/mod_msconnector.c`, `connectors/lighttpd/patches/0001-lighttpd-msconnector-stream-hooks.patch`, `connectors/lighttpd/tests/test_patched_host_contract.py` — Stock/Patched helper scope, ABI-correct raw event identity, exact callback-stride correction, and regression.
- Regression tests: `tests/test_apache_fail_closed.py`, `connectors/nginx/tests/test_fail_closed_contract.py`, `tests/test_native_api_fail_closed_contract.py`, `tests/test_haproxy_spop_peer_isolation_contract.py`, `tests/test_haproxy_spop_transaction_cache_contract.py`, `tests/test_haproxy_spop_response_timeout_contract.py`, `tests/test_haproxy_spop_selftest_cleanup_contract.py`, `tests/test_modsecurity_request_body_limit_status_contract.py`, `tests/test_http_authorization_service_worker_contract.py`, `tests/test_http_authorization_service_runtime.py`, `tests/test_traefik_engine_service_shutdown_contract.py`, `tests/test_traefik_native_local_plugin.py`.
- No CI, Framework/MRTS, Gitlink, dependency, branch-rule, ruleset, or required-check file is part of this record.

### HTX append remediation delta

- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c` now returns `-1` after transaction-local request or response native append failure; only a successfully inspected slice returns its positive length.
- `tests/test_haproxy_htx_payload_fail_closed_contract.py` adds the request/response callback contract.
- The retained HAProxy `3.2.22` host run reproduced the original request and response forwarding (`200`), then observed patched request `400` with zero backend dispatches and patched response affected-stream close (`000`, `curl_exit=52`). Both cases served a legitimate same-process Allow control and released their exact task-owned listeners.
- This is FND-PARENT-0946: a local security fix with HTTP/1.1 evidence, not a verified H2/H3, reload, full-FD, or exact-delivered-head result.
- Actual checks: `python3 -m unittest tests/test_haproxy_htx_payload_fail_closed_contract.py` passed (2 tests); the focused 22-test HAProxy helper/binding suite passed; rebuilding the overlay with `connectors/haproxy/htx-overlay/build-overlay.sh` against retained HAProxy `3.2.22` passed. Retained run `haproxy-htx-append-failure-20260825T131500Z` has SHA-256 `12e4d30c68ff46f45f2f8481d810eb53099f6512f384520e3942fadb0434da9c`.

## Tests and actual results
### Final runtime hardening delta — 2026-08-25

- Envoy `ext_proc` now treats a timed-out native transaction cleanup as terminal: it stops accepting reusable work, reports one fatal error to the process owner, forces bounded gRPC stop, and exits nonzero for supervisor restart. This is separate from the documented stream-idle timeout.
- HAProxy SPOP now rejects a typed peer value that would not fit with its NUL terminator, rather than silently truncating it. Header count/name/value/total sizes are bounded before allocation; `spoe-timeout`, `worker-count`, and `max-transactions` use strict decimal ranges `1..60000`, `1..64`, and `1..4096`, with at most `65536` aggregate transaction slots.
- Apache and lighttpd harness additions make process/listener cleanup identity-bound and fail closed on uncertain ownership; HTX payload append errors now stop the affected stream rather than claiming a positive successful append.
- Focused current validation passed 237 tests with 2 expected skips, `make -C connectors/haproxy check-htx-overlay`, and `git diff --check`. The final sealed security-diff review contains zero reportable findings and partial coverage.
- The Draft PR is intentionally partial: full native 17-vector-by-10-connector host coverage, exact uninterruptible CGo-host reproduction, and the two named proof gaps remain open. CI was not changed or run.


The exact retained commands and observed results are in the evidence file named above.

- Apache contracts: 4 passed; the current source module built against Apache 2.4.66/APXS and earlier isolated real-host controls returned Allow `200`, P1 Block `403`, and P2 Block `403`. A new bounded V7 diagnostic returned proxy `502`, but its inline follow-up backend was malformed and cleanup was not attributable: task ports `29471/29472` remain listening without a visible PID after the exact stop attempt. No unsafe signal was issued. Apache V7/V16/V17 therefore remain `BLOCKED_ENVIRONMENT` under FND-HOST-0007; the optional synchronized `engine-limit` and `client-abort` fixtures were separately blocked before upstream address publication.
- NGINX contracts: 13 passed, including the zero-return-to-500 fail-closed regression. The current source built against pinned NGINX 1.31.4. A bounded native V7 host observed a controlled upstream that sent 21 of declared 128 bytes; NGINX logged the early close, the client observed committed `200` then `curl_exit=18` with 107 bytes missing, NGINX survived, and same-host Allow/Block/Allow returned `200 -> 403 -> 200`. A separate bounded V6/V10 upload probe sent 5 of declared 100 bytes then FIN or TCP RST; the client had already closed, NGINX logged `400`, the host survived, the same process returned `200 -> 403 -> 200`, and its exact PID/port `29583` plus temporary directories were removed. A fresh direct native-host parallel run served 16 concurrent requests (8 Allow `200`, 8 Block `403`) in one still-live process, then returned `200 -> 403 -> 200`; its exact PID, port `29671`, and PID file were absent after bounded cleanup. The RST upload shape is not promoted as an independent V9 proof. Bounded cleanup removed the V7 PIDs/ports `29371/29372`. The direct-mode result does not cover worker identity; the canonical sandbox worker harness remains blocked by `chown(..., nobody)` `EINVAL`; separate port `29183` was released and a later Parent read-only recheck found neither `29182` nor `29183` listening.
- Direct C API contracts: 3 passed.
- HAProxy SPOP source contracts: 13 focused checks passed, including response-body-timeout rejection, peer-local response-phase rejection, and metadata ownership/collision controls. The current production binary rejected `--response-body-timeout 25` with exit `2`; its self-test emitted `metadata_cleanup: PASS` and left no metadata. The current request-only `run_haproxy_spop_cache_miss.sh` control with `max-transactions=1` observed response-phase `deny`/`503`/`response_phase_disabled_closed`, real rule Block `403`, fresh Allow `200`, agent cleanup, and an absent dynamic listener. The older cache-miss `stateful_response_transaction_missing_closed` path remains source-level evidence. GCC/Clang runtime self-tests, reset/EPIPE, peer isolation, saturated-peer immediate close, HELLO deadline, and follow-up controls also passed.
- HAProxy HTX overlay checks and helper suite (11 tests) passed. A fresh bounded native-host P1--P4 run returned Allow `200`, P1 precommit denials `403` and `429`, P2 client-body denial `403` before upstream dispatch, P3 response-header denial `403` after one upstream request, and P4 late committed-response safe-log-only `200` with the first client byte before upstream EOS. It recorded `processes_stopped=yes`, no task-owned frontend/UDS listener after cleanup, and `capability_promotion=not_permitted`; it is evidence for those controls only, not a full 17-vector or response-bridge acceptance.
- Envoy builds/configs passed. `ext_authz` runtime passed malformed-peer recovery, `200` Allow, `403` Block, bounded exit, and listener cleanup.
- Envoy `ext_proc` Go unit and `-race` suites plus the tagged native CGo test passed, including timeout, cancellation, shutdown, admission release, follow-up controls, and `TestCommonRuntimeEngineCloseHonorsShutdownContext`; all three config checks passed.
- Traefik `forwardAuth` config/runtime passed malformed-peer recovery, `200` Allow, `403` Block, exit, and port cleanup.
- Traefik Native UDS GCC, Clang, and ASan/UBSan passed protocol, reset, follow-up, ownership, and cleanup with no sanitizer diagnostic. The current native service regression filled all 64 workers with non-reading UDS peers, observed no early follow-up service, then a fresh request at 31.0 seconds and complete socket/process cleanup; the same case passed under ASan/UBSan.
- lighttpd focused contracts passed (44 tests, 2 expected skips). The exact patched 1.4.85 normal and ASan/UBSan hosts survived benign/P2-marker partial TCP RSTs with no synthetic P2 abort or sanitizer diagnostic; empty/32-byte Allow `200`, ordinary P2 `403`, same-wording ordinary `403`/`451`, 33/64-byte limit `413`, independent follow-up, event evidence, PID, and listener cleanup passed.
- Current dual-ABI lighttpd validation passed 37 focused contracts (2 expected namespace skips), rebuilt the same module with C17 against retained Stock and Patched 1.4.85 headers, and observed `200` Allow, `403` Block, then `200` same-process Allow for both variants. Stock raw events contain only `native-lighttpd-plugin`, Patched raw events only `patched-native-lighttpd`, and both task-owned listener/PID checks were clean.
- Bounded lighttpd backend-close receipts declared 64 bytes, sent only `short` (5 bytes), and yielded a five-second frontend timeout. The later controls and final PID/listener absence remain retained, but neither variant observed frontend EOF/defined error, a peer-error event, or immediate stream/FD/transaction cleanup before the explicit host stop. Neither Stock nor Patched V7/V11 is promoted. The current ABI-correct Stock repeat verifies module `d1429392...` and `native-lighttpd-plugin`, but has the same closure-evidence gap. The original receipt is retained at `/var/tmp/codex/ModSecurity-conector/runs/20260824T120000Z-connector-runtime-hardening/runtime-continuation/lighttpd-backend-close-20260824T230000Z/validation.md` (SHA-256 `ef460a10515fbdb6ff994f0d57ffb2f13c39d4eae1debd6e39eca6088bcc4a4d`); the independent correction is retained at `/var/tmp/codex/ModSecurity-conector/runs/20260824T120000Z-connector-runtime-hardening/runtime-continuation/lighttpd-stock-current-close-20260824T233000Z/closure-review-addendum.md` (SHA-256 `d43e72ab55fca997c9b840c01de4cd90aa9f0d300273138bdde7776e1d84e10d`). FND-PARENT-0311 tracks the required raw upstream/frontend closure harness.
- A separate current Stock raw V7/V11 lifecycle fixture committed HTTP `200` and a declared 64-byte body, sent five body bytes, then closed; the bounded host/transport harness and its cleanup receipts passed. It is deliberately limited evidence: it does not claim a typed Stock connector event, direct transaction-state release, a complete FD/leak audit, or full V7/V11 acceptance. Patched-lighttpd's corresponding complete frontend-close/transaction-cleanup proof remains open.
- Evidence was retained and hashed as stated in Identity.

## Commands executed

The retained evidence records the exact commands and results. The principal
local checks were the connector contract suites, HAProxy SPOE/SPOP runtime
self-tests, Envoy `go test ./...` and `go test -race ./...`, the tagged Envoy
native test, Traefik Native UDS GCC/Clang/ASan/UBSan runs, fresh lighttpd
Stock/Patched smokes, `make check-doc-links`, and `make check-bilingual-docs`.
The reproducible SPOP cache control is
`BUILD_ROOT=<task-owned-build> SPOA_BIN=<current-agent> RUNTIME_ROOT=<task-owned-runtime> connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh`.

## Runtime evidence

The retained evidence covers engine-start availability, in-transaction failure, timeout, invalid/incomplete peer input, client/peer reset, incomplete HELLO and body/stream boundaries where the local harness provides them, parallel requests/streams, size/admission bounds, cancellation, shutdown, follow-up controls, and cleanup. SPOP logs record reset `errno=104`, EPIPE `errno=32`, explicit unsupported-timeout rejection, atomic metadata cleanup, and the current cache-miss `503` followed by real Block and Allow controls. The bounded current HAProxy HTX host run records P1 `403`/`429`, P2 pre-upstream `403`, P3 `403`, and committed P4 safe-log-only `200` without full-response buffering; it is explicitly `native_host_runtime_nonpromoted`. The bounded NGINX V7 evidence retains its early-close log, committed-status transport failure, same-host `200 -> 403 -> 200`, and PID/port cleanup; its V6/V10 receipt retains incomplete FIN/RST uploads, server-side `400`, process survival, follow-ups, and port/temp-directory cleanup without an independent V9 claim. A fresh direct-mode NGINX run additionally retains 16 concurrent Allow/Block results, same-process controls, and PID/port cleanup, but not worker-identity semantics. Apache retains earlier Allow/Block controls and a diagnostic V7 `502`, but its V7 follow-up/cleanup is deliberately blocked by non-attributable listeners rather than promoted. Patched lighttpd retains normal and ASan/UBSan partial-RST, exact `413` status, event, PID, and listener evidence. Both bounded lighttpd backend-close receipts remain partial/nonpromoted because they timed out rather than establishing frontend closure and immediate cleanup before host stop; FND-PARENT-0311 retains the exact gap. The Native UDS test asserts a legitimate subsequent request and absence of the assigned UDS listener after both reset and 64-peer send-deadline exhaustion.

The separate current Stock raw V7/V11 lifecycle fixture observed a truncated
64-byte upstream body after five bytes and bounded host/transport cleanup. It
does not supersede FND-PARENT-0311's complete frontend/transaction-release
requirement, and it does not claim a typed Stock event or full leak audit.

## Checks not run and rationale

- The bounded HAProxy HTX P1--P4 native-host control run is available, but native V7 early-close/RST, V6/V9 transport-fault, V12--V15 lifecycle/limit/concurrency, and full 17-vector acceptance remain unexecuted. NGINX has the bounded V7 Native-Host result above but its canonical worker harness remains sandbox-blocked. Apache has only earlier scoped controls; its newest V7 run is blocked until listener ownership and cleanup are observable.
- The bounded current Stock raw V7/V11 fixture ran, but is host/transport-only and does not prove a typed connector event, direct transaction release, or a full FD/leak audit. Patched-lighttpd V7/V11 still needs raw upstream-close, frontend EOF/defined-error, immediate stream/FD/transaction cleanup, and same-host post-fault controls before promotion.
- No native Envoy proxy or Traefik proxy host was started; connector/agent binaries and common services were exercised.
- A deliberately hung libmodsecurity engine was not simulated unsafely; bounded shutdown and controlled nonzero restart were checked by source/tests.
- Default Traefik `check-config` tried to create historical global `/var/tmp/ModSecurity-conector-verified/logs` and was sandbox-blocked. A task-owned config and `event_path` passed; no global path was created.
- Full native-host, HTTP/2/HTTP/3, reload, cross-connector leak, and ThreadSanitizer matrices remain unexecuted. CI was intentionally not run or changed.

## Known limitations

Native host integration and production-specific reload, TLS, HTTP/2, HTTP/3, and long-duration scheduling remain environment-dependent. The controlled restart branch is an explicit availability decision for an uninterruptible engine worker; it does not claim such a worker can be recovered without process restart. The retained evidence is strong local evidence, not complete hosted-matrix proof.

## Remaining risks

Operators still need to validate connector-specific limits, timeouts, TLS/UDS permissions, reload sequencing, and monitoring in native host versions. Unavailable native hosts and unexecuted matrices remain release-readiness limitations until independently reproduced. No CI or governance protection was weakened.

## Final diff and review status

Implementation evidence is retained, scoped to Parent, and paired with this bilingual Change Record. The NGINX zero-return, HAProxy SPOP saturated-admission/response-cache/timeout/metadata, Traefik Native UDS unread-peer, Envoy `ext_proc` native-shutdown, Common Runtime `413`, and patched-lighttpd callback-stride remediations are locally fixed; their finding records remain open or fixed rather than closed wherever native host/FD-vector evidence is still incomplete. Draft PR [#346](https://github.com/Easton97-Jens/ModSecurity-conector/pull/346) is open after the separate scoped diff review and delivery-policy checks; it neither performs nor authorizes a merge or finding closure.
