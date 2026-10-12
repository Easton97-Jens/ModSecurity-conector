# Change Record: CR-20261011-pr382-i10-adapter-errors

**Language:** English | [Deutsch](CR-20261011-pr382-i10-adapter-errors.de.md)

## Identity

| Field / Feld | Value / Wert |
| --- | --- |
| Change ID | CR-20261011-pr382-i10-adapter-errors |
| Date (UTC) | 2026-10-11 |
| Base revision | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| Original branch | `fix/unified-native-results-events-20260921` |
| Own branch | `fix/pr382-i10-adapter-errors-20261011` |
| `origin/master` and merge base | `3019722fbda40dc281b861c1cc38085be2f430a0` |
| Initial working tree | clean |
| Worktree | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` |
| Delivery worktree | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors-stack` |
| Delivery branch | `fix/pr382-i10-adapter-errors-stack-20261011` |
| Delivery base | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |
| Framework gitlink | `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| Current acceptance | `IMPLEMENTATION_PASS` |


## Motivation and problem statement

I10covers technical failure propagation through productive adapter/host boundaries. Completed I10a–I10e remain intact. Later user instructions authorize a separate worktree and a stacked Draft PR; merge, deployment and history rewriting remain outside scope.

## Acceptance criteria

Each of ten logical routes and separate request/companion legs must propagate technical failures terminally before and after commit. Off cannot ignore failures; Safe cannot convert technical failure into successful rule log_only. Strict admission follows the current registry. No stale rule state, second response, or repeated engine/EOS/host completion after failure is accepted. Productive executable caller tests, effective negative mutations and existing regressions must pass. Final focused, native, mutation, regression and lint checks passed. I10is checked; I11/I12 remain open.

| Route | Registry profile | Pre-commit off/safe/strict | Post-commit off/safe/strict | Reentry | Codefix | Test | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apache direct | `apache` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | Existing I10e retained | `tests.test_apache_terminal_contract_failures` | `IMPLEMENTATION_PASS` |
| NGINX direct | `nginx` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | Existing I10a/I10c retained | `tests.test_nginx_late_error_results` | `IMPLEMENTATION_PASS` |
| HAProxy direct HTX | `haproxy-htx` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | Terminal host action, commit, EOS and cleanup | `tests.test_haproxy_i10_host_callers` | `IMPLEMENTATION_PASS` |
| HAProxy SPOE/SPOP + HTX companion | `haproxy-spoe-spop` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | Request ACK503; separate binding/HTX response stop | `tests.test_haproxy_i10_binding_callers` | `IMPLEMENTATION_PASS` |
| Envoy ext_authz + MRC1 companion | `envoy-ext-authz` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | HTTP/gRPC authorization and independent response stop | `tests.test_i10_service_callers; compositeenvoy` | `IMPLEMENTATION_PASS` |
| Envoy ext_proc | `envoy-ext-proc` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | Checked close ABI and incomplete stream propagation | `internal/processor` | `IMPLEMENTATION_PASS` |
| Traefik forwardAuth + MRC1 observer | `traefik-forwardauth` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | HTTP failclosed; observer commit/outcome ordering | `tests.test_i10_service_callers; response_observer` | `IMPLEMENTATION_PASS` |
| Traefik Native/UDS | `traefik-native-uds` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | MSE1 terminal result; middleware ErrAbortHandler | `tests.test_traefik_i10_dispatcher; native_middleware` | `IMPLEMENTATION_PASS` |
| lighttpd stock/sidecar | `lighttpd-stock` | off/safe: failclosed; strict: supported | off/safe: terminal host result; no second response; strict: supported | once-only terminal latch | Exchange return, socket shutdown, first status | `tests.test_lighttpd_i10_adapter_errors` | `IMPLEMENTATION_PASS` |
| lighttpd patched/native | `lighttpd-patched` | off/safe: failclosed; strict: unsupported; admission unchanged | off/safe: terminal host result; no second response; strict: unsupported; admission unchanged | once-only terminal latch | Terminal hooks, reset, upstream error | `tests.test_lighttpd_i10_adapter_errors` | `IMPLEMENTATION_PASS` |

The 14 separately inventoried route legs are:

`nginx-native`, `apache-native`, `haproxy-native-htx`, `haproxy-spoe-spop-request`, `haproxy-spop-htx-response-companion`, `envoy-ext-proc`, `envoy-ext-authz-request`, `envoy-ext-authz-response-companion`, `traefik-native-middleware-uds`, `traefik-forwardauth-request`, `traefik-forwardauth-response-observer`, `lighttpd-stock-sidecar`, `lighttpd-stock-native-control`, `lighttpd-patched-native`.

`lighttpd-stock-native-control` is an additional control route, not an eleventh canonical route. SPOP, ext_authz and forwardAuth request legs do not prove P3/P4 processing; companion evidence is retained separately.

### Internal nine-column I10evidence matrix

Rows describe actual executed test scope; they do not claim a complete Cartesian product of every cause, mode and host transport state. Shared policy and productive caller matrices are separate evidence. Exact case partitions are in versioned fixtures and test logs.

| Route | Error class | Commit state | Mode | Common decision | Adapter result | Host control | Actual observation | Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `apache-native` | native/intervention/host failure | pre; committed headers/body; reentry | off/safe; strict not admitted | technical error precedes rule | APR/filter terminal result | existing failclosed/filter stop | compiled productive APR/native seams | `tests.test_apache_terminal_contract_failures` |
| `nginx-native` | late native/technical failure | pre; committed headers/body; reentry | off/safe; legacy strict regression only | technical error precedes late rule | terminal nginx status | existing dispatcher stop | compiled actual collector/dispatcher/P4 chain | `tests.test_nginx_late_error_results` |
| `haproxy-native-htx` | Common/native/header/EOS/ack failure | pre; committed headers/body; reentry | off/safe; parsed strict only | retained first technical error | latched error/once cleanup | 503 before commit; kill request after | actual extracted HTX API calls; no client-abort claim | `tests.test_haproxy_i10_host_callers` |
| `haproxy-spoe-spop-request` | P1/P2 native/finish failure | pre; terminal reentry | detect/enforce x open/closed | technical failure independent of rule mode | disruptive SPOP503 ACK | deny/error request output | productive TU; real encoded ACK | `tests.test_haproxy_i10_binding_callers` |
| `haproxy-spop-htx-response-companion` | P3/P4/header/commit/EOS/ack failure | pre; committed headers/body; reentry | off/safe; strict not admitted | first cause retained; no stale rule | MRC1/HTX terminal result | once HTX stop request | productive binding + controlled HTX host seam | `tests.test_haproxy_i10_binding_callers` |
| `envoy-ext-proc` | response begin/EOS/cancel/cleanup failure | pre; committed headers/body; reentry | off/safe; strict rejected | terminal technical failure | non-nil gRPC error/checked close | stop callback chain | productive processor; real CGo/libmodsecurity suite separate | `internal/processor/technical_error_test.go; tests.test_i10_envoy_finish` |
| `envoy-ext-authz-request` | five canonical causes at begin/handoff/finish | pre; first-cause cleanup | off/safe; strict not admitted | canonical technical classification | HTTP error or non-nil authz error | no allow or stale host action | productive C socket output + productive Go AuthzServer | `tests.test_i10_service_callers; compositeenvoy/technical_error_test.go` |
| `envoy-ext-authz-response-companion` | five backend causes; protocol/commit/EOS failure | pre; committed headers/body; terminal reentry | off/safe; strict not admitted | first cause; non-OK MRC1 | MRC1 error; non-nil gRPC error | no second ImmediateResponse | productive transport wire bytes + productive composite server | `tests.test_i10_service_callers; compositeenvoy/technical_error_test.go` |
| `traefik-native-middleware-uds` | five causes; commit/EOS/finish/destroy/host-write | pre; committed headers/body; reentry | configured off/safe; strict rejected | first technical error; no log_only success | ERROR MSE1;500 precommit; ErrAbortHandler late | HTTP failclosed/terminal host stop | productive C dispatcher + real private UDS + ServeHTTP | `tests.test_traefik_i10_dispatcher; native_middleware/technical_error_test.go` |
| `traefik-forwardauth-request` | five canonical begin/handoff/finish causes | pre; first-cause cleanup | off/safe; strict not admitted | canonical technical classification | HTTP error | no allow | productive authorization service/socket bytes | `tests.test_i10_service_callers` |
| `traefik-forwardauth-response-observer` | typed technical/body/EOS/release/ack/host-write | pre; committed headers/body; reentry | off/safe; strict not admitted | technical differs from genuine rule log_only | 503 precommit; original status late | ErrAbortHandler; WriteHeader before ACK | productive observer + real MRC1 private socket | `response_observer/observer_test.go` |
| `lighttpd-stock-sidecar` | runtime/metadata/P3/P4/EOS/ack failure | pre; committed headers/body; reentry | off/safe/strict supported | clean allow required; first cause retained | failed exchange result | shutdown only after successful syscall | productive socket exchange; real peer EOF at seam | `tests.test_lighttpd_i10_adapter_errors` |
| `lighttpd-stock-native-control` | P1/P3/commit/reset error | pre; headers/body commit; reentry | off/safe; strict unsupported | retained diagnostic-control error | terminal hook result | no default accept | mechanically compiled actual productive native hooks | `tests.test_lighttpd_i10_adapter_errors` |
| `lighttpd-patched-native` | P1/P2/P3/P4/upstream/reset failure | pre; committed headers/body; reentry | off/safe; strict unsupported | terminal technical latch | HANDLER_ERROR; once destruction | stop native hook; no second status | mechanically compiled productive hooks + real Common types | `tests.test_lighttpd_i10_adapter_errors` |

### Technical causes and commitment

Common classifies the first cause under the existing contract. Default HTTP statuses below come from `common/src/error.c`; a specific adapter may use its existing fail-closed status. No universal equality of outward host status is claimed.

| Canonical class | Common cause | Default HTTP status |
| --- | --- | --- |
| `INVALID_ENGINE_RESPONSE` | `MODSECURITY_FAILURE` | 500 |
| `CONNECTOR_ERROR` | `HOST_API_FAILURE`, `IO`, `INTERNAL` | 500 |
| `PROTOCOL_ERROR` | `PROTOCOL` | 502 |
| `ENGINE_TIMEOUT` | `TIMEOUT` | 504 |
| `ENGINE_UNAVAILABLE` | `RUNTIME_UNAVAILABLE` | 503 |

Executable matrices vary precommit, committed headers, started body and terminal reentry. EOS, commit, host acknowledgement and native/body/companion failures retain their actual produced error; client cancel/upstream disconnect are tested only at the existing respective productive seams. Off/Safe select technical failure handling, never successful rule log_only; genuine late-rule log_only controls remain intact. A later cleanup/logging failure does not erase the first cause.

## Implementation decision and rationale

Common state-machine and wire contracts remain intact. Productive callers require exactly `1`, preserve the first technical failure and seal subsequent callbacks. Before commit they use existing canonical error statuses. After commit host errors/stop-I/O, `http.ErrAbortHandler` and non-nil gRPC errors propagate terminal failure without inventing a replacement response. Checked Envoy cleanup ABI supplements the compatible existing ABI. A requested HAProxy stream shutdown is not recorded as observed client abort.

| Productive path | Before / Root cause | Fix | Executable regression |
| --- | --- | --- | --- |
| Common HTTP authorization | Nonzero runtime/handoff accepted; cleanup could replace first cause | Exact 1; separate cleanup error; preserve first response cause | `test_i10_service_callers.py` |
| Common MRC1 backend | Invalid nonzero result could be success; failed release could close state as success | Exact 1 normalization; typed error preservation; once cleanup | `test_i10_service_callers.py` |
| HAProxy HTX/binding | Terminal callbacks could pass payload/repeat action; commit/EOS/outcome errors swallowed | Terminal result and action latch; checked commit/finish/ack; no invented observed abort | `test_haproxy_i10_host_callers.py`, `test_haproxy_i10_binding_callers.py` |
| HAProxy SPOP | fail_mode=open/detect-only converted technical failure to pass; finish failure lost | Technical ACK503 independent of rule enforcement mode; first cause retained | productive SPOP C fixture |
| Envoy ext_authz companion | Committed error sent another ImmediateResponse; initial terminal EOS allowed reentry | Commit guard, terminal loop guard, gRPC failure | `compositeenvoy/technical_error_test.go` |
| Envoy ext_proc | Incomplete stream/checked cleanup failure could end normally | Terminal stream failure and checked close propagation | `processor/technical_error_test.go` |
| Traefik native C/UDS/Go | Begin/commit/EOS/cleanup/ack and ignored host-write failures could continue | Exact 1, failed-session seal, first error, ErrAbortHandler after commit | C dispatcher and productive UDS middleware tests |
| Traefik observer | Technical result treated as rule; host outcome acknowledged before WriteHeader; failed body/EOS/release ignored | Typed technical failure; host write before ACK; terminal host stop | `response_observer/observer_test.go` |
| lighttpd native | Failed context freed/recreated; commit/reset/upstream errors swallowed | Tombstone until reset; checked commit; HANDLER_ERROR after commit; single destruction | productive native fixture |
| lighttpd stock sidecar | Receipt write success became exchange success; unchecked runtime metadata/ack | Require clean allow completion; retain canonical failure; checked shutdown before action record | productive sidecar/socket fixture |
| lighttpd sidecar first cause | sidecar_exchange_error checked expired deadline before existing state.error.code, producing 504/timeout after first HOST/MODSECURITY failure | Retained typed code precedes deadline; timeout only for NONE; separate completion_error preserves diagnostics through fail/action/finish | 27 late-deadline controls +2 status/timeout mutations; final 479-case run PASS |


Additional final productive cause audit: Common MRC1 preserves MODSECURITY as INVALID_ENGINE_RESPONSE instead of CONNECTOR_ERROR. HAProxy retrieves the retained first code through a bounded getter; response-header API failure remains HOST_API_FAILURE and native engine failure remains MODSECURITY_FAILURE; RELEASE-consumed pointers are not reused. Envoy server stop before Serve could leave an unadopted listener; a local waiter closes it safely. limitedListener guards Close with sync.Once, tested with 32 concurrent closes and a deterministic mutation. Current final native/caller/mutation checks validate these edits.

## Changed files

Product changes cover two Common runtime files, Envoy composite/processor/bridge files, HAProxy HTX/binding/SPOP, lighttpd module/sidecar and Traefik C service/Go middleware/observer. Tests add executable C/Go/Python callers, socket and mutation fixtures, plus updated HAProxy adoption assertions. Root Makefile and five existing connector/Common workflows wire the tests. Documentation pairs are this Change Record, the PR checklist and remaining-work matrix. Framework/MRTS and the gitlink remain unchanged.

Two baseline-stale source assertions in `tests/test_native_api_fail_closed_contract.py` and `tests/test_apache_fail_closed.py` were aligned with unchanged productive native helpers and typed Apache fail-closed paths, strengthened with truth-table/delegation checks. The initial broad core run showed 15 failures/4 errors from old assertions; it is not relabelled as product PASS. Fresh core-final passes 87 tests including the two added controls. The older combined NGINX adoption run was terminated after 1800 s;103 of 110 cases ran without adoption failure, and the seven remaining cases passed separately with ten Envoy bridge cases.

## Commands executed

All commands below ran through RTK. Each run has `command.json`, `result.json` and `output.log` under the external evidence root. This final ledger retains both passed final checks and earlier failed/timed checkpoints. Earlier failed runs are not relabelled; corrected reruns require separate evidence. A zero count means no machine-readable count was collected, not zero assertions checked.

`/var/tmp/codex/ModSecurity-conector/i10-20261011/evidence`

| Run | Exact payload command | Working directory | Exit | Counts | Evidence relative to root |
| --- | --- | --- | --- | --- | --- |
| `common-callers-complete` | `rtk proxy make check-i10-common-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=6; Go test counts not collected/not applicable | `common-callers-complete/result.json`, `common-callers-complete/output.log` |
| `common-callers-final` | `rtk proxy make check-i10-common-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=6; Go test counts not collected/not applicable | `common-callers-final/result.json`, `common-callers-final/output.log` |
| `common-callers-retained` | `rtk proxy make check-i10-common-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 2 | unittest=6; Go test counts not collected/not applicable | `common-callers-retained/result.json`, `common-callers-retained/output.log` |
| `common-native` | `rtk proxy make check-common-helpers-c17 check-http-authorization-service-timeout` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=0; Go test counts not collected/not applicable | `common-native/result.json`, `common-native/output.log` |
| `core-confirmed` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_pr382_profile_errors tests.test_pr382_decision_safety tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_native_api_fail_closed_contract tests.test_apache_native_lifecycle tests.test_apache_terminal_contract_failures tests.test_apache_fail_closed tests.test_nginx_late_error_results tests.test_nginx_native_intervention_chain tests.test_envoy_bridge_failures` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 1 | unittest=85; Go test counts not collected/not applicable | `core-confirmed/result.json`, `core-confirmed/output.log` |
| `core-final` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_pr382_profile_errors tests.test_pr382_decision_safety tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_native_api_fail_closed_contract tests.test_apache_native_lifecycle tests.test_apache_terminal_contract_failures tests.test_apache_fail_closed tests.test_nginx_late_error_results tests.test_nginx_native_intervention_chain tests.test_envoy_bridge_failures` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=87; Go test counts not collected/not applicable | `core-final/result.json`, `core-final/output.log` |
| `core-regressions` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_pr382_profile_errors tests.test_pr382_decision_safety tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_native_api_fail_closed_contract tests.test_apache_native_lifecycle tests.test_apache_terminal_contract_failures tests.test_apache_fail_closed tests.test_nginx_late_error_results tests.test_nginx_native_intervention_chain tests.test_nginx_common_adoption tests.test_envoy_bridge_failures` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | -15 | unittest=0; Go test counts not collected/not applicable | `core-regressions/result.json`, `core-regressions/output.log` |
| `core-remaining` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unconditional_mapper_early_return_is_rejected tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unscanned_local_include_extension_is_rejected tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unscanned_out_of_root_local_header_is_rejected tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unknown_angle_include_is_rejected tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unreachable_body_response_mapper_calls_are_rejected tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unreachable_header_response_mapper_calls_are_rejected tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_unreachable_or_unchecked_chain_call_is_rejected tests.test_envoy_bridge_failures` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=17; Go test counts not collected/not applicable | `core-remaining/result.json`, `core-remaining/output.log` |
| `envoy-finish-c` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i10_envoy_finish` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=4; Go test counts not collected/not applicable | `envoy-finish-c/result.json`, `envoy-finish-c/output.log` |
| `envoy-focused-final` | `rtk proxy go test -mod=readonly -count=1 -json ./internal/processor ./internal/compositeenvoy` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/connectors/envoy/ext_proc` | 1 | unittest=0; Go pass/fail/skip events=155/1/0 | `envoy-focused-final/result.json`, `envoy-focused-final/output.log` |
| `envoy-go` | `rtk proxy go test -mod=readonly -count=1 -json ./...` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/connectors/envoy/ext_proc` | 0 | unittest=0; Go pass/fail/skip events=275/0/0 | `envoy-go/result.json`, `envoy-go/output.log` |
| `envoy-go-final` | `rtk proxy go test -mod=readonly -count=1 -race -json ./...` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/connectors/envoy/ext_proc` | 1 | unittest=0; Go pass/fail/skip events=279/1/0 | `envoy-go-final/result.json`, `envoy-go-final/output.log` |
| `envoy-i10-final` | `rtk proxy make check-i10-envoy-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 2 | unittest=5; Go test counts not collected; packages PASS=8 | `envoy-i10-final/result.json`, `envoy-i10-final/output.log` |
| `envoy-i10-integrated` | `rtk proxy make check-i10-envoy-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=5; Go test counts not collected; packages PASS=8 | `envoy-i10-integrated/result.json`, `envoy-i10-integrated/output.log` |
| `envoy-mutations-complete` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i10_envoy_mutations` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=1; Go test counts not collected/not applicable | `envoy-mutations-complete/result.json`, `envoy-mutations-complete/output.log` |
| `envoy-native` | `rtk proxy make -C connectors/envoy test-envoy-ext-proc MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu MODSECURITY_LIB_FILE=/usr/lib/x86_64-linux-gnu/libmodsecurity.so` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 2 | unittest=0; Go test counts not collected; packages PASS=15 | `envoy-native/result.json`, `envoy-native/output.log` |
| `envoy-native-complete` | `rtk proxy make -C connectors/envoy test-envoy-ext-proc MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu MODSECURITY_LIB_FILE=/usr/lib/x86_64-linux-gnu/libmodsecurity.so` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=0; Go test counts not collected; packages PASS=16 | `envoy-native-complete/result.json`, `envoy-native-complete/output.log` |
| `envoy-native-final` | `rtk proxy make -C connectors/envoy test-envoy-ext-proc MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu MODSECURITY_LIB_FILE=/usr/lib/x86_64-linux-gnu/libmodsecurity.so` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 2 | unittest=0; Go test counts not collected; packages PASS=7 | `envoy-native-final/result.json`, `envoy-native-final/output.log` |
| `envoy-target-complete` | `rtk proxy make check-i10-envoy-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=5; Go test counts not collected; packages PASS=8 | `envoy-target-complete/result.json`, `envoy-target-complete/output.log` |
| `envoy-vet` | `rtk proxy go vet -mod=readonly ./...` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/connectors/envoy/ext_proc` | 0 | unittest=0; Go test counts not collected/not applicable | `envoy-vet/result.json`, `envoy-vet/output.log` |
| `envoy-vet-complete` | `rtk proxy go vet -mod=readonly ./...` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/connectors/envoy/ext_proc` | 0 | unittest=0; Go test counts not collected/not applicable | `envoy-vet-complete/result.json`, `envoy-vet-complete/output.log` |
| `focused-services` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i10_service_callers tests.test_i10_envoy_mutations` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=7; Go test counts not collected/not applicable | `focused-services/result.json`, `focused-services/output.log` |
| `haproxy-suite-complete` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_haproxy*.py' -v` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=194; Go test counts not collected/not applicable | `haproxy-suite-complete/result.json`, `haproxy-suite-complete/output.log` |
| `haproxy-target-complete` | `rtk proxy make check-i10-haproxy-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=7; Go test counts not collected/not applicable | `haproxy-target-complete/result.json`, `haproxy-target-complete/output.log` |
| `integration-contracts` | `rtk proxy make check-haproxy-common-adoption check-envoy-common-adoption check-traefik-common-adoption check-lighttpd-common-adoption check-remaining-connectors-host-integration check-remaining-connectors-build-wiring check-remaining-connectors-start-wiring check-remaining-connectors-claim-policy check-haproxy-htx-overlay check-common-security-contract check-adapter-contracts` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=12; Go test counts not collected/not applicable | `integration-contracts/result.json`, `integration-contracts/output.log` |
| `lighttpd-integrated` | `rtk proxy make check-i10-lighttpd-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=7; Go test counts not collected/not applicable | `lighttpd-integrated/result.json`, `lighttpd-integrated/output.log` |
| `lighttpd-sidecar-native-complete` | `rtk proxy make -C connectors/lighttpd build-lighttpd-stock-sidecar MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=0; Go test counts not collected/not applicable | `lighttpd-sidecar-native-complete/result.json`, `lighttpd-sidecar-native-complete/output.log` |
| `lighttpd-suite-complete` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_lighttpd*.py' -v` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=22; Go test counts not collected/not applicable | `lighttpd-suite-complete/result.json`, `lighttpd-suite-complete/output.log` |
| `lighttpd-suite-final` | `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_lighttpd*.py' -v` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=22; Go test counts not collected/not applicable | `lighttpd-suite-final/result.json`, `lighttpd-suite-final/output.log` |
| `lint` | `rtk proxy make lint` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 2 | unittest=214; Go test counts not collected; packages PASS=1 | `lint/result.json`, `lint/output.log` |
| `lint-complete` | `rtk proxy make lint` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=302; Go test counts not collected; packages PASS=33 | `lint-complete/result.json`, `lint-complete/output.log` |
| `lint-final` | `rtk proxy make lint` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | -15 | unittest=265; Go test counts not collected; packages PASS=1 | `lint-final/result.json`, `lint-final/output.log` |
| `nginx-native-complete` | `rtk proxy make check-nginx-c17 NGINX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/i10-20261011/prerequisites/nginx-1.31.6` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=0; Go test counts not collected/not applicable | `nginx-native-complete/result.json`, `nginx-native-complete/output.log` |
| `traefik-integrated` | `rtk proxy make check-i10-traefik-callers` | `/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors` | 0 | unittest=3; Go test counts not collected; packages PASS=2 | `traefik-integrated/result.json`, `traefik-integrated/output.log` |

