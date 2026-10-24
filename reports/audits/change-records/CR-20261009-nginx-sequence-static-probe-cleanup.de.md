# Change Record: CR-20261009-nginx-sequence-static-probe-cleanup

**Sprache:** [English](CR-20261009-nginx-sequence-static-probe-cleanup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-sequence-static-probe-cleanup |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `b884c6653a72dc490c4ae472dd3cbf5a1ee646b8` |

## Motivation und Problemstellung

Der echte R10-Full97-Lauf mit Root-Master/nobody-Worker erreichte einen echten
HTTP-200-Request für `clean_shutdown`. Danach lehnte die Framework-Retention
korrekt zwei `transaction_cleanup`-Source-Events für dieselbe konfigurierte
Transaktions-ID ab. Die Parent-Sequenz-Fixture verwendete
`try_files $uri /index.html;`: Die synthetische Sequenz-URI fehlte, daher führte
NGINX einen internen Redirect auf `index.html` aus, erzeugte einen zweiten
Location-Transaktionskontext und räumte einen vollständigen sowie einen
vorzeitigen Kontext auf. Dies ist ein Parent-Fixture-Routing-Defekt und kein
Grund, den Exact-one-Cleanup-Vertrag des Frameworks abzuschwächen.

## Akzeptanzkriterien

- Jede statische Nicht-Upstream-Sequenz liefert das feste projizierte
  `index.html` ohne internen Redirect aus.
- Echte Upstream-Cases behalten ihren realen `proxy_pass`-Pfad.
- Produktseitige Redirect-Context-Isolation, strikte Framework-Validierung,
  die 97 Required-Auswahlen, Framework und MRTS bleiben unverändert.
- Ein frischer echter Sequenz-Request muss genau ein wahrheitsgetreues
  Cleanup-Event je zugelassener Transaktion erzeugen, bevor diese Änderung
  einen Canonical PASS stützen kann.

## Implementierungsentscheidung und Begründung

Die aus dem generischen Startup-Template übernommene Redirect-Location wird vor
der Case-spezifischen Konfiguration durch die bestehende Probe-Location
`try_files /index.html =404;` ersetzt. Die feste projizierte Datei existiert,
daher liefert NGINX sie im ursprünglichen Request-Kontext aus. Upstream-Cases
ersetzen diese Probe-Location direkt durch ihre bestehende ungepufferte
Proxy-Konfiguration. Das Connector-Modul und sein absichtliches Verhalten mit
neuem Kontext nach echten internen Redirects werden nicht geändert.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`
- `tests/test_nginx_sequence_driver.py`
- `reports/audits/change-records/CR-20261009-nginx-sequence-static-probe-cleanup.md`
- `reports/audits/change-records/CR-20261009-nginx-sequence-static-probe-cleanup.de.md`

## Ausgeführte Befehle

Befehle verwendeten RTK im isolierten Parent- oder Framework-Worktree;
temporäre Daten blieben unter `/var/tmp/codex/ModSecurity-conector`.

- RED: Parent-Unittest
  `tests.test_nginx_sequence_driver.DriverTests.test_static_sequence_probes_do_not_create_internal_redirect_contexts`;
  Exit 1 mit zehn fehlschlagenden Nicht-Upstream-Konfigurationen, die weiterhin
  `try_files $uri /index.html;` enthielten.
- GREEN: derselbe fokussierte Unittest; Exit 0, ein Test.
- Parent `tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases`;
  Exit 0, 28 Tests.
- Parent-Driver-Tabellenvertrag mit dem exakten Framework-Root; Exit 0, sieben
  Tests. Erweiterte Matrix aus Sequenz, Transport, Dispatcher, H1-Protokoll
  und ausgewähltem Runner-/Authority-Wiring; Exit 0, 90 Tests.
- Framework `tests.no_crs.test_nginx_native_operation_bundle`; Exit 0, 26
  Tests. Seine Exact-one-Cleanup-Ablehnung bleibt unverändert.
- Der benachbarte Parent-Cleanup-/Redirect-Befehl führte 21 Tests aus, endete
  jedoch mit Exit 1, weil der unveränderten C-Fixture
  `NginxErrorPageInterventionTests` ein Stub für das zuvor eingeführte
  `ngx_http_modsecurity_request_completion_log_event` fehlt; die reine
  Source-Assertion zur Redirect-Context-Grenze und die übrigen 20 Tests
  bestanden.
- Das native `ci/tools/new-change-record.py create` erzeugte dieses Paar ab
  der exakten Basis; Exit 0.
- Change-Record-Prüfung, 30 Change-Record-/Sequenztests, zweisprachige
  Dokumentationsprüfung und Repository-Linkprüfung; alle Exit 0.
- Vollständiges Parent-`make lint` in einem frischen externen Build-Root;
  Exit 0, keine `SKIPPED`-, Fehler-, Error- oder Traceback-Markierung. SHA256
  des erhaltenen Logs ist
  `6eac50fee96f663af17c336c4d9f81a94030904c6f788abcdee3e0053b969906`.
- `rtk proxy git diff --check`; Exit 0 nach dem Implementierungsabschnitt.

## Security-Auswirkung

Die Änderung entfernt einen unbeabsichtigten internen Redirect aus
kontrollierten Runtime-Fixtures und verhindert dadurch, dass ein verlassener
zusätzlicher Transaktionskontext als Teil einer logischen Probe erscheint. Sie
lockert keine Event-, Cleanup-, Pfad-, Projektions-, Privileg-, Source- oder
Evidence-Validierung. Die Root-Master/nobody-Worker-Grenze und die
Produktbehandlung echter Redirects bleiben erhalten.

## Runtime-Evidence

R10 bleibt als Fehler-Evidence erhalten: Ein echter HTTP-200-Request hatte
Master-UID 0, Worker-UID 65534 sowie verifizierten Prozess-/Listener-Cleanup
und emittierte danach unter derselben Transaktions-ID zuerst normalen Cleanup,
dann `common_return=-8` / `cleanup_incomplete`. Noch lief keine Post-Fix-Runtime;
daher wird kein lokaler oder Canonical PASS behauptet.

## Bekannte Einschränkungen

Der Unittest beweist die erzeugte Konfiguration, nicht das Live-Verhalten von
NGINX bei Redirects. Nur H1 ist im Umfang. R10 erzeugte kein Canonical
`result.json`, weil die Native-Artefakt-Retention vorher fehlschlug.

## Verbleibende Risiken

Ein frischer Exact-Head-Build und isolierter Request mit
Root-Master/nobody-Worker muss genau einen Cleanup je Transaktion beweisen.
Weitere unabhängige Defekte in Required-Records können nach Beseitigung des
ersten R10-Retention-Fehlers auftreten. Der benachbarte vorbestehende
C-Fixture-Kompilierungsfehler bleibt separat sichtbar.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer NGINX-Build, Post-Fix-Runtime, Canonical-Finalisierung,
Current-Head-CI, Sonar und Delivery liefen noch nicht, weil dieses Record den
Pre-Commit-Implementierungsabschnitt erfasst. Ruff ist nicht als separates
lokales Tool installiert; das repository-native `make lint` bestand. Protected
Exact-Head bleibt wegen seiner unabhängig fehlenden Trusted-Base-, Runner-,
Environment- und administrativen Host-Gate-Voraussetzungen blockiert.

## Finaler Diff- und Review-Status

Der aktuelle Vier-Dateien-Diff ist Parent-only und erhält die Framework-/MRTS-
Gitlinks. Die fokussierte Regression ist auf der Basis RED und nach der
Treiberänderung GREEN; fokussierte, erweiterte, Dokumentations- und vollständige
Parent-Lint-Gates bestehen. Commit, Clean-Head-Validierung, frische Runtime und
Delivery-Prüfung laufen noch. R10 bleibt FAIL und wird weder wiederverwendet
noch umetikettiert.
