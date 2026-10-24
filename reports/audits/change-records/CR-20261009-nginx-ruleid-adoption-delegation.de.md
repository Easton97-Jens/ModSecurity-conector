# Change Record: CR-20261009-nginx-ruleid-adoption-delegation

**Sprache:** [English](CR-20261009-nginx-ruleid-adoption-delegation.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-ruleid-adoption-delegation |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `c09480ff9b5b83b52883f5cf116266f1da5ca4d1` |

## Motivation und Problemstellung

Die nur namensbasierte Prüfung auf doppelte Parser lehnte den vorhandenen Wrapper `ngx_http_modsecurity_extract_intervention_rule_id` ab, obwohl Common das Parsing besitzt. Der unveränderte Checker lieferte Exit 1 mit ausschließlich `FAIL: Duplicate NGINX rule-id helper is absent`.

## Akzeptanzkriterien

Begrenzte Delegation akzeptieren; veränderte Eingabe, Ausgabe, Größe, Null-Prüfung, lokales Parsing, Log-Konfigurationsbedingungen, inaktive sichere Zwillinge, fehlende oder späte Extraktion, fehlenden oder nichtleeren Reset, Duplikate und Makroüberschreibungen ablehnen. Die anderen Adoptionsverträge erhalten und innerhalb der vier zugewiesenen Dateien bleiben.

Direktes `return` / `goto` auf oberster Ebene vor der Extraktion ablehnen;
die vorhandenen bedingten frühen Prüfungen erhalten.

## Implementierungsentscheidung und Begründung

Den vollständigen aktiven und unmaskierten Wrapper-Rumpf mit den vorhandenen lexikalischen C-Helfern prüfen: eine Null-Log-Prüfung und ein Common-Aufruf mit Interventionsnachricht, `ctx->last_intervention_rule_id` und dessen `sizeof`. Einen direkten Aufruf unmittelbar nach dem leeren Reset und vor Limitklassifikation, terminaler Aufzeichnung, Redirect-/Status-Dispatch und Cleanup verlangen. Zusätzliche Connector-Regel-ID-Helfernamen und zusätzliche Common-Extraktionsaufrufe im Interventionsmodul ablehnen; die unabhängige Common-Delegation des Loggers erhalten. Kritische Makroprüfungen auf Helfer, Aufrufer, Ein-/Ausgabeidentifikatoren, `sizeof` und `NULL` erweitern. Der vollständige Vertrag ersetzt die namensbasierte Prüfung; keine Parsernamens-Whitelist ersetzt die Validierung.

Die unabhängige Prüfung zeigte, dass ein direktes `goto cleanup;` vor dem
Reset den ansonsten geordneten Aufruf unerreichbar machte. Ein zweiter
Test-first-Schritt lehnt direktes `return` / `goto` im Aufruferpräfix mit
`c_direct_matches` ab; verschachtelte bedingte Prüfungen bleiben akzeptiert.

## Geänderte Dateien

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20261009-nginx-ruleid-adoption-delegation.md`
- `reports/audits/change-records/CR-20261009-nginx-ruleid-adoption-delegation.de.md`

## Ausgeführte Befehle

Portable Notation: `$PARENT_PYTHON` steht für den bereits ausgewählten
Parent-Virtual-Environment-Interpreter; `<temporary-work-root>` steht für das
aufgabeneigene externe Arbeitsverzeichnis. Tatsächliche absolute
Ausführungspfade bleiben in externer Ausführungsevidence, nicht in diesem
versionierten Record.

Arbeitsverzeichnis: `<temporary-work-root>/worktrees/parent-ruleid-adoption-20261009`. Die Befehle liefen über `rtk proxy bash -c` mit `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1` und externem `TMPDIR` / `PYTHONPYCACHEPREFIX`. Python: `$PARENT_PYTHON`.

- Unveränderter nativer Checker: Exit 1; ursprüngliches RED in `native-red.log` erhalten.
- Positiver Baseline-Test gegen den unveränderten Checker: Exit 1, ein erwarteter Fehler mit der ursprünglichen Namensverbotsdiagnose; `positive-red.log`.
- `make check-nginx-common-adoption PYTHON=$PARENT_PYTHON`: Exit 0; `native-green.log`.
- Native Vorlagenerstellung mit `ci/tools/new-change-record.py create --name nginx-ruleid-adoption-delegation --base-revision c09480ff9b5b83b52883f5cf116266f1da5ca4d1 --date 2026-10-09`: Exit 0.
- `make check-doc-links PYTHON=$PARENT_PYTHON`: Exit 2; fehlende bestehende Framework-verknüpfte Pfade in diesem isolierten Worktree; `doc-links.log`.
- `make check-bilingual-docs PYTHON=$PARENT_PYTHON`: Exit 2 wegen derselben fehlenden Framework-Pfade; `bilingual.log`.
- `ci/tools/new-change-record.py check` mit ausgewähltem Interpreter: Exit 0; nur struktureller Archivvertrag; `change-record-check.log`.
- Vier gezielte `test_rule_id_delegation_*`-Methoden: Exit 0, 4 Tests in 85.734s; `focused-tests.log`.
- `$PARENT_PYTHON -m unittest -v tests.test_nginx_common_adoption tests.test_nginx_upstream_security_contract tests.test_nginx_native_intervention_chain`: Exit 0, 143 Tests in 698.443s, keine Skips; `scoped-tests.log`. Dieser vorherige Lauf enthält den unabhängigen Vertrag zur geordneten Extraktion und den nativen Interventions-Unit-Harness mit echtem Common-Code. Er lag vor der Early-Exit-Korrektur und begann vor dem ersten Einfrieren des Kandidaten; die finale Abdeckung der neun Makrosymbole lief separat. Dies ist kein 143-Test-Ergebnis für den finalen Kandidaten.
- Finaler Wiederholungslauf von `test_rule_id_delegation_rejects_macro_overrides`: Exit 0, 1 Test in 27.105s; neun kritische Symbole; `final-macro-tests.log`.
- `rtk proxy git diff --check`: Exit 0.
- Optionales `python -m ruff check ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` mit ausgewähltem Interpreter: Exit 1, `No module named ruff`; `ruff.log`. Keine Installation wurde versucht.
- `rtk --version`: `0.51.0`; `rtk gain` war verfügbar.

Logs bleiben unter `<temporary-work-root>/analysis/nginx-all-required-20261008T124555Z/ruleid-adoption` erhalten.

SHA256-Werte des vorherigen eingefrorenen Kandidaten: Checker
`9edc90aa7ccfb026cfe471e8bdc23352b2aca5ff5d9a6470a742770f33e01dfd`, Tests
`8010273f47b86dce9894ac8d1785e05a65a02fa55691717ce49bc4593d1c5cc6`.
SHA256-Werte des finalen Kandidaten: Checker
`4046f208daf62c3e61c80b8b9e9bfe78265c66fd27f6d12e7ad6779de9b20399`, Tests
`84f17120a5bdb67fe1e1372942bcc93006927dee4351b31a9cfe5bf0fbcab033`.

RED des zweiten Schritts: `test_rule_id_delegation_rejects_direct_early_exits_before_extraction`
gegen den vorherigen Checker, Exit 1, drei erwartete Fehler in 9.856s;
`early-exits-red.log`. Finaler nativer Adoptionschecker: Exit 0;
`final-native-green.log`.

Gezielter Lauf des finalen Kandidaten: `$PARENT_PYTHON -m unittest -v` mit
`test_current_helper_aware_contract_is_accepted` und allen fünf
`test_rule_id_delegation_*`-Methoden von
`tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests`: Exit 0,
6 Tests in 113.614s, keine Skips; `final-six-focused-tests.log`. Quellcode- und
Testdateien blieben während dieses Laufs eingefroren.

Direktes `$PARENT_PYTHON ci/checks/documentation/check-repository-path-references.py`:
Exit 2 wegen bestehender fehlender Framework-verknüpfter Pfade;
`final-path-references.log`. Die Record-Paare verwenden portable Pfadnotation
und enthalten keine verbotenen absoluten lokalen Quell-Checkout-Pfade.

Unabhängige Root-Integrationsvalidierung bei den finalen Checker-/Test-Hashes:
`rtk proxy $PARENT_PYTHON -m unittest -v` mit denselben sechs Checker-Methoden
sowie `tests.test_nginx_native_intervention_chain` und
`tests.test_nginx_upstream_security_contract`: Exit 0, 40 Tests in 113.853s,
keine Skips; `root-ruleid-focus-r2.log` / `.exit` in der externen Task-Analyse.
Der echte Common-C-Unit-Pfad lief; dies ist keine NGINX-Host-Evidence.

Im befüllten Parent-Integrationsworktree an derselben Basis c09480ff lief
`rtk proxy make check-nginx-common-adoption check-bilingual-docs check-doc-links
check-variable-documentation` mit expliziten Parent-/Framework-Interpretern
und Roots vor der Pause mit Exit 0. Diese integrierten Ergebnisse ersetzen
die isolierte Einschränkung fehlender Framework-Pfade nur für jenen Checkout.
Ein frischer vollständiger 144-Test-Lauf und vollständiger nativer Lint
bleiben nach dem normalen Korrektur-Commit ausstehend; der frühere 143-Test-
Lauf wird nicht als finale Evidence wiederverwendet.

## Security-Auswirkung

Verstärkt die Quellvertragsprüfung ohne Produktquellcode, Parser oder Host-Verhalten zu ändern. Synthetische Mutationen dürfen den Checker nicht zur Akzeptanz einer fehlerhaften Grenze der begrenzten Delegation bringen.

## Runtime-Evidence

Keine Ausführung auf einem laufenden Host. Native Interventions-Unit-Tests sind andere Evidence als ein laufender NGINX-Host; es wird keine neue Host-/Runtime-Aussage getroffen.

## Bekannte Einschränkungen

Dies ist ein konservativer lexikalischer Quellvertragsvalidator, kein C-Compiler oder Runtime-Beweis. Dem isolierten Worktree fehlen befüllte Framework-Pfade für das vollständige Dokumentationslink-Target.

## Verbleibende Risiken

Künftige gleichwertige Wrapper-Refactorings können eine ausdrücklich geprüfte Aktualisierung des Checker-Vertrags benötigen. Externe Header und Verhalten auf laufenden Hosts liegen außerhalb des Evidence-Umfangs dieser Korrektur.

## Nicht ausgeführte Prüfungen mit Begründung

Produkt-Builds, vollständige Repository-Testsuite, Host-Runtime, Scanner-Authentifizierung und administrative Prüfungen waren aus dieser begrenzten Aufgabe ausgeschlossen. Framework-/MRTS-Änderungen und Dependency-/Toolchain-Installation waren nicht autorisiert.

Der vorherige 143-Test-Lauf wurde nach dem minimalen Early-Exit-Schritt nicht
wiederholt; gezielte Regressionen und unabhängige Integrationsprüfungen decken
diese finale Änderung ab.

## Finaler Diff- und Review-Status

Die vier zugewiesenen Dateien bleiben zur unabhängigen Parent-Integrationsprüfung erhalten. Produktquellcode, Framework, MRTS, Dependency- und Konfigurationsdateien wurden nicht geändert. Diese Aufgabe führte keinen Commit, Push, PR, Merge oder Master-Integration aus.

Die manuelle EN/DE-Inhaltsprüfung bestätigte gleichwertige technische Fakten
und Literale. Die isolierte Dokumentations-Einschränkung bleibt historisch;
Dokumentationsvalidierung im befüllten Integrationsworktree und der unabhängige
40-Test-Lauf bestanden. Vollständige unveränderliche Post-Commit-Prüfungen
und echte Host-Ausführung bleiben ausstehend.

Die begrenzte Checker-Korrektur und alle angegebenen Negativkontrollen sind
verifiziert. Das gesamte Worktree-Validierungsergebnis ist teilweise erfüllt,
weil die vollständigen Dokumentationstargets hier nicht bestehen konnten.
