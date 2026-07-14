# Change Record: Apache-Request-Transaktionsbereinigung

**Sprache:** [English](CR-20260714-apache-request-transaction-cleanup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Apache-Request-Transaktionsbereinigung |
| Change-ID | CR-20260714-apache-request-transaction-cleanup |
| Datum (UTC) | 2026-07-14T10:51:57Z |
| Autor oder ausführender Agent | Codex /root |
| Basis-Revision | db3f1747bddd2d36470f61c9b04029876f864667 |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b (implementation; this Change Record is uncommitted) |

## Motivation und Problemstellung

Der bestätigte Befund war, dass eine native ModSecurity-<code>Transaction</code>
unter Apache nicht pro Request freigegeben wurde. Vor dieser Änderung speicherte
<code>create_tx_context</code> den nativen Pointer in Request-Notizen, registrierte
aber kein Request-Pool-Cleanup, und der Apache-Connector enthielt keinen Aufruf
von <code>msc_transaction_cleanup</code>.

Der gelieferte Befund enthält keine Scan-ID, Severity, Scanner-Version,
Scan-Zeitstempel, ursprüngliche Scan-Revision oder versionierten Apache-Scanreport.
Ein passender Report wurde im Repository nicht gefunden; diese Provenance-Werte
sind daher unbekannt. Der Befundtitel bleibt wie geliefert erhalten:
<code>Apache transaction is not released per request</code>.

## Betroffene Komponenten und Sicherheitsgrenzen

<code>connectors/apache/src/</code> besitzt die Grenze zwischen Apache-Request
und APR-Pool. Eine erfolgreich erzeugte native <code>Transaction</code> gehört
jetzt dem primären Apache-Request-Pool. Interne Redirects und Subrequests teilen
absichtlich weiterhin den primären Kontext; getrennte Top-Level-Requests auf
einer Keepalive-Verbindung behalten getrennte Request-Pools und Transaktionen.

Der native Destruktor ist nicht idempotent. Deshalb löscht der Callback den
nativen Pointer und die Owner-Notiz vor <code>msc_transaction_cleanup</code>.
Er ändert weder Request-Parsing, Regeln, Logging/Redaction, Response-Verhalten,
Intervention-Cleanup noch Framework-Quellcode. Der lokale Apache-Runtime-Build
und die Rohlogs blieben ausschließlich unter <code>$task_tmp</code> und sind
nicht Teil des versionierten Diffs.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Eine erfolgreiche native Transaktion wird erst nach einer Nicht-NULL-Erzeugung veröffentlicht und erhält genau ein normales Cleanup am primären <code>r-&gt;pool</code>. | erfüllt | Source-Regressionstest und APR-Lifecycle-Harness |
| Der Callback löscht nativen Pointer und primäre Owner-Notiz vor dem nicht-idempotenten nativen Destroy-Aufruf. | erfüllt | Source-Regressionstest und APR-Lifecycle-Harness |
| Keepalive-Request-Pools bleiben unabhängig; Subrequest- und Redirect-Lookup behalten das bestehende Ownership-Modell des primären Kontexts. | erfüllt | APR-Lifecycle-Harness und Source-Regressionstest |
| Fehlgeschlagene Erzeugung, Early-Error-/Intervention-Pfade, Abort und doppelte Callback-Ausführung leaken oder zerstören die native Transaktion nicht doppelt. | erfüllt | APR-Lifecycle-Harness |
| Das gepatchte Modul erhält repräsentativen normalen Apache-Verkehr. | erfüllt, begrenzt | Lokaler Apache-Smoke beobachtete HTTP 200 und HTTP 403 für die ausgewählten No-CRS-Cases |
| Der Apache-Transaktionsbereinigungsvertrag und sein Change Record haben englische/deutsche Begleiter. | erfüllt | <code>make check-bilingual-docs</code>, <code>make check-doc-links</code> und <code>make check-variable-documentation</code> |

## Untersuchte Alternativen

- Cleanup am Modul- oder Prozess-Pool wurde verworfen, weil es Request-spezifische
  native Transaktionen über ihre Request-Lebensdauer hinaus hält.
- Freigabe nur im Log-Hook wurde verworfen, weil Early Errors, Aborts und
  Intervention-Pfade diesen Hook umgehen können.
- Verwendung des veränderlichen <code>msr-&gt;r</code> im Cleanup wurde verworfen,
  weil Redirect- und Subrequest-Lookup dieses Feld aktualisieren; der primäre
  Owner muss festgehalten werden.
- Eine Änderung der Redirect-/Subrequest-Wiederverwendung wurde verworfen, weil
  der bestehende Quellcode die primäre Transaktion absichtlich teilt.
- Eine Änderung von <code>msc_intervention_cleanup</code> wurde ausgeschlossen:
  Sie ist ein separater Befund und eine eigene Verhaltensgrenze.

## Implementierungsentscheidung und Begründung

<code>msc_t</code> hält jetzt <code>owner_request</code> getrennt vom
veränderlichen <code>r</code>. Nach erfolgreicher nativer Erzeugung speichert
der Connector den Kontext und registriert <code>msc_cleanup_request_transaction</code>
als normales APR-Cleanup am primären Request-Pool. Der Callback sichert den
nativen Pointer, setzt <code>msr-&gt;t</code> und <code>owner_request</code> auf
NULL, entfernt <code>NOTE_MSR</code> vom festgehaltenen primären Request und
ruft danach <code>msc_transaction_cleanup</code> auf. Diese Reihenfolge
verhindert eine veraltete Notiz und wiederholtes Cleanup am nicht-idempotenten
nativen Destruktor.

## Geänderte Dateien

- <code>connectors/apache/src/mod_security3.c</code>
- <code>connectors/apache/src/mod_security3.h</code>
- <code>connectors/apache/src/msc_utils.c</code>
- <code>connectors/apache/src/msc_utils.h</code>
- <code>ci/checks/connectors/apache/check-apache-c-standards.sh</code>
- <code>ci/checks/connectors/apache/apache_request_transaction_cleanup.c</code>
- <code>ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh</code>
- <code>tests/test_apache_request_transaction_cleanup.py</code>
- <code>Makefile</code>
- <code>docs/connectors/apache.md</code>
- <code>docs/connectors/apache.de.md</code>
- <code>reports/audits/change-records/CR-20260714-apache-request-transaction-cleanup.md</code>
- <code>reports/audits/change-records/CR-20260714-apache-request-transaction-cleanup.de.md</code>
- <code>reports/audits/change-records/README.md</code>
- <code>reports/audits/change-records/README.de.md</code>

Es wurde weder Framework- noch Generated-Report-Quellcode geändert. Die
Implementierungsdateien wurden während der Verifikation durch einen externen
Working-Tree-Commit in <code>f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b</code>
aufgenommen; dieser Change Record und seine Index-Zeilen bleiben uncommitted.
Bestehende unabhängige Änderungen im Worktree wurden erhalten.

## Hinzugefügte oder geänderte Tests

- <code>tests/test_apache_request_transaction_cleanup.py</code> prüft
  Source-Reihenfolge, Owner-Pool-Registrierung, Callback-Invalidierung sowie
  erhaltene Redirect-/Subrequest-Semantik.
- <code>ci/checks/connectors/apache/apache_request_transaction_cleanup.c</code>
  führt den produktiven Callback mit echten APR-Pools für Normal-, Keepalive-,
  Failed-Create-, Early-Error-/Intervention-, Abort-/Doppel-Cleanup-,
  Subrequest- und Redirect-Fälle aus.
- <code>ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh</code>
  kompiliert und führt diesen Harness mit verfügbaren Apache-/APR-Headern aus.

## Ausgeführte Befehle

Die folgenden Pfade verwenden die sanitisierten Platzhalter <code>$task_tmp</code>,
<code>$cache</code> und <code>$framework</code>. Sie enthalten weder Rohlogs
noch vollständige Umgebungs-Exports.

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_apache_request_transaction_cleanup</code> | 1 | Pre-Fix-Regression: fünf Fehler, weil der erwartete Cleanup-Helper nicht existierte. | None | None |
| <code>rtk env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_apache_request_transaction_cleanup</code> | 1 | Der erste Post-Patch-Lauf zeigte ein Prototype-Match des Test-Parsers; der Test-Helper wurde korrigiert. | None | None |
| <code>rtk sh -n ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh</code> | 0 | Shell-Syntaxprüfung bestanden. | None | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup</code> | non-zero | Der erste Harness-Lauf konnte <code>libapr-1.so.0</code> nicht laden; der Runner erhielt danach das APR-Bibliotheksverzeichnis als rpath. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup</code> | non-zero | Eine Zwischenversion der APR-Library-Directory-Probe schrieb Usage-Text in Compiler-Flags; der Runner leitet <code>-L</code> nun aus APR-Link-Flags ab. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup</code> | 0 | Fünf Source-Contract-Tests und der echte APR-Lifecycle-Harness bestanden. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk make check-apache-common-adoption</code> | 0 | Apache-Common-Adoption-Prüfung bestanden. | None | None |
| <code>rtk make check-apache-c-standard-wiring</code> | 0 | Apache-C-Standard-Wiring-Prüfung bestanden. | None | None |
| <code>rtk env CI=true APACHE_C_STANDARDS_OUT="$task_tmp/build/apache-c-standards" make check-apache-c17</code> | 0 | C17-Kompilierung einschließlich <code>msc_utils.c</code> bestanden. | <code>$task_tmp/build/apache-c-standards</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/apache-request-transaction-cleanup" make check-apache-request-transaction-cleanup-lint</code> | 0 | Die Lint-Integration führte Source-Contract und APR-Harness erfolgreich erneut aus. | <code>$task_tmp/build/apache-request-transaction-cleanup</code> | None |
| <code>rtk env AUTO_FETCH_SMOKE_SOURCES=0 ... sh $framework/ci/runtime/run-apache-smoke.sh</code> | 77 | Der erste Offline-Modul-Build wurde durch einen fehlenden Cached-HTTPD-APR-Library-Suchpfad blockiert, nicht durch Source-Kompilierung. | <code>$task_tmp/build/apache-runtime</code> | None |
| <code>rtk env AUTO_FETCH_SMOKE_SOURCES=0 ... sh $framework/ci/runtime/run-apache-smoke.sh</code> | 1 | Das gepatchte Modul wurde erfolgreich gebaut; die gewählten kurzen Case-Namen wurden ohne <code>NO_CRS_BASELINE=1</code> nicht zu No-CRS-Cases. | <code>$task_tmp/build/apache-runtime</code> | None |
| <code>rtk env NO_CRS_BASELINE=1 ... sh connectors/apache/harness/run_apache_smoke.sh</code> | 0, not executable | Beiden Cases fehlte <code>MODSECURITY_RULE_PREAMBLE_FILE</code>; es wurde kein Verkehrsergebnis beansprucht. | <code>$task_tmp/build/apache-runtime/results-traffic</code> | None |
| <code>rtk env NO_CRS_BASELINE=1 MODSECURITY_RULE_PREAMBLE_FILE="$framework/tests/rules/no-crs-baseline.conf" ... sh connectors/apache/harness/run_apache_smoke.sh</code> | 0 | Das frisch gepatchte Modul bestand die lokalen Apache-No-CRS-Verkehrsfälle: <code>allow_without_marker=200</code> und <code>deny_header_marker_403=403</code>. | <code>$task_tmp/build/apache-runtime/results-traffic-verified</code> | None |
| <code>rtk env BUILD_ROOT="$task_tmp/build/final-docs" PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs</code> | 0 | Zweisprachige Dokumentationsprüfung bestanden. | None | None |
| <code>rtk env BUILD_ROOT="$task_tmp/build/final-docs" PYTHONDONTWRITEBYTECODE=1 make check-doc-links</code> | 0 | Repository-Pfade und Dokumentationslinks bestanden. | None | None |
| <code>rtk env BUILD_ROOT="$task_tmp/build/final-docs" PYTHONDONTWRITEBYTECODE=1 make check-variable-documentation</code> | 0 | Variablendokumentationsprüfung bestanden. | None | None |
| <code>rtk env CI=true BUILD_ROOT="$task_tmp/build/final-lint" PYTHONDONTWRITEBYTECODE=1 make lint</code> | 0 | Vollständiger Lint bestand, einschließlich Apache-Cleanup-Lint-Target und APR-Harness. | <code>$task_tmp/build/final-lint</code> | None |
| <code>rtk env CI=true BUILD_ROOT="$task_tmp/build/final-quick" PYTHONDONTWRITEBYTECODE=1 make quick-check</code> | 0 | Quick-Check bestand und führte seine Lint- und Whitespace-Prüfungen aus. | <code>$task_tmp/build/final-quick</code> | None |
| <code>rtk env CI=true APACHE_REQUEST_TRANSACTION_CLEANUP_OUT="$task_tmp/build/final-target" PYTHONDONTWRITEBYTECODE=1 make check-apache-request-transaction-cleanup</code> | 0 | Post-Commit-Source-Contract-Tests und der APR-Lifecycle-Harness bestanden. | <code>$task_tmp/build/final-target</code> | None |
| <code>rtk git show --check --format=fuller --no-ext-diff f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b</code> | 0 | Der externe Implementierungs-Commit hat keine Whitespace-Fehler. | None | None |
| <code>rtk git diff --check</code> | 0 | Der Post-Record-Working-Tree-Diff hat keine Whitespace-Fehler. | None | None |

## Security-Auswirkung

Dies schließt eine Lücke in der nativen Transaktionslebensdauer pro Request, die
nativen Zustand über Apache-Requests hinweg ansammeln konnte. Die
sicherheitsrelevante Grenze ist die Ownership-Übergabe vom Adapter an
libmodsecurity: Ein Nutzerrequest kann native Transaktionsallokation auslösen,
und sein primärer Request-Pool gibt sie jetzt genau einmal frei. Defaults,
Regelsemantik, Logging/Redaction-Verhalten und Intervention-Cleanup blieben
unverändert.

## Dokumentationsänderungen

- <code>docs/connectors/apache.md</code> und
  <code>docs/connectors/apache.de.md</code> beschreiben jetzt
  Primary-Request-Ownership, Pool-Cleanup-Reihenfolge und absichtliche
  Redirect-/Subrequest-Wiederverwendung.
- Dieses englische/deutsche Change-Record-Paar und beide Change-Record-Indizes
  dokumentieren Entscheidung, Verifikationsgrenze und Einschränkungen.

## Runtime-Evidence

Ein lokaler Apache-Modul-Build und zwei lokale HTTP-Requests liefen mit
<code>AUTO_FETCH_SMOKE_SOURCES=0</code>; das gepatchte Modul beobachtete wie
oben beschrieben HTTP 200 und HTTP 403. Der Lauf hatte keine kanonische Run-ID,
und seine task-lokalen Artefakte werden nach dieser Aufgabe absichtlich entfernt.
Für diese Änderung wird daher keine dauerhafte Runtime-Evidence oder
Produktionsaussage beansprucht. Der APR-Lifecycle-Harness ist die direkte
Evidenz für die Cleanup-Reihenfolge.

## Bekannte Einschränkungen

- Der APR-Harness nutzt den produktiven Cleanup-Callback und echte APR-Pools,
  läuft aber nicht mit einem Apache-Worker und Memory-Leak-Instrumentierung.
- Der Runtime-Smoke deckt normalen Allow-/Deny-Verkehr ab, aber keine
  langlaufende Keepalive-Leak-Messung, jeden Error-Pfad oder jedes
  Redirect-/Subrequest-Verhalten.
- Die ursprüngliche Scan-Provenance und Severity sind unbekannt.

## Verbleibende Risiken

- Eine zukünftige Änderung könnte <code>create_tx_context</code> umgehen oder
  den Primary-Request-Sharing-Vertrag ändern. Source-Regressionstest und
  APR-Harness schützen das aktuelle Wiring und die Reihenfolge.
- <code>msc_intervention_cleanup</code> bleibt ein separater Scope und muss
  unabhängig bewertet werden.

## Nicht ausgeführte Prüfungen mit Begründung

Das netzwerkgestützte kanonische Target <code>make runtime-smoke-apache</code>
lief nicht: Sein Wrapper kann ohne invocation-lokalen Snapshot während der
Component-Preparation Release-APIs kontaktieren. Der explizite Offline-Modul-Build
und der lokale Apache-Harness nutzten stattdessen den vorhandenen Cache mit
<code>AUTO_FETCH_SMOKE_SOURCES=0</code>. Ein Memory-Leak-Profiler war nicht
verfügbar; der APR-Harness ist die fokussierte Cleanup-Verifikation.

## Finaler Diff- und Review-Status

Der finale Review bestand: Post-Commit-Targeted-Cleanup-Prüfung,
zweisprachige/Dokumentationsprüfungen, <code>make lint</code>,
<code>make quick-check</code>, <code>git show --check</code> für
<code>f4f9aefede434a8bb2c579a87c1d3fe6fbb3506b</code> sowie der
Post-Record-<code>git diff --check</code> bestanden. Die Implementierung liegt
in diesem externen Commit; dieses Change-Record-Paar und seine Index-Zeilen
bleiben uncommitted. Dieser Agent führte weder Commit, Staging, Reset,
Framework-Änderung noch Bereinigung unabhängiger Worktree-Änderungen durch.
