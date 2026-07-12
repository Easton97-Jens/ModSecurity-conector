# Alle Connectoren: Full-Lifecycle-Readiness

**Sprache:** [English](all-connectors-full-lifecycle-readiness.md) | Deutsch

## Aktuelle Host-Evidence vom 12.07.2026

Dieses Update ersetzt den nachfolgenden Implementierungsstatus vom 11.07.2026,
soweit er einen Pfad als rein passthrough- oder observer-basiert beschreibt.
Es dokumentiert ausgewählte echte Hostläufe mit Common-/libmodsecurity-
Transaktionen; weder eine vollständige Connector-Matrix noch Production-
Eigenschaften werden behauptet.

- **Runtime-Roots und Cache-v2:** Jeder ausgewählte Full-Lifecycle-Runner
  verwendet eigene Build-, Run-, Log- und Evidence-Roots. Gemeinsame native
  Abhängigkeiten bleiben unveränderliche Schlüssel-Einträge in Cache-v2;
  Connector- oder Common-Änderungen wählen vor einem Hostlauf einen neuen
  Connector-Eintrag.
- **Traefik:** Die gepinnte native Middleware wählt im echten Traefik-Route
  ihren persistenten lokalen UDS-Common-/libmodsecurity-Dienst. Der
  ausgewählte Lauf belegt P1/P2/P3-Enforcement und P4-Safe `log_only`.
  Strict bleibt ohne beim Client sichtbaren Post-Commit-Reset `NOT EXECUTED`.
- **Envoy:** Der echte `ext_proc`-Listener erreicht pro Stream die CGo-
  Common-/Runtime-Bridge. Der ausgewählte Lauf belegt P1/P2/P3-Enforcement
  und P4-Safe `log_only`; ein strikter Downstream-Reset bleibt `NOT EXECUTED`.
- **HAProxy:** Der native HTX-Filter wendet im ausgewählten Host echte P1-
  und P3-Pre-Commit-Antworten (403/429/403) an. P2/P4-Host-Enforcement und
  Late-Action-Claims bleiben nicht promoted.
- **lighttpd:** Der passende gepatchte Core/das Modul besitzt reale P1/P2/P3-
  Ergebnisse. Sein verfügbarer Output-Hook sieht HTTP/1-Wire-Bytes statt einer
  decodierten Entity; Response-Body-Inspektion und P4-Promotion bleiben daher
  `NOT EXECUTED`.
- **Apache und NGINX:** Frische native Hostläufe liefern P1/P2/P3-Ergebnisse
  sowie getrennte P4-Safe-`log_only`- und Strict-Connection-Abort-Records.
  Dem verwalteten NGINX-Build fehlt `--with-http_v2_module`; HTTP/2 ist für
  diesen Build deshalb `NOT_APPLICABLE` und wird nicht aus HTTP/1.1 abgeleitet.

## Implementierungsstatus vom 11.07.2026

Dieses Update dokumentiert Arbeit nach dem darunterstehenden Source-Audit vor der Implementierung. Es
stuft keinen Connector zu einem verifizierten Full-Lifecycle-, Low-Latency-
oder Production-Status hoch. Wo das ältere Audit einen Pfad als fehlend
beschreibt, ersetzt dieses Update nur diese Aussage und nur innerhalb der hier
genannten Evidenzgrenze.

- **Isolierte Runtime-Roots und Cache:** `ci/resolve-runtime-paths.py` leitet
  je Connector Evidence-, Build-, Run- und Log-Roots unter einem vom Aufrufer
  gewählten `VERIFIED_RUN_ROOT` ab und validiert sie. Der gemeinsame
  Komponenten-Cache liegt unter `cache-v2/shared`; Aufrufer erben nicht mehr
  implizit den Build- oder Evidence-Root eines anderen Connectors. Das ist
  Resolver-/Cache-Plumbing, kein Runtime-Nachweis für einen Connector.
- **Apache und NGINX:** Beide nativen Adapter haben echte Hostläufe für
  Phase-3-Deny und -Redirect (403/302) sowie synchronisierte First-Byte-vor-
  EOS-Proben. Diese abgegrenzten Ergebnisse verifizieren nicht die vollständigen
  Lifecycle-Matrizen.
