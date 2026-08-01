# FND-SONAR-0017 — MRTS-PR #4 beseitigt alle aufgabeneigenen SonarCloud-Issues auf dem gemergten main

## Klassifikation

ID: FND-SONAR-0017
Kategorie: sonarqube_finding
Repository: mrts
Ownership: mrts_explicit_user_task
Priorität: P1
Schweregrad: not_applicable
Konfidenz: validated
Status: closed (archiviert)
Release-Blocker: nein
Security relevant: ja
Verification-Status: verified_merged_main_hosted_sonar_zero
Remediation-Status: closed_verified_merged_main_hosted_sonar_zero

## Zusammenfassung und Verhalten

Die 12-Elemente-MRTS-SonarCloud-Basis wurde ohne Änderung von
Scanner-Kontrollen remediated. Der exakte PR-#4-Source-Head
9cdfd4136286014b244f8fecfb99701681fecae4 wurde Head-geschützt als Squash nach
`main` 615b13bacbd008562c17408246c41ab27dca3104 gemergt. Das resultierende
`main` hat 0 offene SonarCloud-Issues, Quality Gate OK, erfolgreiche Workflows
Push on main, Python governance und CodeQL sowie keinen offenen CodeQL-Alarm.

Basis-Issues waren sieben python:S5778, zwei python:S1172, zwei python:S3776
und ein pythonsecurity:S8705. Die erste PR-Analyse führte ein
python:S1192-Duplicate-Literal-Issue in mrts/mrts.py:66 ein;
GO_FTW_CONFIGURATION entfernte es ohne Verhaltensänderung. Sowohl die exakte
PR- als auch die Resulting-Main-Abfrage liefern total 0.

Erwartetes Verhalten sind null offene aufgabeneigene Issues und ein
OK-Quality-Gate auf der gemergten Main-Revision ohne Regel-, Gate-, Exclusion-,
False-Positive-, NOSONAR-, Suppressions- oder Security-Control-Änderungen.

## Auswirkung, Scope und Reproduktion

Der Nutzer verlangte null Issues vor der Main-Integration. PR #4 wurde danach
mit der gewählten geschützten Squash-Methode gemergt und die Resulting-Main-
Verifikation besteht. Betroffene Dateien sind mrts/mrts.py,
tools/test_mrts_path_utils.py, tools/test_validate_governance.py und
tools/validate-governance.py.

SonarCloud-Main-Issues mit componentKeys=Easton97-Jens_MRTS, branch=main,
resolved=false, ps=500 abfragen; Quality Gate mit projectKey=Easton97-Jens_MRTS
und branch=main abfragen; Merge-Status von PR #4, resultierenden Main-SHA,
Main-Workflow-Runs und CodeQL-Alarm-Liste prüfen.

## Evidenz

- sonar-pr-issues.json: SHA-256 ee8fdf86104a53c760e40f0d42b92b51d2c13f2e289efcb6b562dce9076f6a55, total 0.
- sonar-quality-gate.json: SHA-256 1db063f467b49ec05719b0f44b2c703bc402ae52f2515452169ddafbe4343c64, Quality Gate OK.
- pr-status.json: SHA-256 cf4ad16887f3e9723292215666e48e269c4a3a4f01b319024973e2915a4fa5a6, exakter Head und vier erfolgreiche Checks.
- local-validation.md: SHA-256 5fdc769af00f7c81b8839766bf6f65834b91278f65a55c00a2adc5677db743fd, 38 Tests, compileall und diff check bestanden.

- github-post-merge.json: SHA-256 6d77c474bdc6a8b9744dd3ac8e2b6c76195a47e47fb945caa75acb5173a1f936, geschützter Squash-Merge, resultierendes main, erfolgreiche Workflows, kein offener CodeQL-Alarm und unveränderte Gitlinks.
- sonar-main-issues.json: SHA-256 58cf67de638c7b544b279c8365ac3334eb279716faed0996d6fe439a6ac9ad58, total 0 auf main.
- sonar-main-quality-gate.json: SHA-256 0f88c3322a2a779ea067fcf61cbf21946c614836989b5f5d360f7c04f078e69b, Main-Quality-Gate OK.

Alle liegen aufbewahrt unter .codex/runs/20260726T101017Z-mrts-sonarcloud-zero-pr4.
Die Resulting-Main-Receipts sind unter
.codex/runs/20260726T105800Z-mrts-pr4-squash-merge versiegelt.

## Root Cause, Remediation und Validierung

Assertion-Call-Refactors, unbenutzte Argumente, kognitive Komplexität und ein
Scanner-Taint-Kandidat erforderten enge Source-/Test-Änderungen. Sink-lokale
Validierung erzeugte ein wiederholtes Literal, danach entfernte
GO_FTW_CONFIGURATION S1192. Feste go-ftw-argv, shell=False, Pfadvalidierung,
Fehlermeldungen und Governance-Prädikate bleiben bewahrt. Keine
Scanner-Kontrolle wurde geändert.

Akzeptanz: Das resultierende main hat 0 Issues; Quality Gate und alle
anwendbaren Main-Workflows sind grün; die fokussierte MRTS-Suite hat 38
erfolgreiche Tests; keine Suppression/Control-Abschwächung, kein direkter
Main-Push, keine Gitlink-Aktion und keine nicht autorisierte Cleanup-Löschung
traten auf.

Legitime Kontrollen belegen, dass Shell-ähnliche vorhandene Pfade einzelne
Popen-argv-Operanden mit shell=False bleiben, die Default-Konfiguration
akzeptiert wird, fehlende Inputs vor Popen fehlschlagen und Governance-
Negativkontrollen erwartete Fehler bewahren.

## Abhängigkeiten, Blocker, verwandte Findings, Restrisiko und Historie

Es gibt keine verbleibenden Remediation-Abhängigkeiten oder Blocker.
FND-SONAR-0012 ist verwandt, hat aber einen anderen PR und eine andere Root
Cause. Der gemergte Remote-Branch und das saubere Task-Worktree bleiben
erhalten, weil keine Lösch-/Entfernungsaktion autorisiert wurde.

Keine vollständige go-ftw-Integration und kein Remote-Exploit werden
behauptet. Nachgelagerte Konfigurationssemantik und PATH-Trust bleiben getrennt.

- 2026-07-26T09:00:00Z: Basis mit 12 Issues gemappt.
- 2026-07-26T10:02:19Z: erste PR-Analyse fand S1192; Konstantenextraktion
  statt Suppression gewählt.
- 2026-07-26T10:10:17Z: exakter Head mit 0 Issues, Quality Gate OK und vier
  erfolgreichen Checks verifiziert.
- 2026-07-26T10:55:25Z: Exact-Head-geschützter Squash-Merge erzeugte main
  615b13bacbd008562c17408246c41ab27dca3104.
- 2026-07-26T10:58:00Z: alle Resulting-Main-Workflows bestanden; Main-
  SonarCloud meldete 0 offene Issues und Quality Gate OK; kein offener CodeQL-
  Alarm existiert.

Final disposition: closed_verified_merged_main_hosted_sonar_zero