Additional worker evidence: `/var/tmp/codex/ModSecurity-conector/{haproxy-i10,traefik-i10,lighttpd-i10}`.

Traefik: actual Go race command `rtk proxy env GOTOOLCHAIN=local GOFLAGS=-mod=readonly GOCACHE=/var/tmp/codex/ModSecurity-conector/traefik-i10/go-cache GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -count=1 -race -json ./...` in both Go modules: native 56 top-level/115 PASS events, observer 32/54, exit 0, no skips. RTK-wrapped `go vet ./...` exits 0 in both. Selected Parent 26 tests exit 0. Durable negative controls 11Go+4C individually passed (each mutation assertion-red); final root aggregate remains authoritative.

Lighttpd final owned run: `rtk proxy sh -c '/root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lighttpd_i10_adapter_errors > /var/tmp/codex/ModSecurity-conector/lighttpd-i10/final-owned-pass.log 2>&1'`, exit 0, 7 tests in 78.424 s, 450 C executions including 7 assertion-red mutations. Native/patched and sidecar are tested separately. Older full discovery 42 is an earlier source snapshot. Root lighttpd-suite-final freshly passed 22 selected Parent tests; connector-local Framework tests are not part of that pattern.

Earlier HAProxy caller checkpoint: `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_i10_host_callers tests.test_haproxy_i10_binding_callers`, exit 0, 6 tests in 167.715 s, all 15 compiled/executed mutations assertion-red (HTX9/SPOP4/binding 2); evidence `/var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/final-callers.log`. `rtk proxy make check-haproxy-common-adoption check-haproxy-c-standard-wiring check-haproxy-htx-overlay` exit 0; `rtk proxy make -C connectors/haproxy test-htx-overlay BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/haproxy-i10/build` exit 0,28 overlay assertions+18 helper tests. Binding matrix 126 =7 causes×2 routes×3 modes×3 commit states; Strict parsing cases do not establish admitted Strict profile capability.

