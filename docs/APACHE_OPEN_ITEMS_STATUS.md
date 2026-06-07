# Apache Connector Open Items Status

Stand: 2026-05-24. Diese Analyse basiert auf den aktuell offenen GitHub-Issues und -Pull-Requests in `owasp-modsecurity/ModSecurity-apache`, den lokalen Quellen in `ModSecurity-conector` und den vorhandenen Test-/Runtime-Artefakten in `ModSecurity-test-Framework`. Es wurden keine Produktivcodeänderungen vorgenommen und keine neuen Smoke-Runs gestartet.

## Quelle

- Offene Issues: https://github.com/owasp-modsecurity/ModSecurity-apache/issues
- Offene Pull Requests: https://github.com/owasp-modsecurity/ModSecurity-apache/pulls

## Zusammenfassung

- Anzahl geprüfter Issues: 26
- Anzahl geprüfter PRs: 4
- Anzahl umgesetzt: 6
- Anzahl teilweise umgesetzt: 12
- Anzahl nicht umgesetzt: 8
- Anzahl nicht relevant: 3
- Anzahl unklar: 1

Wichtigste technische Lücken:

- Phase-4/`RESPONSE_BODY`-Blocking ist im Apache-Connector weiterhin nicht als stabile Fähigkeit belegt. Die Runtime-Snapshots zeigen für mehrere Response-Body- und Outbound-Audit-Fälle erwartete `403`, aber tatsächlich `200`.
- V2-kompatible Apache-Direktiven wie `SecDataDir` oder `SecDefaultAction` sind nicht als native Apache-Direktiven registriert; sie können nur über die v3-Connector-Direktiven und `modsecurity_rules` in den libmodsecurity-Regelsatz gelangen.
- Build-/Installationspfade sind nur teilweise robuster dokumentiert. `DESTDIR` bei `make install` und flexible `--with-libmodsecurity=/usr/lib`-Erkennung sind nicht gelöst.
- Es fehlen Regressionstests für graceful-restart-Speicherverhalten, vollständige CRS-v2/v3-Parität, vhost-/UID-abhängige Audit-Logs, SecRequestBodyAccess-Off-Verhalten und vollständige Phase-5-Abdeckung.
- RemoteIPHeader ist lokal implementiert und durch einen connector-eigenen Runtime-Gate belegt.

## Status-Tabelle

