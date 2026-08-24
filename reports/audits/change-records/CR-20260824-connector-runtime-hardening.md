# Change Record

**Language:** English | [Deutsch](CR-20260824-connector-runtime-hardening.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260824-connector-runtime-hardening |
| Date (UTC) | 2026-08-24 |
| Base revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Repository boundary | Parent only; Framework, MRTS, Gitlink, CI, branch rules, rulesets, and required checks unchanged |
| Evidence | `runs/20260824T120000Z-connector-runtime-hardening/evidence/runtime-hardening-validation.md`; SHA-256 `5fc2c8d6f5f2bdd36bd757fd044ab6f0f8d5f8f0e976a65ac46153ce3975ef63` |
| Delivery status | No commit, push, PR, or merge performed by this record |

## Motivation and problem statement

The task required one explicit failure, availability, and cleanup model for Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy `ext_authz`, Envoy `ext_proc`, Traefik `forwardAuth`, Traefik Native UDS, lighttpd Stock, and lighttpd Patched. A malformed or unavailable engine, peer, backend, client, stream, body, or handshake must not silently terminate a long-lived connector, permanently block later work, retain unbounded resources, or leave processes, ports, UDS files, streams, or transaction state behind.

## Acceptance criteria

- Direct libmodsecurity C API calls treat exactly `1` as success and fail closed on `0` or negative returns in the covered Apache, NGINX, HAProxy, and shared runtime paths.
- HAProxy SPOE/SPOP writes are signal-safe and evaluated; peer reset/EPIPE, incomplete or slow HELLO, parallel peers, follow-up HELLO, and Allow/Block controls have bounded, isolated outcomes. A lost stateful response transaction is an explicit closed `deny`/`503`, never a silent `pass`/`200`.
- Common HTTP authorization for Envoy `ext_authz` and Traefik `forwardAuth` bounds worker admission, survives malformed-peer close, and permits subsequent Allow and Block requests.
- Envoy `ext_proc` separates engine timeout from stream idle timeout, defines activity per complete request, bounds concurrent streams, propagates cancellation, and releases state.
- Traefik Native UDS bounds worker/socket tracking, applies a separate monotonic 30-second peer-output write deadline, handles reset and shutdown, and uses a defined controlled restart path if an uninterruptible engine worker cannot drain.
- lighttpd Stock and Patched compile and pass baseline, Block, event, and listener/cleanup smokes.
- No CI workflow, branch rule, ruleset, required check, Framework source, MRTS source, or Parent gitlink is changed.

## Implementation decision and rationale

- Malformed, incomplete, timed-out, reset, or cancelled engine/protocol state fails closed where authorization is undecidable; a legitimate follow-up request is admitted after peer-local cleanup. Host action, status, event, cleanup, and operator impact are recorded in the paired runtime policy and retained evidence.
- Signal safety is local to each socket write (`MSG_NOSIGNAL`, with platform fallback where available); no global SIGPIPE ignore is used.
- Admission and shutdown are bounded. Cleanup is idempotent or ownership-isolated; state is not freed while an uninterruptible worker still owns it.
- The project-supplied HAProxy closed-default SPOE configuration omits `option continue-on-error`: that HAProxy opt-in is incompatible with `fail-mode=closed` because an agent failure can otherwise become an Allow. An admission close without an ACK is a closed SPOP transport failure; a failure ACK maps to `503`. The exact native-HAProxy client status for an unacknowledged admission close remains `NOT_EXECUTED`, while peer-local admission/HELLO isolation is retained.
- A response-side SPOP cache correlation miss is separately fail-closed even when an operator selected ordinary engine-error `fail-mode=open`: bounded eviction can remain an availability limit, but a later response NOTIFY now emits `deny`/`503`, `disruptive=1`, and `stateful_response_transaction_missing_closed` rather than silently skipping response enforcement.
- `ext_proc` activity resets only after a complete processing request and its response/engine work. The general engine timeout is not a stream-idle timeout.
- The ext_proc follow-up fixture asserts `pendingReceives == 0` after the idle handler returns; mutex and forced-stop waits are deadline-bounded. An already-running uninterruptible native C destructor uses a controlled nonzero restart path, not an in-process cancellation claim.
- Native UDS RESULT writes use one `CLOCK_MONOTONIC` peer deadline with `poll(POLLOUT)` and nonblocking `MSG_NOSIGNAL | MSG_DONTWAIT`. Expiry closes only that peer and releases its worker; it is not an engine-operation or receive timeout.
- Stock lighttpd response-start helpers are compiled outside the patched-host ABI guard so both host variants use the same cleanup-safe path.

## Security impact

The changes harden trust-boundary transitions between hosts, clients, peers, engines, sockets, protocol streams, and transaction state. They reduce crash, deadlock, resource-exhaustion, request-stall, stale-listener, and ambiguous-authorization outcomes. Allow and Block controls remain available and were rechecked after malformed-peer and timeout/cancel cases. This is local source, service, connector, and host-smoke evidence, not proof of every production host, HTTP/2/HTTP/3, reload, or external deployment combination.

## Changed files

- `common/runtime/msconnector_runtime.c` — exact libmodsecurity transaction success checks.
- `common/runtime/http_authorization_service.c` — signal-safe writes, bounded worker admission, and bounded shutdown ownership.
- Apache: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c` — fail-closed transaction and response/body checks.
- NGINX: `connectors/nginx/src/ngx_http_modsecurity_access.c`, `ngx_http_modsecurity_body_filter.c`, `ngx_http_modsecurity_header_filter.c`, `ngx_http_modsecurity_module.c` — exact C API result handling.
- HAProxy: `connectors/haproxy/src/haproxy_modsecurity_binding.c`, `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh`, `examples/haproxy/compatibility-spoe/modsecurity-agent.conf` — HTX checks, isolated signal-safe SPOE/SPOP handling, a reproducible cache-miss control, and closed response-cache correlation loss.
- Envoy: `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`, `connectors/envoy/ext_proc/internal/processor/config.go`, `processor.go`, `processor_test.go`, `connectors/envoy/config/envoy-ext-proc-service.json`, `examples/envoy/minimal/envoy-ext-proc-service.json`, `examples/envoy/safe/envoy-ext-proc-service.json` — idle/admission/cancellation/shutdown controls and config.
- Traefik: `connectors/traefik/src/traefik_engine_service.c`, `connectors/traefik/build/test-engine-service-runtime.sh` — bounded Native UDS drain, controlled restart, and unread-peer write-deadline runtime regression.
- lighttpd: `connectors/lighttpd/module/mod_msconnector.c`, `connectors/lighttpd/tests/test_patched_host_contract.py` — Stock/Patched helper scope and regression.
- Regression tests: `tests/test_apache_fail_closed.py`, `connectors/nginx/tests/test_fail_closed_contract.py`, `tests/test_native_api_fail_closed_contract.py`, `tests/test_haproxy_spop_peer_isolation_contract.py`, `tests/test_haproxy_spop_transaction_cache_contract.py`, `tests/test_http_authorization_service_worker_contract.py`, `tests/test_http_authorization_service_runtime.py`, `tests/test_traefik_engine_service_shutdown_contract.py`, `tests/test_traefik_native_local_plugin.py`.
- No CI, Framework/MRTS, Gitlink, dependency, branch-rule, ruleset, or required-check file is part of this record.

## Tests and actual results

The exact retained commands and observed results are in the evidence file named above.

- Apache contracts: 4 passed; the current source module built against Apache 2.4.66/APXS and isolated real-host cases returned Allow `200`, P1 Block `403`, and P2 Block `403`; task-owned ports and test processes were absent after every case. This is not same-host post-fault follow-up evidence. The optional synchronized `engine-limit` and `client-abort` fixtures were blocked before upstream address publication.
- NGINX contracts: 13 passed, including the zero-return-to-500 fail-closed regression. The current source built against pinned NGINX 1.31.4 and a native host returned Allow `200`, header Block `403`, then Allow `200`; port `29183` was released. The canonical sandbox harness was blocked by `chown(..., nobody)` `EINVAL`; a task-owned listener from that failed attempt was separately ownership-verified and controlled-cleaned.
- Direct C API contracts: 3 passed.
- HAProxy SPOP source contracts: 8 focused checks passed; the current `run_haproxy_spop_cache_miss.sh` production-agent control with `max-transactions=1` observed cache-miss `deny`/`503`/`stateful_response_transaction_missing_closed`, real rule Block `403`, fresh Allow `200`, and agent cleanup. GCC/Clang runtime self-tests, reset/EPIPE, peer isolation, saturated-peer immediate close, HELLO deadline, and follow-up controls also passed.
- HAProxy HTX overlay checks and helper suite (11 tests) passed; native HAProxy host unavailable.
- Envoy builds/configs passed. `ext_authz` runtime passed malformed-peer recovery, `200` Allow, `403` Block, bounded exit, and listener cleanup.
- Envoy `ext_proc` Go unit and `-race` suites plus the tagged native CGo test passed, including timeout, cancellation, shutdown, admission release, follow-up controls, and `TestCommonRuntimeEngineCloseHonorsShutdownContext`; all three config checks passed.
- Traefik `forwardAuth` config/runtime passed malformed-peer recovery, `200` Allow, `403` Block, exit, and port cleanup.
- Traefik Native UDS GCC, Clang, and ASan/UBSan passed protocol, reset, follow-up, ownership, and cleanup with no sanitizer diagnostic. The current native service regression filled all 64 workers with non-reading UDS peers, observed no early follow-up service, then a fresh request at 31.0 seconds and complete socket/process cleanup; the same case passed under ASan/UBSan.
- lighttpd contracts passed (36 tests, 2 expected skips). Fresh Stock and Patched builds/checks and runtime smokes passed baseline `200`, Block `403`, event, shutdown, and listener cleanup.
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

The retained evidence covers engine-start availability, in-transaction failure, timeout, invalid/incomplete peer input, client/peer reset, incomplete HELLO and body/stream boundaries where the local harness provides them, parallel requests/streams, size/admission bounds, cancellation, shutdown, follow-up controls, and cleanup. SPOP logs record reset `errno=104`, EPIPE `errno=32`, and the current cache-miss `503` followed by real Block and Allow controls. Current Apache and NGINX hosts likewise retain Allow/Block/follow-up observations and listener cleanup. The Native UDS test asserts a legitimate subsequent request and absence of the assigned UDS listener after both reset and 64-peer send-deadline exhaustion.

## Checks not run and rationale

- No HAProxy HTX native host was available. NGINX and Apache have only the scoped current-host controls above, not complete host-vector coverage; the canonical NGINX harness remains sandbox-blocked.
- No native Envoy proxy or Traefik proxy host was started; connector/agent binaries and common services were exercised.
- A deliberately hung libmodsecurity engine was not simulated unsafely; bounded shutdown and controlled nonzero restart were checked by source/tests.
- Default Traefik `check-config` tried to create historical global `/var/tmp/ModSecurity-conector-verified/logs` and was sandbox-blocked. A task-owned config and `event_path` passed; no global path was created.
- Full native-host, HTTP/2/HTTP/3, reload, cross-connector leak, and ThreadSanitizer matrices remain unexecuted. CI was intentionally not run or changed.

## Known limitations

Native host integration and production-specific reload, TLS, HTTP/2, HTTP/3, and long-duration scheduling remain environment-dependent. The controlled restart branch is an explicit availability decision for an uninterruptible engine worker; it does not claim such a worker can be recovered without process restart. The retained evidence is strong local evidence, not complete hosted-matrix proof.

## Remaining risks

Operators still need to validate connector-specific limits, timeouts, TLS/UDS permissions, reload sequencing, and monitoring in native host versions. Unavailable native hosts and unexecuted matrices remain release-readiness limitations until independently reproduced. No CI or governance protection was weakened.

## Final diff and review status

Implementation evidence is retained, scoped to Parent, and paired with this bilingual Change Record. The NGINX zero-return, HAProxy SPOP saturated-admission and response-cache, Traefik Native UDS unread-peer, and Envoy `ext_proc` native-shutdown remediations are locally fixed; their finding records remain open or fixed rather than closed wherever native host/FD-vector evidence is still incomplete. This record performs no commit, push, PR, merge, or finding closure. Final delivery and any Draft PR require the parent agent's separate scoped diff review and delivery-policy checks.
