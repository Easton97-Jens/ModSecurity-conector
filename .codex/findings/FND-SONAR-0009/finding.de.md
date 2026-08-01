# FND-SONAR-0009 — Der Model-1-Same-Repository-Coverage-Workflow für Framework-PR #39 ist lokal implementiert; die Hosted-SonarQube-Cloud-Coverage bleibt extern blockiert

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-SONAR-0009 |
| Kategorie | sonarqube_finding |
| SonarQube-Cloud-Klassifikation | coverage_configuration |
| Repository / Ownership | framework / sonarqube_configuration |
| Priorität / Severity / Confidence | P1 / not_applicable / validated |
| Lifecycle-Status / Feasibility | blocked / blocked_external_dependency |
| Release-Blocker / Security relevant | true / true |
| Profil | Framework PR #39 Model 1 same-repository SonarQube Cloud coverage |
| Finale Disposition | null |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

Der Nutzer hat Model 1 ausgewählt. Der Framework-Worktree enthält nun einen
lokalen Same-Repository-Pull-Request-Workflow, der fokussierte hash-gesperrte
Tests unter Coverage.py ausführt, transientes Cobertura XML erzeugt und den
festen SonarQube-Cloud-Scanner aufruft. Die lokale Implementierung ist
abgeschlossen, doch das Finding bleibt blocked, nicht fixed oder verified.

Die zurückgehaltene ursprüngliche PR-#39-Beobachtung lautete 0,0 % Coverage on
New Code. Die finale kombinierte direkte Suite nach dem Master-Sync bestand
23 Tests in 31.756s: 14 CI-security-evidence-contract tests und 9
workflow-security tests. Der generische Workflow-Checker, der CI-security
contract checker, der CI-security evidence-contract checker, die ausgewählte
Syntax-Kompilierung und `make lint` bestanden ebenfalls. `make lint` umfasste
90 CI-security-Tests, Dokumentationsprüfungen und `git diff --check`.

Diese lokalen Ergebnisse können keine Projekt-Token-Konfiguration, keine
Umstellung von automatischer auf CI-basierte Analyse, keine GitHub-Actions-
Ausführung, keine Scanner/Import-Ausführung, keine Hosted-Coverage, kein
Hosted-Quality-Gate und keine Exact-Head-Delivery belegen. Der getrennte
lokale CPython-_sqlite3-Blocker verhindert lokales Cobertura XML und wird in
FND-HOST-0006 erfasst. Er darf nicht mit dem Hosted-Configuration-Blocker
vermischt werden.

## Tatsächlicher Model-1-Framework-Scope und Trust Boundary

| Art | Tatsächlicher Framework-Pfad oder Symbol |
| --- | --- |
| Workflow | .github/workflows/ci-security-coverage.yml |
| Generisches Workflow-Control | ci/checks/security/check-github-actions-workflows.py |
| CI-Security-Control | ci/checks/security/check-ci-security-contract.py |
| Evidence-Contract-Control | ci/checks/security/check-ci-security-evidence-contract.py |
| Evidence-Contract-Test | tests/ci_security/test_ci_security_evidence_contract.py |
| Workflow-Security-Test | tests/security_regression/test_workflow_security_contract.py |
| Gesperrte Coverage-Dependency | requirements-ci.lock, coverage==7.15.2 |
| Evidence-Contract-Symbole | same_repository_sonar_coverage_errors, same_repository_sonar_coverage_job_errors, same_repository_sonar_coverage_producer_errors |

Der Workflow ist auf einen Same-Repository-Pull-Request begrenzt, checkt den
exakten Pull-Request-Head ohne persistierte Credentials aus, verwendet
runner-lokale Coverage-Pfade und beschränkt SONAR_TOKEN auf die geprüfte feste
Scanner-Action. Seine lokalen Controls beweisen nicht, dass im Hosted-Projekt
ein nutzbares Token existiert.

## Tatsächliche finale lokale Validierung

Alle folgenden Commands liefen in:

~~~text
/var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater
~~~

Nach normaler Synchronisierung mit `origin/master`
`f73f8842f45318e2df8aff1d31855eeb7c20a22f` war der lokale HEAD der
Merge-Commit `0b0c20f686fcc2fd76a7035daf691bc17566d2e1`;
`origin/master...HEAD` war `0 5`, und die Task-Änderungen wurden nach dem
Merge unstaged wiederhergestellt.