| Typ | Nummer | Titel | Status | Relevanz für ModSecurity-conector | Relevanz für Test-Framework | Nachweis im Code/Test | Nächste Schritte |
|---|---:|---|---|---|---|---|---|
| Issue | 12 | Having the exactly same results for apache version 2 and version 3 while running the OWASP CRS | Teilweise umgesetzt | V2/v3-Parität und CRS-Verhalten | Hoch, aber nur als Teilmenge vorhanden | `docs/testing/generated/apache-runtime-results.generated.md`, `docs/testing/generated/connector-gap-summary.generated.md`, `docs/testing/v2-vs-v3-compatibility.md` | Vollständigen CRS-Lauf mit Log-Parser und v2/v3-Diff ergänzen |
| Issue | 15 | Have all the phases correctly attached to Apache | Teilweise umgesetzt | Apache-Hooks, Filter, Phase 1 bis 5 | Hoch | `connectors/apache/src/mod_security3.c`: `hook_request_late`, `hook_insert_filter`, `hook_log_transaction`; PR-70-Tests phase 1 bis 3 PASS, phase 4 former expected-failure | Phase 4 stabilisieren und Phase-5-Test ergänzen |
| Issue | 17 | Implement the logging callback | Umgesetzt | libmodsecurity-Logcallback in Apache | Mittel, dedizierter Logcallback-Test fehlt | `modsecurity_log_cb`, `msc_set_log_cb`, `modsecurity_use_error_log` in `connectors/apache/src/mod_security3.c` und `connectors/apache/src/msc_config.c` | Regression für error-log-Forwarding bei `log,deny` ergänzen |
| Issue | 23 | Configuration merge is not working as expected | Teilweise umgesetzt | Directory/Location-Merge, Ruleset-Merge, Enable/Disable | Hoch | `msc_hook_merge_config_directory`; `ci/check-apache-directive-config.sh` testet `modsecurity off` in `Location` | Merge-Reihenfolge und Directory-vs-Location-Regelvererbung testen |
| Issue | 24 | Module name should be investigated | Nicht umgesetzt | Modulname und LoadModule-Kompatibilität | Niedrig | Modul bleibt `mod_security3.so` und `security3_module` in `connectors/apache/Makefile.am`, `COMPILE_APACHE.md` | Entscheidung dokumentieren oder Alias-/Installationsstrategie entwerfen |
| Issue | 25 | Make sure that the performance numbers are at very least equally to the ones on version 2 | Nicht umgesetzt | Performance/Regression | Mittel | Keine Benchmarks oder Performance-Suites gefunden | Apache-v2/v3-Benchmark-Suite und Baselines ergänzen |
| Issue | 26 | Having all the configurations set in the Apache fashion | Teilweise umgesetzt | Direktiven-API und v2-Kompatibilität | Hoch | Registriert sind nur `modsecurity`, `modsecurity_rules`, `modsecurity_rules_file`, `modsecurity_rules_remote`, `modsecurity_use_error_log`, `modsecurity_transaction_id`, `modsecurity_transaction_id_expr` | V2-Direktivenmatrix erstellen und native Kompatibilitätsstrategie festlegen |
| Issue | 27 | Version banner at startup | Teilweise umgesetzt | Startup-Logging | Niedrig | `msc_hook_post_config` loggt `ModSecurity-Apache v0.1.1-beta configured.` | libmodsecurity-Version, Build-Quelle und Test für Banner ergänzen |
| Issue | 30 | modsec audit log repeats section F | Nicht umgesetzt | Response-Header/Audit-Log-Serialisierung | Hoch | `output_filter` fügt `err_headers_out` und `headers_out` pro Filteraufruf hinzu; keine Guard-Flag gegen Wiederholung | Einmalige Header-Verarbeitung pro Transaktion implementieren und Section-F-Test ergänzen |
| Issue | 47 | fail to compile on standard archlinux install | Nicht umgesetzt | Autotools/APXS, Installationsziel | Hoch | `find_libmodsec.m4` erwartet Prefix mit `include/` und `lib/`; `Makefile.am` nutzt `@APXS@ -i` ohne `DESTDIR` | libdir/pkg-config-Erkennung und DESTDIR-respektierende Installation implementieren |
| Issue | 55 | ./configure fails... configure: error: ModSecurity libraries not found! | Teilweise umgesetzt | Build-Dokumentation und libmodsecurity-Erkennung | Mittel | `COMPILE_APACHE.md` dokumentiert `--with-libmodsecurity`; `find_libmodsec.m4` bleibt prefix-orientiert | `pkg-config`, explizite Lib/Header-Pfade und bessere Fehlermeldungen ergänzen |
| Issue | 57 | General Apache Startup Error | Teilweise umgesetzt | Direktiven und v2-vs-v3-Konfiguration | Mittel | Docs nennen v3-Connector-Direktiven; `SecDataDir` ist keine Apache-Direktive des Connectors | Migrationsdoku für v2-Direktiven und ggf. warnende Kompatibilitätsdirektiven ergänzen |
| Issue | 67 | Apache error log does not work for blocking actions | Unklar | Blocking-Logpfad und Callback | Hoch | Callback existiert, aber kein Test belegt `log,deny` im Apache error log | Reproduktionsfall als Regressionstest aufnehmen |
| Issue | 72 | ModSecurity SecRequestBodyAccess Off still process the POST request | Nicht umgesetzt | Request-Body-Filter und Phase 2 | Hoch | `hook_request_late` und `input_filter` rufen `msc_process_request_body` ohne sichtbare SecRequestBodyAccess-Off-Gate-Logik auf | Off-Fall testen und Body-Verarbeitung an Engine-Status koppeln |
| Issue | 77 | What does "ModSecurity-apache is unstable" mean, exactly? | Teilweise umgesetzt | Dokumentation und v2-Konfigurationsunterschiede | Mittel | `README.md`, `COMPILE_APACHE.md`, `docs/connectors/directive-parity.md` dokumentieren aktuellen Stand und Lücken | Benutzerorientierte "v2 to v3 Apache config" Doku ergänzen |
| Issue | 78 | The modsecurity-apache v2.9 rule chain always appears #conforms | Nicht relevant | Betrifft v2.9, nicht den v3 Apache-Connector im Workspace | Niedrig | Keine v3-Relevanz gefunden | Kein Connector-Code nötig; ggf. Upstream-v2 verweisen |
| Issue | 79 | Under mod_ruid2 ot mod_mpm_itk SecAuditLog is only being logged to when request is to an IP (or localhost) | Nicht umgesetzt | Audit-Log unter vhost/UID-Kontext | Mittel | Keine mod_ruid2/mod_mpm_itk-spezifische Logik oder Tests | vhost/UID-Audit-Szenario in Apache-Harness ergänzen |
| Issue | 80 | Future plans? | Nicht relevant | Projektplanung, keine konkrete Codeanforderung | Niedrig | Roadmap-/Statusdokumente existieren lokal | Keine technische Umsetzung außer Roadmap-Pflege |
| Issue | 81 | Apache connector 3.0 not factoring in RemoteIPHeader like mod_security2 | Umgesetzt | REMOTE_ADDR/RemoteIPHeader | Hoch | `msc_apache_client_ip` nutzt `r->useragent_ip`; `ci/check-apache-directive-config.sh` testet `RemoteIPHeader X-Forwarded-For` mit Status `406` | Test in Framework oder CI-Pipeline sichtbarer machen |
| Issue | 82 | apache graceful restart + Apache connector + rules = memory leak | Nicht umgesetzt | Lifetime/Cleanup bei graceful restart | Hoch | Kein Memory-Test; `rules_set`-Cleanup und `name_for_debug`-Lifetime sind nicht durch Tests belegt | Graceful-restart-Leaktest und Cleanup-Audit ergänzen |
| Issue | 83 | modsec3 module not loaded for Linux 7.2 os version | Teilweise umgesetzt | ABI/API-Kompatibilität zu libmodsecurity | Mittel | `msc_new_transaction_with_id` wird verwendet; `COMPILE_APACHE.md` dokumentiert Load-/ldd-Mismatch | Version-/Symbol-Check oder klare Mindestversion im configure ergänzen |
| Issue | 84 | Unable to disable module once loaded | Umgesetzt | `modsecurity off` in Apache-Kontexten | Hoch | `msc_config_modsec_state`, `create_tx_context`; `ci/check-apache-directive-config.sh` erwartet `Location`-Bypass mit HTTP `200` | Framework-Test für vhost/location-disable ergänzen |
| Issue | 85 | Segmentation Fault in modsecurity_log_cb (Security) | Umgesetzt | Sicherheitsrelevanter Format-String-Fix | Hoch | `modsecurity_log_cb` nutzt `"%s", msg` für `ap_log_rerror` und `ap_log_error` | Security-Regressionsfall mit `%` im Logtext ergänzen |
| Issue | 87 | v3.0.5 of ModSecurity breaks apache connector | Teilweise umgesetzt | API-Typen `Rules`/`RuleSet` | Hoch | `mod_security3.h` nutzt `rules_set.h` bedingt und `void *rules_set`; keine v3.0.5-Matrix | Build-Matrix gegen 3.0.5 und aktuelle v3 ergänzen |
| Issue | 89 | Plans for production readyness? | Nicht relevant | Projekt-/Supportfrage | Niedrig | Lokale Doku markiert bekannte Lücken | Roadmap aktuell halten, kein direkter Code-Fix |
| Issue | 90 | Is it possible to change the SecAuditLogStorageDir variable so that the logs are sorted by vhost? | Nicht umgesetzt | Audit-Log-Konfiguration pro vhost | Niedrig bis mittel | Keine vhostbasierte `SecAuditLogStorageDir`-Erweiterung gefunden | Prüfen, ob libmodsecurity-Variable/Apache-Ausdruck sinnvoll integrierbar ist |
| PR | 56 | Smallfixes | Teilweise umgesetzt | Request-Body-Verarbeitung, Format-String, Filterentfernung | Hoch | Format-String durch PR #86 erledigt; `ap_remove_input_filter` durch PR #65 erledigt; `hook_request_late` verarbeitet Body weiterhin | PR in Teiländerungen aufteilen; Body-Duplikation und Empty-Body-Fall testen |
| PR | 65 | Removing the input filter using the corresponding API | Umgesetzt | Input-Filter-Fehlerpfad | Mittel | `connectors/apache/src/msc_filters.c` nutzt `ap_remove_input_filter` in `input_filter` | Regression für Intervention im Input-Filter ergänzen |
| PR | 70 | Enable audit log and add 00-phases tests | Teilweise umgesetzt | Audit-Log-Phase-Tests | Hoch | `pr70_phase1_audit_request_header`, `pr70_phase2_audit_urlencoded_body`, `pr70_phase3_audit_response_header` PASS; `pr70_phase4_response_body_audit_xfail` former expected-failure | Phase 4 stabilisieren und Phase-5-Test importieren |
| PR | 86 | Fix logging format string | Umgesetzt | Sicherheitsfix im Logcallback | Hoch | `modsecurity_log_cb` nutzt feste Formatzeichenkette `"%s"` | Dedizierten `%`-Payload-Test ergänzen |

