# Audit zu Transport-Härtung und vollständigen Body-Phasen

**Sprache:** [English](transport-hardening-audit.md) | Deutsch

## Ergebnis und Umfang

Dies ist ein Source-/API- und lokaler Host-Audit der Transport-Härtung und
vollständigen Body-Phasen auf `feature/all-connectors-no-crs-baseline`. Er hält
fest, was Framework, Connector-Quellen, Harnesses und diese Maschine belegen
können. Er ist kein Promotion-Report und macht weder ein Configure-Flag, einen
kompilierten Mux, einen internen Callback-Fehler noch ein synthetisches Event
zu client-sichtbarer HTTP/1.1-, HTTP/2- oder HTTP/3-Laufzeit-Evidence.

Das Framework besitzt jetzt einen payload-freien Protocol-Client-Vertrag,
kanonische Protocol-Provenienz und Katalogfälle für Negotiation, Phase 1--4,
Multiplexing, Reset, First Byte und No Full Buffer. Dieser Audit promotet für
keinen Connector ein neues HTTP/2- oder HTTP/3-Full-Lifecycle-Ergebnis.
Modern-Protocol-Fälle bleiben daher `NOT EXECUTED`, bis ein zukünftiger echter
Hostlauf das vollständige Evidence-Gate erfüllt.

Der lokale Client ist `curl 8.18.0`: Seine Feature-Liste enthält `HTTP2`, aber
nicht `HTTP3`. Ein erzwungener H2-/H2C-Preflight kann auf diesem Host versucht
werden; ein H3-Probe ist bereits vor dem Connector-Kontakt mit
`client_http3_unsupported` `BLOCKED`. Das ist ein Client-Umgebungsblocker und
keine Aussage, dass ein Connector durch sein Host-Modell nicht unterstützt
wird.

## Audit-Eingaben

Die Framework-Schlüsse stammen aus
`modules/ModSecurity-test-Framework/ci/checks/protocol/protocol_client.py`,
`modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`, den No-CRS-Schemas
und den Protocol-Fällen in
`modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json`.
Die Aussage zum verwalteten NGINX
stammt aus `ci/provisioning/components/prepare-runtime-components.py`, dem Framework-
`modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh` und
`connectors/nginx/harness/run_nginx_smoke.sh`. Die Grenzen pro Connector sind
die sechs Inventare `connectors/*/capabilities.json`, gegengeprüft mit ihren
nativen Quellen und Harnesses. Die lokalen Fakten sind direkte Beobachtungen
von `curl --version`, `nginx -V`, `haproxy -vv` und der Apache-Modulliste; es
wird kein Netz-Probe als ausgeführt dargestellt.

## Evidence-Vertrag

Die Common-Event- und Case-Result-Verträge halten folgende Dimensionen
getrennt:

| Dimension | Kanonische Werte / Regel |
|---|---|
| Angefordertes, Downstream-, Upstream-, ausgehandeltes Protokoll | `http1`, `h2`, `h2c`, `h3`; Downstream und Upstream werden niemals voneinander abgeleitet. |
| Transport | `tcp`, `tls_tcp`, `quic_udp`; allein der H3-Name belegt keinen UDP-/QUIC-Verkehr. |
| Negotiation | H2 über TLS benötigt ALPN `h2`; H3 benötigt ALPN `h3`, beobachtetes QUIC/UDP, eine Stream-ID, QUIC-Version und nur `quic_connection_id_present`, niemals eine rohe QUIC-Connection-ID. |
| Korrelation | Ein promotierbares Ergebnis bindet Connector, Integrationsmodus, Run-ID, Transaction-ID, gegebenenfalls Rule-ID, Phase, gegebenenfalls Stream-ID und denselben begrenzten `transport_case_id`, den der verwaltete Client sendet. |
| Fallback | `fallback_used` muss false sein. H3 verwendet curl `--http3-only`; das fallback-fähige `--http3` wird abgelehnt. |
| Strikte späte Aktion | Bei H2/H2C/H3 muss ein Deny nach Commit ein beim Client beobachteter, request-lokaler `stream_reset` mit Reset-Code und `transport_result=stream_reset` sein; er darf nicht als Connection-Abort umetikettiert werden. |

