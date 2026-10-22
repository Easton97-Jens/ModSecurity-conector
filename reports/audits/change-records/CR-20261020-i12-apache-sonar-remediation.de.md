# Change Record: CR-20261020-i12-apache-sonar-remediation

**Sprache:** [English](CR-20261020-i12-apache-sonar-remediation.md) | Deutsch

Apache-spezifische Bereinigung des Abnahme-Harness in Draft-PR #414. Dieser Bericht beschreibt Quelländerungen und lokale Validierung; er gibt keinen Apache-Runtime-Fall frei.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261020-i12-apache-sonar-remediation |
| Datum (UTC) | 2026-10-20 |
| Basis-Revision | `fe2c30f710a26e3ea7ef0dcc2b847e3fb093deb6` |
| Apache-Bereinigungscommit | `ee68b78f4f802149ed6d864a32ff5198e8c0596b` |
| Weiterer Sonar-Bereinigungscommit | `33e89e8ad636787a5c9a19eafbbe9bc8eaadabd1` |
| Ausgeführter Produktquell-Head | `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38` |
| Veröffentlichter Head der finalen Prüfhärtung | `de23f2fa4b490c66f15ac97f2646434351f05c5e` |
| PR-#410-Zielbranch-Head bei der finalen Prüfung | `76672071c3f7665dfde3340bef9e64271d6f6e70` |

## Motivation und Problemstellung

Die vollständige SonarQube-Cloud-Abfrage für PR #414 an der Basis-Revision enthält 179 unterschiedliche ungelöste Issues: 11 Vulnerabilities und 168 Code Smells mit 495 sekundären Flow-Positionen. GitHub zeigte nur 50 Anmerkungen. Maßgeblich ist die Analyse `eb509cd6-12be-445f-b81b-c966be977bc3`, CE-Task `AaFOsW5SEA5tm64SJa9s`, vom `2026-10-18T11:04:17Z`. Anmerkungszahlen belegen daher kein vollständiges Issue-Inventar.

Die Änderung bearbeitet Eingabeprüfung, Ressourcenfreigabe und Wartbarkeit des Apache-Test-Harness unter Erhalt der tatsächlichen SDK-/APR-Aufrufe und ursprünglichen Abnahmeverträge. Eine neue Cloud-Analyse muss zeigen, welche Findings behoben sind.

Die nachfolgende revisionsgebundene Cloud-Analyse für `a36f9831cb34532d388d2da9a787b25268721b74` meldete weiterhin 22 ungelöste Issues. Dies ist eine getrennte Analyse zum historischen Inventar mit 179 Issues, kein Nachweis einer unabhängig geprüften Schließung jeder Differenz. Commit `33e89e8ad636787a5c9a19eafbbe9bc8eaadabd1` bearbeitet diese Quell-Findings. Spätere Commits und die aktuelle Runtime-Kampagne beweisen für sich kein grünes Cloud-Gate; exakte Head-CI und Serveranalyse bleiben getrennte Liefernachweise.

## Akzeptanzkriterien

Die 155 ursprünglichen Apache-IDs, ihre Original-Oracles und historischen Fehler bleiben erhalten; echte SDK-/APR-Ergebnisse und physisches Fehlerverhalten bleiben erhalten. Dateisystemeingaben müssen begrenzt und identitätsgeprüft sein, private HTTP-Endpunkte auf die zugelassene Loopback-/High-Port-Grenze beschränkt und eigene Descriptoren auch bei Ausnahmen freigegeben werden. Relevante lokale Regressionen müssen bestehen; vor einer Sonar-Abschlussbehauptung muss eine spätere Analyse an den tatsächlich veröffentlichten Commit gebunden sein. Host-Abnahme erfordert weiterhin neue, vollständig qualifizierte Ausführungsnachweise.

## Implementierungsentscheidung und Begründung

Der Observed-Module-Builder prüft kanonische Wurzeln und Elternpfade, verwirft Symlinks und ungültige Dateitypen, liest über begrenzte `O_NOFOLLOW`-/`O_CLOEXEC`-Descriptoren und parst/hasht dieselben geprüften Bytes. Er erhält den exakten Vertrag mit 28 Wrappern, Prüfungen definierter ELF-Symbole und die SDK-Bindung.

