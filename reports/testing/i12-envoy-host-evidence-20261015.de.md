# I12 Envoy: Hostmessungen und verbleibende Abnahme

**Sprache:** [English](i12-envoy-host-evidence-20261015.md) | Deutsch

Status: **PARTIAL**. Die vollständige Abnahme aller 284 Originalfälle ist nicht erreicht.

Quellrevision der nativen/Hostevidenz: `f27eb59b53beff6f65384fc2e5037881a3052c01`.

Die JSON-Begleitdatei erhält alle 284 exakten Original-IDs und ihre Baseline-Ergebnisse. Neue synthetische Hostproben haben eigene Identitäten; nur separat validierte, einzeln freigegebene vollständige Nachweispakete qualifizieren Originalfälle.

[i12-envoy-host-evidence-20261015.json](i12-envoy-host-evidence-20261015.json)

## Drei getrennte Routenergebnisse

| Route | Original IDs | Lifecycle PASS | Config PASS | Without lifecycle | Original oracles | Open |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| envoy-ext-proc | 117 | 5 | 0 | 112 | 51 | 46 |
| envoy-ext-authz-request | 94 | 1 | 8 | 93 | 40 | 39 |
| envoy-ext-authz-response-companion | 73 | 1 | 0 | 72 | 34 | 33 |

Exakt qualifizierte IDs:

