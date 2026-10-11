# Change Record: CR-20261011-i09-native-route-reconciliation

**Language:** English | [Deutsch](CR-20261011-i09-native-route-reconciliation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-i09-native-route-reconciliation |
| Date (UTC) | 2026-10-11 |
| Base revision | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |

## Motivation and problem statement

I09 still had unaudited native/API callers and technical errors that could become successful phases, false rule events or invented host actions. Audit and fix all ten profiles and their 14 actual route legs on PR382 without redesigning completed subsets.

## Acceptance criteria

Inventory every supported leg; use operation-specific results; preserve first cause/phase, truthful typed events and terminal reentry/cleanup; execute compiled fault and legitimate-success controls; retain separate I10/I11/I12 acceptance.

## Implementation decision and rationale

Retain canonical error_phase and checked once-only logging; normalize undocumented callbacks with nullable error output; seal missing-rule failures. Repair Apache filter action order, HAProxy binding/bridge/HTX producers, Traefik UDS/Go acknowledgements and lighttpd commit/abort hooks. Each change fixes a confirmed caller path without changing defaults or sink contracts.

## Changed files

- `.github/workflows/lint.yml`
- `Makefile`
- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`
- `common/include/msconnector/event_protocol.h`
- `common/include/msconnector/modsecurity_engine.h`
- `common/include/msconnector/transaction_contract.h`
- `common/runtime/msconnector_runtime.c`
- `common/runtime/response_companion_transport.c`
- `common/src/modsecurity_engine.c`
- `common/src/transaction_state.c`
- `connectors/apache/src/msc_filters.c`
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.h`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/lighttpd/module/mod_msconnector.c`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/tests/test_i09_api_returns.py`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `connectors/traefik/composite_middleware/api_failure_test.go`
- `connectors/traefik/composite_middleware/middleware.go`
- `connectors/traefik/native_middleware/api_failure_test.go`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/response_observer/api_failure_test.go`
- `connectors/traefik/response_observer/observer.go`
- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/tests/test_i09_api_returns.py`
- `docs/pr-382-checklist.de.md`
- `docs/pr-382-checklist.md`
- `docs/pr-382-i09-i12-rest-matrix.de.md`
- `docs/pr-382-i09-i12-rest-matrix.md`
- `docs/pr-382-i09-route-audit.de.md`
- `docs/pr-382-i09-route-audit.md`
- `reports/audits/change-records/CR-20261011-i09-native-route-reconciliation.de.md`
- `reports/audits/change-records/CR-20261011-i09-native-route-reconciliation.md`
- `reports/audits/i09-native-route-command-evidence.de.md`
- `reports/audits/i09-native-route-command-evidence.md`
- `tests/test_apache_common_adoption.py`
- `tests/test_apache_i09_filter_events.py`
- `tests/test_apache_native_security_contract.py`
- `tests/test_apache_phase4_response_regression_wiring.py`
- `tests/test_event_transport_observation.py`
- `tests/test_haproxy_binding_phase_contract.py`
- `tests/test_haproxy_binding_refactor.py`
- `tests/test_haproxy_header_validation_contract.py`
- `tests/test_haproxy_host_native_results.py`
- `tests/test_haproxy_htx_filter_security_contract.py`
- `tests/test_haproxy_native_results.py`
- `tests/test_haproxy_spop_transaction_cache_contract.py`
- `tests/test_haproxy_transaction_contract_binding.py`
- `tests/test_i09_body_phase.py`
- `tests/test_i09_common_routes.py`
- `tests/test_i09_native_decision.py`
- `tests/test_native_api_fail_closed_contract.py`
- `tests/test_native_request_body_limit_adapter_contract.py`
- `tests/test_runtime_event_sink_failures.py`

## Commands executed

Exact commands, exits, test counts, retained failures and evidence layers: [I09 audit](../../../docs/pr-382-i09-route-audit.md#final-command-reconciliation). Final 33 compiled tests/Common C17 smoke; Common contracts 74; adoption 19 plus connector checks; HAProxy 194/12 skips; Traefik 86/4 skips; lighttpd 178/13 skips; Go race 56/30/21; native Envoy build. See the report for baseline/environment non-passes.

## Security impact

Undocumented results and failed API acknowledgements stay terminal technical failures. Original cause/phase and empty unobserved actual_action/rule_id are retained; body-limit policy stays distinct. Legitimate rule denial and memory append0/1 controls remain. Validation/authentication/isolation/default policies are not weakened.

## Runtime evidence

No live-host runtime evidence was collected or claimed. Compiled production seams, C17 translation units and native tagged Go tests prove their stated code/API layers only. External evidence root: /var/tmp/codex/ModSecurity-conector/analysis/i09-20261011.

## Known limitations

I10 host mode handling, I11 physical sinks and I12/V08–V10 live host/transport evidence remain open. Stock-native lighttpd exposes only P1/P3. HTX whole-host compilation lacks HAProxy headers. Local Sonar analysis is403 Forbidden; current-head CI/Quality Gate is not inferred from historical checks.

## Remaining risks

Live reset/client-byte/neighbor-stream/log-sink behavior and final-release validation remain unaccepted. One pre-existing Apache generated-doc wording test and the baseline Python workflow checker fail outside the product fixes.

## Checks not run and rationale

No deployment, merge, live-host/CRS/H2/H3/full runtime matrix or physical sink fault matrix. No package/header provisioning. Ruff/pytest are unavailable; Python syntax, repository-native checks and compiled tests provide applicable alternatives. Interrupted HTX C17 provisioning attempts are not passes.

## Final diff and review status

Isolated task branch is stacked on PR382 at the unchanged base revision above. Independent source review found the denial/terminal-finish cases, both confirmed and fixed with compiled controls; follow-up review found no residual material I09 gap in those paths. Framework/MRTS Gitlinks remain unchanged. Draft delivery does not imply release, Ready, CI/Quality-Gate pass or merge.

Draft CI remediation and actual follow-up checks: [command evidence](../i09-native-route-command-evidence.md). Draft PR [#408](https://github.com/Easton97-Jens/ModSecurity-conector/pull/408) is stacked on PR #382. Commit `e15f31f2b5c0aa4b9e85efbdf015985b076ff633` produced real CI failures: absent Apache/APR prerequisites, two missing temporary directories, local command paths in product documentation and 29 Sonar findings. Sonar server Quality Gate passed but repository zero-issue/zero-duplication gates failed; authenticated readback found four new duplicated lines in two Common finish-preflight blocks. The follow-up supplies CI-only prerequisites, portable temporary paths, paired audit evidence for original commands and behavior-preserving Common/HAProxy/Traefik helpers. No scanner threshold, negative test or error contract was weakened. Old-head green connector runs do not certify the follow-up head. Successful API readback commands below prove readback only, not zero findings. Unrelated generated cache reports and environment snapshot files appeared during work and are preserved outside the scoped commit.

Final CI prerequisite reconciliation: CI for `27b32df9e4b207906700f5c98bd3399941a8ca11`, lint run `38122479270`/job `114419887846`, confirmed one remaining setup error: `msc_filters.h:2:10: fatal error: modsecurity/modsecurity.h: No such file or directory`. The I09 target ran 23 methods with one Apache fixture setup error; all HAProxy fixtures passed. Add the already-used Apache CI prerequisite `libmodsecurity-dev`, keeping compilation mandatory. Exact-head Sonar check `114420352962` reported one excessive nesting issue in the Traefik poll error mapping and 0.0% new-code duplication. Extracting the poll-error mapper preserves POLLNVAL/EBADF precedence over POLLHUP/ECONNRESET and fallback EIO; five compiled controls and the actual C17 translation unit pass. Server Quality Gate success does not satisfy strict zero-finding acceptance; updated-head checks remain required.

## Apache harness linker reconciliation

For exact head `f49de8c3ca6731af9753848be75da5724a638b70`, lint run `38123028562`/job `114421500877` passed the 33-method I09 step and both strict Sonar gates. Authenticated Cloud readback/check `114421798669` reported zero new issues, accepted issues, hotspots and annotations; raw new duplication was zero lines, zero blocks and 0.0% density. The sole failed step was lightweight lint: the existing Apache RulesSet native harness had undefined `__wrap_ap_log_perror_` references in a GCC LTO object. SDK provisioning exposed this unchanged baseline check. The runner now explicitly roots the existing wrapper with `--undefined` while preserving `--wrap`, LTO, section GC, warnings and all cleanup assertions. The specific elimination mechanism is an inference: local GCC15 passed before the correction, including LTO/whole-program; only the retained hosted run is red evidence. Native default, LTO and ASAN/UBSAN runs pass after the correction, as do 51 lifecycle methods and the separate native request-cleanup harness. Independent bounded review found no material issue. Updated-head hosted verification is required; earlier-head green checks do not establish its acceptance.
