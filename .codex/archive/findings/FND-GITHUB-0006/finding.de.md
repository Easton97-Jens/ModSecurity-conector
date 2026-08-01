# FND-GITHUB-0006 — Framework-master-Advanced-CodeQL-Uploads scheitern bei aktiviertem GitHub Default Setup

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-GITHUB-0006` |
| Kategorie | `ci_failure` |
| Repository / Ownership | `framework` / `github_configuration` |
| Priorität / Severity | `P1` / `not_applicable` |
| Confidence / Status | `confirmed` / `accepted_risk` |
| Feasibility | `out_of_scope` |
| Release-Blocker | `true` |
| Security-relevant | `true` |

## Zusammenfassung, Beobachtung und Auswirkung

Auf dem exakten Framework-master `6de40c1714410241e917e9083ee890a82fb2fdbb` schlug der vertrauenswürdige Advanced-CodeQL-Workflow aus PR #27 für Actions, C/C++ und Python fehl. Jede Sprache analysierte den Source, anschließend lehnte GitHub die SARIF-Verarbeitung ab, weil Default Setup aktiviert bleibt. Die drei Default-Setup-Analysen für denselben SHA bestanden und die Code-Scanning-API meldet null offene Alerts.

Dies ist ein externer GitHub-Konfigurations-/Control-Konflikt, keine nachgewiesene Framework-Code-Schwachstelle. Er verhindert die Behauptung, dass der geprüfte vertrauenswürdige Advanced-Uploader erfolgreich war, und blockiert ein vollständig verifiziertes Master-Integrationsergebnis, obwohl Default Setup alternative Abdeckung liefert.

Nach der Erfassung der Merge-Evidence dieses Tasks führten externe Commits den
Framework-`master` auf `8572da580e11bc3c62f6ef559152f49b30650056` weiter. Ein
nur lesender GitHub-Readback meldete danach Default Setup `not-configured` und
erfolgreiche Advanced-CodeQL-Jobs für Actions, C/C++ und Python. Dieser Task
hat weder den Settings-Wechsel noch die späteren Commits vorgenommen. Der
spätere Zustand macht den fehlgeschlagenen Upload auf dem exakten `6de40c...`
nicht rückwirkend zu einem Pass und belegt nicht, dass die aktuelle
Konfiguration die ausdrücklich vom Nutzer autorisierte Konfiguration ist.

## Scope, Reproduktion und Evidence

- Betroffener Workflow: `.github/workflows/ci-security-codeql.yml`; Controls: `analyze-trusted`, `github/codeql-action/analyze`, `upload: always` und job-scoped `security-events: write`.
- Voraussetzungen: Default Setup ist für Actions, C/C++ und Python konfiguriert; der vertrauenswürdige Workflow läuft bei `push` auf `master`.
- Fehlgeschlagener Run: [CodeQL analysis `29701466354`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29701466354); Jobs `88231112053`, `88231112086` und `88231112094`.
- Aufbewahrte Evidence: `pr27-master-6de40c-post-merge-verification.de.md` (`/var/tmp/codex/ModSecurity-conector/runs/20260719T180448Z-framework-pr27-sonar-remediation-72a73203/evidence/pr27-master-6de40c-post-merge-verification.de.md`), SHA-256 `01e1b6c361e5bc6aa25d6b4dc0f0c8646b56007fdb1680e6bb26557f65d6ec6f`.

```text
Code Scanning could not process the submitted SARIF file:
CodeQL analyses from advanced configurations cannot be processed when the default setup is enabled
```

Die aufbewahrte Evidence enthält lesende Befehle für den fehlgeschlagenen Run, Exact-Master-Check-Runs, Default-Setup-Status und Exact-SHA-Code-Scanning-Analysen; alle endeten mit Exit `0`.

Der spätere externe Zustands-Readback (nicht als lokales Artifact aufbewahrt)
verwendete:

```text
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/code-scanning/default-setup
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/8572da580e11bc3c62f6ef559152f49b30650056/check-runs --paginate
```

Er beobachtete `state: not-configured` und terminal erfolgreiche
Advanced-CodeQL-Jobs für alle drei Sprachen. Dies ist ausschließlich
Current-State-Evidence; es schreibt den externen Konfigurationswechsel weder
diesem Task zu noch autorisiert ihn.

## Grundursache und erwartetes Verhalten

GitHub Default Setup und der repositoryeigene vertrauenswürdige Advanced-Workflow sind beide dafür konfiguriert, CodeQL-Ergebnisse für dieselben Master-Sprachen hochzuladen. GitHub lehnt die Advanced-SARIF-Verarbeitung ab, solange Default Setup aktiviert bleibt. Genau eine kompatible Konfiguration soll je Sprache hochladen und der gewählte vertrauenswürdige Workflow muss ohne Unterdrückung oder Abschwächung eines Controls erfolgreich enden.

## Remediation, Akzeptanz und Validierung

Ein autorisierter Owner muss auf einem neuen geprüften normalen Framework-PR eine Konfiguration wählen: Default Setup deaktivieren und den geprüften Advanced-Uploader behalten oder den Advanced-Uploader neu gestalten/entfernen, während unabhängig verifiziertes kompatibles Scanning erhalten bleibt. Keinen direkten Master-Push, keinen Control-Bypass, keine Permission-Abschwächung, keine Failure-Unterdrückung und keine Parent-/MRTS-Änderung vornehmen.

- [ausstehend] GitHub-Readback belegt die ausdrücklich autorisierte Konfiguration; der spätere externe Zustand `not-configured` ist nicht diese Autorisierung.
- [historischer Fehler / späterer Erfolg] Die Advanced-Uploads auf `6de40c...` scheiterten; die späteren externen Advanced-Jobs auf `8572da...` bestanden, validieren aber nicht das historische Merge-Ergebnis.
- [bestanden] Default Setup erzeugte Actions-, C/C++- und Python-Analysen für `6de40c171...` und null offene Alerts.
- [ausstehend] Der Advanced-Uploader besteht oder wird durch ein autorisiertes, unabhängig verifiziertes Design ersetzt.

Regression-/Control-Checks: Exact-Master-CodeQL-Run `29701466354`; Default-Setup-Analysen für alle drei Sprachen; null offene Code-Scanning-Alerts; und der erhaltene vertrauenswürdige Workflow mit job-scoped `security-events: write` ohne `pull_request`-Trigger.

## Abhängigkeiten, Blocker, verwandte Findings, Restrisiko und Historie

Abhängigkeiten: eine autorisierte GitHub-Code-Scanning-Konfigurationsentscheidung, ein neuer geprüfter Framework-PR falls eine Repository-Änderung nötig ist, und GitHub-gehostete CodeQL-Verarbeitung. Blocker: Der später extern beobachtete Zustand `not-configured` ist keine ausdrückliche autorisierte Konfigurationsdisposition und widerspricht der früheren Retain-Default-Setup-Entscheidung für PR #27; der fehlgeschlagene exakte Upload auf `6de40c...` bleibt historische Evidence. Verwandte Findings: `FND-FRAMEWORK-0017`, `FND-FRAMEWORK-0020`, `FND-GITHUB-0005` und `FND-SONAR-0002`; dieser Record ist von allen verschieden.

Der Nutzer autorisierte diesen konkreten PR-#27-Merge nach Offenlegung, aber das macht den beobachteten Advanced-Fehler nicht zu einem Pass und autorisiert keine korrigierende Settings-/Workflow-Änderung. Der spätere externe Konfigurationszustand kann Advanced-Uploads erlauben, bleibt aber nicht genehmigt und hinsichtlich Dauerhaftigkeit unverifiziert. Der separate Master-SonarCloud-Fehler bleibt das begrenzte akzeptierte Risiko `FND-SONAR-0002` und waived dieses Finding nicht.

- `2026-07-19T20:00:39Z`: resulting_master_advanced_codeql_upload_failure_confirmed — PR #27 wurde bei `6de40c1714410241e917e9083ee890a82fb2fdbb` gemergt; alle drei Advanced-Uploads scheiterten nach der Analyse, weil Default Setup aktiviert ist, während alle drei Default-Setup-Analysen bestanden.
- `2026-07-19T20:32:09Z`: external_post_merge_code_scanning_state_change_observed — Framework-master war extern auf `8572da580e11bc3c62f6ef559152f49b30650056` weitergelaufen; der API-Readback meldet Default Setup `not-configured` und erfolgreiche Advanced-CodeQL-Jobs. Kein Setting und kein Master-Commit wurde durch diesen Task vorgenommen, und der ursprüngliche Exact-SHA-Fehler bleibt historische Evidence bis zu einer aktuellen autorisierten Konfigurationsdisposition.

## Aktuelle Nutzer-Accepted-Risk-Archiv-Disposition — 2026-07-26

Um `2026-07-26T14:18:25Z` akzeptierte der aktuelle Nutzer dieses exakte
Restrisiko ausdrücklich für die lokale Archivierung. Der exakte
Resulting-Master-Advanced-CodeQL-Fehler ist kein Pass, und der später extern
beobachtete `not-configured`-Default-Setup-Zustand mit erfolgreichen Advanced-
Jobs belegt keine absichtlich gewählte, dauerhafte, autorisierte Konfiguration.
Der Status ist `accepted_risk`, nicht `closed`; vor Produktion,
Veröffentlichung oder Release muss der Record wiederhergestellt und neu
validiert werden.
