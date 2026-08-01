# FND-FRAMEWORK-0052 — Framework-PR #42: CPython-3.14-Pyright weist zwei Test-Fixture-Annotationen zurück

## Identität

| Feld | Wert |
| --- | --- |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Severity / Confidence | P1 / not_applicable / confirmed |
| Status / Feasibility | verified / already_fixed |
| Release-Blocker / sicherheitsrelevant | false / false |
| Historische fehlerhafte Revision | f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c |
| Exakte behobene Revision | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Exakter verifizierter Framework-Master | 935cf14c676a24672be5c336e92cd13457cc35c8 |
| Pull Request / Check | #42 / python-ci-security-quality |

## Zusammenfassung

Der historische Head f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c von Framework-PR
#42 scheiterte im GitHub-Actions-Python-Quality-Run 29961019802, Job
89061788219, während gehostetes CPython 3.14.6 den gepinnten Pyright-Befehl
ausführte. Das aufbewahrte Receipt zeichnet genau zwei Test-Fixture-Diagnosen
auf: urllib.error.HTTPError benötigt Message[str, str]-Header statt eines
untypisierten leeren dict, und ein inferiertes dict[str, str] darf nicht mit
dict[str, object] gemischt werden, weil Dictionaries invariant sind.

Die fokussierte test-only-Korrektur ist jetzt in exaktem PR-Head
2930e04e1558b5b10bdeb87a76abb077a2085566 enthalten. Dessen gehosteter
CPython-3.14.6-Python-Quality-Run 29962792445/Job 89067507532 besteht die
gepinnte Pyright-Phase; aktuelle OSV- und SonarQube-Cloud-Checks bestehen und
es gibt weder Review noch Inline-Kommentar. Das aufbewahrte Verification-Receipt
ist framework-pr42-2930e04-hosted-verification.md mit SHA-256
4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.

Dieser historische P1-nicht-sicherheitsrelevante CI-Blocker ist getrennt von
den früheren OSV-, Ruff- und Fünf-Diagnosen-Pyright-Findings. PR #42 wurde am
2026-07-23T07:41:13Z normal gemergt, und exakter resultierender Framework-Master
935cf14c676a24672be5c336e92cd13457cc35c8 hat den gebundenen CI-security-
Python-quality-Workflow-Run 29989195066 mit `success`. Sein Tree
5df6cce7d7385a041a817ff54fae777902645f1d entspricht dem geprüften
PR-Head-Tree. Das aufbewahrte Postmerge-Receipt ist
framework-pr42-20260723-postmerge-verification.md mit SHA-256
0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
Der ursprüngliche Pyright-CI-Fehler ist deshalb verified, nicht closed.

## Beobachtetes und erwartetes Verhalten

Der historische Python-Quality-Workflow erreichte seine gepinnte Pyright-Phase
und scheiterte mit genau zwei Fehlern in
tests/ci_security/test_update_python_version.py:224 und :255. Der Job meldete
keinen Updater-Runtime-, Workflow-, Dependency-, OSV-, Berechtigungs-, Token-
oder Security-Control-Fehler.

Der bestehende gepinnte Pyright-Befehl muss unter gehostetem CPython 3.14.6 mit
unveränderter Type-Quality-Konfiguration des Repositorys erfolgreich
abschließen. Die Fixtures müssen Standardbibliotheks-HTTPError-Header und
heterogene Release-Records korrekt modellieren, ohne Updater-Verhalten zu
ändern.

## Auswirkung, Grundursache und Remediation

Der historische f2-PR-Head konnte einen erforderlichen Python-Quality-Gate nicht
erfüllen. Die Fixtures sind verhaltensmäßig ausreichend, aber für den
gepinten Pyright-Standardbibliotheksvertrag unvollständig typisiert: HTTPError
hdrs ist Message[str, str], und Python-Dictionaries sind invariant. Der
Produkt-Updater und die CI-Konfiguration sind nicht die fehlerhafte Grenze.