- `I12::envoy-ext-proc::NEED-request-eos-once`
- `I12::envoy-ext-proc::NEED-client-exit-signal`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-authz-request::NEED-request-eos-once`
- `I12::envoy-ext-authz-response-companion::NEED-lease-claim`

Die erhaltene Baseline enthielt 281 IDs ohne vollständige Hostabnahme: 8 reine Konfigurations-PASS und 273 unqualifizierte Fälle. Von den ursprünglichen 125 offenen Oracles waren 3 aufgelöst und 122 offen. Die erhaltene Baseline und ihre physischen Quellen wurden mit den aktuellen zentralen Validatoren erneut geprüft. Dieser Envoy-Task änderte keinen gemeinsamen Validator. Neue Qualifikationen stehen separat mit ihren vollständigen Receipts im aktuellen Stand oben.

## Neue physische Hostmessungen

Jede Zeile ist eine gemessene Probe, kein Lifecycle-Verdikt. HTTP/Framing, Transportabschluss, native Phasen und Cleanup bleiben getrennt. Frühere Fehlversuche und Wiederholungen bleiben sichtbar. Bei Envoy ext_proc kann bereits vor einem P2-Deny ein unvollständiger Backendrequest beginnen.

| Batch / probe | Route | Runner exit | Target HTTP | Neighbor HTTP | Backend starts | Overlap |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| host-v2/ext-proc-p1-deny | envoy-ext-proc | 77 | 403 | None | 0 | None |
| host-v2/ext-proc-streaming | envoy-ext-proc | 77 | 200 | 200 | 2 | False |
| host-v2/ext-proc-p2-deny | envoy-ext-proc | 0 | 403 | 200 | 2 | False |
| host-v2/ext-proc-p3-deny | envoy-ext-proc | 77 | 403 | 200 | 2 | False |
| host-v2/ext-proc-p4-deny-safe | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-proc-request-reject | envoy-ext-proc | 0 | 403 | 200 | 2 | False |
| host-v2/ext-proc-request-partial | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-proc-response-partial | envoy-ext-proc | 77 | 200 | None | 1 | None |
| host-v2/ext-proc-response-reject | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-proc-mime-out | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-request-streaming | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-request-p1-deny | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-v2/ext-authz-request-p2-deny | envoy-ext-authz-request | 77 | None | None | None | None |
| host-v2/ext-authz-request-host-reject | envoy-ext-authz-request | 77 | 413 | None | 0 | None |
| host-v2/ext-authz-request-host-partial | envoy-ext-authz-request | 77 | 503 | None | 0 | None |
| host-v2/ext-authz-request-request-reject | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-v2/ext-authz-request-request-partial | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-streaming | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-p3-deny | envoy-ext-authz-response-companion | 77 | 403 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-p4-deny-safe | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-response-partial | envoy-ext-authz-response-companion | 77 | 200 | None | 1 | None |
| host-v2/ext-authz-response-companion-mime-out | envoy-ext-authz-response-companion | 77 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-response-reject | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-v3/ext-authz-request-concurrent | envoy-ext-authz-request | 0 | 200 | 200 | 2 | True |
| host-v3/ext-proc-concurrent | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-v3/ext-authz-response-companion-concurrent | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-v3/ext-proc-streaming | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v3/ext-proc-p1-deny | envoy-ext-proc | 0 | 403 | 200 | 1 | False |
| host-v3/ext-proc-p3-deny | envoy-ext-proc | 77 | 403 | 200 | 2 | False |
| host-v3/ext-proc-response-partial | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-faults-v2/ext-authz-response-companion-cancel | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-faults-v2/ext-proc-cancel | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-faults-v2/ext-proc-grpc-unavailable | envoy-ext-proc | 77 | 500 | 500 | 0 | False |
| host-faults-v2/ext-authz-response-companion-missing-lease | envoy-ext-authz-response-companion | 0 | 503 | 503 | 2 | False |
| host-faults-v2/ext-authz-response-companion-expired-lease | envoy-ext-authz-response-companion | 0 | 503 | 200 | 2 | False |
| host-faults-v2/ext-authz-request-grpc-unavailable | envoy-ext-authz-request | 77 | 500 | 500 | 0 | False |
| host-final/ext-authz-request-grpc-unavailable | envoy-ext-authz-request | 77 | 500 | 500 | 0 | False |
| host-final/ext-proc-grpc-unavailable | envoy-ext-proc | 0 | 500 | 500 | 0 | False |
| host-final/ext-proc-incomplete-response | envoy-ext-proc | 77 | 502 | 200 | 2 | False |
| host-final/ext-authz-response-companion-incomplete-response | envoy-ext-authz-response-companion | 77 | 502 | 200 | 2 | False |
| host-final/ext-proc-p3-deny | envoy-ext-proc | 0 | 403 | 200 | 2 | False |
| host-final/ext-authz-request-p2-deny | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-final/ext-authz-request-host-reject | envoy-ext-authz-request | 0 | 413 | 200 | 1 | False |
| host-final/ext-authz-response-companion-p3-deny | envoy-ext-authz-response-companion | 0 | 403 | 200 | 2 | False |
| host-final/ext-authz-request-host-partial | envoy-ext-authz-request | 77 | 503 | 200 | 1 | False |
| host-postcommit/ext-authz-response-companion-incomplete-response | envoy-ext-authz-response-companion | 77 | 200 | 200 | 2 | False |
| host-postcommit/ext-authz-request-grpc-unavailable | envoy-ext-authz-request | 0 | 500 | 500 | 0 | False |
| host-postcommit/ext-proc-incomplete-response | envoy-ext-proc | 77 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-streaming-0 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-content-type-present-1 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-charset-present-2 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-process-partial-3 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-streaming-4 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-content-type-present-5 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-charset-present-6 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-mime-scope-in-7 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-mime-scope-out-8 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-client-response-bytes-10 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-process-partial-9 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-client-exit-signal-11 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-neighbor-connection-stream-12 | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-proc-need-independent-neighbor-stream-13 | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-request-need-request-multiple-chunks-14 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-request-content-type-present-15 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-request-charset-present-16 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-client-response-bytes-17 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-neighbor-connection-stream-18 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-request-need-host-413-before-engine-20 | envoy-ext-authz-request | 0 | 413 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-complete-sample-19 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-native-engine-403-21 | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-native-body-limit-22 | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-native-body-limit-23 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-host-buffer-not-engine-limit-24 | envoy-ext-authz-request | 0 | 413 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-host-buffer-not-engine-limit-25 | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-host-buffer-not-engine-limit-26 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-allow-27 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-response-streaming-28 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-cancel-29 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-response-companion-need-incomplete-framing-31 | envoy-ext-authz-response-companion | 77 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-client-response-bytes-30 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-backend-count-exclusion-32 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-neighbor-connection-stream-33 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-response-companion-need-missing-correlation-34 | envoy-ext-authz-response-companion | 0 | 503 | 503 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-lease-expiry-35 | envoy-ext-authz-response-companion | 0 | 503 | 200 | 2 | False |
| companion-retake-original-v1/original-envoy-ext-authz-response-companion-need-allow-0 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| fault-host-v1/ext-proc-drop-response-eos | envoy-ext-proc | 77 | 200 | 200 | 2 | False |

## Gerichtete Response-EOS-Fehlerprobe

Die gerichtete echte `envoy-ext-proc`-Probe entfernt ausschließlich das leere Response-EOS des Zielstreams und führt danach den tatsächlichen gRPC-Half-Close aus. Die Engine liefert API-Status 14. Envoys eigener Trace bindet den empfangenen Trailer, Remote-Close und Fehlercallback mit Status 14 über Ziel-Nonce, Connection-ID und Stream-ID an denselben HTTP-Stream; danach folgt ein Reset, nachdem HTTP-200-Header bereits gesendet waren. Der Proxy beobachtet weiterhin keinen Wire-Status und erfindet daraus keinen Erfolg. Der Zielclient erhält den exakten 96-Byte-Prefix in Chunks 64+32, aber keinen terminalen Nullchunk, und endet mit Fehler. Nativ laufen P1–P3; P4 und Response-EOS fehlen, `runtime_finish` wird einmal versucht und liefert 0, während Logging, Free und Cleanup je einmal beobachtet werden. Der Nachbarstream schließt mit P1–P4 und erfolgreichem Finish. Runner-Exit 77, Controller-Exit 1, Client-Exit 1 und `new_lifecycle_pass=0` bleiben erhalten.


`None` bezeichnet fehlende Messung. Ein unterer Backend-Zähler bleibt in JSON ausdrücklich als `request_count_is_lower_bound` gekennzeichnet. Runner-Exit 0 ist keine Oracle-Abnahme; Exit 77 bleibt Nicht-PASS.

## Native Identität und Nachweiskette

- Quellrevision der nativen/Hostevidenz: `f27eb59b53beff6f65384fc2e5037881a3052c01`.
- Envoy: `b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1/Clean/RELEASE/BoringSSL`.
- Envoy image SHA256: `002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8`.
- SDK: `ModSecurity v3.0.14 (Linux)`; SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`.
- Go: `go1.27.2`; `go.mod`: `go 1.26.9`; `golang.org/x/net v0.61.0`.