- **HAProxy:** Ein isoliertes Overlay für echten HAProxy 3.2.21 HTX kann als
  nativer HTX-Observer gebaut und ausgeführt werden. Seine vier P1--P4-
  Regelpfade wurden im Observer-Modus beobachtet, während der für Clients
  sichtbare Status `200` blieb. Das ist absichtlich nicht promoted: Es belegt
  weder Pre-Commit-Enforcement noch Safe-/Strict-Late-Action, First-Byte- oder
  No-Full-Buffer-Evidence.
- **Envoy:** Ein echter `ext_proc`-Listener/-Service nutzt jetzt gestreamte
  Request- und Response-Processing-Modi. Der aktuelle Service ist explizit
  ein Passthrough-Transporttest ohne Promotion, Common-Runtime-Bridge oder
  Regelauswertung; er ist keine P1--P4- oder Enforcement-Evidence.
- **Traefik:** Der Build-/Config-/Start-Abhängigkeitspfad für das
  `forwardAuth`-Binary wurde repariert und bleibt das Kompatibilitätsprofil.
  Das Full-Lifecycle-Profil wählt die native Middleware separat in einem
  gepinnten Local-Plugin-Host; Plugin-Laden und Router-Traffic werden
  beobachtet, aber `PassthroughEngine` hat keine Common-/libmodsecurity-Bridge
  und promotet keine Lifecycle-Capability.
- **lighttpd:** Ein versionsgebundener gepatchter Core und das passende Modul
  bauen jetzt als echtes Host-Paar; ein P1-Smoke-Pfad wurde ausgeführt. Dieser
  Harness erzwingt `response_body_mode=none`; Phase 4 wurde nicht ausgeführt.
  Daraus folgt keine Promotion für Response-Body, EOS, Late Action, First
  Byte oder No Full Buffer.

Die Trennung zwischen nativem und Kompatibilitätsprofil bleibt absichtlich:
Kompatibilitätsprofile können diagnostisch nützlich sein, ersetzen aber keine
Evidence für die geforderten nativen Full-Lifecycle-Routen.

Die Source-Audit-Matrizen und Connector-Erkenntnisse unterhalb dieses Updates
bewahren den historischen Snapshot. Ihre Aussagen über fehlende Pfade dienen
der Design-Provenance und sind keine aktuellen Aussagen über den HTX-Observer,
den separaten Envoy-`ext_proc`-Transportpfad, den nativen Traefik-Local-
Plugin-Hostprobe oder den gepatchten lighttpd-Host; deren begrenzter aktueller
Stand steht oben.

## Historische technische Zusammenfassung

Kein Connector ist aktuell als latenzarmer Full-Lifecycle-Connector zur Runtime verifiziert. Dieses Source-Audit findet brauchbare Bausteine, aber kein neues Artefaktset pro Connector, das P1–P4, Safe-/Strict-Late-Intervention, fehlendes vollständiges Response-Buffering und first byte before response end gemeinsam belegt.

- Apache gibt die aktuelle Output-Brigade vor EOS weiter und finalisiert P2/P4 bei EOS. Der First-Byte- und Hosttransport-Nachweis fehlt.
- NGINX appendiert im Source pro Body-Puffer und wertet bei EOS aus; kanonische Runtime-Evidence fehlt.
- HAProxy deaktiviert sein früheres wait-for-body-/res.body-Sample bewusst; der gewählte SPOP-Pfad besitzt keinen Response-Body- oder Phase-4-Pfad. Die gepinnte native HTX-Filter-API hat einen optionalen Source-only-Observer für bodylose Requests, der jedoch nicht ausgewählt und kein vollständiger Lifecycle-Pfad ist.
- Envoy ext_authz und Traefik forwardAuth sind bewusst Request-only. Ihre Response-Facetten sind in genau diesen Modi unsupported_by_host_model; ext_proc bzw. native Middleware fehlen.
- lighttpd deaktiviert Request- und Response-Body-Pfade explizit.

implemented_not_asserted bedeutet vorhandenen Code ohne Runtime-PASS. not_implemented bedeutet fehlenden oder ungeeigneten Pfad. unsupported_by_host_model gilt nur für den jeweils aktivierten Integrationsmodus und nicht für die gesamte Hostplattform.

