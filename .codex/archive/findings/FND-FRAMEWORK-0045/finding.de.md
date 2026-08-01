# FND-FRAMEWORK-0045 — Framework-PR-#37-Change-Record enthält eine veraltete No-Merge-Delivery-Anweisung

- Kategorie: `documentation_drift`
- Repository / Ownership: `framework` / `framework`
- Priorität / Schweregrad / Konfidenz: `P1` / `not_applicable` / `confirmed`
- Status: `verified`
- Release-Blocker / Security-Relevanz: `false` / `true`

## Zusammenfassung

Die versionierten englischen und deutschen Change Records in Framework-PR #37
besagten ursprünglich,
besagten, dass kein `master`-Merge erlaubt ist, ein normaler Commit/Push
verbleibt und PR #37 ungemergt bleiben muss. Nach ihrer Source-Korrektur nannte
auch die GitHub-PR-Beschreibung noch den alten Head, bezeichnete den PR als
Draft, bestritt einen Merge und sagte laufende Checks. Der exakte Head ist
bereits gepusht und der aktuelle Benutzer hat die Framework-only-Integration
von PR #37 ausdrücklich autorisiert. Der korrigierte Head wurde normal als
Framework-master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` gemergt. Das ist
ein Wahrheits- und Release-Readiness-Defekt, kein Product-Exploit.

## Beobachtetes und erwartetes Verhalten

Bei `c1523a8f51b2647228dea44284fa8d4a7ac38710` verbieten sowohl
`reports/audits/change-records/20260720-03-reconcile-codex-cloud-framework-security.md`
als auch der deutsche Companion einen Merge. Der erwartete Record bewahrt den
historischen Draft-PR-Kontext, erhält das Verbot eines direkten
`master`-Push und stellt klar, dass ein Merge nur über den aktuell ausdrücklich
autorisierten PR-Workflow nach frischer Exact-Head-Validierung möglich ist.
Die GitHub-PR-Beschreibung muss gleichwertig den aktuellen Head
`1e9fa0d22639517193d450b05eb7b07193e41257`, abgeschlossene Checks und
dasselbe bedingte Delivery-Modell nennen. Auf resultierendem Master
`f73f8842f45318e2df8aff1d31855eeb7c20a22f` fehlen die ursprünglichen
veralteten Aussagen (`Allow no master merge` / `the PR must remain unmerged`
und ihre deutschen Entsprechungen), während das direkte-`master`-Push-Verbot
erhalten bleibt.

## Auswirkung, Root Cause und Behebung

Dies war ein P1-Framework-Release-Blocker, weil eine geschützte, autorisierte
Integration der versionierten Traceability-Evidence widersprechen würde. Die
Root Cause war eine als dauerhafte Regel fortgeführte historische
Draft-PR-Beschränkung. Die fokussierte Behebung aktualisierte nur die gepaarten
Change-Record-Aussagen und bestand danach Dokumentations-, Security-,
Exact-Head-Hosted-, Protected-Merge- und Post-Merge-Formulierungsprüfungen.
Der unabhängige Default-Branch-SonarCloud-Quality-Gate-Fehler wird getrennt
als `FND-SONAR-0002` verfolgt.

## Evidence und Reproduktion

- Run: `20260721T060210Z-framework-pr-37-master-integration-6be553a4`
- Evidence: `analysis/pr37-stale-change-record-evidence.md` und
  `analysis/pr37-stale-pr-description-evidence.md`
- SHA-256: `9c6c842aa3a1658733ffc7ba4154478233690b07c4fb00c8bff5b6adb15208d4` und
  `b10f04784dba50f3c9a99b79615d7a3126107b8069cb2d10c6f78285baf205b7`
- Befehl: RTK-wrapped GitHub-PR-Metadaten-/Check-Review und Exact-Head-
  Change-Record-Inspektion, Exit `0`.
- Post-Merge-Evidence: `analysis/postmerge-master-sonar-triage.md`, SHA-256
  `a9a312f1ba760030ceb45644ced6b0d533fe01b9a4d2f8e19c1e832dc54b5830`.
- Sie erfasst den normalen Merge des exakten Source-Heads `1e9fa0d…` als
  Master `f73f884…`, bestandene PR-Head-Dokumentations-/Security-/Hosted-
  Controls, fehlende ursprüngliche veraltete Formulierungen auf Master und
  erhaltene Direct-Push-Schutzkontrollen.

Die gepaarten Records bei der festgehaltenen Revision und die
Pre-Correction-PR-Beschreibung inspizieren und ihre No-Merge-Aussagen mit der
aktuellen Benutzeranfrage vergleichen. Die retained Evidence enthält die exakt
betroffenen Aussagen und den beobachteten Delivery-Status.

## Akzeptanz und Validierung

- Englische und deutsche Delivery-Aussagen bleiben gleichwertig und wahr.
- Die GitHub-PR-Beschreibung nennt den aktuellen Head und berichtet Scope,
  abgeschlossene Checks und die bedingte Protected-Delivery-Regel korrekt.
- Direkte `master`-Pushes bleiben verboten; der Record selbst ist niemals
  Merge-Autorität.
- Der normale Merge verwendete frische Exact-Head-Checks, Sonar, Reviews und
  die aktuelle ausdrückliche Benutzerautorisierung.
- Dokumentations- und Whitespace-Checks, die fokussierte Framework-Security- /
  Regressionsmenge, Exact-Head-Hosted-Checks und die resulting-master-
  Formulierungsverifikation bestanden.

Die legitime Kontrolle ist, dass der überarbeitete Record direkte
`master`-Pushes und Bypässe weiterhin verbietet. Der Bypass-Review bestätigt,
dass die Formulierung weder Schutzmaßnahmen schwächt noch Delivery selbst
autorisiert. Es sind keine Dependency, Parent-Änderung oder MRTS-Aktion nötig.

## Restrisiko und Historie

Dieses Finding ist verified und kein Release-Blocker mehr. `FND-SONAR-0002`
bleibt der getrennte P1-Default-Branch-SonarCloud-Blocker: Sein Master-only-
Fehler reproduziert den veralteten Change-Record-Defekt nicht und eröffnet
dieses Finding nicht erneut.

- `2026-07-21T06:02:10Z`: `delivery_record_drift_confirmed` — gepaarte
  PR-#37-Records widersprechen der aktuellen Framework-only-master-Autorisation.
- `2026-07-21T07:01:09Z`: `delivery_metadata_drift_confirmed_and_corrected` —
  die veraltete PR-Beschreibung wurde ohne Änderung des PR-Source-Heads ersetzt.
- `2026-07-21T07:28:49Z`: `verified_after_pr37_normal_merge_and_scoped_reproduction` —
  exakter Source `1e9fa0d…` mergte normal als `f73f884…`; die ursprünglichen
  veralteten Aussagen fehlen auf Master und die Direct-Push-Kontrolle bleibt.
