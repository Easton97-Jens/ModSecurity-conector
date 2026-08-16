# Change Record: Python-Workflow-Contract-Ausrichtung

**Sprache:** [English](CR-20260816-python-workflow-contract-alignment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260816-python-workflow-contract-alignment |
| Datum (UTC) | 2026-08-16 |
| Basis-Revision | 4cd60d4fef492fcaa8522b902886bea6e0256f87 |
| Delivery-Status | Der aktuelle Benutzer autorisierte ausdrücklich die Reparatur des task-eigenen PR #296 und die geschützte Integration in `master`. Der Merge bleibt von frischer Exact-Head-Review, Checks, SonarQube-Cloud-Evidence, Ruleset-Compliance und Resulting-Master-Verifikation abhängig; direkte Master-Writes, Force-Aktionen, Bypässe und Auto-Merge bleiben verboten. |

## Motivation und Problemstellung

GitHub-Actions-Run 31926824164, Job 95115630935, scheiterte ausschließlich in
Run focused Python version contracts auf Parent-master
4cd60d4fef492fcaa8522b902886bea6e0256f87. Der aktuelle Checker reproduzierte
27 Verletzungen: eine veraltete verified-report-Inventaridentität, sechs echte
Python-Jobs ohne kanonische Interpreter-Contract-Form und zwei aktuelle
Shell-Formen außerhalb der stabilen statischen Scanner-Teilmenge. Der Fehler
verhinderte, dass die angeforderte Updater-Validierung ihre fokussierten Tests
erreichte.

Die erste Exact-Head-Hosted-Analyse des Draft-PR meldete trotz bestandenem
Quality Gate ein task-eigenes New Issue: `python:S1192` bei
`ci/checks/common/check-python-version-contract.py:104` verlangt die
Deduplizierung von `update-workflow-tools.yml` über seine bestehenden
Inventareinträge publisher, resolver und validator. Der aktuelle Benutzer
verlangte ausdrücklich, dieses Issue zu beheben und den korrigierten
task-eigenen PR nach `master` zu bringen.

## Akzeptanzkriterien

- Die veraltete verified-report-Identität wird entfernt, während die einzelne
  report-governance-Workflow-Topologie unverändert bleibt.
- Jeder der sechs echten Python-Jobs ist explizit inventarisiert und nutzt die
  unveränderliche setup-python-Action, id setup-python, kanonische
  .python-version und den exakten Verifier vor Python oder Pip.
- Der CodeQL-Go-Guard und die Submodule-Pfad-Allowlist sind parser-sicher und
  behalten ihre exakte restriktive Semantik.
- Der reale Python-Contract-Checker, fokussierte Unit-/Security-Contracts,
  actionlint und Offline-ZiZmor-Checks bestehen ohne Parser-Suppression oder
  Control-Lockerung.
- Der exakte PR-Head besitzt null offene task-eigene SonarQube-Cloud-New-Issues
  ohne Suppression, Issue-Acceptance, `NOSONAR`, Exclusion oder Quality-Gate-
  Lockerung.
- Die vom Benutzer autorisierte PR-#296-Integration nutzt den
  repository-genehmigten geschützten Workflow und erhält Resulting-Master-
  Verifikation.

## Implementierungsentscheidung und Begründung

Die Korrektur entfernt nur die obsolete FND-PARENT-0062-Inventaridentität und
ergänzt genau die sechs erkannten normalen Python-Job-Identitäten, wodurch sich
das explizite Normal-Inventar von 33 auf 38 Jobs ändert. Sie fügt nur die
bereits vorhandene unveränderliche setup-python- und Verifier-Form in die
betroffenen Workflows ein und behält Trigger, Berechtigungen, Tokens und
Publisher-State-Machines bei.

Der Parser bleibt fail-closed. Der CodeQL-Bash-Regular-Expression-Guard wird
als exakte statische awk-Validierung einschließlich Ein-Zeilen-Eingabevorgabe
ausgedrückt. Der Submodule-Publisher ersetzt einen dynamischen Case-Arm durch
dieselbe Fixed-String-Whole-Line-Pfad-Allowlist. Diese Entscheidungen
adressieren FND-PARENT-0062, FND-PARENT-0162 und FND-PARENT-0163 ohne breite
Ausnahmen.

Der Sonar-Follow-up ergänzt die geschlossene Konstante
`UPDATE_WORKFLOW_TOOLS_WORKFLOW` und ersetzt nur die drei wiederholten
Dateinamenliterale. Die `JobIdentity`-Werte, Inventarreihenfolge/-kardinalität,
Parser, Setup-/Verifier-Checks und fail-closed-Ablehnungspfade bleiben
unverändert. Damit wird das lokale Finding `FND-SONAR-0042` durch eine
quellennative Reparatur statt durch eine Scanner-Abkürzung adressiert.

## Geänderte Dateien

- .github/workflows/ci-security-codeql.yml
- .github/workflows/test-apache.yml
- .github/workflows/test-haproxy.yml
- .github/workflows/update-submodules.yml
- .github/workflows/update-workflow-tools.yml
- ci/checks/common/check-python-version-contract.py
- tests/test_python_version_contract.py
- tests/test_ci_security_workflows.py
- dieses gekoppelte Change-Record-Paar und seine gekoppelten Archivindizes

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Current-Master-Checker vor dem Fix | als Fehlerreproduktion bestanden: Exit 1, 43 erkannte Jobs, 27 Verletzungen |
| Realer Checker nach dem Fix | bestanden: Status valid, 42 erkannte Jobs, 0 Verletzungen |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-python-version-contract | bestanden |
| Fokussierte Python-Contract-/Interpreter-/CI-Security-Suite | bestanden: 59 Tests |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract | bestanden: 103 Tests, 4 umgebungsbedingt übersprungen, gepinnte Tool-Validierung bestanden |
| python -m compileall -q ci scripts tests mit task-eigenem Pycache | bestanden |
| actionlint für alle .github/workflows-YAML-Dateien | bestanden |
| Offline-ZiZmor für die fünf geänderten Workflow-Dateien | bestanden: keine Befunde, 24 Repository-Suppressions |
| git diff --check vor diesem Record | bestanden |
| Öffentliche SonarQube-Cloud-PR-#296-Issue-Query vor dem Follow-up | als statische Reproduktion bestanden: genau ein OPEN `python:S1192` bei `ci/checks/common/check-python-version-contract.py:104` |
| Fokussiertes `tests.test_python_version_contract` nach dem reinen Konstanten-Follow-up | bestanden: 24 Tests einschließlich 38-Einträge-Inventar und fail-closed-Negativ-Controls |
| Realer Checker nach dem reinen Konstanten-Follow-up | bestanden: Status valid, 42 erkannte Jobs, 0 Verletzungen |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-python-version-contract nach dem Follow-up | bestanden |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract nach dem Follow-up | bestanden: 103 Tests, 4 umgebungsbedingt übersprungen, gepinnte Tool-Validierung bestanden |
| python -m compileall -q ci/checks/common tests/test_python_version_contract mit externem Pycache | bestanden |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs | blockiert: Exit 2 nur weil das absichtlich nicht initialisierte Framework-Submodule vorbestehende referenzierte Dateien fehlen lässt; kein geänderter Change-Record-Pfad wird gemeldet |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-doc-links | blockiert: Exit 2 wegen derselben vorbestehenden fehlenden Framework-Submodule-Targets; kein geänderter Change-Record-Pfad wird gemeldet |
| git diff --check nach Source- und Documentation-Follow-up | bestanden |

## Security-Auswirkung

Die betroffene Grenze umfasst GitHub-Actions-Workflow-Auswahl,
Python-Interpreter-Provenance, statische Shell-Erkennung und einen
Submodule-Maintenance-Publisher. Der Fix bewahrt unveränderliche Action-Pins,
Least Privilege, read-only Checkout-Credentials, die exakte Pfad-Allowlist,
Draft-PR-State-Controls und fail-closed Ablehnung unbekannter Shell-Syntax.
Keine Credential-, Token-, Workflow-Berechtigungs-, Trigger-, direkte
Master-Write-, Merge- oder Auto-Merge-Funktion wird ergänzt oder erweitert.

Es wird kein Exploit oder unautorisierter Write behauptet. FND-PARENT-0162 und
FND-PARENT-0163 sind sicherheitsrelevante CI-Contract-Findings, weil ein breiter
Workaround die bestehende Sicherheitsgrenze schwächen würde.

`python:S1192` selbst ist ein Maintainability-Befund, keine Sicherheitslücke.
Die Extraktion nur per Konstante ändert weder vertrauenswürdige Inputs,
akzeptierte Jobs, Berechtigungen, Trigger, Tokens, Publisher-Verhalten noch
eine Sicherheitsentscheidung.

## Runtime-Evidence

Der ursprüngliche GitHub-hosted Fehler wird im verlinkten Run und im
Task-Evidence-Root aufbewahrt. Lokale Validierung belegt nur Source- und
Contract-Verhalten. Kein Live-Workflow-Dispatch, Publisher-Token-Mint,
Maintenance-Branch-Update, Merge oder Resulting-Master-Proof wird behauptet.

## Bekannte Einschränkungen

Der erste Hosted-Check-Satz gehört zum Vorgänger-Exact-Head. Ein neuer Commit
erfordert eine frische PR-Head-SonarQube-Cloud-Analyse und alle anwendbaren
Hosted-Checks vor dem Merge. Die lokale check-ci-security-contract-Suite
übersprang vier Namespace- oder Identitäts-Tests, weil dieser Umgebung deren
erforderliche Fähigkeiten fehlen; die nicht übersprungenen Controls bestanden.

## Verbleibende Risiken

Der strenge Parser weist nicht unterstützte künftige Shell-Formen absichtlich
weiter zurück. Die neuen Source-Formen sind auf seine statische Teilmenge
beschränkt, aber Hosted-Ausführung bleibt nötig, um GitHub-Actions-Syntax und
Repository-Policy auf dem exakten PR-Head zu verifizieren. FND-PARENT-0062,
FND-PARENT-0162 und FND-PARENT-0163 können ohne diese Evidence nicht über den
lokalen Fixed-Status hinausgehen.
Das exakte Issue `AaAJBpj4Kije7nS9rbMB` bleibt offen, bis die
Successor-Head-Analyse die Reparatur nur per Konstante beweist.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Live-Updater-Dispatch oder App-Token-Mint wurde ausgeführt; diese
operativen Aktionen liegen außerhalb der statischen Inventarreparatur.
Vollständige Connector-Runtime-Matrizen sind nicht relevant. Commit, Push, ein
frischer Exact-Head-Hosted-Check-Satz, geschützter Merge,
Resulting-Master-Workflows und Workspace-Restoration stehen noch aus und werden
nur aus beobachteten Ergebnissen dokumentiert. Die vollständigen Bilingual- /
Documentation-Link-Checks wurden ausgeführt, sind aber wegen der vorbestehenden
referenzierten Pfade des absichtlich nicht initialisierten Framework-Submodules
blockiert; diese Reparatur ändert weder Framework noch unterdrückt sie die
Checks.

## Finaler Diff- und Review-Status

Die eingegrenzte Source-Änderung beschränkt sich auf den verlinkten
Actions-Fehler, seine direkte Workflow-Contract-Coverage, den einen
SonarQube-Cloud-Duplicate-Literal-Follow-up und erforderliche zweisprachige
Nachvollziehbarkeit. Lokale Source-, Security-, Syntax- und Contract-Checks
bestehen. Die Aufgabe ist erst abgeschlossen, wenn der Successor-Exact-
Remote-/PR-Head, Hosted-Checks, Sonar-Disposition, geschützter Merge,
Resulting-Master-Checks und sichere Parent-Restoration beobachtet sind.