## Historische Audit-Evidenzgrenze

Der historische Audit-Snapshot beruht auf Source, Capability-Dateien, Harnesses und Framework-Katalog auf feature/all-connectors-no-crs-baseline. Für diesen Snapshot lief kein neuer kanonischer Full-Lifecycle-Runtime-Test. Spätere abgegrenzte Läufe stehen im Update oben und promoten selbst kein kanonisches Full-Lifecycle-Resultat. Runtime-Aussagen der historischen Matrix sind deshalb NOT EXECUTED, im Request-only-Modus UNSUPPORTED oder Source-only implemented_not_asserted.

Vor einer Promotion ist je Lauf mindestens erforderlich:

~~~text
manifest.json
result.json
results.jsonl
events.jsonl
inventory.json
stdout.log
stderr.log
host.log
~~~

## Historische Source-Audit-Readiness-Matrix

| Connector | Aktivierter Pfad | P1 | P2 | P3 | P4 | Safe | Strict | Kein Full Buffer | First Byte | Aktueller Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | Natives httpd-Modul/Filter | implemented_not_asserted | implemented_not_asserted | implemented_not_asserted | implemented_not_asserted; Ingestion/EOS | implemented_not_asserted | implemented_not_asserted | implemented_not_asserted aus Source | NOT EXECUTED | Keine Host-Evidence für First Byte, Commit, Late-Modi, Cleanup oder Keep-Alive. |
| NGINX | Natives HTTP-Modul | implemented_not_asserted | implemented_not_asserted | implemented_not_asserted | implemented_not_asserted; Ingestion/EOS | implemented_not_asserted | implemented_not_asserted | implemented_not_asserted aus Source | NOT EXECUTED | Host-Event, Transport, HTTP/2 und First-Byte-Nachweis fehlen. |
| HAProxy | SPOE/SPOP-Agent | implemented_not_asserted | implemented_not_asserted für begrenztes Request-Sample | implemented_not_asserted | not_implemented | not_implemented | not_implemented | not_implemented | not_implemented | Früheres Response-Sample bewusst deaktiviert. Ein optionaler HAProxy-3.2.21-HTX-Observer verarbeitet nur bodylose Requests, ist nicht ausgewählt und korreliert keine vollständige Transaktion. |
| Envoy | HTTP ext_authz | implemented_not_asserted | configured_not_exercised | unsupported_by_host_model | unsupported_by_host_model | unsupported_by_host_model | unsupported_by_host_model | unsupported_by_host_model im Request-only-Modus | unsupported_by_host_model | Kein ext_proc-Service, Proto-Mapper, Stream-Config oder Evidence. |
| Traefik | HTTP forwardAuth | implemented_not_asserted | not_implemented | unsupported_by_host_model | unsupported_by_host_model | unsupported_by_host_model | unsupported_by_host_model | unsupported_by_host_model im Request-only-Modus | unsupported_by_host_model | Keine native Middleware/ResponseWriter-Route oder Custom-Build-Evidence. |
| lighttpd | Natives mod_msconnector.so | implemented_not_asserted | not_implemented | implemented_not_asserted | not_implemented | not_implemented | not_implemented | not_implemented | NOT EXECUTED | Body-Modi werden abgelehnt; der öffentliche lighttpd-1.4.84-Plugin-ABI besitzt keinen Output-Body-/EOS-Hook, daher ist ein versionierter Core-/ABI-Patch nötig. |

## Vom historischen Source-Audit belegter Common-Vertrag

Die Common Engine und Runtime haben jetzt explizite borrowed-pointer Chunk- und Finish-Operationen:

~~~text
transaction_begin
process_request_headers
append_request_body_chunk
finish_request_body
process_response_headers
append_response_body_chunk
finish_response_body
transaction_finish / transaction_destroy
~~~

Append ingestiert nur den aktuellen Chunk. Finish ruft den nativen Body-Prozessor auf; P2/P4 kann daher bei EOS auswerten. Das ist kein Claim einer Regelauswertung pro Chunk. Die Runtime behält keine Host-Body-Pointer nach Rückkehr aus append.

Der gemeinsame Late-Resolver ergibt vor Commit deny_if_possible, nach Commit bei minimal/safe log_only und nach Commit bei strict abort_connection. Erst ein Hostpfad kann beweisen, ob der Connector dies umsetzt.