Die frische C17-/C++17-/CGo-Erzeugung nutzt dieselbe Envoy-Capture-Variante und den gemeinsamen Observer. Quellkopie, acht Overlays, geladene Images, effektive Konfiguration, getrennte echte Clients/Backend, native Scopes, tatsächliche EOS-Argumente, P1–P4, Logging/Free, Finish-Aufrufe und physische Eventlogs sind hashgebunden. Pro normaler Transaktion sind native Logging/Free und logischer Finish-Übergang jeweils einmal zu prüfen; zwei idempotente Common-Finish-Aufrufe sind kein doppelter Übergang.

Eine abgeschlossene HTTP-Entity kann von einem TCP-Reset gefolgt werden. Ein beobachteter lokaler HTTP/2-Reset belegt keinen Remote-`grpc-status`. Fehlt dieser Status, bleibt erfolgreicher gRPC-Abschluss false/unknown. Authorization-Erfolg braucht explizite Trailer und den zugehörigen Streamabschluss.

## Request-Sample und Response-Companion

`max_request_bytes` ist die Hostbuffer-Grenze. Die nativen Limitproben verwenden eine vollständige Probe unterhalb der größeren Hostkapazität. Host-413 vor der Engine, verworfene Partial-Metadaten mit technischem gRPC-Fehler, native 403-Intervention und echte Backendwirkung werden getrennt erfasst. Mehrere Client-Schreibvorgänge sind bei Authorization/Check keine mehreren Engine-Bodycallbacks.

Der Companion hat eigene Läufe für P3/P4, Streaming, native Response-Limits, fehlende/abgelaufene Leases und Cancellation. Die gleiche HTTP-Receipt qualifiziert Request und Response nicht automatisch gemeinsam. Zeitliche Client-Überlappung belegt nur die beobachtete Parallelität; eine mehrdeutige gRPC-Zuordnung bleibt unbekannt.

## Cleanup und Isolation

UID/GID 65534, Capabilities 0, NoNewPrivs 1 sowie private Netzwerk-/PID-/Mount-Namespaces und die Listenergrenzen bleiben erhalten. Ein alter v5-Lauf meldete einen fremden Traefik-Prozess als Survivor; dessen Identität und Namespace-ID sprechen für eine Wiederverwendung der Namespace-ID nach Ende des Envoy-Laufs. Dieser Prozess wurde nicht signalisiert; der ursprüngliche Exit 77 bleibt erhalten. Die Envoy-spezifische Controllerkopie hält jetzt einen positiv an die eigene Init-Identität gebundenen Namespace-FD bis nach Cleanup offen, validiert die Identität vor/nach Open und behandelt nicht belegbare Ownership als Fehler.

## Verifikation und Grenzen