`ci/checks/protocol/protocol_client.py` schreibt für einen verwalteten Probe immer diese
payload-freien Artefakte:

- `client-version.txt`
- `client-features.txt`
- `client-command.txt`
- `client-protocol-observation.json`

Der Client leitet Response-Bodies an das Null-Device und persistiert weder
rohe Header noch Payloads, rohe curl-Stderr-Ausgabe, Request-Geheimnisse oder
rohe QUIC-Connection-IDs. Fehlende Stream-/ALPN-/QUIC-Provenienz erzeugt ein
nicht promotierbares Ergebnis, kein geratenes `PASS`.

Die Statuswörter haben absichtlich unterschiedliche Bedeutungen:

- `not_implemented` bedeutet, dass Connector-Quelle oder eigener Harness
  keinen solchen Integrationspfad haben.
- `implemented_not_asserted` bedeutet, dass eine kontrollierte Build- oder
  Konfigurationsoberfläche existiert, aber keine passende erzwungene Client-
  und echte Connector-Evidence.
- `NOT EXECUTED` bedeutet, dass kein Katalog-/Laufzeit-Claim belegt ist. Er
  kann mit jedem der beiden Capability-Status zugleich auftreten.
- `BLOCKED` dokumentiert eine Umgebungs-Voraussetzung wie das fehlende
  HTTP/3-fähige curl dieses Hosts, ohne den Connector-Capability-Status zu
  ändern.

## Lokaler Host-Audit

| Geprüfter Gegenstand | Lokaler Befund | Konsequenz |
|---|---|---|
| curl | `curl 8.18.0`, Feature `HTTP2` vorhanden, `HTTP3` fehlt | H2-/H2C-Probes können vorbereitet werden; jeder erzwungene H3-Probe ist lokal bereits vor dem Request `BLOCKED`. |
| NGINX-Laufzeitbinärdatei | `nginx 1.31.1 -V` enthält weder `--with-http_v2_module` noch `--with-http_v3_module` | Dies ist eine H1-Binärdatei. Sie kann unabhängig vom Modulcode keine H2-/H3-Evidence liefern. |
| HAProxy-Laufzeitbinärdatei | H2-Mux ist gelistet; der Build meldet `-OPENSSL`, `-SSL` und `-QUIC` | Der Mux-Eintrag ist weder ein H2-TLS-/ALPN-Frontend noch ein QUIC-/H3-Pfad. |
| Apache-Laufzeitmodule | Die geladene Modul-Inventur enthält kein `mod_http2` | Der gepinnte Apache-Host ist nicht als H2-Connector-Pfad verwendbar. |
| Envoy-, Traefik-, lighttpd-CLIs | `envoy --version`, `traefik version` und `lighttpd -V` sind auf dieser Maschine nicht verfügbar | Für diese Hosts wird kein lokaler Laufzeitversions- oder Protokoll-Claim erhoben. |
| H2-Hilfsclients | `nghttp` und `h2load` sind nicht verfügbar | Sie können die verwaltete curl-Evidence auf dieser Maschine nicht ersetzen. |

Die verwaltete NGINX-Build-Logik hat explizite Profile `h1`, `h1-h2` und
`h1-h2-h3-quic`. Letzteres hält einen gepinnten QUIC-fähigen OpenSSL-Eingang
fest und verweigert einen stillen H3-Fallback-Build. Diese Profile sind
Build-Provenienz, keine Aussage, dass die lokal geprüfte H1-Binärdatei H2 oder
H3 ausgehandelt hat.

## Phase-0-Matrix für Transport und APIs

Diese Source-/Harness-Matrix beschreibt die ausgewählte Repository-Integration,
nicht eine allgemeine Aussage darüber, was ein Upstream-Server unterstützen
könnte. „Keine API“ bedeutet, dass der gepinnte Connector mit seinem eigenen
Harness keine öffentliche request-lokale Operation verdrahtet; aus einem
fehlenden Test wird keine Host-Modell-Unmöglichkeit abgeleitet.

