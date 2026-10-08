# Change Record: CR-20261008-nginx-seven-contract-hostoperations

**Sprache:** [English](CR-20261008-nginx-seven-contract-hostoperations.md) | Deutsch

Record im Implementierungsstadium; Runtime- und abschließender Delivery-Abgleich stehen aus.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-seven-contract-hostoperations |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `a44d276b37f4ba1ce2c57af2f016d4cf96af43b6` |

## Motivation und Problemstellung

Selektierte NGINX-Konfigurationsfälle benötigen echte operationsspezifische
Host-Invocations und erhaltene Evidence, keinen aus HTTP oder beliebigem
nonzero Exit abgeleiteten Erfolg. Duplicate-Header benötigen tatsächliche
H1-Felder und native Beobachtung.

## Akzeptanzkriterien

Geschlossener Selected-Dispatch muss jeden deklarierten Configtest mit genauer
Eingabe, Exit- und Diagnoseerwartung aufrufen. Receipts binden Case-/Run-/
Source-Identität sowie Raw-Binary-/Modul-/Config-/Ausgabebytes; der Collector
erhält diese Bindungen. Fehlende oder abweichende Evidence darf nicht bestehen.
Required-Selection bleibt erhalten.

## Implementierungsentscheidung und Begründung

Bestehenden Driver, Dispatcher und Collector für `missing_rules_file`,
`invalid_rule_syntax`, `unknown_config_key` und `unsafe_event_path` erweitern.
Dazu eigene fehlende/Directory-Leaves innerhalb des autorisierten Case-Baums,
feste Inline-Syntax beziehungsweise NGINX-Directive-Lookup verwenden.
Configtest-only belegt tatsächliches `nginx -t`, niemals Daemon, Worker,
Request oder Reload. Framework besitzt den entsprechenden strikten
Validierungsvertrag und die Ordered-Header-Fixture; Parent verwendet echten
H1-Transport weiter. Ein separater Driver `run-nginx-valid-rules.py` führt die
geschlossene Startup-Operation für `valid_rules_file` aus: echten Configtest,
Root-Master/nobody-Worker-Startup, GET `/no-crs/deny`, Korrelation nativer Regel
`1100001` und verifiziertes Cleanup. Dispatch übergibt tatsächlichen Framework-Root
und Regeldatei; der Collector erhält die zusammengesetzten Raw-Artefakte.
Explizites `access_log off` verhindert historische Compile-Prefix-Ausgabepfade
in kopierten Konfigurationen. Common erzeugt `engine_decision` /
`MSCONN_EVENT_ENGINE_DECISION`, keine beobachtete Host-Aktion: `actual_action`
ist leer, `visible_http_status` ist `0` und `transport_result` ist `not_observable`.
Separat gebundenes tatsächliches HTTP `403` liefert die Client-Beobachtung,
ohne das Event umzuschreiben.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-configtest.py`,
`ci/runtime/lifecycle/run-nginx-valid-rules.py`,
`ci/runtime/lifecycle/run-selected-nginx-configtests.py`,
`ci/runtime/lifecycle/collect-no-crs-source.py`,
`tests/test_nginx_configtest_driver.py`,
`tests/test_nginx_selected_configtest_wiring.py`,
`tests/test_nginx_configtest_collection.py`,
`tests/test_nginx_valid_rules_driver.py` und
`tests/test_nginx_valid_rules_wiring.py`; dieses EN/DE-Paar.
Framework-Änderungen und die spätere separate Gitlink-Integration sind Arbeit
an einer getrennten Repository-Grenze.

## Ausgeführte Befehle

Der repository-native Change-Record-Generator erzeugte dieses Paar mit Basis
`a44d276b37f4ba1ce2c57af2f016d4cf96af43b6` und Datum `2026-10-08`.
Fokuslogs unter
`/var/tmp/codex/ModSecurity-conector/analysis/nginx-seven-contracts-20261008T080604Z`
belegen 23 bestandene Driver-, 17 Dispatch- und 7 Collector-Tests:
`parent-config-green.log`, `parent-config-wiring-green.log` und
`parent-collector-green.log`. Rote Regressionslogs sind separat erhalten.
Dies sind Unit-/Integration-Contract-Tests, keine aktuelle Runtime-Coverage.
Dokumentationsvalidierung mit `make check-bilingual-docs check-doc-links` und
`python ci/tools/new-change-record.py check` endete mit `0`; `git diff --check`
endete ebenfalls mit `0`. Alle Command-Payloads verwendeten den vorgeschriebenen RTK-Proxy.

## Security-Auswirkung

Pfad-, Ownership-, Symlink-, Artefakt-, Provenance-, Validator- und
Required-Regeln werden nicht abgeschwächt. Kein fremder sensitiver Pfad wird
berührt. Common-/Produktänderung, MRTS-Mutation, Protected-Dispatch oder
administrative Freigabe sind nicht enthalten.

## Runtime-Evidence

Vier Discovery-Proben mit historischem Modul lieferten tatsächlichen
Configtest-Exit `1`; sie sind ausdrücklich keine New-Head-Evidence.
`diagnostic-valid-r2` beobachtete zusätzlich tatsächlichen Configtest-Exit `0`,
Root-Master/nobody-Worker, Client-Exit `0` / HTTP `403`, native Regel-Evidence und
verifiziertes Cleanup, verwendete jedoch uncommitteten Arbeitsstand und historische
Binary-/Modul-Artefakte. Dies bleibt Diagnose, keine Coverage des committeten Heads.
Frische Binary-/Modul-gebundene Operationen, echte H1-/native Events,
Root-Master/nobody-Worker-Identität soweit erforderlich, Cleanup und
Canonical-Auswertung warten noch auf integrierte Ausführung. Hier werden
weder Gesamt-Exact-Head-PASS noch neue Coverage-Zahlen behauptet.

## Bekannte Einschränkungen

`PRODUCT DECISION REQUIRED — invalid_status`: Der bestehende Katalog bestimmt
nicht eindeutig Engine-Statusaktionssyntax oder Common-/Adapter-
Default-Statusfeld. Owner und Akzeptanz-/Ablehnungssemantik unterscheiden
sich; weder Statusbereich noch NGINX-Directive werden erfunden. Der Record
bleibt Required und unerfüllt. Andere historische Producer-Lücken bleiben
außerhalb dieses Auftrags.

## Verbleibende Risiken

Erfolgreiche Unit-Tests oder passende Hashes allein beweisen keine
Runtime-Semantik. Der erfolgreiche Ladefall braucht tatsächliche Ausführung
von Regel `1100001`; Duplicate-Header brauchen nativen Phase-1-Anzahl-/
Wertnachweis über Regel `1100504`, nicht allein HTTP `200`. Voraussetzungen
der geschützten Control-Plane bleiben unabhängig erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger nativer Lint, frischer Standard-Lifecycle, C17-Regression,
vollständige Framework-Suite und revisionsgebundene CI/Sonar sind für diesen
Arbeitsstand noch nicht abgeschlossen. Frühere Basis-Commit-Ergebnisse werden
nicht auf den späteren Head übertragen.

## Finaler Diff- und Review-Status

Finaler Diff-, Whitespace-, Bilingual-, vollständiger Suite-, Runtime- und
Delivery-Review bleiben Integrationsarbeit. PR #396 bleibt Draft;
Framework-Veröffentlichung ist ausschließlich über
`fix/nginx-seven-contracts-20261008` und einen neuen Draft-Folge-PR freigegeben.
Merge, Retarget, Amend, Force-Push und Protected-Dispatch sind nicht
freigegeben. Keine Secrets oder Raw-Bodies sind in diesem Paar eingebettet.
