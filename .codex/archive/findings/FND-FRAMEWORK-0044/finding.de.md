# FND-FRAMEWORK-0044 — Framework-PR #42 hat 27 lokal behobene SonarQube-Cloud-Code-Smells, deren Exact-Head-Bestätigung aussteht

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0044 |
| Kategorie | sonarqube_finding |
| SonarQube-Cloud-Klassifikation | maintainability |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P2 / not_applicable |
| Confidence / Status | validated / fixed |
| Feasibility | feasible_now |
| Release-Blocker / Security relevant | true / false |
| Finale Disposition | local_framework_pr42_remediation_and_cpython_3_14_6_migration_fixed_pending_exact_head_hosted_confirmation |

## PR-#47-Follow-up — 2026-07-26

Der exakte Initial-Head `3bbb2e806f4892e8f92476e35740d149b8b9b17b` von
Framework-PR #47 enthält drei aufgabeneigene Maintainability-Diagnosen in
`ci/checks/security/check-ci-security-contract.py`: zwei `python:S1192`-
Duplicate-Literal-Findings und ein `python:S3776`-
Cognitive-Complexity-Finding. Es sind dieselben begrenzten Grundursachen wie
in diesem kanonischen Record; daher werden sie hier verfolgt statt ein
Duplikat-Finding anzulegen.

Das zurückgehaltene SonarQube-Cloud-Inventar ist
`/var/tmp/codex/ModSecurity-conector/runs/20260726T105400Z-framework-pr47-sonar-merge/evidence/sonar-pr47-initial-issue-inventory.json`,
SHA-256 `d98ef7664e411e8d6f820eec8a4b8b82e9501fcf5aabf42e9b7a1cd857006937`.
Die lokale Reparatur benennt die wiederholten Checkout-Policy-Literale und
teilt die Submodule-Updater-Validierung in begrenzte Helper auf, während die
positiven und Rejection-Contracts erhalten bleiben. Die fokussierte
CI-Security-Contract-Suite sowie Workflow-/Dokumentations-Controls bestanden
lokal. Eine frische SonarQube-Cloud-Analyse für den danach eingereichten
exakten PR-Head bleibt erforderlich; kein `NOSONAR`, keine Suppression,
Regel- oder Quality-Gate-Änderung, Exclusion oder False-Positive-Markierung
wird verwendet.

## Aktueller PR-#42-Abgleich — 2026-07-22

Das zurückgehaltene initiale PR-#42-Inventar am exakten Head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` enthält 42 offene oder bestätigte
New-Code-`CODE_SMELL`-Diagnosen. Dieses Finding besitzt 27 Diagnosen in
`check-ci-security-contract.py`, `check-python-version.py`,
`update-python-version.py` und dem Updater-Exception-Testpfad; die übrigen
15 `python:S3415`-Assertion-Order-Diagnosen gehören unabhängig zu
`FND-FRAMEWORK-0050`.

Die aktuelle 27-Key-Ownership ist auf diese vier Pfade begrenzt:

- `ci/checks/security/check-ci-security-contract.py` (7 Keys)
- `ci/checks/security/check-python-version.py` (5 Keys)
- `ci/tools/update-python-version.py` (14 Keys)
- `tests/ci_security/test_update_python_version.py` (1 Key:
  `AZ-K30-lbx6VBofpXBhy:208`)

Das vollständige Key-nach-Regel-Inventar ist kanonisch in `finding.json` und
wortgetreu in `evidence/sonar-pr42-initial-issue-inventory.md` aufbewahrt; es
ist die Akzeptanzmenge für die spätere Exact-Head-No-Suppression-Abfrage.

Der kombinierte lokale Patch bewahrt die Sonar-Grundursachenremediation und
migriert den aktiven Framework-Python-Contract auf exaktes CPython `3.14.6`.
Die ausgewählte lokale CPython-`3.14.4`-Validierung bestand die 61
Migrationstests, die 49 direkten Sonar-Remediation-Tests, `pip check`,
Contracts, Dokumentationsprüfungen, CP314-positive und CP313-negative
Hash-Lock-Controls, `git diff --check` und das vollständige native
`make lint`-Target. Der vollständige 22-Pfad-Security-Scan meldete kein
reportable Finding; sein Report-SHA-256 ist
`1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36`.
Der lokale Validierungs-Receipt ist
`evidence/framework-pr42-python314-local-validation.md` im Run
`20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`, SHA-256
`4f3f7967438688697da9dcca5cb57bcaf7914c700342d9af8bb07f16a8d63075`.

