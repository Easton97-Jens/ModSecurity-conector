# Change Record: CR-20261012-pr409-base-refresh

**Language:** English | [Deutsch](CR-20261012-pr409-base-refresh.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261012-pr409-base-refresh |
| Date (UTC) | 2026-10-12 |
| Base revision | `1e7f7c8405ddcc7fc4a5ff117ef45c5bf0686707` |

## Motivation and problem statement

PR #409 at `caafe7ecec1a91669cbb82cea18b2b97309cde44` conflicted with its updated PR #382 base. The base now includes I09 (#408), I11 (#406), and engine-owned request/response body policy (#407). The user requested updating this PR and checking it again in the existing separate worktree. Origin/master stays `3019722fbda40dc281b861c1cc38085be2f430a0`; original delivery base was `498653c2a193d34b7b25b2903b1e4db1c45e7f73`. Initial task tree was clean. PR #409 is now ready for review (`draft=false`), the observed state retained by this update.

## Acceptance criteria

- Preserve published history while incorporating initial refreshed base `d94a7a38b90bc56b828d70f7df8794e12fd21e10` and the subsequent current base `1e7f7c8405ddcc7fc4a5ff117ef45c5bf0686707`; do not merge the PR into its base/master.
- Resolve all 18 integration conflicts without losing I09/I10/I11 or engine-owned body policy.
- Preserve exact-one, first technical cause, terminal reentry, truthful host observations and once-only cleanup.
- Execute current caller/native/mutation/SDK/regression/lint/docs checks; retain failed attempts and skipped checks explicitly.
- Deliver current-SHA checks and Sonar readback; old-head success is historical evidence only. I12 host/client/transport acceptance remains separate.

## Implementation decision and rationale

Integrate the newer base with a normal merge commit into the task branch; no rebase, amendment or force-push. Common HTTP authorization retains the new incremental request stream while requiring exactly one for begin, buffered/socket append, EOS, companion handoff and finish. The fixture checks canonical error codes so a later IO error with the same HTTP status cannot mask the primary cause; a deterministic POST supplies its byte only after headers, exercising the real socket-loop append.

Envoy combines the canonical four-argument checked close/observed-close and separate finish classification with the compatible void ABI, first-cause and commitment guards. HAProxy preserves typed native errors, I11 sinks and I10 host latches; SPOP technical failures remain disruptive503 even in detect-only/open. Traefik retains streaming and terminal latches, checks the new commit callback exactly once, and tests the intended ErrAbortHandler outcomes. Native and stock lighttpd retain request-stream/spool APIs and current engine-owned limits. Existing compiled fixtures now target the actual signatures and valid SPOP framing; assertions and negative controls are retained.

Real SDK loopback testing exposed three sidecar resets after queued/rejected input: removing every worker shutdown avoided duplicates but omitted graceful completion. Each exchange now stores shutdown attempt and observed success. All stop paths share that latch, never retry failed shutdown, and normal final stop happens after snapshots/receipts without inventing a HostAction. Failed decision delivery always enters the technical failure path.

The immediate client-RST regression also failed on the unchanged exact base, before transaction admission. A test-only --wrap=send pipe gate now synchronizes at the real HTTP418 write after native P2; no sleep or production hook. This exposed a genuine missing ConnectorError: a terminal prospective RuleDecision prevented explicit technical failure, and its existing terminal-event latch suppressed the new event. A fail-only correlated-rule transition now clears actionable rule metadata while remaining TERMINAL. Generic decision mutability is unchanged; BODY_LIMIT, prior causes and cleanup stay protected. Runtime rejects conversion after accepted host action or finish, replays physical IO failures, and resets the event latch once. Productive native ordering completes P2 before RuleDecision, preserving the technical event phase. The test asserts the current flat canonical event schema, error status, empty rule/action, no invented abort and zero upstream requests.

I09/I10/I11 closure and all historical route evidence remain distinct; the four paired checklist/matrix files retain 14 productive I10 legs and 56 historical rows. Updated source tests use actual function definitions instead of requiring recursion or obsolete helpers. The HTX path-security fixture supplies the newly required explicit engine policy, preserving path/symlink guards.

First pushed integration head `e4c4f2a6` passed the normal Cloud gate but full authenticated readback found two c:S3776 CODE_SMELL findings: HTTP authorization complexity26 versus25 and sidecar exchange27 versus25. Mandatory zero-findings enforcement correctly rejected it; duplication was0.0%. Narrow helper extraction separates streamed authorization error mapping and Strict sidecar completion, preserving all guards, callbacks, terminal state and observations. Productive Common11 and full lighttpd51 SDK/caller/mutation tests pass again. No scanner/gate/threshold change or suppression. Current-head CI/Sonar readback is recorded in the PR after ordinary follow-up push.

During the final audit PR382 advanced again to `1e7f7c84`, incorporating master #411. Its30-file CI/tool/documentation/test delta merged without conflicts and leaves all Common/connector product source unchanged from independently reviewed `35a7b0a9`. All I10 targets and the new tool pins/NGINX producer-snapshot handoff are retained. Full authenticated Sonar readback for35a reports zero findings and its mandatory scaffold-lint passed; this is historical once the second merge is pushed. The new CI-security contract exposed three upload-artifact references in the protected exact-head workflow that were already stale in exact base1e7. Align them with the existing central locked v7.0.2 SHA; retain all workflow guards, permissions, isolation and tests. No new dependency choice or scanner weakening.

Local Make lint also exposed a base integration gap: it still called raw installed actionlint, which rejected the new self-repository syntax. A separate installed-tool adapter reuses the existing safe in-memory normalizer and fixed workflow discovery. It preserves the previous PATH tool selection, default ShellCheck behavior, unchanged source and all failure/timeout outcomes; no tool/file override, download or installation. Strict security/candidate tool staging and guards are unchanged. Eleven adapter methods and actual installed-actionlint execution pass; affected local checks are recorded below.

The first ordinary push of local merge `c7361835` was safely rejected because a concurrent publisher had added `9b2ef717`, an equivalent PR382-base merge. Its delta contains exactly the already inspected30-file base change and no extra product edits. A normal task-branch merge preserves that published commit and our tested corrections; the merged source tree matchesc736 before this paired record note. No force-push, rebase or discarded foreign work.

Current8e CI exposed one further integration defect: actionlint job114944636231/run38289128723 failed when real updater validation copied a private proposed tree without the newly imported installed-lint adapter. Add that regular file to the existing read-only baseline inventory; updater publication authority, symlink guards, tool selection and assertions are unchanged. The complete updater module now passes46 top-level tests in196.608s, including actual proposed-tree CI-security contract execution. The earlier local281-method target selected the nonrecursive test class and did not execute this integration test; its PASS was not proof of the omitted layer. Failed hosted log and exact-SHA Sonar readback (zero findings) are retained; Sonar8e remains historical after corrective push.

## Changed files

- `.github/workflows/test-common.yml`
- `.github/workflows/run-protected-nginx-exact-head.yml`
- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-haproxy.yml`
- `.github/workflows/test-lighttpd.yml`
- `.github/workflows/test-traefik.yml`
- `Makefile`
- `ci/tools/lint_installed_workflows.py`
- `ci/tools/update-workflow-tools.py`
- `common/runtime/http_authorization_service.c`
- `common/runtime/msconnector_runtime.c`
- `common/runtime/response_companion_transport.c`
- `common/src/transaction_state.c`
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main_test.go`
- `connectors/envoy/ext_proc/internal/compositeenvoy/server.go`
- `connectors/envoy/ext_proc/internal/compositeenvoy/technical_error_test.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `connectors/envoy/ext_proc/internal/processor/technical_error_test.go`
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.h`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/lighttpd/module/mod_msconnector.c`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/tests/test_i09_api_returns.py`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `connectors/traefik/native_middleware/api_failure_test.go`
- `connectors/traefik/native_middleware/engine_uds.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/middleware_test.go`
- `connectors/traefik/native_middleware/technical_error_test.go`
- `connectors/traefik/response_observer/observer.go`
- `connectors/traefik/response_observer/observer_test.go`
- `connectors/traefik/src/traefik_engine_service.c`
- `docs/pr-382-checklist.de.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/pr-382-checklist.md`
- `docs/pr-382-i09-i12-rest-matrix.de.md`
- `docs/pr-382-i09-i12-rest-matrix.md`
- `reports/audits/change-records/CR-20261011-pr382-i10-adapter-errors.de.md`
- `reports/audits/change-records/CR-20261011-pr382-i10-adapter-errors.md`
- `reports/audits/change-records/CR-20261012-pr409-base-refresh.de.md`
- `reports/audits/change-records/CR-20261012-pr409-base-refresh.md`
- `tests/fixtures/lighttpd_i10_native.c`
- `tests/fixtures/lighttpd_i10_sidecar.c`
- `tests/haproxy_i10_binding_caller_test.c`
- `tests/haproxy_i10_host_caller_test.c`
- `tests/haproxy_i10_spop_caller_test.c`
- `tests/test_apache_fail_closed.py`
- `tests/test_haproxy_binding_phase_contract.py`
- `tests/test_haproxy_header_validation_contract.py`
- `tests/test_haproxy_host_native_results.py`
- `tests/test_haproxy_htx_filter_security_contract.py`
- `tests/test_haproxy_htx_transaction_id.py`
- `tests/test_haproxy_i10_binding_callers.py`
- `tests/test_haproxy_i10_host_callers.py`
- `tests/test_haproxy_spop_config_security_contract.py`
- `tests/test_haproxy_spop_event_sink_failures.py`
- `tests/test_i10_envoy_finish.py`
- `tests/test_i10_envoy_mutations.py`
- `tests/test_i10_service_callers.py`
- `tests/test_lint_workflows.py`
- `tests/test_lighttpd_i10_adapter_errors.py`
- `tests/test_native_api_fail_closed_contract.py`
- `tests/test_runtime_rule_delivery_failure.py`
- `tests/test_traefik_i10_dispatcher.py`
- `tests/test_traefik_i10_mutations.py`
- `tests/traefik_i10_dispatcher_test.c`

## Commands executed

All commands ran through RTK with task-owned external build/cache/temp roots and the installed Parent Python environment. Exact cwd and selected nonsecret environment accompany each run. Python counts are methods, Go counts are packages; skips and earlier failed runs are not executed PASS. Earlier combined failures stopped subsequent Make targets; passing focused replacements are recorded separately.

| Exact command | Exit | Count | Seconds | Run / evidence |
| --- | --- | --- | --- | --- |
| `rtk proxy make check-i10-adapter-errors` | 0 | Python 28; Go packages 10 | 344.819 | `evidence/all-i10-callers/` |
| `rtk proxy make check-apache-c17 check-nginx-c17 NGINX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/i10-20261011/prerequisites/nginx-1.31.6` | 0 | Python 0 | 22.791 | `evidence/apache-nginx-native/` |
| `rtk proxy make check-i09-native-routes check-apache-event-sink check-haproxy-spop-event-sink check-apache-native-response-limit` | 2 | Python 33 | 41.079 | `evidence/base-i09-i11-policy/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_native_api_fail_closed_contract tests.test_engine_response_limits tests.test_removed_phase4_body_limit tests.test_phase4_all_connector_budget tests.test_haproxy_binding_phase_contract tests.test_haproxy_htx_filter_security_contract tests.test_haproxy_header_validation_contract tests.test_haproxy_binding_refactor tests.test_haproxy_spop_peer_isolation_contract tests.test_envoy_bridge_failures tests.test_traefik_engine_service_contract` | 0 | Python 109 | 23.034 | `evidence/base-native-policy-final/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarLoopbackContractTest.test_client_reset_during_a_rule_block_does_not_invent_an_abort_host_action` | 1 | Python 1 | 12.412 | `evidence/base-rst-rule-control/` |
| `rtk proxy make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-flow-integrity` | 0 | Python 0 | 6.139 | `evidence/common-current-contracts/` |
| `rtk proxy make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-flow-integrity` | 0 | Python 0 | 5.689 | `evidence/common-delivery-contracts/` |
| `rtk proxy make check-i10-common-callers` | 0 | Python 11 | 37.751 | `evidence/common-late-rule-final/` |
| `rtk proxy make check-i10-common-callers` | 0 | Python 6 | 21.402 | `evidence/common-stream-callers/` |
| `rtk proxy make check-i10-common-callers` | 0 | Python 6 | 28.932 | `evidence/common-stream-final/` |
| `rtk proxy make check-i10-common-callers` | 2 | Python 6 | 32.336 | `evidence/common-stream-mutations/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_pr382_profile_errors tests.test_pr382_decision_safety tests.test_apache_fail_closed tests.test_apache_native_lifecycle tests.test_apache_terminal_contract_failures tests.test_apache_event_sink_failures tests.test_apache_native_response_limit tests.test_nginx_late_error_results` | 0 | Python 79 | 13.192 | `evidence/core-retained/` |
| `rtk proxy make -C connectors/envoy test-envoy-ext-proc` | 0 | Python 0; Go packages 16 | 11.97 | `evidence/envoy-native-delivery-final/` |
| `rtk proxy make -C connectors/envoy test-envoy-ext-proc` | 0 | Python 0; Go packages 16 | 71.092 | `evidence/envoy-native-final/` |
| `rtk proxy make check-bilingual-docs check-doc-links` | 0 | Python 0 | 14.566 | `evidence/final-docs/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_native_api_fail_closed_contract tests.test_engine_response_limits tests.test_removed_phase4_body_limit tests.test_phase4_all_connector_budget tests.test_haproxy_binding_phase_contract tests.test_haproxy_htx_filter_security_contract tests.test_haproxy_header_validation_contract tests.test_haproxy_binding_refactor tests.test_haproxy_spop_peer_isolation_contract tests.test_envoy_bridge_failures tests.test_traefik_engine_service_contract connectors.lighttpd.tests.test_stock_sidecar_contract` | 1 | Python 127 | 39.792 | `evidence/frozen-source-contracts/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_haproxy_*.py'` | 1 | Python 219 | 134.946 | `evidence/haproxy-full/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_haproxy_*.py'` | 0 | Python 238; skipped 12 | 126.532 | `evidence/haproxy-full-final/` |
| `rtk proxy make check-i09-native-routes check-apache-event-sink check-haproxy-spop-event-sink` | 0 | Python 72 | 20.944 | `evidence/i09-and-sinks-final/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lighttpd_i10_adapter_errors connectors.lighttpd.tests.test_i09_api_returns connectors.lighttpd.tests.test_stock_sidecar_contract` | 1 | Python 0 | 0.368 | `evidence/lighttpd-final/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lighttpd_i10_adapter_errors connectors.lighttpd.tests.test_i09_api_returns connectors.lighttpd.tests.test_stock_sidecar_contract` | 0 | Python 51 | 50.744 | `evidence/lighttpd-owned-delivery-final/` |
| `rtk proxy make lint` | 0 | Python 304 | 175.022 | `evidence/lint-current/` |
| `rtk proxy make lint` | 0 | Python 304 | 171.891 | `evidence/lint-delivery-final/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarLoopbackContractTest.test_client_reset_during_a_rule_block_does_not_invent_an_abort_host_action` | 1 | Python 1 | 14.377 | `evidence/rule-delivery-native-reproducer/` |
| `rtk proxy make check-apache-event-sink check-haproxy-spop-event-sink check-apache-native-response-limit` | 2 | Python 20 | 7.363 | `evidence/sink-regressions/` |
| `rtk proxy make check-apache-event-sink check-haproxy-spop-event-sink check-apache-native-response-limit` | 0 | Python 48 | 10.856 | `evidence/sink-regressions-final/` |
| `rtk proxy /usr/local/bin/sonar-with-env list issues -p Easton97-Jens_ModSecurity-conector --pull-request 409 --new-code --page-size 500 --page 1 --format json` | 0 | Python 0 | 1.478 | `evidence/sonar-current-readback/` |
| `rtk proxy make check-i10-common-callers` | 0 | Python 11 | 38.104 | `evidence/sonar-refactor-common/` |
| `rtk proxy make check-bilingual-docs check-doc-links` | 0 | Python 0 | 14.012 | `evidence/sonar-refactor-docs/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lighttpd_i10_adapter_errors connectors.lighttpd.tests.test_i09_api_returns connectors.lighttpd.tests.test_stock_sidecar_contract` | 0 | Python 51 | 50.655 | `evidence/sonar-refactor-lighttpd/` |

Additional worker evidence under `native-worker/` and `go-worker/`: HAProxy7 caller methods/22 detected mutants; lighttpd original479 cases and9 mutants retained, with new socket-owner controls and a tenth mutant; Traefik dispatcher690 failures/690 terminal reentries/270 valid controls in admitted modes and15 C/Go mutants; Envoy18 compiled bridge/finish checks plus8 genuine Common/libModSecurity/CGo packages. New Common delivery regression has5 methods,12 rule cases,6 sealed-lifecycle negatives,4 first-cause/physical-IO cases and2 detected source mutations. Common HTTP matrix360 negative cases plus120 MRC1 failures and6 compiled mutations. Strict remains admitted only where current registry allows it. No compiler warning or assertion was weakened.

Second-base evidence follows. The first two CI-contract runs exposed upload/download pin mismatches; the first lint run exposed raw-actionlint syntax incompatibility. Final281-method CI contracts passed with5 existing user-identity/mount/PID-namespace skips, final304-method lint passed, and all11 adapter methods plus real installed-tool and3 NGINX handoff checks passed. Full exact-base inventory found6 stale artifact references (3 upload v7.0.2 /3 download v8.0.2); all now match the existing central lock. The Sonar-final-readback row is bound to35a and historical for the second merge; current delivery proof follows its new push.

| Exact command | Exit | Count | Seconds | Run / evidence |
| --- | --- | --- | --- | --- |
+| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_lint_workflows` | 0 | Python 11 | 0.519 | `evidence/second-base-actionlint-adapter/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m ci.tools.lint_installed_workflows` | 0 | Python 0 | 20.207 | `evidence/second-base-actionlint-real/` |
| `rtk proxy make check-ci-security-contract` | 2 | Python 278; skipped 5 | 164.904 | `evidence/second-base-ci-contract/` |
| `rtk proxy make check-ci-security-contract` | 0 | Python 281; skipped 5 | 166.317 | `evidence/second-base-ci-contract-complete/` |
| `rtk proxy make check-ci-security-contract` | 2 | Python 278; skipped 5 | 165.603 | `evidence/second-base-ci-contract-final/` |
| `rtk proxy make lint` | 2 | Python 304 | 172.935 | `evidence/second-base-lint/` |
| `rtk proxy make lint` | 0 | Python 304 | 177.216 | `evidence/second-base-lint-final/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_exact_head_runtime_handoff` | 0 | Python 3 | 6.941 | `evidence/second-base-nginx-handoff/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_all_remote_actions_are_immutable_sha_pins` | 1 | Python 1 | 0.317 | `evidence/second-base-pin-diagnosis/` |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_all_remote_actions_are_immutable_sha_pins` | 0 | Python 1 | 0.469 | `evidence/second-base-pin-final/` |
| `rtk proxy /usr/local/bin/sonar-with-env list issues -p Easton97-Jens_ModSecurity-conector --pull-request 409 --new-code --page-size 500 --page 1 --format json` | 0 | Python 0 | 1.422 | `evidence/sonar-final-readback/` |

| Exact command | Exit | Count | Seconds | Run / evidence |
| --- | --- | --- | --- | --- |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.ci_security.test_update_workflow_tools` | 0 | Python 46, including real proposed-tree baseline | 196.608 | `evidence/updater-full-final/` |

## Security impact

The update preserves fail-closed/terminal technical failures and separates prospective rule decisions from failed host delivery. A client reset cannot leave a false rule-only technical completion. The observed missing-event defect does not demonstrate an enforcement bypass. Shutdown success is bounded socket-owner evidence, not proof of live client reset or neighbor-stream impact. No scanner rule, exclusion, suppression, gate, authentication, profile admission, warning flag or dependency contract changed.

## Runtime evidence

The real libModSecurity3.0.14 sidecar loopback suite executes task-local sockets, native rules and private event/receipt files, including a controlled client RST at the productive send boundary. This is scoped sidecar regression evidence, not an all-route I12 campaign. Compiled fixtures and Go/CGo tests prove only their exercised caller/API/event layer. Original PR implementation history is in [the earlier Change Record](CR-20261011-pr382-i10-adapter-errors.md); it is not current-head evidence.

## Known limitations

Installed local Python3.14.4/Go1.27.2 differ from pinned3.14.7/1.27.1. Existing SDKs and retained task-owned native sources were selected explicitly; no install or system mutation occurred. Skips and historical failed attempts stay visible in the ledger. Baseline RST scheduling failure is recorded separately from the validated deterministic Common completion defect. Static review also noted pre-existing void composite Finish behavior: it can return nil in the current RPC while coordinator failure aborts sessions, rejects admission and propagates through its process owner; this was not demonstrated as a new exploitable defect.

## Remaining risks

I12/V08–V10 full host/client/reset/neighbor-stream evidence remains open. I09/I10/I11 code/evidence closures belong to their scoped revisions and checked boundaries. At commit preparation the new-head hosted CI/Sonar cannot yet have run; PR description and external final-delivery evidence carry the terminal current-head readback. No human review was present at initial readback.

## Checks not run and rationale

No all-route live-host/client/neighbor-stream campaign, deployment, PR/master merge, dependency installation, full matrix export, or destructive cleanup. No exact local pinned patch-version toolchain run because those versions are absent. The baseline verification worktree stays detached at the exact base; Framework/MRTS and their gitlinks remain unchanged.

## Final diff and review status

Independent source review covered Common, Envoy, Traefik and bounded HAProxy/lighttpd overlap; no new unresolved material finding remains in that reviewed surface after the narrow Common correction. Its real-SDK/compiled acceptance is recorded above. Final source diff, whitespace, EN/DE, current base ancestry, local/remote/PR equality, review threads and all hosted checks must be read again for the pushed SHA; earlier green CI is not promoted. PR ready state retained; no merge into its base/master. Worktrees and full evidence are retained externally.
