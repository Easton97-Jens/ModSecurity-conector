# Alle Connectoren: Plan für einen latenzarmen Full-Lifecycle

**Sprache:** [English](all-connectors-full-lifecycle-plan.md) | Deutsch

## Aktueller Implementierungs- und Evidence-Stand vom 12.07.2026

Der darunterstehende Stand ist historisch, soweit er die ausgewählten
Traefik- und Envoy-Routen als rein passthrough oder HAProxy als reinen
Observer beschreibt. Die aktuell ausgewählten Pfade sind native Traefik-
Middleware mit persistentem lokalem UDS-Common-/libmodsecurity-Dienst, Envoy
`ext_proc` mit CGo-Common-Bridge sowie der native HAProxy-HTX-Filter mit P1-
und P3-Antworten. Der gepatchte lighttpd-Host besitzt P1/P2/P3-Evidence, aber
keinen Decoded-Entity-Response-Body-Hook.

Frische native Apache- und NGINX-Hostläufe erfassen P4-Safe `log_only` und
Strict-Connection-Abort getrennt. NGINX-HTTP/2 ist nicht ausgewählt: Dem
verwalteten Build fehlt laut `nginx -V` `--with-http_v2_module`. Jedes
unbeobachtete Verhalten bleibt `NOT EXECUTED`; Source-Route, Build oder
synthetischer Harness ersetzen keine kausale Host-Evidence.

## Implementierungsstatus vom 11.07.2026

Dieser Plan behält den darunterstehenden Source-Audit-Stand vor der Implementierung bei und ergänzt
ihn um die folgende abgegrenzte Implementierungsaktualisierung. Keiner dieser
Punkte stuft einen Connector zu verifiziertem Full-Lifecycle-, Low-Latency-
oder Production-Status hoch; frühere Aussagen über fehlende Pfade werden nur
im hier beschriebenen Umfang ersetzt.

- `ci/resolve-runtime-paths.py` zentralisiert validierte Evidence-, Build-,
  Run- und Log-Roots je Connector unter `VERIFIED_RUN_ROOT`, mit gemeinsamem
  Komponenten-Cache `cache-v2/shared`. Das verhindert Root-/Cache-Vererbung
  zwischen Connectors, ist aber keine Connector-Runtime-Evidence.
- Apache und NGINX haben echte native Hostläufe für P3-Deny/Redirect (403/302)
  sowie synchronisierte First-Byte-vor-EOS-Proben. Diese abgegrenzten
  Ergebnisse verifizieren nicht die vollständigen Lifecycle-Matrizen.
- Das HAProxy-3.2.21-HTX-Overlay besitzt einen echten nativen Observer-Lauf:
  P1--P4-Regelpfade werden beobachtet, während der für Clients sichtbare
  Status `200` bleibt. Der Observer ist absichtlich nicht promoted und
  behauptet weder Enforcement noch Late Action, First Byte oder No Full
  Buffer.
- Envoy besitzt jetzt einen echten gestreamten `ext_proc`-Listener/-Service-
  Lauf. Er ist Passthrough und nicht promoted, ohne Common-Runtime-Bridge oder
  Regelauswertung, also keine P1--P4-Evidence.
- Traefiks Kompatibilitäts-`forwardAuth`-Binary-/Config-/Start-Pfad ist
  repariert. Das Full-Lifecycle-Profil wählt die native Middleware separat in
  einem gepinnten Local-Plugin-Host: Plugin-Laden und Router-Traffic werden
  beobachtet, aber `PassthroughEngine` hat keine Common-/libmodsecurity-Bridge
  und promotet keine P1--P4-, Late-Action-, First-Byte- oder No-Buffer-
  Capability.
- lighttpd baut jetzt einen gepinnten gepatchten Core mit passendem Modul und
  hat einen P1-Smoke-Lauf. Der Harness verwendet `response_body_mode=none`;
  P4 wurde nicht ausgeführt und keine Response-Body-bezogene Capability wird
  hochgestuft.

Kompatibilitätsprofile bleiben von nativer Host-Evidence getrennt und können
diesen Plan nicht eigenständig abschließen.

