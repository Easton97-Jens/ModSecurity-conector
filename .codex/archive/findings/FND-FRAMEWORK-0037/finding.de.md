# FND-FRAMEWORK-0037 — Python-Wartungsworkflow verwendete nicht unterstützten jobweiten Runner-Kontext und nicht annotiertes literales Markdown

Das Exact-Head-Workflow-Lint für Framework-PR #39 wies `runner.temp` im
jobweiten `env` des neuen Kandidatenjobs zurück, weil `runner` in diesem Scope
nicht verfügbar ist. Zusätzlich meldete es SC2016 für beabsichtigte
Markdown-Backticks im einfach quotierten Draft-PR-Body. Dies ist ein
deterministischer P1/non-security-Delivery-Blocker, keine Berechtigungs- oder
Token-Exposition.

Die Reparatur behält nur den Kandidaten auf Job-Ebene, initialisiert die festen
Runner-Pfade zur Step-Laufzeit über `$GITHUB_ENV` und unterdrückt SC2016 eng
direkt vor dem literalen `printf`. Alle vorhandenen Read/Write-Isolationen,
immutable Pins, Schedule/Manual-Gates und Draft-only-Publikation müssen
erhalten bleiben. Lokale Workflow-/Contract-Checks, die vollständige native
Lint-Suite und der versiegelte 11-Dateien-Security-Diff-Scan bestehen jetzt.
Das Finding ist lokal `fixed`; ein frischer Exact-Current-Head-gehosteter
Workflow-Lint-Run und die übrigen PR-Gates sind vor einer verifizierten
Delivery-Disposition weiterhin nötig.

## Validierung und Historie

- Der frühere Fehler ist im GitHub-Actions-Run `29774954611`, Job
  `88461998115`, aufbewahrt; er meldete den nicht unterstützten jobweiten
  Kontext und SC2016.
- Die Reparatur bestand 36 fokussierte Tests, 85 CI-Security-Tests,
  `make check-github-actions-workflows`, `make test-workflow-contract`,
  `make check-documentation`, vollständiges natives `make lint` und
  `git diff --check`.
- Der versiegelte Follow-up-Scan-Report ist
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T180337Z-framework-python-313-updater-f3349a7e/analysis/codex-security-scans/ModSecurity-test-Framework/4a31df0_remediation_followup_20260720T210011Z/report.md`
  mit SHA-256 `be92a7e65c3c81e72140b5441494eb4461df4417ee361c344bd3d0cf56775a5c`.
- 2026-07-20T21:12:33Z — Status nach lokaler Regressions-, Workflow- und
  Security-Validierung auf `fixed` gesetzt. Der remediierte Commit muss noch
  aktuelle gehostete Head-Actions bestehen; kein Merge, Parent-Gitlink-Update
  oder MRTS-Aktion ist autorisiert.