Python-Request-Framing, Response-Parsing, Fallauswahl, Backend-Verarbeitung und Batch-Erfassung werden in gezielte Hilfsfunktionen aufgeteilt. Konstanten ersetzen wiederholte Literale. Die Portfreigabe wird an CLI- und Socket-Grenzen geprüft. Direkte Child-Cancellation erhält Beendigung und Reaping bei beliebigen `BaseException`-Ausnahmen. Native Refactorings erhalten echte Rückgaben, `errno`, Weiterleitung und Cleanup-Reihenfolge. Der Multipart-Observer nutzt RAII für Descriptor-Cleanup und feste Diagnosen bei Allokationsfehlern; ein nativer Prozesstest prüft C++17-`steady_clock`-Zeitstempel gegen die tatsächliche monotone Linux-Epoche.

Es gibt keine Scanner-Unterdrückung, keinen reduzierten Testvertrag, keinen TLS-Ersatz und keine Erhöhung des Sprachstandards zur Erzeugung eines PASS. Privates unverschlüsseltes HTTP bleibt Bestandteil des Apache-Testvertrags; entsprechende Findings benötigen eine neue serverseitige Bewertung oder bleiben ausdrücklich offen.

Die Folgeänderung erhält native Funktionsadressen für Identitätsprüfungen und nutzt gewöhnliche Funktionszeigeraufrufe; sie vereinfacht den C++17-Multipart-Observer ohne Änderung seines Beobachtungsvertrags. Der Python-Builder nutzt begrenzte, benannte Validierungsschritte; das Backend erhält den zugelassenen Loopback-HTTP-Vertrag, und Tests führen Assertions ausdrücklich in Ist-/Soll-Reihenfolge aus.

Apache-Ledger und -Paketierung leiten Config-Controls, Pre-Native-Hostablehnungen und Lifecycle-Pakete nun an ihre jeweiligen vorhandenen gemeinsamen Validatoren weiter. Additive Felder `fresh_qualification_scope`, `fresh_case_qualified`, `fresh_case_outcome` und `fresh_case_qualified_pass` sowie getrennte Config-/Pre-Native-/Fallzähler erhalten den Qualifikationsumfang. Ein Control-PASS wird niemals zum Lifecycle-PASS: Lifecycle-Felder bleiben bei fehlender Lifecycle-Qualifikation false oder `null`. Dieser Dispatch liefert weder fehlende semantische Prädikate noch eine Freigabe unsignierter Review-Kandidaten.

## Geänderte Dateien

Alle folgenden Implementierungspfade liegen unter `ci/runtime/lifecycle/apache-i12/`:

