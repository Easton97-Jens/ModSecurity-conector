# FND-HOST-0006 — Task-CPython 3.13.14 fehlt _sqlite3 und blockiert die lokale Coverage.py-Cobertura-XML-Validierung

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-HOST-0006 |
| Kategorie | tooling |
| Repository / Ownership | host_environment / host_environment |
| Priorität / Severity / Confidence | P2 / not_applicable / confirmed |
| Lifecycle-Status / Feasibility | blocked / blocked_environment |
| Release-Blocker / Security relevant | false / false |
| Profil | Framework PR #39 local CPython 3.13.14 Coverage.py/Cobertura validation |
| Finale Disposition | null |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

Der Task-CPython-3.13.14-Umgebung fehlt das Standardbibliotheksmodul _sqlite3.
Der ausgewählte hash-gesperrte Import coverage==7.15.2 scheitert deshalb über:

~~~text
coverage.sqldata -> sqlite3 -> _sqlite3
~~~

Der exakte lokale Coverage.py-Command endete vor dem Start seiner ausgewählten
Framework-Tests mit 1 und:

~~~text
ModuleNotFoundError: No module named _sqlite3
~~~

Es wurde kein lokales Cobertura XML erzeugt, erfunden, hochgeladen oder
zurückgehalten. Dies ist ein P2-non-security-Host-Environment-Tooling-Blocker.
Er ist von FND-SONAR-0009 getrennt: Diese Finding betrifft eine lokale
Interpreter/Build-Prerequisite, nicht einen dedizierten SONAR_TOKEN, den
Projektanalysemodus, Scanner/Import-Ausführung, Hosted-Coverage oder ein
Quality Gate.

## Voraussetzungen, Scope und Reproduktion

- Framework-Worktree:
  /var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater
- Erforderliche und ausgewählte Interpreter-Lane: CPython 3.13.14.
- Gesperrte Dependency: coverage==7.15.2.
- Dem CPython-Build fehlt die SQLite-Development-Headers/pkg-config-Discovery,
  die zum Aktivieren von _sqlite3 erforderlich ist.
- Diese Aufgabe schließt Installation, Host-Rebuild und Substitute-Runtimes
  ausdrücklich aus.

Nur in der ausgewählten exakten Umgebung reproduzieren:

~~~text
.venv/bin/python -m coverage run -m unittest -v tests.ci_security.test_framework_ci_security_contract tests.ci_security.test_python_version_contract tests.ci_security.test_update_python_version tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract
~~~

Das erwartete aktuelle Ergebnis ist exit 1 vor den Tests, nicht Cobertura XML.
CPython 3.14 nicht substituieren und keine _sqlite3-Erweiterung handkopieren;
beides entwertet den exakten CPython-3.13.14-hash-gesperrten
Validierungsclaim.

## Zurückgehaltene Evidence

| Feld | Wert |
| --- | --- |
| Run ID | 20260721T055738Z-framework-pr39-delivery-followup-416b152c |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-coverage-sqlite-blocker.md |
| Artifact type | coverage_validation_blocker_receipt |
| SHA-256 | 15d6518ccdb7015622df3bda5d0d1c0c4726096e3e4a392314786b448157cf9e |
| Command | .venv/bin/python -m coverage run -m unittest -v tests.ci_security.test_framework_ci_security_contract tests.ci_security.test_python_version_contract tests.ci_security.test_update_python_version tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract |
| Working directory | /var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater |
| Exit code | 1 |
| Observed at | 2026-07-21T07:41:04Z |
| Retention | retained |

Das externe Artefakt existiert und sein SHA-256 wurde verifiziert. Es ist
retained Evidence, keine nicht verfügbare Parent-.codex/runs-Kopie und kein
Coverage-Report.

## Ursache, Remediation, Akzeptanzkriterien und Validierungsplan

Dem Task-CPython-3.13.14-Build fehlt die SQLite-Development-Headers/pkg-config-
Discovery, die zum Bauen der Standardbibliotheks-_sqlite3-Erweiterung nötig
ist. Weil Coverage.py sqlite3 über coverage.sqldata importiert, scheitert der
Coverage-Command vor der Testausführung und kann kein Cobertura XML erzeugen.