Documentation check: `rtk proxy make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/modules/ModSecurity-test-Framework` exit 0; bilingual structure, repository path references and doc links PASS. Initial own run exit 2 due to missing mandatory Change Record identity fields; a fresh rerun passed after correction. `rtk proxy git diff --check` exit 0. RTK0.51.0 and `rtk gain` observed.

Current final HAProxy evidence after the last getter/nested-result/borrowed-reason fixes: host 2 tests exit 0 in 23.910 s (`final-nested-verified.log`,14 mutations); binding/SPOP4 tests exit 0 in 128.057 s (`final-retained-verified.log`,5SPOP+2 binding mutations); borrowed-reason 1 test exit 0 in 17.711 s (`final-borrowed-reason.log`,1 additional SPOP mutation). Current 7 new test methods and 22 actual compiled/executed mutations (host 14/SPOP6/binding 2). Current source regressions 34 exit 0; native 3 targets exit 0 with 115 PASS assertions. Earlier full discovery 193 exit 0,12 skips,195.649 s predates the last fixes; the fresh root haproxy-suite-complete now executes all 194 current tests successfully in 181.819 s. The fresh haproxy-target-complete also passes 7 methods/22 mutations in 134.454 s. Newly found nested-result defect: API return 1 with `result.success=0/-1/2` could degrade EOS Off/Safe; productive nested results now also require exactly 1. RELEASE raw 0/-1/2 controls are tested independently; requested stream shutdown produces no invented observed OUTCOME.

