# FND-FRAMEWORK-0038 — Fallback-YAML-Parser klassifizierte nach der geprüften Python-Migration Klartext-Listenskalare mit Doppelpunkt falsch

Der geprüfte Python-3.13-Runner von PR #39 verwendete in `test-common` den
abhängigkeitsfreien Fallback-YAML-Parser, weil PyYAML nicht installiert war.
Dieser Parser interpretierte jeden Doppelpunkt in einem Listenskalaren als
Mapping-Separator, wandelte die gültige Einschränkung `ARGS:foo.` in ein Dict
um und ließ die Case-Validierung scheitern. Dies ist ein durch die geforderte
Migration sichtbar gewordener P1/non-security-Exact-Head-Blocker.

Die enge Reparatur erkennt ein Inline-Mapping nur bei einem Doppelpunkt mit
folgendem Whitespace oder Wertende. Die Regression muss beweisen, dass
`ARGS:foo.` ein String bleibt und den vorhandenen
`- name: Content-Type`-Mapping-Control erhalten. Fokussierte Parser- und
Common-Structure-Checks, reale Fallback-Parser-Materialisierung, die
vollständige native Lint-Suite und der versiegelte Follow-up-Security-Diff-Scan
bestehen jetzt. Das Finding ist lokal `fixed`; frische gehostete
Exact-Current-Head-Evidenz ist vor einer verifizierten Delivery-Disposition
weiterhin nötig.

## Validierung und Historie

- Der frühere Fehler ist im GitHub-Actions-Run `29774954997`, Job
  `88461999826`, aufbewahrt; das gültige Element `ARGS:foo.` wurde als Dict
  geparst.
- Das verfeinerte Separator-Prädikat erhielt sowohl `ARGS:foo.` als Skalar als
  auch das legitime Inline-Mapping `name: Content-Type` in fokussierten Tests
  und in der realen test-common-CLI-Materialisierung.
- Der versiegelte Follow-up-Scan-Report ist
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T180337Z-framework-python-313-updater-f3349a7e/analysis/codex-security-scans/ModSecurity-test-Framework/4a31df0_remediation_followup_20260720T210011Z/report.md`
  mit SHA-256 `be92a7e65c3c81e72140b5441494eb4461df4417ee361c344bd3d0cf56775a5c`.
- 2026-07-20T21:12:33Z — Status nach lokaler Parser-, Workflow- und
  Security-Validierung auf `fixed` gesetzt. Der remediierte Commit benötigt
  noch aktuelle gehostete Head-Common-Structure- und übrige PR-Gates; kein
  Merge, Parent-Gitlink-Update oder MRTS-Aktion ist autorisiert.
