# FND-FRAMEWORK-0026 — Framework-PR #30: C/C++-CodeQL-Initialisierung war durch einen externen GitHub-Dienstausfall blockiert

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0026 |
| Kategorie | external_dependency |
| Repository / Ownership | framework / external_tool |
| Priorität / Severity | P1 / not_applicable |
| Confidence / Status | confirmed / verified |
| Feasibility | already_fixed |
| Release-Blocker | false |
| Security-relevant | true |

## Zusammenfassung, Beobachtung, erwartetes Verhalten und Auswirkung

Der historische exakte PR-#30-Head
`2706506be9e5f4b5bae57ec6d9419a715a8f3544` hatte einen C/C++-CodeQL-
Initialisierungsfehler, bevor die Source-Analyse begann. Die CodeQL-C/C++-Jobs
`88253045864` und `88253302100` schlugen in
`Initialize CodeQL for actual Framework languages` fehl. GitHubs öffentliche
Annotation meldete HTTP 503 bei der Ermittlung der Feature-Aktivierung: kein
Server war zur Bedienung der Anfrage verfügbar.

Dies war ein externer gehosteter Abhängigkeitsfehler, kein Framework-Source-
oder Workflow-Defekt. Die geänderten PR-Dateien enthielten weder C/C++-Source
noch den CodeQL-Workflow, und es wurde kein CodeQL-Source-Finding erzeugt.
Produktcode zu patchen oder CodeQL als Reaktion abzuschwächen wäre unangemessen
gewesen.

Der aktualisierte exakte Head `a448d056ef98e745d8551c198b2e56d33fe38194`
beendete CodeQL-Pull-Request-Run `29722369621` erfolgreich für Actions-Job
`88287878237`, Python-Job `88287878246` und C/C++-Job `88287878247`. Alle
terminalen nicht übersprungenen Checks bestanden. Der ursprüngliche externe
Fehler reproduziert nicht mehr, daher ist dieser Befund `verified`; er
autorisiert keinen Master-Merge.

## Scope, Voraussetzungen, Reproduktion und Evidence

Der Vorfall erfordert, dass Framework PR #30 durch den CodeQL-Pull-Request-
Workflow am historischen Head `2706506be9e5f4b5bae57ec6d9419a715a8f3544`
analysiert wird, während GitHubs CodeQL-Feature-Enablement-Dienst temporär
nicht verfügbar ist.

1. Die aufbewahrte Job-Annotation für die Jobs `88253045864` und `88253302100`
   in Workflow-Run `29710235017` lesen.
2. Die CodeQL-Check-Runs des exakten aktualisierten Heads
   `a448d056ef98e745d8551c198b2e56d33fe38194`, einschließlich C/C++-Job
   `88287878247`, lesen.
3. GitHubs terminalen Check-Status mit demselben PR-Head-SHA vergleichen.

Aufbewahrte Evidence:

- Run: `20260719T230508Z-framework-pr30-duplication-master-37469460`
- Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-codeql-cpp-hosted-503.md`
- SHA-256: `d41e0212f555f36f073bca5d2d25639acdc55ecbcfe309815609051a8ab1750a`
- Command: GitHub-Actions-Job-Annotation und Failed-Log-Readback für
  CodeQL-Pull-Request-Run `29710235017`; bereinigte aufbewahrte Zusammenfassung
- Working Directory: `/root/git/ModSecurity-conector`
- Exit-Code: `0`
- Beobachtet: `2026-07-20T01:08:00Z`
- Retention: `retained`
- Ergebnis: CodeQL C/C++ schlug vor der Analyse fehl, während die
  Feature-Aktivierung HTTP 503 lieferte; kein Source-Finding oder Debug-
  Artefakt wurde erzeugt.

- Run: `20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef`
- Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef/evidence/pr30-refresh-summary.md`
- SHA-256: `04a0b6891f92b0485c298bb939e57fb464cea2bd5872eb74c65d97f6450f4255`
- Command: GitHub-Exact-Head-Check-Run/Review-Readback für Framework PR #30;
  bereinigte aufbewahrte Zusammenfassung
- Working Directory: `/root/git/ModSecurity-conector`
- Exit-Code: `0`
- Beobachtet: `2026-07-20T06:43:42Z`
- Retention: `retained`
- Ergebnis: CodeQL-Actions-, Python- und C/C++-Jobs `88287878237`,
  `88287878246` und `88287878247` bestanden auf exaktem Head
  `a448d056ef98e745d8551c198b2e56d33fe38194`.