## Details pro Issue/PR

### Issue #12: Having the exactly same results for apache version 2 and version 3 while running the OWASP CRS

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/12
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Gewünscht ist ein vollständiger Vergleich von Apache v2 und Apache v3 beim Ausführen des OWASP CRS mit Log-Parser-Auswertung.
- Relevante Dateien im ModSecurity-conector: `reports/testing/real-world-connector-validation.md`, `reports/testing/generated/runtime-matrix.generated.md`, `README.md`.
- Relevante Tests im ModSecurity-test-Framework: `docs/testing/generated/apache-runtime-results.generated.md`, `docs/testing/generated/runtime-matrix.generated.md`, `docs/testing/v2-vs-v3-compatibility.md`.
- Bewertung: Das Framework deckt viele portable Regel-, Body-, Audit- und Phasenfälle ab, aber keinen vollständigen CRS-v2/v3-Gleichlauf.
- Fehlende Umsetzung: Vollständiger CRS-Lauf, ModSecurity-log-utilities-Integration, reproduzierbarer v2-vs-v3-Diff und akzeptierte Abweichungsliste.
- Empfohlene nächste Schritte: CRS-Fixtures in `ModSecurity-test-Framework` aufnehmen, `ci/run-apache-smoke.sh` um CRS-Profil ergänzen, Log-Parser-Ausgabe als Artefakt persistieren. Vermuteter Aufwand: hoch.

### Issue #15: Have all the phases correctly attached to Apache

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/15
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Alle libmodsecurity-Phasen sollen korrekt an Apache-Hooks und Filter angebunden sein.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `hook_request_late`, `hook_insert_filter`, `hook_log_transaction`, `process_request_headers`; `connectors/apache/src/msc_filters.c` mit `input_filter` und `output_filter`.
- Relevante Tests im ModSecurity-test-Framework: `tests/cases/audit-log/pr70-phases/pr70_phase1_audit_request_header.yaml`, `pr70_phase2_audit_urlencoded_body.yaml`, `pr70_phase3_audit_response_header.yaml`, `pr70_phase4_response_body_audit_xfail.yaml`, `docs/testing/generated/apache-runtime-results.generated.md`.
- Bewertung: Phase 1 bis 3 sind durch PR-70-Derivate belegt; Phase 4 bleibt former expected-failure und Phase 5 hat keinen vergleichbaren PR-70-Test.
- Fehlende Umsetzung: Stabiles Response-Body-Blocking, vollständige Audit-Assertions für Phase 4 und dedizierter Phase-5-Logging-Test.
- Empfohlene nächste Schritte: Guard/State im `output_filter` ergänzen, `msc_process_response_body` nur einmal pro Transaktion verifizieren, Phase-5-YAML aus PR #70 ableiten. Vermuteter Aufwand: hoch.

### Issue #17: Implement the logging callback

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/17
- Typ: Issue
- Statusbewertung: Umgesetzt
- Kurzbeschreibung: libmodsecurity soll Logmeldungen in den Apache error log schreiben können.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `modsecurity_log_cb` und `msc_set_log_cb`; `connectors/apache/src/msc_config.c` mit `modsecurity_use_error_log`.
- Relevante Tests im ModSecurity-test-Framework: Kein dedizierter Callback-Test gefunden.
- Bewertung: Der Callback ist implementiert und nutzt feste Formatstrings.
- Fehlende Umsetzung: Testabdeckung für tatsächliche error-log-Einträge bei `log`, `deny` und `modsecurity_use_error_log off`.
- Empfohlene nächste Schritte: Apache-Harness um Error-Log-Assertion ergänzen. Vermuteter Aufwand: mittel.