| Connector | Protokoll | Commit-Erkennung | Client-Abbruch-API | Stream-Reset-API | Upstream-Cancel | EOS-Callback | Keep-Alive-Verhalten | aktuelle Grenze |
|---|---|---|---|---|---|---|---|---|
| Apache natives Modul | HTTP/1.1 ausgewählt; kein eigener H2/H2C- oder H3-Pfad | Output-Filter folgt auf Response-Header; sein Strict-Source-Zweig liefert bei Response-EOS `APR_ECONNABORTED` | Kein ausgewählter Peer-Disconnect-Fall | Kein request-lokaler H2/H3-Reset verdrahtet | Kein ausgewählter Upstream-Abbruchfall | `APR_BUCKET_IS_EOS` finalisiert den Response-Body einmal | Kein transportspezifischer Keep-Alive-Lauf | H2 über TLS/H2C und natives H3 sind im gepinnten Harness nicht implementiert |
| NGINX natives Modul | HTTP/1.1 ausgewählt; H2/H3-Buildprofile existieren, aber ohne Client-Dispatcher | Header-/Body-Filter verfolgen den Commit; `last_buf` ist die Response-EOS-Grenze | Strict-Source-Pfad markiert einen Connection-Error; keine Client-Abbruch-Beobachtung angehängt | Keine stream-lokale H2/H3-Reset-Aktion verdrahtet | Kein ausgewählter Upstream-Abbruchfall | Body-Filter beendet bei `last_buf` | Kein Modern-Protocol-Keep-Alive-Lauf | H2/H3-Profile bleiben Build-/Config-Provenienz und ergeben ohne erzwungenen Client `NOT EXECUTED` |
| HAProxy HTX | HTTP/1.1 ausgewählt; kein eigener TLS-/ALPN-H2- oder QUIC/H3-Frontend | Nativer HTX-Filter sieht Response-Payload-Blöcke; keine promotete Post-Commit-Aktion | Keine ausgewählte Client-Disconnect-API/Test | Keine belegte H2/H3-Stream-Reset-API im Filter | Kein ausgewählter Upstream-Reset-Fall | `http_end` ist die Response-EOS-/Finish-Grenze | Kein Modern-Protocol-Reuse-Test | Ein H2-Mux-Fund ist kein Connector-Frontend; QUIC/H3 ist nicht konfiguriert |
| Envoy ext_proc | HTTP/1.1-Listener ausgewählt; kein eigener H2- oder H3-Listener | `ext_proc` erhält Response-Header- und gestreamte Body-Callbacks; dies ist keine Client-Commit-Evidence | gRPC-Context-Cancel wird bereinigt, bleibt aber einem Downstream-Client-Abbruch nicht zuordenbar | Kein Downstream-H2/H3-Reset-Hook verdrahtet | Keine ausgewählte Upstream-Reset-Zuordnung | Response-Body-`end_stream` löst den Common-Finish-Pfad aus | Kein Modern-Protocol-Keep-Alive-Lauf | gRPC-Stream-Close ist kein Client-Reset; ein QUIC-Listener fehlt |
| Traefik native Middleware | Nur klartextiges HTTP/1.1-Entry-Point `web`; kein eigener H2/H3-Pfad | Der umschlossene `http.ResponseWriter` erfasst Header-/Body-Commit | `http.Hijacker` bleibt erhalten, aber kein kontrollierter Client-Abbruchpfad wird verwendet oder belegt | Keine H2/H3-request-lokale Reset-API verdrahtet | Kein ausgewählter Upstream-Abbruchfall | `responseWriter.finish()` liefert den Response-EOS-Callback | Kein Modern-Protocol-Reuse-Test | Nativer Harness hat kein TLS-Zertifikat, ALPN, UDP-/QUIC-Listener oder Alt-Svc-Konfiguration |
| lighttpd patched native | Nur gepatchter HTTP/1.x-Pfad; kein eigener H2/H3-Pfad | Gepinnter 1.4.84-Hook erhält geliehene Identity-Entity-Bytes in `http_chunk`, vor HTTP-Transfer-Framing | Keine ausgewählte Client-Abbruch-API/Test | Kein H2/H3-Stream-Reset-Hook | Kein ausgewählter Upstream-Abbruchfall | Entity-Hook hat monotone Offsets und eine Einmal-EOS-Sperre | Kein Modern-Protocol-Keep-Alive-Lauf | Echter P4-Hostlauf, Strict, gzip/br, HTTP/2 und Socket-Fault-Evidence bleiben nicht ausgeführt |

