# Change Record: CR-20261025-sonarqube-multilanguage

**Sprache:** [English](CR-20261025-sonarqube-multilanguage.md) | Deutsch

> **Historische Momentaufnahme von master #420**
> Dieser Bericht erhält die ursprünglichen #420-Revisionen und Ergebnisse. Die PR-382-Integration verwendet Python3.15.1/Go1.27.3, das gemeinsame Aktivinventar und tatsächliche generische Python-/Native- sowie native Go-Reports; siehe [aktuelle Integration](../../../docs/pr-382-merge-readiness.de.md#integration-von-master-420). Die folgenden getrennten coverage.py-/Go-Auswahlen sind historisch und kein zusätzlicher automatischer Katalog.

## Identität

| Field | Value |
| --- | --- |
| Change-ID | CR-20261025-sonarqube-multilanguage |
| Datum (UTC) | 2026-10-25 |
| Basis-Revision | `9913026c1feec85a1862d22987689a1ebcef6d97` |

## Motivation und Problemstellung

Die automatische Parent-Analyse meldete keine explizite Python-Zielversion und
erkannte Tests ohne `sonar.tests`. Verteilte Tests, unabhängige native Binaries
und gepflegte Build-/CI-Skripte benötigen einen konsistenten Parent-Scan.
Der Benutzer fordert unverbindliche repositoryweite Sonar-Analysen für C++20 und C++23 statt komponentenbegrenzter Compiler-Checks.

## Akzeptanzkriterien

Python `3.14` aus Pin `3.14.7` verwenden, alle vorgesehenen Parent-Komponenten und
vier Go-Module erhalten, CFamily-Tests im Source-Scope belassen, Ausschlüsse und
Grenzen dokumentieren, echte unterstützte Reports erzeugen und die tatsächliche
PR-Revision prüfen. Repositoryweite C++20-/C++23-Sonar-Scans müssen sichtbar und nicht entscheidend sein;
C++17 bleibt maßgeblich. Submodulinhalte, Regeln und Quality Gates nicht ändern.

## Implementierungsentscheidung und Begründung

Drei repositoryweite manuelle SonarScanner-CLI-Varianten `8.1.0.6389` verwenden die unveränderliche
Action `v8.3.0` (`d209202bc7d53ff1cc128f7f907dac145c9d6ae9`). Organisation
`easton97-jens` und bereits deaktivierte Cloud Automatic Analysis wurden über
den kanonischen Wrapper verifiziert. Explizite Scanner-Autokonfiguration ist
deaktiviert. CFamily AutoConfig erhält alle 136 Translation Units, weil die
vorhandenen echten Compilation-Database-Erzeuger Teilbereiche abdecken.
C++17-Berichtsregeln bleiben maßgeblich.

Enge Python-/Go-Testmuster erhalten CFamily-Tests und gepflegte Connector-
`build/`-Skripte. Ausschlüsse betreffen eigenständiges `modules/**`, Root-Ausgaben,
`reports/testing/generated/**` und exakte YAML-Workflow-Fixture-Muster.
JSON/YAML verwenden das dokumentierte Opt-in. Der Checker lehnt Versions-/
Scope-Abweichungen ab.

Vier vorhandene Go-Szenarien erzeugen native Profile in ihren Modulen.
Coverage `7.17.0` verwendet ein offizielles hashgepinntes Universal-Wheel,
Apache-2.0, Python >=3.11 und keine Abhängigkeiten. Eine getrennte externe
virtuelle Umgebung führt die echte Checker-CLI und acht gezielte Unit-Testmethoden
aus, kombiniert Branch-Daten und erzeugt Cobertura-XML mit relativen Pfaden.
Zwei nicht ausgeführte Analyseskripte bleiben bei echter Null; keine Coverage-
Ausschlüsse oder Ersatzreports werden verwendet.

Der PR-Sicherheitsvertrag erlaubt ausschließlich den exakten Same-Repository-
Ausdruck und das schrittlokale Token an der unveränderlichen Scanner-Action.
Generische PR-Secretverbote bleiben erhalten; Negativkontrollen lehnen Guard-
Umgehung, globale/Shell-Secrets, andere Actions und Klammer-/direkten Zugriff
auf den Secret-Kontext ab. Die drei Maintainability-Findings des ersten Scans
wurden durch Aufteilen der Validierungsverantwortung, Entfernen einer redundanten
Exception-Klasse und Trennen von Test-Assertions bearbeitet.

