# Change Record: CR-20261012-pr409-base-refresh

**Sprache:** [English](CR-20261012-pr409-base-refresh.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261012-pr409-base-refresh |
| Datum (UTC) | 2026-10-12 |
| Basis-Revision | `d94a7a38b90bc56b828d70f7df8794e12fd21e10` |

## Motivation und Problemstellung

PR #409 bei `caafe7ecec1a91669cbb82cea18b2b97309cde44` hatte Konflikte mit der aktualisierten PR-#382-Basis. Die Basis enthält jetzt I09 (#408), I11 (#406) und engine-gesteuerte Request-/Response-Body-Policy (#407). Der Nutzer verlangte die Aktualisierung dieses PRs und eine erneute Kontrolle im bestehenden eigenen Worktree. Origin/master bleibt `3019722fbda40dc281b861c1cc38085be2f430a0`; ursprüngliche Delivery-Basis war `498653c2a193d34b7b25b2903b1e4db1c45e7f73`. Taskbaum anfangs sauber. PR #409 ist inzwischen bereit zur Prüfung (`draft=false`); der beobachtete Zustand bleibt erhalten.

## Akzeptanzkriterien

- Veröffentlichte Historie erhalten und exakte Basis `d94a7a38b90bc56b828d70f7df8794e12fd21e10` integrieren; den PR nicht in seine Basis/master mergen.
- Alle18 Integrationskonflikte ohne Verlust von I09/I10/I11 oder engine-gesteuerter Body-Policy lösen.
- Exakt-eins, erste technische Ursache, terminales Reentry, wahrheitsgemäße Hostbeobachtungen und einmaliges Cleanup erhalten.
- Aktuelle Caller-/Native-/Mutations-/SDK-/Regressions-/Lint-/Dokumentprüfungen ausführen; Fehlversuche und Skips ausdrücklich erhalten.
- Checks und Sonar-Readback für den aktuellen SHA liefern; ältere Head-Erfolge bleiben historisch. I12-Host-/Client-/Transportakzeptanz separat.

## Implementierungsentscheidung und Begründung

Neuere Basis mit normalem Merge-Commit in den Taskbranch integrieren; kein Rebase/Amend/Force-Push. Common-HTTP-Autorisierung erhält den neuen inkrementellen Requeststream und verlangt exakt eins bei Begin, gepuffertem/Socket-Append, EOS, Companion-Handoff und Finish. Die Fixture prüft kanonische Fehlercodes, damit spätere IO-Fehler mit gleichem HTTP-Status die Erstursache nicht verdecken; ein deterministischer POST liefert sein Byte erst nach Headern und erreicht den echten Socket-Loop-Append.

Envoy kombiniert kanonisches vierargumentiges Checked-Close/Observed-Close und getrennte Finish-Klassifikation mit kompatibler void-ABI, Erstursache und Commitguards. HAProxy erhält typisierte Nativefehler, I11-Sinks und I10-Hostlatches; technische SPOP-Fehler bleiben auch bei detect-only/open disruptive503. Traefik erhält Streaming/Terminal-Latches, prüft den neuen Commitcallback exakt eins und testet die beabsichtigten ErrAbortHandler-Ergebnisse. Natives/Stock-lighttpd erhalten Requeststream-/Spool-APIs und aktuelle engine-gesteuerte Limits. Kompilierte Fixtures verwenden tatsächliche Signaturen und gültiges SPOP-Framing; Assertions und Negativkontrollen bleiben erhalten.

Echte SDK-Loopback-Tests zeigten drei Sidecar-Resets nach wartendem/abgelehntem Input: Entfernen aller Worker-Shutdowns verhinderte Duplikate, ließ aber geordneten Abschluss aus. Jeder Exchange speichert jetzt Shutdown-Versuch und beobachteten Erfolg. Alle Stop-Pfade teilen den Latch, wiederholen fehlgeschlagenen Shutdown nie, und normaler finaler Stop erfolgt nach Snapshots/Receipts ohne erfundene HostAction. Fehlgeschlagene Decision-Auslieferung erreicht immer den technischen Fehlerpfad.

Der Immediate-Client-RST-Test scheiterte auch auf unveränderter exakter Basis vor Transaktionsadmission. Ein testseitiger --wrap=send-Pipe-Gate synchronisiert jetzt am echten HTTP418-Write nach nativem P2; kein Sleep/Produktionshook. Dies belegte einen fehlenden ConnectorError: eine terminale vorgesehene RuleDecision blockierte explizites technisches Scheitern, und ihr vorhandener Terminalevent-Latch unterdrückte den neuen Event. Ein Fail-only-Übergang für korrelierte Regeln löscht jetzt actionable Regelmetadaten und bleibt TERMINAL. Allgemeine Decision-Mutability unverändert; BODY_LIMIT, frühere Ursachen und Cleanup bleiben geschützt. Runtime verweigert den Übergang nach bestätigter Hostaktion/Finish, replayt physische IO-Fehler und setzt den Eventlatch einmal zurück. Produktive native Reihenfolge schließt P2 vor RuleDecision ab und erhält die technische Eventphase. Der Test prüft das aktuelle flache kanonische Eventschema, Errorstatus, leere Regel/Aktion, keinen erfundenen Abort und null Upstreamrequests.

I09/I10/I11-Abschluss und historische Routenevidenz bleiben getrennt; vier Checklist-/Matrix-Paardokumente erhalten14 produktive I10-Legs und56 historische Zeilen. Source-Tests verwenden tatsächliche Funktionsdefinitionen statt Rekursion oder veraltete Helfer zu verlangen. Die HTX-Pfadsicherheitsfixture übergibt die neu erforderliche explizite Enginepolicy und erhält Pfad-/Symlinkguards.

## Geänderte Dateien

- `.github/workflows/test-common.yml`
- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-haproxy.yml`
- `.github/workflows/test-lighttpd.yml`
- `.github/workflows/test-traefik.yml`
- `Makefile`
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
- `tests/test_lighttpd_i10_adapter_errors.py`
- `tests/test_native_api_fail_closed_contract.py`
- `tests/test_runtime_rule_delivery_failure.py`
- `tests/test_traefik_i10_dispatcher.py`
- `tests/test_traefik_i10_mutations.py`
- `tests/traefik_i10_dispatcher_test.c`

## Ausgeführte Befehle

Alle Befehle liefen über RTK mit task-eigenen externen Build-/Cache-/Temp-Roots und installierter Parent-Pythonumgebung. Exaktes cwd und ausgewählte geheimnisfreie Umgebung begleiten jeden Run. Pythoncounts zählen Methoden, Go-Counts Packages; Skips und frühere Fehlversuche sind kein ausgeführtes PASS. Frühere kombinierte Fehler verhinderten folgende Make-Targets; erfolgreiche gezielte Ersatzläufe stehen separat.

| Exakter Befehl | Exit | Anzahl | Sekunden | Run / Evidence |
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

Zusätzliche Worker-Evidence unter `native-worker/` und `go-worker/`: HAProxy7 Callermethoden/22 erkannte Mutanten; lighttpd ursprüngliche479 Fälle/9 Mutanten erhalten, mit neuen Socketowner-Kontrollen und zehntem Mutanten; Traefik-Dispatcher690 Fehler/690 terminale Reentries/270 gültige Kontrollen in zugelassenen Modi und15 C-/Go-Mutanten; Envoy18 kompilierte Bridge-/Finishchecks plus8 echte Common-/libModSecurity-/CGo-Packages. Neue Common-Delivery-Regression:5 Methoden,12 Regelfälle,6 versiegelte Lifecycle-Negative,4 Erstursachen-/physische IO-Fälle und2 erkannte Sourcemutationen. Common-HTTP-Matrix360 Negativfälle plus120 MRC1-Fehler und6 kompilierte Mutationen. Strict bleibt nur nach aktuellem Registry zugelassen. Keine Compilerwarnung/Assertion abgeschwächt.

## Security-Auswirkung

Die Aktualisierung erhält fail-closed/terminale technische Fehler und trennt vorgesehene RuleDecisions von gescheiterter Hostauslieferung. Clientreset kann keinen fälschlich rule-only technischen Abschluss hinterlassen. Der belegte fehlende Event beweist keinen Enforcement-Bypass. Shutdown-Erfolg ist begrenzte Socketowner-Evidence und kein Live-Clientreset-/Nachbarstreambeweis. Keine Scannerregel, Exclusion, Suppression, Gate, Authentifizierung, Profilzulassung, Warnflag oder Dependencyvertrag verändert.

## Runtime-Evidence

Die echte libModSecurity3.0.14-Sidecar-Loopback-Suite führt task-lokale Sockets, native Regeln und private Event-/Receiptdateien aus, einschließlich kontrolliertem Client-RST an produktiver Sendgrenze. Dies ist begrenzte Sidecar-Regressions-Evidence, keine I12-Kampagne aller Routen. Kompilierte Fixtures und Go-/CGo-Tests beweisen nur ihre Caller-/API-/Eventebene. Ursprüngliche PR-Implementierungshistorie steht im [früheren Change Record](CR-20261011-pr382-i10-adapter-errors.de.md); keine aktuelle Head-Evidence.

## Bekannte Einschränkungen

Lokale Python3.14.4/Go1.27.2 weichen von Pins3.14.7/1.27.1 ab. Vorhandene SDKs und erhaltene task-eigene native Sources ausdrücklich ausgewählt; keine Installation/Systemänderung. Skips und historische Fehlversuche bleiben im Ledger. Baseline-RST-Schedulingfehler separat vom belegten deterministischen Common-Abschlussdefekt. Statische Prüfung nennt außerdem bestehendes void-Composite-Finish-Verhalten: aktueller RPC kann nil liefern, während Coordinatorfehler Sessions abbrechen, Admission verweigern und zum Prozessowner propagieren; kein neu belegter ausnutzbarer Defekt.

## Verbleibende Risiken

I12/V08–V10 vollständige Host-/Client-/Reset-/Nachbarstream-Evidence bleibt offen. I09/I10/I11-Code-/Evidence-Abschluss gehört zu seinen begrenzten Revisionen/geprüften Grenzen. Bei Commitvorbereitung kann neue Head-Hosted-CI/Sonar noch nicht gelaufen sein; PR-Beschreibung/externe finale Delivery-Evidence enthalten den terminalen aktuellen Readback. Bei initialem Readback keine menschlichen Reviews.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-Host-/Client-/Nachbarstreamkampagne aller Routen, Deployment, PR-/Mastermerge, Dependencyinstallation, vollständiger Matrixexport oder destruktives Cleanup. Keine exakt gepinnten lokalen Toolchain-Patchversionen, da nicht vorhanden. Baseline-Prüfworktree bleibt detached an exakter Basis; Framework/MRTS und ihre Gitlinks unverändert.

## Finaler Diff- und Review-Status

Unabhängiger Sourcereview prüfte Common, Envoy, Traefik und begrenzte HAProxy-/lighttpd-Überlappungen; kein neuer ungelöster materieller Befund in diesem Scope nach enger Common-Korrektur. Echte SDK-/kompilierte Akzeptanz steht oben. Finaler Sourcediff, Whitespace, EN/DE, aktuelle Basisancestry, Local-/Remote-/PR-Gleichheit, Reviewthreads und alle Hostedchecks erneut für gepushten SHA lesen; ältere grüne CI wird nicht übertragen. PR-Ready-Zustand erhalten; kein Merge in Basis/master. Worktrees/volle Evidence extern erhalten.