- `acceptance/backend.py`, `acceptance/batch.py`, `acceptance/build_fault_boundary.py`, `acceptance/build_host_io.py`, `acceptance/build_observed_module.py`, `acceptance/cancellation.py`, `acceptance/cases.py`, `acceptance/keepalive.py`, `acceptance/review_batch.py`, `observed_curl.py`.
- `acceptance/common_sink_boundary.c`, `acceptance/fault_boundary.c`, `acceptance/host_bucket.c`, `acceptance/host_io.c`, `acceptance/multipart_observer.cpp`.
- `ledger.py`, `package.py` mit `tests/test_apache_i12_ledger.py` und `tests/test_apache_i12_package.py`.
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
| Frühere Apache-I12-Unittest-Discovery | 269 Tests, Exit 0, 3 ausdrückliche Opt-in-/Root-DAC-Skips; als gemeinsamer lokaler Lauf durch die unten erfasste Validierung mit 287 Tests abgelöst. |
| Batch-Review-Opt-ins mit tatsächlichem Capture nach den abschließenden Quellkorrekturen | 8 Tests, Exit 0, keine Skips. Zwei vorherige Aufrufe wählten den falschen beibehaltenen Spec-Pfad und scheiterten vor der Extraktion; maßgeblich ist der Lauf mit der versuchseigenen `2-smoke-spec-v2.json`. |
| Separater Common-Sink-Boundary-Lauf unter UID/GID `65534` nach den C-Änderungen | 9/9 Tests bestanden, Exit 0, einschließlich echtem `EACCES`/`errno 13` am schreibgeschützten Elternverzeichnis; Evidence liegt unter `/var/tmp/codex/ModSecurity-conector/nonroot-common-boundary-414-20261020-v2/evidence`. |
| Breite Auswahl von Sonar-Gate-, Reliability- und Helpertests | Erster integrierter Lauf: 60 bestanden; ein veraltetes HAProxy-Fixture scheiterte beim Linken, Exit 1. Die reine Fixturekorrektur wurde unabhängig geprüft, zentral als `92cd1133ceb3de1afee0e935be167dac39673a8c` auf #410 veröffentlicht und normal übernommen. Exakter integrierter Wiederholungslauf: 61 Tests bestanden, Exit 0. |
| Eingehende Zielbranch-Regressionen | Lighttpd-Response-Splice/Empty-EOS: 2 Tests bestanden, Exit 0. Gemeinsames Config-/Lifecycle-/Pre-Native-Ledger: 40 Tests bestanden, Exit 0. |
| Gemeinsame Apache-I12-Discovery nach Sonar-Folgekorrekturen und typisiertem Dispatch | Insgesamt 287 Tests: 284 PASS, 3 ausdrückliche Opt-in-/Root-DAC-Skips, Exit 0. |
| Apache-Ledger-/Paketierungstests nach typisiertem Dispatch | 34 Tests bestanden, Exit 0; einschließlich Control-/Lifecycle-Trennung und Mutationsablehnung. |
| Wiederholung der gemeinsamen Config-/Lifecycle-/Pre-Native-Ledger-Regression | 40 Tests bestanden, Exit 0. |
| Wiederholung der nativen Helper-Regression | Insgesamt 67 Tests, Exit 0, einschließlich 1 Root-DAC-Skip; separate Ausführung unter UID/GID `65534` mit 9/9 bestanden. |
| Opt-ins mit beibehaltenem Capture nach der Folgeänderung | 8/8 bestanden, Exit 0. Ein Aufruf wählte die `all-v2`-Spec und scheiterte im Setup wegen `15 != 3`; maßgeblich ist der korrigierte, an den Spec-Hash gebundene `smoke-v2`-Wiederholungslauf. Der Setup-Fehler bleibt erhalten und ist weder Host-Fallfehler noch PASS. |
| Frische private Kampagne aller 155 Fälle an Produktquelle `57e94983...` | Controller und Kandidat Exit 0, kein Timeout, 155 erfasste Haupt-/Control-Ausführungen, vollständiges Controller-Cleanup. Diese Zahl bedeutet weder 155 vollständige Fallverträge noch PASS-Ergebnisse. |
| Abschließende Apache-I12-Discovery nach Prüfhärtung | Insgesamt 387 Tests, Exit 0, mit 5 ausdrücklichen Opt-in-/Root-DAC-Skips. |
| Fokussierte Batch-/Abschlussprüfungs-Suite | Insgesamt 52 Tests, Exit 0, mit 2 ausdrücklichen Opt-in-Skips. |
| Aktuelle Native-Helper-Regression | Insgesamt 67 Tests, Exit 0, mit 1 Root-DAC-Skip. |
| Aktuelle gemeinsame Lifecycle-Ledger-Regression | 40 Tests bestanden, Exit 0. |
| Freigegebene abschließende Einzelfallprüfung | 155 Entscheidungen, 4 vollständige Lifecycle-PASS, 151 null/offen, `i12_complete=false`; Validierung durch das unveränderte gemeinsame Ledger mit Exit 0. |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` | Exit 0; nur Change-Record-Struktur, keine Evidence-Validierung. |
| `rtk proxy make check-bilingual-docs` mit Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` nur-lesbar an der Gitlink-Position | Exit 0, `bilingual docs ok`. Der erste direkte Checkout-Versuch zeigte nur den absichtlich nicht ausgecheckten Worktree-Gitlink; maßgeblich ist der Read-only-Wiederholungslauf mit exaktem Pin. |
| `rtk proxy make check-doc-links` im selben nur-lesbaren Namespace mit exaktem Pin | Exit 0; Repository-Pfadverweise und Dokumentlinks bestanden. |
| `rtk proxy git diff --check` | Exit 0 nach Ausfüllen dieses Berichtspaars. |

Der native Helper-Beleg liegt unter `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/native-sonar-remediation-20261020.json`. Er erfasst 48 tatsächliche Allokationsfehler-Budgets, null Descriptor-Lecks, erhaltenes `errno` und die feste Fehlerdiagnose. Ein unabhängiges Abschlussreview reproduzierte zwei Regressionen des Kandidaten bei CLI-Portkonvertierung und Child-Exit-Behandlung; beide wurden korrigiert und erneut geprüft. Der Reviewer fand im begrenzten Diff des abschließenden Prüfverfahrens keine verbleibende konkrete blockierende Abweichung. Die exakte Head-Cloud-Analyse bleibt vom Host-Evidence-Ergebnis getrennt.

## Security-Auswirkung

Dies ist defensive Test-/Build-/Evidence-Arbeit im ausdrücklich autorisierten privaten Umfeld. Die frische TAC-Abfrage meldete am `2026-10-22T20:59:23.107554+00:00` `granted`, Stufe `tac1`, Quelle `user`; die Aufgabe behandelt dies als die vom Nutzer beschriebene DrayTek-Blue-Grenze ohne zusätzliche Berechtigungen abzuleiten. Private Controller-Isolation, Identitätsprüfungen, Berechtigungen, Redaktion und Quality Gates bleiben erforderlich.