Exact final HAProxy commands, each in the own worktree:

| Command | Exit | Counts |
| --- | --- | --- |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_i10_host_callers > /var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/final-nested-verified.log 2>&1` | 0 | 2 tests;14 mutants |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_i10_binding_callers > /var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/final-retained-verified.log 2>&1` | 0 | 4 methods loaded;7 mutants |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_i10_binding_callers.HAProxyI10BindingCallers.test_spop_failure_reason_negative_control > /var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/final-borrowed-reason.log 2>&1` | 0 | 1 test;1 mutant |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_htx_filter_security_contract tests.test_haproxy_htx_payload_fail_closed_contract tests.test_haproxy_spop_peer_isolation_contract > /var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/final-nested-regressions.log 2>&1` | 0 | 34 tests |
| `rtk proxy make check-haproxy-common-adoption check-haproxy-c-standard-wiring check-haproxy-htx-overlay > /var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/final-nested-native.log 2>&1` | 0 | 115 PASS assertions |

Current lighttpd final evidence: `rtk proxy sh -c '/root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lighttpd_i10_adapter_errors > /var/tmp/codex/ModSecurity-conector/lighttpd-i10/final-first-cause-verified.log 2>&1'` exit 0,7 tests in 116.098 s,479 executable cases including 9 assertion-red mutations. Before commit typed HOST/MODSECURITY failure stays 500 despite a later expired deadline; after commit no second response or timeout relabelling occurs. Full sidecar C17-Wall-Wextra-Werror syntax and diff checks exit 0. Earlier 450/7-mutation evidence remains historical checkpoints.