### Issue #23: Configuration merge is not working as expected

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/23
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Directory- und Location-Konfigurationen sollen wie bei v2 zusammengeführt werden.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/msc_config.c` mit `msc_hook_create_config_directory` und `msc_hook_merge_config_directory`; `connectors/apache/src/mod_security3.c` mit `create_tx_context`.
- Relevante Tests im ModSecurity-test-Framework: Keine umfassende Directory-/Location-Merge-Matrix. Connector-eigener Gate: `ci/check-apache-directive-config.sh`.
- Bewertung: Enable/Disable und Transaction-ID-Overrides werden gemerged, Rulesets ebenfalls, aber die Reihenfolge und v2-Parität sind nicht vollständig belegt.
- Fehlende Umsetzung: Tests für Parent/Child-Regelreihenfolge, Directory-vs-Location-Precedence, `modsecurity_rules_file` und `modsecurity_rules_remote` in verschachtelten Kontexten.
- Empfohlene nächste Schritte: Connector-spezifische Apache-YAML- oder CI-Fälle für Merge-Semantik ergänzen; bei Abweichung `msc_rules_merge`-Reihenfolge prüfen. Vermuteter Aufwand: mittel bis hoch.

### Issue #24: Module name should be investigated

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/24
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Es soll geprüft werden, ob das Modul `mod_security` statt `mod_security3` heißen sollte.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/Makefile.am`, `connectors/apache/build/apxs-wrapper.in`, `COMPILE_APACHE.md`.
- Relevante Tests im ModSecurity-test-Framework: Keine.
- Bewertung: Der aktuelle Workspace verwendet weiterhin `mod_security3.so` und `security3_module`.
- Fehlende Umsetzung: Namensentscheidung, mögliche Alias-/Symlink-Strategie und Migrationsdokumentation.
- Empfohlene nächste Schritte: Entscheidung in `docs/connectors/directive-parity.md` oder Build-Doku festhalten, Installationspfad testen. Vermuteter Aufwand: niedrig bis mittel.

### Issue #25: Make sure that the performance numbers are at very least equally to the ones on version 2

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/25
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Apache-v3-Performance soll mindestens v2-Niveau erreichen oder vergleichbar dokumentiert sein.
- Relevante Dateien im ModSecurity-conector: Keine Performance-Suite gefunden.
- Relevante Tests im ModSecurity-test-Framework: Keine Benchmarks gefunden.
- Bewertung: Der Workspace enthält funktionale Smoke- und Runtime-Matrix-Artefakte, aber keine Performance-Baselines.
- Fehlende Umsetzung: Lasttest-Szenarien, Latenz-/Durchsatzmessungen, v2/v3-Vergleich mit CRS.
- Empfohlene nächste Schritte: Separates Benchmark-Profil in `ModSecurity-test-Framework/ci` anlegen und Ergebnisse in `reports/testing/` ablegen. Vermuteter Aufwand: hoch.

### Issue #26: Having all the configurations set in the Apache fashion

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/26
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: v2-ähnliche Apache-Konfigurationsdirektiven sollen in v3 verfügbar oder sauber migriert sein.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/msc_config.c`, `common/include/msconnector/directives.h`, `docs/connectors/directive-parity.md`, `README.md`.
- Relevante Tests im ModSecurity-test-Framework: `ci/check-apache-directive-config.sh` im Connector; Framework hat nur indirekte Regeltests.
- Bewertung: Die v3-Connector-Direktiven sind registriert. Eine breite native v2-Direktivenkompatibilität ist nicht vorhanden.
- Fehlende Umsetzung: Direktivenmatrix für v2-Apache-Konfigurationsnamen, Warn-/Fallback-Verhalten für nicht mehr unterstützte Direktiven, Tests für Startup- vs Runtime-Fehler.
- Empfohlene nächste Schritte: V2-Direktiven aus `ModSecurity_V2/apache2/apache2_config.c` gegen aktuelle v3-Connector-Direktiven mappen. Vermuteter Aufwand: hoch.

### Issue #27: Version banner at startup

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/27
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Beim Start soll ein hilfreiches Versionsbanner erscheinen.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.h` mit `MSC_APACHE_CONNECTOR`; `connectors/apache/src/mod_security3.c` mit `msc_hook_post_config`.
- Relevante Tests im ModSecurity-test-Framework: Keine Banner-Assertion.
- Bewertung: Der Connector loggt den Connectornamen und die Version, aber keine libmodsecurity-Version oder Builddetails.
- Fehlende Umsetzung: Erweiterte Diagnoseinformationen und Test, dass der Banner im error log erscheint.
- Empfohlene nächste Schritte: `msc_hook_post_config` um libmodsecurity-Version erweitern und Log-Assertion ergänzen. Vermuteter Aufwand: niedrig.

### Issue #30: modsec audit log repeats section F

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/30
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Section F des Audit-Logs enthält wiederholte Response-Header.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/msc_filters.c` mit `output_filter`.
- Relevante Tests im ModSecurity-test-Framework: `tests/cases/response/headers/phase3_response_headers_multi_value_connector_gap.yaml`, `phase3_response_headers_duplicate_value_runtime_difference.yaml`, `docs/testing/generated/apache-runtime-results.generated.md`.
- Bewertung: Der Output-Filter addiert Response-Header pro Filterdurchlauf; ein "already processed"-Flag ist nicht erkennbar.
- Fehlende Umsetzung: Transaktionszustand für einmalige `msc_process_response_headers`-Ausführung und Section-F-Deduplizierungsregression.
- Empfohlene nächste Schritte: State in `msc_t` ergänzen, Header nur einmal an libmodsecurity übergeben, Audit-Log-Fixture mit duplizierten Headern prüfen. Vermuteter Aufwand: mittel.

### Issue #47: fail to compile on standard archlinux install

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/47
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: `./configure --with-libmodsecurity=/usr/lib` findet die Bibliothek nicht; `make install` respektiert `DESTDIR` nicht.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/build/find_libmodsec.m4`, `connectors/apache/Makefile.am`, `connectors/apache/build/apxs-wrapper.in`.
- Relevante Tests im ModSecurity-test-Framework: `ci/prepare-apache-build.sh` nutzt einen staging prefix, testet aber nicht Arch-Layout oder `DESTDIR`.
- Bewertung: Der lokale Buildpfad ist für den Framework-Staging-Prefix brauchbar, aber das gemeldete Distribution-Packaging-Problem bleibt.
- Fehlende Umsetzung: libdir/include-dir/pkg-config-Erkennung und Installationsziel ohne root-Schreibzugriff.
- Empfohlene nächste Schritte: `PKG_CHECK_MODULES` oder explizite `--with-libmodsecurity-libdir`/`--with-libmodsecurity-includedir` ergänzen, `DESTDIR`-Installtest hinzufügen. Vermuteter Aufwand: mittel.