Die Source-Audit-Matrizen und Connector-Erkenntnisse unterhalb dieses Updates
bewahren den historischen Snapshot. Ihre Aussagen über fehlende Pfade dienen
der Design-Provenance und sind keine aktuellen Aussagen über den HTX-Observer,
den separaten Envoy-`ext_proc`-Transportpfad, den nativen Traefik-Local-
Plugin-Hostprobe oder den gepatchten lighttpd-Host; deren begrenzter aktueller
Stand steht oben.

## Historische technische Zusammenfassung

Dies ist ein Plan aus einem Quellcode-Audit, kein Runtime-Nachweis. Die sechs
eingecheckten Integrationen bilden noch keinen einheitlich verifizierten
Full-Lifecycle-Pfad. Die nativen Apache- und NGINX-Filter liegen dem Ziel im
Quellcode am nächsten, benötigen aber echte Host-Evidence für Phase 4 sowie
für *first byte before response end*. HAProxy hat seinen früheren
Response-Sample-Pfad hinter `http-response wait-for-body` bewusst deaktiviert;
der gewählte SPOP-Pfad besitzt keinen Response-Body-Pfad, daher ist Phase 4
dort `not_implemented`. Der gepinnte HAProxy-3.2.21-Source bietet zwar einen
nativen HTX-Filterweg mit Payload- und EOS-Callbacks. Ein optionaler
eingecheckter Observer-Overlay nutzt ihn nur für bodylose Requests, aber die
ausgewählte SPOP-Integration aktiviert ihn nicht und korreliert keinen
vollständigen Lifecycle. Envoy `ext_authz` und Traefik
`forwardAuth` sind bewusst Request-seitige Protokolle; sie sind in diesen
*gewählten Modi* Response-unfähig, nicht etwa ein Beweis gegen einen künftigen
`ext_proc`- bzw. nativen Middleware-Pfad. Das native lighttpd-Modul schaltet
beide Body-Modi ausdrücklich aus.

Die verbindliche Bezeichnung für Phase 4 lautet **inkrementelle
Body-Ingestion; Phase-4-Auswertung am End-of-Stream**.  Erst
`msc_process_response_body` beziehungsweise die Common-Finish-Operation ist
die Auswertungsgrenze. Ein Append-Aufruf wird in diesem Plan niemals als
Regelauswertung pro Chunk bezeichnet.

## Audit-Scope und Evidenzgrenze

Untersucht wurden der Branch `feature/all-connectors-no-crs-baseline`, die
Capability-Deklarationen, Host-Glue, Harnesses, Common SDK und das eingebettete
Framework. Für dieses Dokument wurde kein neuer Connector-Runtime-Lauf
ausgeführt. Deshalb bleibt vorhandenes Source-/Config-Wiring
`implemented_not_asserted`, niemals `verified`.

Zu Beginn geprüfte Heads:

| Repository | Branch | Zu Beginn geprüfter Head |
| --- | --- | --- |
| Superprojekt | `feature/all-connectors-no-crs-baseline` | `062e5ef` |
| Framework-Submodule | `feature/all-connectors-no-crs-baseline` | `3e7a085` |

Auch die im selben Arbeitsbaum vorgenommenen Common-Lifecycle- und
Cache-Änderungen werden erfasst. Ein späterer Runtime-Lauf muss ein eigenes
Manifest, Resultat, JSONL-Events, Inventory und Host-Logs liefern, bevor eine
Capability hochgestuft werden darf.

## Statusvokabular

| Zustand | Bedeutung in diesem Bericht |
| --- | --- |
| `implemented_not_asserted` | Es gibt einen echten Source-/Config-Pfad, aber kein passendes kanonisches Host-Resultat. |
| `configured_not_exercised` | Konfiguration beschreibt einen Pfad, der vorhandene Harness hat ihn aber nicht ausgeführt. |
| `not_implemented` | Der nötige Pfad, Hook, das Protokoll oder der Evidence-Mechanismus fehlt oder verletzt das geforderte Modell. |
| `unsupported_by_host_model` | Der *aktuell gewählte Integrationsmodus* kann diese Phase nicht beobachten. Das ist keine Aussage über alle Host-Modi. |
| `not_applicable` | Im gewählten Request-only-Modus gibt es keinen Response-Pfad, den die Messung prüfen könnte. |

`UNSUPPORTED` zählt niemals als PASS. Mapper, Self-Tests, Direktiven oder
direkte Common-Aufrufe sind keine Runtime-Evidence.

## Historische Source-Audit-Architekturmatrix

