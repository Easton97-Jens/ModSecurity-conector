# Change Record: Apache-Helper-aware-Common-Adoption-Contract-Reparatur

**Sprache:** [English](CR-20260904-apache-helper-aware-common-adoption-contract.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260904-apache-helper-aware-common-adoption-contract |
| Datum (UTC) | 2026-09-04 |
| Basis-Revision | 2b3d7f7f0bec006b236b5998d011069c9125033f |
| Delivery-Status | Autorisierte Korrektur-Delivery auf einem fokussierten Branch ausgehend von der genannten Revision. Jeder Commit, normaler Push und jede Draft-PR-Aktion erfordert einen frischen Remote-Preflight. Dieser Record autorisiert keinen Merge. |

## Motivation und Problemstellung

Nach dem Squash-Merge von PR #345 stoppten fünf resultierende-master-Workflows
an demselben Apache/Common-Adoption-Static-Check. Die Produktsource hatte den
P2-Bucket-Pfad aus `input_filter()` nach
`apache_input_filter_process_bucket()` verschoben und den Append-Contract auf
das begrenzte `plan.append_size` umgestellt. Der alte Checker verlangte weiter
das frühere monolithische Token-Layout und wies damit die aktuelle begrenzte
Helper-Architektur ab.

Die Reparatur betrifft nur Checker und Tests. Sie behauptet keine Behebung des
separaten nativen Apache-Reverse-Proxy-P2-Runtime-Problems aus
`FND-PARENT-0986`. Dieses Finding bleibt in Bearbeitung und release-blocking,
bis seine eigenen nativen Controls und Delivered-Head-Evidenz vorliegen.

## Akzeptanzkriterien

- Der Checker folgt dem echten P2-Helper-Aufrufgraphen: Dispatcher,
  Non-EOS-Prozessor, EOS-Handler, Finalizer und Terminal-Error-Bridge.
- Jeder Non-EOS-Bucket erfordert Direct-Body-Read, Limit-Plan, Common-Record,
  begrenzten Append mit `plan.append_size`, Buchhaltung und erst danach den
  Remove-/Forward-Sink.
- EOS verwirft ein Duplikat, finalisiert genau einmal, leitet eine Intervention
  über die Input-Terminal-Bridge und gibt EOS erst danach frei und entfernt den
  Filter.
- Nur Kommentare und Tokens in fremden Funktionen können keine
  Helper-spezifischen Assertions erfüllen.
- Ein Constant-false-Dead-Code-Dekoy kann den P2-Source-to-Sink-Contract nicht
  erfüllen, während der aktive Pfad einen Bucket weiterleitet.
- Enthalten sind keine Apache-Produktsource-, Workflow-, Ruleset-,
  Branch-Protection-, Required-Check-, Quality-Gate-, Exclusion-, Suppression-,
  Framework-, MRTS-, Gitlink- oder PR-#346-Änderung.

## Implementierungsentscheidung und Begründung

`apache_common_adoption_base.py` extrahiert jetzt eine maskierte, ausbalancierte
C-Funktionsdefinition und stellt eine Direct-Body-Projektion bereit, die
verschachtelte Compound-Blöcke maskiert. Der Apache-Review-Checker verwendet
diese lokal begrenzten Ansichten statt eines breiten `msc_filters.c`-Ausschnitts.

Der Non-EOS-Guard verlangt die laufende Pipeline im direkten Funktionsrumpf,
einen direkten kanonischen Success-Tail und verwirft enge mehrdeutige
Control-Konstrukte in kritischen P2-Helpern (Preprocessor-Branches, Labels,
`goto` und offensichtliche Constant-false-Controls). Der EOS-Helper verlangt
ebenfalls genau einen direkten kanonischen Success-Tail. Der Dispatcher muss
den tatsächlichen EOS-Branch unmittelbar gefolgt von der Non-EOS-Processor-
Delegation bewahren. Bestehende Exact-Success-, Terminal-Bridge-, Bounded-
Append- und P3-Fail-Closed-Checks bleiben erhalten.

Dies ist absichtlich ein strenger Source-Contract, keine Behauptung eines
vollständigen C-AST- oder beliebigen Runtime-Reachability-Beweises. Ein
zukünftiger legitimer Helper-Shape-Wechsel muss Checker und Negativ-Controls
bewusst anpassen, statt eine Tokensuche still zu verbreitern.

## Source-to-Contract-Nachweis

| Sicherheitsinvariante | Aktuelle Produktfunktion | Delegierende Call-Site | Veraltete Checker-Annahme | Neuer Checker-Nachweis | Regression-Control |
| --- | --- | --- | --- | --- | --- |
| Non-EOS-Body-Bytes werden begrenzt verarbeitet, bevor sie weitergereicht werden. | `apache_input_filter_process_bucket` | `input_filter` nach dem EOS-Branch | Die gesamte Body-Pipeline liegt lexikalisch in `input_filter`. | Lokal begrenzte Direct-Body-Reihenfolge: Read → Plan → Common-Record → `plan.append_size`-Append → Buchhaltung → ein Remove-/Forward-Tail. | Frühes Forwarding, unbounded Append und Constant-false-Pipeline-Dekoys werden verworfen. |
| P2 wird nur am kanonischen EOS genau einmal finalisiert, und eine Intervention geht der Freigabe voraus. | `apache_input_filter_handle_eos` und `msc_finalize_request_body` | Der `APR_BUCKET_IS_EOS`-Branch in `input_filter` | Finalisierungs- und EOS-Fehler-Tokens liegen im früheren monolithischen Abschnitt. | Ein gescopeter Finalizer-Aufruf, Duplicate-EOS-Bridge, direkter EOS-Release-Tail und kein offensichtlicher Dead-Code-Control. | Entfernte Finalisierung und Constant-false-EOS-Finalisierungs-Dekoys werden verworfen. |
| Input-Fehler scheitern fail-closed über Apache Core statt über einen Output-seitigen Error-Bucket. | `apache_input_filter_terminal_error` | Kontext-, Konfigurations-, Non-EOS- und EOS-Helper-Error-Returns | Terminal-Aufrufe werden nur im alten `input_filter`-Slice gezählt. | Benannte Helper-Scopes erfordern alle drei Caller sowie Statusneutralisierung, `ap_die` und `AP_FILTER_ERROR` im Terminal-Helper. | Fehlende EOS-Delegation/-Bridge sowie Comment-only- und Foreign-function-Token-Dekoys werden verworfen. |

## Security-Auswirkung

Die Source-to-Sink-Grenze sind Request-Body-Daten, die
`apache_input_filter_process_bucket()` betreten und über `APR_BUCKET_REMOVE`
plus `APR_BRIGADE_INSERT_TAIL` verlassen. Die Reparatur bewahrt die Anforderung,
dass der begrenzte Common-Pfad vor diesem Forwarding-Sink erfolgreich sein
muss.

Ein adversariales Review reproduzierte vor der Reparatur einen reinen
Checker-Bypass: Erforderliche Plan-/Record-/Append-/Buchhaltungs- und
Fehler-Tokens innerhalb von `if (0)` ließen den alten lexikalischen Guard
bestehen, während der aktive Pfad einen Bucket ohne diese Controls las und
weiterleitete. Die aktuelle Produktsource enthielt diesen Pfad nicht. Die neuen
Direct-Body- und Terminal-Tail-Checks verwerfen die Reproduktion; die
Regressionssuite enthält Non-EOS- und EOS-Constant-false-Mutationen.

Da keine Produkt-Runtime-Source verändert wird, ändern sich weder
Event-Serialisierung, Body-Payload, Header-, Remote-Rule-, Endpoint-,
Filesystem-, Archiv- noch Runtime-Enforcement-Verhalten.

## Geänderte Dateien

- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `tests/test_apache_common_adoption.py`
- `Makefile`
- `reports/audits/change-records/CR-20260904-apache-helper-aware-common-adoption-contract.md`
- `reports/audits/change-records/CR-20260904-apache-helper-aware-common-adoption-contract.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Pre-Patch direkter Apache-Checker und `make check-apache-common-adoption` | Die zwei genannten veralteten Apache-Assertions gegen Basis `2b3d7f7f0bec006b236b5998d011069c9125033f` reproduziert. |
| Python-Kompilierung der geänderten Checker-/Testdateien | Bestanden. |
| Direkter Apache-Checker | Bestanden, einschließlich Helper-aware-P2-, EOS-, Terminal-Bridge-, Bounded-Append- und P3-Guards. |
| `tests.test_apache_common_adoption` | Bestanden: 10 Tests, einschließlich positiver Architektur und neun Negativmutationen. |
| `make check-apache-common-adoption` | Bestanden. |
| `python3 -m unittest discover -s tests -p 'test_apache*.py' -v` | Bestanden: 69 Tests. |
| Apache-C17-Lint | Außerhalb der Sandbox bestanden, weil der Projektcheck einen festen temporären Probe-Root nutzt. |
| `make check-no-crs-source-normalization` | Nach Initialisierung des bereits gepinnten Framework-Checkouts im isolierten Worktree bestanden: 145 Tests. |
| `make generate-test-matrix` und `make check-test-matrix` | Abgeschlossen; generierte Report-Drift lag außerhalb der Aufgabe und die neun generierten Dateien wurden auf `HEAD` zurückgestellt. |
| Apache-/NGINX-Harness-Shell-Syntax und `make -n`-Smoke-/Runtime-Targets | Bestanden. |
| `make lint` und `make quick-check` | Erreichten und bestanden alle vorherigen Apache-Checks, stoppten danach an zwei unveränderten NGINX-Common-Adoption-Assertions aus bestehendem `FND-PARENT-1010`. Der Candidate-to-Base-Diff für NGINX-Source und -Checker ist leer; hier wird keine NGINX-Änderung vorgenommen. |
| Finaler `git diff --check` und Dokumentationschecks | Nach Hinzufügen des Paars bestanden. |

## Runtime-Evidence

Dies ist eine Source-Contract-Reparatur. Für diese Änderung wurde kein nativer
Apache-Server, Proxy, Request- oder Response-Flow gestartet und kein Request-
oder Response-Body aufbewahrt. Der aktuelle Produkt-P2-Pfad wurde statisch als
Read → Plan → Record → Bounded-Append → Buchhaltung → Forwarding verfolgt;
dieser Nachweis ersetzt keine native P2-Runtime-Validierung.

## Nicht ausgeführte Prüfungen mit Begründung

Es werden kein nativer Apache-P2-Runtime-Replay, keine vollständige P1–P4-
Abnahme, keine vollständige native 17×10-Hostmatrix, keine Sanitizer-Matrix
und kein resultierender-master-Workflow-Rerun behauptet. Sie sind nicht nötig,
um eine Checker-only-Reparatur zu belegen, und bleiben separate
Evidenzpflichten. Exact-Pushed-Head-GitHub-Actions, SonarQube-Cloud- und
Review-Evidenz stehen ebenfalls aus, bis der autorisierte Draft-PR existiert.

## Bekannte Einschränkungen

Der Checker verwirft den reproduzierten Dead-Code-Bypass und macht die
erforderliche P2-Form explizit, ist aber kein vollständiger C-Parser oder
Beweis beliebiger Makro- und Runtime-Reachability. Ein künftiges
Source-Refactoring kann legitimerweise ein bewusstes Checker-/Test-Update
erfordern.

## Verbleibende Risiken

Die Aufgabe löst weder die native HTTP-500/HTTP-403-Übersetzungsfrage aus
`FND-PARENT-0986` noch den separaten Master-NGINX-Checkerfehler aus
`FND-PARENT-1010`; letzterer blockiert die lokalen Aggregate `make lint` und
`make quick-check` vor späteren Controls.

## Finaler Diff- und Review-Status

Der Delivery-Diff enthält keine Apache-Runtime-Source-, Workflow-, Governance-
oder Generated-Report-Änderung. Dieser Pre-Delivery-Static-Record behauptet
keinen Commit, Push, Draft-PR, Exact-Head-Hosted-Check, SonarQube-Cloud-
Ergebnis, Ready-for-Review-Status oder Merge; diese Delivery-Fakten erfordern
unabhängige Exact-Head-Evidenz.

Ein unabhängiges finales Read-only-Security-Diff-Review führte die zwei
Constant-false-Dekoys, die Zehn-Test-Mutationssuite, den direkten Apache-
Checker und `git diff --check` erneut aus. Es fand keinen weiteren bestätigten
Security-Befund und bestätigte, dass die Produkt-Runtime-Source unverändert
ist. Seine verbleibende Notiz ist dieselbe deklarierte Checker-Grenze:
Beliebiger nichtkonstanter C-Control-Flow und Makrosemantik werden durch diesen
Static-Contract nicht bewiesen.
