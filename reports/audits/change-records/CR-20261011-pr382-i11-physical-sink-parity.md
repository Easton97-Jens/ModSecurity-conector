# Change Record: CR-20261011-pr382-i11-physical-sink-parity

**Language:** English | [Deutsch](CR-20261011-pr382-i11-physical-sink-parity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-pr382-i11-physical-sink-parity |
| Date (UTC) | 2026-10-11 |
| Base revision | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |

Baseline: branch `fix/i11-event-sink-parity-20261011`, HEAD `0df51024008fc84f0a6820f3b011055b69c3a3e2`, `origin/master` / merge base `3019722fbda40dc281b861c1cc38085be2f430a0`. Own worktree `/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity`; clean at creation. Unrelated Parent-checkout edits were not imported. Current evidence identifies this base plus the uncommitted patch.

## Motivation and problem statement

Apache lost physical sink results in void callers; SPOP ignored fputs. The request covers I11 producer/sink parity, first cause, no retry/duplicate terminal event and no successful completion after mandatory sink failure. NGINX diagnostic return and Envoy close/writer propagation were also corrected.

## Acceptance criteria

Canonical serialization/size and I/O classes remain distinct; mandatory callers receive failure, while diagnostic events do not automatically change host status. First technical cause survives. No sink replay or duplicate host completion; truthful requested_action/actual_action; all active producers reconciled and current compiled tests passing. Current compiled acceptance is satisfied; I11 is `[x]`, without promoting I12/V10 live-host evidence.

## Implementation decision and rationale

Existing Common error taxonomy is reused, without another error model. Common source remains unchanged: sequence reservation follows the existing contract; previous_hash advances only after successful write. Adapters do not own hash/sequence commit logic. No fsync/durability claim.



### Apache

| Sink stage | before | after | error class | caller behavior | test |
| --- | --- | --- | --- | --- | --- |
| serialization | void / diagnostic | serialize before open | INTERNAL / EVENT_TOO_LARGE | mandatory fails; diagnostic retains sink error | serialization/no-file-change |
| open | warning only | typed checked secure open | IO | no success or second write | missing parent/directory/invalid target |
| write / incomplete | apr_file_puts; lost result | apr_file_write_full + exact byte count | IO | precommit fail closed; postcommit terminal filter | real OS failure + controlled APR seam |
| flush | unbuffered APR | unbuffered APR; no separate flush | not applicable | write_full and close checked | write/close controls |
| close | warning only | checked apr_file_close | IO | first contract cause preserved | controlled close failure |
| replay / terminal | result not propagated | sticky first sink failure | original retained | no new sink operation; no second response | repeat/precommit/postcommit |

### HAProxy SPOP

| Sink stage | before | after | error class | caller behavior | test |
| --- | --- | --- | --- | --- | --- |
| serialization | fputs after serializer success | typed serialize before stdio | INTERNAL / EVENT_TOO_LARGE | caller gets false + typed error | normal/invalid/oversized |
| open | caller-specific failure | checked caller open | IO | mandatory response path fails | private temporary target |
| write | unchecked fputs | fputs == EOF / ferror checked | IO | failed SPOP result; no success fallback | real stdio write failure |
| flush | unchecked buffered result | fflush checked | IO | first error retained; no retry | buffered flush-only failure |
| close | owned fclose already checked | existing checked close preserved and revalidated | IO | existing cleanup failure result retained; no sink replay | checked close seam with real cleanup |
| replay / terminal | sink success could be assumed | per-request sticky sink error | original retained | no second physical write/ACK success | caller/replay/positive control |

Caller chains: Apache producer → msconnector_event_write_jsonl_line → apache_open_event_file → apr_file_write_full → apr_file_close → typed phase/intervention callers → request/filter error path. SPOP producer → decision_log_write → bounded memory staging including phase4_common_event_write → physical fputs/ferror → fflush → SPOP processing/response error path before ACK. Existing checked owned-stream fclose runs during resource cleanup; it is not a new per-notification receipt. Already committed Apache responses are not replaced with another HTTP response. Diagnostic rule-match output alone does not force HTTP 500.

Envoy: C close invokes finish even after an earlier failure and returns its preserved class. Go cleanup reporting distinguishes transaction-local `ErrTransactionFinishPhaseSequence` from physical sink errors/unsafe cleanup requiring controlled restart. Both coordinator close paths inspect cleanup reporters; first causes remain sticky. Actual descriptor fault injection replaces an ineffective earlier fixture fault.

## Changed files

- `Makefile`
- `.github/workflows/lint.yml`
- `.github/workflows/test-apache.yml`
- `.github/workflows/test-haproxy.yml`
- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `connectors/apache/src/mod_security3.c`
- `connectors/apache/src/mod_security3.h`
- `connectors/apache/src/msc_filters.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_apache_event_sink_failures.py`
- `tests/test_apache_intervention_cleanup.py`
- `tests/test_apache_native_lifecycle.py`
- `tests/test_apache_terminal_contract_failures.py`
- `tests/test_haproxy_spop_event_sink_failures.py`
- `tests/test_haproxy_spop_selftest_cleanup_contract.py`
- `tests/test_nginx_bounded_event_uri.py`
- `tests/test_envoy_bridge_failures.py`
- `connectors/envoy/ext_proc/cmd/msconnector-composite/observer.go`
- `connectors/envoy/ext_proc/cmd/msconnector-composite/observer_test.go`
- `connectors/envoy/ext_proc/internal/composite/coordinator.go`
- `connectors/envoy/ext_proc/internal/composite/coordinator_test.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.h`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/jsonl.go`
- `connectors/envoy/ext_proc/internal/processor/jsonl_test.go`
- `docs/pr-382-checklist.md`
- `docs/pr-382-checklist.de.md`
- `docs/pr-382-i09-i12-rest-matrix.md`
- `docs/pr-382-i09-i12-rest-matrix.de.md`
- `reports/audits/change-records/CR-20261011-pr382-i11-physical-sink-parity.md`
- `reports/audits/change-records/CR-20261011-pr382-i11-physical-sink-parity.de.md`

- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_apache_common_adoption.py`
- `tests/test_haproxy_common_adoption.py`
- `tests/test_haproxy_spop_response_timeout_contract.py`
- `tests/test_nginx_common_adoption.py`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`

## Commands executed

Recorded exact commands and results from `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/*.json`. Working directory: isolated worktree, except Go under `connectors/envoy/ext_proc`. Failed intermediate runs remain visible. `not enumerated` means an unavailable test count, not zero scope. Counts are not disjoint totals. The full Envoy tagged suite exercises actual Common/libModSecurity code.

| Command | Exit | Tests | Result |
| --- | --- | --- | --- |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links` | 0 | not enumerated | PASS; repeated full documentation acceptance; `docs-acceptance-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp 'CC=clang -fsanitize=address,undefined -fno-omit-frame-pointer -g' /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_event_sink_failures tests.test_haproxy_spop_event_sink_failures tests.test_envoy_bridge_failures` | 0 | 46 | PASS; all three C fixture compilers use ASan + UBSan; `all-physical-sinks-asan-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_common_adoption tests.test_apache_native_adoption` | 0 | 28 | PASS; `apache-adoption-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_apache*.py'` | 1 | 195 | FAIL; 195 tests / 8 failures / 7 errors on unchanged base; `apache-baseline-suite.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/build/i11-apache-c17 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/i11-apache-native FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-apache-event-sink check-apache-common-adoption check-apache-c-standard-wiring check-apache-intervention-cleanup check-apache-request-transaction-cleanup check-apache-c17` | 2 | 18 | FAIL (intermediate; later rerun or baseline assessment recorded separately); `apache-native-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/build/i11-apache-c17 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/i11-apache-native FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-apache-common-adoption check-apache-c-standard-wiring check-apache-intervention-cleanup check-apache-request-transaction-cleanup check-apache-c17` | 0 | 45 | PASS; `apache-native-v2.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_apache*.py'` | 1 | 189 | FAIL (intermediate; later rerun or baseline assessment recorded separately); `apache-suite-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_apache*.py'` | 1 | 215 | FAIL (intermediate; later rerun or baseline assessment recorded separately); `apache-suite-v2.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_apache*.py'` | 1 | 215 | FAIL; 215 tests / 7 failures / 7 errors; no new failure/error sets against full base; `apache-suite-v3.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` | 0 | not enumerated | PASS; `change-record-structure-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-review/verify_changed_source.py` | 0 | not enumerated | PASS; `changed-source-format-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/i11-common FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-adapter-contracts` | 0 | not enumerated | PASS; `common-native-contracts.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_event_sink_failures tests.test_runtime_host_action_validation tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_pr382_decision_safety tests.test_pr382_profile_errors tests.test_envoy_bridge_failures` | 0 | 60 | PASS; `core-events-final-v2.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_event_sink_failures tests.test_runtime_host_action_validation tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_pr382_decision_safety tests.test_pr382_profile_errors tests.test_envoy_bridge_failures` | 0 | 59 | PASS; `core-events-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links` | 0 | not enumerated | PASS; `docs-final.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -json ./internal/processor ./cmd/msconnector-composite ./internal/composite` | 0 | 101 Go tests / 156 cases / 3 packages | PASS; `envoy-sink-go-focused-final.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -json ./internal/processor ./cmd/msconnector-composite ./internal/composite` | 0 | 104 Go tests / 163 cases / 3 packages | PASS; `envoy-sink-go-focused-reviewed.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -json ./internal/processor ./cmd/msconnector-composite ./internal/composite` | 1 | 100 Go tests / 155 cases / 2 packages | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-go-focused.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -race -json ./internal/processor ./cmd/msconnector-composite ./internal/composite` | 0 | 105 Go tests / 164 cases / 3 packages | PASS; `envoy-sink-go-race-reviewed.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -race -json ./internal/processor ./cmd/msconnector-composite ./internal/composite` | 0 | 101 Go tests / 156 cases / 3 packages | PASS; `envoy-sink-go-race.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -json -overlay=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-sink-redgreen/overlay.json -run 'Test(JSONLObserverRetains|CompositeObserverRetains|DispatcherDoesNotReplay|CoordinatorReportsCleanup)' ./internal/processor ./cmd/msconnector-composite ./internal/composite` | 1 | 0 Go tests / 0 cases / 0 packages | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-go-red-reviewed.json` |
| `rtk proxy env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu ENVOY_EXT_PROC_COMMON_TEST=1 GOFLAGS=-p=1 GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp sh connectors/envoy/build/build_ext_proc.sh` | 0 | not enumerated | PASS; `envoy-sink-native-build-final.json` |
| `rtk proxy env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu ENVOY_EXT_PROC_COMMON_TEST=1 GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp sh connectors/envoy/build/build_ext_proc.sh` | 1 | not enumerated | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-native-build-reviewed.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' go test -mod=readonly -count=1 -tags libmodsecurity -json ./...` | 1 | 213 Go tests / 313 cases / 7 packages | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-native-green-final.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' go test -mod=readonly -count=1 -tags libmodsecurity -json -p=1 ./...` | 0 | 218 Go tests / 324 cases / 8 packages | PASS; `envoy-sink-native-green-reviewed.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' go test -mod=readonly -count=1 -tags libmodsecurity -json ./...` | 1 | 213 Go tests / 314 cases / 7 packages | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-native-green-v2.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' go test -mod=readonly -count=1 -tags libmodsecurity -json -overlay=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-sink-redgreen/native-overlay.json -run 'TestCommonRuntime(CleanupFailureRetainsFirstCause|CloseReportsTerminalEventSinkFailure)' ./internal/processor` | 1 | 0 Go tests / 0 cases / 0 packages | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-native-red-reviewed.json` |
| `rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' go test -mod=readonly -count=1 -tags libmodsecurity -json -overlay=/var/tmp/codex/ModSecurity-conector/runs/i11-envoy-sink-redgreen/native-overlay.json -run 'TestCommonRuntime(CleanupFailureRetainsFirstCause|CloseReportsTerminalEventSinkFailure)' ./internal/processor` | 1 | 0 Go tests / 0 cases / 0 packages | FAIL (intermediate; later rerun or baseline assessment recorded separately); `envoy-sink-native-red.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-haproxy-common-adoption check-haproxy-c-standard-wiring` | 2 | not enumerated | FAIL (intermediate; later rerun or baseline assessment recorded separately); `haproxy-adoption-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-haproxy-common-adoption check-haproxy-c-standard-wiring check-haproxy-event-transport-contract` | 2 | not enumerated | FAIL (intermediate; later rerun or baseline assessment recorded separately); `haproxy-adoption-green.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_binding_phase_contract tests.test_haproxy_header_validation_contract tests.test_haproxy_spop_response_timeout_contract` | 1 | 20 | FAIL; unchanged-base reproduction of 5 existing failures; `haproxy-baseline-binding.json` |
| `rtk proxy env CI=true PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/i11-haproxy-c17 FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-haproxy-c17` | 2 | not enumerated | BLOCKED: Make exit 2 / native exit 77; missing HAProxy native headers, CI=true non-provisioning mode; `haproxy-c17-prerequisite-check.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-haproxy-common-adoption check-haproxy-c-standard-wiring` | 0 | not enumerated | PASS; `haproxy-native-adoption-final.json` |
| `rtk proxy cc -std=c17 -Wall -Wextra -Werror -pthread -I common/include -I connectors/haproxy/src -fsyntax-only connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | 0 | not enumerated | PASS; `haproxy-native-syntax-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_haproxy*.py'` | 1 | 198 | FAIL (intermediate; later rerun or baseline assessment recorded separately); `haproxy-suite-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -v -s tests -p 'test_haproxy*.py'` | 1 | 203 | FAIL; 5 baseline failures / 12 skips; same 5 failures reproduced by haproxy-baseline-binding; `haproxy-suite-v2.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_common_adoption tests.test_nginx_late_error_results tests.test_native_error_classification tests.test_pr382_decision_safety` | 124 | not enumerated | TIMEOUT (900 s; not PASS; all 110 adoption methods subsequently pass in four disjoint shards); `nginx-adoption-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-review/run_nginx_shard.py --index 0 --total 4` | 0 | 28 | PASS; `nginx-adoption-shard-0.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-review/run_nginx_shard.py --index 1 --total 4` | 0 | 28 | PASS; `nginx-adoption-shard-1.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-review/run_nginx_shard.py --index 2 --total 4` | 0 | 27 | PASS; `nginx-adoption-shard-2.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-review/run_nginx_shard.py --index 3 --total 4` | 0 | 27 | PASS; `nginx-adoption-shard-3.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_current_helper_aware_contract_is_accepted tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_current_projected_jsonl_pipelines_are_reported_without_traceback tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_projected_jsonl_pipeline_rejects_active_bypasses_and_decoys tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_strict_projected_jsonl_pipeline_rejects_raw_event_and_early_success tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests.test_harmless_object_macro_remains_accepted` | 0 | 5 | PASS; `nginx-checker-focused-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_bounded_event_uri tests.test_nginx_request_error_events tests.test_nginx_native_logging` | 0 | 29 | PASS; `nginx-diagnostic-green.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_bounded_event_uri` | 1 | 6 | FAIL (intermediate; later rerun or baseline assessment recorded separately); `nginx-diagnostic-red.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_event_sink_failures tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_common_adoption tests.test_haproxy_adoption_rule_id` | 0 | 50 | PASS; `physical-sinks-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp CC=clang 'APACHE_SINK_CFLAGS=-fsanitize=address,undefined -fno-omit-frame-pointer -g' 'HAPROXY_SINK_CFLAGS=-fsanitize=address,undefined -fno-omit-frame-pointer -g' 'ENVOY_BRIDGE_CFLAGS=-fsanitize=address,undefined -fno-omit-frame-pointer -g' /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_event_sink_failures tests.test_haproxy_spop_event_sink_failures tests.test_envoy_bridge_failures` | 0 | 46 | PASS; partial instrumentation: Apache only; superseded by all-physical-sinks-asan-final; `physical-sinks-sanitized-final.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_sonar_zero_gate tests.test_sonar_duplication_gate tests.test_run_native_case_sonar_helpers` | 0 | 26 | PASS; `source-quality-baseline.json` |
| `rtk proxy /root/go/bin/actionlint .github/workflows/lint.yml .github/workflows/test-apache.yml .github/workflows/test-haproxy.yml` | 0 | not enumerated | PASS; `workflow-lint-final.json` |
| `rtk proxy python3 ci/tools/new-change-record.py check` | 0 | archive | PASS: structure only |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 /var/tmp/codex/ModSecurity-conector/analysis/i11-review/check_owned_docs.py` | 0 | 3 pairs / 6 files | PASS: owned structure, switches, schema and local links only |
| `rtk git diff --check` | 0 | patch | PASS |

## Security impact

Sink failure no longer becomes successful mandatory completion. Earlier canonical technical errors remain authoritative. No validation, compiler warning, isolation, authentication or scanner requirement is weakened. Existing configuration and event schema remain intact.

## Runtime evidence

Compiled function/contract tests exercise production C functions with controlled APR/stdio injection; Go tests exercise writers and propagation. These are not new physical Apache/HAProxy/Envoy host runs. R16/R17 remain historical downstream NGINX-H1 evidence for their own revisions.

## Known limitations

Documentation environment: the initial full check was blocked by 22 unchanged Framework links. A fixture exported from the exact pinned Framework revision was subsequently installed in the isolated worktree; full bilingual, runtime-path and link checks pass (`docs-final.json`). Original Framework checkout and gitlink remain unchanged; MRTS remains read-only. This fixture is test setup, not a Framework product change.

I12/V10 live-host/physical-host evidence remains open. No persistence promise beyond successful write/flush/close API outcomes. Already sent bytes cannot be taken back. Stock lighttpd control route and unsupported host actions retain their boundaries.

## Remaining risks

I11 code: no known implementation gap after final independent review. Current integrated evidence: physical sink tests 50, Common/event regressions 60, fully instrumented C ASan/UBSan tests 46, Apache native/C17 45 and adoption 28, Envoy native/tagged 218 tests/324 cases/8 packages and race 105/164/3 pass. All 110 NGINX adoption methods pass in four disjoint shards of 28+28+27+27 tests. Bilingual/path/link, workflow, format and Change Record checks pass. Broad Apache suite: current patch 215 tests, 7 failures/7 errors; unchanged base 195 tests, 8 failures/7 errors. No new failure/error sets; the earlier precommit_rate_limit fixture failure now passes. Three UID/chown environment errors occur on both revisions. HAProxy suite: 203 tests, five failures reproduced on base, twelve skips. Neither broad suite is claimed fully green. I12/V10: real host action and physical host evidence remain separately open. Protected CI, secret scan and server Sonar for this patch are not claimed here. Environment: HAProxy C17 is blocked by missing native headers (native exit 77, Make 2); no automatic provisioning. Broad baseline/environment failures are not removed by weakening tests.

## Checks not run and rationale

No new live-host/H2/H3/CRS/production runs for this local sink patch. The existing `memcheck-nginx` target and installed Valgrind are available, but were not run without prepared host setup. HAProxy C17 was attempted and remains blocked by missing native headers; no toolchain/package installation. Protected Exact-Head CI, secret scan and server Sonar remain independently open. Executed local focused acceptance, sanitizer, adoption, race, format and documentation gates pass; broad suites retain the recorded baseline/environment failures.

## Final diff and review status

Local final diff and independent review complete: no findings; I11 implementation acceptance satisfied. The subsequently authorized stacked Draft PR on PR #382 is delivered by the root task; new head SHA and PR link are bound in the external delivery report only after actual creation. Current identity: base plus reviewed working-tree patch. No merge, history rewrite or deployment. Authorized five-part commit split: Apache; HAProxy SPOP; Envoy; NGINX; shared CI/Make integration and synchronized EN/DE documentation. Full diff and test artifacts remain available for review.

I11 IMPLEMENTATION COMPLETE – remaining live-host evidence belongs to I12/V10