Dies ist nur lokale Evidence. Sie belegt keinen Hosted-Job mit Ziel-`3.14.6`,
kein Live-Python.org-Update, keine reale Paketinstallation, kein GitHub-
Actions-Ergebnis, keinen Review-/Branch-Protection-Status und kein SonarQube-
Cloud-Ergebnis. Der nächste erforderliche Control ist eine normale
Task-Branch-Einreichung mit anschließender Exact-Head-SonarQube-Cloud-Abfrage,
die alle 27 besessenen Keys ohne `NOSONAR`, Suppression, False-Positive-
Markierung, Regel-/Gate-Änderung oder Exclusion als nicht vorhanden zeigt. Die
unabhängige aktuelle Master-Bedingung bleibt `FND-SONAR-0002`; dieser lokale
Finding-Status autorisiert keine Master-Integration.

### Aktuelle Evidence

| Feld | Initiales PR-#42-SonarQube-Cloud-Inventar |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/sonar-pr42-initial-issue-inventory.md |
| Artifact type | task_owned_sonarqube_cloud_pr42_initial_inventory |
| SHA-256 | 7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44 |
| Command | rtk run curl SonarQube-Cloud-Issues-API mit pullRequest=42, OPEN/CONFIRMED, sinceLeakPeriod=true, ps=500 |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T18:18:47Z |
| Retention status | task_owned_retained_evidence |

| Feld | Lokale CPython-3.14-Validierung |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-python314-local-validation.md |
| Artifact type | framework_pr42_cpython3146_local_validation_receipt |
| SHA-256 | 4f3f7967438688697da9dcca5cb57bcaf7914c700342d9af8bb07f16a8d63075 |
| Command | Ausgewählte CPython-3.14.4-Fokustests, Contracts, CP314-Hash-Lock-Dry-Runs, vollständiges natives make lint und Diff-Hygiene für die konfigurierte CPython-3.14.6-Migration |
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

### Aktuelle Historie

| Zeit | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-22T20:14:50Z | framework_pr42_sonar_remediation_and_cpython3146_local_validation_reconciled | Die 27 besessenen PR-#42-Code-Smell-Remediations und die gekoppelte exakte CPython-3.14.6-Migration sind lokal fixed. Ausgewählte CPython-3.14.4-Fokusvalidierung, direkte Sonar-Remediation-Tests, vollständiges natives make lint, CP314-positive/negative Hash-Lock-Controls und der vollständige 22-Pfad-Security-Scan bestanden. Keine Hosted-Sonar-, GitHub-, Live-Update-, Real-Installation- oder CPython-3.14.6-Hosted-Job-Evidence wird behauptet. |

## Historischer PR-#39-Record

Das verbleibende PR-#39-Material wird nur als historische Evidence aufbewahrt.
Es beschreibt nicht den aktuellen PR-#42-Delivery-Status und erzeugt für diese
Aufgabe keine Abhängigkeit von `FND-SONAR-0009`.

### Historische PR-#39-Zusammenfassung, beobachtetes Verhalten und Auswirkung

Das zurückgehaltene initiale SonarQube-Cloud-PR-#39-Inventar meldet 25 offene
New-Code-CODE_SMELL-Issues in den sechs aufgeführten Framework-Dateien. Am
2026-07-21T04:40:00Z lieferte die öffentliche Abfrage total 25, ausschließlich
CODE_SMELL-Issues. Die lokale Remediation ist fixed, aber eine Hosted-
Bestätigung wird bewusst nicht aus lokaler Source-, Test- oder Scan-Evidence
abgeleitet.

Am 2026-07-21T06:13:56Z bestand die zurückgehaltene Framework-spezifische
CPython-3.13.14-Qualifikation die hash-locked-PyYAML-6.0.3-Installation und
pip check, 30 direkte betroffene Tests, make test-ci-security-contract mit 89
Tests, Workflow- und Dokumentations-Checks, python -m compileall -q ci tests,
den Response-Body-Guard und make lint. Dies qualifiziert nur den lokalen Diff:
Es erfolgten keine Hosted-SonarQube-Cloud- oder GitHub-Bestätigung und keine
Coverage-, Scanner-, Quality-Gate-, Regel-, Exclusion-, Suppression- oder
Hosted-Service-Konfigurationsänderung.

Dies ist ein nicht sicherheitsrelevantes Maintainability-Finding: Severity ist
not_applicable und security_relevant ist false. Es bleibt ein Release-Blocker,
weil eine frische Hosted-Analyse für den exakten Head eine
Akzeptanzbedingung ist. Die versiegelte lokale Security-Review ist nur Evidence
für die Framework-Codeänderung; sie beweist kein gehostetes SonarQube-Cloud-
Ergebnis.

