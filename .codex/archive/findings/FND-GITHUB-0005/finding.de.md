# FND-GITHUB-0005 — Framework-master-Governance und Actions-Defaults besitzen keine externe Durchsetzung

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-GITHUB-0005 |
| Titel | Framework-master-Governance und Actions-Defaults besitzen keine externe Durchsetzung |
| Kategorie | github_governance |
| Repository | framework |
| Ownership | github_configuration |
| Priorität | P1 |
| Schweregrad | not_applicable |
| Konfidenz | validated |
| Status | accepted_risk |
| Feasibility | out_of_scope |
| Release-Blocker | true |
| Security-Relevanz | true |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

Der Framework-PR-#27-Source begrenzt Pull-Request-CodeQL korrekt auf einen
exakten, credentialless, read-only Head ohne Upload und hält den
vertrauenswürdigen Uploader außerhalb des Pull-Request-Triggers mit nur
security-events write. Diese Source-Controls sind gültige Defense in Depth,
erzwingen aber nicht unabhängig, dass spätere master- oder Workflow-Änderungen
dieselben Deklarationen behalten.

Für Easton97-Jens/ModSecurity-test-Framework auf exaktem geprüftem Head
2f635be02ede802024ec9e0ce2ed41e3030cbff2 beweist der aufbewahrte
schreibgeschützte GitHub-Konfigurations-Receipt:

- klassischer master-Schutz liefert HTTP 404 Branch not protected;
- master meldet protected=false und keine Required Checks;
- Repository-Rulesets und effektive master-Regeln sind leer;
- Actions default_workflow_permissions ist write; und
- ein direkter Collaborator besitzt admin-, maintain- und push-Fähigkeiten.

Das Ergebnis ist eine reale GitHub-Governance- und Master-Integrations-Control-
Lücke. Ein privilegierter Collaborator oder ein kompromittiertes privilegiertes
Credential kann master oder den entscheidenden Workflow ohne nachgewiesenen
unabhängigen PR-, Review- oder current-head-Check ändern. Es werden keine
unauthentifizierte RCE, kein PR-Write-Token, keine Secret-Exposition, keine
Parent-Gitlink-Aktion und keine MRTS-Aktion behauptet.

Die abgeschlossene Attack-Path-Analyse nennt dies absichtlich keine reportable
Security-Vulnerability: Der einzige nachgewiesene Angreifer besitzt bereits
privilegierte Repository-Write-Autorität und es ist keine Lower-Privilege-
Eskalation bewiesen. Dieses Policy-Ergebnis stellt das fehlende gehostete
Governance-Control nicht her und macht die master-Delivery nicht sicher.

## Erwartetes Verhalten, betroffener Scope, Voraussetzungen und Reproduktion

GitHub muss unabhängig No-bypass-master-Schutz oder Regeln, current-head
Pull-Request-/Review-/Required-Check-Anforderungen und Least-Privilege-
Actions-Defaults erzwingen. Die aktuellen Source-kontrollierten
Workflow-Berechtigungen bleiben Defense in Depth statt eines Ersatzes für
dieses gehostete Control.

Betroffener Source-Kontext:

- .github/workflows/ci-security-codeql-pr.yml
- .github/workflows/ci-security-codeql.yml

Der beobachtete Pfad erfordert einen böswilligen privilegierten Collaborator
oder ein kompromittiertes privilegiertes Credential. Kein Lower-Privilege-
externer oder Fork-PR-Pfad ist nachgewiesen.

~~~bash
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master/protection
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rulesets
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rules/branches/master
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/actions/permissions/workflow
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/collaborators?affiliation=direct
~~~

## Evidence

- Run-ID: 20260719T081017Z-framework-pr-resolution-20260719-840082e0
  - Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/framework-github-governance-readback-20260719T160637Z.md
  - Typ: github_master_governance_read_only_configuration_receipt
  - SHA-256: 1cbdf30f5a0dfe329c354f753cce92f037067d92ba8ccd9435e6efe08ee1d354
  - Command: rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master/protection; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/branches/master; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rulesets; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/rules/branches/master; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/actions/permissions/workflow; rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/collaborators?affiliation=direct
  - Working directory: /var/tmp/codex/worktrees/framework-ci-security; Exit-Code: 0; beobachtet am 2026-07-19T16:06:37Z; Retention: retained_task_evidence.

Der Diff-Scan-Bericht liegt unter /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/analysis/security-diff-pr27-final-sync/report.md. Sein Kandidat CAND-PR27-GITHUB-GOVERNANCE-001 besitzt Discovery-, Validation- und Attack-Path-Receipts. Die Attack-Path-Final-Policy ist ignore, weil die nachgewiesene Quelle privileged-only ist; dieses Finding bewahrt die getrennte Release-Control-Disposition.

## Grundursache, Remediation und Akzeptanzkriterien