Complete native HAProxy HTX build: `rtk proxy env MAKE_JOBS=8 TMPDIR=/var/tmp/codex/ModSecurity-conector/haproxy-i10/full-htx-20261011/tmp MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu make -C connectors/haproxy build-htx-overlay BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/haproxy-i10/full-htx-20261011 HAPROXY_HTX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/i10-20261011/prerequisites/haproxy-3.2.25 HAPROXY_HTX_BUILD_DIR=/var/tmp/codex/ModSecurity-conector/haproxy-i10/full-htx-20261011/overlay FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/i10-adapter-errors/modules/ModSecurity-test-Framework > /var/tmp/codex/ModSecurity-conector/haproxy-i10/evidence/full-htx-build.log 2>&1`, exit 0. Pinned HAProxy 3.2.25 with genuine ModSecurity 3.0.14; productive HTX filter, binding and Common client compiled/linked completely. Eight warnings under unchanged build flags (7 C90 mixed declarations,1 existing unused helper), no warning-free claim. Optional Rule-ID API feature probe used its expected fallback; the build passed. Binary SHA256 `29f259454bc5bb107b7a003ae44b7d87393dfe93d1287b4f6717aaacd5ec53ed`; staged current product hashes match. Build evidence does not prove live-host/client reset.

## Security impact

