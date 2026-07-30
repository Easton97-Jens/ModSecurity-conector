# Change Record: Parent-CI-Capability-State-Map-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-ci-capability-state-map-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-capability-state-map-deduplication` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` |
| Bewertete Source-Revision | Aktueller lokaler Task-Working-Tree-Diff von der Basis-Revision; der gerebasete Implementierungs-Commit ist `b25dcb4d487a648e019d323cdaef957aff342ce9`. Beim Schreiben dieses Records werden kein Push, Pull Request, Hosted Check oder Merge beansprucht. |
| Grenze | Ausschließlich Parent-`ci/evidence/collectors/connector_capabilities.py`, sein direkter Parent-Test, dieses englisch/deutsche Change-Record-Paar und gepaarte Change-Record-Indizes. Keine `.github/`-, `scripts/`-, Framework-, MRTS-, Gitlink-, Manifest-, Scanner-Konfigurations-, Quality-Gate-, Exclusion-, Suppression- oder Default-Branch-Änderung ist enthalten. |
| SonarQube-Cloud-Verknüpfung | Zielt auf den aktuellen doppelten Envoy-/Traefik-Host-Model-State-Block in `_validate_relationships()`. Die Änderung zentralisiert ausschließlich die gemeinsamen elf `unsupported_by_host_model`-State-Anforderungen und behält jede connector-spezifische Override bei. |

## Motivation und Problemstellung

Der Parent-CI-Capability-Collector enthält doppelte feste State-Zuweisungen
für die prä-Upstream-Host-Modelle Envoy `ext_authz` und Traefik `ForwardAuth`.
Diese Deklarationen sind ein fail-closed Contract: Eine Capability, die die
spätere Upstream-Response nicht beobachten kann, muss exakt
`unsupported_by_host_model` bleiben und nicht nur irgendeinen nicht-verifizierten
State tragen. Die Duplikation muss reduziert werden, ohne erwartete States
konfigurierbar zu machen oder den Ablehnungspfad zu schwächen.

## Implementierungsentscheidung und Begründung

`connector_capabilities.py` besitzt jetzt die gemeinsame Elf-Capability-
Response- und Phase-4-Map einmal. `MappingProxyType` macht diese gemeinsame
Map, jede Connector-Map und die äußere Connector-Zuordnung nach dem Import
unveränderlich. Envoy behält `request_body_buffered` und `phase2` als
`configured_not_exercised`; Traefik behält `request_body_buffered` und
`phase2` als `not_implemented` sowie seine separate
`request_body_streaming`-Anforderung. Die unveränderte Lighttpd-Map ist
ebenfalls als unveränderliche statische Map dargestellt, damit der vollständige
Policy-Owner während der Validierung nicht geändert werden kann.

Es wurden kein Validator-Parameter, keine CLI-Option, keine Environment-
Eingabe, keine aus dem Manifest abgeleitete Policy und keine dynamische
Dokumentations-URL eingeführt. `_validate_relationships()` verwendet weiterhin
die feste Map des ausgewählten Connectors, erzeugt den identischen Fehler
`host-model invariant requires ...` und behält die separate exakte
Traefik-ForwardAuth-Referenzprüfung.

## Akzeptanzkriterien

- Die gemeinsame Envoy-/Traefik-Elf-Capability-Response- und Phase-4-Map
  besitzt einen unveränderlichen Parent-Source-Owner; die exakten
  connector-spezifischen States bleiben verschieden.
- Jede Envoy- und Traefik-Host-Model-State-Mutation scheitert über den echten
  `validate_manifest()`-Pfad mit dem exakt erwarteten Host-Model-Fehler.
- Kanonische Envoy- und Traefik-Manifeste bleiben gültig, und das Entfernen der
  versionierten offiziellen ForwardAuth-Referenz scheitert fail-closed.
- Der exakte künftige Pull-Request-Head muss null neue SonarQube-Cloud-Issues,
  null neue Duplikatzeilen und `0.0%` New-Code-Duplikation ohne Änderung der
  Scanner-Policy melden.
- Ohne gesonderte ausdrückliche Benutzerautorisierung erfolgt keine
  Default-Branch-Integration.

## Geänderte Dateien

