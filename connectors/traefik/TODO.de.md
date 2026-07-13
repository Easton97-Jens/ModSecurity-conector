# Traefik-Connector-TODO

**Sprache:** [English](TODO.md) | Deutsch

Status: minimal_runtime_smoke (nur forwardAuth-Request-Pfad)
Runtime-Status: connector-gap außerhalb des gezielten Request-Header-Nachweises
Kanonischer No-CRS-Status: `supported_not_verified` / `NOT EXECUTED`
Metadata-Evidence-Zustände: `link_verified`, `minimal_runtime_smoke` und
`connector-gap`.

Der Standard-Kompatibilitätspfad bleibt `forwardAuth`. Das separate
Full-Lifecycle-Profil leitet `native-middleware` über
`full-lifecycle-traefik-native`, das das Go-Modul in einem gepinnten Traefik-
Local-Plugin-Host bereitstellt und eine private persistente UDS-
Common-/libmodsecurity-Engine auswählt. Seine gezielte Host-Evidence bleibt
nicht hochgestuft und kann für sich keine Lifecycle-Capability hochstufen.

Globale Gate-Definitionen sind in `docs/connectors/README.md` und
`docs/testing-and-evidence.md` zusammengefasst.

## Phase 0: Scaffold

- [x] Connector-Verzeichnis erstellt
- [x] README vorhanden
- [x] TODO vorhanden
- [x] Docs vorhanden
- [x] Harness-Contract dokumentiert
- [x] src-Platzhalter dokumentiert
- [x] kein lokaler Ordner `connectors/traefik/tests`

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` hinzugefügt
- [x] `SOURCE_MAP.json` hinzugefügt
- [x] `metadata.*` hinzugefügt
- [ ] Upstream-Traefik-Quellcode dokumentiert
- [ ] Lizenz für eine Upstream-Traefik-Integration dokumentiert

## Phase 2: Build / lokaler Starter

- [x] Build-Starter-Ansatz dokumentiert
- [x] Metadata-Build-Starter-Befehl ausgeführt
- [x] Decision-Service-Starter implementiert
- [x] Decision-Service-Starter-Befehl ausgeführt
- [x] lokaler Decision-Service-Selbsttest ausgeführt
- [x] Connector-eigener forwardAuth-Service-Einstiegspunkt implementiert
- [x] C17-Compile-/Link-only-Connector-Build implementiert
- [x] libmodsecurity-Include-Pfade explizit bereitgestellt
- [x] libmodsecurity-Library-Pfade explizit bereitgestellt
- [x] Connector-Service-Artefaktpfad dokumentiert
- [x] Config-Check und Process-only-Start-Smoke vom Build getrennt
- [ ] Produktions-Traefik-Build-Logs dokumentiert

## Phase 3: Harness

- [x] gezielter Runtime-Smoke-Einstiegspunkt `make smoke-traefik` implementiert
- [x] Harness-Befehl dokumentiert
- [x] BLOCKED-Evidence-Pfad dokumentiert
- [x] Common-Smoke-Result-Writer statt Connector-lokalem JSON-Writer verwendet
- [x] Connector-lokales echtes Traefik -> forwardAuth -> Service-Harness
      implementiert
- [x] erlaubter Request liefert im gezielten nativen Runtime-Smoke HTTP 200
- [x] blockierter Request liefert durch forwardAuth regelgestütztes HTTP 403
- [x] native Go-Middleware-Source-/Build-Grundlage mit fokussierten lokalen
      Tests hinzugefügt
- [x] native Go-Middleware wird nur vom separaten Full-Lifecycle-Local-Plugin-
      Target ausgewählt und bleibt vom Standard-Phase-1-Runtime-Contract für
      forwardAuth ausgeschlossen
- [x] gepinnter Traefik-Local-Plugin-Host-Probe stellt das Modul bereit,
      bestätigt das Laden und routet einen Body-tragenden Request ohne
      Capability-Promotion
- [x] persistente lokale Common-/libmodsecurity-UDS-Engine-Bridge implementiert
      und gezielt auf echtem Host P1/P2/P3/P4-safe mit Evidence belegt, ohne
      hochgestuft zu werden

## Phase 4: No-CRS Runtime

- [ ] `make test-no-crs` für den Traefik-Scope ausgeführt
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert
- [x] Architekturgrenze in `capabilities.json` aufgezeichnet: Traefik 3.7 kann
      einen forwardAuth-Body puffern, aber der eingecheckte forwardAuth-Pfad
      aktiviert `forwardBody` nicht und verwendet `request_body_mode=none`;
      Phase 2 ist daher für den ausgewählten Pfad `not_implemented`.
- [x] Upstream-Response-Headers und -Bodies für `forwardAuth` als
      `unsupported_by_host_model` aufgezeichnet.
- [ ] `make no-crs-baseline-traefik` erzeugt aktuelle kanonische Evidence.
- [ ] `make evidence-check-traefik` validiert das Ergebnis und verwendet den
      Legacy-Python-/Evaluator-Body-Probe nicht als native Service-Evidence.

## Phase 5: With-CRS Runtime

- [ ] `make test-with-crs` für den Traefik-Scope ausgeführt
- [ ] CRS-Loaded-/Effective-Evidence dokumentiert
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert

## Phase 6: Coverage Matrix

- [ ] Phase-1/2/3/4-Runtime-Status dokumentiert
- [ ] Negativ-/Pass-through-Status dokumentiert
- [ ] Audit-/Log-Evidence dokumentiert
- [ ] RESPONSE_BODY-Blockierung bewertet

## Phase 7: Promotion

- [ ] berechtigt für `adapter-owned`
- [ ] berechtigt für `runtime-smoke-verified`
- [ ] berechtigt für `crs-verified`
- [ ] berechtigt für eine Promotion über gezielten `minimal_runtime_smoke`
      hinaus
- [ ] Runtime-Evidence des aktuellen Commits stuft den Service-Source über
      `connector-gap` hinaus

## Kompatibilitäts- und native Phase-4-Grenze

Die Kompatibilitätsintegration `forwardAuth` wird vor dem Upstream-Handling
ausgeführt. Die folgenden Facetten sind daher für diesen Pfad
`unsupported_by_host_model`: `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata`.

- [x] Kompatibilitäts-Phase-4-Cases als `UNSUPPORTED`, nicht als
      `NOT EXECUTED` beibehalten, weil dieses Host-Modell die spätere
      Upstream-Response nicht empfangen kann.
- [x] Nativer UDS-Host-Probe zeichnet P4-safe-`log_only` nach Commit mit einer
      sichtbaren 200 auf; Strict-Late-Abort ist ausdrücklich `NOT EXECUTED`.
- [x] Nativer Safe-Probe erfordert einen HTTP/1.1-Same-Connection-Follow-up und
      schreibt nur ein diagnostisches, nicht hochstufendes Sidecar;
      unvollständige Host-Writes erzeugen kein synthetisches Response-EOS.
- [ ] Request-seitige 200/403, `forwardBody` oder einen Decision-Service-
      Selbsttest nicht als Response-Body-, Late-Action-, Original-Status-,
      Visible-Status- oder Connection-Abort-Evidence verwenden.
- [ ] Den nativen Hostpfad mit Cancellation-/Disconnect- und Strict-Abort-
      Evidence erweitern, bevor irgendeine Capability-Promotion erfolgt.
