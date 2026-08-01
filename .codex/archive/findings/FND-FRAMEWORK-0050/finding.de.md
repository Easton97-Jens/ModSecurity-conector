# FND-FRAMEWORK-0050 — Framework-Test-Assertions vertauschen tatsächliche und erwartete Argumente

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0050 |
| Kategorie | sonarqube_finding |
| SonarQube-Cloud-Klassifikation | maintainability |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P2 / not_applicable |
| Confidence / Status | validated / fixed |
| Feasibility | feasible_now |
| Release-Blocker / Security relevant | true / false |
| Finale Disposition | framework_pr47_s3415_local_remediation_fixed_pending_exact_head_hosted_confirmation |

### PR-#47-Follow-up — 2026-07-26

Der exakte Initial-Head `3bbb2e806f4892e8f92476e35740d149b8b9b17b` von
Framework-PR #47 enthält eine aufgabeneigene `python:S3415`-Diagnose in
`tests/ci_security/test_ci_security_contract.py`. Sie hat dieselbe
Unittest-Grundursache der positionalen `actual, expected`-Reihenfolge wie
dieser kanonische Record und wird daher hier dedupliziert.

Das zurückgehaltene SonarQube-Cloud-Inventar ist
`/var/tmp/codex/ModSecurity-conector/runs/20260726T105400Z-framework-pr47-sonar-merge/evidence/sonar-pr47-initial-issue-inventory.json`,
SHA-256 `d98ef7664e411e8d6f820eec8a4b8b82e9501fcf5aabf42e9b7a1cd857006937`.
Die lokale Reparatur korrigiert die Assertion-Reihenfolge und erweitert die
direkte Rejection-Coverage. Die fokussierte CI-Security-Contract-Suite sowie
Workflow-/Dokumentations-Controls bestanden lokal. Eine frische SonarQube-
Cloud-Analyse für den danach eingereichten exakten PR-Head bleibt erforderlich;
kein Test- oder Scanner-Control wurde geändert.

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

### Framework-PR-#43-Exact-Head-Verifikation — 2026-07-23