## Grundursache und vorgeschlagene Remediation

GitHubs gehosteter CodeQL-Feature-Enablement-Endpunkt lieferte während der
Initialisierung HTTP 503. Der Fehler trat vor der Source-Analyse auf, daher gab
es keine Evidence für einen task-eigenen Framework-Defekt.

Keinen Framework-Code patchen und kein CodeQL-Control lockern. Den exakten
PR-Head nach Wiederherstellung des gehosteten Dienstes aktualisieren oder erneut
ausführen und danach terminal erfolgreiches C/C++-CodeQL zusammen mit der
anderen Exact-Head-Delivery-Evidence verlangen.

## Akzeptanzkriterien und Validierungsplan

- [complete] Der exakte aktualisierte PR-Head hat terminal erfolgreiches `CodeQL PR (c-cpp)`.
- [complete] CodeQL Actions und Python für denselben exakten Head sind terminal erfolgreich.
- [complete] Kein CodeQL-Workflow, keine Scanner-Einstellung, kein Waiver, kein
  Quality Gate und keine Produkt-Source änderten sich zur Umgehung des historischen HTTP 503.
- [complete] Der historische Fehler und seine externe Grundursache bleiben
  aufbewahrt und von Framework-Source-Findings getrennt.

PR-Head, CodeQL-Run, einzelne Jobs und terminale Status für denselben SHA
auslesen. Bestätigen, dass der aktuelle PR-Diff keinen CodeQL-Workflow- oder
C/C++-Workaround enthält, und das secret-freie Paar aus historischem Fehler und
aktuellem Erfolg aufbewahren.

## Regression- und Legitimate-Control-Tests

Regressionstests:

- GitHub-`CodeQL PR (c-cpp)`-Exact-Head-Check-Run.
- GitHub-`CodeQL PR (actions)`-Exact-Head-Check-Run.
- GitHub-`CodeQL PR (python)`-Exact-Head-Check-Run.

Legitimate Controls:

- Der exakte aktualisierte Head beendet CodeQL C/C++ nach Service-Recovery erfolgreich.
- Derselbe exakte Head behält erfolgreiche CodeQL-Actions- und Python-Checks.
- Keine Scanner-Deaktivierung, kein Waiver, kein Workflow-Bypass und kein Source-Workaround ist vorhanden.

## Abhängigkeiten, Grenzen, verwandte Findings und Restrisiko

Abhängigkeiten sind die Verfügbarkeit des von GitHub gehosteten CodeQL und die
Framework-PR-#30-Exact-Head-Actions-Ausführung. Es gibt keine Blocker oder
Duplicate-Records.

Dies ist kein Duplicate von FND-FRAMEWORK-0023 oder FND-FRAMEWORK-0024. Diese
Findings besitzen PR-#30-Sonar-Duplikation und Change-Record-Contract-Defekte.
Dieser Befund besitzt den getrennten externen GitHub-CodeQL-
Initialisierungsausfall, bewiesen durch HTTP 503 vor der Analyse und spätere
Exact-Head-Recovery.

Die Verfügbarkeit des von GitHub gehosteten CodeQL kann unabhängig von
Framework-Source erneut scheitern. Der historische Vorfall ist auf exaktem
PR-Head `a448d056ef98e745d8551c198b2e56d33fe38194` als wiederhergestellt
verifiziert; eine spätere Delivery muss bei Änderung dieses SHA frische
Exact-Head-Evidence sammeln. Keine Framework-master-Integration,
Parent-Gitlink-Änderung oder MRTS-Aktion ist von dieser Aufgabe autorisiert.

## Verlauf

- 2026-07-20T01:08:00Z — hosted_codeql_initialization_outage_confirmed:
  Historische CodeQL-C/C++-Jobs `88253045864` und `88253302100` schlugen vor
  der Analyse am exakten Head `2706506be9e5f4b5bae57ec6d9419a715a8f3544` fehl;
  GitHub meldete HTTP 503 bei der Ermittlung der Feature-Aktivierung.
- 2026-07-20T06:43:42Z — exact_refreshed_head_codeql_recovery_verified:
  Exakter aktualisierter Head `a448d056ef98e745d8551c198b2e56d33fe38194`
  beendete CodeQL-Pull-Request-Run `29722369621` für Actions-Job `88287878237`,
  Python-Job `88287878246` und C/C++-Job `88287878247` ohne Bypass oder
  Source-Workaround.
