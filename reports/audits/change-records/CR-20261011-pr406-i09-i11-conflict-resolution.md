# Change Record: CR-20261011-pr406-i09-i11-conflict-resolution

**Language:** English | [Deutsch](CR-20261011-pr406-i09-i11-conflict-resolution.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-pr406-i09-i11-conflict-resolution |
| Date (UTC) | 2026-10-11 |
| Base revision | `6a79efe7d571d9fc980f970a08073d6334c36a7a` |

## Motivation and problem statement

PR #406 conflicted with its stacked PR #382 base after I09 native API/error-route reconciliation. A plain choice of either branch would discard I09 first-error checks or I11 checked physical-sink propagation. Preserve the published user merge `6a79efe7d571d9fc980f970a08073d6334c36a7a` and integrate base `492663334d89428dce084792145ef94e91579788` with a normal merge commit.

## Acceptance criteria

All five merge conflicts are resolved; Apache prevents successful reentry after either contract or sink failure; SPOP routes new technical error events through checked serializers and physical sinks, preserves the native first cause, and suppresses ACK/replay after a mandatory sink failure. Existing bool serializer callers retain their contract. Paired documents preserve historical evidence and open host acceptance. Fresh local validation and independent review precede normal task-branch delivery; current-head GitHub/Sonar checks are verified separately after push.

## Implementation decision and rationale

Combine Apache guards with OR and retain typed writer returns plus I09 unobserved `actual_action=""`. Stage SPOP technical records before physical I/O, distinguish successful omission from serialization failure with additive checked APIs, and keep existing bool wrappers. Preserve the locked first-error latch across bridge tasks and cleanup. Restore a post-finish checked event write for request-only native finish errors: moving initial logging before finish had otherwise omitted the new I09 terminal producer. Extract a small bridge flush helper without changing lock ownership. Freshly rebuild Common for Envoy rather than linking an archive compiled against the previous structure layout. Fresh Cloud analysis of merge `3f177376` identified c:S3776 in the combined response function (26 versus 25); extract only its native finish/error-write block into the seven-parameter `finish_production_response_transaction` helper. Keep the abort condition, phase argument, typed first cause, consumed transaction and checked write order unchanged; no suppression or gate change.

## Changed files

Manual resolutions/adaptations: `connectors/apache/src/msc_filters.c`; Apache adoption checker/test and `tests/test_apache_i09_filter_events.py`; `connectors/haproxy/src/haproxy_modsecurity_binding.c`, its header and SPOP runtime; HAProxy native/host/sink/timeout fixtures; the EN/DE checklist, remaining-work matrix and historical I09 audit; this paired record. The merge also inherits the I09 base changes and their [I09 record](CR-20261011-i09-native-route-reconciliation.md). Earlier I11 implementation remains traced by the [I11 record](CR-20261011-pr382-i11-physical-sink-parity.md). No Framework/MRTS or Gitlink changes. The Sonar follow-up also updates `tests/test_haproxy_spop_transaction_cache_contract.py` to trace the actual extracted helper.

## Commands executed

Each command below actually ran against the integration checkout. The initial integrated 68-test and broad 215-test runs preceded the final request-finish correction; the `-final` runs verify the final source. Counts overlap and are not a total of unique tests.

Final local results: integrated 70 tests; broad HAProxy 217 tests with 12 documented skips; focused HAProxy 43 and ASan/UBSan 26 tests; runtime sink 8 tests; Apache C17/adoption 20 tests; fresh Envoy native build/tests across 8 packages and native race 142 top-level tests/228 cases/3 packages. Common C17/SDK/security/flow/memory, 26 Python syntax/6 Go formatting files, workflow lint, bilingual/path/link and Change Record structure checks passed.

Sonar follow-up controls pass: 43 focused tests, 26 ASan/UBSan tests, 3 cache contracts, 26 binding function tests and strict C17 syntax. The initial cache contract failed because it expected the now-extracted finish call inline; its replacement follows the real helper and preserves/strengthens the checks. A pytest attempt could not run because pytest is absent; all 26 binding test functions were executed successfully through unittest instead, without installation. Failed attempts remain in the table.

| Exact command / Exakter Befehl | Exit | Receipt / Beleg |
| --- | --- | --- |
| `rtk proxy env CI=true MODSECURITY_INCLUDE_DIR=/usr/include APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-apache-c17 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-apache-c17 check-apache-common-adoption` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/apache-c17-adoption.json` |
| `rtk proxy python3 ci/tools/new-change-record.py check` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/change-record-structure.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/verify_changed_source.py` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/changed-source-format.json` |
| `rtk proxy env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-common TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-flow-integrity check-common-memory-safety` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/common-native-contracts.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/docs-acceptance.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/docs-staged-final.json` |
| `rtk proxy env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-envoy-native-build MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu ENVOY_EXT_PROC_COMMON_TEST=1 GOFLAGS=-p=1 GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp sh connectors/envoy/build/build_ext_proc.sh` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/envoy-native-build.json` |
| `rtk proxy env CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' GOFLAGS=-p=1 GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -race -tags libmodsecurity -json -p=1 ./internal/processor ./internal/responseobserver ./internal/composite` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/envoy-native-race.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_haproxy*.py' -v` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/haproxy-broad-final.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_haproxy*.py' -v` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/haproxy-broad.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-i09-native-routes check-apache-event-sink check-haproxy-spop-event-sink` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/i09-i11-integrated-final.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-i09-native-routes check-apache-event-sink check-haproxy-spop-event-sink` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/i09-i11-integrated.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_event_sink_failures` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/runtime-event-sink.json` |
| `rtk proxy /root/go/bin/actionlint .github/workflows/lint.yml .github/workflows/test-apache.yml .github/workflows/test-haproxy.yml` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/workflow-lint.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_native_results tests.test_haproxy_host_native_results tests.test_haproxy_common_adoption tests.test_haproxy_spop_response_timeout_contract` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-i09-i11-request-finish-focused.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp 'CC=clang -fsanitize=address,undefined -fno-omit-frame-pointer' /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_native_results tests.test_haproxy_host_native_results` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-i09-i11-request-finish-sanitizers.json` |
| `rtk proxy cc -std=c17 -Wall -Wextra -Werror -pthread -I common/include -I connectors/haproxy/src -fsyntax-only connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-i09-i11-request-finish-syntax.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -c 'import unittest; import tests.test_haproxy_transaction_contract_binding as module; suite=unittest.TestSuite(unittest.FunctionTestCase(function) for name,function in vars(module).items() if name.startswith("test_") and callable(function)); result=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(0 if result.wasSuccessful() else 1)'` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-binding-functions.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_haproxy_transaction_contract_binding.py` | 1 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-binding-pytest.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_transaction_cache_contract` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-contracts-v2.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_transaction_cache_contract tests.test_haproxy_transaction_contract_binding` | 1 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-contracts.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_native_results tests.test_haproxy_host_native_results tests.test_haproxy_common_adoption tests.test_haproxy_spop_response_timeout_contract` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-focused.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp 'CC=clang -fsanitize=address,undefined -fno-omit-frame-pointer' /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_native_results tests.test_haproxy_host_native_results` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-sanitizers.json` |
| `rtk proxy cc -std=c17 -Wall -Wextra -Werror -pthread -I common/include -I connectors/haproxy/src -fsyntax-only connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-response-finish-sonar-syntax.json` |

## Security impact

Preserve failure classification and first-cause retention; no test, compiler warning, CI, isolation or Quality Gate is weakened. New technical events cannot silently bypass the checked sink on the reviewed request/response/bridge paths. Existing unobserved host actions remain empty. No credential or raw request/body data is added to evidence.

## Runtime evidence

No runtime evidence was collected or claimed. Compiled production-function fixtures exercise controlled real file-descriptor write/flush faults, state retention, cleanup and ACK suppression. These are bounded local tests, not a live HAProxy/Apache/Envoy host or client-visible transport claim.

## Known limitations

The broad HAProxy suite skips twelve cases: eleven cross-identity staging fixtures need mapped identities/setpriv, and one needs an explicitly built SPOP runtime and registered temporary root. Full HTX host-header compilation and exact-revision live host/companion validation were not performed. I10, I12 and V08–V10 remain open. The historical local I09 Sonar 403 is not a statement about current-head Cloud analysis.

## Remaining risks

Independent review noted an inherited Common typed-CANCEL path using a void fail callback: ownership-release acknowledgement and mandatory-sink failure reporting remain separate API semantics. Its wire behavior was not tested, and this merge does not change that baseline Common callback contract. No claim of complete live-host or release acceptance follows from the local results.

## Checks not run and rationale

No live-host matrix, H2/H3, CRS/Off, deployment or client transport experiment was run for this conflict resolution. No packages, toolchains or system services were changed. Current-head CI and Sonar require the pushed SHA and are recorded in PR #406 and external delivery evidence, rather than inferred from the original I11/I09 heads.

## Final diff and review status

The resolution and minimal Sonar follow-up were independently reviewed against their exact parent changes. The request-finish producer gap is closed with checked writes and compiled positive/fault controls; a controlled red variant confirms the missing event before the correction. Merge `3f177376` preserves both published parents and was pushed normally; GitHub confirms mergeable. Source/index/marker/whitespace checks and paired documents passed. The follow-up helper preserves finish/abort/phase/first-error/ACK semantics and strengthens the helper-traced source contract; current-head delivery after its normal follow-up push is recorded separately. No PR merge or history rewriting.
