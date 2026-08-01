# FND-SONAR-0003 — Exakter Framework-PR-Head hat ein kritisches SonarQube-Cloud-S5443-Security-Signal in einer CRS-Regressions-Assertion

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-SONAR-0003` |
| Kategorie | `sonarqube_finding` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P1` / `not_applicable` |
| Confidence / Status | `validated` / `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `true` |
| Security-relevant | `true` |

## Zusammenfassung und beobachtetes Verhalten

SonarQube Cloud markierte zunächst den Draft-PR-#27-Head `15e9a034…` mit Critical `python:S5443` und Security Impact High und verursachte damit New-Code-Security-Rating D. Der Exact-Head-Check-Run `88088009441` schlug mit einer Vulnerability-Annotation auf `tests/ci_security/test_ci_security_contract.py:287` fehl: `self.assertNotIn("/tmp/crs-version-pinning", script)`. Follow-up-Framework-Commit `66d90872cfc0125536267d574b776d2e88d26b23` besteht jetzt den Exact-Head-SonarQube-Cloud-Check `88089324795` mit Security Rating A und null offenen Pull-Request-Vulnerabilities.

Die Source-to-Sink-Validierung beweist, dass die Zeile ein negativer `unittest`-Vergleich über bereits gelesenen eingecheckten Skripttext ist: Sie erstellt/öffnet keine Datei und startet keinen Prozess. Das Scanner-Signal ist test-only und keine Produktvulnerabilität. Die Ersetzung prüft die tatsächlich ausgemusterte vorhersagbare Form `crs-version-pinning.$$` und erhält die positiven Safe-Root- und Private-`mktemp`-Controls.

## Erwartetes Verhalten, Impact und Scope

Der Regressionstest muss beweisen, dass das Produktionsskript den ausgemusterten vorhersagbaren Pfad nicht verwendet, während kein Testausdruck als unsichere Public-Directory-Dateioperation fehlklassifiziert werden darf. Das exakte Remote-PR-Head-SonarQube-Quality-Gate muss ohne Unterdrückung, Exclusion, Deaktivierung oder Abschwächung eines Controls bestehen.

Die Scanner-Klassifikation ließ ein erforderliches externes Gate vorübergehend fehlschlagen. Sie ist jetzt auf dem exakten PR-Head ohne Suppression, Exclusion, deaktivierten Scanner, abgeschwächten Test oder abgeschwächtes Quality Gate repariert. Dies ist Framework-only-Scope; es autorisiert weder eine Parent-Produkt- oder Gitlink-Änderung noch eine MRTS-Aktion. `FND-SONAR-0002` bleibt ein separater historischer Default-Branch-SonarQube-Backlog.

## Evidence, Grundursache und Remediation

Aufbewahrte Evidence umfasst `sonar-pr27-final-head-failure.md`, SHA-256 `52187029ea9ce58070f5150655dc77766c301552c601c365b5234e4212379a95`, und die finale Remote-Disposition `framework-pr27-final-remote-status.md`, SHA-256 `ccedabbe5e020bf43eb91ccf93b1e1484b8d11471e2817b6d078a95eeddb3552`. Die erste Source-to-Sink-Analyse bestätigt an der markierten Zeile keinen Writable-Directory-File-Creation-, File-Open- oder Subprocess-Sink.

Die implementierte Korrektur erhält die Regression über den exakten früheren vorhersagbaren Suffix, bewahrt alle Safe-Private-`mktemp`-Controls und besteht fokussierte CI-Security-Tests, `make lint`, CodeQL, actionlint, zizmor, OSV, Scorecard, Gitleaks und Exact-Head-SonarQube-Cloud. Das finale Sonar-Ergebnis enthält 17 nicht-sicherheitsrelevante New-Issues, besteht aber Quality-Gate-, Security-, Reliability- und Maintainability-Ratings; es wurde kein unnötiger Semantic-Checker-Refactor gebündelt.

## Akzeptanzkriterien und Validierung

- Source-to-Sink-Validierung stellt das Signal als test-only fest.
- Der Test lehnt weiterhin das exakte ausgemusterte Muster `crs-version-pinning.$$` ab und verlangt weiterhin Safe-Runtime-Path- und private-`mktemp`-Controls.
- Fokussierte Regression- und Legitimate-Control-Tests bestehen ohne eine Abschwächung von Controls.
- Der exakte finale Draft-PR-#27-Head hat ein bestandenes SonarQube-Cloud-Quality Gate, Security Rating A und null offene Pull-Request-Vulnerabilities.

Der Record bleibt `fixed`, nicht geschlossen, bis eine merged-current-master-Verifikation vorliegt. Separate Exact-Head-Required-CI-Blocker `FND-FRAMEWORK-0001` und `FND-GITHUB-0002` verhindern `verified_pr`, werden aber nicht durch diese Remediation verursacht.

## Restrisiko und Historie

Das task-eigene Scanner-Signal reproduziert sich nicht mehr auf dem exakten PR-Head. Der externe PR bleibt `partial`, weil common-structure und Dependency Review unabhängig fehlschlagen; dieser Record wird vor einer merged-current-master-Verifikation nicht geschlossen. `2026-07-18T14:12:00Z`: Signal triagiert. `2026-07-18T14:26:12Z`: Source-to-Sink-Validierung und Exact-Head-Remote-Gate reparierten das Test-only-Signal.
