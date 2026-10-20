# Change Record: CR-20261020-i12-apache-sonar-remediation

**Sprache:** [English](CR-20261020-i12-apache-sonar-remediation.md) | Deutsch

Apache-spezifische Bereinigung des Abnahme-Harness in Draft-PR #414. Dieser Bericht beschreibt Quelländerungen und lokale Validierung; er gibt keinen Apache-Runtime-Fall frei.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261020-i12-apache-sonar-remediation |
| Datum (UTC) | 2026-10-20 |
| Basis-Revision | `fe2c30f710a26e3ea7ef0dcc2b847e3fb093deb6` |

## Motivation und Problemstellung

Die vollständige SonarQube-Cloud-Abfrage für PR #414 an der Basis-Revision enthält 179 unterschiedliche ungelöste Issues: 11 Vulnerabilities und 168 Code Smells mit 495 sekundären Flow-Positionen. GitHub zeigte nur 50 Anmerkungen. Maßgeblich ist die Analyse `eb509cd6-12be-445f-b81b-c966be977bc3`, CE-Task `AaFOsW5SEA5tm64SJa9s`, vom `2026-10-18T11:04:17Z`. Anmerkungszahlen belegen daher kein vollständiges Issue-Inventar.

Die Änderung bearbeitet Eingabeprüfung, Ressourcenfreigabe und Wartbarkeit des Apache-Test-Harness unter Erhalt der tatsächlichen SDK-/APR-Aufrufe und ursprünglichen Abnahmeverträge. Eine neue Cloud-Analyse muss zeigen, welche Findings behoben sind.

## Akzeptanzkriterien

Die 155 ursprünglichen Apache-IDs, ihre Original-Oracles und historischen Fehler bleiben erhalten; echte SDK-/APR-Ergebnisse und physisches Fehlerverhalten bleiben erhalten. Dateisystemeingaben müssen begrenzt und identitätsgeprüft sein, private HTTP-Endpunkte auf die zugelassene Loopback-/High-Port-Grenze beschränkt und eigene Descriptoren auch bei Ausnahmen freigegeben werden. Relevante lokale Regressionen müssen bestehen; vor einer Sonar-Abschlussbehauptung muss eine spätere Analyse an den tatsächlich veröffentlichten Commit gebunden sein. Host-Abnahme erfordert weiterhin neue, vollständig qualifizierte Ausführungsnachweise.

## Implementierungsentscheidung und Begründung

Der Observed-Module-Builder prüft kanonische Wurzeln und Elternpfade, verwirft Symlinks und ungültige Dateitypen, liest über begrenzte `O_NOFOLLOW`-/`O_CLOEXEC`-Descriptoren und parst/hasht dieselben geprüften Bytes. Er erhält den exakten Vertrag mit 28 Wrappern, Prüfungen definierter ELF-Symbole und die SDK-Bindung.

Python-Request-Framing, Response-Parsing, Fallauswahl, Backend-Verarbeitung und Batch-Erfassung werden in gezielte Hilfsfunktionen aufgeteilt. Konstanten ersetzen wiederholte Literale. Die Portfreigabe wird an CLI- und Socket-Grenzen geprüft. Direkte Child-Cancellation erhält Beendigung und Reaping bei beliebigen `BaseException`-Ausnahmen. Native Refactorings erhalten echte Rückgaben, `errno`, Weiterleitung und Cleanup-Reihenfolge. Der Multipart-Observer nutzt RAII für Descriptor-Cleanup und feste Diagnosen bei Allokationsfehlern; ein nativer Prozesstest prüft C++17-`steady_clock`-Zeitstempel gegen die tatsächliche monotone Linux-Epoche.

Es gibt keine Scanner-Unterdrückung, keinen reduzierten Testvertrag, keinen TLS-Ersatz und keine Erhöhung des Sprachstandards zur Erzeugung eines PASS. Privates unverschlüsseltes HTTP bleibt Bestandteil des Apache-Testvertrags; entsprechende Findings benötigen eine neue serverseitige Bewertung oder bleiben ausdrücklich offen.

## Geänderte Dateien

Alle folgenden Implementierungspfade liegen unter `ci/runtime/lifecycle/apache-i12/`:

- `acceptance/backend.py`, `acceptance/batch.py`, `acceptance/build_fault_boundary.py`, `acceptance/build_host_io.py`, `acceptance/build_observed_module.py`, `acceptance/cancellation.py`, `acceptance/cases.py`, `acceptance/keepalive.py`, `acceptance/review_batch.py`, `observed_curl.py`.
- `acceptance/common_sink_boundary.c`, `acceptance/fault_boundary.c`, `acceptance/host_bucket.c`, `acceptance/host_io.c`, `acceptance/multipart_observer.cpp`.
- Tests unter `tests/`: `test_apache_i12_acceptance_driver.py`, `test_apache_i12_acceptance_oracles.py`, `test_apache_i12_backend.py`, `test_apache_i12_boundaries.py`, `test_apache_i12_cancellation.py`, `test_apache_i12_keepalive.py`, `test_apache_i12_multipart_observer.py`, `test_apache_i12_observed_module_builder.py`.
- Dieser deutsche Bericht und `CR-20261020-i12-apache-sonar-remediation.md`.

