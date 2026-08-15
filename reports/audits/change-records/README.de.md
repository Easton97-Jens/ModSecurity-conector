# Change-Record-Archiv

**Sprache:** [English](README.md) | Deutsch

`reports/audits/change-records/` bleibt als Archivplatzhalter erhalten.
Einzelne historische Change-Record-Berichte werden im aktuellen Repository-Baum
nicht mehr gepflegt. Historische Änderungen bleiben über die Git-Historie,
Commits und Pull Requests nachvollziehbar. Neue Einzelberichte dürfen nur nach
einer ausdrücklichen Repository-Policy-Entscheidung oder Benutzerentscheidung
angelegt werden.

## Ausdrücklich autorisierte Records

- [CR-20260815-framework-version-pin-updater-sync](CR-20260815-framework-version-pin-updater-sync.de.md) —
  der aktuelle Benutzer hat die Vorbereitung der Framework-zentralen
  Synchronisationsänderung und ihrer PR-Auslieferung autorisiert. Dieser
  Record weist nur beobachtete lokale Validierung aus; Commit, Push, PR,
  Hosted-Checks und Merge werden hier nicht behauptet.

- [CR-20260814-f-gs-004-hostruntime-p0](CR-20260814-f-gs-004-hostruntime-p0.de.md) —
  der Benutzer hat den abhängigen Draft-PR autorisiert; Delivery- und
  Nachvollziehbarkeitsrichtlinien verlangen diesen gepaarten Parent-Record.
  Er weist nur beobachtete lokale Validierung aus; Hosted-Ausführung,
  PR-Checks und Framework-Merge bleiben ausstehend.

- [CR-20260811-enforce-readonly-submodule-validator](CR-20260811-enforce-readonly-submodule-validator.de.md) —
  dieses Paar ist für die Änderung am schreibgeschützten
  Framework-Submodule-Validator ausdrücklich autorisiert. Es weist nur
  beobachtete Validierung aus; Hosted-Ausführungs- und Security-Scan-Evidence
  werden nicht behauptet.
- [CR-20260813-framework-apr-util-submodule-validation](CR-20260813-framework-apr-util-submodule-validation.de.md) —
  der Benutzer hat einen Draft-PR autorisiert; Delivery- und
  Nachvollziehbarkeitsrichtlinien des Repositorys verlangen diesen gepaarten
  Record für die Parent-Änderung. Er weist nur beobachtete lokale Validierung
  aus; Hosted-Ausführung, PR-Checks und Cross-Repository-Delivery werden nicht
  behauptet.
- [CR-20260814-f-gs-002-lighttpd-autogen-bootstrap](CR-20260814-f-gs-002-lighttpd-autogen-bootstrap.de.md) —
  der aktuelle Benutzer hat den Abschluss und die geschützte Auslieferung des
  F-GS-002-Parent-Build-Fix ausdrücklich autorisiert. Dieser gepaarte Record
  bewahrt die beobachtete offizielle Quelle sowie Fresh-/Core-/Host-/Reuse-,
  Quellenerhaltungs- und Pre-Merge-Evidenz; das Ergebnis des geschützten Merge
  wird nicht vorab behauptet.
- [CR-20260814-f-gs-006-http-authorization-admission](CR-20260814-f-gs-006-http-authorization-admission.de.md) —
  der aktuelle Benutzer hat diesen gepaarten Parent-Security-Hardening-Record
  und einen Draft-PR autorisiert. Er weist nur beobachtete lokale Validierung
  aus; Host-Runtime, Hosted-Ausführung und Delivery-Checks werden nicht
  behauptet.
- [CR-20260814-locked-ci-test-dependencies](CR-20260814-locked-ci-test-dependencies.de.md) —
  der aktuelle Benutzer hat die verpflichtende Dokumentation bedingt
  autorisiert, und die Traceability-Policy verlangt dieses Paar für den
  Parent-CI-Bugfix. Es weist nur beobachtete lokale Validierung aus; weder ein
  Hosted-Rerun noch Delivery werden behauptet.
