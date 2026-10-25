# Change Record: CR-20261025-sonarqube-multilanguage

**Sprache:** [English](CR-20261025-sonarqube-multilanguage.md) | Deutsch

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
Zusätzlich wünscht der Benutzer unverbindliche Tests höherer C++-Standards.

## Akzeptanzkriterien

Python `3.14` aus Pin `3.14.7` verwenden, alle vorgesehenen Parent-Komponenten und
vier Go-Module erhalten, CFamily-Tests im Source-Scope belassen, Ausschlüsse und
Grenzen dokumentieren, echte unterstützte Reports erzeugen und die tatsächliche
PR-Revision prüfen. C++20-/C++23-Tests müssen sichtbar und nicht entscheidend sein;
C++17 bleibt maßgeblich. Submodulinhalte, Regeln und Quality Gates nicht ändern.

## Implementierungsentscheidung und Begründung

Ein manueller SonarScanner-CLI-Scan `8.1.0.6389` verwendet die unveränderliche
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

Eine getrennte nicht blockierende C++20-/C++23-Matrix kompiliert den echten
Evaluator mit `-Wall -Wextra -Werror` zu Objektdateien und verwendet den nativen
gepinnten ModSecurity-Source-Fetch für echte Header. `continue-on-error: true`
ist auf diese ausdrücklich gewünschten Advisory-Jobs beschränkt;
`fail-fast: false` erhält beide Ergebnisse. C++17 und Sonar-Gates bleiben
verbindlich. Es entstehen keine alternativen Sonar-Scans je Standard.

## Geänderte Dateien

- `sonar-project.properties`; `.github/workflows/sonarqube.yml`.
- `ci/checks/analysis/check-sonar-scope.py`; `tests/test_sonar_scope.py`.
- `ci/requirements/sonar-coverage.txt`; `ci/sonar-coverage.ini`.
- `.github/workflows/cpp-compatibility-advisory.yml`;
  `ci/checks/analysis/check-targeted-evaluator-cpp-advisory.sh`.
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
| `rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json` (Parent-Interpreterauswahl) | Bestanden: 1341 Sources, 239 Tests (216 Python / 23 Go), 136 CFamily-Units, vier Module. Manifest: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/scope-manifest-final.json`. |
| Gezielte kombinierte `unittest -v`-Auswahl für Scope, Python-Inventar, unveränderliche Pins, Rechte, YAML, Updater-Allowlist und Sonar-Secretkontrollen | 19 Testmethoden einschließlich aller parametrisierten Negativvarianten bestanden; lokal keine vollständige Standardsuite ausgewählt. |
| Tatsächlichen Python-Coverage-Workflow-Block aus YAML ausführen | Bestanden: isolierte binäre/hashverpflichtende Installation, echte CLI, acht Testmethoden, Kombination und XML. Checker 91.94% Lines, 88.33% Branches, 90.76% kombiniert. |
| Go-Coverage-Workflow-Block mit Guards aus YAML ausführen | Bestanden: vier vorhandene Einzelszenario-Tests; vier gültige native Profile. Statements ausgewählter Pakete 17.2%, 23.6%, 5.4%, 6.8%. |
| `rtk bypass actionlint .github/workflows/sonarqube.yml .github/workflows/cpp-compatibility-advisory.yml .github/workflows/update-workflow-tools.yml` | Bestanden. |
| `rtk bypass zizmor --offline .github/workflows/sonarqube.yml .github/workflows/cpp-compatibility-advisory.yml .github/workflows/update-workflow-tools.yml` | Bestanden; keine Findings, neun bestehende Unterdrückungen. |
| `rtk bypass make check-bilingual-docs check-doc-links PYTHON=<Parent interpreter>` | Einschließlich neuer gestagter Dokumente bestanden. |
| `rtk bypass git diff --check` | Bestanden. |
| Vollständigen Python-Version-Checker mit unveränderter Basis vergleichen | Exit 1 in beiden Bäumen, identische 19 Basisdiagnosen; kein neuer Workflow ergänzt eine Diagnose. |
| C++20-/C++23-Advisory-Checker mit GCC 15.2.0 und echten installierten ModSecurity-3.0.14-Headern über externen Include-Root-Alias | Beide echten Evaluator-Objektkompilierungen bestanden. Shell-Syntax/ShellCheck und Negativprüfungen für ungültigen Standard, Checkout-Ausgabe und fehlende Header bestanden. |

Derselbe echte Evaluator kompilierte außerdem in beiden Modi erfolgreich gegen
die gepinnten Upstream-Checkout-Header am Commit `1925753989ccce977cdaae417b55c9726c7cf02c`.

Das portable Label `.venv/bin/python` bezeichnet oben den vorhandenen Parent-
Interpreter und keine neue Umgebung im Task-Worktree. Gehostete Ergebnisse des
exakten aktuellen Heads stehen in PR #420 und werden nicht lokal abgeleitet.

## Security-Auswirkung

Der Scanner-Job hat nur `contents: read`; Workflow-Standards verweigern Rechte.
Checkout-Credentials werden nicht gespeichert. Nur der feste Scanner-Schritt
erhält `SONAR_TOKEN`; Fork-PRs führen diesen Job nicht aus. Signaturprüfung,
Regeln und Quality Gates bleiben aktiv. Coverage-Tooling ist isoliert und
hashgepinnt. Advisory-C++-Jobs besitzen lesende Rechte und keine Secrets.
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
Coverage und Testausführungsreports fehlen. Advisory-Objekte beweisen weder
Linken noch Laufzeitverhalten. Lokales Python `3.14.4`/Go `1.27.3` weichen von
CI-Pins ab.

## Verbleibende Risiken

Ein Projektadministrator muss das gespeicherte `py Intended Model` mit dem
Parent-only-Source-/Test-Scope abgleichen; kein Modell oder Architekturcheck
wurde zum Verbergen von Warnungen entfernt. Shell-Parsing und CFamily-Treue
bleiben Analyzer-Grenzen. Automatic Analysis muss deaktiviert bleiben.
Der finale Folge-Head benötigt noch gehosteten Scan-/Import-/Gate- und
Advisory-Ergebnis-Readback.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger nativer Host-Build, Linken oder Runtime-Qualifikation waren für
diesen Konfigurationstask nicht erforderlich. Keine sachfremde Basis-Python-
Workflow-Migration oder historische I12-Kampagne ausgeführt. Die ersten
gehosteten Pin-/Scope-/Go-Schritte bestanden; gehostete Python-Coverage und
höhere Standards müssen am tatsächlichen neuen PR-Head bewertet werden.
Bestehende Gates wurden nicht für ein Bestehen abgeschwächt.

## Finaler Diff- und Review-Status

Implementierung, gezielte lokale Tests und bilinguale Dokumentation sind geprüft.
Ein unabhängiges Review validierte Coverage-Zuordnung und Secret-Grenzen;
sein Hinweis auf alternativen Secret-Zugriff wurde behoben und negativ geprüft.
Der erste Commit `b3c7785fd7033fc57394c1e4562d627e2b294c4f` ist in Draft-PR #420
veröffentlicht; Folgeänderungen erhalten die normale Historie. Kein Merge oder
Master-Change erfolgte. Der finale Lieferstatus stammt aus PR-Evidence des
exakten Heads und nicht aus diesem Record vor dem Push.