Die fokussierte Korrektur erzeugt Message[str, str] für die
HTTPError-Fixture-Header und annotiert den heterogenen Fixture-Record als
dict[str, object]. Sie ändert weder Updater-Code noch Pyright-/Ruff-
Konfiguration, Dependencies, Workflow-Berechtigungen, Suppressions, Quality
Gates oder Security-Controls.

Der exakte Python-Quality-Workflow auf dem resultierenden Master besteht jetzt;
dieser behobene nicht-sicherheitsrelevante Defekt ist daher kein Release-Blocker
mehr. Dadurch wird kein Static-Analysis-, Formatter-, Workflow-, Test-,
Security- oder Quality-Gate-Control abgeschwächt.

## Evidence und Reproduktion

| Feld | Wert |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact-Pfad | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-f2-hosted-pyright-failure.md |
| Artifact-Typ | task_owned_framework_pr42_f2_hosted_pyright_failure_receipt |
| SHA-256 | 519327a8a07a13ba70a4679577d31a792238a949d3f7ea6d44270e23ed903050 |
| Producer-Befehl | node "$TOOLS_DIR/pyright/index.js" --project pyrightconfig.json |
| Working Directory | GitHub-Actions-Hosted-Runner für Framework-PR #42 |
| Exit-Code / beobachtet am | 1 / 2026-07-22T21:55:59Z |
| Retention-Status | task_owned_retained_evidence |

Reproduktion durch Inspektion von GitHub-Actions-Run 29961019802/Job
89061788219 für exakten Head f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c,
Verifikation des Receipt-Hashs und Ausführung des Repository-gepinnten
Pyright-Befehls im Hosted-Workflow oder einer äquivalent provisionierten
Framework-Tool-Umgebung nach dem fokussierten Follow-up.

### Resulting-Master-Evidence

| Feld | Wert |
| --- | --- |
| Artifact-Pfad | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Artifact-Typ | task_owned_framework_pr42_resulting_master_verification_receipt |
| SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Befehle | RTK-umhülltes GitHub-PR-/Ref-/Commit-/Workflow-/Check-Suite-, SonarQube-Cloud- und Boundary-State-Readback; exakte Befehle stehen im Receipt |
| Working Directory / Exit-Code / beobachtet am | /root/git/ModSecurity-conector / 0 / 2026-07-23T07:51:09Z |
| Retention-Status | task_owned_retained_evidence |

Das Receipt erfasst den normalen `merge` von PR #42, exakten Master
935cf14c676a24672be5c336e92cd13457cc35c8 und erfolgreichen CI-security-
Python-quality-Workflow-Run 29989195066. Es ist die Resulting-Master-Evidence
für den verified-Übergang; es behauptet nicht, dass getrennte SonarQube- oder
Cloudflare-Delivery-Bedingungen bestehen.

## Akzeptanzkriterien und Validierungsplan

1. Nur tests/ci_security/test_update_python_version.py ändert sich, und die
   bestehenden Runtime-Assertions behalten ihr Verhalten.
2. Fokussierter Ruff-Lint, Ruff-Format-Check, das direkte Unittest-Modul und
   make test-ci-security-contract bestehen ohne Änderung eines
   Pyright-/Ruff-/Workflow-/Controls.
3. Exakter PR-#42-Head 2930e04e1558b5b10bdeb87a76abb077a2085566 besteht
   gehostetes python-ci-security-quality einschließlich gepinntem Pyright
   unter CPython 3.14.6; historischer Run 29961019802 ist keine Ersatzevidence.
4. Aktuelle Exact-Head-OSV- und SonarQube-Cloud-Ergebnisse werden zusammen mit
   den übrigen erforderlichen PR-Checks erneut gelesen, bevor verified_pr in
   Betracht kommt.
5. PR #42 wird normal gemergt und exakte Resulting-Master-Evidence erfasst
   einen erfolgreichen CI-security-Python-quality-Workflow, bevor dieses
   Finding verified wird; kein Parent-Gitlink oder MRTS ändert sich. Closure
   ist nicht Teil dieses Updates.

