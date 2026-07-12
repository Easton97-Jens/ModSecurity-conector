# Audit zur Promotion von Rule-Engine-Evidence

**Sprache:** [English](rule-engine-promotion-audit.md) | Deutsch

## Umfang und Evidence-Grenze

Dieser Audit kartiert ausgewählte echte Hostpfade auf `feature/all-connectors-no-crs-baseline`. Er promotet keine Capability selbst. Ein `PASS` ist nur gültig, wenn ein kanonischer Hostlauf ausgewählten Integrationsmodus, Transaction-ID, Rule-ID, Phase, angeforderte und tatsächliche Aktion sowie sichtbares Hostergebnis verbindet. Build, direkter Common-Aufruf, synthetische Barrier und normalisierte Summary ersetzen diese Evidence nicht.

| Connector | Echter Host-Einstieg | Engine-Begin | P1 | P2 | P3 | P4 append | EOS finish | Intervention | Hostaktion | Cleanup |
|---|---|---|---|---|---|---|---|---|---|---|
| Traefik native Middleware | `Middleware.ServeHTTP` im gepinnten lokalen Plugin | Request-lokale UDS-Session zu `traefik_engine_service` startet Common/libmodsecurity | Header vor Upstream | Gleiche Session, P2 403 ausgewählt | Wrapped Writer vor Commit | Nur aktueller `Write`-Chunk, kein Recorder | Close sendet EOS genau einmal | Common-Entscheidung pro Session | Pre-Commit-Status, Safe log_only | Idempotentes deferred Close; Reset/Cancel nicht ausgewählt |
| Envoy ext_proc | `processor.Service.Process` am echten gRPC-Listener | CGo-Common-/Runtime-Bridge, eine Transaction pro Stream | Reale Request-Header | Gestreamter Request-Body/EOS | Reale Upstream-Response-Header | Gestreamte Nachrichten, kein kompletter Service-Body | `end_of_stream` genau einmal | Common-Entscheidung pro Stream | Immediate Response vor Commit, Safe log_only | Stream-Close; Downstream-Reset/Cancel nicht ausgewählt |
| HAProxy HTX | Native `flt_ops`-Callbacks in `haproxy_modsecurity_htx_filter.c` | Per-Stream-`msc_new_transaction_with_id` | Reale 403- und 429-Antworten | Payload-Callbacks/EOS, kein ausgewähltes P2-Enforcement | Reale 403 vor Client-Commit | Payload-Callback, kein ausgewähltes P4-Ergebnis | `http_end` schützt finish | Stream-Transaction liest libmodsecurity | Nativer P1/P3-Reply-Pfad | Filter-detach gibt Stream-State frei |
| lighttpd patched native | Gepatchte URI-clean-/Modul-Hooks | `msconnector_runtime_transaction_begin` pro Request | Reale 403 und 429 | Gepatchter decoded Body, P2 403 | Response-start, P3 403 | Geliehene Identity-Entity-Bereiche in `http_chunk`; kein realer P4-Hostbefund | Request-EOS; Entity-EOS genau einmal | Common liest verfügbare Entscheidungen | `http_status_set_err()` vor Commit; Safe ist `log_only` | `handle_request_reset` beendet/zerstört genau einmal |
| Apache natives Modul | Native httpd-Hooks/Input-/Output-Filter | Per-Request-libmodsecurity-Transaction | Reale 403/429/Redirect | Input-Filter-EOS, P2 403 | P3 403/302 vor Commit | Begrenzte Brigades laufen weiter | EOS einmal | Begrenzte Common-Events | Pre-Commit-Reply, Safe log_only, Strict Abort | Normales Ende ausgeführt |
| NGINX natives Modul | Native Access-/Header-/Body-Filter | Per-Request-libmodsecurity-Transaction | Reale 403/429/Redirect | Nativer Pfad, P2 403 | P3 403/302 vor Commit | Begrenzte Response-Chains | last-buffer-EOS einmal | Begrenzte Common-Events | Pre-Commit-Reply, Safe log_only, Strict Abort | Normales Ende; HTTP/2 nicht anwendbar |

## Aktuelle ausgewählte Host-Evidence

- Kanonischer Aggregate-Lauf `full-lifecycle-rule-engine-all-final-20260712T083029Z`:
  Alle sechs Runner endeten mit Exit 0, vollständigen Artefakten und ohne
  FAIL/BLOCKED. PASS/NOT-EXECUTED-Zahlen: Apache 31/73, NGINX 31/73,
  HAProxy 13/91, Envoy 17/87, Traefik 16/88 und lighttpd 19/85.

- Jedes finale Connector-Verzeichnis enthält zusätzlich payload-freie
  Engine-Provenienz- und Accounting-Sidecars: `engine-version.txt`, SHA-256
  für Engine-Library und Ruleset, `transaction-counts.json` und
  `lifecycle-counters.json`. Sie inventarisieren nur den aktuellen Hostlauf
  und sind kein Promotion-Eingang.