Die Matrix trennt den vorhandenen vom zu bauenden bzw. zu vervollständigenden
Pfad. Die Werte sind historischer Audit-Stand vor dem Update, keine
Lieferzusage und keine aktuelle Implementierungsaussage.

| Connector | Aktueller Pfad | Neuer Full-Lifecycle-Pfad | P1 | P2 | P3 | P4 | Kein Full Response Buffer | Safe | Strict | Benötigter Host-Patch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | Natives `httpd`-Modul mit Input-/Output-Filtern. Aktuelle Buckets werden im selben Aufruf inspiziert und weitergegeben; P2/P4 finalisieren bei EOS. | Common-Chunk/Finish-Vertrag an diesen Grenzen übernehmen und Host-Transportverhalten belegen. | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` (EOS-Auswertung) | `implemented_not_asserted` nur aus Source | `implemented_not_asserted` | `implemented_not_asserted` | Kein Core-Patch festgestellt; echte Host-Evidence ist noch erforderlich. |
| NGINX | Native Access-, Header- und Body-Filter. Response-Chain-Puffer werden appendiert und `msc_process_response_body` läuft bei `last_buf`; der Request-Callback bleibt gepuffert. | Response-Filtertopologie behalten, echten Request-Chunk-Pfad ergänzen, Common-Chunk/Finish übernehmen und Transportverhalten belegen. | `implemented_not_asserted` | `implemented_not_asserted` (nur gepuffert) | `implemented_not_asserted` | `implemented_not_asserted` (EOS-Auswertung) | `implemented_not_asserted` nur aus Source für Response | `implemented_not_asserted` | `implemented_not_asserted` | Kein Response-Core-Patch erkennbar; Request-Stream-API/Reihenfolge und Hostverhalten brauchen Tests. |
| HAProxy | SPOE/SPOP-Agent; optionale Response-Header, das frühere Response-Body-Sample ist bewusst deaktiviert. | Den optionalen Source-gebundenen HAProxy-3.2.21-HTX-Observer von bodylosen Requests auf eine vollständige korrelierte Transaktion erweitern, kein `wait-for-body`-Sample. | `implemented_not_asserted` | `implemented_not_asserted` (ein begrenztes Request-Sample) | `implemented_not_asserted` | `not_implemented` | `not_implemented` (kein gewählter Response-Body-Pfad) | `not_implemented` | `not_implemented` | Kein Core-Callback-Patch nötig: natives `flt_ops.http_payload`/`http_end` existiert. Der eingecheckte Observer ist nicht ausgewählt und nur bodylos; vollständige Transaktionskorrelation und Host-Evidence fehlen. |
| Envoy | HTTP-`ext_authz`-Service vor dem Upstream. | Connector-eigener gRPC-`ext_proc`-Service und Envoy-spezifischer Proto-Mapper mit unterstützt gestreamtem Modus. | `implemented_not_asserted` | `configured_not_exercised` (gepufferter Request-Body) | `unsupported_by_host_model` in `ext_authz`; Ziel `not_implemented` | `unsupported_by_host_model` in `ext_authz`; Ziel `not_implemented` | `unsupported_by_host_model` im Request-only-Modus; Zielnachweis `not_implemented` | `unsupported_by_host_model` in `ext_authz` | `unsupported_by_host_model` in `ext_authz` | Kein `ext_proc`-Service, generierter Proto oder Config vorhanden; kein Core-Patch vor Audit der gepinnten API begründbar. |
| Traefik | Externer HTTP-`forwardAuth`-Service vor dem Upstream. | Native Go-Middleware in reproduzierbarem Custom-Build oder eine nachweislich streamingfähige Alternative. | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` in `forwardAuth`; Ziel `not_implemented` | `unsupported_by_host_model` in `forwardAuth`; Ziel `not_implemented` | `unsupported_by_host_model` im Request-only-Modus; Zielnachweis `not_implemented` | `unsupported_by_host_model` in `forwardAuth` | `unsupported_by_host_model` in `forwardAuth` | Keine Middleware-/`ResponseWriter`-Implementierung; Custom-Hook nur, wenn die getestete öffentliche API Late Action nicht leisten kann. |
| lighttpd | Natives Modul mit URI-clean- und Response-start-Hook, das Body-Modi ablehnt. | Nativer Request-Body-Pfad und Output-Hook vor Socket-Write. | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` (kein Output-Body-Pfad zu bewerten) | `not_implemented` | `not_implemented` | Der öffentliche Plugin-ABI des gepinnten 1.4.84 besitzt keinen Output-Body-/EOS-Hook; ein versionierter Core-/ABI-Patch über die Write-Pfade ist erforderlich. |

## Historische gemeinsame Source-Erkenntnisse

### Common-Lifecycle-Vertrag

Die Common Engine besitzt nun explizite Append-/Finish-Operationen mit
geliehenen Pointern in `common/include/msconnector/modsecurity_engine.h`; die
Runtime stellt die zugehörigen `append_*_body_chunk`- und
`finish_*_body`-Operationen in `common/runtime/msconnector_runtime.h` bereit.
Die Runtime hält nach Rückkehr aus append keinen Connector-Body-Pointer, sondern
nur Bytezähler, Trunkierungs- und Commit-Metadaten.

Das ist für die Common-API `implemented_not_asserted`, nicht jedoch ein
Adoptionsnachweis für alle Connectoren. Bestehende Adapter müssen die API noch
an echten Host-Chunk-Grenzen aufrufen und genau einmal finishen. Buffered-
Kompatibilitätshilfen dürfen nicht als Low-Latency-Pfad bezeichnet werden.

### Grenze bei Response-Kompression

Kein eingecheckter Connector darf Klartext-Phase-4-Inspektion komprimierter
Responses behaupten. `response_body_decompression` ist für Apache, NGINX,
HAProxy und lighttpd `not_implemented`; in den gewählten Request-only-Modi
Envoy-`ext_authz` und Traefik-`forwardAuth` ist es
`unsupported_by_host_model`. Ein künftiger Hostlauf muss beobachtetes
Content-Encoding sowie Filter-/Dekompressionsreihenfolge erfassen; diese
Capability ist vom ersten No-Buffer-Meilenstein getrennt.

### Phase-4-Entscheidungsmodell

`common/src/late_intervention.c` enthält den gemeinsamen Resolver:

- vor Header-/Body-Commit: `deny_if_possible`;
- nach Commit bei `minimal` oder `safe`: `log_only`;
- nach Commit bei `strict`: `abort_connection`.

Ein Connector darf `deny_if_possible` nur dann zu `deny` übersetzen, wenn sein
Host den sichtbaren Response noch ändern kann. Ein Late-Event muss die
Regelaktion als `requested_action`, den Transportausgang als `actual_action`,
den originalen Hoststatus und den sichtbaren Status erhalten. Es darf nie eine
nach Commit gesendete 403 behaupten.

### Event- und Capability-Lücken

Das Common-JSONL-Event enthält bereits begrenzte Felder für Action,
requested/actual action, Status, Transportresultat, Response-/Commit-Flags,
`content_type`, `body_bytes_seen` und `body_bytes_inspected`
(`common/include/msconnector/event.h`) und enthält bewusst keinen Body-Payload.
Dies ist Source-Vertragsabdeckung; jeder Connector muss echte Feldbefüllung und
Payload-Abwesenheit noch in Events belegen.

Das Framework-Event-Schema akzeptiert diesen begrenzten Common-Wortschatz.
Sein Ingest ordnet Common-Lifecycle-Phasen kanonischen Regelphasen zu und
übernimmt `response_started` sowie `body_truncated` in das Phase-4-
Resultatmodell. Das ist Schema-/Normalisierungsunterstützung, kein
Connector-Runtime-Event.

Das Framework-Capability-Schema und sein Full-Lifecycle-Katalog verlangen jetzt
Begriffe wie `request_body_incremental_ingest`,
`response_body_incremental_ingest`, `phase4_end_of_stream_evaluation`,
`no_full_response_buffering` und `first_byte_before_response_end`.
Alle sechs aktuellen Connector-Manifeste werden mit konservativen,
nicht-verifizierten Zuständen von der Capability-Selektion akzeptiert. Ein
vorhandenes `streaming`-Flag darf nicht als per-Chunk-Regelprüfung umgedeutet
werden.

### Konfigurationsparität

Common besitzt bereits `phase4_mode`, Content-Type-Datei, Phase-4-Eventlogpfad
und Phase-4-Body-Limit. `request_body_limit`, `response_body_limit`,
`body_limit_action` und `late_intervention_timeout` sind nun mit Validierungs-
und Merge-Regeln als Common-Vertrag definiert. Letzteres ist lediglich ein
Millisekunden-Adapterbudget: Common besitzt keinen Host-Timer und keine
Cancel-Primitive. Erst ein reales Connector-Host-Mapping kann Direktivenparität
oder eine Timeout-Durchsetzung belegen.

## Historische Connector-Pläne und genaue Blocker

### Apache

`connectors/apache/src/msc_filters.c` zeigt jetzt echte Host-Integration für
Request-Header, Request-Buckets, Response-Header und Response-Buckets. Der
Input-Filter appendiert geliehene Request-Buckets, erhält die originalen
Apache-Buckets und finalisiert Phase 2 genau einmal bei EOS. Der Output-Filter
liest nur den aktuellen Bucket, appendiert begrenzte in-scope Bytes, gibt
`bb_in` vor EOS sofort an den nächsten Filter weiter und finalisiert Phase 4
einmal bei EOS. Er hält keine `response_brigade` mehr über Filteraufrufe.

Plan:

1. Native geliehene Bucket-/Einmal-EOS-Logik ohne erneute Connector-Kopien auf
   den Common-Chunk/Finish-Vertrag abbilden.
2. Commit-Zustand unmittelbar um den Downstream-Pass erfassen. Pre-Commit darf
   echten Status setzen; spätes `minimal`/`safe` ist log-only, spätes `strict`
   ein kontrollierter Abbruch.
3. Direkte/Proxy-Responses, Chunk-Grenzen, Keep-Alive, Cleanup, Subrequests,
   interne Redirects und Error Documents vor einer Promotion ausführen.

### NGINX

`ngx_http_modsecurity_body_filter.c` appendiert jeden `ngx_chain_t`-Puffer bis
zum konfigurierten Limit und ruft `msc_process_response_body` erst bei
`last_buf`. Anschließend reicht der Filter die originale `in`-Chain an den
nächsten Filter weiter. Das ist Source-Evidence für inkrementelle Ingestion und
EOS-Auswertung, nicht jedoch für Empfang eines frühen Client-Bytes während der
Upstream noch pausiert und auch nicht für Regelauswertung pro Chunk.

Der NGINX-Request-Body-Callback beginnt erst, nachdem NGINX den Host-Request-
Body gesammelt hat. P2 bleibt als gepufferter Pfad Source-präsent;
`request_body_incremental_ingest` ist zutreffend `not_implemented`.

Plan:

1. Die vorhandene Append-/EOS-Logik ohne eine über mehrere Aufrufe kopierte
   `ngx_chain_t` auf die Common-API abbilden.
2. `phase4_pre_commit_deny` bei `not_implemented` belassen, bis ein echter
   Host-Test einen nicht committeten Phase-4-Entscheidungspunkt belegt. Der
   aktuelle Body-Filter liegt nach dem Response-Header-Pfad.
3. Echte Regelaktionen bewahren; der Code leitet bei 3xx bereits `redirect`
   statt hart `deny` ab.
4. Config-Validierung, Short Writes, Content-Type-Scope, HTTP/2 sowie
   Safe-/Strict-Fixtures in kanonische Runtime-Evidence aufnehmen.

### HAProxy

Das frühere experimentelle Response-Body-Sample ist bewusst deaktiviert. Der
Harness setzt `HAPROXY_ENABLE_RESPONSE_BODY=0`, schreibt keine
`http-response wait-for-body`-Regel und sendet kein `res.body` in seiner
SPOE-Response-Nachricht. Damit besitzt die gewählte SPOP-Integration keinen
Phase-4-Response-Body-Pfad. Eine synthetische Agentantwort ist kein Ersatz für
eine Host-Response-Chunk-API und kann die No-Full-Buffer-/First-Byte-Anforderung
nicht erfüllen.

Das Binding besitzt nun geliehene Primitiven
`haproxy_modsecurity_transaction_append_response_body_chunk` und
`...finish_response_body` mit EOS-Phase-4-Auswertung. Das ist
`implemented_not_asserted` für Adapter-Infrastruktur, kein inkrementeller
Hostpfad: Kein aktiver SPOP-Caller liefert Response-Body-Chunks oder EOS.

Der gepinnte 3.2.21-Source klärt die Host-API-Frage: `flt_ops` bietet
`http_payload` und `http_end`, und der Response-Analyzer ruft sie beim
inkrementellen Weiterleiten von HTX-Daten auf. Der aktuelle SPOE-Filter besitzt
solche Events nicht. Der eingecheckte `htx-overlay/` ist ein source-gebundener
Observer, der baut, `filter modsecurity-htx` parst, aktuelle Response-Slices
leiht und bei EOS für bodylose Requests finalisiert. Er umgeht bewusst
bodytragende Requests, weil das aktuelle Binding P2 atomisch schließt. Er ist
nicht durch den SPOP-Harness ausgewählt und belegt weder kanonische Evidence
noch Enforcement.

Plan:

1. Source-gebundenen HTX-Filter im disposable HAProxy-3.2.21-Worktree vom
   bodylosen Observer-Prototyp zu sicherem Request-Body-Lifecycle erweitern,
   dabei nur Per-Stream-Zustand und geliehene Slices verwenden.
2. Request- und Response-Phasen in derselben lokalen Transaktion korrelieren;
   der aktuelle isolierte bodylose P4-Observer ist nicht semantisch äquivalent
   zum SPOA-Pfad.
3. Genau einmal bei `http_end` finalisieren und ein spätes Ergebnis als
   `log_only` erfassen, bis ein Abbruchverhalten getestet ist. Das Response-Ende
   liegt nach dem Weiterleiten; keinen späten HTTP-Status erfinden.
4. Agent-Ausfall strikt von einem absichtlichen Late-Abbruch trennen;
   originaler/sichtbarer Status und Commit-Zeitpunkt dürfen nicht aus Defaults
   abgeleitet werden.

### Envoy

Der einzige eingecheckte Service ist `envoy_ext_authz_service_main.c`; die
Template-Konfiguration verwendet HTTP `ext_authz` und dessen
`with_request_body`-Block. Es gibt keinen `ext_proc`-Config, keinen
Protobuf-Service, keinen generierten gRPC-Code und keine Processing-Mode-Wahl.
Im vorhandenen Modus sind P3/P4/Late Intervention `unsupported_by_host_model`,
weil die Autorisierung vor der Upstream-Response endet.

Plan:

1. `ext_authz` als Request-only-Kompatibilitätsmodus erhalten.
2. Connector-lokalen `ext_proc`-Service und Mapper ergänzen; Envoy-/Proto-Typen
   nicht in `common/` übernehmen.
3. Vor der Auswahl den gestreamten Modus der gepinnten Envoy-API belegen;
   `BUFFERED`/`BUFFERED_PARTIAL` nicht standardmäßig wählen.
4. Per-Request-Zustand über gRPC-Nachrichten führen und Cancel, Timeout,
   Client Disconnect und Shutdown verarbeiten. Nach Commit log-only oder
   belegten Stream Reset melden, keine fiktive 403.

### Traefik

Der einzige eingecheckte Ausführungspfad ist
`traefik_forwardauth_service_main.c` mit `forwardAuth`-Config. Es gibt weder
native Go-Middleware noch Custom-Traefik-Build oder `ResponseWriter`-Wrapper.
Er kann daher weder Response-Header/-Body sehen noch einen committeten Response
kontrollieren. Das ist für `forwardAuth` `unsupported_by_host_model`, während
der gewünschte Full-Lifecycle-Pfad `not_implemented` ist.

Plan:

1. forwardAuth als Request-only-Kompatibilität beibehalten.
2. Native Middleware gegen die gepinnte Traefik-Version bauen und testen. Ihr
   Wrapper muss `http.ResponseWriter`, `http.Flusher` und alle vom Unterbau
   vorhandenen optionalen Interfaces (`Hijacker`, `Pusher`, ggf.
   `io.ReaderFrom`) bewahren.
3. P3 in `WriteHeader`, jeden `Write`-Chunk vor dem Durchreichen appendieren
   und P4 beim Request-Ende ohne Recorder finishen.
4. Wenn die getestete öffentliche API einen committeten HTTP/1.1-/HTTP/2-Stream
   nicht abbrechen kann, diese genaue Grenze dokumentieren und erst dann einen
   versionierten Custom-Build-Hook ergänzen.

### lighttpd

`module/mod_msconnector.c` registriert nur URI-clean, Response-start und
Request-reset. Bei der Konfiguration lehnt es jeden Request-/Response-
Body-Mappervertrag ab, der nicht `UNSUPPORTED` ist; der Mapper setzt Body-Daten
auf null/zero. Der öffentliche Plugin-ABI des gepinnten lighttpd 1.4.84 enthält
keinen Output-Body-/Chunk-/EOS-Callback: `handle_response_start` läuft vor dem
Header-Write, danach schreibt der Core die Response-Queue direkt. Das ist eine
konkrete Grenze des öffentlichen ABI, keine Annahme über das Modul.

Der aktuelle Reset-Pfad ruft bei `response_body_mode=none` absichtlich kein
`finish_response_body` auf; der Patched-Host-Smoke schlägt fehl, falls diese
Finalisierung erfolgt. Da kein Body-Chunk geliefert wird, ist dies keine
Evidence für Phase-4-Body-Regeln oder einen Output-Hook.

Plan:

1. Request-Body-Queue auditieren und begrenzte geliehene Request-Chunks mit
   einmaligem P2-Finish bauen.
2. Den realen `handle_response_start`-P3-Pfad behalten und eine Pre-Commit-
   Response-Header-Intervention belegen.
3. Schmalen versionierten Core-/ABI-Output-Filter-Patch bauen. Er muss aktuelle
   Chunks, EOS, Error/Abort, Cleanup sowie die relevanten HTTP/1.x- und
   HTTP/2-Write-Pfade abdecken; ein reines Plugin kann diese Grenze nicht
   schaffen.
4. Reset/Cleanup für Normalfall, Client-Abbruch, Upstream-Abbruch und
   Keep-Alive-Wiederverwendung ohne Payload-Aufbewahrung ergänzen.

## Kanonischer Evidence-Plan

Der No-CRS-Katalog des Frameworks ist der Ort für die capability-gesteuerten
Fälle und besitzt jetzt einen deklarativen Unterkatalog `full-lifecycle/`; sein
Catalog-Check besteht mit 104 Fällen. Die Fixtures bleiben ausdrücklich future
beziehungsweise `not_executed_until_real_host`: Das ist Katalogvertrags-
Evidence, kein Connector-Runtime-PASS. Die aktuelle Capability-Selektion
akzeptiert alle sechs Manifeste mit konservativen Zuständen. Der
Unterkatalog umfasst:

- P1 Allow/Deny/Alternativstatus/Redirect/Transaction-ID;
- P2 Marker über zwei Chunks, exakt/über Limit, Trunkierung und
  metadata-only Event;
- P3 Header-Regel, Pre-Commit-Deny/-Redirect und originalen/sichtbaren Status;
- P4 beobachtete Regel, geteilter Marker, explizite EOS-Auswertung, Pre-Commit
  nur soweit bewiesen und getrennte `minimal`-/`safe`-/`strict`-Late-Ergebnisse;
- Content-Types in/out/missing/charset sowie ungültige/Wildcard-Scope-Dateien;
- HTTP/1.1 Content-Length/chunked, Keep-Alive, sequenzielle/parallele Requests,
  HTTP/2 soweit unterstützt sowie Client-/Upstream-Abbruch;
- metadata-only Events ohne Body- oder Match-Werte.

Der First-Byte-Nachweis muss einen synchronisierten Upstream verwenden: Header
und erster Chunk werden gesendet, der Upstream wartet, der Client empfängt
diesen Chunk, erst dann wird der Upstream freigegeben. PASS ist nur Empfang,
während der Upstream noch nicht fertig ist; Millisekundengrenzen allein reichen
nicht. Bis eine echte Host-Evidence existiert, bleiben
`no_full_response_buffering` und `first_byte_before_response_end` unasserted
beziehungsweise als Evidence-Capabilities nicht implementiert.

## Umsetzungsreihenfolge

1. Implementierte immutable Cache-Identität, Manifestvalidierung, sichere
   Invalidierung und disposable Patch-/Build-Bäume bei einem echten Host-
   Rebuild erneut belegen.
2. Common-Chunk/Finish-, Status-, Event- und Capability-Verträge abschließen
   und testen.
3. Den jetzt durchreichenden Apache-Output-Pfad ausführen.
4. Vorhandene NGINX-Incremental-/EOS-Topologie stabilisieren und ausführen.
5. Envoy-`ext_proc` und Traefik-Native-Middleware ergänzen.
6. lighttpd Request-/Output-Hooks ergänzen; Patch nur bei Source-belegtem Bedarf.
7. Nativen HAProxy-Incremental-Filterpfad oder minimalen versionierten Patch
   ergänzen.
8. Gemeinsamen capability-selektierten Katalog ausführen und Hostartefakte
   anhängen.

## Source-Index

- Common: `common/include/msconnector/modsecurity_engine.h`,
  `common/runtime/msconnector_runtime.{h,c}`, `common/src/late_intervention.c`
  und `common/{include,src}/msconnector/event.*`.
- Apache: `connectors/apache/src/msc_filters.c` und Apache-Harness.
- NGINX: `connectors/nginx/src/ngx_http_modsecurity_{access,header_filter,body_filter}.c`.
- HAProxy: `connectors/haproxy/harness/run_haproxy_smoke.sh`,
  `src/haproxy_spop_diagnostic_runtime.c` und
  `src/haproxy_modsecurity_binding.c` sowie der nicht ausgewählte
  Source-gebundene Observer `htx-overlay/`.
- Envoy: `connectors/envoy/src/envoy_ext_authz_service_main.c` und
  `config/envoy-ext-authz-smoke.yaml.in`.
- Traefik: `connectors/traefik/src/traefik_forwardauth_service_main.c` und
  `config/traefik-forwardauth-dynamic.yaml`.
- lighttpd: `connectors/lighttpd/module/mod_msconnector.c`.
- Framework: `modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/`
  und `ci/no_crs_baseline.py`.

## Status der Runtime-Provisionierung

Der Cache-Vertrag ist `implemented_not_asserted` mit Unit-/Contract-Evidence:
Die aktuelle Python-Test-Discovery des Frameworks besteht mit 54 Tests.
Superprojekt-Testergebnisse werden separat geführt und sind hier nicht enthalten. Ein frischer
verwalteter Shared-Component-Lauf hat nach Recovery eines absichtlich
abgebrochenen Cache-Roots Expat `R_2_8_2` und libmodsecurity aus `v3/master`
neu gebaut und mit `status=complete` veröffentlicht. Apache, NGINX und HAProxy
waren bewusst `not_selected`; kein Connector-Host-Binary wurde gebaut,
konfiguriert, gestartet oder als P1–P4-Evidence verwendet.
`ci/prepare-runtime-components.py` verwendet Cache-Schema v2 und bildet
wiederverwendbare Einträge aus aufgelöstem Upstream-Commit/Source- und
Patchset-Hash, Compiler-, Linker-/Buildtool-Versionsdaten, Architektur, Flags,
Connector-/Framework-Commits und Buildprofil. Ein Hit verlangt passende
Registry-Completion, vollständiges Manifest, Identität und erwartete Artefakte.

Fehlende/unvollständige Manifeste lösen bei Expat, ModSecurity, Apache, NGINX
und HAProxy einen Neuaufbau statt einer Manifest-Reparatur aus. Dirty/untracked
Git-Source-Checkouts, falsche Origins, fsck-Fehler oder eine bewegliche Ref mit
neuem Commit werden nur unter einem markierten Managed-Cache-Root verworfen,
in einem temporären Clone geprüft und atomar veröffentlicht. Registry-
Completion bleibt außerhalb von Git-Worktrees und kann sie daher nicht dirty
machen. Envoy, Traefik und lighttpd besitzen in diesem Provisioner keinen neuen
Custom-Cachepfad; dafür wird keine gleichwertige Cache-Coverage behauptet.

Die Per-Entry-Löschberechtigung ist nun Source-seitig vorhanden: Ein sicheres
Entfernen verlangt entweder einen vor der Entry-Erstellung registrierten Marker
(Root, Pfad, Schema, Komponente und Cache-Key) oder ein vollständiges,
schema-v2-konformes Manifest mit selbstkonsistenter Identität/Key, das genau
diesen Entry bindet. Bereits vorhandene unmarkierte Entries werden abgelehnt,
nicht nachträglich geclaimt. Das bleibt Unit-/Contract-Evidence und kein
Host-Runtime-Rebuild-Resultat.

## Bewusst nicht erhobene Claims

Dieser Plan behauptet keine Produktionsreife oder Härtung, keine Runtime- oder
Security-Verifikation, keine CRS-Verifikation/-Vollständigkeit, keine
Full-Matrix-Verifikation, keine Null-Latenz/-Overhead, keinen garantierten
späten Phase-4-HTTP-Status und keine vollständige Verifikation aller
Connectoren.