In einer separat autorisierten Host-Environment-Aufgabe besteht die sichere
Remediation darin, die erforderlichen SQLite-Development-Headers/pkg-config-
Daten bereitzustellen, ein frisches externes task-eigenes CPython 3.13.14 zu
bauen, eine frische Framework-Virtual-Environment zu erstellen, nur die
hash-gesperrten Requirements zu installieren, import _sqlite3 zu verifizieren
und danach den exakten Command mit COVERAGE_FILE und COVERAGE_XML unter einem
frischen externen Task-Run erneut auszuführen.

Für die Akzeptanz müssen alle folgenden Punkte erfüllt sein:

1. Die frische erforderliche CPython-3.13.14-Umgebung importiert _sqlite3.
2. Die ausgewählte hash-gesperrte Framework-Umgebung importiert
   coverage==7.15.2 ohne den Fehler coverage.sqldata -> sqlite3 -> _sqlite3.
3. Der exakte Coverage.py-Command führt seine ausgewählten Tests aus und
   erzeugt eine nichtleere Cobertura-XML-Datei unter einem frischen task-
   eigenen externen Run-Pfad.
4. Es werden kein CPython-3.14-Substitut, keine handkopierte Erweiterung, keine
   System/User-Site-Installation und keine nicht autorisierte Host-Mutation
   verwendet.
5. FND-SONAR-0009 wird unabhängig durch seine Hosted-Projekt/Token-
   Configuration und Exact-Head-Scanner/Import-Evidence verifiziert.

## Dependencies, Blocker, Controls und Restrisiko

- Dependencies: separat autorisiertes Host-Setup mit SQLite-Development-
  Headers/pkg-config-Daten, ein frischer task-eigener CPython-3.13.14-Rebuild
  und eine Framework-Virtual-Environment sowie die Framework-hash-gesperrten
  Requirements.
- Blocked by: Dem ausgewählten Task-CPython 3.13.14 fehlt _sqlite3; diese
  Aufgabe verbietet Installation, Host-Rebuild und Substitute-Runtime-Arbeit;
  bis zum Rebuild der exakten Umgebung mit SQLite-Support existiert kein
  gültiger lokaler Cobertura-XML-Pfad.
- Legitimate Controls nach einem erlaubten Setup: Der exakte CPython-3.13.14-
  Interpreter importiert _sqlite3, Coverage.py startet die ausgewählten Tests
  und schreibt nichtleeres Cobertura XML, und FND-SONAR-0009 bleibt separat
  hosted-getestet.
- Related Findings: FND-SONAR-0009 und FND-FRAMEWORK-0044.

Lokales Cobertura XML bleibt unverifiziert. Dies ist non-security Host-Tooling,
keine Aussage über Hosted-GitHub-Actions- oder SonarQube-Cloud-Verhalten. Es
erfolgten kein unsicherer Workaround, keine Installation, kein Build, keine
Configuration-Änderung, keine Delivery-Aktion, kein Parent-Gitlink-Update und
keine MRTS-Änderung.

## Historie

| Zeit | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-21T07:54:45Z | local_coverage_sqlite_blocker_recorded_separately | Als separates P2-blocked_environment-host_environment-tooling-Finding aus dem zurückgehaltenen exakten CPython-3.13.14-Coverage.py-Importfehler angelegt. Es ist nicht der FND-SONAR-0009-Hosted-SONAR_TOKEN/Projektanalyse-Configuration-Blocker. |
| 2026-07-26T17:34:26Z | current_sqlite_prerequisite_revalidation | Das aufbewahrte exakte Lane-Receipt-SHA-256 wurde verifiziert, während das aktuelle `pkg-config` sqlite3 nicht findet und `/usr/include/sqlite3.h` fehlt. Es erfolgten keine Framework-Aktion, Installation, CPython-Rebuild, Substitute-Runtime, Produktänderung oder Delivery-Aktion; das Finding bleibt `blocked_environment`. Aktuelle Evidence: Run `20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`, SHA-256 `81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`. |