### Issue #55: ./configure fails... configure: error: ModSecurity libraries not found!

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/55
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Nutzer können eine installierte libmodsecurity nicht zuverlässig an `configure` übergeben.
- Relevante Dateien im ModSecurity-conector: `COMPILE_APACHE.md`, `connectors/apache/build/find_libmodsec.m4`, `connectors/apache/docs/build.md`.
- Relevante Tests im ModSecurity-test-Framework: `ci/prepare-apache-build.sh` mit `./configure --with-libmodsecurity=$MODSECURITY_STAGE`.
- Bewertung: Dokumentation und Framework-Pfad helfen, aber die Autoconf-Erkennung bleibt restriktiv.
- Fehlende Umsetzung: Bessere Fehlermeldung bei falschem Prefix, Unterstützung für Library-Datei oder pkg-config.
- Empfohlene nächste Schritte: Configure-Makros robuster machen und negative/positive Configure-Tests ergänzen. Vermuteter Aufwand: mittel.

### Issue #57: General Apache Startup Error

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/57
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Apache erkennt v2-Direktiven wie `SecDataDir` nicht als Apache-Direktiven des v3-Connectors.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/msc_config.c`, `README.md`, `COMPILE_APACHE.md`, `docs/connectors/directive-parity.md`.
- Relevante Tests im ModSecurity-test-Framework: Keine direkte `SecDataDir`-Startup-Regression.
- Bewertung: Der Workspace dokumentiert die v3-Direktiven, aber keine vollständige v2-Migrationskompatibilität.
- Fehlende Umsetzung: Migrationshinweise, Beispielkonfigurationen und ggf. warnende Kompatibilitätsdirektiven.
- Empfohlene nächste Schritte: `COMPILE_APACHE.md` um v2-zu-v3-Konfigurationsbeispiele erweitern; Startup-Fehlertest für direkte v2-Direktiven ergänzen. Vermuteter Aufwand: mittel.

### Issue #67: Apache error log does not work for blocking actions

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/67
- Typ: Issue
- Statusbewertung: Unklar
- Kurzbeschreibung: `log,deny` soll bei Blocking-Aktionen in den Apache error log schreiben, tut es laut Issue aber nicht.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `modsecurity_log_cb` und `process_intervention`.
- Relevante Tests im ModSecurity-test-Framework: Kein dedizierter error-log-Test; Audit-Log-Tests sind vorhanden.
- Bewertung: Der Callback existiert, aber vorhandene Artefakte belegen nicht den spezifischen `log,deny`-Pfad im Apache error log.
- Fehlende Umsetzung: Reproduktions- und Regressionstest mit `SecRuleEngine On` und `log,deny`.
- Empfohlene nächste Schritte: In `ci/check-apache-directive-config.sh` oder Framework einen Error-Log-Assert für Blocking-Regeln aufnehmen. Vermuteter Aufwand: mittel.

### Issue #72: ModSecurity SecRequestBodyAccess Off still process the POST request

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/72
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Bei `SecRequestBodyAccess Off` wird Phase 2 bzw. Request-Body-Verarbeitung weiterhin angestoßen.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `hook_request_late`; `connectors/apache/src/msc_filters.c` mit `input_filter`.
- Relevante Tests im ModSecurity-test-Framework: `tests/cases/phases/phase1/phase1_vs_phase2_request_body_gap.yaml`, `tests/cases/negative-pass-through/phase2_header_only_pass_through.yaml`, `docs/testing/generated/apache-runtime-results.generated.md`.
- Bewertung: Es ist keine explizite Off-Gate-Logik sichtbar; der Runtime-Fall `phase1_vs_phase2_request_body_gap` schlägt fehl.
- Fehlende Umsetzung: Body-Verarbeitung muss Engine-/Ruleset-Status respektieren; Debug-Log-Doppelstart sollte regressiongetestet werden.
- Empfohlene nächste Schritte: YAML-Fall mit `SecRequestBodyAccess Off` und POST-Body ergänzen, danach Filter-/Hook-Pfad korrigieren. Vermuteter Aufwand: mittel bis hoch.

### Issue #77: What does "ModSecurity-apache is unstable" mean, exactly?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/77
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Dokumentationsfrage zu Produktionsreife und v2/v3-Konfigurationsunterschieden, inklusive `SecDefaultAction`-Startupfehler.
- Relevante Dateien im ModSecurity-conector: `README.md`, `COMPILE_APACHE.md`, `docs/connectors/directive-parity.md`, `reports/testing/test-coverage-overview.md`.
- Relevante Tests im ModSecurity-test-Framework: `docs/testing/generated/apache-runtime-results.generated.md`, `docs/testing/generated/connector-gap-summary.generated.md`.
- Bewertung: Die lokale Doku beschreibt unterstützte Direktiven und Lücken, aber keine klare Endnutzer-Migrationsseite.
- Fehlende Umsetzung: Explizite Erklärung "unstable/not production ready", Beispiele für CRS-Einbindung über `modsecurity_rules_file`, Umgang mit v2-Direktiven.
- Empfohlene nächste Schritte: Anwenderorientiertes Migrationsdokument ergänzen. Vermuteter Aufwand: niedrig bis mittel.

### Issue #78: The modsecurity-apache v2.9 rule chain always appears #conforms

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/78
- Typ: Issue
- Statusbewertung: Nicht relevant
- Kurzbeschreibung: Das Issue bezieht sich auf ModSecurity Apache v2.9.
- Relevante Dateien im ModSecurity-conector: Keine.
- Relevante Tests im ModSecurity-test-Framework: Keine.
- Bewertung: Der aktuelle Workspace bewertet den v3 Apache-Connector und gemeinsame v3/v2-Kompatibilitätsfälle, nicht einen v2.9-Datenbank-Logging-Bug.
- Fehlende Umsetzung: Keine für diesen Connector.
- Empfohlene nächste Schritte: Upstream-v2-Kontext separat prüfen, falls gewünscht. Vermuteter Aufwand: nicht anwendbar.

### Issue #79: Under mod_ruid2 ot mod_mpm_itk SecAuditLog is only being logged to when request is to an IP (or localhost)

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/79
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Audit-Logging verhält sich unter mod_ruid2 oder mod_mpm_itk bei namensbasierten vhosts anders.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`; keine spezifische UID/vhost-Logik.
- Relevante Tests im ModSecurity-test-Framework: Allgemeine Audit-Log-Tests, aber keine mod_ruid2/mod_mpm_itk- oder vhost-UID-Fälle.
- Bewertung: Das gemeldete Szenario ist nicht abgedeckt.
- Fehlende Umsetzung: Apache-Harness mit named vhost, wechselndem Runtime-User/Group-Kontext und Audit-Log-Rechten.
- Empfohlene nächste Schritte: Erst reproduzieren, dann prüfen, ob libmodsecurity-Dateiöffnung oder Apache-Prozessmodell verantwortlich ist. Vermuteter Aufwand: hoch.

