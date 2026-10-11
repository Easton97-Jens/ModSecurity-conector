# Change Record: CR-20261011-i09-native-route-reconciliation

**Sprache:** [English](CR-20261011-i09-native-route-reconciliation.md) | Deutsch

Nur eine Vorlage. Alle offenen Abschnitte mit tatsächlichen Fakten ausfüllen; keine Validierung wird behauptet.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-i09-native-route-reconciliation |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |






## Motivation und Problemstellung

I09 enthielt ungeprüfte native/API-Aufrufer sowie technische Fehler, die erfolgreiche Phasen, falsche Regel-Events oder erfundene Hostaktionen erzeugen konnten. Alle zehn Profile mit 14 tatsächlichen Routenteilen auf PR382 prüfen und korrigieren, ohne fertige Teilbereiche neu zu entwerfen.

## Akzeptanzkriterien

Jeden unterstützten Routenteil inventarisieren; operationsspezifische Rückgaben; erste Ursache/Phase, wahrheitsgetreue typisierte Events und terminalen Wiedereintritt/Cleanup erhalten; kompilierte Fehler- und echte Erfolgskontrollen ausführen; I10/I11/I12-Abnahme getrennt lassen.

## Implementierungsentscheidung und Begründung

Kanonische error_phase und geprüften einmaligen Auditabschluss erhalten; undokumentierte Callbacks mit optionaler NULL-Fehlerausgabe normalisieren; Fehler ohne Rule-ID versiegeln. Apache-Filter-Aktionsreihenfolge, HAProxy-Binding/Bridge/HTX-Producer, Traefik-UDS/Go-Bestätigungen und lighttpd-Commit-/Abort-Hooks korrigieren. Jede Änderung behebt einen bestätigten Aufruferpfad ohne Defaults oder Sink-Verträge zu ändern.

## Geänderte Dateien

- `.github/workflows/lint.yml`
- `Makefile`
- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
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

## Ausgeführte Befehle

