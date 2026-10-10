# Change Record: NGINX-Configtest-Pfadautorität

**Sprache:** [English](CR-20261003-nginx-configtest-path-authority.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261003-nginx-configtest-path-authority` |
| Datum (UTC) | `2026-10-03` |
| Basis-Revision | `acefed5c81a56f636610601edcc447a257b9e947` |
| Framework, eingefroren | `b9b9534b7e0b15edad31393699ebd0617748148d` |
| MRTS, unverändert | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery-Status | Lokale CI-/Sonar-Remediation; PR #355 OPEN, PR #396 DRAFT; Remote-Prüfungen stehen aus |

## Motivation und Problemstellung

Configtest-Treiber und selektierte Case-Anbindung ließen schreibbare
Ausgabeparents/-vorfahren sowie Build-/Results-/Konfigurationsparents zu.
Test-first-Prüfungen beobachteten sechs negative Subkontrollen, die diese
Inputs nicht ablehnten, während die positive Kontrolle mit eigenem `0755`
bestand. Die Korrektur wendet den bestehenden Autoritätsvertrag für externe
Runtime-Verzeichnisse auf diese genauen Parents an. Remote-Sonar-Review am
veröffentlichten Ausgangsstand ist Remediation-Input und kein bestandener
Nachweis: Quality Gate `ERROR`, 12 gemeldete Issues. Zwei statische
Security-Hinweise bleiben `needs_review`; keiner wird hier als bestätigter
Exploit oder verworfenes Finding veröffentlicht.

## Akzeptanzkriterien

Schreibbare Parents und unsichere bestehende Resultdateien vor Ausführung
oder Append ablehnen. Zulässige eigene `0755`-Parents, legitime `0644`-Results,
externe Root-Containment, Checkout-Ausschluss, frische private `0700`-Children,
selektierte Boolean-/Size-Diagnosen und Receipt-Identität erhalten. Veraltete
Case-Children ablehnen. Mechanische Complexity-/Test-/Shell-Änderungen müssen
verhaltenserhaltend bleiben. Fokussierte Tests, Negativkontrollen, statische
Prüfungen und bilinguale Dokumentation verifizieren; Remote-CI und ein
aktuelles Exact-Head-Sonar-Ergebnis bleiben separate Gates.

## Implementierungsentscheidung und Begründung

Non-Following-`ensure_safe_runtime_directory` für die genauen externen Parents
wiederverwenden, statt eine weitere Verzeichniszulassungspolicy zu schaffen.
Bestehende Resultdateien müssen der effektiven UID gehören, regulär sein,
einen Hardlink besitzen, keine `0022`-Berechtigungsbits haben und höchstens
4 MiB groß sein. Bestehendes Case-Child vor Append ablehnen.
Containment unter `/var/tmp/codex/ModSecurity-conector` und Checkout-Ausschluss
erhalten.
Neue Parents behalten Modus `0700`, statt den Helper-Default `0755` zu
übernehmen; explizite positive Fixtures beweisen zudem, dass bestehende eigene
`0755`-Parents und legitime `0644`-Results diese Modi behalten.

Separate mechanische S3776-Refactors von Collector, Treiber und Dispatcher,
aufgeteilte Assertions und No-op-Shell-Defaults erhalten die Semantik.
Worker-Charakterisierungen bestanden 954 Paritätskontrollen und
Header-Baseline-Parität; diese Beobachtungen sind von finaler kombinierter
Regressionsvalidierung zu unterscheiden.
Die Delivery erfolgt in Phasen: Autoritätskorrektur und gepaarter Record
gehen dem separaten mechanischen Nachfolger im selben Veröffentlichungsbatch
voraus. Dieser Record beschreibt den kombiniert validierten Umfang, ohne
die Commits gleichzusetzen.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-selected-nginx-configtests.py`
- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_configtest_driver.py`
- `tests/test_nginx_selected_configtest_wiring.py`
- `tests/test_nginx_configtest_collection.py`
- `tests/test_nginx_h1_request_protocol.py`
- `tests/test_protected_nginx_exact_head_builder.py`
- `docs/testing-and-evidence.md` und `docs/testing-and-evidence.de.md`
- Dieses Change-Record-Paar und `reports/audits/change-records/README.md` / `README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

Beobachteter Test-first-Stand: sechs negative Pfadautoritäts-Subkontrollen RED;
positive Kontrolle mit eigenem `0755` grün. Eine unveränderliche Wiederholung
an `ac4c746f6a4c07006f25b078f660e31b16341479` führte neun Tests aus:
Die sichere positive Kontrolle bestand und neun negative Subkontrollen
schlugen über zwei Parent-Modi fehl; Subtests erklären den Unterschied
zwischen Test- und Fehlerzahlen.

Finale Koordinatorverifikation durch
`/var/tmp/codex/ModSecurity-conector/analysis/verify-pr396-ci-remediation.py`
orchestrierte RTK-verpackte Befehle und bewahrte vollständige Logs/Exit-Belege:

- Geschützter Fokus: 139 Tests PASS; aktueller NGINX-/Runtime-/Collector-/Config-Fokus: 237 Tests PASS. Insgesamt: 376 Tests, keine Skips, `pr396-ci-final-focus.exit` = 0.
- Pfadautoritäts-/Modusfokus: 33 Tests PASS nach den Guards und erneut nach beiden wesentlichen Refactor-Extraktionen. Unabhängiger Reviewer: 96 Tests PASS.
- Worker-Charakterisierung: 954 Paritätskontrollen und Header-Baseline-Parität PASS.
- Python-Kompilation, `sh -n`, ShellCheck auf Fehlerstufe, actionlint für alle Workflows, native Bilingual-/Pfad-/Linkprüfungen und `git diff --check`: PASS; `pr396-ci-static.exit` = 0.

Logs und Belege liegen unter `/var/tmp/codex/ModSecurity-conector/analysis/`.
Diese Tests verwenden nachgebildete Source-/Fixture-Executables und belegen
Vertragsverhalten, keine echte NGINX-Host-Ausführung und kein neues
Konfigurations-/Runtime-Evidence-Bundle.
Der Dokumentationscheckpoint führte
`rtk proxy make check-bilingual-docs check-doc-links PYTHON=python3 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/pr355-integration-docs`
mit Exit 0 aus, einschließlich Repository-Pfadreferenzen.
`rtk proxy git diff --check` endete ebenfalls mit Exit 0. Diese Prüfungen
ersetzen keine fokussierte Source-Validierung.

## Security-Auswirkung

Die Korrektur stärkt bestehende Output-/Result-Autorität ohne Abschwächung
der Artefakt-, Receipt-, Collector- oder Protected-Host-Zulassung. Die beiden
statischen Security-Hinweise sind zu validierende Review-Inputs.
FND-PARENT-1038 benötigt weiterhin Exact-Head-Verifikation und FND-PARENT-1036
seine externe Abhängigkeit; diese Source-/Fixture-Prüfungen erfüllen keine
Host-/Archivanforderungen. Keine Exploitdetails, Geheimnisse oder rohe
Evidence werden hier veröffentlicht.

## Runtime-Evidence

Keine HTTP-Requests, Daemon-Starts, Protected-Host-Runtime oder unabhängige
Attestierung werden behauptet. Bestehende Config-only-Receipts behalten ihre
ursprüngliche Identität; keine neue Runtime-Evidence wird erfunden.
Exact-Head E2E PASS: NO.

## Bekannte Einschränkungen

Lokale fokussierte und statische Validierung bestand. Remote-CI- und Sonar-Ergebnisse für
diesen lokalen Nachfolger wurden noch nicht beobachtet. Framework und MRTS
sind unverändert.

## Verbleibende Risiken

Pfadzulassung und Dateimetadatenprüfungen belegen nur ihre getestete Schicht.
Aktuelle Remote-Prüfungen und gegebenenfalls Host-Verifikation bleiben
erforderlich; das fehlgeschlagene Quality Gate des aktuell veröffentlichten
Ausgangsstands wird nicht umklassifiziert.

## Nicht ausgeführte Prüfungen mit Begründung

Full Exact-Head E2E, MIME-Arbeit und geschützte Runtime liegen außerhalb dieser
CI-/Sonar-Remediation. PR #355 bleibt bis zur verifizierten Ablösung OPEN;
PR #396 bleibt DRAFT. Kein neuer Push des lokalen Nachfolgers oder Schließen
wird behauptet.

## Finaler Diff- und Review-Status

Lokale Source-/Fixture-Remediation und fokussierte/statische Validierung PASS
für den oben aufgeführten 15-Dateien-Umfang, einschließlich beider
Dokumentationspaare und Indizes. Delivery bleibt INCOMPLETE:
Remote-CI/Sonar stehen aus; aktuell grüne Remote-Ergebnisse werden nicht
behauptet.
