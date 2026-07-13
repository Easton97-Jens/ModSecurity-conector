# Envoy-Connector-TODO

**Sprache:** [English](TODO.md) | Deutsch

Status: gezielter `minimal_runtime_smoke` für den realen HTTP-`ext_authz`-
Request-Pfad
Kanonischer No-CRS-Status: `supported_not_verified` / `NOT EXECUTED`
Metadata-Evidence-Zustände: `compile_verified`, `minimal_runtime_smoke` und
`connector-gap`.

Kanonische Capability-Quelle: `connectors/envoy/capabilities.json`.

Globale Gate-Definitionen sind in `docs/connectors/README.md` und
`docs/testing-and-evidence.md` zusammengefasst.

## Phase 0: Scaffold

- [x] Connector-Verzeichnis erstellt
- [x] README vorhanden
- [x] TODO vorhanden
- [x] Docs vorhanden
- [x] Harness-Contract dokumentiert
- [x] src-Platzhalter dokumentiert
- [x] kein lokaler Ordner `connectors/envoy/tests`

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` hinzugefügt
- [x] `SOURCE_MAP.json` hinzugefügt
- [x] `metadata.*` hinzugefügt
- [x] Upstream-Envoy-Quelle als nicht ausgewählt/importiert dokumentiert
- [x] Lizenz des importierten Upstreams als nicht ausgewählt dokumentiert, weil
      kein Upstream-Quellcode importiert wurde

## Phase 2: Bridge-Starter-Build

- [x] Sidecar-/HTTP-Bridge-Starter-Ansatz dokumentiert
- [x] Include-Pfade für den Bridge-Starter-Build dokumentiert
- [x] Bridge-Starter-Quellcode baut
- [x] Bridge-CLI-Selbsttest läuft
- [x] Connector-eigener C17-ext_authz-Service baut und linkt
- [x] Common-Runtime und echte Mapper-Callbacks sind gelinkt
- [x] Envoy-SDK-/API-Abhängigkeiten als für HTTP ext_authz nicht erforderlich
      dokumentiert
- [x] proxy-wasm-/ext_proc-Abhängigkeiten als außerhalb des ausgewählten Pfads
      dokumentiert
- [ ] Produktionsadapter-Build-Logs dokumentiert

## Separater nicht hochgestufter ext_proc-Full-Lifecycle-Hostpfad

- [x] Gepinntes offizielles Go-Envoy-proto/gRPC-Modul und Checksum-Lock
      hinzugefügt.
- [x] `ExternalProcessor`-Stream-Service im Connector mit Pro-Stream-State,
      begrenzten inkrementellen Header-/Body-Callbacks, EOS-Cleanup und
      Cancellation-Cleanup hinzugefügt.
- [x] Nicht-`BUFFERED`-`STREAMED`-Request-/Response-Envoy-Template und
      externer Materializer hinzugefügt.
- [x] Source-/Unit- und getaggte CGo-Tests decken Chunks, EOS, Cancellation,
      Entscheidungen vor der Response, Response-Commit-Reihenfolge und das
      konservative Late-Action-Ergebnis ab.
- [x] `PassthroughEngine` im normalen Executable durch die geprüfte
      Common-/libmodsecurity-Transaction-Bridge ersetzt. Reine Source-/Protobuf-
      /Unit-Builds behalten Passthrough nur bei, wenn keine Runtime-Config
      akzeptiert werden kann.
- [x] Die gepinnte Envoy-Release gegen die materialisierte Config validieren und
      einen echten lokalen HTTP/1.1-P1/P2/P3/P4-Common-/libmodsecurity-
      Host-Smoke mit roher Common-Rule-/Action-Evidence und Cleanup-Evidence
      ausführen.
- [x] Einen Opt-in-Probe für einen echten HTTP/1.1-Client-Close-after-first-byte
      mit genau einem nicht zurechenbaren terminalen Completion-Record
      (`grpc_context_canceled_unattributed` oder `grpc_peer_eof`) und einem
      fehlerfreien Folge-Request hinzufügen. Sein diagnostisches Sidecar ist
      bewusst keine kanonische Reset- oder Client-Cancel-Promotion-Evidence.
- [ ] HTTP/2-, Timeout-, Reset- und First-Byte-Cases ausführen; eine Bridge
      existiert jetzt, aber diese Cases bleiben unverifiziert und dürfen nicht
      hochgestuft werden.

## Phase 3: ModSecurity-Bridge

- [x] libmodsecurity-Headers über explizite/Framework-Umgebung bereitgestellt
- [x] libmodsecurity-Library mit lokalem Runtime-rpath gelinkt
- [x] ModSecurity-Transaction-Lifecycle an `common/runtime` delegiert
- [x] gezielte echte Rule-Evaluation über den Envoy-ext_authz-Smoke ausgeführt

## Phase 4: Envoy-Harness

- [x] Connector-lokaler Einstiegspunkt `runtime-smoke-envoy` implementiert
- [x] Harness-Befehl dokumentiert
- [x] fehlende Abhängigkeiten sind BLOCKED, während echte Runtime-Fehler FAIL
      ergeben
- [ ] kanonische Framework-Evidence-Normalisierung verarbeitet die
      Connector-lokalen Summary-/Event-Artefakte und schreibt das gemeinsame
      `result.json` und Manifest; offen lassen, bis ein aktueller kanonischer
      Run die Validierung besteht
- [x] echtes Envoy-ext_authz-Runtime-Harness implementiert
- [x] erlaubter Request liefert im lokalen gezielten Smoke HTTP 200
- [x] blockierter Request liefert durch Envoy ext_authz regelgestütztes HTTP
      403

## Phase 5: No-CRS Runtime

- [ ] `make test-no-crs` für den Envoy-Scope ausgeführt
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert
- [ ] Request-Body-Delivery wird ausgeübt, bevor Phase 2 über
      `configured_not_exercised` hinaus hochgestuft wird.
- [ ] `make no-crs-baseline-envoy` erzeugt aktuelle kanonische Evidence.
- [ ] `make evidence-check-envoy` validiert das Ergebnis, ohne die nicht
      unterstützten Upstream-Response-Phasen als FAIL oder PASS zu behandeln.

## Phase 6: With-CRS Runtime

- [ ] `make test-with-crs` für den Envoy-Scope ausgeführt
- [ ] CRS-Loaded-/Effective-Evidence dokumentiert
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert

## Phase 7: Coverage Matrix

- [ ] Phase-1/2/3/4-Runtime-Status dokumentiert
- [ ] Negativ-/Pass-through-Status dokumentiert
- [ ] Audit-/Log-Evidence dokumentiert
- [ ] RESPONSE_BODY-Blockierung bewertet

## Phase 8: Promotion

- [ ] berechtigt für `adapter-owned`
- [ ] berechtigt für `runtime-smoke-verified`
- [ ] berechtigt für `crs-verified`
- [ ] berechtigt für mehr als `partial`

## Kanonische Phase-4-Architekturgrenze

Die ausgewählte HTTP-`ext_authz`-Integration läuft vor dem Upstream-Handling.
Die folgenden Source-Contract-Facetten sind daher
`unsupported_by_host_model`: `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata`.

- [x] Ausgewählte Phase-4-Cases wegen der ext_authz-Upstream-Response-Grenze
      als `UNSUPPORTED` statt als `NOT EXECUTED` klassifizieren.
- [ ] Request-seitige 200/403-Evidence nicht als Response-Body-, Late-Action-,
      Original-Status-, Visible-Status- oder Connection-Abort-Evidence
      behandeln.
- [ ] Diese Zustände nur für eine andere Envoy-Integration neu bewerten, die
      tatsächlich die Upstream-Response erhält; diese Integration erfordert
      neue Host-Path-Evidence und darf ext_authz-Ergebnisse nicht erneut
      verwenden.
