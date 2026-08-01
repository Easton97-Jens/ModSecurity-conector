# FND-FRAMEWORK-0051 — Framework-PR #42: Ruff-Formatierungscheck scheitert an Dateien der CPython-3.14-Umstellung

## Identität

| Feld | Wert |
| --- | --- |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / confirmed |
| Status / Feasibility | verified / already_fixed |
| Release-Blocker / Sicherheitsrelevanz | false / false |
| Historische fehlschlagende Revision | e0564d219980d62bc37162ac6c11641f289f1b71 |
| Exakte behobene Revision | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Exakter verifizierter Framework-Master | 935cf14c676a24672be5c336e92cd13457cc35c8 |
| Pull Request / Check | #42 / python-ci-security-quality |

## Zusammenfassung

Der historische Head e0564d219980d62bc37162ac6c11641f289f1b71 von Framework-PR
#42 scheiterte im GitHub-Actions-Python-Quality-Run 29956021568, Job
89045175402. Deterministischer Ruff-Lint bestand, aber ruff format --check
scheiterte an genau vier Dateien der CPython-3.14-Umstellung. Dies ist ein
bestätigter mechanischer Formatierungsfehler und ein P1-Release-Blocker für den
erforderlichen Quality-Gate, kein Nachweis eines Runtime-Defekts,
Dependency-Problems oder einer Security-Vulnerability.

Die repository-deklarierte Formatierungskorrektur ist in exaktem PR-Head
2930e04e1558b5b10bdeb87a76abb077a2085566 enthalten. Dessen Python-Quality-
Run 29962792445/Job 89067507532 besteht nach den Ruff-Stufen; aktuelle OSV-
und SonarQube-Cloud-Checks bestehen, die Mergeability ist clean und es gibt
weder Reviews noch Inline-Kommentare. Das aufbewahrte Verification-Receipt ist
framework-pr42-2930e04-hosted-verification.md mit SHA-256
4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
PR #42 wurde am 2026-07-23T07:41:13Z normal gemergt. Exakter resultierender
Framework-Master 935cf14c676a24672be5c336e92cd13457cc35c8 hat den gebundenen
CI-security-Python-quality-Workflow-Run 29989195066 mit `success`; sein Tree
5df6cce7d7385a041a817ff54fae777902645f1d entspricht dem geprüften
PR-Head-Tree. Das aufbewahrte Postmerge-Receipt ist
framework-pr42-20260723-postmerge-verification.md mit SHA-256
0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
Der ursprüngliche Ruff-CI-Fehler ist deshalb verified, nicht closed.

## Beobachtetes und erwartetes Verhalten

Das Receipt erfasst, dass Run 29956021568/Job 89045175402 deterministischen
Ruff-Lint bestand und danach nur ruff format --check für folgende Dateien
scheiterte:

- ci/checks/security/check-ci-security-contract.py
- ci/checks/security/check-python-version.py
- ci/tools/update-python-version.py
- tests/ci_security/test_update_python_version.py

Der bestehende Python-Quality-Job muss mit unveränderten aktuellen Ruff-Lint-
und Formatter-Verträgen bestehen. Diese vier Dateien müssen sauber formatieren,
ohne eine Ruff-Regel, Formatter-Konfiguration, Baseline, Exclusion,
Suppression, Quality-Gate-Scope oder einen Security-/Test-Control zu ändern.

## Auswirkung, Grundursache und Remediation

Der historische e056-PR-#42-Head konnte einen erforderlichen Python-Quality-Gate
nicht erfüllen. Das retained Receipt belegt Ergebnis und exakte Dateimenge,
aber keinen Source-Diff oder rohen Formatter-Output. Die gestützte
Grundursachenaussage ist auf diese Dateien beschränkt, die den bestehenden
Ruff-Formatierungsvertrag an e0564d219980d62bc37162ac6c11641f289f1b71 nicht
erfüllen.

Das Framework-Follow-up wendete nur die vom Repository deklarierte Ruff-
Formatierungskorrektur auf die vier genannten Dateien an. Es änderte weder
Ruff-Konfiguration, Exclusion, Baseline, Suppression, Quality Gate noch
Security-/Test-Verhalten.

Der exakte Python-Quality-Workflow auf dem resultierenden Master besteht jetzt;
dieser behobene nicht-sicherheitsrelevante Defekt ist daher kein Release-Blocker
mehr. Dadurch wird kein Ruff-, CI-, Test-, Security- oder Quality-Gate-Control
abgeschwächt.

## Evidence und Reproduktion

| Feld | Wert |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-e056-hosted-ci-failures.md |
| Artifact type | task_owned_framework_pr42_e056_hosted_ruff_format_failure_receipt |
| SHA-256 | 5940246feb917a3d83a7372ef09f2f54673cf506ec24d457d5dec5dfeaa381be |
| Producer command | Im retained Receipt nicht aufgezeichnet |
| Working directory | GitHub Actions hosted runner (external); Receipt liegt unter dem task-eigenen Parent-Run-Root |
| Exit code / Observed at | 1 / 2026-07-22 |
| Retention status | task_owned_retained_evidence |

Das Receipt enthält keinen Producer-Befehl, keinen rohen Formatter-Output und
keine präzisere Beobachtungszeit. Dieser Record erfindet keinen dieser Werte.

Reproduktion durch Inspektion von GitHub-Actions-Run 29956021568/Job
89045175402 für exakten Head e0564d219980d62bc37162ac6c11641f289f1b71,
Verifikation des retained Receipt-Hash und anschließenden Lauf des vom
Repository deklarierten Ruff-Formatters in einer getrennt autorisierten
Framework-Aufgabe mit dem ausgewählten Framework-Interpreter.