Zentrale Matrizen, Berichtgeneratoren, Capture-Manifeste, gemeinsame Observer, produktiver Connector-Code, Workflows und Framework-/MRTS-Gitlinks liegen außerhalb dieser Änderung.

## Ausgeführte Befehle

Befehle verwenden RTK und die vorhandene Python-Umgebung. Arbeitsverzeichnis: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-apache-410-20261015`.

| Verfahren | Beobachtetes Ergebnis und Umfang |
| --- | --- |
| `rtk proxy /usr/local/bin/sonar-with-env api get '/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=414&ps=500&p=1&resolved=false'` | Vollständiges Inventar der Basis-Analyse: 179 Issues; keine neue Analyse der Bereinigung. |
| Apache-I12-Unittest-Discovery vor dem abschließend erweiterten Refactoring | 255 Tests, Exit 0, 3 ausdrückliche Opt-in-/DAC-Skips. |
| Fokussierte Unittests für Acceptance-Cases/-Driver, Keepalive, Cancellation, Backend und Observed-Builder nach dem Python-Refactoring | 118 Tests, Exit 0. |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_apache_i12_common_sink_boundary tests.test_apache_i12_fault_boundary tests.test_apache_i12_host_bucket tests.test_apache_i12_host_io tests.test_apache_i12_multipart_observer` | 67 Tests, Exit 0, 1 Root-DAC-Skip; abschließender nativer Helper-Wiederholungslauf. |
| Batch-Review-Opt-ins mit tatsächlichem Capture | 8 Tests, Exit 0, keine Skips; vorherige Validierungsstufe. |
| Sonar-Strict-Gate-Vertragstests | 44 Tests, Exit 0; vorherige Validierungsstufe. |
| Apache-Native-/Header-/Common-Regressionen | 67 Tests, Exit 0, 1 erwarteter Skip; vorherige Validierungsstufe. Beim ersten Setup fehlte das externe `RUNNER_TEMP`-Verzeichnis; maßgeblich ist der Wiederholungslauf nach dessen Erstellung. |
| Abschließende Apache-I12-Unittest-Discovery nach allen Quellkorrekturen | 269 Tests, Exit 0, 3 ausdrückliche Opt-in-/Root-DAC-Skips. Dies ist der maßgebliche gemeinsame lokale Lauf. |
| Batch-Review-Opt-ins mit tatsächlichem Capture nach den abschließenden Quellkorrekturen | 8 Tests, Exit 0, keine Skips. Zwei vorherige Aufrufe wählten den falschen beibehaltenen Spec-Pfad und scheiterten vor der Extraktion; maßgeblich ist der Lauf mit der versuchseigenen `2-smoke-spec-v2.json`. |
| Separater Common-Sink-Boundary-Lauf unter UID/GID `65534` nach den C-Änderungen | 9/9 Tests bestanden, Exit 0, einschließlich echtem `EACCES`/`errno 13` am schreibgeschützten Elternverzeichnis; Evidence liegt unter `/var/tmp/codex/ModSecurity-conector/nonroot-common-boundary-414-20261020-v2/evidence`. |
| Breite Auswahl von Sonar-Gate-, Reliability- und Helpertests | 61 Tests ausgeführt, Exit 1: 60 bestanden; das bestehende HAProxy-Append-String-Linkfixture scheiterte an nicht aufgelösten Common-/Authorization-Symbolen. Dieser Integrationsfehler eines anderen Connectors liegt außerhalb der Apache-Änderung und wurde weder verborgen noch verändert. |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` | Exit 0; nur Change-Record-Struktur, keine Evidence-Validierung. |
| `rtk proxy make check-bilingual-docs` mit Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` nur-lesbar an der Gitlink-Position | Exit 0, `bilingual docs ok`. Der erste direkte Checkout-Versuch zeigte nur den absichtlich nicht ausgecheckten Worktree-Gitlink; maßgeblich ist der Read-only-Wiederholungslauf mit exaktem Pin. |
| `rtk proxy make check-doc-links` im selben nur-lesbaren Namespace mit exaktem Pin | Exit 0; Repository-Pfadverweise und Dokumentlinks bestanden. |
| `rtk proxy git diff --check` | Exit 0 nach Ausfüllen dieses Berichtspaars. |