Dateisystemfreigabe und Ausnahme-Cleanup verringern Risiken durch Harness-Missbrauch und Evidence-Austausch. Diese Quelländerungen belegen keine produktive Schwachstelle oder deren Behebung. Unabhängig bestätigte produktive Apache-Fehler benötigen einen getrennt freigegebenen Fix auf #382.

## Runtime-Evidence

Die frische Kampagne für `57e94983...` erfasste alle 155 Haupt-/Control-Ausführungen: 141 Host-HTTP-Fälle, 10 Konfigurationstests und 4 Prä-Nativ-Hostkandidaten. Der unveränderte gemeinsame Validator und die ausdrückliche Root-Prüfung qualifizieren genau vier vollständige Request-Lifecycles: `NEED-request-empty`, `NEED-request-single-chunk`, `NEED-request-csv` und `NEED-request-eos-once`. Sie lösen in dieser aktuellen Kampagne 4 der 54 ursprünglich offenen Oracle-Mitglieder; 50 bleiben offen. Die übrigen 151 Ergebnisse bleiben `null`. Das exakte aktuelle Ergebnis und die unveränderlichen Referenzen stehen im [Bericht vom 2026-10-22](../apache-i12-20261022/README.de.md). Der [Bericht vom 2026-10-15](../../../docs/i12-apache-native-evidence-20261015.de.md) bleibt historisch und wird nicht in die aktuelle Quellqualifikation eingerechnet.

Alle zehn Config-Ausführungen und vier Prä-Nativ-Ausführungen bleiben unqualifiziert, weil ihre physischen Receipts die unveränderten typisierten Validatoren nicht erfüllen. Das sind fehlende oder widersprüchliche Nachweise, keine verweigerte Berechtigung. Fehlende Beobachtungen bleiben `null`; `I12_COMPLETE` ist false.

## Bekannte Einschränkungen

Das Inventar mit 179 Issues gehört zur alten Basis-Analyse; die spätere Analyse für `a36f9831cb34532d388d2da9a787b25268721b74` enthält 22 ungelöste Issues. Lokale Quellbereinigung und Host-Evidence belegen kein grünes Cloud-Gate, null neue Findings oder den Abschluss absichtlicher Loopback-HTTP-/C++17-Empfehlungen. Testzahlen von Teilmengen dürfen nicht zu einem vollständigen gemeinsamen Lauf addiert werden. Der Root-DAC-Skip benötigt den separaten Nonroot-Test und einen neuen Lauf bei Änderungen seiner Implementierung.

## Verbleibende Risiken

Refactoring von Framing-, Ausnahme- und Observer-Pfaden kann weiterhin Verhalten außerhalb der lokal ausgeführten Pfade beeinflussen. Der Apache-Abnahme fehlen weiterhin vollständige aktuelle Run-Qualifikation für alle Pflichtfälle und unabhängige Freigabe der Original-Oracle-Vorschläge. Der Apache-spezifische Dispatch ist implementiert; semantische Prädikate und vollständig geprüfte Pakete bleiben offen. Gemeinsame Validatoren und zentraler Generator sind unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Die frische Kampagne aller 155 Fälle und die ausdrückliche Prüfung sind abgeschlossen; die exakte Head-CI-/Cloud-Entscheidung nach dem abschließenden reinen Evidence-Commit bleibt ein Liefernachweis außerhalb der Runtime-Qualifikation. Die 151 offenen Fallentscheidungen benötigen neue Producerfelder, Familienprädikate oder unabhängige Mapping-Nachweise. Für die ausgeführte defensive Arbeit besteht kein Berechtigungsblocker; die verbleibenden Fallsperren sind fehlende oder widersprüchliche Evidence und die dokumentierten gemeinsamen Producer-Integrationsbedarfe.

## Finaler Diff- und Review-Status

Die erste Bereinigung ist als `ee68b78f4f802149ed6d864a32ff5198e8c0596b` committet; die Sonar-Folgeänderung ist `33e89e8ad636787a5c9a19eafbbe9bc8eaadabd1`, die ausgeführte Produktquelle ist `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38`, und die abschließende Prüfhärtung ist unter `de23f2fa4b490c66f15ac97f2646434351f05c5e` veröffentlicht. Das unabhängige Review fand in diesem begrenzten Reviewer-Diff keine verbleibende konkrete Abweichung. Erfolgreiche CI-/Sonar-Prüfung des abschließenden Evidence-Commits und ein PR-Merge werden hier nicht behauptet. Force-Push, automatischer Merge, Release und `I12_COMPLETE` folgen daraus nicht.