### Connector-spezifische Source-/API-Hinweise

- **Apache:** `output_filter` ist der ausgewählte Response-Callback. Sein
  HTTP/1.1-Strict-Source-Zweig kann `APR_ECONNABORTED` liefern, aber keine
  öffentliche H2-Reset-Operation oder versionsgebundener H2/H3-Patch ist
  verdrahtet. Filter-Entfernung und normaler Finish-Pfad sind nur
  Source-Cleanup; ein H2/H3-Client-Effekt wurde nicht beobachtet.
- **NGINX:** die nativen Header- und Body-Filter besitzen Commit- und
  `last_buf`-Behandlung. Der vorhandene Strict-Pfad ist ein Connection-Error-
  Pfad, keine öffentliche Per-Stream-Reset-API; kein Host-Patch ergänzt eine.
  Context-Cleanup ist lokal im Request-/Filter-Pfad, während H2/H3-
  Abort-/Reset- und Client-Effekte `NOT EXECUTED` bleiben.
- **HAProxy:** der ausgewählte native HTX-Filter verwendet `http_payload` und
  `http_end`. Er besitzt weder ein konfiguriertes H2/H3-Frontend noch eine
  öffentliche Reset-Operation oder einen Transport-Cancel-Runner. Sein
  Stream-Detach-/End-Cleanup belegt nicht, dass ein Client einen H2/H3-Reset
  gesehen hat.
- **Envoy:** die ausgewählte API ist gestreamtes `ext_proc`. Der Dienst
  finalisiert seine eigene Common-Transaktion bei EOS oder gRPC-Context-
  Cleanup, aber dieser Context unterscheidet keinen Downstream- von einem
  Upstream-Reset. Es gibt keinen engen Envoy-Filter oder versionsgebundenen
  Reset-Patch; ein Client-Reset-Effekt wird daher nicht behauptet.
- **Traefik:** die Middleware umschließt `http.ResponseWriter` und erhält
  `Hijack`, protokolliert nach Commit aber absichtlich `log_only` statt einen
  Abort oder Reset zu synthetisieren. Ein H2/H3-Entry-Point-Patch oder -Profil
  fehlt; `finish()` ist lokaler Transaction-Cleanup, kein Beweis eines beim
  Client sichtbaren Resets.
- **lighttpd:** der gepinnte 1.4.84-Patch liefert in `http_chunk` vor dem
  Transfer-Framing einen HTTP/1-Identity-Entity-Body-Hook mit
  Short-Write-/EAGAIN-Deduplizierung und einmaligem EOS. Er belegt keinen
  gzip/br-, H2/H3-, Client-Abbruch- oder Stream-Reset-Pfad. Ein nativer
  H2/H3-Reset braucht eine getrennte Host-API/einen Patch und echte
  Client-Evidence.

## Implementierungsstand für Transport-Härtung und Body-Phasen

Dieses Update hält die implementierten H1-Grenzen fest, ohne interne Fehler zu
client-sichtbaren Transportergebnissen zu promoten.