Failures become terminal instead of fail-open. Authentication, isolation, redaction, compiler warnings, assertions and Quality Gates are preserved. Technical errors remain distinct from rule interventions; first cause and already-sent bytes/status are retained. No new Strict capability is declared.

## Runtime evidence

Productive functions execute with real Common types/state/policy contracts, actual local socket bytes and controlled host/native seams. HTTP/MRC1 fixtures cover 180 HTTP failures,120 MRC1 failures and 8 positive transport controls. Traefik C dispatcher covers 600 failures+600 reentries+240 success controls+2 socket-stop checks; installed genuine libmodsecurity 3.0.14 initializes runtime, while native phase calls are deliberately intercepted. This is not genuine rule evaluation. Host API invocation, selected/requested action and observed transport remain separate. ErrAbortHandler, HTX kill and HANDLER_ERROR prove adapter outputs, not actual client reset. Sidecar socket seams observe peer EOF, not live lighttpd operation.

## Known limitations

I11 physical sink serialization/open/write/short-write/close and producer/sink parity remain outside this fix; known Apache and SPOP sink issues are not closed. I12/V08–V10 full live-host/client/transport/neighbor-stream matrices, including actual companions, remain open. Environment: installed Python 3.14.4 versus pinned 3.14.7 and Go 1.27.2 versus 1.27.1 require transparent assessment. Framework venv is absent; task-owned clone uses a compatible existing Parent venv without installation. Initially absent native HAProxy/lighttpd prerequisites were resolved using copied existing host headers/config without installation. Both stock and patched productive lighttpd module builds now pass C17 -Wall -Wextra -Werror and link real libmodsecurity.so.3; check-haproxy-c17 also passed. This does not prove live-host behavior.

