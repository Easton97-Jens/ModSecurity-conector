# Change Record: CR-20261011-pr382-i11-physical-sink-parity

**Sprache:** [English](CR-20261011-pr382-i11-physical-sink-parity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-pr382-i11-physical-sink-parity |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |

Ausgangslage: branch `fix/i11-event-sink-parity-20261011`, HEAD `0df51024008fc84f0a6820f3b011055b69c3a3e2`, `origin/master` / merge base `3019722fbda40dc281b861c1cc38085be2f430a0`. Eigener Worktree `/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity`; beim Start sauber. Fremde Änderungen im Parent-Checkout wurden nicht übernommen. Aktuelle Nachweise beziehen sich auf diese Basis plus den noch nicht committed Patch.

## Motivation und Problemstellung

Apache verlor physische Sink-Ergebnisse in void-Aufrufern; SPOP ignorierte fputs. Der Auftrag umfasst I11-Producer-/Sink-Parität, erste Fehlerursache, kein Retry/dupliziertes Terminalevent und keine erfolgreiche Completion nach verpflichtendem Sinkfehler. Zusätzlich wurden NGINX-Diagnosereturn und Envoy-Close-/Writer-Fehlerweitergabe korrigiert.

## Akzeptanzkriterien

Kanonische Klassen für Serialisierung/Größe und I/O bleiben unterscheidbar; verpflichtende Caller erhalten Fehler, diagnostische Events ändern nicht pauschal Hoststatus. Erste technische Ursache bleibt erhalten. Keine Sink-Wiederholung oder doppelte Hostcompletion; wahrheitsgemäße requested_action/actual_action; alle aktiven Producer abgeglichen und aktuelle kompilierte Tests bestanden. Die aktuelle kompilierte Akzeptanz ist erfüllt; I11 ist `[x]`, ohne I12/V10-Live-Host-Nachweise aufzuwerten.

## Implementierungsentscheidung und Begründung

Bestehende Common-Fehlertaxonomie wird verwendet, kein zweites Fehlermodell. Common-Source bleibt unverändert: Sequence-Reservierung folgt bestehendem Vertrag; previous_hash wird erst nach erfolgreichem Write fortgeschrieben. Adapter besitzen keine eigene Hash-/Sequence-Commitlogik. Keine fsync-/Durability-Zusage.



### Apache

| Sink-Stufe | vorher | nachher | Fehlerklasse | Caller-Verhalten | Test |
| --- | --- | --- | --- | --- | --- |
| Serialisierung | void / diagnostisch | Serialisierung vor Open | INTERNAL / EVENT_TOO_LARGE | verpflichtend: Fehler; diagnostisch: Sinkfehler erhalten | Serialisierung/Datei unverändert |
| Öffnen | nur Warnung | typisiertes geprüftes sicheres Open | IO | kein Erfolg oder zweiter Write | fehlender Parent/Verzeichnis/ungültiges Ziel |
| Write / unvollständig | apr_file_puts; Ergebnis verloren | apr_file_write_full + exakte Byteanzahl | IO | Precommit Fail-Closed; Postcommit terminaler Filter | echter OS-Fehler + kontrollierte APR-Seam |
| Flush | ungepuffertes APR | ungepuffertes APR; kein eigener Flush | nicht anwendbar | write_full und Close geprüft | Write-/Close-Kontrollen |
| Close | nur Warnung | geprüftes apr_file_close | IO | erste Contract-Ursache erhalten | kontrollierter Close-Fehler |
| Wiederholung / terminal | Ergebnis nicht weitergegeben | erster Sinkfehler sticky | ursprünglicher Fehler erhalten | keine neue Sinkoperation; keine zweite Antwort | Wiederholung/Precommit/Postcommit |

### HAProxy SPOP

| Sink-Stufe | vorher | nachher | Fehlerklasse | Caller-Verhalten | Test |
| --- | --- | --- | --- | --- | --- |
| Serialisierung | fputs nach Serializer-Erfolg | typisierte Serialisierung vor stdio | INTERNAL / EVENT_TOO_LARGE | Aufrufer erhält false + typisierten Fehler | normal/ungültig/übergroß |
| Öffnen | aufruferspezifischer Fehler | geprüftes Open beim Aufrufer | IO | verpflichtender Response-Pfad schlägt fehl | privates temporäres Ziel |
| Write | ungeprüftes fputs | fputs == EOF / ferror geprüft | IO | fehlerhaftes SPOP-Ergebnis; kein Erfolgsfallback | echter stdio-Writefehler |
| Flush | ungeprüftes gepuffertes Ergebnis | fflush geprüft | IO | erster Fehler erhalten; kein Retry | gepufferter reiner Flushfehler |
| Close | ungeprüfte Completion | eigenes fclose geprüft | IO | keine erfolgreiche Completion | geprüfte Close-Seam |
| Wiederholung / terminal | Sinkerfolg konnte angenommen werden | sticky Sinkfehler pro Request | ursprünglicher Fehler erhalten | kein zweiter physischer Write/ACK-Erfolg | Aufrufer/Wiederholung/Positivkontrolle |

Die Tabellen verwenden API-/Testbezeichnungen unverändert. Caller-Kette: Apache producer → msconnector_event_write_jsonl_line → apache_open_event_file → apr_file_write_full → apr_file_close → typisierte Phase-/Intervention-Caller → Request-/Filter-Fehlerpfad. SPOP producer → phase4_common_event_write → fputs/ferror → fflush → geprüftes fclose → SPOP-Processing-/Response-Fehlerpfad. Bereits committed Apache-Antworten werden nicht durch eine zweite HTTP-Antwort ersetzt. Diagnostische Rule-Match-Ausgaben allein erzwingen keinen HTTP 500.

Envoy: Der C-Close-Pfad ruft Finish auch bei früherem Fehler auf und liefert dessen erhaltene Klasse zurück. Der Go-Cleanup-Reporter unterscheidet lokale `ErrTransactionFinishPhaseSequence` von physischen Sinkfehlern/unsicherem Cleanup, die kontrollierten Restart verlangen. Beide Coordinator-Close-Pfade werten Cleanup-Reporter aus; erste Ursachen bleiben sticky. Eine reale FD-Fehlerinjektion ersetzt den wirkungslosen früheren Fixturefehler.

## Geänderte Dateien

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

## Ausgeführte Befehle

Erfasste exakte Befehle und Ergebnisse aus `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/*.json`. Working Directory: eigener Worktree, außer Go in `connectors/envoy/ext_proc`. Fehlgeschlagene Zwischenläufe bleiben sichtbar. `not enumerated` bezeichnet fehlende Testzählung, keinen Nullumfang. Die Testzahlen sind keine disjunkten Gesamtsummen. Die vollständige Envoy-Tag-Suite prüft echten Common-/libModSecurity-Code.

| Command | Exit | Tests | Result |
| --- | --- | --- | --- |
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

## Security-Auswirkung

Sinkfehler werden nicht mehr zu erfolgreicher verpflichtender Completion. Frühe kanonische technische Fehler bleiben maßgeblich. Keine Validierung, Compilerwarnung, Isolation, Authentisierung oder Scanneranforderung wird abgeschwächt. Bestehende Konfiguration und Eventschema bleiben erhalten.

## Runtime-Evidence

Kompilierte Funktions-/Contracttests prüfen produktive C-Funktionen mit kontrollierter APR-/stdio-Injektion; Go-Tests prüfen Writer und Fehlerweitergabe. Dies sind keine neuen physischen Apache-/HAProxy-/Envoy-Hostläufe. R16/R17 bleiben historische nachgelagerte NGINX-H1-Belege ihrer eigenen Revision.

## Bekannte Einschränkungen

Dokumentations-Environment: Der erste vollständige Check war durch 22 unveränderte Framework-Links blockiert. Eine Fixture aus der exakt gepinnten Framework-Revision wurde anschließend im isolierten Worktree installiert; vollständige Bilingual-, Runtime-Pfad- und Linkchecks bestehen (`docs-final.json`). Ursprünglicher Framework-Checkout und Gitlink bleiben unverändert; MRTS bleibt read-only. Die Fixture ist Testsetup, keine Framework-Produktänderung.

I12/V10-Live-Host-/Physical-Host-Nachweise bleiben offen. Kein Persistenzversprechen über erfolgreiche Write-/Flush-/Close-API-Ergebnisse hinaus. Bereits gesendete Bytes lassen sich nicht zurücknehmen. Stock-lighttpd-Kontrollroute und nicht unterstützte Hostaktionen behalten ihre Grenzen.

## Verbleibende Risiken

I11-Code: keine bekannte Implementierungslücke nach finaler unabhängiger Gegenprüfung. Aktuelle integrierte Nachweise: physische Sinktests 50, Common/Event-Regressionen 60, vollständig instrumentierte C-ASan/UBSan-Tests 46, Apache-native/C17 45 und Adoption 28, Envoy-native/tagged 218 Tests/324 Cases/8 Pakete sowie Race 105/164/3 bestehen. Alle 110 NGINX-Adoptionsmethoden bestehen in vier disjunkten Shards mit 28+28+27+27 Tests. Bilingual-/Pfad-/Link-, Workflow-, Format- und Change-Record-Checks bestehen. Breite Apache-Suite: aktueller Patch 215 Tests, 7 Failures/7 Errors; unveränderte Basis 195 Tests, 8 Failures/7 Errors. Keine neuen Fail-/Errorsets; der frühere precommit_rate_limit-Fixturefehler besteht jetzt. Drei UID/chown-Environmentfehler treten auf beiden Ständen auf. HAProxy-Suite: 203 Tests, fünf auf der Basis reproduzierte Fehler, zwölf Skips. Keine dieser breiten Suites wird als vollständig grün behauptet. I12/V10: reale Hostwirkung und physische Hostnachweise bleiben separat offen. Protected-CI, Secret-Scan und Server-Sonar dieses Patches sind hier nicht behauptet. Environment: HAProxy-C17 ist durch fehlende Native-Header blockiert (nativer Exit 77, Make 2); keine automatische Bereitstellung. Breite Baseline-/Environmentfehler werden nicht durch Abschwächung der Tests beseitigt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine neuen Live-Host-/H2-/H3-/CRS-/Produktionsläufe für diesen lokalen Sink-Patch. Der vorhandene Target `memcheck-nginx` und installiertes Valgrind sind verfügbar, wurden aber ohne eingerichteten Hostlauf nicht ausgeführt. HAProxy-C17 wurde versucht, bleibt jedoch wegen fehlender Native-Header blockiert; keine Toolchain-/Paketinstallation. Protected-Exact-Head-CI, Secret-Scan und Server-Sonar sind unabhängig offen. Die ausgeführten lokalen fokussierten Akzeptanz-, Sanitizer-, Adoptions-, Race-, Format- und Dokumentationsgates bestehen; breite Suites behalten die ausgewiesenen Baseline-/Environmentfehler.

## Finaler Diff- und Review-Status

Lokaler finaler Diff- und unabhängiger Review abgeschlossen: keine Befunde; I11-Implementierungsakzeptanz erfüllt. Der später autorisierte gestapelte Draft PR auf PR #382 wird vom Root-Task geliefert; neuer Head-SHA und PR-Link werden erst nach tatsächlicher Erstellung im externen Deliverybericht gebunden. Aktuelle Identität: Basis plus geprüfter Working-Tree-Patch. Keine Merge-, History-Rewrite- oder Deploymenthandlung. Autorisierte Commit-Aufteilung in fünf Teile: Apache; HAProxy SPOP; Envoy; NGINX; gemeinsame CI-/Make-Integration und synchronisierte EN/DE-Dokumentation. Vollständiger Diff und Testartefakte bleiben für die Prüfung erhalten.

I11 IMPLEMENTATION COMPLETE – remaining live-host evidence belongs to I12/V10