- Traefik `rule-engine-traefik-final-20260712T071711Z`: reales P1/P2/P3-Enforcement und P4-Safe `log_only` mit passender Event-Metadatenbindung.
- Envoy `rule-engine-envoy-20260712T070435Z`: reales ext_proc P1/P2/P3, P3-Redirect und P4-Safe `log_only` über die CGo-Bridge.
- HAProxy `rule-engine-haproxy-20260712T070510Z`: native P1 403, P1 429 und P3 403. P2/P4 werden nicht aus Callbacks allein promotet.
- lighttpd `rule-engine-lighttpd-20260712T070545Z`: gepatchter Host mit P1 403/429, P2 403 und P3 403; Response-Body-P4 bleibt nicht ausgeführt.
- Apache `rule-engine-apache-20260712T072808Z`: P1/P2/P3 sowie getrennte P4-Safe-`log_only`- und Strict-`connection_aborted`-Events.
- NGINX `rule-engine-nginx-retry-20260712T073639Z`: entsprechende P1/P2/P3- und getrennte P4-Safe-/Strict-Ergebnisse. `nginx -V` enthält kein `--with-http_v2_module`; HTTP/2 ist für diesen Build `NOT_APPLICABLE`.

Alle zitierten Raw-Events enthalten nur Metadaten: keine Request-/Response-Payloads, Matched Values, vollständigen Rule Messages, Authorization-Werte oder Cookies.

## HTTP/2- und HTTP/3-Protokollstatus

Der Katalog zur Transport-Härtung und der payload-freie verwaltete Client sind
vorhanden, aber dieser Report promotet kein Modern-Protocol-Lifecycle-Ergebnis.
Lokales `curl 8.18.0` unterstützt HTTP/2 und hat kein HTTP/3; erzwungene
H3-Arbeit ist daher mit `client_http3_unsupported` `BLOCKED`. Das ist ein
Umgebungsblocker, keine Connector-Klassifikation. Die geprüfte
NGINX-Laufzeitbinärdatei hat weder `--with-http_v2_module` noch
`--with-http_v3_module`; die HAProxy-Binärdatei listet einen H2-Mux, aber keinen
SSL-/QUIC-Build; und Apache lädt kein `mod_http2`.

Moderne Probes führen jetzt einen begrenzten `transport_case_id` in einem
redigierten Request-Header; ein zukünftiger PASS muss ihn in Client-Observation,
Connector-Event und Case-Result übereinstimmend führen. Der verwaltete
curl-Helper dient nur der Negotiation und kann Strict-/Reset-/Cancel- oder
Multiplexing-Evidence ohne dedizierten Stream-Control-Client nicht promoten.
Der NGINX-Profil-Harness stellt ephemeres lokales CA-/Leaf-Material und
getrennte TCP-/UDP-Listener-Fakten bereit; H3-0-RTT bleibt `NOT EXECUTED`.

Folglich bleiben alle H2-/H2C-/H3-Phasen-, Multiplexing-, Stream-Reset-,
First-Byte- und No-Full-Buffer-Fälle `NOT EXECUTED`, bis ein zukünftiger
erzwungener, ausgehandelter Hostlauf korrelierte Client- und Connector-Evidence
liefert. Ein Build-Profil, H2-Mux, `Alt-Svc`, Connection-Abort oder interner
Service-Stream-Close ist kein H2-/H3-`PASS` und kein request-lokaler
Stream-Reset. Der [Audit zur Transport-Härtung](transport-hardening-audit.de.md)
enthält die genaue Connector-Matrix und die Nicht-Claims.

## Verbleibende Grenzen

- Traefik- und Envoy-Strict sind `NOT EXECUTED`: Ein beim Client sichtbarer Post-Commit-Reset ist nicht belegt. Ein interner Service-Stream-Close ist kein Nachweis.
- HAProxy-P2/P4-Enforcement, Late Action, First Byte und No-Full-Buffer bleiben `NOT EXECUTED`; native Callbacks sind keine synthetische Evidence.
- lighttpd-P4 bleibt `NOT EXECUTED`: Der ausgewählte Decoded-Identity-Entity-Hook, Cursor-, Short-write/EAGAIN-Behandlung und einmaliges EOS sind vorhanden, aber ein realer P4-Hostlauf und client-sichtbare Strict-Evidence fehlen weiter.
- Apache und NGINX beanspruchen aus diesen Normalpfadläufen nicht alle Katalogfälle für Cleanup, Disconnect, Body-Limit, Content-Type oder Transport.

Ausgewählte zuvor nicht promotete Lifecycle-Fälle besitzen jetzt echte Host- und libmodsecurity-Rule-Engine-Evidence. Verbleibende `NOT EXECUTED`-Fälle stehen weiterhin für nicht verifiziertes oder nicht implementiertes Verhalten und wurden nicht aus synthetischen Artefakten promotet.
