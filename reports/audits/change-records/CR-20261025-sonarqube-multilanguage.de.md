# Change Record: CR-20261025-sonarqube-multilanguage

**Sprache:** [English](CR-20261025-sonarqube-multilanguage.md) | Deutsch

Dieser Record trennt implementierte Konfiguration, beobachtete lokale Prüfungen
und Cloud-Bestätigung. Er beansprucht weder einen verifizierten PR noch einen
erfolgreichen Cloud-Scan.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261025-sonarqube-multilanguage |
| Datum (UTC) | 2026-10-25 |
| Basis-Revision | `9913026c1feec85a1862d22987689a1ebcef6d97` |

## Motivation und Problemstellung

Die vorherige automatische Parent-Analyse meldete sowohl eine fehlende
Python-Zielversion als auch erkannte Tests ohne `sonar.tests`. Der Parent enthält
verteilte Python- und Go-Tests neben C/C++-Tests, gepflegten Buildskripten und
Konfiguration. Ein sprachunabhängiges Testmuster oder eine unvollständige
Compilation Database würde Teile der vorgesehenen Analyse still entfernen.
Diese Änderung stellt eine wartbare Parent-weite CI-Analyse bereit, ohne
Framework- oder MRTS-Zuständigkeitsgrenzen zu überschreiten.

## Akzeptanzkriterien

- Ein Projekt, expliziten Source-/Test-Scope und Python-Haupt-/Nebenversion `3.14`
  verwenden, abgeleitet aus dem eingecheckten Pin `3.14.7`.
- Alle Parent-Komponenten, vier Go-Modulbeschreibungen und CFamily-Test-
  Translation-Units erhalten; genaue Ausschlüsse und nicht unterstützte Formate
  dokumentieren.
- Gepinnte Scanner-Schnittstellen, minimale CI-Berechtigungen und tatsächlich
  für die analysierte Revision erzeugte Coverage-Berichte verwenden.
- Scope-Drift-Prüfungen, gleichwertige EN/DE-Anleitungen und wahrheitsgemäße
  lokale Prüfergebnisse bereitstellen.
- Vor einer Cloud-Verifizierungsbehauptung den Server-Task, die Warnungen und
  das Quality Gate des exakten PR-Heads beobachten. Dieses letzte Kriterium
  ist durch die hier aufgezeichnete lokale Evidence noch nicht nachgewiesen.

## Implementierungsentscheidung und Begründung

Ein CI-basierter Gesamtscan mit SonarScanner CLI `8.1.0.6389` verwendet
`sonar-project.properties` und die unveränderlich gepinnte Scan-Action `v8.3.0`
mit `d209202bc7d53ff1cc128f7f907dac145c9d6ae9`. Der Organization-Key
`easton97-jens` wurde über die authentifizierte Projekt-API bestätigt. Cloud
Automatic Analysis war bei der Prüfung bereits deaktiviert; keine externe
Einstellung wurde geändert. `sonar.scanner.autoconfig.enabled=false` erhält die
explizite manuelle Klassifikation. CFamily AutoConfig ist von dieser Einstellung
unabhängig und erhält alle Quell-Translation-Units; vorhandene Compilation-
Database-Erzeuger decken nur Teilmengen ab. Der C++17-Reporting-Override steuert
anwendbare Regeln, keine Compilerflags oder den Nachweis eines nativen Builds.

Python-Dateien unter `tests/`, verteilte Connector-Python-Tests und Go-Dateien
`*_test.go` sind Tests. C/C++-Tests und Fixtures bleiben Quellen, weil CFamily
`sonar.tests` nicht unterstützt. Gepflegte Connector-`build/`-Skripte bleiben
enthalten. Ausschlüsse betreffen die unabhängige `modules/**`-Grenze,
SCM-ignorierte Root-Ausgaben, generierte Evidence unter
`reports/testing/generated/**` und ausschließlich YAML-Dateien in den drei
Workflow-Fixture-Verzeichnissen. Ihre gepflegten Generatoren und Python-/C-
Fixtures bleiben enthalten. Generische JSON-/YAML-Analyse verwendet den
dokumentierten Opt-in; ihre tatsächliche Ausführung benötigt Scanner-Evidence.

CI erzeugt vier fokussierte native Go-Coverage-Profile innerhalb des jeweiligen
Moduls, prüft jedes mit `go tool cover` und übergibt deren tatsächliche externe
Pfade an den Scanner. Es werden weder Ersatzreports noch eine Python-Coverage-
Abhängigkeit oder native C/C++-Coverage-Pipeline hinzugefügt. Guards für exakte
Testnamen verhindern einen fälschlichen Null-Test-Erfolg bei umbenanntem Selektor.

## Geänderte Dateien