### Issue #80: Future plans?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/80
- Typ: Issue
- Statusbewertung: Nicht relevant
- Kurzbeschreibung: Projektplanungsfrage ohne konkrete technische Anforderung.
- Relevante Dateien im ModSecurity-conector: `docs/roadmap/roadmap.md`, `README.md`.
- Relevante Tests im ModSecurity-test-Framework: Nicht relevant.
- Bewertung: Keine direkte Implementierung ableitbar.
- Fehlende Umsetzung: Keine.
- Empfohlene nächste Schritte: Roadmap aktuell halten. Vermuteter Aufwand: niedrig.

### Issue #81: Apache connector 3.0 not factoring in RemoteIPHeader like mod_security2

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/81
- Typ: Issue
- Statusbewertung: Umgesetzt
- Kurzbeschreibung: `REMOTE_ADDR` soll nach `RemoteIPHeader X-Forwarded-For` den durch mod_remoteip gesetzten Clientwert nutzen.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `msc_apache_client_ip`, `msc_apache_client_port` und Hook-Reihenfolge mit `mod_remoteip.c`.
- Relevante Tests im ModSecurity-test-Framework: Connector-eigener Test `ci/check-apache-directive-config.sh`.
- Bewertung: Code nutzt `r->useragent_ip` und der CI-Gate blockt bei `X-Forwarded-For: 1.2.3.4` mit `REMOTE_ADDR @ipMatch 1.2.3.4`.
- Fehlende Umsetzung: Der Test liegt im Connector-CI, nicht als allgemeiner Framework-YAML-Fall.
- Empfohlene nächste Schritte: RemoteIP-Fall in die Runtime-Matrix aufnehmen oder den CI-Gate in der Doku sichtbarer referenzieren. Vermuteter Aufwand: niedrig.

### Issue #82: apache graceful restart + Apache connector + rules = memory leak

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/82
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Wiederholte graceful restarts mit geladenen Regeln erhöhen den Speicherverbrauch.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `msc_apache_init`/`msc_apache_cleanup`; `connectors/apache/src/msc_config.c` mit `msc_create_rules_set` und `name_for_debug`.
- Relevante Tests im ModSecurity-test-Framework: Keine Memory- oder graceful-restart-Suite.
- Bewertung: Cleanup wird nur grob registriert; Regeln-/Config-Lifetimes sind nicht durch Leaktests belegt.
- Fehlende Umsetzung: Wiederholter `apachectl graceful`-Test mit Regeln und Speicher-Metrik.
- Empfohlene nächste Schritte: Leak-Repro in `ci/run-apache-smoke.sh` oder separatem Langtest ergänzen; Ruleset-Cleanup auditieren. Vermuteter Aufwand: hoch.

### Issue #83: modsec3 module not loaded for Linux 7.2 os version

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/83
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Apache kann das Modul wegen fehlendem Symbol `msc_new_transaction_with_id` nicht laden.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` nutzt `msc_new_transaction_with_id`; `COMPILE_APACHE.md` enthält Load-/ldd-Troubleshooting.
- Relevante Tests im ModSecurity-test-Framework: `src/v3-api-smoke/v3_api_smoke.c` prüft API-Grundpfade, aber nicht Modul-ABI gegen alte libmodsecurity-Versionen.
- Bewertung: Dokumentation hilft beim Diagnosepfad, aber es gibt keinen configure-Zwang oder Fallback für fehlende Symbole.
- Fehlende Umsetzung: Mindestversion/Symbolcheck beim Build oder Load-Diagnose.
- Empfohlene nächste Schritte: Autoconf-Test für `msc_new_transaction_with_id` ergänzen und klare Mindestversion dokumentieren. Vermuteter Aufwand: mittel.

### Issue #84: Unable to disable module once loaded

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/84
- Typ: Issue
- Statusbewertung: Umgesetzt
- Kurzbeschreibung: ModSecurity soll in einzelnen Kontexten deaktivierbar sein.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/msc_config.c` mit `msc_config_modsec_state`; `connectors/apache/src/mod_security3.c` mit `create_tx_context`.
- Relevante Tests im ModSecurity-test-Framework: Connector-eigener `ci/check-apache-directive-config.sh` mit `Location "/__modsec_directive_off"`.
- Bewertung: `modsecurity off` verhindert lokal die Transaktionserstellung und der Runtime-Gate erwartet HTTP `200`.
- Fehlende Umsetzung: Allgemeiner Framework-Fall für vhost/location-disable fehlt.
- Empfohlene nächste Schritte: Apache-spezifischen Framework-Test oder CI-Dokumentationsverweis ergänzen. Vermuteter Aufwand: niedrig.

