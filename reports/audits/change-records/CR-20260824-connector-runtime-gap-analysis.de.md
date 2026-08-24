# Change Record CR-20260824: Gap-Analyse zur Runtime-Verifikation der Connectoren

**Sprache:** [English](CR-20260824-connector-runtime-gap-analysis.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260824-connector-runtime-gap-analysis` |
| Datum (UTC) | `2026-08-24` |
| Basis-Revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Retained-Runtime-Evidence-Revision | `232b020cac23d5edc0e18adaf502468bb3012237` |
| Scope | Nur Parent: EN/DE-Dokumentation einer read-only, code-nahen Gap-Analyse für zehn Connectorpfade. Keine Produkt-, Connector-, Test-, Harness-, Workflow-, CI-, Governance-, Dependency-, Toolchain-, Framework-, MRTS-, Gitlink- oder Runtime-Host-Änderung. |
| Delivery-Grenze | Ein dokumentationsbezogener Branch und Draft-PR. Kein Merge, Bypass, Branch-Protection-/Ruleset-Änderung oder Manipulation von Checks ist autorisiert. |

## Motivation und Problemstellung

Das Ziel ist `fully_runtime_verified` für Apache, NGINX, HAProxy HTX,
HAProxy SPOE/SPOP, Envoy ext_authz, Envoy ext_proc, Traefik forwardAuth,
Traefik Native UDS, lighttpd Stock und lighttpd Patched. Die retained Evidence
belegt dieses Ziel für keinen der zehn Pfade.

Dieser Record bewahrt Phasenmodell, Source-/Evidence-Grenze, Ist- und
Zielmatrizen, Umsetzungsbacklog, Abhängigkeiten und offene
Architekturentscheidungen. Er befördert weder Source-Capability noch
Build-Ergebnis oder historischen Hostlauf zu einem aktuellen Full-Runtime-Pass.

## Akzeptanzkriterien

- Die repository-definierte P1-, P2-, P3- und P4-Semantik erhalten.
- Alle zehn Pfade mit Source-Ownership, Host-/Build-/Config-/Start-/Prozess-
  Evidence und Phase-/Fehler-/Lifecycle-Evidence behandeln.
- Gleichwertige Ist- und Zielmatrizen bereitstellen.
- Priorisierten Backlog, Abhängigkeiten, genaue Source-Anker, gemeinsame und
  Host-spezifische Arbeiten, Abnahmen, Risiken und offene Entscheidungen geben.
- Den responsefähigen Begleitpfad für Envoy ext_authz und Traefik forwardAuth
  erklären, statt P3/P4 dauerhaft als `not_applicable` zu behandeln.
- Nicht ausgeführte Builds, Hostläufe, Strict-Intervention- und Fehlerpfadtests
  ehrlich ausweisen.
- Nur dieses EN/DE-Change-Record-Paar und die EN/DE-Archiveinträge ändern.

## Evidenzgrenze und Statuskonvention

Die Source-Analyse gilt für Basis-Revision
`a6b4ced4876a19666f7c7203ed9e719674c69ec1`. Retained Build-/Runtime-Berichte
verwenden `232b020cac23d5edc0e18adaf502468bb3012237`; sie beweisen keinen
neueren Source-Baum.

| Symbol | Bedeutung |
| --- | --- |
| `✓M` | Retained Real-Host-Ergebnis in der bereitgestellten Matrix. |
| `src` | Nur Source-Inspektion der aktuellen Basis, kein Runtime-Pass. |
| `NR` | Anwendbare Evidence wurde nicht ausgeführt oder reicht nicht aus. |
| `B` | Konkreter retained Blocker oder Fehler. |
| `—` | Im gewählten Pfad strukturell nicht verfügbar; Ziellücke, keine universelle Ausnahme. |
| `H` | Ziel benötigt hostbestätigten Connection-Abort oder Stream-Reset. |
| `C-V` | Zielverifikation benötigt den benannten responsefähigen Composite. |

`Cleanup ✓M` bedeutet nur retained Harness-Prozessabbau. Es beweist kein
Timeout-, Disconnect-, Fehler- oder Folgeanfrage-Cleanup.

## Kanonische Phasensemantik

Die maßgebliche Semantik steht in `common/include/msconnector/phase.h`,
`common/runtime/msconnector_runtime.c`, `examples/common/rule-examples.md`
und `common/rules/modsecurity_p1_p4_vectors.conf`.

| Benutzerphase | Bedeutung | Kanonischer Vektor |
| --- | --- | --- |
| P1 | Request Headers | `1101001` |
| P2 | Request Body bis Request-EOS | `1102001` |
| P3 | Response Headers vor/an Response-Commit | `1103001` |
| P4 | Response Body bis Response-EOS | `1104001`, `1104002`, `1104003` |

`CONNECTION` und `URI` sind vorhergehende interne Runtime-Schritte und
definieren P1 nicht neu. P4 Safe erhält nach Commit eine wahrheitsgemäße
client-sichtbare Response und protokolliert ein nicht disruptives/Log-only-
Ergebnis. P4 Strict ist nur verifiziert, wenn der Host den angeforderten Abort/
Reset wirklich ausführt und meldet.

## Source-Flow- und Ownership-Karte

| Connector | Source-Flow | Aktuelle Grenze |
| --- | --- | --- |
| Apache | `mod_security3.c` Request-Hooks → `msc_filters.c` Request-/Response-Filter → Common Runtime → Hostaktion/Event/Cleanup | P1–P4-Source-Pfade bestehen; Strict-/Fehler-Hostnachweis ist unvollständig. |
| NGINX | `ngx_http_modsecurity_access.c` → Request-Body-Callback → Headerfilter → Bodyfilter | Retained Resultat ist Single-Process-Sandbox, nicht normaler Master/Worker. |
| HAProxy HTX | `haproxy_modsecurity_htx_filter.c`: Begin, Request-Payload, Response-Headers, Response-Payload, Finish | `report_late_decision` ist keine demonstrierte Strict-Hostaktion. |
| HAProxy SPOE/SPOP | `haproxy_spop_diagnostic_runtime.c`: `accept_loop` → HELLO/Frames/Cache → Antwort/Disconnect | Serielles blockierendes Accept/Read und Peer-Close-Handling blockieren robuste Lifecycle-Proofs. |
| Envoy ext_authz | `envoy_ext_authz_service_main.c` → `http_authorization_service.c` → Begin/Decide/Finish/Destroy | Request-phase-only Service erhält keine Upstream-Response. |
| Envoy ext_proc | `processor.go`: `Service.Process`/`stream.Recv` → Stream-State → Engine → gRPC-Response → Close | Idle-Receive-Streams besitzen keine Deadline-/Kapazitäts-Evidence. |
| Traefik forwardAuth | `traefik_forwardauth_service_main.c` → Authorization-Service → Forward-Auth-Response | Request-only; aktuelle Config forwardet keinen Request-Body. |
| Traefik Native UDS | `middleware.go` → `engine_uds.go` → `traefik_engine_service.c` → Common Runtime | Source-bestätigte P2-vor-P3-Ordering-Lücke bei frühen Downstream-Responses. |
| lighttpd Stock | `mod_msconnector.c` und Mapper → Common Runtime | Build schlägt fehl; Stock-Config deaktiviert Request-/Response-Body-Modi. |
| lighttpd Patched | Stream-Hook-ABI → `handle_request_body`/`handle_response_body` → Common Runtime | Source-Pfad besteht; Real-Host-P2–P4-Proof ist unvollständig. |

## Ist-Matrix: Source, Host und Prozess

| Connector | Source | Retained Hostversion | Build | Config | Start | Prozessmodell |
| --- | --- | ---:|---|---|---|---|
| Apache | `connectors/apache` | 2.4.66 | ✓M | ✓M | ✓M | httpd-Modul; normales Prozessdetail NR |
| NGINX | `connectors/nginx` | 1.31.4 | ✓M | ✓M | ✓M | Single-Process-Sandbox ✓M; Master/Worker NR |
| HAProxy HTX | `connectors/haproxy/htx-overlay` | 3.2.22 | ✓M | ✓M | ✓M | In-Host-HTX-Filter |
| HAProxy SPOE/SPOP | `connectors/haproxy/src` | 3.2.22 | ✓M | ✓M | ✓M | externer Listener; serielles Accept/HELLO |
| Envoy ext_authz | `connectors/envoy/src` + Common | 1.39 | ✓M | ✓M | ✓M | Envoy plus TCP-Authorization-Service |
| Envoy ext_proc | `connectors/envoy/ext_proc` | 1.39 | ✓M | ✓M | ✓M | gRPC-bidi; eine Transaktion je Stream |
| Traefik forwardAuth | `connectors/traefik/src` + Common | 3.7.11 | ✓M | ✓M | ✓M | Traefik plus request-only Service |
| Traefik Native UDS | Native Middleware und UDS-Service | 3.7.11 | ✓M | ✓M | ✓M | Plugin plus UDS je Request |
| lighttpd Stock | `connectors/lighttpd/module` | 1.4.85 | B: FND-GS-0001 | NR | NR | nicht gestartet |
| lighttpd Patched | Stream-Hook-Patch und Modul | 1.4.85 | ✓M | ✓M | ✓M | gepatchte Stream-Hooks |

## Ist-Matrix: Runtime und Lifecycle

| Connector | Allow | P1 | P2 | P3 | P4 Safe | P4 Strict | Engine down | Timeout | Ungültige Antwort | Disconnect/Cancel | Folgeanfrage | Cleanup | Aktueller Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | ✓M 200 | ✓M 403/r1001 | ✓M 403/r1200 | ✓M 403/r1301 | ✓M 200 Pass/Safe; Korrelationslücke | NR | NR | NR | NR | NR | NR | ✓M | partial |
| NGINX | ✓M 200 | ✓M 403/r1000001 | NR | NR | NR | NR | NR | NR | NR | NR | NR | ✓M | partial |
| HAProxy HTX | ✓M 200 | ✓M 403/429 | ✓M 403 | ✓M 403 | ✓M 200 Log-only | NR | NR | NR | NR | NR | NR | ✓M | partial |
| HAProxy SPOE/SPOP | ✓M 200 | ✓M 403 | ✓M query 403 | NR | NR | NR | NR | NR | NR | B: SIGPIPE/EPipe | B nach Peer-Close | ✓M, nicht Fehlerpfad | partial / security gap |
| Envoy ext_authz | ✓M 200 | ✓M 403/r1000001 | NR | — | — | — | NR | NR | NR | NR | NR | ✓M | partial, request-only |
| Envoy ext_proc | ✓M 200 | ✓M 403/302 | ✓M 403 | ✓M 403/302 | ✓M 200 Log-only | NR | NR | B: Idle-Streams | NR | ✓M Cancel | NR | ✓M | partial |
| Traefik forwardAuth | ✓M 200 | ✓M 403/r1000001 | — | — | — | — | NR | NR | NR | NR | NR | ✓M | partial, request-only |
| Traefik Native UDS | ✓M 200 | ✓M 403/429 | ✓M 403, Ordering-Lücke | ✓M 403 | ✓M 200 Log-only | NR | NR | nur src | NR | NR | NR | ✓M | partial / P0 blocker |
| lighttpd Stock | NR | NR | — | NR | — | — | NR | NR | NR | NR | NR | NR | failed build |
| lighttpd Patched | ✓M 200 | ✓M 403/r1000001 | NR | NR | NR | NR | NR | NR | NR | NR | NR | ✓M | partial |

## Ziel-Matrix: Source, Host und Start

| Connector | Source | Hostversion | Build | Config | Start/Readiness | Erforderliches Prozessmodell |
| --- | --- | --- | --- | --- | --- | --- |
| Apache | exakter SHA und Patch-Inventar | gepinnt | nativer Pass | native Validierung | PID/Listener/ready | realer httpd |
| NGINX | exakter SHA und Patch-Inventar | gepinnt | nativer Pass | native Validierung | PID/Listener/ready | realer Master/Worker |
| HAProxy HTX | exakter Overlay-/Host-SHA | gepinnt | nativer Pass | Host-Config-Validierung | PID/Listener/ready | HTX-Filter im Host |
| HAProxy SPOE/SPOP | exakter SHA | gepinnt | nativer Pass | SPOE/SPOP-Validierung | Agent und HAProxy ready | begrenzte parallele Verbindungen |
| Envoy ext_authz | exakter Composite-SHA | gepinnt | nativer Pass | Envoy plus Companion | beide ready | ext_authz plus Response-Observer |
| Envoy ext_proc | exakter SHA | gepinnt | nativer Pass | Envoy/gRPC-Validierung | beide ready | begrenzte gRPC-Streams |
| Traefik forwardAuth | exakter Composite-SHA | gepinnt | nativer Pass | forwardAuth plus Observer | beide ready | forwardAuth plus Response-Observer |
| Traefik Native UDS | exakter SHA | gepinnt | nativer Pass | Traefik/UDS-Validierung | Plugin und UDS ready | kein P3 vor P2-EOS |
| lighttpd Stock | exakter SHA und gewählter Hostpfad | gepinnt | reparierter nativer Pass | reparierte Validierung | Real-Host-ready | streamfähiger Stock-Pfad oder Companion |
| lighttpd Patched | exakter Patch-/Host-SHA | gepinnt | nativer Pass | native Validierung | PID/Listener/ready | gepatchte Stream-Hooks |

## Ziel-Matrix: Runtime und Lifecycle

`V` benötigt für dieselbe Transaktion echtes Client-Ergebnis, Rule-ID,
korreliertes Common-Event, tatsächliche Hostaktion und Lifecycle-Evidence.
`H` benötigt zusätzlich hostbestätigten Abort/Reset. Ein Host ohne diese
Primitive kann keinen vollen Zielpass erhalten, bis sich seine Integration ändert.

| Connector | Allow | P1 | P2 | P3 | P4 Safe | P4 Strict | Engine down | Timeout | Ungültige Antwort | Disconnect/Cancel | Folgeanfrage | Cleanup | Zielstatus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| NGINX | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| HAProxy HTX | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| HAProxy SPOE/SPOP | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| Envoy ext_authz | V | V | V | C-V | C-V | C-H | V | V | V | V | V | V | `fully_runtime_verified` |
| Envoy ext_proc | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| Traefik forwardAuth | V | V | C-V | C-V | C-V | C-H | V | V | V | V | V | V | `fully_runtime_verified` |
| Traefik Native UDS | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| lighttpd Stock | V nach Reparatur | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| lighttpd Patched | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |

## Priorisierter Umsetzungsbacklog

| Priorität | Paket | Source-Anker | Erforderliches Ergebnis |
| --- | --- | --- | --- |
| P0 | Native-UDS-P2-vor-P3-Ordering | `middleware.go`: `Middleware.ServeHTTP`, `streamState.processResponseHeaders`, `processBody`; `engine_uds.go` | Ein Body-matchender Request erreicht keine frühe Response vor P2-Entscheidung; kein synthetisches EOS. |
| P1 | Gemeinsamer Lifecycle und Korrelation | `event.h`, `integrity_event.h`, `decision.h`, `msconnector_runtime.[ch]`, `event.c` | Expliziter terminaler Error/Cancel/Cleanup, Exactly-once-Lifecycle, `decision_id`, neutrales Allow-/Log-only-Result. |
| P1 | SPOP-Transportrobustheit | `read_full`, `write_full`, `recv_frame`, `send_agent_disconnect`, `handle_connection`, `accept_loop`, `transaction_cache` | Pro-Socket-Deadline, kein SIGPIPE-Prozessende, begrenzte Parallelität, funktionierendes Folge-HELLO/Allow/Deny. |
| P1 | Envoy-ext_proc-Idle-Streams | `processor.go`, `config.go`, `main.go`, `processor_test.go` | Idle-`Recv`-Deadline, Active-Stream-Bound, Cancel- und Folgeanfrage-Evidence. |
| P1 | Stock-lighttpd-Build | `mod_msconnector.c`, `build/build_module.sh` | Implizite `mod_msconnector_emit_host_transaction_id`-Deklaration reparieren, danach streamfähigen Pfad wählen. |
| P1 | Envoy-ext_authz-Composite | ext_authz-Service, Authorization-Service, ext_proc-Processor, begrenzter Coordinator | P1/P2-Precheck und P3/P4-Observer teilen eine Transaktion. |
| P1 | Traefik-forwardAuth-Composite | forwardAuth-Service, Native Middleware/UDS, begrenzter Coordinator | Logisch vollständiger P1–P4-forwardAuth-Pfad. |
| P2 | P4-Strict-Aktionen | Apache-/NGINX-Filter, HAProxy-Mappings, Envoy-/Traefik-Observer, lighttpd-Pfad | Client-sichtbarer Abort/Reset und tatsächliches Aktions-Event. |
| P2 | Evidence-Vertrag | kanonische Vektoren, Event-Validator, alle Host-Harnesses, `capabilities.json`, EN/DE-Dokumentation | Unveränderliches Source-/Config-/Prozess-/Client-/Event-/Action-/Cleanup-Manifest. |

## Arbeitsaufteilung und konkrete Source-Anker

Die folgenden Pakete sind künftige Implementierungsarbeiten, keine Änderungen
dieses Records. `Common`-Arbeit wird einmal implementiert; ein Hostadapter darf
keine eigene Phasen- oder Evidenzsemantik nachbilden. Hosttimer, Stream-Resets,
Socket-Cleanup und Prozess-Evidence bleiben Connector-/Host-Verantwortung.

| Klasse | Paket und konkrete Anker | Erforderliches Ergebnis und Abnahme |
| --- | --- | --- |
| Common | **C1 Lifecycle:** `common/include/msconnector/{phase.h,transaction_state.h,flow_guard.h}`, `common/runtime/msconnector_runtime.{h,c}`: `msconnector_runtime_transaction_begin`, `append_request_body_chunk`, `finish_request_body`, `process_response_headers`, `append_response_body_chunk`, `finish_response_body`, `finish`, `destroy`; `common/src/flow_guard.c` | Explizite P1–P4-/EOS-/Error-/Cancel-/Disconnect-Zustände; Duplicate- und Out-of-order-Calls werden abgewiesen; terminales Cleanup genau einmal. |
| Common | **C2 P4 Safe/Strict:** `common/src/late_intervention.c`, `common/runtime/msconnector_runtime.c`: `set_response_commit_state`, `record_host_action`; `common/src/event.c`: `msconnector_event_set_phase4_hard_abort_after_200` | Safe protokolliert ein wahrheitsgemäßes nicht disruptives Ergebnis; Strict wird erst emittiert, nachdem der Adapter tatsächlichen Abort/Reset meldet. Common führt die Hostaktion nie aus. |
| Common | **C3 Korrelation:** `common/include/msconnector/{decision.h,event.h}`, `common/src/{decision.c,event.c,integrity_event.c,transaction_id.c}`, Runtime `record_host_action` | Opake `decision_id` und Parent-Decision-Referenz ergänzen; begrenztes neutrales Result für Allow/Log-only erzeugen; Transaction-/Phase-/Rule-/Action-Korrelation über parallele Requests erhalten. |
| Common | **C4 terminale Fehler und Limits:** `common/include/msconnector/{error.h,limits.h,resource_limits.h,request_mapper_contract.h,response_mapper_contract.h}`, `common/src/{error.c,resource_limits.c,request_mapper_contract.c,response_mapper_contract.c}`, Runtime-Transaction-APIs | Neutrale Terminal-Error-/Cancel-API und ein kanonischer Limitvertrag. Jede Fehlerklasse erzeugt ein korreliertes terminales Event und kein falsches EOS/Success. |
| Connector/Host | **H1 Real-Host-Evidence:** vorhandene connector-eigene `harness/`-Skripte/-Configs, `common/rules/modsecurity_p1_p4_vectors.conf`, `capabilities.json` | Für jede exakte Source-/Host-/Config-Kombination: Build, Config-Validierung, Readiness, Clientresultat, Rule-ID-/Decision-/Event-/Action-Korrelation, Error/Timeout/Cancel/Folgeanfrage und Cleanup-Evidence. Das ist künftige Test-/Harness-Arbeit, keine CI-Änderung. |
| Dokumentation | **D1 Evidence-Recording:** dieser EN/DE-Record und der gekoppelte Archive-Index | Capability erst nach unveränderlichen Source-/Config-/Prozess-/Client-/Event-/Action-/Cleanup-Artefakten aktualisieren; `fully_runtime_verified` nie aus einem Framework-Report oder Source-Pfad ableiten. |

## Umsetzungs- und Abnahmeplan pro Connector

Jede Zeile nennt die nächste source-eigene Arbeit und den minimal fehlenden
Nachweis vor einer Promotion. Alle Zeilen benötigen auch den gemeinsamen
C1–C4-Vertrag und H1-Evidence; „Strict“ bedeutet immer beobachtete Hostaktion,
nicht Common-Intent oder Logfeld.

| Connector | Connector-spezifische Implementierungsanker | Promotionsabnahme für diesen Pfad |
| --- | --- | --- |
| Apache | `connectors/apache/src/mod_security3.c`: Request-Hooks und `hook_insert_filter`; `msc_filters.c`: `msc_finalize_request_body`, `apache_input_filter_handle_eos`, Response-Filter; `harness/run_apache_smoke.sh` | Allow/P1/P2/P3/P4 Safe auf exaktem Host wiederholen, Post-Commit-Strict-Aktion implementieren/beweisen, dann Engine-down, Deadline, malformed Host-/Engine-Result, Disconnect, Folgeanfrage und Exactly-once-Cleanup. |
| NGINX | `connectors/nginx/src/ngx_http_modsecurity_{access,header_filter,body_filter}.c`, einschließlich Phase-4-Action-/Log-Helfer; `harness/run_nginx_smoke.sh` | Sandbox-only-Evidence durch normalen Master/Worker-Host ersetzen; echte P2/P3/P4 Safe und Strict, alle geforderten Fehlerfälle, Korrelation sowie Teardown-/Folgeanfrage-Proof ergänzen. |
| HAProxy HTX | `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`: `haproxy_modsecurity_htx_process_response_headers`, Request-/Response-Payload-Appender, `haproxy_modsecurity_htx_report_late_decision`, `haproxy_modsecurity_htx_finish_context` | `report_late_decision` an hostbestätigte Strict-Aktion binden, dann tatsächliche Clientwirkung und alle Engine-/Timeout-/Invalid-/Cancel-/Folgeanfrage-/Cleanup-Fälle im echten HTX-Host zeigen. |
| HAProxy SPOE/SPOP | `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`: `read_full`, `write_full`, `recv_frame`, `send_agent_disconnect`, `handle_connection`, `accept_loop`, `transaction_cache` | Accepted-Socket-Deadlines und begrenzte Parallelität ergänzen; SIGPIPE-/EPipe-Prozessende verhindern; danach Response-Phasen, Safe/Strict, Peer-Close-Recovery und unabhängiges Folge-HELLO/Allow/Deny nach Timeout/Error beweisen. |
| Envoy ext_authz | `connectors/envoy/src/envoy_ext_authz_service_main.c`; `common/runtime/http_authorization_service.{h,c}`: `authorization_process_runtime_request`, `handle_authorization_request`; `connectors/envoy/config/{envoy-ext-authz.conf,envoy-ext-authz-smoke.yaml.in}` | ext_authz als Request-Precheck erhalten und bounded Response-Observer/Composite ergänzen. Beweisen, dass ein hostgeminteter Lease P1/P2 mit P3/P4 einschließlich Strict-Clientwirkung und allen Lifecycle-/Error-Fällen verbindet. ext_authz allein kann P3/P4 nicht bestehen. |
| Envoy ext_proc | `connectors/envoy/ext_proc/internal/processor/{processor.go,config.go}`, `cmd/msconnector-envoy-ext-proc/main.go`; `Service.Process`, `processStream`, `receiveProcessingRequest`; `processor_test.go` | Idle-`Recv` und aktive Streams begrenzen, Cancel-/Timeout-Freigabe und Next-Stream-Recovery beweisen, dann Strict-/Error-/Folgeanfrage-Evidence vollständig erbringen, ohne nicht beobachteten Downstream-Reset zu behaupten. |
| Traefik forwardAuth | `connectors/traefik/src/traefik_forwardauth_service_main.c`, `connectors/traefik/config/{traefik-forwardauth.conf,traefik-forwardauth-dynamic.yaml}`, Common-Authorization-Service; Companion `connectors/traefik/native_middleware/{middleware.go,engine_uds.go}` | Body-Forwarding für P2 entscheiden/dokumentieren, dann forwardAuth per servergemintetem Lease an responsefähigen Companion binden. P3/P4/Strict und alle Error-/Lifecycle-Fälle als eine Transaktion beweisen; request-only forwardAuth allein kann sie nicht bestehen. |
| Traefik Native UDS | `connectors/traefik/native_middleware/middleware.go`: `Middleware.ServeHTTP`, `streamState.processResponseHeaders`, Request-/Response-Body-Handling; `engine_uds.go`: `SetResponseCommit`, `AcknowledgeLateLogOnly`; `src/traefik_engine_service.c` | Zuerst P0-Garantie reparieren, dass P2 sein valides EOS erreicht, bevor P3 verarbeitet werden kann. Dann Commit-/Late-Acknowledgements beobachtbar machen, echte Strict-Primitive beweisen oder nur Safe belassen und volle Error-/Cancel-/Folgeanfrage-/Cleanup-Evidence ausführen. |
| lighttpd Stock | `connectors/lighttpd/module/mod_msconnector.c`: `mod_msconnector_emit_host_transaction_id`, `mod_msconnector_handle_request_body`, `mod_msconnector_handle_response_body`; `build/build_module.sh` | Impliziten Deklarations-Buildfehler reparieren und streamfähigen Stock-Integrationspfad auswählen. Erst dann können Build/Config/Start und P1–P4-/Safe-/Strict-/Error-/Lifecycle-Evidence erhoben werden. |
| lighttpd Patched | Gepatchte Stream-Hook-ABI plus `connectors/lighttpd/module/mod_msconnector.c`: Request-/Response-Body-Handler; Patched-Host-Build/Config/Harness | Gepatchten ABI-Vertrag erhalten, echte P2/P3/P4 Safe und Strict plus Failure-/Cancel-/Folgeanfrage-/Cleanup-Proof ergänzen und jede Hostaktion an den Common-Decision-/Event-Record binden. |

## Abhängigkeiten und empfohlene Reihenfolge

```text
Native-UDS-P0-Ordering
  -> gemeinsamer Lifecycle/Event/Korrelation
     -> Strict-Hostaktionen und einheitliche Fehler-Evidence
     -> vollständige Zehnpfad-Runtime-Matrix

SPOP-Transportreparatur -> SPOP-Response-Phasen -> SPOP-Vollmatrix
ext_proc-Idle-Reparatur -> Envoy-Composite       -> ext_authz-Vollmatrix
Stock-Build-Reparatur   -> streamfähiger Pfad    -> Stock-Vollmatrix
```

Zuerst Source-/Evidence-Identität einfrieren; dann Native-UDS-P0 beheben;
gemeinsame Lifecycle-/Korrelation-/Limit-/Fehler-Schnittstellen einführen;
Stock-/SPOP-/ext_proc-Blocker auflösen; source-fähige Adapter validieren;
request-only-Companions implementieren; echte P4-Strict-Aktion beweisen; volle
Hostmatrix ausführen; erst dann Capability-Claims aktualisieren.

## Architektur für Envoy ext_authz und Traefik forwardAuth

`common/runtime/http_authorization_service.h` definiert einen
request-phase-only Service. Der Handler mappt einen Request, ruft Begin, Decide,
Finish und Destroy und gibt eine Authorization-Response zurück, bevor eine
Upstream-Response existieren kann. ext_authz und forwardAuth können P3/P4 nicht
selbst beobachten.

Die erforderliche Lösung ist ein begrenzter hosteigener
Transaktionskoordinator, keine zweite unkorrelierte Transaktion:

1. Der Request-Precheck öffnet die Common-Transaktion und verarbeitet P1/P2.
2. Ein vertrauenswürdiger Response-Observer verarbeitet P3/P4 derselben Transaktion.
3. Der Host berichtet angeforderte/tatsächliche Aktion, Commit-Status,
   Transportresultat, Fehler, Timeout und Cleanup genau einmal.
4. Der Coordinator entfernt State nach terminalem Outcome, Timeout, Cancel,
   Disconnect, Duplicate-Erkennung oder Capacity-Eviction.

`x-request-id`, URI, Methode oder ein Client-Header dürfen nicht alleiniger
Korrelationsschlüssel sein. Der Host erzeugt einen einmaligen opaken begrenzten
Lease, bindet ihn an Host-Request/Stream und Deadline und verwendet geschützte
Metadaten. Bei unvermeidlichem Header-Transport werden eingehende Kopien
entfernt, das Token geschützt und vor Upstream/Client entfernt. Kein Fallback
per URI oder wiederverwendeter Client-ID genügt.

Das bevorzugte Envoy-Design ist ext_authz-Precheck plus ext_proc-Response-
Observer. Das bevorzugte Traefik-Design ist forwardAuth plus native
Response-beobachtende Middleware/UDS. Bestehende ext_proc-/Native-UDS-Evidence
darf erst geliehen werden, wenn der Composite eine Transaktion Ende zu Ende
beweist.

## Security-Auswirkung

Diese reine Dokumentationsänderung verändert keinen Parser, Authorization-Rule,
Netzwerklistener, Timeout, Secret, Privileg, Request-/Response-Pfad oder
Security-Control.

Die Analyse hält zwei source-gestützte Risiken für künftige Remediation fest:

- Concurrent Finding `FND-PARENT-0220` beschreibt einen P0/high-Native-
  Traefik-UDS-Ordering-Defekt: Eine frühe Downstream-Response kann P3 erreichen,
  bevor ein ungelesener P2-Body EOS erreicht. Dieser Record verändert oder
  schließt ihn nicht.
- Ein begrenzter read-only Security-Scan hielt einen SPOP-Availability-Candidate
  mit mittlerer Konfidenz fest: serielles `accept_loop` plus blockierende
  Frame-Reads kann einem Partial-Frame erlauben, den Listener anzuhalten. Er
  unterscheidet sich von retained `FND-GS-0002` SIGPIPE/EPipe-Peer-Close-
  Verhalten. Es lief kein Runtime-Exploit.

Künftige Remediation muss payload-freie begrenzte Events, servereigenen
Korrelationsstate, wahrheitsgemäße Response-Commit-Semantik und kein falsches
erfolgreiches EOS erhalten.

## Geänderte Dateien

- `reports/audits/change-records/CR-20260824-connector-runtime-gap-analysis.md`
- `reports/audits/change-records/CR-20260824-connector-runtime-gap-analysis.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Keine Produkt-, Connector-, Test-, Harness-, CI-/Workflow-, Governance-,
Framework-, MRTS-, Gitlink-, Dependency- oder generierte Runtime-Datei wird
verändert.

## Ausgeführte Befehle und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Read-only-Remote-Preflight | Bestanden: Fetch- und effektive Push-URL sind `git@github.com:Easton97-Jens/ModSecurity-conector.git`; Repository ist exakt, nicht archiviert, Default-Branch `master`, Viewer-Permission `ADMIN`. |
| Basis-/Destination-Readback | Bestanden: Remote und lokales `origin/master` lösen auf `a6b4ced4876a19666f7c7203ed9e719674c69ec1`; Task-Branch fehlte vor Erstellung. |
| Ruleset-Readback | Bestanden: aktives Ruleset `Protect master` `19138299` hat keine Bypass-Akteure, fordert PR/Thread-Resolution und sechs strikte Checks. |
| Basis-Required-Check-Snapshot | Für Basis-SHA bestanden: `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint` und `zizmor` waren `completed/success`. Dies ist keine künftige PR-Head-Evidence. |
| Boundary des gemischten Worktrees | Bestanden: vorhandene fremde Änderungen wurden durch einen sauberen Task-Worktree ausgeschlossen. |
| Manuelle zweisprachige Parität | Bestanden: beide Records besitzen 24 entsprechende Top-Level-Abschnitte; Basis-/Evidence-SHAs, Connectormatrizen, Finding-IDs, Branch und Zielstatus wurden in beiden Sprachen geprüft. |
| Scoped-Diff-Review | Bestanden: der Task-Worktree enthält genau die vier geplanten Dokumentationspfade und `git diff --check` ist sauber. |
| Dokumentationschecks | Nicht ausgeführt: Die Repository-Targets rufen CI-eigene Scripts außerhalb dieser dokumentationsbezogenen Ausnahme auf. Stattdessen laufen manuelle EN/DE-Überschriften-/Faktenparität und scoped Git-Checks. |

## Runtime-Evidence

Für diese reine Dokumentationsänderung wurden kein Build, Hostprozess,
Runtime-Harness oder Connector-Test ausgeführt. Retained Inputs sind das
bereitgestellte Set `14-security-posture.md`, `15-supply-chain-state.md`,
`16-runtime-readiness.md`, `19-findings-inventory.md` und
`25-build-runtime-matrix.md` plus bereitgestellte Finding-Records. Sie
begründen nur partielle Hostresultate auf ihrer aufgezeichneten Revision.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Connector-Build, Host-Start, Smoke-Test, Runtime-Matrix-, Timeout-,
  Strict-Intervention- oder Fehlerpfad-Test lief: Der Benutzer autorisierte
  Dokumentations-Delivery, nicht Produkt-/Runtime-Ausführung.
- Kein Produkttest und kein Harness wurde geändert.
- `make check-bilingual-docs` und `make check-doc-links` wurden nicht
  ausgeführt, weil ihre Targets CI-eigene Scripts aufrufen, die außerhalb der
  eng autorisierten Delivery-Preflight-Ausnahme bleiben.
- Frische PR-Head-Hosted-Checks und SonarQube-Ergebnisse existieren beim ersten
  Schreiben nicht und werden nicht behauptet. Sie werden erst nach PR-Erstellung
  beobachtet.

## Bekannte Einschränkungen

Dies ist ein Gap-Analyse- und Delivery-Artefakt, keine Implementierung. Alle
zehn Pfade bleiben unterhalb des Ziels, bis Zielmatrixbedingungen für exakte
aktuelle Source-, Host-, Config- und Prozess-Evidence bewiesen sind. Retained
Evidence liegt vor der Basis-Revision und kann ohne Rerun nicht promotet werden.

## Restrisiken

P4 Strict kann nach Response-Commit in einem bestimmten Host unmöglich sein,
bis eine verifizierbare Abort-/Reset-Primitive besteht. Request-only-Protokolle
benötigen stateful Companions und bringen begrenzten State-, Timeout-, Restart-,
Duplicate- und Cleanup-Risiken. Native-UDS-P0-Ordering- und SPOP-Availability-
Risiken blockieren eine vertrauenswürdige Vollpromotion, bis sie behoben oder
von einem künftigen Benutzer ausdrücklich risikakzeptiert sind.

## Finaler Diff- und Review-Status

Der beabsichtigte Diff ist auf die vier genannten Dateien in einem sauberen,
task-eigenen Worktree auf verifiziertem `master` begrenzt. Dieser Record
autorisiert keinen Merge, direkten `master`-Push, Force-Push,
Workflow-/Config-Änderung, Check-Bypass, Framework-Delivery oder Remediation
eines aufgezeichneten Findings.

## Auslieferungsstatus

Der aktuelle Benutzer autorisierte einen Dokumentationsbranch, Commit, Push und
Draft-PR. Der Branch ist `agent/connector-runtime-gap-analysis-20260824`;
Ziel ist `master`. Commit-SHA, PR-Nummer/-URL und Exact-Head-Check-Ergebnisse
werden nicht erfunden und erst aufgezeichnet, wenn sie existieren.