### Historisches PR-#39-erwartetes Verhalten und vorgeschlagene Remediation

Die fokussierten lokalen Refactorings müssen CI-Security- und Python-Version-
Contracts bewahren und zugleich die 25 ursprünglichen Maintainability-Issues
beseitigen. Die verhaltenserhaltenden lokalen Refactorings und zugehörigen
Tests beibehalten, den exakten Remediation-Head über den autorisierten
Framework-Delivery-Pfad einreichen und eine passende SonarQube-Cloud-PR-
Analyse erhalten. Jeder ursprüngliche Key muss ohne NOSONAR, Suppression,
Regeländerung, Quality-Gate-Änderung oder Exclusion fehlen.

### Historische PR-#39-betroffene Dateien und Symbole

Betroffene Dateien:

- ci/checks/security/check-ci-security-contract.py
- ci/checks/security/check-python-version.py
- ci/tools/update-python-version.py
- tests/ci_security/test_framework_ci_security_contract.py
- tests/ci_security/test_python_version_contract.py
- tests/ci_security/test_update_python_version.py

Betroffene Regel- oder Abfrage-Identifikatoren: python:S6035, python:S1066,
python:S1192, python:S8786, python:S3776, python:S6353, python:S5713,
python:S5778 und SonarQube Cloud PR #39 issue query.

### Historisches PR-#39-ursprüngliches Issue-Inventar

Alle 25 ursprünglichen offenen oder bestätigten CODE_SMELL-Keys sind nach Pfad
und Regel aufbewahrt. Das Suffix nach jedem Key ist seine Source-Zeile.

- ci/checks/security/check-ci-security-contract.py
  - python:S1192: AZ-BJmy21Sm1F-_jUkdY:54, AZ-BJmy21Sm1F-_jUkdX:536
  - python:S6035: AZ-BreILltpcPPRUrDMO:71
  - python:S8786: AZ-BJmy21Sm1F-_jUkdZ:83
  - python:S3776: AZ-BJmy21Sm1F-_jUkda:684
- ci/checks/security/check-python-version.py
  - python:S6353: AZ-BJmyl1Sm1F-_jUkdS:19, AZ-BJmyl1Sm1F-_jUkdT:32,
    AZ-BJmyl1Sm1F-_jUkdU:35, AZ-BJmyl1Sm1F-_jUkdV:39
  - python:S3776: AZ-BJmyl1Sm1F-_jUkdW:281
- ci/tools/update-python-version.py
  - python:S6353: AZ-BJmyc1Sm1F-_jUkdE:32, AZ-BJmyc1Sm1F-_jUkdF:33,
    AZ-BJmyc1Sm1F-_jUkdG:34, AZ-BJmyc1Sm1F-_jUkdH:36,
    AZ-BJmyc1Sm1F-_jUkdI:36, AZ-BJmyc1Sm1F-_jUkdJ:36,
    AZ-BJmyc1Sm1F-_jUkdK:36, AZ-BJmyc1Sm1F-_jUkdL:36,
    AZ-BJmyc1Sm1F-_jUkdM:36, AZ-BJmyc1Sm1F-_jUkdN:36
  - python:S5713: AZ-BJmyc1Sm1F-_jUkdO:232
  - python:S3776: AZ-BJmyc1Sm1F-_jUkdP:262, AZ-BJmyc1Sm1F-_jUkdQ:568
  - python:S1066: AZ-BreDOltpcPPRUrDMN:470
- tests/ci_security/test_update_python_version.py
  - python:S5778: AZ-BJmv31Sm1F-_jUkdC:208

### Historische PR-#39-Voraussetzungen und Reproduktion

- Das zurückgehaltene Inventar gehört zum SonarQube-Cloud-Projekt
  Easton97-Jens_ModSecurity-test-Framework und Pull Request 39.
- Die lokale Remediation ist auf die sechs betroffenen Framework-Dateien
  begrenzt.
- Die Hosted-Bestätigung benötigt einen eingereichten Remediation-Head und eine
  frische SonarQube-Cloud-PR-Analyse für genau diesen Head.

Den zurückgehaltenen Abfragebefehl verwenden:

rtk proxy python3 -c 'import json, urllib.request; data=json.load(urllib.request.urlopen("https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-test-Framework&pullRequest=39&issueStatuses=OPEN%2CCONFIRMED&sinceLeakPeriod=true&ps=500")); print(data["total"])'

