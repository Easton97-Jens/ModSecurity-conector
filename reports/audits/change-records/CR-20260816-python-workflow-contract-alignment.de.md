# Change Record: Python-Workflow-Contract-Ausrichtung

**Sprache:** [English](CR-20260816-python-workflow-contract-alignment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260816-python-workflow-contract-alignment |
| Datum (UTC) | 2026-08-16 |
| Basis-Revision | 4cd60d4fef492fcaa8522b902886bea6e0256f87 |
| Delivery-Status | Ein fokussierter Parent-Draft-PR ist für den verlinkten Actions-Job autorisiert. Kein Merge, direkter Master-Write, Force-Aktion, Bypass oder Auto-Merge ist autorisiert. |

## Motivation und Problemstellung

GitHub-Actions-Run 31926824164, Job 95115630935, scheiterte ausschließlich in
Run focused Python version contracts auf Parent-master
4cd60d4fef492fcaa8522b902886bea6e0256f87. Der aktuelle Checker reproduzierte
27 Verletzungen: eine veraltete verified-report-Inventaridentität, sechs echte
Python-Jobs ohne kanonische Interpreter-Contract-Form und zwei aktuelle
Shell-Formen außerhalb der stabilen statischen Scanner-Teilmenge. Der Fehler
verhinderte, dass die angeforderte Updater-Validierung ihre fokussierten Tests
erreichte.

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
- Ein task-eigener Parent-Draft-PR wird erstellt; es erfolgt kein Merge.

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

## Runtime-Evidence

Der ursprüngliche GitHub-hosted Fehler wird im verlinkten Run und im
Task-Evidence-Root aufbewahrt. Lokale Validierung belegt nur Source- und
Contract-Verhalten. Kein Live-Workflow-Dispatch, Publisher-Token-Mint,
Maintenance-Branch-Update, Merge oder Resulting-Master-Proof wird behauptet.

## Bekannte Einschränkungen

GitHub-hosted Actions-Ausführung und Exact-PR-Head-Checks sind erst verfügbar,
wenn der task-eigene Draft-PR gepusht ist. Die lokale
check-ci-security-contract-Suite übersprang vier Namespace- oder
Identitäts-Tests, weil dieser Umgebung deren erforderliche Fähigkeiten fehlen;
die nicht übersprungenen Controls bestanden.

## Verbleibende Risiken

Der strenge Parser weist nicht unterstützte künftige Shell-Formen absichtlich
weiter zurück. Die neuen Source-Formen sind auf seine statische Teilmenge
beschränkt, aber Hosted-Ausführung bleibt nötig, um GitHub-Actions-Syntax und
Repository-Policy auf dem exakten PR-Head zu verifizieren. FND-PARENT-0062,
FND-PARENT-0162 und FND-PARENT-0163 können ohne diese Evidence nicht über den
lokalen Fixed-Status hinausgehen.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Live-Updater-Dispatch, App-Token-Mint, Merge oder Resulting-Master-Rerun
wurde ausgeführt: Der Benutzer autorisierte einen neuen korrigierenden PR,
nicht operative Veröffentlichung oder Integration. Vollständige Connector-
Runtime-Matrizen sind für diese reinen Workflow-Contract-Änderungen nicht
relevant. Die finalen Bilingual-/Documentation-Link-Checks, finale
Diff-Prüfung, Commit, Push und Exact-Head-Hosted-Checks stehen noch aus und
werden nur aus beobachteten Ergebnissen dokumentiert.

## Finaler Diff- und Review-Status

Die eingegrenzte Source-Änderung beschränkt sich auf den verlinkten
Actions-Fehler, seine direkte Workflow-Contract-Coverage und erforderliche
zweisprachige Nachvollziehbarkeit. Lokale Source-, Security- und Contract-
Checks bestehen. Die Aufgabe ist erst abgeschlossen, wenn der Draft-PR erstellt
ist sowie sein exakter Remote-Head und anwendbare Hosted-Checks beobachtet
sind; ein Merge ist weder autorisiert noch impliziert.