### Issue #85: Segmentation Fault in modsecurity_log_cb (Security)

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/85
- Typ: Issue
- Statusbewertung: Umgesetzt
- Kurzbeschreibung: Unsicherer Formatstring in `ap_log_rerror`/`ap_log_error` kann Crash oder Format-String-Angriff auslösen.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c` mit `modsecurity_log_cb`.
- Relevante Tests im ModSecurity-test-Framework: Kein dedizierter `%`-Payload-Test.
- Bewertung: Beide Apache-Log-Aufrufe verwenden lokal `"%s", msg`.
- Fehlende Umsetzung: Regressionstest mit `%`-Sequenzen im Regel-/Payload-Logtext.
- Empfohlene nächste Schritte: Security-Smoke in Apache-Harness aufnehmen. Vermuteter Aufwand: niedrig.

### Issue #87: v3.0.5 of ModSecurity breaks apache connector

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/87
- Typ: Issue
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: Typänderung `Rules` zu `RuleSet` bricht den Build gegen bestimmte libmodsecurity-v3-Versionen.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.h` mit `MSC_USE_RULES_SET`, `rules_set.h` und `void *rules_set`; `connectors/apache/src/mod_security3.c` ohne alten `(Rules *)`-Cast.
- Relevante Tests im ModSecurity-test-Framework: `src/v3-api-smoke/v3_api_smoke.c`; keine explizite v3.0.5-Buildmatrix.
- Bewertung: Der alte harte `Rules`-Cast ist lokal entschärft, aber die Versionsbedingung ist nicht gegen v3.0.5 nachgewiesen.
- Fehlende Umsetzung: Build-Test gegen v3.0.5 und aktuelle v3, inklusive Headerpfade in `msc_filters.h`/`msc_utils.h`.
- Empfohlene nächste Schritte: Matrix in CI oder lokalem Buildscript ergänzen, Makros anhand realer Header prüfen. Vermuteter Aufwand: mittel.

### Issue #89: Plans for production readyness?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/89
- Typ: Issue
- Statusbewertung: Nicht relevant
- Kurzbeschreibung: Projekt-/Supportfrage zur Produktionsreife.
- Relevante Dateien im ModSecurity-conector: `README.md`, `docs/roadmap/roadmap.md`, `reports/testing/real-world-connector-validation.md`.
- Relevante Tests im ModSecurity-test-Framework: Runtime-Matrix und Smoke-Artefakte als Evidenz, aber keine direkte "production ready"-Prüfung.
- Bewertung: Kein einzelnes umsetzbares Code-Item.
- Fehlende Umsetzung: Keine technische Umsetzung direkt aus dem Issue.
- Empfohlene nächste Schritte: Status-/Roadmapdokumente aktuell halten und bekannte Lücken klar nennen. Vermuteter Aufwand: niedrig.

### Issue #90: Is it possible to change the SecAuditLogStorageDir variable so that the logs are sorted by vhost?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/90
- Typ: Issue
- Statusbewertung: Nicht umgesetzt
- Kurzbeschreibung: Audit-Logs sollen nach vhost in unterschiedliche Storage-Verzeichnisse geschrieben werden können.
- Relevante Dateien im ModSecurity-conector: Keine vhostbasierte Erweiterung gefunden; Audit-Pfade werden über libmodsecurity-Regeln konfiguriert.
- Relevante Tests im ModSecurity-test-Framework: Audit-Log-Tests nutzen `@@AUDIT_LOG@@` und `@@AUDIT_LOG_DIR@@`, aber keine vhost-Sortierung.
- Bewertung: Aktuell nicht umgesetzt.
- Fehlende Umsetzung: Konzept für Apache-Ausdruck/vhost-Variable in Audit-Log-Konfiguration oder Dokumentation, warum dies libmodsecurity-seitig liegt.
- Empfohlene nächste Schritte: Machbarkeit mit libmodsecurity-Konfigurationsmodell prüfen; vhost-Harness-Test ergänzen. Vermuteter Aufwand: mittel.