Native/CGo Go `./...`, Race `./...` und Vet `./...`: PASS. Die historische f27-Evidenz enthält 32 gemeinsame native Observer-Kontrollen; der aktuelle a622-Native-v3-Lauf enthält 34 PASS. Die aktuelle vollständige Envoy-Evidenzsuite hat 232 PASS ohne Skip. Neue Kontrollen prüfen unveränderte IDs/Oracles, physische Hashes, fehlende gRPC-Trailer, geordnete Streamweiterleitung, versiegelte Fault-Fixtures, Quell-/Binary-Austausch, Backend-Framing und Namespace-Ownership-Rennen. Exakte Kommandos, Ergebnisse und Loghashes stehen in den referenzierten Receipts.

Offen bleiben die vollständige unabhängige Oracle-/Original-ID-Abnahme, direkte native MIME-/Charset-Auswahl, vollständig korrelierte parallele gRPC-Terminalstatus, gezielt fehlende/wiederholte Hostcallbacks, alle physischen Event-Sink-Fehler und der vollständige Observer-Stop/Restart-Vertrag. P4 Strict wird nicht als unterstützt oder abgenommen behauptet. Unit-, Native- und Race-Erfolg ersetzen diese Hostnachweise nicht.

## Unabhängige Oracle-Prüfung und Original-ID-Retakes

Alle 125 Original-Oracles wurden einzeln gegen Quell-, SDK- und Hostsemantik geprüft. Die drei Envoy-eigenen Reviewdateien erhalten die Original-Oracles unverändert. Konkrete neue Fixture-/Erwartungsvorschläge stehen getrennt von kanonischer Auflösung und Hostabnahme:

| Route | Reviewed original oracles | New source proposals | Retaken original IDs |
| --- | ---: | ---: | ---: |
| envoy-ext-proc | 51 | 14 | 14 |
| envoy-ext-authz-request | 40 | 10 | 10 |
| envoy-ext-authz-response-companion | 34 | 9 | 9 |

Neue individuell geprüfte Lifecycle-PASS:

- `I12::envoy-ext-proc::NEED-client-exit-signal` — `953ddad0f0a52ec0e8c68ba84c75e6ccb8006b901778f45c5047b2817aeacb4b`.
- `I12::envoy-ext-proc::NEED-client-response-bytes` — `c57174a568ec4afeabcd24a8635b93d1e099adf9203895af753774e7960ba012`.
- `I12::envoy-ext-proc::NEED-request-streaming` — `2704758dfbf0b216cd0f4fa22fb0ce2623a36659e2952459e68c5fb43e9772cd`.
- `I12::envoy-ext-proc::NEED-response-streaming` — `0f804e6cbb4712823765f323e392dc0623ad2a23495f6bd8c06e8424cd20a398`.

Nicht erneut freigegeben, weil die sichtbaren Authorization-Trailer nicht streamgebunden sind und der Remote-gRPC-Status unbekannt bleibt:

- `I12::envoy-ext-authz-request::NEED-complete-sample`.
- `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`.
- `I12::envoy-ext-authz-request::NEED-client-response-bytes`.
- `I12::envoy-ext-authz-response-companion::NEED-allow`.

Der eigene aktuelle Abnahmestand hat 7 aufgelöste und 118 offene Original-Oracles. Der zentrale Baseline-Bestand bleibt unverändert.

Jeder neue Vorschlag hat eine explizite Original-ID-/Fixture-Bindung und physische Quellreferenzen. Die zugehörigen Retakes bleiben bis zur vollständigen Prüfung aller fallbezogenen Nachweise unqualifiziert; auch ein passendes HTTP-Ergebnis löst kein Original-Oracle automatisch auf.

Die Postcommit-Proben synchronisieren den absichtlichen Backend-EOF mit einer tatsächlichen Client-Receipt des ersten Entitybytes. ext_proc und Companion liefern jeweils HTTP 200/32 Bodybytes vor unvollständigem Chunk-Framing. Der Client endet mit Fehler; der erste physische Common-Fehler bleibt protocol_error mit originalem/sichtbarem Status 200 und gesetztem Commit. Free/Cleanup sind beobachtet; ein erfolgreicher runtime_finish wird dafür nicht erfunden.