- `ci/evidence/collectors/connector_capabilities.py`
- `tests/test_connector_capabilities.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-capability-state-map-deduplication.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-capability-state-map-deduplication.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| Fokussierte Host-Model-, Deep-Immutability- und ForwardAuth-Reference-Tests | Bestanden: `3` Tests. Der Test iteriert jede Envoy-/Traefik-State-Anforderung gegen eine Deep-Copy des kanonischen Manifests und prüft den exakten fail-closed Fehler. |
| `ci/evidence/collectors/connector_capabilities.py check` | Bestanden: sechs Connectoren und 60 Capabilities. |
| Selected-File-`py_compile` mit task-eigenem Bytecode-Cache | Bestanden. |
| `git diff --check` | Bestanden. |
| Vollständiges Modul `tests.test_connector_capabilities` | Externe Abhängigkeit blockiert: 15 Tests bestanden; der bereits bestehende `test_framework_validator_is_required_for_each_runtime_result` scheitert, weil dem isolierten Worktree `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py` fehlt, bevor sein gemockter Subprocess-Pfad erreicht wird. Kein Test und keine Framework-Grenze wurde geschwächt. |
| Ruff und Pyright | Nicht ausgeführt: Keines der Tools ist im ausgewählten Parent-Virtual-Environment installiert; keine Provisionierung eines optionalen Tools ist autorisiert oder erforderlich, um die projektnativen Checks zu ersetzen. |
| Vollständiges `make lint` | Externe Abhängigkeit blockiert, nachdem beide Shell-Syntaxchecks und die Kompilierung aller Parent-`ci`-Python-Dateien bestanden: `check-no-crs-source-normalization` importiert die fehlende Framework-Datei `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`. Der task-eigene `BUILD_ROOT` blieb extern; kein Check wurde geschwächt. |
| `make check-bilingual-docs` | Externe Abhängigkeit blockiert: Jedes gemeldete fehlende Link-Target liegt unter dem fehlenden Framework-Submodule; kein Fehler in einem geänderten Change Record wird gemeldet. |
| `make check-doc-links` | Externe Abhängigkeit blockiert: Seine Repository-Path-Phase meldet dieselben fehlenden Framework-Link-Targets, bevor der Framework-eigene Link-Checker laufen kann. |

## Security-Auswirkung

Die Eingabe ist ein versioniertes Connector-Capability-Manifest. Der nächste
Control ist die statische erwartete State-Map in `_validate_relationships()`;
eine Abweichung fließt als Diagnose und Exit-Code `1` zu `main()`, bevor
erfolgreiches Checking oder Report-Generierung stattfinden können. Eine
geschwächte Map könnte einer prä-Upstream-Integration erlauben, Response-,
Phase-4- oder Late-Intervention-Capability zu beanspruchen, die sie nicht
bereitstellen kann.

Die Map bleibt Source-eigen und tief unveränderlich. Neue direkte Tests decken
den echten Validierungspfad für alle 27 Envoy-/Traefik-Anforderungen, gültige
kanonische Controls, die Ablehnung einer Mutation der äußeren und inneren Map
sowie das unabhängige Gate für die versionierte ForwardAuth-Referenz ab. Die
Source-/Security-Vorprüfung und der finale scoped Diff-Review fanden keinen
plausiblen diff-eingeführten Kandidaten.

## Runtime-Evidence

Es wurde kein Connector-Server, Netzwerk, Runtime-Matrix oder generiertes
Repository-Artefakt ausgeführt oder beansprucht. Dies ist ein deterministischer
Manifest-Validator-Refactor; die fokussierten Tests arbeiten mit In-Memory-
Deep-Copies der kanonischen Parent-Manifeste und rufen die produktive
Validierungsfunktion direkt auf.

## Bekannte Einschränkungen

- Dieses Record deckt einen unabhängigen CI-Duplikationscluster ab, nicht den
  vollständigen Parent-CI-SonarQube-Cloud-Backlog.
- Der isolierte Task-Worktree enthält nicht den Framework-Validator, den ein
  bereits bestehender Test und breitere Make-Targets benötigen. Diese externe
  Abhängigkeit wird hier nicht verborgen oder gepatcht.
- Hosted-GitHub-Actions- und SonarQube-Cloud-Evidence müssen für den exakten
  künftigen Pull-Request-Head eingeholt werden.

## Verbleibende Risiken

Die statische Capability-Deklaration bleibt eine Source-Contract-Assertion.
Dieser Patch beansprucht weder ein Live-Envoy-/Traefik-Runtime-Result noch
ändert er die bestehenden separaten Runtime-Evidence-/Promotion-Controls. Sein
Risiko bleibt auf die bestehende vertrauenswürdige Source- und CI-Policy-Grenze
begrenzt; es wird kein neuer File-System-, Netzwerk-, Prozess-, Credential-
oder Framework-/MRTS-Dependency-Pfad eingeführt.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Framework-abhängige Tests und die verbleibenden Lint- und
  Dokumentationslayer sind durch den fehlenden Framework-Checkout/-Validator
  im isolierten Task-Worktree blockiert. Ihre tatsächlichen Ergebnisse sind
  oben erfasst; kein Control wird umgangen.
- Kein Runtime-Smoke oder Full-Matrix-Lauf wurde ausgeführt, weil er keinen
  direkteren Beweis für den deterministischen Host-Model-State-Map-Contract
  liefern würde.

## Finaler Diff- und Review-Status

Fokussierte Tests, der All-Connector-Manifest-Check, ausgewählte Kompilierung,
Whitespace-Validierung und der finale fokussierte Security-Review haben
bestanden. Ein vollständiger Modultest sowie vollständige Lint- und
Dokumentationschecks sind wie oben beschrieben extern blockiert. Ein lokaler
gerebaseter Implementierungs-Commit existiert; Push, Draft PR, Hosted Checks,
SonarQube-Cloud-Result, Review-Status und Merge werden beim Schreiben dieses
Records nicht beansprucht. Keine Default-Branch-Aktion ist autorisiert oder
impliziert.
