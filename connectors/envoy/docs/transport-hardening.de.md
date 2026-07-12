# Envoy ext_proc: Grenze für Transport-Hardening

Diese Notiz beschreibt den repository-eigenen HTTP-Pfad `envoy.filters.http.ext_proc` für das gepinnte Envoy-Release `1.38.2`. Er ist vom alten `ext_authz`-Kompatibilitätspfad getrennt und promotet keine Capability.

## API-Audit und Strict-Grenze nach Commit

Die ausgewählte Konfiguration nutzt `STREAMED` für Request- und Response-Bodies. Ein erfolgreiches ext_proc-`CONTINUE` für Response-Header ist nur eine Adapter-Ordnungsgrenze: Der Prozessor hat eine Antwort an Envoy gesendet, aber damit ist noch kein Downstream-Client-Byte beobachtet.

Das gepinnte `ProcessingResponse`-API bietet `BodyResponse`, Stream-Schließen und `ImmediateResponse`. Seine Source-Dokumentation beschreibt, dass ein `ImmediateResponse` nach begonnenem Response entweder als lokale Antwort den Downstream-Codec erreichen oder den Stream zurücksetzen kann. Das ist kein deterministischer, protokollspezifischer und clientseitig beobachteter Resetnachweis. Der ausgewählte Prozessor sendet nach Commit absichtlich kein `ImmediateResponse` und deutet keinen gRPC-Fehler als Reset. Siehe das [gepinnte `v1.38.2`-ext_proc-Proto](https://github.com/envoyproxy/envoy/blob/v1.38.2/api/envoy/service/ext_proc/v3/external_processor.proto).

| Downstream-Protokoll | Ausgewählter Host-/API-Status | Evidenzstatus |
| --- | --- | --- |
| HTTP/1.1 | Der Host-Probe besitzt einen Cleartext-HTTP/1-Listener; Strict läuft als `strict_abort_not_attempted` weiter | Client-Abbruch nach Commit ist `NOT EXECUTED` |
| HTTP/2 | Der gRPC-Service-Cluster nutzt HTTP/2, aber der repository-eigene Downstream-Listener besitzt kein TLS/ALPN- oder erzwungenes H2-Profil | Kein Downstream-`RST_STREAM`-Nachweis; `NOT EXECUTED` |
| HTTP/3 | Kein QUIC-Listener oder HTTP/3-Client-Profil ausgewählt | `NOT EXECUTED` |

Eine spätere Strict-Implementierung muss einen gepinnten, request-lokalen Envoy-HTTP-Filter verwenden oder das exakte `ImmediateResponse`-Verhalten pro Protokoll mit einem echten Client verifizieren. Sie muss einen committed Response, ein sichtbares erstes Body-Byte, einen unvollständigen Response (oder einen konkreten H2-Reset-Code), Exactly-once-Cleanup und einen unabhängigen gesunden Follow-up belegen. Ein gRPC-Close, Servicefehler oder synthetischer HTTP-403 reicht nicht.

## Opt-in-Beobachtung eines Client-Cancels

Der normale Smoke bleibt kurz. Ein Opt-in-Transport-Probe führt nun Folgendes aus:

1. Er verwendet einen echten Cleartext-HTTP/1-Client, der auf Header und ein Body-Byte wartet.
2. Er schließt diese Client-Verbindung, während der Test-Upstream seinen finalen Chunk absichtlich zurückhält.
3. Er verlangt genau einen terminalen ext_proc-Completion-Record für diese
   Transaktion mit `grpc_context_canceled_unattributed` oder `grpc_peer_eof`.
4. Er verlangt einen erfolgreichen unabhängigen Folge-Request.

Führe ihn nur über den echten gepinnten Envoy/ext_proc-Hostpfad aus:

```sh
make -C connectors/envoy transport-cancel-smoke-envoy-ext-proc
```

Der Target entspricht `ENVOY_TRANSPORT_CANCEL_PROBE=1` für
`runtime-smoke-envoy-ext-proc`.

Das Ergebnis ist ein payload-freies, nicht promotendes `transport-observations.diagnostic.json`. Es notiert die clientseitige First-Byte-/Close-Beobachtung, den einen Completion-Record, das Überleben des Hosts und das Folgeergebnis, enthält aber absichtlich keine synthetischen kanonischen Korrelationsfelder. Beide erlaubten terminalen Service-Labels bleiben unattributed: ext_proc identifiziert nicht, ob Envoy einen Downstream-Client-Reset, einen Upstream-Fehler oder einen anderen Stream-Termination-Grund beobachtet hat. Deshalb werden Client-Cancel-, Upstream-Reset-, Strict-, HTTP/2- oder HTTP/3-Capabilities nicht promotet.

## Lifecycle und Nicht-Claims

Der Prozessor besitzt einen Transaktionszustand pro gRPC-Stream und ruft auf seinem Cancellation-Pfad `Close` genau einmal auf. Unit-Tests decken Exactly-once-Cancellation-Cleanup und die Abwesenheit einer erfundenen Hostaktion ab. Ein Source-/Unit-Test oder das Opt-in-Sidecar allein ist kein Downstream-Reset-Nachweis und wird niemals als solcher behandelt.