### Resulting-Master-Evidence

| Feld | Wert |
| --- | --- |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Artifact type | task_owned_framework_pr42_resulting_master_verification_receipt |
| SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Befehle | RTK-umhülltes GitHub-PR-/Ref-/Commit-/Workflow-/Check-Suite-, SonarQube-Cloud- und Boundary-State-Readback; exakte Befehle stehen im Receipt |
| Working directory / Exit code / Observed at | /root/git/ModSecurity-conector / 0 / 2026-07-23T07:51:09Z |
| Retention status | task_owned_retained_evidence |

Das Receipt erfasst den normalen `merge` von PR #42, exakten Master
935cf14c676a24672be5c336e92cd13457cc35c8 und erfolgreichen CI-security-
Python-quality-Workflow-Run 29989195066. Es ist die Resulting-Master-Evidence
für den verified-Übergang; es behauptet nicht, dass getrennte SonarQube- oder
Cloudflare-Delivery-Bedingungen bestehen.

## Akzeptanzkriterien und Validierungsplan

1. Nur die vier genannten Dateien erhalten repository-deklarierten
   Ruff-Formatter-Output; Regeln, Konfiguration, Baselines, Scope,
   Suppressions, Quality Gates und Security-/Test-Semantik bleiben unverändert.
2. Die deklarierten Ruff-Lint- und ruff format --check-Controls bestehen für
   den betroffenen Scope mit dem ausgewählten Framework-Interpreter.
3. Exakter PR-#42-Head 2930e04e1558b5b10bdeb87a76abb077a2085566 besteht
   python-ci-security-quality einschließlich der Ruff-Formatter-Stufe.
   Historischer fehlschlagender e056-Run 29956021568 ist kein Ersatznachweis.
4. PR #42 wird normal gemergt und exakte Resulting-Master-Evidence erfasst
   einen erfolgreichen CI-security-Python-quality-Workflow vor dem
   verified-Übergang; closure ist nicht Teil dieses Updates.

Der begrenzte Formatter-Diff, die deklarierten Ruff-Lint-/Format-Befehle, die
betroffenen Contracts und das frische Hosted-Ergebnis sind für den behobenen
exakten Head aufgezeichnet.

## Regressions- und Legitimate-Control-Tests

Regression-Tests:

- Repository-deklariertes ruff format --check für die vier genannten Dateien.
- Repository-deklarierter Ruff-Lint für denselben Scope.
- GitHub Actions python-ci-security-quality auf einem neuen exakten
  Framework-PR-#42-Head.

Legitimate Controls:

- Deterministischer Ruff-Lint bleibt unter unveränderter Konfiguration
  erfolgreich.
- Bestehende CI-Security-Contracts und Python-Version-Verhalten bleiben ohne
  Formatter-Exclusion, Suppression oder Quality-Gate-Änderung abgedeckt.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

- Abhängigkeiten: keine für dieses verified Finding; closure ist bewusst nicht
  Teil dieses Updates.
- Blocker: keine für diesen behobenen Ruff-Defekt.
- Verwandte Findings: FND-FRAMEWORK-0044, FND-FRAMEWORK-0046,
  FND-FRAMEWORK-0049, FND-FRAMEWORK-0050, FND-SONAR-0002 und
  FND-GITHUB-0007.

Für diesen Ruff-Defekt ist kein Risiko akzeptiert. Der erfolgreiche
Resulting-Master-Python-Quality-Workflow verifiziert den ursprünglichen Fehler.
FND-SONAR-0002 und FND-GITHUB-0007 sind separate akzeptierte PR-#42-Delivery-
Limitierungen; ihre globalen Records bleiben separat blocked, und keine
Limitierung blockiert, schließt oder verändert dieses behobene Finding. Kein
Formatter-, Lint-, Test-, Security- oder Gate-Control darf geschwächt werden.

## Historie

- 2026-07-23T07:51:09Z — framework_pr42_resulting_master_ruff_verified:
  PR #42 wurde am 2026-07-23T07:41:13Z normal gemergt. Exakter resultierender
  Framework-Master 935cf14c676a24672be5c336e92cd13457cc35c8, dessen Tree
  5df6cce7d7385a041a817ff54fae777902645f1d dem geprüften PR-Head-Tree
  entspricht, hat erfolgreichen CI-security-Python-quality-Run 29989195066.
  Die aufbewahrte Postmerge-Verification-Receipt-SHA-256 ist
  0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
  FND-SONAR-0002 und FND-GITHUB-0007 bleiben separate akzeptierte PR-#42-
  Delivery-Limitierungen und blockieren diesen behobenen Ruff-Defekt nicht.
- 2026-07-22T22:35:46Z — framework_pr42_2930_exact_head_ruff_fixed:
  Exakter Head 2930e04e1558b5b10bdeb87a76abb077a2085566 bestand Python-
  Quality-Run 29962792445/Job 89067507532 nach den behobenen Ruff-Stufen. Die
  aufbewahrte Receipt-SHA-256 ist
  4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
  Der Status ist nur fixed; es erfolgten kein Master-Merge, keine Resulting-
  Master-Evidence, keine Parent-Gitlink-Aktion und keine MRTS-Aktion.
- 2026-07-22T21:23:05Z —
  framework_pr42_e056_hosted_ruff_format_failure_tracked: Nach Receipt-Review
  und Deduplizierung erfasst dieses getrennte Finding exakten Head
  e0564d219980d62bc37162ac6c11641f289f1b71, Run 29956021568/Job
  89045175402, bestandenen deterministischen Ruff-Lint und den Vier-Dateien-
  ruff format --check-Fehler. Es wird keine Source-, Git-, GitHub-, Parent-,
  Framework- oder MRTS-Aktion behauptet.