Das Common-Event bleibt metadata-only und enthält Action, requested_action, actual_action, Status, Transportresultat, Commit-Flags, content_type, body_bytes_seen und body_bytes_inspected. Das ist Source-Vertrag; echte Feldbefüllung und Payload-Abwesenheit im Run bleiben NOT EXECUTED.

Das Framework akzeptiert den begrenzten Common-Event-Wortschatz, ordnet
Common-Lifecycle-Phasen kanonischen Regelphasen zu und übernimmt
response_started/body_truncated in sein Phase-4-Resultatmodell. Das ist nur
Schema-/Normalisierungsunterstützung, kein Connector-Runtime-Event.

Das Framework-Schema verlangt *_incremental_ingest, phase4_end_of_stream_evaluation, no_full_response_buffering und first_byte_before_response_end. Die Capability-Selektion akzeptiert alle sechs aktuellen Manifeste mit konservativen, nicht-verifizierten Zuständen. Vorhandene *_streaming-Namen dürfen nicht als Beweis für Chunk-Regelauswertung gelten. Common definiert nun Merge- und Validierungssemantik für request_body_limit, response_body_limit, body_limit_action sowie das Millisekunden-Adapterbudget late_intervention_timeout. Da Common keinen Host-Timer und keine Cancel-Primitive besitzt, bleiben Timeout-Durchsetzung und Connector-Direktivenzuordnung unverified und werden nicht durch den Vertrag behauptet.

### Grenze bei Kompression

response_body_decompression ist für Apache, NGINX, HAProxy und lighttpd not_implemented. In den gewählten Request-only-Modi Envoy-ext_authz und Traefik-forwardAuth ist es unsupported_by_host_model. Kein Bericht oder künftiges Resultat darf komprimierte Response-Bytes als Klartext-Inspektion bezeichnen, bis ein Hostpfad Content-Encoding und Filter-/Dekompressionsreihenfolge erfasst.

## Historische Erkenntnisse pro Connector

### Apache

Der Input-Filter appendiert geliehene Request-Buckets, erhält Apache-eigene Buckets und führt msc_process_request_body genau einmal bei EOS aus. Der Output-Filter liest und appendiert nur aktuelle begrenzte Response-Bytes, ruft den nächsten Filter mit bb_in vor EOS auf und führt msc_process_response_body einmal bei EOS aus. Die frühere Cross-Call-Akkumulation response_brigade ist entfernt.

minimal/safe log-only und strict abort sind Codezweige, aber keine Runtime-Evidence für Commit-Behandlung, Connection-Reuse oder sichtbaren Transport. Erforderlich sind P2-Chunks, P3-Pre-Commit-Status, P4 bei EOS, Content-Type-Scope, Safe/Strict, Keep-Alive, Cleanup und der synchronisierte First-Byte-Test.

### NGINX

Der Body-Filter durchläuft die aktuelle ngx_chain_t, appendiert jeden erlaubten Puffer und ruft msc_process_response_body erst bei last_buf auf. Er reicht die originale Chain weiter. Die korrekte Source-Aussage lautet inkrementelle Body-Ingestion mit Phase-4-Auswertung am End-of-Stream. Der Request-Body-Callback beginnt dagegen erst nach dem Sammeln des Host-Request-Bodys; P2 ist Source-präsent als gepufferter Pfad, aber request_body_incremental_ingest ist not_implemented.

Die aktuelle Body-Filter-Zeitlage belegt keinen P4-Pre-Commit-Deny; diese Facette bleibt not_implemented. Redirect, Safe log-only und Strict Abort benötigen separate reale HTTP/1.1-/HTTP/2-Events.

### HAProxy

Das frühere experimentelle P4-Sample ist bewusst deaktiviert: run_haproxy_smoke.sh setzt HAPROXY_ENABLE_RESPONSE_BODY=0, schreibt keine http-response-wait-for-body-Direktive und übergibt kein res.body in einer check-response-SPOE-Nachricht. Der aktuelle SPOP-Pfad kann daher weder Response-Body-Delivery noch Phase-4-Auswertung, Post-Commit-Intervention oder First Byte belegen. phase4, Late Intervention, log-only, strict abort und Late-Status-Metadaten sind in der aktuellen Capability-Datei korrekt not_implemented.