| Check | Ergebnis |
| --- | --- |
| Kombinierte direkte Suiten | exit 0; Ran 23 tests in 31.756s; OK |
| Generischer Workflow-Checker | exit 0; output includes ok ci-security-coverage.yml |
| CI-security contract checker | exit 0; CI security contract passed. |
| CI-security evidence-contract checker | exit 0; CI security evidence contract passed. |
| Ausgewählte Model-1-Checker-Syntax | exit 0 |
| Finales `make lint` | exit 0; umfasst 90 CI-security-Tests, Dokumentationsprüfungen und `git diff --check` |

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-refactor-pycache .venv/bin/python -m unittest -v tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-checkers-pycache .venv/bin/python ci/checks/security/check-github-actions-workflows.py --workflow-root .github/workflows --check all
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-checkers-pycache .venv/bin/python ci/checks/security/check-ci-security-contract.py --root .
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-checkers-pycache .venv/bin/python ci/checks/security/check-ci-security-evidence-contract.py --root .
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-refactor-pycache .venv/bin/python -m compileall -q ci/checks/security/check-github-actions-workflows.py ci/checks/security/check-ci-security-evidence-contract.py
~~~

~~~text
make lint
~~~

Dies sind nur direkte lokale Checks. Sie sind keine Hosted-Scanner-,
Report-Import-, Quality-Gate- oder Delivery-Evidence.

## Evidence und Reproduktion

| Feld | Ursprüngliche Coverage-Beobachtung | Lokales Coverage.py-Blocker-Receipt |
| --- | --- | --- |
| Run ID | 20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8 | 20260721T055738Z-framework-pr39-delivery-followup-416b152c |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8/evidence/sonar-pr39-initial-inventory.md | /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-coverage-sqlite-blocker.md |
| Artifact type | markdown | coverage_validation_blocker_receipt |
| SHA-256 | f9feb36fe34055f6c17f47ed0011803d70b3128a2104d483bad9b01be54dcddd | 15d6518ccdb7015622df3bda5d0d1c0c4726096e3e4a392314786b448157cf9e |
| Working directory | /root/git/ModSecurity-conector | /var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater |
| Exit code | 0 | 1 |
| Observed at | 2026-07-21T04:40:00Z | 2026-07-21T07:41:04Z |
| Retention | retained | retained |

Das lokale Blocker-Receipt dokumentiert diesen exakten Coverage.py-Command:

~~~text
.venv/bin/python -m coverage run -m unittest -v tests.ci_security.test_framework_ci_security_contract tests.ci_security.test_python_version_contract tests.ci_security.test_update_python_version tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract
~~~

Er endete mit 1 vor den Tests, weil coverage.sqldata sqlite3 importiert und
der Standardbibliotheksimport danach mit ModuleNotFoundError für _sqlite3
fehlschlug. Das Receipt existiert am aufgezeichneten externen Pfad und sein
SHA-256 wurde verifiziert. Es ist retained und kein erfundener Cobertura-Report.

### Erneuertes Delivery-Preflight-Receipt

Das geheimnissichere erneuerte Receipt ist unter
`.codex/runs/20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2/evidence/framework-pr39-renewed-sonar-delivery-preflight-receipt.json`
aufbewahrt. Sein SHA-256 lautet
`8141302e6bbd8303c7b86e2bdf50f35ebd7e669aaefb9faf9aa1f4d41cde5863`.
Das versiegelte Run-Manifest und das nicht selbstreferenzielle Hash-Inventar
sind
`.codex/runs/20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2/manifest.json`
und
`.codex/runs/20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2/hash-inventory.json`.