- `sonar-project.properties`; `.github/workflows/sonarqube.yml`.
- `ci/checks/analysis/check-sonar-scope.py`; `tests/test_sonar_scope.py`.
- `ci/checks/common/check-python-version-contract.py`;
  `tests/test_python_version_contract.py` (37 normale Python-Jobs).
- `ci/tooling/security-tools.lock.yml`; `ci/tools/update-workflow-tools.py`;
  `.github/workflows/update-workflow-tools.yml` (zentraler Action-Lock,
  Updater-Allowlist und explizites Publisher-Staging).
- `docs/sonarqube-analysis.md`; `docs/sonarqube-analysis.de.md`.
- `docs/README.md`; `docs/README.de.md`.
- `docs/security/ci-security-tooling.md`;
  `docs/security/ci-security-tooling.de.md`.
- Dieser Change Record und sein englischer Begleiter.

Es werden keine Submodul-Inhalte oder Gitlinks geändert.

## Ausgeführte Befehle

Alle lokalen Projektbefehle verwenden RTK. `.venv/bin/python` bezeichnet unten
portabel den tatsächlich über seinen absoluten Pfad ausgewählten vorhandenen
Parent-Interpreter. Folgende Ergebnisse wurden beobachtet; sie sind keine
Ableitungen aus der Konfiguration:

| Befehl oder abgegrenztes Verfahren | Beobachtetes Ergebnis |
| --- | --- |
| `rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json` | Auf dem gestagten Inventar bestanden: 1337 Quelldateien, 239 Tests (216 Python, 23 Go), 136 CFamily-Translation-Units, vier Go-Module. Vollständiges Scope-Manifest: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/scope-manifest.json`. |
| `rtk bypass .venv/bin/python -m unittest -v tests.test_sonar_scope` | Vier Scope-Regressionstests bestanden. |
| `rtk bypass .venv/bin/python -m unittest -v tests.test_sonar_scope tests.test_python_version_contract.PythonVersionContractTest.test_expected_inventory_has_37_normal_jobs_and_one_special_job tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_all_remote_actions_are_immutable_sha_pins tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_all_workflows_default_deny_and_declare_job_permissions tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_workflow_and_lock_yaml_reject_forbidden_indirection tests.ci_security.test_update_workflow_tools.WorkflowToolUpdaterTests.test_all_locked_action_references_are_in_the_publisher_allowlist` | Neun fokussierte Tests bestanden mit der vorhandenen Parent-Umgebung, Python `3.14.4`. Das belegt keine Ausführung mit dem exakten CI-Pin `3.14.7`. |
| `rtk bypass actionlint .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Bestanden, Exit 0. |
| `rtk bypass zizmor --offline .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Bestanden, Exit 0; keine Findings, acht durch bestehende Konfiguration unterdrückte Diagnosen. |
| Aus Workflow-YAML extrahierten Go-Coverage-Shellblock mit lokalem Go `1.27.3` ausführen | Vier vorhandene Einzelfalltests bestanden; alle vier Profile ließen sich parsen. Die Statement-Coverage der Pakete betrug 17.2%, 23.6%, 5.4% beziehungsweise 6.8%. Das sind begrenzte Messungen ausgewählter Pakete, keine Repository-Gesamtabdeckung. Der vollständige Workflow-Block wurde anschließend mit den `-list`-Guards und dem Parsen der Profile je Modul erneut ausgeführt; Exit 0. |
| Vollständiger Python-Version-Contract-Checker, Task gegen saubere Basis | Beide endeten mit Exit 1 und denselben 19 Diagnosen, bytegleich. Es kam keine zusätzliche Sonar-Job-Diagnose hinzu. Evidence: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/python-contract-task.txt` und `python-contract-baseline.txt`. |
| `rtk bypass git diff --check` | Auf dem integrierten Task-Stand bestanden, Exit 0. |
| `rtk bypass make check-doc-links PYTHON=<Parent interpreter>` | Bestanden, Exit 0, einschließlich der Prüfung neuer Dokumente nach dem Staging. |
| `rtk bypass make check-bilingual-docs PYTHON=<Parent interpreter>` | Bestanden, Exit 0 nach Korrektur des Sprachumschalters im deutschen Guide. |

Die authentifizierte Sonar-Bestandsaufnahme verwendete
`/usr/local/bin/sonar-with-env` über RTK; Query-CLI `1.10.1` verband sich
erfolgreich. Projektidentität und deaktivierte Automatic Analysis wurden
zurückgelesen. Die GitHub-Abfrage der Secret-Namen bestätigte die Existenz von
`SONAR_TOKEN`, ohne seinen Wert zu lesen oder seine Scanner-Berechtigung zu
belegen.

## Security-Auswirkung

