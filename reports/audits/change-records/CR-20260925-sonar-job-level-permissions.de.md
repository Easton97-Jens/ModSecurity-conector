# Change Record: SonarQube-Cloud-Remediation für GitHub-Actions-Berechtigungen auf Job-Ebene

**Sprache:** [English](CR-20260925-sonar-job-level-permissions.md) | Deutsch

## Identity

| Feld | Wert |
| --- | --- |
| Change ID | CR-20260925-sonar-job-level-permissions |
| Datum (UTC) | 2026-09-25 |
| Basisrevision | `34aa7da8eea8c7a820c3951ee6c9846567e95b8a` |
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
- Keine Sonar-Regel, Exclusion, Suppression, akzeptiertes Issue, kein Quality
  Gate, Branch Protection, Authentifizierungs- oder Validierungs-Control wird
  geschwächt.

## Technische Entscheidungen

Die Reparatur ändert den Autorisierungs-Scope, nicht die effektive
Job-Capability. Der bisherige Workflow-Level-Default `contents: read` wird
durch `permissions: {}` ersetzt. Jobs ohne direkte Permission-Mapping erhalten
ein job-lokales `contents: read`; Jobs mit bestehenden expliziten Mappings
behalten diese Mappings unverändert.

Der CI-Security-Contract versteht jetzt auch inline leere Permission-Mappings
und verlangt Default-Deny auf Workflow-Ebene sowie eine explizite
Permission-Deklaration für jeden Job. Die bestehende exakte Allowlist für
Write-Permissions bleibt erhalten.

## Security-Auswirkung

Dies ist eine Least-Privilege-Härtung der CI. Ein neu hinzugefügter Job kann
nicht mehr stillschweigend Repository-Read-Rechte erben, und die Token-Grenze
jedes bestehenden Jobs ist dort prüfbar, wo der Job definiert ist. Kein Job
erhält eine Capability, die er vor dieser Änderung nicht effektiv hatte.
Bestehende eng allowlistete Write-Jobs bleiben unverändert.

## Geänderte Dateien

- Alle versionierten Dateien unter `.github/workflows/*.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260925-sonar-job-level-permissions.md`
- `reports/audits/change-records/CR-20260925-sonar-job-level-permissions.de.md`

Framework-Source, der Parent-Framework-Gitlink und verschachteltes MRTS bleiben
unverändert.

## Tests und tatsächliche Ergebnisse

| Check | Ergebnis | Beobachtetes Ergebnis |
| --- | --- | --- |
| Pre-Fix-Readback des exakten `master`-SonarQube-Cloud-Checks über den GitHub-Check | erwartungsgemäß fehlgeschlagen | Security Rating on New Code `C`; erforderlich ist `A`. |
| Historischer exakter `master`-Vergleich | Passed-/Failed-Grenze identifiziert | `5170d248...` bestand; `7dd47a0...` und `34aa7da...` scheitern an derselben Security-Rating-Bedingung. |
| Repository-weites Workflow-Permission-Inventar | bestanden | Workflow-Level-Vererbung von `contents: read` und die davon abhängigen Jobs wurden identifiziert; bestehende Write-Grants sind job-spezifisch. |
| Source-Transformationsinvarianten | bestanden | Top-Level-Scope wird Default-Deny; zuvor erbende Read-Jobs erhalten expliziten job-lokalen Read-Scope; bestehende direkte Permission-Blöcke bleiben erhalten. |
| Hosted Draft-PR-Checks | ausstehend | Dürfen erst für den exakten Draft-PR-Head nach Veröffentlichung bewertet werden. |

## Runtime-Evidenz

Es ändert sich kein Connector-Runtime-Verhalten. Runtime-Evidenz ist für diese
Reparatur des GitHub-Actions-Token-Scopes nicht anwendbar.

## Nicht ausgeführte Checks

Lokale Repository-Kommandos wurden nicht ausgeführt, weil die aktuelle
Ausführungsoberfläche GitHub-Repository-Operationen statt der vom Repository
geforderten RTK-/lokalen Command-Umgebung bereitstellt. Hosted Checks des
veröffentlichten Draft PR sind die verfügbare Ausführungsevidenz für diese
Delivery.

## Bekannte Einschränkungen

Der SonarCloud-Issue-List-Payload selbst war über die aktuelle Umgebung nicht
verfügbar; deshalb erfindet dieser Record keinen Issue-Key. Die Remediation ist
an das beobachtete fehlschlagende Security Rating, die aktuellen
Sonar-Rule-Semantiken und das passende Repository-weite Workflow-Muster
gebunden.

## Restrisiken

`FND-SONAR-0090` ist durch die Source-Änderung `fixed`, aber erst
`verified`, wenn der exakte Draft-PR-Head eine terminale SonarQube-Cloud-
Analyse besitzt und die erwarteten Hosted-CI-Security-Checks erfolgreich
abschließen. Ein separates verbleibendes Sonar-Finding muss gegebenenfalls auf
Basis frischer Exact-Head-Evidenz behandelt werden, statt Scanner oder Quality
Gate zu schwächen.

## Finaler Review-Status

Der begrenzte Diff ändert ausschließlich die Platzierung von
GitHub-Actions-Token-Berechtigungen, ihren statischen Regression-Contract und
diesen zweisprachigen Change Record. Kein Merge ist durch diese Aufgabe
autorisiert oder ausgeführt.