| Connector | zusätzlicher ausgewählter Pfad | erhaltene reale Beobachtung | bewusst nicht promotet |
|---|---|---|---|
| Traefik | nativer Middleware-ResponseWriter | unvollständiges `Write`/`ReadFrom` verhindert falsches EOS; Safe prüft einen H1-Follow-up auf demselben Socket | HTTP/1-Strict-Abbruch und jeder H2/H3-Reset |
| Envoy | nativer `ext_proc`-H1-Cancel-Probe | Client schließt nach einem Body-Byte; genau ein nicht zuordenbarer gRPC-Cancel und ein unabhängiger erfolgreicher Follow-up sind erforderlich | Downstream-Reset-Ursache und Strict-Ergebnis |
| HAProxy | P2 `http_payload`/`http_end`, P4 Response-Payload/EOS | frischer 3.2.21-Overlay-Build und realer nicht-promoteter Host-Smoke; der einblockige P2-Reply protokolliert null oder eine beobachtete Upstream-Anfrage ohne deren Reihenfolge zu belegen, Safe ist `log_only` | inkrementelles Request-Forwarding, Post-Commit-Strict-Abbruch, First-Byte- und clientseitiger No-Buffer-Nachweis |
| lighttpd | gepinnter 1.4.84-Entity-Body-Hook in `http_chunk` | geliehene Identity-Entity-Bytes kommen vor Transfer-Framing an; monotoner Offset und einmaliges EOS verhindern doppelte Inspektion bei Short Write/EAGAIN | echter P4-Hostlauf, Strict-Abbruch, gzip/br, HTTP/2 und Socket-Fault-Evidence |
| Apache / NGINX | vorhandene native Phase-4-Filter plus synchronisierte H1-Barriere | First Byte vor Upstream-EOS bleibt eine reale Host-Low-Latency-Beobachtung | Transport-Hardening-PASS: kein Raw-Client-/Fault-/Upstream-/Keep-Alive-/Parallel-Driver und keine kausalen Client-IDs |

### Gemeinsamer Transport- und Lifecycle-Vertrag

Common serialisiert jetzt ausschließlich begrenzte Transport-Metadaten:
Protokoll-/Stream-Identität, Connection-Reuse, Disconnect-/Cancel-Flags,
Reset-Akteur/-Code, Timeout-Phase, Write-Ergebnis, EOS-Status und
Cleanup-Grund. Der Source-Normalizer besitzt eine explizite Allowlist und
verwirft Payloads, Body-Snippets, Credentials, vollständige Rule-Messages und
rohes Netzwerkmaterial. Eine HTTP/3-Connection-ID bleibt nur als
`sha256:`-Token ohne rückrechenbaren Inhalt erhalten.

Full-Lifecycle-Läufe schreiben payload-freie Client-, Upstream-, Transport-
und Cleanup-Logs, Transport-Observations, Connection-Lifecycle,
Barrier-Events sowie ein Hash-only-Effective-Config-Manifest. Ein
Barrier-Event ist kanonisches Event-JSONL mit Connector, Integrationsmodus,
Run-ID, Transaktion, Rule, Phase, Event/Message und `transport_case_id`; es
enthält absichtlich kein Katalog-only-`case_id`. Eine Observation leitet ihre
Case-Beziehung ausschließlich aus der expliziten `transport_case_id` ab, die
ein zukünftiger kanonischer PASS mit der Case-ID gleichsetzen muss. Dadurch
entsteht keine Fixture-Namen-Inferenz.

Die Sidecars sind Inventar und allein nie Promotion-Evidence. Sie bleiben leer,
wenn einem vorhandenen Event die vollständige Client-/Case-/Transaktions- oder
Lifecycle-Korrelation fehlt. Ein künftiger Transport-PASS benötigt genau ein
kanonisches Event, eine Observation und einen Lifecycle-Record pro Korrelation,
gebundene Zähler sowie bei Strict eine client-sichtbar unvollständige Response
nach Commit und einen erfolgreichen unabhängigen Follow-up. Der Follow-up
besitzt einen eigenen begrenzten Korrelations-Token und denselben nicht
rückrechenbaren Target-Authority-Hash; er verwendet nicht den primären Token
erneut und persistiert keine rohe URL. Diagnostische
Reset-/Abort-Records ohne PASS bleiben `NOT EXECUTED` und werden nicht als
Erfolg umetikettiert.

## Status der Protokoll-Testinfrastruktur

