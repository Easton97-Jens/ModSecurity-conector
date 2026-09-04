# Change-Record-Archiv

**Sprache:** [English](README.md) | Deutsch

`reports/audits/change-records/` bleibt als Archivplatzhalter erhalten.
Einzelne historische Change-Record-Berichte werden im aktuellen Repository-Baum
nicht mehr gepflegt. Historische Änderungen bleiben über die Git-Historie,
Commits und Pull Requests nachvollziehbar. Neue Einzelberichte dürfen nur nach
einer ausdrücklichen Repository-Policy-Entscheidung oder Benutzerentscheidung
angelegt werden.

## Ausdrücklich autorisierte Records

- [CR-20260904-protected-base-exact-head-nginx](CR-20260904-protected-base-exact-head-nginx.de.md) |
  [English](CR-20260904-protected-base-exact-head-nginx.md) — Vorbereitung
  eines geschützten Base-Dispatchers, privilegierten Launchers und unabhängigen
  Collectors für NGINX-Exact-Head-Evidence. Geschützte Environment und
  dedizierter Runner fehlen weiterhin; kein Hosted-Ergebnis und kein Merge
  werden behauptet. Ausschließlich Vorbereitung — keine Merge-Autorisierung.

- [CR-20260824-connector-security-invariants](CR-20260824-connector-security-invariants.de.md)
  | English companion: `CR-20260824-connector-security-invariants.md` — das
  Parent-only-Connector-Security-Hardening hält lokale Remote-Rule-, HTTP-
  Grenz- und Event-Runtime-Evidence fest. Es schließt Framework/MRTS, Gitlink,
  CI/Governance und gemischte gleichzeitige Edits aus; Remote-Delivery wartet
  auf eine explizite Autorisierung des aktuellen Benutzers, und Hosted-Checks
  sowie ein Merge werden nicht behauptet.
- [CR-20260903-no-crs-doc-consistency-repair](CR-20260903-no-crs-doc-consistency-repair.de.md) —
  der aktuelle Benutzer autorisierte diese Parent-only-Reparatur des
  reproduzierten Traefik-No-CRS-Dokumentations-/Capability-Katalog-
  Konsistenzfehlers in einem eigenen Worktree und einen normalen PR. Sie
  bewahrt den begrenzten, nicht hochgestuften P2-Zustand und nicht
  unterstütztes Request-Body-Streaming; keine Framework-/MRTS-Source,
  Gitlink-, Workflow-Berechtigungs-, Sonar-Control- oder Merge-Änderung wird
  behauptet.

- [CR-20260902-nginx-workflow-contract-repair](CR-20260902-nginx-workflow-contract-repair.de.md) —
  der aktuelle Benutzer autorisierte diese Parent-only-Reparatur eines
  reproduzierten NGINX-Source-Contract-Checker-Fehlers in einem eigenen
  Worktree und einen Draft PR. Die erforderliche Codex-Security-Arbeit
  identifizierte und ergänzte anschließend die enge Envoy-grpc-go-High-Severity-
  Dependency-Remediation. Der Record bewahrt die laufenden Once-only-Mapper-,
  Phase-4-Scope- und Common-Body-Limit-Assertions; er ändert weder NGINX-
  Runtime-Source, Workflows, Framework/MRTS, Gitlinks, Sonar-Controls noch
  Merge-Status.

- [CR-20260825-fnd-parent-0221-composite-connectors](CR-20260825-fnd-parent-0221-composite-connectors.de.md) —
  der aktuelle Benutzer autorisierte eine Parent-only-Composite-
  Korrelationsimplementierung, gekoppelte Nachvollziehbarkeit, scoped
  Commit/Push und einen Draft-PR. Der Record hält aktuelle lokale und
  Real-H1-Evidenz fest, belässt `FND-PARENT-0221` aber wahrheitsgemäß
  release-blockierend und P4 Strict, Duplicate/Cancel, Same-Process-Traefik-
  Follow-up, H2/H3 und Paritäts-Evidenz offen; kein Merge ist autorisiert oder
  behauptet.

- [CR-20260824-canonical-runtime-observation](CR-20260824-canonical-runtime-observation.de.md) —
  der aktuelle Benutzer autorisierte diesen Parent-only Canonical-Runtime-
  Observation-Vertrag, Safe-Evidence-Reader-Hardening, gekoppelte Traceability
  und einen unabhängigen Draft PR. Der Record hält nur beobachtete lokale
  Evidence fest; keine Framework-/MRTS-Source, kein Gitlink, Workflow,
  geschützte NGINX-Grenze, Hosted-Result, Ready-Status oder Merge wird
  behauptet.