The final lighttpd late-deadline cause-overwrite finding is repaired and verified by the latest 479-case run. Final cross-route/lint reconciliation passed; this repaired defect is distinct from I11/I12.

Current full HAProxy194 suite retains12 unchanged baseline skips; a skip is not an executed PASS. Productive new caller/mutation checks skip no technical acceptance. Exact toolchain patch-version pins remain a separate reproducibility limitation; native SDK prerequisite gaps are resolved by actual builds.

## Remaining risks

I10implementation: final cross-route reconciliation and aggregate validation passed; no known adapter code gap remains. A finding cannot be closed before its productive caller test and regression pass. I11/I12 and environment remainder are separate from implementation completion. CI/Sonar/reviews and Draft PR head must be freshly observed at actual delivery.

## Checks not run and rationale

No full live-host matrix, production run, H2/H3 neighbor-stream matrix or physical sink fault campaign was run: these belong to I11/I12. No merge/deployment or toolchain installation. Checks with actual failures remain in the ledger; outstanding reruns are not claimed as PASS.

Stacked delivery: base branch remains fix/unified-native-results-events-20260921. Its remote head was subsequently observed as `498653c2a193d34b7b25b2903b1e4db1c45e7f73`; new B09 changes do not overlap. Our initial HEAD remains `0df51024008fc84f0a6820f3b011055b69c3a3e2`; no merge/rebase is claimed. Actual Draft PR head and CI must be freshly bound at delivery.

## Final diff and review status

