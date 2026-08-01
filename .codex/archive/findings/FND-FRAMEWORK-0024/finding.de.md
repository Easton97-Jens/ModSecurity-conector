# FND-FRAMEWORK-0024 — Framework-PR-#30-Change-Record-Paar verletzt den aktuellen kanonischen Überschriftenvertrag

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0024 |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P1 / not_applicable |
| Confidence / Status | reproduced / fixed |
| Feasibility | feasible_now |
| Release-Blocker | false |
| Security-relevant | false |

## Zusammenfassung, Beobachtung, erwartetes Verhalten und Auswirkung

Nach dem normalen Framework-master-Update für PR #30 lehnte der aktuelle
CI-Security-Change-Record-Vertrag beide bestehenden Records ab:
reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.md
und seinen .de.md-Begleiter. Jeder Record hat bereits die kanonischen dreizehn
Abschnitte auf Ebene 2, fügt danach aber vier historische Follow-up-Narrative
als weitere Abschnitte auf Ebene 2 hinzu. Der aktuelle Vertrag verlangt die
kanonische Abschnittssequenz exakt.

make test-ci-security-contract führte 69 Tests aus: 68 bestanden und
ChangeRecordContractTest.test_checked_in_change_records_pass schlug fehl. Die
exakte Diagnose lautete: English Change Record headings do not match the
template; German Change Record headings do not match the template.

Beide Records müssen jedes historische Narrativ, den reziproken Sprachlink und
die Change-ID bewahren und zugleich exakt die kanonischen dreizehn
Überschriften auf Ebene 2 ausweisen. Die Reparatur darf Checker, Test, Template
oder CI-Security-Enforcement nicht ändern. Dies war ein reproduzierbarer
erforderlicher CI-Fehler, keine validierte Schwachstelle.

Am aktualisierten exakten PR-Head `a448d056ef98e745d8551c198b2e56d33fe38194`
bestand die unveränderte CI-Security-Suite alle 69 Tests,
Dokumentationsprüfungen bestanden und jeder terminale nicht übersprungene
Hosted Check war erfolgreich. Der Befund ist daher auf dem verifizierten
PR-Head `fixed`, ohne Checker-, Template-, Traceability-Control- oder
Exception-Änderung. Er ist nicht auf Master `verified`, weil die aktuelle
Aufgabe keinen Framework-master-Merge autorisiert.

## Scope, Voraussetzungen, Reproduktion und Evidence

Betroffen sind die gepaarten PR-#30-Change-Records. Der relevante Vertrag ist
ci/checks/documentation/check-change-records.py und sein Test ist
tests/ci_security/test_change_record_contract.py. Voraussetzungen sind der
aktuelle Framework-master 9a729226d2e040d07d7e7a4acebf201faf06ab37 im
Task-Worktree und die vier zusätzlichen History-Überschriften auf Ebene 2 in
den bestehenden Records.

~~~
rtk proxy env <task-owned roots> make -C <Framework PR30 worktree> test-ci-security-contract
rtk rg -n '^## ' reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.md reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.de.md
rtk sed -n '1,160p' ci/checks/documentation/check-change-records.py
~~~

Aufbewahrte Evidence:
- Run: 20260719T230508Z-framework-pr30-duplication-master-37469460
- Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-merge-change-record-contract-failure.md
- SHA-256: 1b0055525f231fc5584fff88b49e357ffbb92228f77a56ae0736a78ee1e321da
- Working Directory: /root/git/ModSecurity-conector
- Exit-Code: 2
- Beobachtet: 2026-07-19T23:35:54Z
- Retention: retained

- Run: 20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef
- Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef/evidence/pr30-refresh-summary.md
- SHA-256: 04a0b6891f92b0485c298bb939e57fb464cea2bd5872eb74c65d97f6450f4255
- Command: Task-root-CI-Security- und Dokumentationsprüfungen plus GitHub-Exact-Head-Check-Run/Review-Readback
- Working Directory: /root/git/ModSecurity-conector
- Exit-Code: 0
- Beobachtet: 2026-07-20T06:43:42Z
- Retention: retained
- Ergebnis: Exakter PR-#30-Head `a448d056ef98e745d8551c198b2e56d33fe38194`
  bestand die unveränderte 69-Test-CI-Security-Suite,
  Dokumentationsprüfungen und alle terminalen nicht übersprungenen Hosted
  Checks.