- [CR-20260825-shared-transaction-phase-contract](CR-20260825-shared-transaction-phase-contract.de.md) —
  der aktuelle Benutzer hat ausdrücklich einen Parent-Draft-PR für den
  gemeinsamen Transaktions-Phasenvertrag autorisiert. Der Record unterscheidet
  lokale Komponentenvalidierung von nicht ausgeführter Real-Host-/Hosted-
  Evidence und erhält die offenen P0/P1-Findings; kein Merge, keine
  CI-Scope-Änderung, keine Framework-/MRTS- oder Gitlink-Aktion wird
  behauptet.

- [CR-20260825-lighttpd-phase2-pre-upstream-gate](CR-20260825-lighttpd-phase2-pre-upstream-gate.de.md) —
  das vom Benutzer autorisierte Parent-only-Phase-2-Pre-Upstream-Zulassungsgate
  für den ausgewählten gepatchten Lighttpd-HTTP/1.1-`mod_proxy`-Pfad. Es hält
  lokale Runtime-Evidence, den gemergten PR #339 als geerbte `master`-ABI-
  Basis und den Draft-PR—nicht einen Merge—als erlaubten Auslieferungsstatus
  fest.

- [CR-20260823-pr309-lighttpd-config-reference-repair](CR-20260823-pr309-lighttpd-config-reference-repair.de.md) —
  die Parent-only-Nachfolgereparatur stellt den geschlossenen Lighttpd-
  Config-Reference-Vertrag nach dem Post-Merge-Validierungsfehler von PR #309
  wieder her. Sie weist keine Framework-/MRTS-, Gitlink-, Runtime-Source-,
  Workflow- oder Quality-Control-Änderung aus und verlangt frische
  Successor-Head- und Resulting-Master-Evidence.

- [CR-20260822-trusted-lighttpd-namespace-dispatch](CR-20260822-trusted-lighttpd-namespace-dispatch.de.md) —
  der aktuelle Benutzer autorisierte eine separate Protected-master-
  `workflow_dispatch`-Grenze für den Lighttpd-Namespace-Test. Der Record weist
  nur lokale Contracts aus; Protected Merge und manueller Runtime-Lauf stehen
  noch aus.

- [CR-20260822-sonar-pr313-hostruntime-remediation](CR-20260822-sonar-pr313-hostruntime-remediation.de.md) —
  der aktuelle Benutzer autorisierte die Behebung von vier Parent-eigenen
  SonarCloud-Code-Smells aus PR #313 über einen Nachfolge-Draft-PR. Die
  historische #313-Analyse ist unveränderlich; der Record verlangt frische
  Sonar-Evidence des Successor-Heads mit null offenen New-Code-Issues und
  behauptet weder Framework-/MRTS-, Gitlink-, NGINX- noch Merge-Änderung.

- [CR-20260821-go-and-runtime-workflow-remediation](CR-20260821-go-and-runtime-workflow-remediation.de.md) —
  der aktuelle Benutzer autorisierte diese Parent-only-Go- und Runtime-
  Workflow-Remediation, das sichere Schließen der ersetzten PRs #306–#308, die
  gekoppelte Nachvollziehbarkeit und später einen nicht gemergten Draft-PR. Der
  Record unterscheidet lokale Evidence von ausstehenden Exact-Head-Hosted-
  Läufen und behauptet weder Framework-/MRTS-Änderung noch Merge.

- [CR-20260822-nginx-framework-updater-decoupling](CR-20260822-nginx-framework-updater-decoupling.de.md) —
  Der aktuelle Nutzer autorisierte die Trennung von NGINX vom allgemeinen
  Framework-Updater. Der geschützte NGINX-Broker bleibt auf der neuesten
  offiziell veröffentlichten Version `1.31.3`; kein Merge wird behauptet.

- [CR-20260821-parent-only-workflow-maintenance-bundle](CR-20260821-parent-only-workflow-maintenance-bundle.de.md) —
  der aktuelle Benutzer autorisierte einen Parent-only gebündelten
  Action-/Tool-Wartungsweg und eine kontrollierte #311-`master`-Integration,
  nachdem alle geschützten Delivery-Voraussetzungen bestehen. Der Record hält
  fest, dass keine Framework-/MRTS-Änderung und keine Aktion an
  Legacy-Dependabot-PRs autorisiert ist und kein Merge vorab erfolgt oder
  behauptet wird.

- [CR-20260821-github-workflow-hostruntime-consolidation](CR-20260821-github-workflow-hostruntime-consolidation.de.md) —
  der aktuelle Benutzer hat diese Parent-only-Workflow-Konsolidierung, die
  Updater-Reparatur, gekoppelte Traceability, einen Branch, einen Commit und
  einen nicht gemergten PR autorisiert. Der Record unterscheidet beobachtete
  lokale/Security-Evidence von ausstehenden Exact-Head-Hosted-Checks und
  behauptet weder Framework-Änderung noch Merge.

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