Die vollständige Bilingual-Prüfung endet mit Exit 2 wegen 22 unveränderter Links in den nicht initialisierten Framework-Gitlink dieses Worktrees. Die Parent-Sprachverträge und sämtliche neuen Dokumentlinks bestehen die abgegrenzte API-Prüfung. Das ist kein globales Bilingual-PASS. Alle 2.105 Buildquellen wurden unabhängig aus dem archivierten Parent und den Capture-Overlays rekonstruiert; Fall-/Routen-/Parent-Austausch und der äußere Timeoutpfad haben eigene Negativkontrollen.


## Ergänzende Hostproben auf der aktuellen Base

Die separat hashgebundene Ergänzung prüft die Base `a62296fb57263f9be18c6ac879e36e0ab2a9935c` mit dem von der Base geforderten Go 1.27.2 für den Enginebuild, x/net 0.61.0, ModSecurity 3.0.14 und Envoy 1.39.1. Die Hostumgebung meldet separat das installierte Go 1.27.3; diese Messung belegt keinen Enginebuild. Der frühere Enginebuild mit Go 1.27.3 und seine drei Hostproben bleiben als überholte, nicht qualifizierende Evidenz erhalten. Ein weiterer verworfener Build scheiterte vor dem Hoststart technisch an der Mischung aus Go-1.27.2-Treiber und Go-1.27.3-Compiler; Receipt und Fehlerlog bleiben hashgebunden erhalten. Drei frühere Admission-Fehler bleiben Exit 77 mit unbekannter Hostausführung und ohne Cleanup-Behauptung erhalten. Drei neue Streaming-Proben haben Runner-Exit 0 und physisch geprüftes Cleanup. Je Route sind Zielrequest/-response 95/96 Bytes, Nachbarrequest/-response 6/7 Bytes und zwei Backendrequests belegt. Die folgende Tabelle erhält den tatsächlich belegten Authorization-Status je Route und Client. Nicht zuordenbare Trailer bleiben unbekannt und erfolgreicher Abschluss false. Der fehlende Process-gRPC-Status bleibt unbekannt und erfolgreicher Abschluss false. Diese Proben qualifizieren keine Original-ID: `new_lifecycle_pass=0`. Die historischen Messungen, Retakes, Oracle-Zähler und die Quellrevision der bisherigen nativen Evidenz bleiben erhalten.

- **`envoy-ext-proc`:** Request-Callbacks `64/31/0-EOS` und Response-Callbacks `64/32/0-EOS`, P1–P4-Regeln `1900111–1900114`, exakt 95/96 Zielbytes und vollständiges Finish/Cleanup für Ziel und Nachbar sind physisch belegt. Beide Process-Streams enden mit lokalem HTTP/2-Reset 2; ihr Remote-gRPC-Status bleibt unbekannt. Der Nachbar lief sequenziell. Reject/ProcessPartial, Cancellation, fehlende oder wiederholte Callbacks sowie native MIME-/Charset-Auswahl werden durch diese Probe nicht belegt.
- **`envoy-ext-authz-request`:** Envoy puffert mit `max_request_bytes=4096`, `allow_partial_message=false`; die Engine erhält genau ein vollständiges 95-Byte-Sample mit EOS unter ihrem nativen 1024-Byte-Reject-Limit. Kein Host-413, natives Reject/ProcessPartial, Regelblock oder Runtimefehler wird ausgelöst. Ziel und Nachbar liefern HTTP 200 und je einen vollständigen Backendrequest. Die sichtbaren Authorization-Status-0-Trailer sind nicht streamgebunden und bleiben für beide Rollen unbekannt; der Target-Process ist nicht sicher zugeordnet, der Nachbar endet mit lokalem Reset 2.
- **`envoy-ext-authz-response-companion`:** Dieselbe serverseitige Decision-ID bindet Lease-Ausgabe und -Annahme an P1–P4; P3 endet vor dem Common-Commit, der seinerseits vor den Response-Bodycallbacks und P4 liegt. Response-Callbacks `64/32/0-EOS`, Finish und Cleanup laufen für zwei getrennte native Scopes. Der Zielclient erhält die vollständige HTTP-200-Entity mit 96 Bytes und danach TCP-Reset `errno 104`; der Nachbar erhält 7 Bytes und EOF. Authorization bleibt für beide Rollen unbekannt, Target-Process unbekannt und Nachbar-Process lokaler Reset 2. Fehlende/abgelaufene Leases, Observer-/gRPC-Abbruch, technische erste Fehlerursache und Strict-P4-Fähigkeit bleiben offen.