Das Binding hat nun geliehene Append-Response-Chunk- und EOS-Finish-Primitiven.
Das ist implemented_not_asserted für Adapter-Infrastruktur, nicht für einen
inkrementellen Hostpfad: Kein aktiver SPOP-Caller liefert Response-Body-Chunks
oder EOS. Der optionale Source-gebundene HTX-Observer baut und parst gegen
HAProxy 3.2.21, appendiert geliehene Response-Daten und finalisiert bei EOS
für bodylose Requests, ist aber nicht ausgewählt und nach dem Weiterleiten nur
observer-only. Er umgeht bodytragende Requests bewusst, weil P2 im aktuellen
Binding atomisch ist. Incremental-/No-Buffer-/First-Byte-Capabilities des
gewählten SPOP-Pfads bleiben daher not_implemented.

HAProxy 3.2.21 bietet bereits `flt_ops.http_payload` und `http_end` über seine
HTX-Filter-API; der eingecheckte bodylose Observer muss deshalb zu einem
Source-gebundenen Filter erweitert werden, der die vollständige
P1–P4-Transaktion besitzt oder explizit korreliert. Er muss nur
Per-Stream-Zustand halten, für P4 nie `wait-for-body` verwenden und
Agent-Ausfall von einem absichtlichen Post-Commit-Abbruch trennen. Der
EOS-Callback liegt nach dem Weiterleiten; ein später HTTP-Status darf nicht
behauptet werden.

### Envoy

Der eingecheckte Service ist ein HTTP-ext_authz-Profil mit optional gepuffertem Request-Body. Es gibt keinen ext_proc-Service, keine gRPC-/Protobuf-Artefakte, keinen processing_mode und keinen Response-Handler. P3/P4/Late sind folglich nur im aktivierten ext_authz-Modus unsupported_by_host_model; der gewünschte ext_proc-Pfad ist not_implemented.

### Traefik

Der eingecheckte Pfad ist ein HTTP-forwardAuth-Service. Es gibt keine Go-Middleware, keinen ResponseWriter-Wrapper, kein Flush-/Hijack-Handling und keinen Custom-Build. P3/P4/Late sind für forwardAuth unsupported_by_host_model; eine Full Middleware ist not_implemented.

Der Zielpfad muss Writer-Interfaces bewahren, P3 vor WriteHeader ausführen, jeden Write-Chunk ohne Recorder ingestieren und eine echte HTTP/1.1-/HTTP/2-Strict-Strategie oder genaue API-Grenze belegen.

### lighttpd

Das native Modul registriert URI-clean, Response-start und Request-reset. Bei Config-Load verlangt es, dass Request- und Response-Body unsupported sind; der Mapper liefert null/zero-Bodies. Der Response-start-Hook belegt nur Source-P3. Der öffentliche Plugin-ABI von lighttpd 1.4.84 enthält keinen generischen Output-Body-/EOS-Callback; `handle_response_start` liegt vor dem Header-Write und der Core schreibt die Queue danach direkt. P2/P4/Safe/Strict sind deshalb not_implemented, nicht unsupported_by_host_model.

Der aktuelle Reset-Pfad ruft bei `response_body_mode=none` absichtlich kein
`finish_response_body` auf; der Patched-Host-Smoke schlägt fehl, falls diese
Finalisierung erfolgt. Da kein Response-Chunk die Runtime erreicht, ist dies
keine Phase-4-Body-Regel- oder Output-Hook-Evidence.

Erforderlich sind native geliehene Request-Chunks und Cleanup sowie ein enger
versionierter Core-/ABI-Output-Filter für aktuelle Chunks, EOS, Abort, Cleanup
und relevante HTTP/1.x-/HTTP/2-Write-Pfade. Ein normaler Response-start-Hook
ist kein Phase-4- oder Late-Intervention-Hook.

## Tests, Cache und Promotion