### PR #56: Smallfixes

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/56
- Typ: PR
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: PR bündelt Format-String-Workaround, Request-Body-Verarbeitung und Testkonfigurationsänderungen.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`.
- Relevante Tests im ModSecurity-test-Framework: `tests/cases/phases/phase1/phase1_vs_phase2_request_body_gap.yaml`, `tests/cases/audit-log/pr70-phases/*`.
- Bewertung: Format-String-Fix ist durch PR #86 sauberer umgesetzt; Input-Filter-Entfernung durch PR #65. Der Body-Verarbeitungsteil ist nicht vollständig übernommen und der lokale Code ruft `msc_process_request_body` weiterhin in `hook_request_late` auf.
- Fehlende Umsetzung: Eindeutige Request-Body-State-Maschine, Empty-Body-Fall, Off-Fall, CRS-Regressionsnachweis.
- Empfohlene nächste Schritte: PR in atomare Fixes zerlegen und nur mit Tests übernehmen. Vermuteter Aufwand: mittel bis hoch.

### PR #65: Removing the input filter using the corresponding API

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/65
- Typ: PR
- Statusbewertung: Umgesetzt
- Kurzbeschreibung: Im Input-Filter soll `ap_remove_input_filter` statt `ap_remove_output_filter` verwendet werden.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/msc_filters.c`.
- Relevante Tests im ModSecurity-test-Framework: Kein dedizierter Input-Filter-Fehlerpfad-Test.
- Bewertung: Lokaler Code verwendet `ap_remove_input_filter` im Null-Kontext- und Interventionspfad.
- Fehlende Umsetzung: Regressionstest für Input-Filter-Intervention.
- Empfohlene nächste Schritte: POST-Body-Blocking-Fall mit früher Intervention ergänzen. Vermuteter Aufwand: niedrig.

### PR #70: Enable audit log and add 00-phases tests

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/70
- Typ: PR
- Statusbewertung: Teilweise umgesetzt
- Kurzbeschreibung: PR aktiviert Audit-Log-Auswertung in Apache::Test und ergänzt Phase-Tests.
- Relevante Dateien im ModSecurity-conector: Keine direkte Codeänderung nötig; relevant sind `connectors/apache/src/mod_security3.c` und `connectors/apache/src/msc_filters.c`.
- Relevante Tests im ModSecurity-test-Framework: `tests/cases/audit-log/pr70-phases/pr70_phase1_audit_request_header.yaml`, `pr70_phase2_audit_urlencoded_body.yaml`, `pr70_phase3_audit_response_header.yaml`, `pr70_phase4_response_body_audit_xfail.yaml`, `docs/testing/pr70-audit-phase-coverage-plan.md`.
- Bewertung: Phase 1 bis 3 wurden als portable YAML-Fälle importiert und laufen laut Runtime-Snapshot PASS. Phase 4 bleibt former expected-failure; Phase 5 ist nicht importiert.
- Fehlende Umsetzung: Stabile Phase-4-Response-Body-Assertions und Phase-5-Audit-/Logging-Test.
- Empfohlene nächste Schritte: Phase-5-Fall aus PR #70 ableiten, Response-Body-Pfad zuerst reparieren. Vermuteter Aufwand: mittel bis hoch.

### PR #86: Fix logging format string

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/86
- Typ: PR
- Statusbewertung: Umgesetzt
- Kurzbeschreibung: Fix für Issue #85 durch feste Formatzeichenkette.
- Relevante Dateien im ModSecurity-conector: `connectors/apache/src/mod_security3.c`.
- Relevante Tests im ModSecurity-test-Framework: Kein dedizierter `%`-Payload-Test.
- Bewertung: Der Patchinhalt ist lokal vorhanden: `ap_log_rerror(..., "%s", msg)` und `ap_log_error(..., "%s", msg)`.
- Fehlende Umsetzung: Automatischer Regressionstest.
- Empfohlene nächste Schritte: Testfall mit `%5C`, `%n`-ähnlichen Sequenzen im geloggten Text ergänzen. Vermuteter Aufwand: niedrig.

## Fehlende Tests

- Vollständiger OWASP-CRS-v2/v3-Vergleich mit Log-Parser für Issue #12.
- Phase-4-Response-Body-Blocking als stabiler PASS, inklusive Audit-Log-Section und Intervention, für Issue #15, PR #70 und verwandte Response-Body-Lücken.
- Phase-5-Logging/Audit-Test aus PR #70.
- Error-log-Callback-Test für `log,deny`, `DetectionOnly`, `success` und `modsecurity_use_error_log off` für Issues #17 und #67.
- Directory-/Location-/vhost-Merge-Matrix für Issue #23 und Issue #84.
- `SecRequestBodyAccess Off` mit POST-Body und Debug-/Audit-Negativassertion für Issue #72.
- Audit-Log-Section-F-Deduplizierung für Issue #30.
- mod_ruid2/mod_mpm_itk oder gleichwertiger vhost/UID-Audit-Log-Repro für Issue #79.
- Graceful-restart-Memory-Leak-Test für Issue #82.
- Build-Matrix für Arch-/Alpine-artige Layouts, `DESTDIR`, `pkg-config` und libmodsecurity-v3.0.5 für Issues #47, #55, #83 und #87.
- Startup-Banner-Assertion mit Connector- und libmodsecurity-Version für Issue #27.
- Performance-Benchmark gegen ModSecurity v2 für Issue #25.
- Vhost-basierte `SecAuditLogStorageDir`- oder Audit-Pfad-Tests für Issue #90.

## Priorisierung

### Hoch

- Issue #85 / PR #86: Format-String-Sicherheit ist umgesetzt, aber Regressionstest fehlt.
- Issue #15 / PR #70: Phase-4- und Phase-5-Abdeckung fehlen; `RESPONSE_BODY` bleibt nicht verifiziert.
- Issue #72: `SecRequestBodyAccess Off` wird nicht ausreichend respektiert oder getestet.
- Issue #30: Audit-Log-Section-F-Duplikate können Forensik und Parität brechen.
- Issue #47, #55, #83, #87: Build-/ABI-Kompatibilität kann Installation oder Modul-Load blockieren.
- Issue #82: Graceful-restart-Leak mit Regeln kann Produktionsbetrieb gefährden.
- Issue #23: Config-Merge-Parität ist für vhost/Location-Sicherheit zentral.
- Issue #67: Blocking-Error-Log-Verhalten ist sicherheitsoperativ relevant, aber unklar.

### Mittel

- Issue #12: CRS-v2/v3-Parität ist wichtig, aber eine größere Validierungsstrecke.
- Issue #26, #57, #77: V2-zu-v3-Konfigurationsmigrationslücken.
- Issue #79: Audit-Log-Verhalten unter vhost/UID-Modulen.
- Issue #81: RemoteIPHeader ist umgesetzt; Framework-Promotion des Tests wäre sinnvoll.
- Issue #84: Deaktivieren ist umgesetzt; breitere Merge-/vhost-Regression fehlt.
- PR #56, PR #65: Teilweise übernommene Fixes sollten atomar mit Tests abgesichert werden.
- Issue #90: Vhost-sortierte Audit-Logs sind funktional nützlich, aber nicht core-blockierend.

### Niedrig

- Issue #24: Modulname/Installationsalias ist vor allem Migrationskomfort.
- Issue #27: Startup-Banner ist teilweise vorhanden, Erweiterung und Test fehlen.
- Issue #78: Betrifft v2.9 und ist für diesen v3-Connector nicht relevant.
- Issue #80 und Issue #89: Projektplanungsfragen ohne direkten Code-Fix.
- Dokumentations-Cleanup für bekannte Apache-vs-NGINX-Abweichungen, insbesondere Apache ohne NGINX-Phase-4-Direktiven.