Die Validierungsreihenfolge ist Ein-Datei-Diff-/Whitespace-Review; fokussierte
Repository-native Ruff-, Unittest- und Contract-Checks; expliziter
Ein-Datei-Commit/Push samt SHA-Gleichheit; danach frisches gehostetes
Pyright-Ergebnis und vollständige Current-Head-PR-Neuprüfung.

## Regression- und Legitimate-Control-Tests

Regressionstests:

- python -m unittest tests.ci_security.test_update_python_version -v
- ruff check tests/ci_security/test_update_python_version.py
- ruff format --check tests/ci_security/test_update_python_version.py
- make test-ci-security-contract
- GitHub Actions python-ci-security-quality auf dem neuen exakten PR-#42-Head

Legitime Controls:

- Die HTTPError-Fixture übt weiterhin den Updater-HTTP-404-Pfad mit typisierten
  leeren Message-Headern aus.
- Der unabhängige Python-3.13-Record bleibt vor Release-Flag-Auswertung
  ausgeschlossen, während die heterogene Fixture typsicher ist.
- Gehostete Pyright-, OSV- und SonarQube-Cloud-Controls bleiben aktiviert.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

- Abhängigkeiten: keine für dieses verified Finding; closure ist bewusst nicht
  Teil dieses Updates.
- Blocker: keine für diesen behobenen Pyright-Defekt.
- Verwandte Findings: FND-FRAMEWORK-0046, FND-FRAMEWORK-0049,
  FND-FRAMEWORK-0051, FND-SONAR-0002 und FND-GITHUB-0007.

Für diesen Pyright-Defekt ist kein Risiko akzeptiert. Der erfolgreiche
Resulting-Master-Python-Quality-Workflow verifiziert den ursprünglichen Fehler.
FND-SONAR-0002 und FND-GITHUB-0007 sind separate akzeptierte PR-#42-Delivery-
Limitierungen; ihre globalen Records bleiben separat blocked, und keine
Limitierung blockiert, schließt oder verändert dieses behobene Finding. Kein
Static-Analysis-, Formatter-, Workflow-, Dependency-, Test-, Security- oder
Quality-Gate-Control darf abgeschwächt werden, um einen Pass zu erzielen.

## Historie

- 2026-07-23T07:51:09Z — framework_pr42_resulting_master_pyright_verified:
  PR #42 wurde am 2026-07-23T07:41:13Z normal gemergt. Exakter resultierender
  Framework-Master 935cf14c676a24672be5c336e92cd13457cc35c8, dessen Tree
  5df6cce7d7385a041a817ff54fae777902645f1d dem geprüften PR-Head-Tree
  entspricht, hat erfolgreichen CI-security-Python-quality-Run 29989195066.
  Die aufbewahrte Postmerge-Verification-Receipt-SHA-256 ist
  0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
  FND-SONAR-0002 und FND-GITHUB-0007 bleiben separate akzeptierte PR-#42-
  Delivery-Limitierungen und blockieren diesen behobenen Pyright-Defekt nicht.
- 2026-07-22T22:35:46Z — framework_pr42_2930_exact_head_pyright_fixed:
  Exakter Head 2930e04e1558b5b10bdeb87a76abb077a2085566 bestand gehostetes
  CPython-3.14.6-gepinntes Pyright in Run 29962792445/Job 89067507532. Die
  aufbewahrte Receipt-SHA-256 ist
  4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
  Der Status ist nur fixed; es erfolgten kein Master-Merge, keine Resulting-
  Master-Evidence, keine Parent-Gitlink-Aktion und keine MRTS-Aktion.
- 2026-07-22T22:08:40Z — framework_pr42_f2_hosted_pyright_fixture_failure_tracked:
  nach Deduplizierung als eigenständiger CI-Fehler angelegt. Exakter PR-#42-Head
  f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c scheiterte in Run 29961019802/Job
  89061788219 mit genau zwei Test-Fixture-Type-Diagnosen unter gehostetem
  CPython 3.14.6. Die task-owned Source-Korrektur ist uncommitted; kein
  gehosteter Erfolg, Merge, Parent-Aktion oder MRTS-Aktion wird behauptet.