Dieselbe vollständige Source-/Testkonfiguration und dieselben Python-/Go-
Coverage-Erzeuger laufen in drei Varianten. C++17 verwendet das verbindliche
kanonische Projekt. C++20/C++23 verwenden `sonar.cfamily.reportingCppStandardOverride`
mit getrennten öffentlichen Projekten
`Easton97-Jens_ModSecurity-conector_cpp20_advisory` und
`Easton97-Jens_ModSecurity-conector_cpp23_advisory`. Beide Projekte wurden über
den kanonischen Wrapper manuell angelegt und als ungebunden, Automatic Analysis
false, Hauptbranch `master` zurückgelesen. Ihre relevanten Profile-Keys und das
`Sonar way` Gate stimmen mit dem kanonischen Projekt überein. Ein redundanter
Setting-Schreibversuch wurde von der API abgelehnt; Readback belegte den bereits
korrekten deaktivierten Zustand.

Der explizite Advisory-Hauptbranchparameter vermeidet kanonische PR-Zuordnung.
`continue-on-error` stammt ausschließlich aus der festen Advisory-Matrix;
C++17 bleibt verbindlich und jeder Scanner wartet auf sein tatsächliches Gate.
Serialisierung je Projekt und Task-/SHA-Zusammenfassungen erhalten die
Nachvollziehbarkeit. Partieller Source-Scope, alternative Properties-Datei,
komponentenbezogene Compilation Database oder reine Compiler-Advisory-Jobs
verbleiben nicht. Matrixvertrag und negative Gating-Kontrolle sind getestet.

## Geänderte Dateien

- `sonar-project.properties`; `.github/workflows/sonarqube.yml`.
- `ci/checks/analysis/check-sonar-scope.py`; `tests/test_sonar_scope.py`.
- `ci/requirements/sonar-coverage.txt`; `ci/sonar-coverage.ini`.
- `tests/test_ci_security_workflows.py`;
  `ci/checks/common/check-python-version-contract.py`; `tests/test_python_version_contract.py`.
- `ci/tooling/security-tools.lock.yml`; `ci/tools/update-workflow-tools.py`;
  `.github/workflows/update-workflow-tools.yml`.
- `docs/sonarqube-analysis.md`; `docs/sonarqube-analysis.de.md`;
  `docs/README.md`; `docs/README.de.md`;
  `docs/security/ci-security-tooling.md`; `docs/security/ci-security-tooling.de.md`.
- `reports/audits/change-records/CR-20261025-sonarqube-multilanguage.md`;
  `reports/audits/change-records/CR-20261025-sonarqube-multilanguage.de.md`.

Keine Framework-/MRTS-Inhalte oder Gitlinks geändert.

## Ausgeführte Befehle

Alle Shell-Prozeduren verwendeten RTK und den über absoluten Pfad ausgewählten
vorhandenen Parent-Interpreter (Python `3.14.4`) beziehungsweise Task-eigene
externe Coverage-Umgebungen.

