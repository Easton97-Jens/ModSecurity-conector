# Change Record: SonarQube-Cloud-Remediation für GitHub-Actions-Berechtigungen auf Job-Ebene

**Sprache:** [English](CR-20260925-sonar-job-level-permissions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260925-sonar-job-level-permissions |
| Datum (UTC) | 2026-09-25 |
| Basis-Revision | `34aa7da8eea8c7a820c3951ee6c9846567e95b8a` |
| Finding | `FND-SONAR-0090`; GitHub-Actions-Vulnerability-Muster für Token-Berechtigungen auf Job-Ebene (`githubactions:S8264`) |
| Benutzerautorisierung | Die bereitgestellten offenen SonarCloud-Findings untersuchen und in einem GitHub-Draft-PR beheben. |
| Delivery-Status | Begrenzte Parent-Reparatur auf `fix/sonar-job-level-permissions`; Draft-PR-Delivery ist autorisiert, Merge, Auto-Merge, direkte `master`-Writes, Framework-/MRTS-Änderungen, Rule-Suppression, Issue-Akzeptanz und Quality-Gate-Änderungen sind es nicht. |

## Motivation und Problemstellung

Der exakte `master`-SonarQube-Cloud-Check für
`34aa7da8eea8c7a820c3951ee6c9846567e95b8a` schlägt am Quality Gate fehl,
weil das Security Rating on New Code `C` ist, während `A` erforderlich ist.
Die vorherige `master`-Revision
`5170d24801243cdcd7bf1bca6123bf8cb2c72386` bestand; die erste beobachtete
fehlschlagende `master`-Analyse ist
`7dd47a0ba9a94c8aec110630d417dd5e7bd6d271`.

Die bereitgestellte SonarCloud-Issue-Seite ist über die verfügbare Umgebung
nicht direkt lesbar, daher wird kein unbeobachteter Sonar-Issue-Key behauptet.
Aktuelle Sonar-Regeln für GitHub Actions klassifizieren Read-Berechtigungen,
die vom Workflow-Scope geerbt statt am Job-Scope deklariert werden, als
`githubactions:S8264`-Vulnerability-Muster. Die Repository-Prüfung ergab,
dass alle versionierten GitHub-Actions-Workflows `contents: read` auf
Workflow-Ebene setzen und mehrere Jobs diese Berechtigung erben.

Der erste exakte PR-Head legte zusätzlich zwei unabhängige Ursachen roter
Checks offen. Der Phase-4-Migrationstest prüfte noch die entfernte
Workflow-Level-Read-Syntax, und der with-CRS/no-MRTS-Workflow erwartete weiter
MRTS `615b13bacbd008562c17408246c41ab27dca3104`, obwohl der geprüfte Framework-
Commit `6c248afe85c24ebdfb1cd66e171e908f7ef29d48` den Gitlink
`8a6bb546c4c81d8ffc7be801dceac60c6925685f` enthält. Der GitHub-Vergleich
zeigt, dass die neue MRTS-Revision exakt einen Nachfolge-Commit vor der alten
Revision liegt.

## Akzeptanzkriterien

- Jeder versionierte GitHub-Actions-Workflow hat eine Default-Deny-Deklaration
  `permissions: {}` auf Top-Level.
- Jeder Job deklariert seine eigene Berechtigungsgrenze explizit.
- Jobs, die zuvor `contents: read` geerbt haben, erhalten exakt
  `contents: read` auf Job-Ebene.
- Bestehende job-spezifische Write-Berechtigungen bleiben hinsichtlich ihrer
  Capabilities unverändert und werden nicht erweitert.
- Ein fokussierter CI-Security-Regressionstest weist künftig Workflows ab, die
  geerbten Top-Level-Read-Zugriff wieder einführen oder eine explizite
  Job-Berechtigungsgrenze auslassen.
- Der Phase-4-Workflow-Contract prüft die neue Default-Deny- plus job-lokale
  Read-Permission-Form statt der entfernten geerbten Form.
- Der with-CRS/no-MRTS-Workflow pinnt die exakte MRTS-Revision, die im
  geprüften Framework-Commit eingetragen ist, sodass die fünf Zellen ihre
  Revisionsprüfung passieren können.
- Keine Sonar-Regel, Exclusion, Suppression, akzeptiertes Issue, kein Quality
  Gate, Branch Protection, Authentifizierungs- oder Validierungs-Control wird
  geschwächt.

## Implementierungsentscheidung und Begründung

Die Reparatur ändert den Autorisierungs-Scope, nicht die effektive
Job-Capability. Der bisherige Workflow-Level-Default `contents: read` wird
durch `permissions: {}` ersetzt. Jobs ohne direkte Permission-Mapping erhalten
ein job-lokales `contents: read`; Jobs mit bestehenden expliziten Mappings
behalten diese Mappings unverändert.

Der CI-Security-Contract versteht jetzt auch inline leere Permission-Mappings
und verlangt Default-Deny auf Workflow-Ebene sowie eine explizite
Permission-Deklaration für jeden Job. Die bestehende exakte Allowlist für
Write-Permissions bleibt erhalten. Die Phase-4-Regression prüft denselben
Vertrag statt der entfernten Workflow-Level-Zeile `contents: read`.

Für die Runtime-Matrix wird ausschließlich die Parent-seitige erwartete
MRTS-Konstante von `615b13bacbd008562c17408246c41ab27dca3104` auf
`8a6bb546c4c81d8ffc7be801dceac60c6925685f` angehoben. Der Framework-Gitlink
bleibt `6c248afe85c24ebdfb1cd66e171e908f7ef29d48`; dieser PR ändert weder
Framework- noch MRTS-Source. Der neue Wert entspricht dem tatsächlichen
Nested-Gitlink dieses Framework-Commits und erhält die Exact-SHA-Prüfung.

## Security-Auswirkung

Dies ist eine Least-Privilege-Härtung der CI. Ein neu hinzugefügter Job kann
nicht mehr stillschweigend Repository-Read-Rechte erben, und die Token-Grenze
jedes bestehenden Jobs ist dort prüfbar, wo der Job definiert ist. Kein Job
erhält eine Capability, die er vor dieser Änderung nicht effektiv hatte.
Bestehende eng allowlistete Write-Jobs bleiben unverändert. Der MRTS-Follow-up
weitet Vertrauen nicht aus: Ein veralteter exakter SHA wird durch den exakten
Nested-Gitlink ersetzt, den der geprüfte Framework-Commit bereits auswählt;
diese MRTS-Revision ist ein verifizierter direkter Nachfolge-Commit des alten
Pins.

## Geänderte Dateien

- Alle versionierten Dateien unter `.github/workflows/*.yml`
- `tests/test_ci_security_workflows.py`
- `tests/test_phase4_migration_contract.py`
- `reports/audits/change-records/CR-20260925-sonar-job-level-permissions.md`
- `reports/audits/change-records/CR-20260925-sonar-job-level-permissions.de.md`

Framework-Source, der Parent-Framework-Gitlink und verschachtelte MRTS-Source
bleiben unverändert. Der erwartete MRTS-SHA im Parent-Workflow wird mit dem
bereits ausgewählten Framework-Nested-Gitlink synchronisiert.

## Ausgeführte Befehle

| Check | Ergebnis | Beobachtetes Ergebnis |
| --- | --- | --- |
| Pre-Fix-Readback des exakten `master`-SonarQube-Cloud-Checks über den GitHub-Check | erwartungsgemäß fehlgeschlagen | Security Rating on New Code `C`; erforderlich ist `A`. |
| Historischer exakter `master`-Vergleich | Passed-/Failed-Grenze identifiziert | `5170d248...` bestand; `7dd47a0...` und `34aa7da...` scheitern an derselben Security-Rating-Bedingung. |
| Repository-weites Workflow-Permission-Inventar | bestanden | Workflow-Level-Vererbung von `contents: read` und die davon abhängigen Jobs wurden identifiziert; bestehende Write-Grants sind job-spezifisch. |
| Source-Transformationsinvarianten | bestanden | Top-Level-Scope wird Default-Deny; zuvor erbende Read-Jobs erhalten expliziten job-lokalen Read-Scope; bestehende direkte Permission-Blöcke bleiben erhalten. |
| Framework/MRTS-Exact-Revision-Readback | bestanden | Framework `6c248afe...` enthält MRTS `8a6bb546...`; der GitHub-Vergleich zeigt, dass `8a6bb546...` einen Commit vor `615b13ba...` liegt. |
| Hosted Checks des ersten Draft-PR-Heads `64b38a34...` | gemischt während der Reparatur | Permission-Regressionstest, `zizmor`, Report-Governance, Protocol-Contract, CodeQL-Actions und PR-Diff übten den neuen Workflow-Scope aus; zwei task-eigene Contract-/Dokumentationsabweichungen wurden für den nächsten Follow-up identifiziert. Die CRS/no-MRTS-Runtime-Matrix scheiterte separat an ihrem veralteten MRTS-Revisions-Assert (`615b13ba...` erwartet, `8a6bb546...` ausgecheckt), bevor Runtime-Ausführung begann. |

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Runtime-Evidenz ist für diese
Reparatur des GitHub-Actions-Token-Scopes nicht anwendbar.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Repository-Kommandos wurden nicht ausgeführt, weil die aktuelle
Ausführungsoberfläche GitHub-Repository-Operationen statt der vom Repository
geforderten RTK-/lokalen Command-Umgebung bereitstellt. Hosted Checks von
Draft PR #386 liefen gegen `64b38a34...`; sie legten die zwei task-eigenen
Contract-/Dokumentationsabweichungen offen, die dieser Follow-up korrigiert,
sowie den oben beschriebenen separaten bestehenden MRTS-Pin-Konflikt. Der
exakte Successor-Head muss erneut gelesen werden.

## Bekannte Einschränkungen

Der SonarCloud-Issue-List-Payload selbst war über die aktuelle Umgebung nicht
verfügbar; deshalb erfindet dieser Record keinen Issue-Key. Die Remediation ist
an das beobachtete fehlschlagende Security Rating, die aktuellen
Sonar-Rule-Semantiken und das passende Repository-weite Workflow-Muster
gebunden.

## Verbleibende Risiken

`FND-SONAR-0090` ist durch die Source-Änderung `fixed`, aber erst
`verified`, wenn der exakte Draft-PR-Head eine terminale SonarQube-Cloud-
Analyse besitzt und die erwarteten Hosted-CI-Security-Checks erfolgreich
abschließen. Ein separates verbleibendes Sonar-Finding muss gegebenenfalls auf
Basis frischer Exact-Head-Evidenz behandelt werden, statt Scanner oder Quality
Gate zu schwächen.

## Finaler Diff- und Review-Status

Der begrenzte Diff ändert ausschließlich die Platzierung von
GitHub-Actions-Token-Berechtigungen, ihren statischen Regression-Contract und
diesen zweisprachigen Change Record. Der erste veröffentlichte Head
`64b38a34...` lieferte reale Hosted-Evidenz; dieser Follow-up richtet die
negative Permission-Mutation und das verpflichtende Change-Record-Schema aus,
ohne Workflow-Capabilities zu ändern. Kein Merge ist autorisiert oder
ausgeführt.