Die Grundursache ist externe GitHub-Control-Plane-Konfiguration. Der
Framework-Workflow-Source begrenzt den aktuellen PR, aber GitHub verlangt nicht
unabhängig, dass künftige master- oder Workflow-Änderungen seine Berechtigungen,
den exact-head Checkout oder die Upload-Trennung erhalten. Fehlender
Schutz/effektive Regeln und ein write-Actions-Default sind vom aktuell sicheren
PR-Source verschieden.

Nur ein autorisierter GitHub-Repository-Owner oder Administrator darf die
Remediation entscheiden und anwenden:

1. No-bypass-master-Schutz oder Regeln herstellen;
2. current-head PR-, Review- und Required-Check-Durchsetzung verlangen; und
3. Least-Privilege-Default-Actions-Workflow-Berechtigungen setzen.

Danach dieselben Endpoints erneut lesen und die Exact-Head-PR-#27-Delivery-
Verifikation wiederholen. Keinen direkten master-Push, keinen Administrator-
Bypass und keine Check-Abschwächung verwenden und Risikoakzeptanz nicht aus
einer Merge-Anfrage ableiten.

Akzeptanzkriterien:

- Ein Post-Change-schreibgeschützter Receipt beweist No-bypass-master-Schutz
  oder effektive Regeln.
- Die Regel verlangt die beabsichtigten current-head PR-, Review- und
  Required-Check-Controls ohne direkten Push oder Administrator-Bypass.
- Der Actions-Endpoint meldet einen Least-Privilege-Default statt
  default_workflow_permissions=write.
- PR #27 wird auf seinem exakten aktuellen Head erneut gelesen und erfüllt
  alle Delivery-, Review-, Thread-, Ruleset- und Merge-Method-Voraussetzungen.
- Kein Parent-Source/Gitlink, MRTS-Content/Gitlink, Framework-Source,
  Security-Control oder SonarCloud-Ergebnis wird als Workaround abgeschwächt.

## Validierung, Abhängigkeiten, Blocker, verwandte Findings, Restrisiko und Historie

Die Validierung erfordert einen frischen hash-adressierten API-Readback, die
Prüfung der effektiven master-Regel und Bypass-Settings, einen erneuten
Exact-Head-PR-#27-Preflight und die Bestätigung, dass die bestehenden PR- und
vertrauenswürdigen CodeQL-Workflows legitime Controls bleiben.

Abhängigkeiten: eine explizite aktuelle Nutzerentscheidung, die
GitHub-Konfigurationsänderung zu autorisieren, oder eine explizite Akzeptanz
des präzisen Restrisikos; außerdem ein GitHub-Repository-Owner oder
Administrator, der die Konfiguration anwenden und erneut lesen kann.

Blocker: Diese Aufgabe besitzt keine explizite Autorität, Branch Protection,
Rulesets, Bypass-Settings oder Actions-Defaults zu ändern; der Receipt beweist
die Abwesenheit der Voraussetzungen. Die Accepted-Risk-Archiventscheidung des
aktuellen Nutzers behebt das verbleibende Direct-master-/Check-Bypass-Risiko
nicht.

Verwandte, aber getrennte Records sind FND-GITHUB-0001, FND-GITHUB-0002,
FND-GITHUB-0004, FND-FRAMEWORK-0013 und FND-FRAMEWORK-0019.

Vor der Archiventscheidung des aktuellen Nutzers vom 2026-07-26 wurde kein
Risiko akzeptiert. Bis eine autorisierte Konfigurationsentscheidung und ein
Endpoint-Readback erfolgen, kann ein privilegierter Collaborator oder ein
kompromittiertes privilegiertes Credential die unabhängig erzwungene
master-Review-/current-head-Check-Grenze umgehen, die für sichere Integration
erforderlich ist. Aktuelle PR-Controls bleiben gültig, sind aber keine externe
No-bypass-Garantie.

Historie:

- 2026-07-19T16:06:37Z: Read-only-API-Evidence zeichnete fehlenden
  master-Schutz/-Regeln und den write-Actions-Default auf.
- 2026-07-19T16:35:35Z: CAND-PR27-GITHUB-GOVERNANCE-001 schloss Discovery,
  Validation und Attack-Path-Analyse ab. Die Security-Policy ignorierte ihn als
  privileged-only; die unabhängige master-Integrations-Governance-Anforderung
  bleibt blocked.

## Aktuelle Nutzer-Accepted-Risk-Archiv-Disposition — 2026-07-26

Um `2026-07-26T14:18:25Z` akzeptierte der aktuelle Nutzer dieses exakte
Restrisiko ausdrücklich für die lokale Archivierung. Bis eine autorisierte
GitHub-Konfigurationsentscheidung und ein Endpoint-Readback erfolgen, kann ein
privilegierter Collaborator oder ein kompromittiertes privilegiertes Credential
die unabhängig erzwungene master-Review-/current-head-Check-Grenze umgehen.
Keine Regel, kein Schutz, kein Bypass und kein Actions-Default wurde geändert.
Der Status ist `accepted_risk`, nicht `closed`; vor Produktion,
Veröffentlichung oder Release muss der Record wiederhergestellt und neu
validiert werden.