/var/tmp/codex/ModSecurity-conector/runs/20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8/evidence/sonar-pr39-initial-inventory.md
lesen und SHA-256 f9feb36fe34055f6c17f47ed0011803d70b3128a2104d483bad9b01be54dcddd
vergleichen. Nach autorisierter Einreichung die Abfrage für den exakten Head
wiederholen und verifizieren, dass alle ursprünglichen Keys fehlen.

### Historische PR-#39-Evidence

| Feld | Initiales SonarQube-Cloud-Inventar |
| --- | --- |
| Run ID | 20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8 |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8/evidence/sonar-pr39-initial-inventory.md |
| Artifact type | markdown |
| SHA-256 | f9feb36fe34055f6c17f47ed0011803d70b3128a2104d483bad9b01be54dcddd |
| Command | rtk proxy python3 -c 'import json, urllib.request; data=json.load(urllib.request.urlopen("https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-test-Framework&pullRequest=39&issueStatuses=OPEN%2CCONFIRMED&sinceLeakPeriod=true&ps=500")); print(data["total"])' |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-21T04:40:00Z |
| Retention status | retained |

| Feld | Versiegelter lokaler Security-Diff-Scan |
| --- | --- |
| Run ID | security-diff-ee513e45-20260721t042538z |
| Artifact path | /var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-test-Framework/ee513e45_20260721T042538Z.UwIsr9/report.md |
| Artifact type | sealed_codex_security_diff_scan_report |
| SHA-256 | 23e40aeb939a82f90c02662c02817775177cc9467cb6dc22857f6a7aed2e986c |
| Command | Codex Security diff review of the local PR #39 Sonar code-smell remediation patch; retained report records 0 reportable findings. |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-21T04:25:38Z |
| Retention status | sealed_task_evidence |

Das zweite Evidence-Objekt stützt nur die lokale Framework-Codeänderungs-
Security-Review. Es ist kein Nachweis dafür, dass eine gehostete
SonarQube-Cloud-Analyse, ein Quality Gate oder eine Exact-Head-Key-Abfrage
abgeschlossen ist.

| Feld | Framework-spezifische CPython-3.13.14-Qualifikation |
| --- | --- |
| Run ID | 20260721T055738Z-framework-pr39-delivery-followup-416b152c |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-cpython313-validation.md |
| Artifact type | framework_pr39_cpython31314_local_qualification |
| SHA-256 | 2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30 |
| Command | Framework PR #39 CPython 3.13.14 qualification receipt: hash-locked PyYAML-6.0.3 installation and pip check; 30 direct affected tests; make test-ci-security-contract (89 tests); make check-python-version; make check-github-actions-workflows; make test-workflow-security-contract (7 tests); make check-documentation; python -m compileall -q ci tests; worktree-scoped response-body guard; make lint. |
| Working directory | framework-python-updater |
| Exit code | 0 |
| Observed at | 2026-07-21T06:13:56Z |
| Retention status | retained |

Dieser Receipt belegt nur die lokale Qualifikation. Er belegt keine Hosted-
SonarQube-Cloud-, GitHub-, Review-, Branch-Protection-, Push- oder Merge-
Evidence und ändert keine Coverage- oder Scanner-Konfiguration.

### Historische PR-#39-Grundursache

Die initiale Analyse identifizierte regelspezifische Maintainability-Schulden
in eng gekoppelten CI-Security-Checks, Python-Version-Validierung,
Updater-Metadatenbehandlung und einer Unit-Test-Exception-Assertion. Nur eine
frische Hosted-Analyse kann zeigen, dass die ursprünglichen Scanner-Findings
auf dem eingereichten Head nicht mehr reproduzieren.

### Historische PR-#39-Akzeptanzkriterien und Validierungsplan

1. Eine frische SonarQube-Cloud-PR-Analyse ist an den exakten eingereichten
   Framework-PR-#39-Remediation-Head gebunden.
2. Jeder der 25 ursprünglichen Keys fehlt in dieser Exact-Head-Analyse.
3. Kein NOSONAR, keine Suppression, Regeländerung, Quality-Gate-Änderung,
   Exclusion, False-Positive-Disposition oder Risikoakzeptanz wird verwendet.
4. Die Framework-spezifische CPython-3.13.14-Qualifikation bewahrt hash-locked
   PyYAML-6.0.3, pip check, 30 direkte betroffene Tests, 89 make
   test-ci-security-contract Tests, Workflow- und Dokumentations-Checks,
   python -m compileall -q ci tests, den Response-Body-Guard und make lint.