Final diff was reviewed against original requirements and productive seams; independent review and final first-cause/reentry/negative controls leave no known adapter implementation gap. I10a–I10e remain intact. I09/I11/I12 and V08–V10 retain their separate open remainder. Stacked Draft [PR #409](https://github.com/Easton97-Jens/ModSecurity-conector/pull/409) is open on the selected base branch. Initial commit `4d451b8515e0f7bea888050dc1e898d645dfd30a` was pushed and verified against local, remote and PR head. Current CI follow-up work remains `checks_pending`; no merge/deployment is claimed.

Delivery was prepared in an additional own worktree on the observed PR #382 base `498653c2a193d34b7b25b2903b1e4db1c45e7f73`. The complete task patch was transferred; original worktree/branch/start HEAD and test identities remain intact. Fresh delivery checks confirmed the transferred I10 source hashes and retained B09 fix. No merge/rebase/history rewrite occurred; follow-up CI/Sonar head binding remains checks_pending at commit preparation.

Delivery verification passed: all 58 task files were byte-identical after transfer (delivery-source-binding.json); the retained B09 fixture passed 4 tests (delivery-b09, exit 0), and fresh bilingual/path/link checks passed (delivery-checks, exit 0).

## Hosted CI follow-up

Stacked Draft PR409 was created and initial head `4d451b8515e0f7bea888050dc1e898d645dfd30a` pushed. Its first hosted checks exposed two test-driver prerequisite defects: lighttpd embedded RTK in child argv although RTK is only the local outer execution proxy; Traefik's C mutation driver treated a successfully skipped child without libmodsecurity as a surviving mutation. Both are corrected without weakening assertions. A PATH=/usr/bin:/bin run executes all7 lighttpd methods without child RTK. Actual installedSDK executes all15 Traefik mutations without skips; controlled missing compiler/library branches each produce an explicit Skip without launching a child. The latter are prerequisite checks, not executed C acceptance.

Full wrapper-authenticated Sonar readback for that exact initial head returned170 OPEN CODE_SMELL issues (HAProxy76, lighttpd75, Traefik17, Envoy2), zero accepted issues/security hotspots and0.0% duplication. The standard Quality Gate passed, while the repository's stricter zero-findings check failed; neither that gate nor earlier successful checks establish the follow-up head's pass. Readback pagination total170 matched all170 records. Authentication used the verified canonical `/usr/local/bin/sonar-with-env` under RTK, without credentials in evidence.

Follow-up changes split declarations/assignments/ternaries and extract bounded scenario helpers. Real native headers and production ABI remain unchanged. Read-only controlled test stubs are explicitly named fixture seams mapped after the headers; their const qualifiers describe the test seam only. All case combinations, typed first-cause, terminal reentry, once-only cleanup and effective mutations remain. lighttpd's two nested status expressions become equivalent ordered conditions, preserving an earlier typed cause over a later deadline. Independent review additionally retained the native lighttpd expected-status oracle as literal504/503/502/500 values instead of sharing production status mapping. No rule, gate, exclusion, suppression or assertion was relaxed.

Fresh focused follow-up checks (own delivery worktree; external environment and command.json/result.json/output.log retained):

| Exact command | Exit | Python methods | Seconds | Run ID |
| --- | --- | --- | --- | --- |
| `rtk proxy env PATH=/usr/bin:/bin /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lighttpd_i10_adapter_errors` | 0 | 7 | 17.498 | `ci-lighttpd-no-rtk-path` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_traefik_i10_mutations` | 0 | 2 | 49.729 | `ci-traefik-mutation-prerequisites` |
| `rtk proxy make check-i10-envoy-callers` | 0 | 5 | 30.007 | `envoy-sonar-test-refactor` |
| `rtk proxy go vet -mod=readonly ./...` | 0 | 0 | 2.095 | `envoy-sonar-vet` |
| `rtk proxy make check-i10-traefik-callers` | 0 | 3 | 56.693 | `sonar-traefik-refactor` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_lighttpd*.py' -v` | 0 | 22 | 15.227 | `sonar-lighttpd-oracle` |
| `rtk proxy env MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu make -C connectors/lighttpd build-lighttpd-stock-sidecar` | 0 | 0 | 9.906 | `sonar-lighttpd-native` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_haproxy_i10_host_callers tests.test_haproxy_i10_binding_callers -v` | 0 | 7 | 68.521 | `sonar-haproxy-refactor` |

Traefik target also executes both Go race/vet packages and the native dispatcher; Envoy target executes8 Go race packages and all5 Go mutations plus checked-C-finish controls. HAProxy retains7 methods/22 effective mutants. The latest lighttpd22 suite retains479 executable cases/9 mutants; genuine native sidecar compile/link uses installed libmodsecurity3.0.14 with C17 warning controls. The controlled Traefik prerequisite proof is separately recorded in `evidence/ci-traefik-prerequisite-skips/` (exit0, two explicit skips). Initial portable-source tests and initial refactor runs remain historical evidence; final oracle-preserving lighttpd result supersedes the earlier fixture refactor.

The initial58-file byte-identical transfer remains historical and valid. These scoped follow-up edits intentionally change selected transferred test files and two sidecar status expressions; no claim of unchanged current58 hashes is made. Complete base-to-final-head patch is refreshed at delivery. At follow-up commit preparation, fresh hosted CI and Sonar for the new head are `checks_pending`; final observed head/status are recorded in the PR body and external delivery evidence.

The Cloud analysis of follow-up head `7db88256d3d4a74a645e0f27450d35cd382cc8fe` confirmed all original170 issues absent, but raised one new fixture parameter-count issue. `fixture_verify` now accepts five parameters, grouping case values and captured counters in a const snapshot. The independent literal status oracle, all assertions,479 cases and9 effective mutants are retained. Fresh `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_lighttpd*.py' -v` passed (exit0,22 methods,15.477 s; `evidence/sonar-lighttpd-parameters/`). Fresh Cloud/CI must bind to the subsequent head.

I10 IMPLEMENTATION COMPLETE – remaining live-host/transport evidence belongs to I12/V08-V10
