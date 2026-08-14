# Change-Record-Archiv

**Sprache:** [English](README.md) | Deutsch

`reports/audits/change-records/` bleibt als Archivplatzhalter erhalten.
Einzelne historische Change-Record-Berichte werden im aktuellen Repository-Baum
nicht mehr gepflegt. Historische Änderungen bleiben über die Git-Historie,
Commits und Pull Requests nachvollziehbar. Neue Einzelberichte dürfen nur nach
einer ausdrücklichen Repository-Policy-Entscheidung oder Benutzerentscheidung
angelegt werden.

## Ausdrücklich autorisierte Records

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
- [CR-20260814-f-gs-006-http-authorization-admission](CR-20260814-f-gs-006-http-authorization-admission.de.md) —
  der aktuelle Benutzer hat diesen gepaarten Parent-Security-Hardening-Record
  und einen Draft-PR autorisiert. Er weist nur beobachtete lokale Validierung
  aus; Host-Runtime, Hosted-Ausführung und Delivery-Checks werden nicht
  behauptet.