Der native Helper-Beleg liegt unter `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/native-sonar-remediation-20261020.json`. Er erfasst 48 tatsächliche Allokationsfehler-Budgets, null Descriptor-Lecks, erhaltenes `errno` und die feste Fehlerdiagnose. Ein unabhängiges Abschlussreview reproduzierte zwei Regressionen des Kandidaten bei CLI-Portkonvertierung und Child-Exit-Behandlung; beide wurden korrigiert und erneut geprüft. Der Reviewer fand im abschließenden Code-Diff keine verbleibende konkrete blockierende Abweichung. Die Cloud-Analyse des exakt veröffentlichten Heads muss die integrierende Aufgabe noch erfassen.

## Security-Auswirkung

Dies ist defensive Test-/Build-/Evidence-Arbeit im ausdrücklich autorisierten privaten Umfeld. Die TAC-Abfrage meldete am `2026-10-18` `granted`, Stufe `tac1`, Quelle `user`; die Aufgabe behandelt dies als die vom Nutzer beschriebene DrayTek-Blue-Grenze ohne zusätzliche Berechtigungen abzuleiten. Private Controller-Isolation, Identitätsprüfungen, Berechtigungen, Redaktion und Quality Gates bleiben erforderlich.

Dateisystemfreigabe und Ausnahme-Cleanup verringern Risiken durch Harness-Missbrauch und Evidence-Austausch. Diese Quelländerungen belegen keine produktive Schwachstelle oder deren Behebung. Unabhängig bestätigte produktive Apache-Fehler benötigen einen getrennt freigegebenen Fix auf #382.

## Runtime-Evidence

Diese Bereinigung behauptet keinen neuen vollständig qualifizierten Host-PASS und keine Lösung eines Original-Oracles. Helper-/Unittests belegen nur ihre eigene Schicht. Das historische Inventar bleibt bei 155 IDs: 10 Config- und 145 Host-Fälle; 28 ausgeführt, 8 vollständig qualifizierte PASS, 20 teilweise und 127 nicht ausgeführt. Es gibt 54 ursprünglich offene Apache-Oracle-Mitglieder. Das unabhängige Quellenreview ergab 41 bedingte Vorschläge, 13 Lücken und null neu genehmigte Lösungen.

Neue Builds des abschließenden Quellstands, geladene Binary-/Config-/SDK-/Run-Identitäten, private Host-Ausführung und semantische Qualifikation jedes Falls bleiben erforderlich. Fehlende Beobachtungen bleiben `null` oder offen. `I12_COMPLETE` wird nicht behauptet.

## Bekannte Einschränkungen

Das vollständige Inventar mit 179 Issues gehört zur alten Basis-Analyse. Lokale Quellbereinigung belegt kein grünes Cloud-Gate, null neue Findings oder den Abschluss absichtlicher Loopback-HTTP-/C++17-Empfehlungen. Die 118 Python- und 67 nativen Tests decken unterschiedliche Teilmengen ab; ihre Zahlen dürfen nicht zu einem vollständigen gemeinsamen Lauf addiert werden. Der Root-DAC-Skip benötigt den separaten Nonroot-Test und einen neuen Lauf bei Änderungen seiner Implementierung.

## Verbleibende Risiken

Refactoring von Framing-, Ausnahme- und Observer-Pfaden kann weiterhin Verhalten außerhalb der lokal ausgeführten Pfade beeinflussen. Der Apache-Abnahme fehlen weiterhin vollständige aktuelle Run-Qualifikation für alle Pflichtfälle und unabhängige Freigabe der Original-Oracle-Vorschläge. Gemeinsamer Ledger-Dispatch für Config-/Pre-Native-/Host-Qualifikation bleibt Integrationsbedarf; diese Änderung verändert den zentralen Generator nicht. Der unabhängige HAProxy-Fixture-Linkfehler bleibt ebenfalls ein zentraler beziehungsweise Connector-Integrationsbedarf außerhalb des erlaubten Apache-Dateiumfangs.

## Nicht ausgeführte Prüfungen mit Begründung

In dieser lokalen Validierungsstufe des Berichts sind eine neue commitgebundene Cloud-Analyse und eine neue Host-Kampagne mit 155 Fällen noch nicht nachgewiesen. Die integrierende Aufgabe muss sie ausführen und berichten. Für die autorisierte defensive lokale Arbeit besteht kein Berechtigungsblocker; dies sind fehlende Ausführungsnachweise und keine behauptete Sicherheitsverweigerung.

## Finaler Diff- und Review-Status

Die Bereinigung ist ein uncommitteter Kandidat relativ zum vollständigen Basis-SHA oben. Ein unabhängiges Abschlussreview deckte den erweiterten Diff ab, fand die beiden oben erfassten Regressionen und verifizierte ihre Korrekturen; es fand keine verbleibende konkrete blockierende Security- oder Verhaltensabweichung. Normale Commits/Pushes und Zielbranch-Integration sind autorisiert; hier werden weder ein veröffentlichter Bereinigungs-SHA, erfolgreiche commitgenaue CI-/Sonar-Prüfung noch ein PR-Merge behauptet. Abschließende Lieferung und Runtime-Qualifikation werden in der integrierenden Aufgabe getrennt verfolgt.