Das verwaltete NGINX-Profil erzeugt jetzt eine ephemere lokale Test-CA und ein
getrennt davon ausgestelltes Leaf-Zertifikat mit einem Tag Laufzeit und den
SANs `localhost`/`127.0.0.1`. CA-Key, Leaf-Key, CSR, Zertifikate und
Serial-Datei werden beim Cleanup entfernt und niemals in kanonische Evidence
kopiert. Der Applicability-Record trennt außerdem `tcp_listener` und
`udp_listener` einschließlich ihrer gemeinsamen numerischen Portnummer und
führt letzteren als `quic_udp`. Das sind kontrollierte Konfigurationsfakten,
keine ausgehandelte Runtime-Evidence.

Folgende Punkte bleiben explizite `NOT EXECUTED`-Lücken:

- `http3_0rtt`: Es gibt keine 0-RTT-Konfiguration, keinen Replay-Test und
  keinen Test der Transaction-Semantik.
- Stream-Steuerung: Der verwaltete curl-Helper ist nur für Negotiation
  geeignet. Er kann selbst keinen stream-lokalen Reset/Cancel oder
  multiplexte Peer-Streams auslösen oder beobachten. Eine Sidecar liefert nur
  begrenzte ergänzende Provenienz und ist nie Reset-Runtime-Evidence;
  Reset-/Cancel-/Multiplexing-Fälle bleiben `NOT EXECUTED`, bis ein dedizierter
  Stream-Control-Client bereitgestellt ist.
- Moderne Protocol-Probes führen einen begrenzten `transport_case_id` in einem
  redigierten Request-Header und verlangen denselben Token in
  Client-Observation, Connector-Event und kanonischem Case-Result. Ein nur
  nachträglich beschriftetes Client-Artefakt kann keine andere Transaction
  promoten.

## Connector-/Protokollmatrix

Die Matrix beschreibt die aktuelle Source-/Harness-Grenze. „Vorhandene
H1-Evidence“ bezeichnet die getrennt auditierte HTTP/1.x-Lifecycle-Arbeit; sie
erstreckt sich nicht auf moderne Protokolle.

| Connector | Vorhandene H1-Evidence | H2 Downstream / TLS-ALPN | H2C | H3 Downstream / QUIC / Alt-Svc | Multiplexing, Reset, First Byte, No Buffer | Aktuelle Ausführung moderner Protokolle |
|---|---|---|---|---|---|---|
| Apache natives Modul | Ja, getrennt auditiert | `not_implemented`: gepinntes Connector-Profil baut/prüft weder `mod_http2` noch einen ALPN-Listener | `not_implemented` | `not_implemented`: kein auditierter H3-Modul-, QUIC-Listener- oder Alt-Svc-Pfad | `not_implemented`; Strict modelliert derzeit nur einen Connection-Abort | `NOT EXECUTED`; lokale Modul-Inventur hat kein `mod_http2`, lokaler H3-Client ist blockiert |
| NGINX natives Modul | Ja, getrennt auditiert | `implemented_not_asserted`: verwaltetes `h1-h2`-Profil kann v2 bauen, aber kein erzwungener ausgehandelter Lauf | `not_implemented` | `implemented_not_asserted`: verwaltetes H3-/QUIC-Profil und Alt-Svc-Template existieren, aber keine erzwungene H3-Beobachtung | `not_implemented`: keine Parallel-Stream-Isolation, kein request-lokaler Reset, kein ausgehandelter First-Byte-/No-Buffer-Nachweis | `NOT EXECUTED`; geprüfte Binärdatei ist nur H1, H3-Client ist blockiert |
| HAProxy HTX | Ausgewählter nativer Lifecycle-Pfad existiert | `not_implemented`: H2-Mux-Verfügbarkeit erzeugt kein TLS-/ALPN-Frontend oder eigenen Connector-Lauf | `not_implemented` | `not_implemented`: kein konfiguriertes QUIC-/H3-Frontend oder Alt-Svc-Profil | `not_implemented`: Filter hat keinen belegten H2-/H3-Reset oder Multiplex-Isolationspfad | `NOT EXECUTED`; kein qualifizierendes Frontend, lokaler H3-Client ist blockiert |
| Envoy ext_proc | Ja, getrennt auditiert | `not_implemented`: ausgewählter nativer Harness hat keinen TLS-/ALPN-H2-Listener | `not_implemented` | `not_implemented`: kein QUIC-Listener oder H3-Alt-Svc-Profil | `not_implemented`: gRPC-Stream-Close/-Cancel ist kein HTTP-Reset beim Client | `NOT EXECUTED`; kein eigener Modern-Protocol-Listener |
| Traefik native Middleware | Ja, getrennt auditiert | `not_implemented`: nativer Harness rendert nur den klartextigen Entry-Point `web`, ohne TLS-H2-Listener oder ALPN-Konfiguration | `not_implemented` | `not_implemented`: nativer Harness hat keinen H3-Entry-Point, UDP-/QUIC-Listener oder Alt-Svc-Konfiguration | `not_implemented`: keine beim Client sichtbare H2-/H3-Reset-API oder Multiplexing-Evidence | `NOT EXECUTED`; kein Connector-eigenes H2/H3-Profil, lokaler H3-Client ist blockiert |
| lighttpd patched native | Ja, getrennt auditiert | Legacy-H2-Status ist `unsupported_by_host_model`; detaillierter H2-Pfad ist `not_implemented`, weil der Patch H2 ablehnt | `not_implemented` | `not_implemented`: gepinnter Host hat keinen auditierten H3-/QUIC-/Alt-Svc-Pfad | `not_implemented`: kein dekodierter Modern-Protocol-Response-Hook, Reset- oder Isolationsvertrag | `NOT EXECUTED`; kein unterstützter nativer Modern-Protocol-Pfad |

