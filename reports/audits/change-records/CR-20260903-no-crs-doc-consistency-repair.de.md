# Change Record CR-20260903-no-crs-doc-consistency-repair

**Sprache:** [English](CR-20260903-no-crs-doc-consistency-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260903-no-crs-doc-consistency-repair |
| Datum (UTC) | 2026-09-03 |
| Basis-Revision | d50fad793a8af1fa4cf0dc83a951c041dcd940e9 |
| Delivery-Status | In Bearbeitung in einem eigenen Parent-Worktree. Die ursprüngliche Benutzeranfrage autorisiert einen normalen PR, aber dieser Record behauptet keinen Commit, Push, PR, Hosted-Result, SonarCloud-Result oder Merge. |

## Motivation und Problemstellung

Fünf `master`-Workflows an der Basisrevision
`d50fad793a8af1fa4cf0dc83a951c041dcd940e9` endeten in
`ci/checks/documentation/check-no-crs-doc-consistency.py`. Das kanonische
Traefik-Manifest beschrieb den begrenzten `forwardAuth`-Phase-2-Pfad bereits
als `configured_not_exercised`, aber der eingecheckte erzeugte Katalog war
veraltet und den gekoppelten TODOs fehlte die von diesem Konsistenz-Control
erwartete Legacy-Grenze `request_body_mode=none`.

## Akzeptanzkriterien

- Beide Traefik-TODO-Dateien behalten die exakte Legacy-
  Kompatibilitätsgrenze `request_body_mode=none` bei und beschreiben den
  ausgewählten Pfad als gepuffert.
- Der unterstützte Generator aktualisiert alle drei versionierten
  Capability-Katalog-Ausgaben und weist für Traefik `request_body_buffered`
  und `phase2` als `configured_not_exercised` aus.
- `make check-no-crs-doc-consistency` und fokussierte Traefik-/Bilingual-
  Controls bestehen ohne Runtime-Promotion oder Request-Body-Streaming.
- Vor der Auslieferung wird ein versiegelter Codex-Security-Review abgeschlossen.

## Implementierungsentscheidung und Begründung

Diese Parent-only-Reparatur ändert das englische/deutsche TODO-Paar und führt
den unterstützten Generator `make capabilities-all-connectors` erneut aus. Sie
bearbeitet keine erzeugte Ausgabe von Hand, ändert keinen Runtime-Sourcecode,
keine CI-Berechtigungen, schwächt den Konsistenzcheck nicht, verändert
`modules/ModSecurity-test-Framework` nicht und aktualisiert keinen Gitlink.
Die vollständige Katalogaktualisierung ist beabsichtigt: Die vorherige Version
wurde aus älteren Capability-Manifest-Inputs erzeugt, daher aktualisiert der
Generator sämtliche aktuellen Connector-Einträge als ein Source-of-Truth-
Artefakt.

Ein unabhängiges Source-Review stellte fest, dass der frühere Capability-Text
eine Auslassung des Response Observers durch einen Betreiber zu weitgehend
beschrieb. Das eingecheckte Dynamic-Profil und sein Source-Contract-Test
verlangen die Reihenfolge `forwardAuth` zu Response Observer. Das kanonische
Manifest wird deshalb auf dieses eingecheckte Profil eingegrenzt und markiert
einen ausgelassenen oder umgeordneten Observer wahrheitsgemäß als
Out-of-Profile-Deployment-Änderung, die separate P3/P4-Validierung benötigt.
Dies ändert nur die Metadatenformulierung, nicht die Runtime-Kette.

## Security-Auswirkung

Die betroffene Grenze ist die Integrität von Repository- und CI-Metadaten. Die
Reparatur bewahrt `request_body_mode=buffered`, behält
`request_body_mode=none` ausschließlich für den Legacy-Kompatibilitätspfad
ohne Request-Body, lässt Request-Body-Streaming
`unsupported_by_host_model` und behauptet keine echte Host-Phase-2-Evidence.
Sie ändert weder Request-Parser noch Listener, Autorisierungsregel, Secret,
Dependency oder Workflow-Berechtigung.

## Geänderte Dateien

- `connectors/traefik/TODO.md`
- `connectors/traefik/TODO.de.md`
- `connectors/traefik/capabilities.json`
- `reports/testing/generated/canonical/connector-capabilities.generated.json`
- `reports/testing/generated/canonical/connector-capabilities.generated.md`
- `reports/testing/generated/canonical/connector-capabilities.generated.de.md`
- `reports/audits/change-records/CR-20260903-no-crs-doc-consistency-repair.md`
- `reports/audits/change-records/CR-20260903-no-crs-doc-consistency-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

- `rtk proxy make capabilities-all-connectors` — bestanden;
  `connector_capabilities: ok connectors=6 capabilities=60`.
- `rtk proxy make check-no-crs-doc-consistency` — bestanden.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_connector_capabilities tests.test_traefik_forwardauth_p2_contract tests.test_traefik_runtime_smoke_security tests.test_bilingual_docs` — bestanden, 62 Tests.
- Nach der Klärung der Response-Observer-Formulierung bestanden
  `rtk proxy make capabilities-all-connectors` und
  `rtk proxy make check-no-crs-doc-consistency`.
- Derselbe fokussierte 62-Test-Befehl bestand nach der Klärung, einschließlich
  `test_forwardauth_runtime_chain_requires_the_private_response_observer`.
- `rtk proxy make check-bilingual-docs` — nur durch 20 vorbestehende fehlende
  Framework-Gitlink-Targets blockiert; kein aufgaben-eigener Change-Record-
  Fehler wurde gemeldet.
- `rtk proxy make check-doc-links` — nur durch dieselben fehlenden Framework-
  Targets blockiert.
- `rtk proxy git diff --check` — bestanden.

## Runtime-Evidence

Es wurde keine Connector-Runtime gestartet. Diese Reparatur stellt nur die
statische Dokumentations- und Generator-Konsistenz wieder her; sie ist keine
echte Host-Phase-2-, Over-Limit-, Response- oder CRS-Evidence und stuft keine
Capability hoch.

## Nicht ausgeführte Prüfungen mit Begründung

Die vollständigen Bilingual- und Link-Checks können nicht abschließen, weil der
ausgewählte Worktree die von ihrer Ausgabe benannten Framework-Gitlink-Targets
nicht enthält. Keine Framework-Initialisierung oder -Änderung ist autorisiert.
Ein versiegelter Codex-Security-Diff-Scan deckt diesen Produkt-Snapshot ab.
Commit-, Pull-Request-, gehostete Workflow- und PR-spezifische SonarCloud-
Evidence sind davon getrennte Delivery-Evidence und werden nicht durch die
obigen lokalen Controls behauptet.

## Bekannte Einschränkungen

Die Katalogaktualisierung enthält korrekt aktuelle Manifeständerungen auch
außerhalb von Traefik, weil es sich um ein gemeinsames repository-weites
erzeugtes Artefakt handelt. Die Aufgabe behebt nicht die fünf historischen
offenen SonarCloud-Issues auf `master`, darunter einen Framework-eigenen Pfad
außerhalb dieser Parent-only-Autorität.

## Verbleibende Risiken

Die gepufferte Phase-2-Route bleibt `configured_not_exercised`, bis frische
echte Host-Allow-, Deny- und Over-Limit-Evidence vorhanden ist. Request-Body-
Streaming bleibt `unsupported_by_host_model`. Die Reparatur benötigt vor jeder
Integrationsentscheidung weiterhin Exact-Head-CI- und SonarCloud-Evidence. Ein
Betreiber, der den Response Observer auslässt oder umordnet, ändert das
ausgewählte Profil und muss P3/P4 separat validieren; dieser Record behauptet
nicht, dass eine Out-of-Profile-Deployment-Konfiguration fail-closed ist.

## Finaler Diff- und Review-Status

In Bearbeitung. Der aktuelle Benutzer autorisierte unter der ursprünglichen
Failed-Workflow-Anfrage eine Parent-only-Reparatur in einem eigenen Worktree
und einen normalen PR. Dieser Record dokumentiert lokale
Remediation-Entscheidungen; er begründet selbst keinen Commit, Push, Pull
Request, Hosted-Result, SonarCloud-Result oder Merge.