Der Scan-Job besitzt nur `contents: read`; Workflow-Standardberechtigungen sind
leer. Checkout speichert keine Credentials und initialisiert keine Submodule.
Das vorhandene Secret `SONAR_TOKEN` wird nur dem unveränderlich gepinnten
Scanner-Schritt übergeben. Fork-PRs können den privilegierten Job nicht ausführen;
es entsteht kein `pull_request_target`-Pfad. Die Scanner-Signaturprüfung bleibt
aktiv. Regeln, Quality Gates, Secret-Werte, Anwendungsautorisierung und
Runtime-Defaults bleiben unverändert. Workflow- und Tooling-Änderungen erweitern
die vorhandenen zentralen Lock- und Publisher-Grenzen, statt sie zu umgehen.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Lokale
Konfigurationsprüfungen, fokussierte Unit-Tests, Coverage-Erzeugung und statische
Workflow-Analyse qualifizieren kein gehostetes Connector-Verhalten.

## Bekannte Einschränkungen

CFamily AutoConfig leitet Host-Optionen ab; es reproduziert nicht jeden
unabhängigen Connector-Build, generierten Header, Define oder optionalen
Profilzweig. Header benötigen eine einbindende Translation Unit. Regeln über
Translation-Units und das Gesamtprojekt können an Präzision verlieren, wenn
unabhängige Executables ein Projekt teilen. Für das Shell-Template
`connectors/apache/build/apxs-wrapper.in` ist keine Erkennung durch den
Shell-Analyzer bestätigt. Andere Host-Konfigurations- und Buildformate besitzen
nicht durchgehend dedizierte semantische Analyzer.

Python- und C/C++-Coverage sowie Testausführungsbericht-Importe werden nicht
bereitgestellt. Die vier Go-Profile decken nur ausgewählte vorhandene Tests ab.
Lokales Python `3.14.4` und Go `1.27.3` unterscheiden sich von den CI-Pins
`3.14.7` und `1.27.1`; Ausführung mit den exakten Pins benötigt Hosted-CI.
Vorhandene Python-Contract-Inkonsistenzen der Basis bleiben bestehen.

## Verbleibende Risiken

Dem vorhandenen `SONAR_TOKEN` kann weiterhin eine gültige Analyseberechtigung
fehlen. Externe Automatic Analysis muss deaktiviert bleiben, um konkurrierende
Scan-Modi zu vermeiden. Neue Analyzer-/Konfigurationswarnungen, bestehende
Code-Findings oder ein fehlgeschlagenes Quality Gate können im echten Scan
auftreten; nichts davon wird durch diese Änderung unterdrückt oder akzeptiert.
Ein bestandener Scope-Check beweist weder die Verarbeitung jeder enthaltenen
Datei durch jeden Analyzer noch das Verschwinden der beiden ursprünglichen
Cloud-Warnungen.

## Nicht ausgeführte Prüfungen mit Begründung

Die Bilingual-Prüfung und die Linkprüfung nach dem Staging bestanden. Ein unabhängiges statisches Review fand keine umsetzbaren Korrektheits- oder Sicherheitsprobleme in Konfiguration, Workflow, Scope-Checker oder Updater-Integration. Die gestagte Scope-Erfassung und der
Go-Coverage-Block mit Guards haben bestanden. Ein
echter gehosteter Scan, serverseitiger Abschluss am exakten Head,
Warnungs-Readback und Quality Gate liegen vor PR-Lieferung noch nicht vor. Ein
lokaler Scanner wurde nicht gestartet: Das vorgeschriebene
`/usr/local/bin/sonar-with-env` startet die Query-CLI, keinen beliebigen Scanner.
Für diese Konfigurationsänderung war weder ein hostnativer Build noch
Runtime-Qualifikation erforderlich. Es wurden keine leeren Reports oder
ersatzweisen Erfolgsergebnisse erzeugt.

## Finaler Diff- und Review-Status

Konfiguration und CI-Integration sind implementiert. Scope-Erfassung, die neun
gezielten Tests, Go-Coverage mit Guards, Workflow-Lint, bilinguale Dokumentation,
Links und Diff-Prüfungen bestanden. Das unabhängige statische Review fand keine
umsetzbaren Korrektheits-/Sicherheitsprobleme. Der vollständige Python-Workflow-
Checker meldet weiterhin exakt dieselben 19 Basisdiagnosen. Sachfremde Änderungen,
Secrets, Submodulinhalte oder Gitlinks sind nicht enthalten. Commit, PR-Nummer,
Merge, Cloud-Analyse-ID oder Gate-Erfolg werden hier nicht erfunden. Die
PR-Beschreibung und Task-Evidence müssen gehostete Ergebnisse des exakten Heads
festhalten, bevor `verified_pr` beansprucht wird.