| Feld | Erneuerte Preflight-Beobachtung |
| --- | --- |
| Run-ID | 20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2 |
| Framework local HEAD / enthaltenes `origin/master` | 0b0c20f686fcc2fd76a7035daf691bc17566d2e1 / f73f8842f45318e2df8aff1d31855eeb7c20a22f |
| Remote-PR-#39-Head / Status | 0b0c20f686fcc2fd76a7035daf691bc17566d2e1 / draft, `mergeable=true` und `UNSTABLE`, weil ein Check fehlschlägt |
| Repository-Actions-Secrets | list exit 0 und reported empty; API count 0; kein Credential-Wert aufbewahrt |
| Öffentliche Sonar-Einstellung | inherited `sonar.autoscan.enabled=true` |
| Aktuelle PR-Metriken | keine Coverage-Metrik zurückgegeben; nur `new_duplicated_lines_density=0.0` |
| New-Code-Issues | 25 `OPEN`/`CONFIRMED` Issues |
| Aktuelles Gate | `OK` auf dem exakten aktuellen PR-#39-Head, ohne Coverage-Condition |

Das Receipt hält nur vom Parent bereitgestellte Ergebniszusammenfassungen fest.
Es bewahrt keine rohe Endpoint-Antwort auf, spielt keine Endpoint-Commands
erneut ab oder rekonstruiert sie und erfindet nicht den exakten älteren
Quality-Gate-SHA. Das Repository-Actions-Secret-Ergebnis ist auf die
gemeldete Repository-Liste und den API-Count begrenzt; es belegt nicht, dass
Organization-, Environment- oder andere externe Credential-Configuration
fehlt.

Diese erneuerte Evidence bestätigt die bestehende Disposition, statt sie zu
ändern: Der exakte aktuelle Remote-Head ist verfügbar, doch es wurde keine
Coverage-Metrik oder kein Model-1-Scanner/Import-Run beobachtet. Sein aktuelles
`OK` Quality Gate hat keine Coverage-Condition. Der Lifecycle bleibt daher
`blocked` / `blocked_external_dependency`, der Release-Blocker bleibt true,
und es wurde kein Risiko akzeptiert.

## Ursache, Remediation, Akzeptanzkriterien und Validierungsplan

Die ursprüngliche Bedingung hatte zwei unabhängige Ursachen. Model 1 behebt
das lokale Fehlen von Workflow/Configuration. Die verbleibende Hosted-
Bedingung ist eine externe Projektabhängigkeit: Der Projekt-Owner muss einen
dedizierten least-privilege SONAR_TOKEN konfigurieren und das bestehende
SonarQube-Cloud-Projekt von automatischer auf CI-basierte Analyse umstellen.
Keine der Aktionen erfolgte in dieser Aufgabe.

Für die Akzeptanz müssen alle folgenden Punkte erfüllt sein:

1. Die aufgeführten lokalen Model-1-Workflows und Controls bleiben passing.
2. Der Projekt-Owner konfiguriert einen dedizierten least-privilege SONAR_TOKEN
   ohne seinen Wert offenzulegen.
3. Das bestehende Projekt wird von automatischer auf CI-basierte Analyse
   umgestellt.
4. Ein Exact-Head-Same-Repository-Workflow-Run erzeugt und importiert einen
   nichtleeren Cobertura-XML-Report.
5. Die passende frische SonarQube-Cloud-Analyse zeigt die importierte Coverage
   und ihr tatsächliches Quality-Gate-Ergebnis.
6. Es werden keine Thresholds abgesenkt, keine relevanten Exclusions,
   Suppressions, False-Positive-Dispositionen, Rule/Gate-Änderungen oder
   Risikoakzeptanzen verwendet.

Validierung nach der Owner-Aktion: die lokalen fokussierten Controls erneut
ausführen; nach Auflösung von FND-HOST-0006 den exakten lokalen Coverage.py-
Command mit der erforderlichen CPython-3.13.14-Umgebung erneut ausführen; dann
den Exact-Head-GitHub-Actions-Run, Scanner/Import-Logs, SonarQube-Cloud-
Report-Import, Coverage und Quality Gate prüfen.

## Abhängigkeiten, Blocker, Controls und Restrisiko

- Dependencies: Projekt-Owner-Konfiguration eines dedizierten least-privilege
  SONAR_TOKEN; Umstellung des bestehenden Projekts von automatischer auf
  CI-basierte Analyse; ein Exact-Head-Hosted-Same-Repository-Workflow; und
  Hosted-SonarQube-Cloud-Zugriff für die Verifikation.