Der normale Framework-only-Draft-PR [#43](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/43)
wurde aus `agent/framework-sonarqube-test-issues-507` gegen `master` erstellt.
Lokales Worktree, Remote-Branch und GitHub-PR-Head zeigen alle auf den exakten
Commit `4c55bb2855b8e0196fe54cb0c6f90f43aa993962`; seine Basis ist
`935cf14c676a24672be5c336e92cd13457cc35c8`. Es wurde kein Merge und kein
Master-Update ausgeführt.

SonarQube Cloud analysierte genau diesen PR-Head um
`2026-07-23T10:39:35+0000`. Das Quality Gate ist `OK`, der PR hat null offene
`python:S3415`-Issues und null offene Issues insgesamt; seine Sonar-Zusammenfassung
meldet null Bugs, Vulnerabilities und Code Smells. Die terminalen GitHub-PR-
Checks bestanden, einschließlich SonarCloud Code Analysis, CodeQL für
Actions/Python/C++, Secret Scanning, OSV, Scorecard, Structure-, Action-Version-
und Scaffold-Lint-Checks. Der aufbewahrte Delivery-Receipt ist
`/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-delivery-verification.md`,
SHA-256 `1d70d068c9c3079de55abc76a7271a5fc37b20454a4fb3f99a29cbb68c0d052b`.

Dies verifiziert die aktuelle 507-Key-Remediation am eingereichten Draft-PR-
Head; es autorisiert keinen Merge und behauptet nicht, die getrennte
MRTS-only-`FND-SONAR-0002`-Master-Bedingung zu lösen.

### Resulting-Master-Verifikation nach PR #43 — 2026-07-23

GitHub mergte PR [#43](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/43)
am `2026-07-23T11:24:30Z` normal mit Exact-Head-Schutz. Sein exakter Source
`4c55bb2855b8e0196fe54cb0c6f90f43aa993962` ist der zweite Parent des
resultierenden Framework-masters `f98a8739cb13b583f23d646784b144e596b61441`.

Die exakte Resulting-Master-SonarQube-Cloud-Analyse
`77e255d6-17a2-4e8a-bb29-6438e91e6fa8` hat null offene `python:S3415`-Issues.
Das resultierende Quality Gate ist ausschließlich wegen New Security Rating C
(Actual `3`, Threshold `1`) aus neun read-only-MRTS-Vulnerability-Signalen
ERROR, die vom unabhängigen `FND-SONAR-0002` getrackt werden; dies ist kein
Beleg für eine Regression dieser Assertion-Order-Remediation. `test-common`,
OpenSSF Scorecard, lint und CodeQL analysis schlossen erfolgreich ab; der
PR-only-Head-Job war beim Master-Trigger absichtlich übersprungen. Parent und
MRTS blieben unverändert. Der aufbewahrte Post-Merge-Receipt ist
`/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-postmerge-master-verification.md`,
SHA-256 `d8a63662d10def3118b5795c90474a0c63ab9a96a82d5e93debb8436c79bd79c`.

### Aktuelle Master-Erweiterung — 2026-07-23

Die aktuelle SonarQube-Cloud-Analyse `dda3ea04-2721-4ee6-a9c1-74bd2925f139`
des Framework-`master` am exakten Revisionstand
`935cf14c676a24672be5c336e92cd13457cc35c8` meldet 507 ungelöste
`python:S3415`-MAJOR-CODE_SMELL-Diagnosen. Es sind Framework-eigene
Teststellen in 29 Dateien: 262 unter `tests/security_regression/`, 220 unter
`tests/no_crs/`, 23 unter `tests/protocol_client/` und 2 unter
`tests/makefile_contract/`. Das vollständige aktuelle Inventar ist unter
`/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/sonar-master-s3415-inventory.md`
mit SHA-256
`0e9f549877fc1da2d3c629073e966e51f101348e913641cc7f539b29896379ef`
aufbewahrt.

Die paginierte ungelöste Abfrage liefert 500 Items auf Seite 1 und 7 auf Seite
2. Jedes Item trägt dieselbe Meldung: „Swap these 2 arguments so they are in
the correct order: actual value, expected value.“ Dies bleibt dieselbe
kanonische Assertion-Order-Ursache wie die historischen fünfzehn PR-#42-Keys
und erweitert daher dieses Finding statt ein Duplikat anzulegen. Sie ist nicht
auf `assertEqual` beschränkt: Repräsentative aktuelle Stellen umfassen auch
`assertNotEqual`.

Die 507 sind nicht sicherheitsrelevante Maintainability-Items und nicht der
Grund dafür, dass das aktuelle Master-Quality-Gate ERROR ist. Die unabhängige
Security-C-Bedingung wird von neun read-only-Scanner-Signalen unter
`tools/MRTS/mrts/**` verursacht und bleibt durch `FND-SONAR-0002` getrackt;
diese Framework-Test-Order-Remediation darf nicht behaupten, sie zu beheben
oder MRTS zu ändern.

### Historische PR-#42-Beobachtung

Die öffentliche SonarQube-Cloud-Abfrage für den exakten Head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` von Framework-PR #42 meldet
fünfzehn offene CODE_SMELL-Diagnosen unter `python:S3415`. Jede benennt einen
`unittest.assertEqual`-Aufruf, bei dem der erwartete Wert vor dem tatsächlichen
Wert übergeben wird. Das verringert die Klarheit der Fehlermeldung, ohne die
geprüfte Gleichheitsrelation zu verändern.

Das aufbewahrte initiale Inventar ist
`/var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/sonar-pr42-initial-issue-inventory.md`,
SHA-256
`7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44`.
Es dokumentiert ein Issue in `test_fetch_security_tool.py`, sieben in
`test_update_workflow_tools.py` und sieben in `test_parser_hardening.py`. Alle
42 Exact-Head-Issues sind CODE_SMELL; dieses Finding besitzt nur die fünfzehn
Assertion-Order-Items.

Dies ist ein nicht sicherheitsrelevantes Maintainability-Finding: Severity ist
`not_applicable` und `security_relevant` ist false. Es blockiert die
Auslieferung, weil der Nutzer die Behebung aller 42 neuen PR-#42-Issues vor der
Master-Integration ausgewählt hat. Die Umordnung der Argumente darf die
Parser-Härtungs- oder CI-Security-Controls, die diese Tests ausüben, nicht
abschwächen.

Die lokale Korrektur ist abgeschlossen: Alle fünfzehn Aufrufe verwenden jetzt
die Reihenfolge `tatsächlich, erwartet`, die drei direkten Module bestanden 49
Tests, das vollständige native `make lint`-Target bestand und der kombinierte
22-Pfad-Security-Scan meldete kein Finding (Report-SHA-256
`1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36`). Der
ausgewählte lokale Interpreter ist CPython `3.14.4`, während das eingecheckte
Ziel `3.14.6` ist; keines der lokalen Ergebnisse ersetzt frische
Exact-Submitted-Head-SonarQube-Cloud- oder Hosted-Python-Evidence.

## Erwartetes Verhalten und vorgeschlagene Remediation

Jede betroffene unittest-Assertion muss die Reihenfolge `tatsächlich,
erwartet` verwenden und dabei dieselbe Relation, Meldungen, Fixtures,
Testausführung und Security-Regression-Verhalten bewahren. Die historischen
fünfzehn PR-#42-Korrekturen bleiben Teil dieses Records; der aktive Scope sind
die 507 aktuellen Master-Keys. Nur die geprüften positionalen
Argumentänderungen beibehalten; keine Testerwartung ändern, keine
Parser-Härtungs-Coverage entfernen und die Regel nicht unterdrücken. Wenn ein
Ausdruckargument Seiteneffekte hat, die Auswertungsreihenfolge durch ein
geprüftes lokales Temporary bewahren statt Ausdrücke blind zu tauschen.

Eine frische Exact-Head-SonarQube-Cloud-PR-Analyse muss alle fünfzehn
ursprünglichen `S3415`-Keys ohne `NOSONAR`, Suppression, False-Positive-
Markierung, Exclusion, Regeländerung oder Quality-Gate-Änderung als nicht
vorhanden zeigen.

## Betroffene Dateien und Symbole

- `tests/ci_security/test_fetch_security_tool.py`: `AZ-K30-bbx6VBofpXBhx`
- `tests/ci_security/test_update_workflow_tools.py`: `AZ-K30_Ibx6VBofpXBhz`,
  `AZ-K30_Ibx6VBofpXBh0`, `AZ-K30_Ibx6VBofpXBh1`,
  `AZ-K30_Ibx6VBofpXBh2`, `AZ-K30_Ibx6VBofpXBh3`,
  `AZ-K30_Ibx6VBofpXBh4`, `AZ-K30_Ibx6VBofpXBh5`
- `tests/security_regression/test_parser_hardening.py`:
  `AZ-K306Vbx6VBofpXBhr`, `AZ-K306Vbx6VBofpXBhs`,
  `AZ-K306Vbx6VBofpXBhq`, `AZ-K306Vbx6VBofpXBht`,
  `AZ-K306Vbx6VBofpXBhu`, `AZ-K306Vbx6VBofpXBhv`,
  `AZ-K306Vbx6VBofpXBhw`
- Regel: `python:S3415`

### Aktueller Master-Scope

- Revision / Analyse: `935cf14c676a24672be5c336e92cd13457cc35c8` /
  `dda3ea04-2721-4ee6-a9c1-74bd2925f139`.
- Anzahl / Ownership: 507 Framework-eigene Testdiagnosen in 29 Dateien;
  `tests/security_regression/` 262, `tests/no_crs/` 220,
  `tests/protocol_client/` 23 und `tests/makefile_contract/` 2.
- Exakte Pfade und Zeileninventar: im oben genannten aktuellen Master-
  Evidence-Artifact aufbewahrt. Source-Mapping und Diff-Review müssen jeden
  Pfad vor Delivery auflösen.

## Voraussetzungen und Reproduktion

1. Für den aktiven aktuellen Master-Scope SonarQube Cloud für das Projekt
   `Easton97-Jens_ModSecurity-test-Framework`, `branch=master`,
   `statuses=OPEN`, `rules=python:S3415`, `ps=500` und die Seiten 1 und 2
   abfragen. `total=507` (500 dann 7) sowie die exakte Analyse-/Revision-
   Bindung oben verifizieren.
2. Jede aktuelle gemeldete Test-Source-Stelle untersuchen. Ihre
   Pre-Remediation-Assertion übergibt erwartet vor tatsächlich; bei Bedarf
   die Seiteneffekt-Auswertungsreihenfolge bewahren.
3. Historische PR-#42-Reproduktion: SonarQube Cloud für das Projekt
   `Easton97-Jens_ModSecurity-test-Framework`, `pullRequest=42`,
   `issueStatuses=OPEN,CONFIRMED`, `sinceLeakPeriod=true` und `ps=500`
   abfragen.
4. Das historische aufbewahrte Inventar lesen und SHA-256
   `7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44`
   verifizieren.
5. Nach `python:S3415` filtern; der historische initiale Count ist fünfzehn.
6. Die drei historischen Testdateien untersuchen. Vor der Remediation verwendet
   jede dokumentierte Stelle die Reihenfolge `assertEqual(erwartet, tatsächlich)`.

## Evidence

| Feld | Wert |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/sonar-pr42-initial-issue-inventory.md |
| Artifact type | task_owned_sonarqube_cloud_pr42_initial_inventory |
| SHA-256 | 7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44 |
| Command | `rtk run curl -fsSL https://sonarcloud.io/api/issues/search --get --data-urlencode componentKeys=Easton97-Jens_ModSecurity-test-Framework --data-urlencode pullRequest=42 --data-urlencode issueStatuses=OPEN,CONFIRMED --data-urlencode sinceLeakPeriod=true --data-urlencode ps=500` |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T18:18:47Z |
| Retention status | task_owned_retained_evidence |

| Feld | Framework-PR-#43-Exact-Head-Delivery-Verifikation |
| --- | --- |
| Run ID | 20260723T092456Z-framework-sonarqube-test-issues-507-10387697 |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-delivery-verification.md |
| Artifact type | framework_pr43_exact_head_delivery_verification |
| SHA-256 | 1d70d068c9c3079de55abc76a7271a5fc37b20454a4fb3f99a29cbb68c0d052b |
| Command | Exakter Vergleich von lokalem/Remote-/PR-Head; `gh pr checks 43`; SonarQube-Cloud-PR-Quality-Gate-, Issue- und Pull-Request-Abfragen |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-23T10:41:53Z |
| Retention status | task_owned_retained_evidence |

| Feld | Lokale Remediation-Validierung |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-python314-local-validation.md |
| Artifact type | framework_pr42_local_s3415_and_cpython3146_validation |
| SHA-256 | 4f3f7967438688697da9dcca5cb57bcaf7914c700342d9af8bb07f16a8d63075 |
| Command | Ausgewählter CPython-3.14.4-Lauf der drei direkten S3415-Module (49 Tests), kombinierte Checks und vollständiges natives make lint für die konfigurierte CPython-3.14.6-Migration |
| Working directory | framework-worktree-v4 |
| Exit code | 0 |
| Observed at | 2026-07-22T20:14:50Z |
| Retention status | task_owned_retained_evidence |

| Feld | Versiegelter kombinierter 22-Pfad-Security-Scan |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/analysis/security-diff-pr42-python314-20260722T200333Z/report.md |
| Artifact type | sealed_codex_security_diff_scan_report |
| SHA-256 | 1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36 |
| Command | Vollständiger 22-Pfad-Codex-Security-Diff-Scan der kombinierten lokalen PR-#42-Remediation und CPython-3.14.6-Migration |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T20:14:50Z |
| Retention status | sealed_task_evidence |

| Feld | Aktuelles Master-S3415-Inventar |
| --- | --- |
| Run ID | 20260723T092456Z-framework-sonarqube-test-issues-507-10387697 |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/sonar-master-s3415-inventory.md |
| Artifact type | current_framework_master_s3415_paginated_inventory |
| SHA-256 | 0e9f549877fc1da2d3c629073e966e51f101348e913641cc7f539b29896379ef |
| Command | RTK-umhüllte SonarQube-Cloud-Leseaufrufe für `project_analyses`, paginiertes `issues/search`, `qualitygates/project_status` und den GitHub-Master-Ref |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-23T09:24:56Z |
| Retention status | task_owned_retained_evidence |

## Grundursache

Die betroffenen unittest-Assertions wurden mit der positionalen Reihenfolge
`erwartet, tatsächlich` geschrieben. Sonar-Regel `S3415` verlangt
`tatsächlich, erwartet`, damit eine fehlgeschlagene Assertion den beobachteten
Wert an ihrer vorgesehenen Position zeigt. Dies ist unabhängig von den
komplexen CI-Security-Contract-, Python-Version- und Updater-Refactorings in
`FND-FRAMEWORK-0044`. Die 507 aktuellen Master-Keys sind eine neue Beobachtung
derselben Ursache an einer getrennten aktuellen Testmenge, kein Duplikat-
Record: Das kanonische Finding bewahrt nun sowohl die historische 15-Key-
PR-#42-Beobachtung als auch die unabhängig bearbeitbare 507-Key-Master-
Beobachtung.

## Akzeptanzkriterien und Validierungsplan

1. Alle 507 aktuellen Master-Stellen sind gemappt und verwenden
   `tatsächlich, erwartet` ohne Relation-, Message-, Fixture-, Control- oder
   Auswertungsreihenfolge-Änderung.
2. Ausdruckargumente mit Seiteneffekten erhalten geprüfte sichere Behandlung
   statt eines blinden Tauschs.
3. Fokussierte betroffene Testfamilien-Module bestehen einschließlich ihrer
   legitimen Security-Regression-Controls.
4. `git diff --check`, natives Framework-Lint und erforderliche
   Dokumentations-/Change-Record-Checks bestehen für den task-eigenen
   Framework-Range.
5. Die frische SonarQube-Cloud-Draft-PR-Analyse am exakten eingereichten Head
   `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` meldet keinen der ursprünglichen
   507 `S3415`-Keys, kein offenes PR-Issue und keine verbotene Scanner-Control-
   Änderung.
6. Parent-Gitlink und MRTS-Source bleiben unverändert; dieser PR behauptet
   nicht, die unabhängige `FND-SONAR-0002`-Security-C-Gate-Bedingung zu lösen.

Ein isoliertes Worktree vom frisch beobachteten Remote-Master anlegen; jedes
aktuelle Issue auf seine Source-Assertion abbilden; den task-eigenen Diff auf
nur Argumentreihenfolge-Änderungen und verbotene Controls prüfen; danach
betroffene Module nach Testfamilie sowie native Source-Quality- und
Dokumentations-Checks ausführen. Frische Exact-Head-GitHub-/Sonar-Evidence
nach normaler Draft-PR-Einreichung beobachten.

## Regression- und Legitimate-Control-Tests

Regression-Tests:

- Geänderte `tests/security_regression/`-Module
- Geänderte `tests/no_crs/`-Module
- Geänderte `tests/protocol_client/`-Module
- Geänderte `tests/makefile_contract/`-Module
- Natives `make lint`, Change-Record- und Dokumentations-Checks

Legitimate Controls:

- Bestehende akzeptierte und abgewiesene Path-Containment-, Parser/Provenance-,
  Workflow/Action-Pin-, Protocol- und Makefile-Fixtures bewahren dasselbe
  erwartete Ergebnis und dieselbe Diagnose.

## Dependencies, Blocker, Related Findings und Restrisiko

- Dependencies: Für dieses Finding bleibt keine Delivery-Abhängigkeit: PR #43
  ist gemergt und sein ursprünglicher S3415-Scope ist auf resultierendem
  Framework-master verifiziert.
- Blocked by: kein technischer Blocker für dieses Finding. Der unabhängige
  `FND-SONAR-0002`-Master-Quality-Gate-Blocker bleibt außerhalb dieses Findings.
- Related Findings: `FND-FRAMEWORK-0044`, `FND-FRAMEWORK-0046`,
  `FND-FRAMEWORK-0047`, `FND-FRAMEWORK-0048`, `FND-FRAMEWORK-0049` und
  `FND-SONAR-0002`.
- Restrisiko: Ein Bulk-positionaler-Tausch kann Auswertungsreihenfolge oder
  Testdiagnostik unbeabsichtigt ändern. Nur geprüfte Assertion-Calls dürfen
  sich ändern, jede betroffene Control-Familie muss erneut laufen, und kein
  Scanner-/Test-Control darf abgeschwächt werden. Es wurde kein Risiko
  akzeptiert.

## Historie

| Zeit | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-22T18:18:47Z | framework_pr42_s3415_finding_created | Nach vollständiger öffentlicher Exact-Head-PR-#42-Issue-Abfrage und Deduplizierung angelegt. Fünfzehn `python:S3415`-CODE_SMELL-Diagnosen in drei Testmodulen bilden eine unabhängig behebbare Test-Maintainability-Grenze; dieser Record behauptet keine Source-, Git-, GitHub-, Parent- oder MRTS-Aktion. |
| 2026-07-22T20:14:50Z | framework_pr42_s3415_local_fix_and_validation_reconciled | Alle fünfzehn positionalen Assertion-Reihenfolgen wurden lokal korrigiert. Die direkte Drei-Modul-Suite bestand 49 Tests, das vollständige native `make lint` bestand und der vollständige kombinierte 22-Pfad-Security-Scan meldete null Findings. Das Finding ist fixed, nicht verified oder closed, bis Hosted-Sonar-Evidence für den exakten eingereichten Head beobachtet wurde. |
| 2026-07-23T09:27:46Z | current_master_s3415_observation_deduplicated_into_canonical_finding | Vollständige aktuelle Master-Pagination identifizierte 507 getrennte aktuelle `python:S3415`-Keys in 29 Framework-Testdateien. Dies ist dieselbe Assertion-Order-technische Ursache wie die historischen fünfzehn PR-#42-Keys und erweitert daher diesen kanonischen Record statt ein Duplikat anzulegen. Der neue aktuelle Scope ist unabhängig bearbeitbar; `FND-SONAR-0002` bleibt die getrennte MRTS-only-Security-C-Gate-Abhängigkeit. Diese Beobachtung behauptet keine Framework-Source-, Git-, GitHub-, Parent- oder MRTS-Aktion. |
| 2026-07-23T10:41:53Z | framework_pr43_exact_head_verified | Framework-Draft-PR #43 wurde normal am exakten Head `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` gegen Master `935cf14c676a24672be5c336e92cd13457cc35c8` erstellt. Lokale/Remote-/PR-Heads stimmten überein; alle terminalen GitHub-Checks bestanden; die exakte Sonar-PR-Analyse hat Quality Gate OK mit null offenen `python:S3415`- und null offenen Issues. Das Finding ist verified, nicht closed; kein Merge und keine Parent-/MRTS-Aktion erfolgten. |
| 2026-07-23T11:25:34Z | framework_pr43_merged_and_s3415_verified_on_resulting_master | Der exakte PR-#43-Source `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` mergte normal als Framework-master `f98a8739cb13b583f23d646784b144e596b61441`. Die exakte Master-Analyse `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` hat null offene `python:S3415`-Issues. Ihr Quality-Gate-ERROR ist ausschließlich Security C (Actual `3`, Threshold `1`) aus neun read-only-MRTS-Signalen, die das unabhängige `FND-SONAR-0002` trackt; diesem Finding wird keine Kausalität zugeschrieben. Parent und MRTS blieben unverändert. |