Der vorhandene No-CRS-Katalog ist der einzige Result-Schema-Ort für capability-gesteuerte Full-Lifecycle-Fälle. Sein neuer deklarativer Unterkatalog full-lifecycle besteht den Catalog-Check mit 104 Fällen; alle neuen Fixtures sind future beziehungsweise not_executed_until_real_host. Das ist implemented_not_asserted für den Katalogvertrag, nicht Runtime-Evidence. Die Capability-Selektion akzeptiert alle sechs aktuellen Connector-Manifeste mit konservativen Zuständen. P1/P2/P3/P4, Content-Type-Scope, Limits, Safe/Strict, Protokolle und Payload-Privacy sind aktuell NOT EXECUTED, bis echte Hostartefakte vorliegen.

Der First-Byte-Fall muss einen synchronisierten Upstream verwenden: Header und erster Chunk werden gesendet, der Upstream wartet, der Client erhält den Chunk, erst dann wird der Upstream freigegeben. Eine Millisekundengrenze allein ist kein Nachweis.

Cache-Integrität ist Voraussetzung, nicht Evidence-Ersatz. Das Cache-Upgrade
ist implemented_not_asserted: Die aktuelle Python-Test-Discovery des Frameworks
besteht mit 54 Tests. Superprojekt-Testergebnisse werden separat geführt und
sind hier nicht enthalten. Ein frischer verwalteter Shared-Component-Lauf hat außerdem
einen abgebrochenen Cache-Root wiederhergestellt und Expat `R_2_8_2` sowie
libmodsecurity aus `v3/master` jeweils mit vollständigem Manifest und den
erwarteten Artefakten atomar gebaut. Apache, NGINX und HAProxy waren bewusst
`not_selected`; es wurde kein Connector-Host-Binary gebaut, konfiguriert,
gestartet oder als Lifecycle-Evidence verwendet. Cache-Schema v2 bindet
aufgelöste Upstream-/Source-/Patchset-Hashes, Compiler-, Linker-/Buildtool-
Versionsdaten, Architektur, Flags, Connector-/Framework-Commits und
Buildprofil. Ein wiederverwendbarer Eintrag benötigt Registry-Completion,
passende Identität, status complete und erwartete Artefakte.

Fehlende oder unvollständige Manifeste lösen für Expat, ModSecurity, Apache,
NGINX und HAProxy einen Neuaufbau statt einer Manifest-Reparatur aus. Managed
Git-Source-Checkouts, die dirty/untracked sind, eine falsche Origin haben, fsck
nicht bestehen oder eine bewegliche Ref auf einen neuen Commit auflösen, werden
nur unter einem markierten Cache-Root verworfen, in einem temporären Clone
geprüft und atomar veröffentlicht. Registry-Completion liegt außerhalb des
Git-Worktrees und kann ihn daher nicht dirty machen. Superprojekt, Framework,
Submodule und unbekannte Checkouts dürfen nicht bereinigt werden. Envoy,
Traefik und lighttpd besitzen in diesem Provisioner keinen neuen Custom-
Cachepfad; dafür wird keine gleichwertige Coverage behauptet. Kein Connector
wird nur wegen eines Cache-Hits hochgestuft.

Sicheres Entfernen verlangt jetzt Per-Entry-Berechtigung: entweder einen vor
der Erstellung registrierten und an Cache-Root, Pfad, Schema, Komponente und
Key gebundenen Marker oder ein vollständiges Schema-v2-Manifest mit
selbstkonsistenter Identität/Key, das genau diesen Entry bindet. Bereits
vorhandene unmarkierte Entries werden abgelehnt statt unmittelbar vor der
Löschung geclaimt. Das ist Source- und Unit-/Contract-Evidence, keine
Host-Runtime-Evidence.

Ein Connector darf erst weiterpromotet werden, wenn ein echter Hostlauf P1–P4, EOS-Finalisierung, First Byte vor Upstream-Ende, korrekte Pre-/Post-Commit-Semantik, metadata-only Events, Cleanup, Keep-Alive, Limits und anwendbare Protokolle im vollständigen Artefaktset belegt.

## Bewusst nicht erhobene Claims

Dieser Bericht behauptet keine Produktionsreife/-härtung, keine Runtime- oder Security-Verifikation, keine CRS-Verifikation/-Vollständigkeit, keine Full-Matrix-Verifikation, keine Null-Latenz/-Overhead, keinen garantierten späten Phase-4-HTTP-Status und keine vollständige Verifikation aller sechs Connectoren.
