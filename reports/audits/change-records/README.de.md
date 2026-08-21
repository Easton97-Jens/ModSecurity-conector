# Change-Record-Archiv

**Sprache:** [English](README.md) | Deutsch

`reports/audits/change-records/` bleibt als Archivplatzhalter erhalten.
Einzelne historische Change-Record-Berichte werden im aktuellen Repository-Baum
nicht mehr gepflegt. Historische Änderungen bleiben über die Git-Historie,
Commits und Pull Requests nachvollziehbar. Neue Einzelberichte dürfen nur nach
einer ausdrücklichen Repository-Policy-Entscheidung oder Benutzerentscheidung
angelegt werden.

## Ausdrücklich autorisierte Records

- [CR-20260820-full-matrix-evidence-selector](CR-20260820-full-matrix-evidence-selector.de.md) —
  der aktuelle Benutzer hat die Parent-only-`AUDIT_AND_FIX`-Reparatur, ihren
  gekoppelten Change Record und später einen Parent-Draft-PR ausdrücklich
  autorisiert; keine Framework-Source-Änderung ist autorisiert. Der Record
  weist nur beobachtete lokale Evidence aus; Hosted-Ergebnisse und ein Merge
  werden nicht behauptet.

- [CR-20260819-fnd-parent-0185-crs-provenance-exports](CR-20260819-fnd-parent-0185-crs-provenance-exports.de.md) —
  der aktuelle Benutzer hat diese Parent-only-Reparatur und einen Draft-PR
  autorisiert und Framework-Moduländerungen ausdrücklich untersagt. Die
  Hosted-Checks des Implementierungs-Heads bestanden; der vom Benutzer
  autorisierte geschützte Merge und die Post-Merge-Verifikation folgen dem
  geschützten Delivery-Lifecycle.

- [CR-20260819-readonly-submodule-sandbox-preservation](CR-20260819-readonly-submodule-sandbox-preservation.de.md) —
  der aktuelle Benutzer hat diese Parent-only-Sandbox-Reparatur zur
  Source-Preservation, die gepaarte Nachvollziehbarkeit und Draft PR
  [#302](https://github.com/Easton97-Jens/ModSecurity-conector/pull/302)
  ausdrücklich autorisiert. Der Record weist nur beobachtete lokale Evidence
  aus; weder Framework-Änderung, Gitlink-Update, Hosted-Ergebnis,
  Ready-for-Review-Status noch Merge werden behauptet.

- [CR-20260818-framework-component-resolver](CR-20260818-framework-component-resolver.de.md) —
  der aktuelle Benutzer hat diese Parent-only-Reparatur des statischen
  Resolvers und die gepaarte Nachvollziehbarkeit sowie anschließend ausdrücklich
  einen Parent-Draft-PR autorisiert. Der Record
  weist nur beobachtete lokale Validierung aus; weder Framework-Änderung,
  Gitlink-Update, Hosted-Rerun, finaler Delivery-Identifier noch Merge werden
  behauptet.

- [CR-20260816-python-updater-publisher-dependency](CR-20260816-python-updater-publisher-dependency.de.md) —
  der aktuelle Benutzer hat die fokussierte Parent-CI-Fehlerbehebung und die
  Draft-PR-Auslieferung autorisiert. Dieser gekoppelte Record weist nur
  beobachtete lokale Validierung aus; gehostete Pull-Request-Checks und die
  absichtlich an `master` gebundene Ende-zu-Ende-Ausführung des Publishers
  stehen noch aus.

- [CR-20260816-python-workflow-contract-alignment](CR-20260816-python-workflow-contract-alignment.de.md) —
  der aktuelle Benutzer hat die fokussierte Parent-Reparatur, den Sonar-
  Follow-up von PR #296 und die bedingte geschützte `master`-Integration für
  den verlinkten Actions-Contract-Fehler autorisiert. Der gekoppelte Record
  unterscheidet beobachteten lokalen Nachweis von ausstehender Successor-Head-
  Hosted- und Resulting-Master-Evidence und behauptet keinen Merge vorab.

- [CR-20260815-python-updater-framework-port](CR-20260815-python-updater-framework-port.de.md) —
  der aktuelle Benutzer hat den eingeschränkten Parent-Python-Updater-Port und
  die Draft-PR-Auslieferung autorisiert. Dieser gekoppelte Record weist nur
  beobachtete lokale Validierung aus; Hosted-Ausführung, Delivery-Checks und
  Merge werden nicht behauptet.

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