## Grundursache und vorgeschlagene Remediation

Das historische PR-#30-Paar stammt vor dem strikten aktuellen
Change-Record-Checker. Es platzierte spätere historische Updates auf Ebene 2
statt als Unterabschnitte auf Ebene 3 unter dem erforderlichen finalen
Review-Abschnitt.

Nur diese vier zusätzlichen History-Überschriften in jeder Sprache von Ebene 2
auf Ebene 3 herabstufen. Allen Text, Sprachlinks, Change-IDs, die kanonischen
dreizehn Überschriften und Englisch-/Deutsch-Parität bewahren. Den Checker oder
ein Control nicht ändern.

## Akzeptanzkriterien und Validierungsplan

- [complete] Beide Records weisen exakt die kanonischen dreizehn Überschriften auf Ebene 2 aus.
- [complete] Die vier historischen Updates bleiben als Unterabschnitte auf Ebene 3 vorhanden.
- [complete] Reziproke Englisch-/Deutsch-Links und passende Change-IDs bleiben gültig.
- [complete] Der direkte Change-Record-Vertrag und die unveränderte 69-Test-CI-Security-Suite bestehen.
- [complete] Der aktualisierte PR-Head bestand alle terminalen nicht übersprungenen Hosted Checks.
- [pending authorization] Framework-master-Integration und Resulting-Master-Revalidation sind von der aktuellen Aufgabe nicht autorisiert.

Überschriften vor und nach der Reparatur prüfen; den direkten Vertrag und die
vollständige CI-Security-Suite mit task-eigenen Roots ausführen; EN/DE-Parität
und den abgegrenzten Diff prüfen; danach Exact-Head-Hosted-CI nach dem normalen
Push verlangen.

## Regression- und Legitimate-Control-Tests

Regressionstests sind:
- tests/ci_security/test_change_record_contract.py
- make test-ci-security-contract

Der unveränderte Checker muss nichtkanonische oder fehlende Überschriften
weiterhin ablehnen und das reparierte kanonische Paar mit gültigen reziproken
Links und Change-IDs akzeptieren.

## Abhängigkeiten, Grenzen, verwandte Findings und Restrisiko

Abhängigkeiten sind aktuelle Framework-master-Change-Record-Controls, der
isolierte PR-#30-Worktree und Exact-Head-Hosted-CI nach dem normalen Push. Es
gibt keine aktuellen Blocker oder Duplicate-Records.

Dieser Befund ist von FND-FRAMEWORK-0023 verschieden, das PR-#30-Sonar-
Duplikation und Source-/Test-Refaktorierung besitzt. Dieser Befund besitzt den
unabhängigen Change-Record-Formatfehler, der durch den normalen Master-Update
sichtbar wurde.

Der ursprüngliche Fehler reproduziert auf dem exakten PR-Head nicht mehr,
daher ist dieser Befund fixed. Die einzige Delivery-Lücke ist die bewusst nicht
ausgeführte Framework-master-Integration mit Resulting-Master-Revalidation; sie
folgt weder aus diesem Finding noch ist sie vom aktuellen Nutzer autorisiert.
Kein Checker, Traceability-Control, Parent-Gitlink oder MRTS-Zustand wird
geändert oder waived.

## Verlauf

- 2026-07-19T23:35:54Z —
  change_record_contract_failure_confirmed_after_normal_master_update: Die
  aktuelle Master-CI-Security führte 69 Tests aus und nur der gepaarte PR-#30-
  Change-Record-Überschriftenvertrag schlug fehl. Die geplante Reparatur ist
  eine Level-2-zu-Level-3-Überschriftenanpassung in beiden Records ohne
  Checker- oder Control-Änderung.
- 2026-07-20T06:43:42Z — exact_refreshed_pr_head_passes_unchanged_contract:
  Exakter PR-#30-Head `a448d056ef98e745d8551c198b2e56d33fe38194` bestand die
  unveränderte 69-Test-CI-Security-Suite, Dokumentationsprüfungen und jeden
  terminalen nicht übersprungenen Hosted Check. Der Befund ist auf dem
  verifizierten PR-Head fixed; die Master-Integration bleibt nicht autorisiert.