Alle sechs Connectoren behalten für protokollspezifische Transaction-Isolation,
First-Byte-before-Response-End und No-Full-Response-Buffering
`not_implemented`, bis ein ausgehandelter H2- oder H3-Hostlauf die passende
Evidence liefert.

## Absichtlich nicht erhobene Claims

- Aus Build-Flag, H2-Mux, Library-Support, `Alt-Svc`-Template oder einem
  Protokollnamen in der Konfiguration wird kein H2-/H3-Downstream-`PASS`
  abgeleitet.
- H3-Negotiation, QUIC-/UDP-Beobachtung, QUIC-Version oder H3-Stream-ID werden
  nicht aus curl-Ausgabe erfunden. Der Client dieses Hosts hat kein
  `HTTP3`-Feature.
- Für keinen Connector wird H2C Prior Knowledge behauptet.
- TCP-Connection-Close, Apache-/NGINX-Connection-Abort, HAProxy-Filter-
  Teardown oder Envoy-ext_proc-/gRPC-Cancel werden nicht als `RST_STREAM`,
  H3-Reset oder striktes beim Client sichtbares Ergebnis gemeldet.
- Upstream-Protokoll wird nicht aus Downstream-Protokoll abgeleitet, und
  Connection-Evidence wird nicht als multiplexte Transaction-Isolation
  akzeptiert.
- Bestehende HTTP/1.1-Argumente zu First Byte und Buffering werden nicht auf
  H2 oder H3 promotet.

## Erforderliche Evidence vor einer Promotion

Damit ein Connector-/Protokoll-Paar über `NOT EXECUTED` hinausgeht, muss ein
echter nativer Hostlauf den erzwungenen verwalteten Client verwenden, die vier
Client-Artefakte erhalten und sie mit begrenzten Connector-Events korrelieren.
Er muss angefordertes und ausgehandeltes Protokoll, Transport, erforderliches
ALPN, keinen Fallback, Stream-Identität und Phasenaktion belegen. H3 benötigt
zusätzlich echte QUIC-/UDP-Beobachtung, QUIC-Version und nur Evidence über das
Vorhandensein einer Connection-ID. Ein strikter später Deny braucht sichtbaren
Post-Commit-Client-Zustand, unvollständige Response-/EOS-Semantik, einen
request-lokalen Reset und bei den Multiplexing-Fällen einen gesunden fremden
Stream. Bis dahin ist der Katalog ein Ausführungsplan, keine bestandene
Transportmatrix.