Exakte Befehle, Exits, Testzahlen, aufbewahrte Fehler und Evidence-Ebenen: [I09-Audit](../../../docs/pr-382-i09-route-audit.de.md#abschließender-befehlsabgleich). Final 33 kompilierte Tests/Common-C17-Smoke; Common-Verträge 74; Adoption 19 plus Connector-Checks; HAProxy 194/12 Skips; Traefik 86/4 Skips; lighttpd 178/13 Skips; Go-Race 56/30/21; nativer Envoy-Build. Baseline-/Environment-Nicht-PASS stehen im Bericht.

## Security-Auswirkung

Undokumentierte Ergebnisse und fehlgeschlagene API-Bestätigungen bleiben terminale technische Fehler. Ursprüngliche Ursache/Phase sowie leere unbeobachtete actual_action/rule_id bleiben erhalten; Body-Limit bleibt eigene Policy. Echte Regelblockade und Memory-append0/1-Kontrollen bleiben erhalten. Validierung/Authentifizierung/Isolation/Default-Policies werden nicht abgeschwächt.

## Runtime-Evidence

Keine Live-Host-Runtime-Evidence erhoben oder beansprucht. Kompilierte produktive Seams, C17-Translation-Units und native Go-Tag-Tests belegen nur ihre beschriebenen Code-/API-Ebenen. Externer Evidence-Root: /var/tmp/codex/ModSecurity-conector/analysis/i09-20261011.

## Bekannte Einschränkungen

I10-Host-Modusbehandlung, I11-physische Sinks und I12/V08–V10-Live-Host-/Transportbelege bleiben offen. Natives Stock-lighttpd hat nur P1/P3. HTX-Gesamt-Hostkompilierung fehlt ohne HAProxy-Header. Lokale Sonar-Analyse ist403 Forbidden; aktuelle CI/Quality Gate wird nicht aus alten Checks abgeleitet.

## Verbleibende Risiken

Live-Reset-/Client-Byte-/Nachbarstream-/Log-Sink-Verhalten und finale Release-Verifikation bleiben unabgenommen. Ein bestehender Wortlauttest der generierten Apache-Dokumentation und der Baseline-Python-Workflow-Checker scheitern außerhalb der Produktkorrekturen.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Deployment, Merge, Live-Host-/CRS-/H2-/H3-/vollständige Runtime-Matrix oder physische Sink-Fehlermatrix. Keine Paket-/Header-Provisionierung. Ruff/pytest fehlen; Python-Syntax, Repository-Checks und kompilierte Tests liefern passende Alternativen. Unterbrochene HTX-C17-Provisionierungsversuche sind kein PASS.

## Finaler Diff- und Review-Status

Isolierter Task-Branch wird auf PR382 mit unveränderter obiger Basis gestapelt. Unabhängiger Source-Review fand Denial-/Terminal-Finish-Fälle; beide sind bestätigt und mit kompilierten Kontrollen behoben. Der Folge-Review fand keine verbleibende wesentliche I09-Lücke dieser Pfade. Framework/MRTS-Gitlinks bleiben unverändert. Draft-Auslieferung bedeutet weder Release, Ready, CI-/Quality-Gate-PASS noch Merge.

Draft-CI-Korrekturen und tatsächliche Folgeprüfungen: [Befehlsbericht](../i09-native-route-command-evidence.de.md). Draft-PR [#408](https://github.com/Easton97-Jens/ModSecurity-conector/pull/408) ist auf PR #382 gestapelt. Commit `e15f31f2b5c0aa4b9e85efbdf015985b076ff633` erzeugte echte CI-Fehler: fehlende Apache/APR-Voraussetzungen, zwei fehlende temporäre Verzeichnisse, lokale Befehls-Pfade in der Produktdokumentation und 29 Sonar-Befunde. Das serverseitige Sonar-Quality-Gate bestand; die Repository-Gates für null Issues/Duplikation scheiterten. Authentifiziertes Readback fand vier neue duplizierte Zeilen in zwei Common-Finish-Preflight-Blöcken. Der Folgecommit ergänzt reine CI-Voraussetzungen, portable Testpfade, gepaarte Auditevidenz für originale Befehle und verhaltenserhaltende Common-/HAProxy-/Traefik-Helfer. Kein Scanner-Grenzwert, Negativtest oder Fehlervertrag wurde abgeschwächt. Grüne Connector-Läufe des alten Heads bestätigen den Folge-Head nicht. Erfolgreiche API-Readback-Befehle unten belegen nur Readback, nicht null Befunde. Fremde generierte Cache-Berichte und Environment-Snapshot-Dateien erschienen während der Arbeit und bleiben außerhalb des Commit-Scopes erhalten.

Finaler CI-Voraussetzungsabgleich: CI für `27b32df9e4b207906700f5c98bd3399941a8ca11`, Lint-Run `38122479270`/Job `114419887846`, bestätigte einen verbleibenden Setupfehler: `msc_filters.h:2:10: fatal error: modsecurity/modsecurity.h: No such file or directory`. Das I09-Target führte 23 Methoden mit einem Apache-Fixture-Setupfehler aus; alle HAProxy-Fixtures bestanden. Die bereits in Apache-CI genutzte Voraussetzung `libmodsecurity-dev` wird ergänzt; Kompilierung bleibt verpflichtend. Der exakte Sonar-Head-Check `114420352962` meldete einen Verschachtelungsbefund im Traefik-Poll-Fehlermapper und 0.0% neue Codeduplikation. Extraktion des Poll-Fehlermappers erhält POLLNVAL/EBADF vor POLLHUP/ECONNRESET und Fallback EIO; fünf kompilierte Kontrollen und die tatsächliche C17-Translation-Unit bestehen. Ein serverseitig bestandenes Quality Gate genügt der strikten Null-Befund-Abnahme nicht; Prüfungen am aktualisierten Head bleiben erforderlich.
