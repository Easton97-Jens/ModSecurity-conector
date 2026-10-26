# Change Record: CR-20261026-ubuntu26-workflow-migration

**Sprache:** [English](CR-20261026-ubuntu26-workflow-migration.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261026-ubuntu26-workflow-migration |
| Datum (UTC) | 2026-10-26 |
| Basis-Revision | `542a98bc20a16f885f114375bfa5225a9364dcf2` |

## Motivation und Problemstellung

Der Benutzer verlangt Ubuntu 26 für Connector- und Framework-Actions. Hosted-Runner-Labels explizit pinnen und geschütztes Self-hosted-Routing erhalten.

## Akzeptanzkriterien

Alle aktiven Hosted-Runner-Felder in Parent und Framework deklarieren ubuntu-26.04; geschützte Self-hosted-Runner behalten ihre expliziten Labels. Gates, unveränderliche Vertrauens-Pins und begrenzte Connector-E2E erhalten. Frische Hosted-CI muss vor Abschluss die Kompatibilität belegen.

## Implementierungsentscheidung und Begründung

Der aktuelle Parent-Baum enthält 66 tatsächliche runs-on-Felder in 34 Workflow-Dateien: 64 ubuntu-26.04 und zwei geschützte Self-hosted-Listen. Der neue native Security-Workflow ergänzt zwei Hosted-Felder. Die getrennt veröffentlichte Framework-Revision `5bffa21d3dd49d3ca647e89eebe005b8421b0812` enthält 31 ubuntu-26.04-Felder in 18 Workflows. Der Parent-Framework-Gitlink bleibt unverändert. Exakte ergänzende actionlint-Labels und gezielte Runner-Vertragserwartungen folgen dieser Migration.

## Geänderte Dateien

Parent-Runner-Deklarationen in `.github/workflows/`, `.github/actionlint.yaml`, gezielte Workflow-/Toolchain-Verträge samt Fixtures sowie zweisprachige Sonar-Analyse-/Native-Leitfäden. Framework-Änderungen gehören zum getrennten PR #138. Dieser Record dokumentiert die Integration und beansprucht keine Ownership der übrigen nativen Security-Implementierung.

## Ausgeführte Befehle

Tatsächliche runs-on-Felder beider aktiver Worktrees mit schreibgeschützter Python-Auswertung über RTK gezählt. Native Change-Record-Vorlage mit ci/tools/new-change-record.py erzeugt. Für diese Dokumentationsänderung keine funktionalen Tests ausgeführt.

Die integrierte Auswahl nach Master-Übernahme bestand **94 Ausführungen / 342 expandierte Fälle ohne Skips**, beim Inventar `e13c73b981fd1399fbe0c161a8abd753d6cbc4d429957caa86d7c33e1f59bf7c`. Das Inventar deklariert 1992 Fälle / 918 Ausführungen: 97 Kernfälle / 77 Ausführungen plus 1895 autorisierte Offline-Fälle / 841 Ausführungen, mit 614 Quellbindungen und 1.672.802 Bytes. Die Auswahl enthält acht Inventarkontrollen einschließlich Überlauf-Abweisung und sieben Broker-Selektoren / 36 Fälle sowie korrigierte Helper-Capture-Pfad- und isolierte NGINX-Archivvertragskontrollen. Das frühere PASS 79/298 bei `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be` ist ein Vor-Merge-Zwischenstand. Lokale grüne Ergebnisse belegen keine Hosted-Native12-Analyse.

## Security-Auswirkung

Der benutzerfreigegebene Broker-[PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422) wurde regulär vom erwarteten Head `3d633ee27b48b64b940042e278c157f1aa629679` nach Master-Revision `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` gesquasht; Provider-Readback bestätigte den Merge. Unabhängiges finales Review aller sieben Dateien fand keinen konkreten Befund. Alle sechs PR-Ruleset-Prüfungen und terminalen C++17/20/23-Sonar-Ergebnisse bestanden an genau diesem PR-Head. Der Parent-Aufrufer pinnt jetzt Broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` und dessen tatsächliches Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; der Parent-Gitlink bleibt unverändert. Geschützte Self-hosted-Labels und Masters einheitlicher Runner-Validator bleiben erhalten; die doppelte Coverage-Ausschlussproperty wurde auf eine Deklaration reduziert. Kein geschützter manueller Broker-Lauf oder erweiterter Connector-E2E wurde gestartet. Die Autorisierung umfasste nur #422 und den anschließenden Aufrufer-Pin, keinen #382-Merge.

Alle sechs Master-Ruleset-Prüfungen bestanden bei `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`. Masters C++17-Sonar scheiterte tatsächlich mit Security E / Reliability E gegen eine `previous_version`-Baseline vom 14. Mai; die schreibgeschützte Prüfung fand 20 bereits bestehende Security-/Reliability-Befunde, keinen durch #422 eingeführten; fünf native Auslöser sind in #382 bereits entfernt. Kein bestandenes Master-Sonar-Gate wird behauptet. Diese Master-Ergebnisse bleiben von der erfolgreichen Analyse des exakten PR-Heads getrennt. Der PR-Liefernachweis muss den exakten Parent-Native12-/Ubuntu-Commit und frische CI binden, ohne ältere Erfolge zu übertragen.

## Runtime-Evidence

Keine neuen Parent-Hosted-Ubuntu-26-Laufzeitnachweise. Zwölf native Entwicklungs-Captures enthalten zusammen 611 Parent-TU-Kompilierungen, keine eindeutigen Dateien oder Hosted-Analyse. Der Koordinator meldet 34 lokale Ausführungen / 98 expandierte Fälle erfolgreich beim Vor-Ubuntu-Inventar `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578`. Diese Ergebnisse übertragen sich nicht auf die geänderte Runner-Umgebung.

Der getrennte [Framework-Draft-PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) ist jetzt bei `5bffa21d3dd49d3ca647e89eebe005b8421b0812` veröffentlicht und behält 31 Ubuntu-26.04-Runner-Felder. Der Koordinator bestand 86 lokale Methoden ohne Skips; beim letzten Readback waren zehn von zwölf CI-Workflows erfolgreich, Sonar-SDK- und Scaffold-Prüfungen standen aus. Die frühere Analyse von `5ef4dc3c815c97121578cd34382b80088b9c61ec` führte C-/Python-Taint tatsächlich aus und ihr Gate wurde nach quellbasiertem False-positive-Readback `OK`; das Ergebnis ist für den neuen Head veraltet. Kein aktuelles finales Framework-Gate oder Parent-Gitlink-Import wird behauptet.

## Bekannte Einschränkungen

Der aktuelle uncommittete Ubuntu-/Native12-Stand besitzt keinen Hosted-Nachweis am veröffentlichten Head. Framework-Lieferung bleibt getrennt und wird durch den unveränderten Parent-Gitlink nicht importiert. Historische I12-Host-, Matrix- und Oracle-Kampagnen bleiben geschlossen.

## Verbleibende Risiken

Abweichende Ubuntu-Images und Toolchains können Regressionen aufdecken; lokale Quellzählungen und Offline-Prüfungen belegen keinen aktuellen Hosted-Native12- oder geschützten Laufzeiterfolg.

## Nicht ausgeführte Prüfungen mit Begründung

Frische Parent-Ubuntu-26-Hosted-Workflows, Native12-Analyzer-/Serverabschluss und geschützte Broker-Ausführung stehen aus. Der Dokumentationsagent führte keine funktionalen Tests, Dienste, Host-/Matrix-/Oracle-/I12-Kampagnen oder Provider-Schreibzugriffe aus.

## Finaler Diff- und Review-Status

Die Dokumentation ist für Roots Prüfung zusammen mit dem aktuellen Integrationsdiff vorbereitet. Der Abschluss bleibt von frischer einschlägiger Validierung und der frischen Prüfung der integrierten Broker-Pins abhängig.