| Tatsächlicher Befehl oder begrenzte Prozedur | Beobachtetes Ergebnis |
| --- | --- |
| `rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json` (Parent-Interpreterauswahl) | Bestanden: 1339 Sources, 239 Tests (216 Python / 23 Go), 136 CFamily-Units, vier Module. Manifest: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/scope-manifest-final.json`. |
| Gezielte kombinierte `unittest -v`-Auswahl für Scope, Python-Inventar, unveränderliche Pins, Rechte, YAML, Updater-Allowlist und Sonar-Secretkontrollen | 21 Testmethoden einschließlich aller parametrisierten Negativvarianten bestanden; lokal keine vollständige Standardsuite ausgewählt. |
| Tatsächlichen Python-Coverage-Workflow-Block aus YAML ausführen | Bestanden: isolierte binäre/hashverpflichtende Installation, echte CLI, acht Testmethoden, Kombination und XML. Checker 91.94% Lines, 88.33% Branches, 90.76% kombiniert. |
| Go-Coverage-Workflow-Block mit Guards aus YAML ausführen | Bestanden: vier vorhandene Einzelszenario-Tests; vier gültige native Profile. Statements ausgewählter Pakete 17.2%, 23.6%, 5.4%, 6.8%. |
| `rtk bypass actionlint .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Bestanden. |
| `rtk bypass zizmor --offline .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Bestanden; keine Findings, sieben bestehende Unterdrückungen. |
| `rtk bypass make check-bilingual-docs check-doc-links PYTHON=<Parent interpreter>` | Einschließlich neuer gestagter Dokumente bestanden. |
| `rtk bypass git diff --check` | Bestanden. |
| Vollständigen Python-Version-Checker mit unveränderter Basis vergleichen | Exit 1 in beiden Bäumen, identische 19 Basisdiagnosen; kein neuer Workflow ergänzt eine Diagnose. |


Das portable Label `.venv/bin/python` bezeichnet oben den vorhandenen Parent-
Interpreter und keine neue Umgebung im Task-Worktree. Gehostete Ergebnisse des
exakten aktuellen Heads stehen in PR #420 und werden nicht lokal abgeleitet.

## Security-Auswirkung

Der Scanner-Job hat nur `contents: read`; Workflow-Standards verweigern Rechte.
Checkout-Credentials werden nicht gespeichert. Nur der feste Scanner-Schritt
erhält `SONAR_TOKEN`; Fork-PRs führen diesen Job nicht aus. Signaturprüfung,
Regeln und Quality Gates bleiben aktiv. Coverage-Tooling ist isoliert und
hashgepinnt. Alle Varianten besitzen lesende GitHub-Rechte. Nur ihr gepinnter Scanner-Schritt erhält das bestehende Analysetoken; Fork-PRs sind ausgeschlossen.
Produktionslaufzeit, Autorisierung und Logging-Verhalten ändern sich nicht.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Objektkompilierung,
Tests, Coverage und statische Scans qualifizieren kein gehostetes Connector-Verhalten.

## Bekannte Einschränkungen

Der erste Scan der Revision `b3c7785fd7033fc57394c1e4562d627e2b294c4f`, Run
`40218724634`, schloss Servertask `AaF0Nx8EdkEpBguA0kbW` erfolgreich als Analyse
`8436e500-b997-4b7a-b428-b577aca20a43` ab. Wirksames Python `3.14`, explizite Tests
und CLI `8.1.0.6389` wurden gegen diesen SHA zurückgelesen. Beide ursprünglichen
Python-Warnungen verschwanden; die CE-Warnungsliste war leer. Sein Gate scheiterte
nur an New-Code-Coverage `0.0 < 80`, worauf echte Python-Coverage integriert wurde.
Dies ist historische Erst-Head-Evidence und keine Bestätigung des finalen Gates.

Der Scanner analysierte alle 136 CFamily-Units vollständig mit Qualitätsscore
77.52/100, lud vier Go-Reports und führte Python-, Go-, Shell-, Actions-, YAML-
und JSON-Sensoren aus. AutoConfig reproduziert nicht alle Host-Builds und
deaktiviert C/C++-Taint-Analyse. Header-/Binary-Grenzen bleiben. Sechs bestehende
Shell-Parsewarnungen, ignorierte Go-Testduplikationsmeldungen und 44 ungültige
Labels der gespeicherten Python-Architekturperspektive sind im Guide dokumentiert.
`warningCount=0` bedeutet keine Warnungsfreiheit der Scanner-Logs.

Coverage ist gezielt und keine vollständige Repository-Testausführung. C/C++-
Coverage und Testausführungsreports fehlen. Statische Standardvarianten beweisen weder native Kompilierung noch Linken oder Laufzeitverhalten. Lokales Python `3.14.4`/Go `1.27.3` weichen von
CI-Pins ab.

## Verbleibende Risiken

Ein Projektadministrator muss das gespeicherte `py Intended Model` mit dem
Parent-only-Source-/Test-Scope abgleichen; kein Modell oder Architekturcheck
wurde zum Verbergen von Warnungen entfernt. Shell-Parsing und CFamily-Treue
bleiben Analyzer-Grenzen. Automatic Analysis muss deaktiviert bleiben.
Revision `ed2c9c7cb6739f802aba3d842f46e18e9f3d414c` schloss den kanonischen Task
`AaF0TdarwSmsgR9Bxtvb`, Analyse `f474f764-2b07-48dc-9f5e-248f5f891140`, mit
Gate OK und 90.8% New-Code-Coverage ab; ihre Current-Head-CI bestand. Die finale
Drei-Standard-Matrix benötigt noch frischen gehosteten Projekt-/SHA-/Gate-Readback.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger nativer Host-Build, Linken oder Runtime-Qualifikation waren für
diesen Konfigurationstask nicht erforderlich. Keine sachfremde Basis-Python-
Workflow-Migration oder historische I12-Kampagne ausgeführt. Die ersten
gehosteten Pin-/Scope-/Go-Schritte bestanden; die finalen repositoryweiten Standardvarianten müssen am tatsächlichen neuen PR-Head bewertet werden.
Bestehende Gates wurden nicht für ein Bestehen abgeschwächt.

## Finaler Diff- und Review-Status

Implementierung, gezielte lokale Tests und bilinguale Dokumentation sind geprüft.
Ein unabhängiges Review validierte Coverage-Zuordnung und Secret-Grenzen;
sein Hinweis auf alternativen Secret-Zugriff wurde behoben und negativ geprüft.
Der erste Commit `b3c7785fd7033fc57394c1e4562d627e2b294c4f` ist in Draft-PR #420
veröffentlicht; Folgeänderungen erhalten die normale Historie. Kein Merge oder
Master-Change erfolgte. Der finale Lieferstatus stammt aus PR-Evidence des
exakten Heads und nicht aus diesem Record vor dem Push.