| Route | Client | Authorization grpc-status | Successful completion |
| --- | --- | --- | --- |
| envoy-ext-proc | target | unknown | false |
| envoy-ext-proc | neighbor | unknown | false |
| envoy-ext-authz-request | target | unknown | false |
| envoy-ext-authz-request | neighbor | unknown | false |
| envoy-ext-authz-response-companion | target | unknown | false |
| envoy-ext-authz-response-companion | neighbor | unknown | false |

## Physische Referenzen

- `baseline`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/baseline-envoy-reconciliation.json` — SHA256 `e5bc09638b139351aa9816df79faffcb8923117f1bd74ca59fdd7b21021ac469`.
- `native`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/native-v2/native-build/receipt.json` — SHA256 `fd429f2d49a76c71233eb581992a24fc81ac47b1ca8662fd3892be046eee16b0`.
- `validation`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/ci/final-envoy-controls-232-base-a622-v7.json` — SHA256 `deca197b45205e7670480a821c03added0bd5dc302f3e03524b409c83011f9d4`.
- `I12__envoy-ext-proc__NEED-client-exit-signal`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v11/I12__envoy-ext-proc__NEED-client-exit-signal.json` — SHA256 `953ddad0f0a52ec0e8c68ba84c75e6ccb8006b901778f45c5047b2817aeacb4b`.
- `I12__envoy-ext-proc__NEED-client-response-bytes`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v11/I12__envoy-ext-proc__NEED-client-response-bytes.json` — SHA256 `c57174a568ec4afeabcd24a8635b93d1e099adf9203895af753774e7960ba012`.
- `I12__envoy-ext-proc__NEED-request-streaming`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v11/I12__envoy-ext-proc__NEED-request-streaming.json` — SHA256 `2704758dfbf0b216cd0f4fa22fb0ce2623a36659e2952459e68c5fb43e9772cd`.
- `I12__envoy-ext-proc__NEED-response-streaming`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v11/I12__envoy-ext-proc__NEED-response-streaming.json` — SHA256 `0f804e6cbb4712823765f323e392dc0623ad2a23495f6bd8c06e8424cd20a398`.
- `oracles-ext-proc`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-ext-proc.json` — SHA256 `a25fe9a5808df508a5182cedf343166ccafebefabaeaa7d7898a4eb6d2c61a2f`.
- `oracles-authz-request`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-authz-request.json` — SHA256 `00299799b27918783dff71e44720059d23bc539570f71c4e37a4b6d91ac08ddf`.
- `oracles-companion`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-companion.json` — SHA256 `fe98c20ebd63ad455a34e2a65dbced229d43cab63755d70e743a18abdaf9f1b3`.
- `oracles-companion-allow-retake`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-companion-allow-retake.json` — SHA256 `6a00134155aea20f146cf7be2fe7c37b4517a378529af609e8b1fc7af9205d63`.
- `review-release-host-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-v2.json` — SHA256 `c07e6c0825d15b1d80adf88519e3e4539d2378e7c0adf811ad29940771962155`.
- `review-release-host-v3`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-v3.json` — SHA256 `5379f6fd2129ac7c411f89fcfa7487bf16db826e15dbc397523144f97f657ce7`.
- `review-release-host-faults-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-faults-v2.json` — SHA256 `433d338c4286a03c3f0d2b8618e3b719715685695939adc252a0eba1b5ab5406`.
- `review-release-host-final`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-final.json` — SHA256 `36f9d21db12bca52562c53b0654cedfaefc56096f8f2410b6940d442f3cc07f7`.
- `review-release-host-postcommit`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-postcommit.json` — SHA256 `6add24def432637fb8d701fe98f8b2890d473992a38939a2f27bdb21d672f27e`.
- `review-release-host-originals`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-originals.json` — SHA256 `2de58afa0962ac01258a7fd1a9fac9553eb97f54543c0e5d303668477101d7fd`.
- `review-companion-retake-v1`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-companion-retake-v1.json` — SHA256 `8e343b65be316565c222163d95c812a337b3e3de66d2544bdb8520bbffe79869`.
- `review-fault-host-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-fault-host-v2.json` — SHA256 `862c108d07b69ccfdaa6c8dd51493a03361c8ad1f3c85b6d4a704b56c077dc3e`.
- `current_base_supplement`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/current-base-evidence-v1.json` — SHA256 `a2f6178f4a6e0434016c4de9ef292c78dd3196c250d58c12678f7e0ca19e0e95`.

Die Referenzen liegen im task-eigenen externen Speicher; der PR enthält nur Quellcode und bereinigte Metadaten, keine Binaries, Caches, privaten Schlüssel oder Rohpayloads.