5. SHA-adressierte Evidence und englische, deutsche, Index-, Backlog- und
   Roadmap-Records bleiben synchronisiert.

Den exakten eingereichten Diff prüfen, den
20260721T055738Z-framework-pr39-delivery-followup-416b152c Framework-
spezifischen CPython-3.13.14-Qualifikations-Receipt aufbewahren, die aktuelle
FND-SONAR-0009-Nutzerentscheidung einholen, die Scope und Owner der externen
CI- und SonarQube-Cloud-Coverage-Authentifizierung auswählt und autorisiert,
dann die frische Hosted-Analyse beobachten, die vollständige ursprüngliche
Key-Menge abfragen und die Scanner- sowie Projektkonfigurationshistorie auf
verbotene Control-Änderungen untersuchen. Den lokalen Qualifikations-Receipt
nicht als Hosted-SonarQube-Cloud-, GitHub-, Review-, Branch-Protection-, Push-
oder Merge-Evidence behandeln.

### Historische PR-#39-Regression- und Legitimate-Control-Tests

Regression-Tests:

- tests/ci_security/test_framework_ci_security_contract.py
- tests/ci_security/test_python_version_contract.py
- tests/ci_security/test_update_python_version.py

Legitimate Controls:

- Gültige CI-Security-Contract-Inputs bleiben akzeptiert, während ungültige
  Workflow- oder Context-Inputs abgewiesen bleiben.
- Gültige Python-Version-Workflow- und Release-Metadaten-Inputs behalten ihr
  Acceptance- und Failure-Verhalten.
- Der Updater behält striktes Metadaten-Parsing, Check-only-Nichtschreib-
  Verhalten und kontrolliertes atomares Update-Verhalten.

### Historische PR-#39-Dependencies, Blocker, Related Findings und Restrisiko

- Dependencies: FND-SONAR-0009, eine aktuelle Nutzerentscheidung, die Scope
  und Owner der externen CI- und SonarQube-Cloud-Coverage-Authentifizierung
  auswählt und autorisiert, eine autorisierte Framework-Einreichung und eine
  frische SonarQube-Cloud-PR-Analyse für genau diesen Head.
- Blocked by: FND-SONAR-0009 benötigt diese aktuelle Nutzerentscheidung, bevor
  die Delivery fortfahren kann; Hosted-SonarQube-Cloud-Bestätigung für den
  exakten Head wurde nach dieser Entscheidung und einer autorisierten
  Einreichung noch nicht beobachtet.
- Related Findings: FND-FRAMEWORK-0033, FND-FRAMEWORK-0037,
  FND-FRAMEWORK-0038, FND-FRAMEWORK-0039 und FND-SONAR-0009.
- Restrisiko: ein oder mehrere ursprüngliche Keys könnten offen bleiben oder
  ein neues aufgabeneigenes Issue könnte auftreten, bis FND-SONAR-0009 seine
  erforderliche aktuelle Nutzerentscheidung erhält und der exakt eingereichte
  Head eine frische Hosted-Analyse hat. Es wurde kein Risiko akzeptiert, und
  weder die lokale CPython-3.13.14-Qualifikation noch der lokale Security-Scan
  verzichten auf die Exact-Head-Hosted-Anforderung.

### Historische PR-#39-Historie

| Zeit | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-21T04:48:27Z | framework_pr39_code_smell_remediation_finding_created | Als separates Framework-P2-Nichtsecurity-SonarQube-Cloud-Finding nach SHA-256-Verifikation des zurückgehaltenen initialen 25-Key-Inventars angelegt. Die lokale Remediation ist fixed; alle ursprünglichen Keys benötigen weiterhin frische Hosted-Exact-Head-Bestätigung ohne Scanner-Control-Änderungen. |
| 2026-07-21T06:13:56Z | framework_pr39_cpython31314_local_qualification_reconciled | Der zurückgehaltene Receipt 20260721T055738Z-framework-pr39-delivery-followup-416b152c, SHA-256 2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30, etabliert eine Framework-spezifische CPython-3.13.14-virtuelle Umgebung, hash-locked-PyYAML-6.0.3-Installation und pip check, 30 direkte betroffene Tests, 89 make test-ci-security-contract Tests, Workflow- und Dokumentations-Checks, python -m compileall -q ci tests, den Response-Body-Guard und make lint. Er ersetzt die lokale blocked_environment-Prämisse. Status bleibt fixed; FND-SONAR-0009 benötigt weiterhin die aktuelle Coverage-Authentifizierungs-Nutzerentscheidung und die Hosted-SonarQube-Cloud-Exact-Head-Bestätigung steht weiter aus. |
