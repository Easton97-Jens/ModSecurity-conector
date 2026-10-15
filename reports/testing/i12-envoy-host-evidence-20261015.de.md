# I12 Envoy: Hostmessungen und verbleibende Abnahme

**Sprache:** [English](i12-envoy-host-evidence-20261015.md) | Deutsch

Status: **PARTIAL**. Die vollständige Abnahme aller 284 Originalfälle ist nicht erreicht.

Basis und Produktvertrag: `f27eb59b53beff6f65384fc2e5037881a3052c01`.

Die JSON-Begleitdatei erhält alle 284 exakten Original-IDs und ihre Baseline-Ergebnisse. Neue synthetische Hostproben haben eigene Identitäten; nur separat validierte, einzeln freigegebene vollständige Nachweispakete qualifizieren Originalfälle.

[i12-envoy-host-evidence-20261015.json](i12-envoy-host-evidence-20261015.json)

## Drei getrennte Routenergebnisse

| Route | Original IDs | Lifecycle PASS | Config PASS | Without lifecycle | Original oracles | Open |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| envoy-ext-proc | 117 | 3 | 0 | 114 | 51 | 48 |
| envoy-ext-authz-request | 94 | 2 | 8 | 92 | 40 | 38 |
| envoy-ext-authz-response-companion | 73 | 1 | 0 | 72 | 34 | 33 |

Exakt qualifizierte IDs:

- `I12::envoy-ext-proc::NEED-request-eos-once`
- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-authz-request::NEED-request-eos-once`
- `I12::envoy-ext-authz-request::NEED-complete-sample`
- `I12::envoy-ext-authz-response-companion::NEED-lease-claim`

Die Baseline enthielt 281 IDs ohne vollständige Hostabnahme: 8 reine Konfigurations-PASS und 273 unqualifizierte Fälle. Von den ursprünglichen 125 offenen Oracles waren 3 aufgelöst und 122 offen. Diese Eingaben wurden mit den unveränderten zentralen Validatoren und physischen Quellen erneut geprüft. Neue Qualifikationen stehen separat mit ihren vollständigen Receipts im aktuellen Stand oben.

## Neue physische Hostmessungen

Jede Zeile ist eine gemessene Probe, kein Lifecycle-Verdikt. HTTP/Framing, Transportabschluss, native Phasen und Cleanup bleiben getrennt. Frühere Fehlversuche und Wiederholungen bleiben sichtbar. Bei Envoy ext_proc kann bereits vor einem P2-Deny ein unvollständiger Backendrequest beginnen.

| Batch / probe | Route | Controller exit | Target HTTP | Neighbor HTTP | Backend starts | Overlap |
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

`None` bezeichnet fehlende Messung. Ein unterer Backend-Zähler bleibt in JSON ausdrücklich als `request_count_is_lower_bound` gekennzeichnet. Controller-Exit 0 ist keine Oracle-Abnahme; Exit 77 bleibt Nicht-PASS.

## Native Identität und Nachweiskette

- Parent: `f27eb59b53beff6f65384fc2e5037881a3052c01`.
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

Native/CGo Go `./...`, Race `./...`, Vet `./...` und 32 gemeinsame native Observer-Kontrollen: PASS. 79 bestehende Vertragskontrollen: PASS mit einem Setup-Skip des separat erfolgreich ausgeführten Observers. Neue Kontrollen prüfen unveränderte IDs/Oracles, physische Hashes, fehlende gRPC-Trailer, Quell-/Binary-Austausch, Backend-Framing und Namespace-Ownership-Rennen. Exakte Kommandos, Ergebnisse und Loghashes stehen in den referenzierten Receipts.

Offen bleiben die vollständige unabhängige Oracle-/Original-ID-Abnahme, direkte native MIME-/Charset-Auswahl, vollständig korrelierte parallele gRPC-Terminalstatus, gezielt fehlende/wiederholte Hostcallbacks, alle physischen Event-Sink-Fehler und der vollständige Observer-Stop/Restart-Vertrag. P4 Strict wird nicht als unterstützt oder abgenommen behauptet. Unit-, Native- und Race-Erfolg ersetzen diese Hostnachweise nicht.

## Unabhängige Oracle-Prüfung und Original-ID-Retakes

Alle 125 Original-Oracles wurden einzeln gegen Quell-, SDK- und Hostsemantik geprüft. Die drei Envoy-eigenen Reviewdateien erhalten die Original-Oracles unverändert. Konkrete neue Fixture-/Erwartungsvorschläge stehen getrennt von kanonischer Auflösung und Hostabnahme:

| Route | Reviewed original oracles | New source proposals | Retaken original IDs |
| --- | ---: | ---: | ---: |
| envoy-ext-proc | 51 | 14 | 14 |
| envoy-ext-authz-request | 40 | 10 | 10 |
| envoy-ext-authz-response-companion | 34 | 9 | 9 |

Neue individuell geprüfte Lifecycle-PASS:

- `I12::envoy-ext-proc::NEED-request-streaming` — `cf8c6b76c81a6d9c6c231bfc5486af279f123e09841d3612711ec055516e1066`.
- `I12::envoy-ext-proc::NEED-response-streaming` — `602bcebc22f375e75a7fe9c7ff42321dd190e207d58bd190bc63eb6ef3c45a6b`.
- `I12::envoy-ext-authz-request::NEED-complete-sample` — `8f5282e25a7389b8e4cf62b4474b515dd7689f0758884d849c0741e72d644c25`.

Der eigene aktuelle Abnahmestand hat 6 aufgelöste und 119 offene Original-Oracles. Der zentrale Baseline-Bestand bleibt unverändert.

Jeder neue Vorschlag hat eine explizite Original-ID-/Fixture-Bindung und physische Quellreferenzen. Die zugehörigen Retakes bleiben bis zur vollständigen Prüfung aller fallbezogenen Nachweise unqualifiziert; auch ein passendes HTTP-Ergebnis löst kein Original-Oracle automatisch auf.

Die Postcommit-Proben synchronisieren den absichtlichen Backend-EOF mit einer tatsächlichen Client-Receipt des ersten Entitybytes. ext_proc und Companion liefern jeweils HTTP 200/32 Bodybytes vor unvollständigem Chunk-Framing. Der Client endet mit Fehler; der erste physische Common-Fehler bleibt protocol_error mit originalem/sichtbarem Status 200 und gesetztem Commit. Free/Cleanup sind beobachtet; ein erfolgreicher runtime_finish wird dafür nicht erfunden.

Die vollständige Bilingual-Prüfung endet mit Exit 2 wegen 22 unveränderter Links in den nicht initialisierten Framework-Gitlink dieses Worktrees. Die Parent-Sprachverträge und sämtliche neuen Dokumentlinks bestehen die abgegrenzte API-Prüfung. Das ist kein globales Bilingual-PASS. Alle 2.105 Buildquellen wurden unabhängig aus dem archivierten Parent und den Capture-Overlays rekonstruiert; Fall-/Routen-/Parent-Austausch und der äußere Timeoutpfad haben eigene Negativkontrollen.

## Physische Referenzen

- `baseline`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/baseline-envoy-reconciliation.json` — SHA256 `e5bc09638b139351aa9816df79faffcb8923117f1bd74ca59fdd7b21021ac469`.
- `native`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/native-v2/native-build/receipt.json` — SHA256 `fd429f2d49a76c71233eb581992a24fc81ac47b1ca8662fd3892be046eee16b0`.
- `I12__envoy-ext-proc__NEED-request-streaming`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals/I12__envoy-ext-proc__NEED-request-streaming.json` — SHA256 `cf8c6b76c81a6d9c6c231bfc5486af279f123e09841d3612711ec055516e1066`.
- `I12__envoy-ext-proc__NEED-response-streaming`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals/I12__envoy-ext-proc__NEED-response-streaming.json` — SHA256 `602bcebc22f375e75a7fe9c7ff42321dd190e207d58bd190bc63eb6ef3c45a6b`.
- `I12__envoy-ext-authz-request__NEED-complete-sample`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals/I12__envoy-ext-authz-request__NEED-complete-sample.json` — SHA256 `8f5282e25a7389b8e4cf62b4474b515dd7689f0758884d849c0741e72d644c25`.
- `oracles-ext-proc`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-ext-proc.json` — SHA256 `a25fe9a5808df508a5182cedf343166ccafebefabaeaa7d7898a4eb6d2c61a2f`.
- `oracles-authz-request`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-authz-request.json` — SHA256 `00299799b27918783dff71e44720059d23bc539570f71c4e37a4b6d91ac08ddf`.
- `oracles-companion`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-companion.json` — SHA256 `fe98c20ebd63ad455a34e2a65dbced229d43cab63755d70e743a18abdaf9f1b3`.
- `review-release-host-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-v2.json` — SHA256 `c07e6c0825d15b1d80adf88519e3e4539d2378e7c0adf811ad29940771962155`.
- `review-release-host-v3`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-v3.json` — SHA256 `5379f6fd2129ac7c411f89fcfa7487bf16db826e15dbc397523144f97f657ce7`.
- `review-release-host-faults-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-faults-v2.json` — SHA256 `433d338c4286a03c3f0d2b8618e3b719715685695939adc252a0eba1b5ab5406`.
- `review-release-host-final`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-final.json` — SHA256 `36f9d21db12bca52562c53b0654cedfaefc56096f8f2410b6940d442f3cc07f7`.
- `review-release-host-postcommit`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-postcommit.json` — SHA256 `6add24def432637fb8d701fe98f8b2890d473992a38939a2f27bdb21d672f27e`.
- `review-release-host-originals`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-originals.json` — SHA256 `2de58afa0962ac01258a7fd1a9fac9553eb97f54543c0e5d303668477101d7fd`.

Die Referenzen liegen im task-eigenen externen Speicher; der PR enthält nur Quellcode und bereinigte Metadaten, keine Binaries, Caches, privaten Schlüssel oder Rohpayloads.