- Blocked by: Keine der Projekt-Owner-Token/Configuration-Aktionen, kein
  Exact-Head-Model-1-Hosted-Workflow, kein Scanner/Import-Log und kein
  importiertes Coverage-Ergebnis wurde beobachtet. Der aktuelle Remote-Head
  `0b0c20f686fcc2fd76a7035daf691bc17566d2e1` ist exakt, liegt jedoch vor den
  unstaged lokalen Model-1-Source-Änderungen; sein Quality Gate ist `OK` ohne
  Coverage-Condition.
- Lokale Legitimate Controls: Die 23 ausgewählten Tests, der generische
  Workflow-Checker, der CI-security contract checker und der CI-security
  evidence-contract checker bestanden; die beiden letzteren Controls erzwingen
  den Same-Repository-Guard und ein einzelnes geprüftes SONAR_TOKEN
  scanner-action mapping.
- Related Findings: FND-FRAMEWORK-0044, FND-HOST-0006, FND-SONAR-0002 und
  FND-SONAR-0004.

Die exakte Restrisiko-Annahme lautet: same-repository PR initiators are
authorized for the project analysis token. Dies ist keine Risikoakzeptanz.
Keine Hosted-Konfiguration, Token-Provisionierung, Scanner/Import-Ausführung,
kein Coverage-Ergebnis, Quality Gate, PR-Delivery, Framework-Delivery,
Parent-Gitlink-Update oder MRTS-Änderung wird behauptet.

## Historie

| Zeit | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-21T04:48:27Z | framework_pr39_coverage_ingestion_blocker_created | Als separates P1-blocked-SonarQube-Cloud-Configuration-Finding angelegt, nachdem retained Evidence 0.0% Coverage on New Code und keinen lokalen Coverage-Producer oder Import-Pfad bestätigte. |
| 2026-07-21T07:54:45Z | model_one_selected_locally_fixed_and_hosted_verification_blocked | Der Nutzer wählte Model 1. Lokale Same-Repository-Implementierung und finale fokussierte Static/Direct-Validierung bestanden. Dedizierte least-privilege-SONAR_TOKEN-Konfiguration und die Umstellung des SonarQube-Cloud-Projekts von automatisch auf CI-basiert bleiben unbeobachtete externe Projekt-Owner-Dependencies. FND-HOST-0006 erfasst den getrennten lokalen CPython-_sqlite3-Blocker. |
| 2026-07-21T08:13:50Z | post_master_sync_local_validation_recorded | Nach normaler Synchronisierung mit origin/master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` war der lokale HEAD `0b0c20f686fcc2fd76a7035daf691bc17566d2e1` fünf Commits voraus. Der generische Workflow-Checker, die finale kombinierte 23-Test-Suite (31.756s) und `make lint` bestanden. Hosted-SONAR_TOKEN-/Projektanalyse-Voraussetzungen und FND-HOST-0006 bleiben ungelöst. |
| 2026-07-21T08:22:13Z | lifecycle_reconciled_as_externally_blocked | Der kanonische Lifecycle ist `blocked` / `blocked_external_dependency`, weil kein Hosted-Exact-Head-Scan, keine importierte Coverage und kein Hosted-Quality-Gate beobachtet wurden. Die lokal implementierte Model-1-Workflow-Remediation ist eine abgeschlossene Teil-Remediation, keine vollständige Behebung oder Verifikation. |
| 2026-07-21T10:21:06Z | renewed_remote_delivery_preflight_recorded | Das geheimnissichere Receipt `8141302e6bbd8303c7b86e2bdf50f35ebd7e669aaefb9faf9aa1f4d41cde5863` dokumentiert übereinstimmenden Framework-local-, Origin-Task-Branch- und Remote-PR-#39-Head `0b0c20f686fcc2fd76a7035daf691bc17566d2e1` einschließlich `origin/master` `f73f8842f45318e2df8aff1d31855eeb7c20a22f`; der PR ist draft, `mergeable=true` und `UNSTABLE`, weil ein Check fehlschlägt. Es dokumentiert außerdem eine empty reported Repository-Actions-Secret-Liste/API count 0, inherited `sonar.autoscan.enabled=true`, keine Coverage-Metrik (nur `new_duplicated_lines_density=0.0`), 25 `OPEN`/`CONFIRMED` New-Code-Issues und ein aktuelles `OK` Quality Gate ohne Coverage-Condition. Es verifiziert keine importierte Coverage. |
