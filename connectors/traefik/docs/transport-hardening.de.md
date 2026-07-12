# Traefik: Grenze für Transport-Hardening des nativen Pfads

Diese Notiz gilt ausschließlich für den repository-eigenen nativen
Local-Plugin-Pfad (`native-traefik-middleware`) auf dem gepinnten
Traefik-Host `3.7.5`. Der getrennte `forwardAuth`-Kompatibilitätspfad und
Capability-Promotionen bleiben unverändert.

## API-Audit und Strict-Grenze

Die Commit-Grenze des Plugins ist die erfolgreiche Delegation von
`WriteHeader` oder eines Body-Writes durch `responseWriter`; anschließend
übermittelt es nur begrenzte Commit-Metadaten an seine UDS-Engine-Session. Eine
späte Phase-4-Entscheidung ist kein HTTP-Status-Rewrite.

| Downstream-Protokoll | Öffentliche Hostoberfläche | Ausgewähltes Verhalten | Evidenzstatus |
| --- | --- | --- | --- |
| HTTP/1.1 | `http.Hijacker` kann eine Verbindung übernehmen, falls der tatsächlich umschlossene Writer dies unterstützt | Das Plugin erhält die Schnittstelle für einen Upstream-Handler; bei einer Regelentscheidung ruft es `Hijack` nicht auf | Strict-Abbruch nach Commit ist `NOT EXECUTED` |
| HTTP/2 | Gos `ResponseWriter` implementiert `http.Hijacker` für HTTP/2 absichtlich nicht | Im Local-Plugin-API und im ausgewählten Harness existiert kein request-lokaler `RST_STREAM`-Pfad | `NOT EXECUTED` |
| HTTP/3 | Es gibt keinen repository-eigenen UDP/QUIC-Entry-Point und keinen Middleware-Stream-Control-Pfad | Nicht konfiguriert | `NOT EXECUTED` |

Die Go-API dokumentiert, dass Hijacking die gesamte Verbindung übernimmt,
Wrapper die Schnittstelle möglicherweise nicht implementieren und HTTP/2-Writer
sie nicht unterstützen. Das ist ein verbindungsweiter HTTP/1.1-Mechanismus,
kein HTTP/2-Streamnachweis. Siehe den [Go-Vertrag für
`http.Hijacker`](https://pkg.go.dev/net/http#Hijacker).

Das native UDS-Protokoll stellt deshalb derzeit kein regelgesteuertes spätes
`abort_connection`-Ergebnis bereit. Eine zukünftige HTTP/1.1-Implementierung
muss auf dem gepinnten Traefik-Host vorher alles Folgende mit einem echten
Client belegen: einen zur Laufzeit unterstützten Writer, bereits sichtbare
Header und ein Body-Byte, einen unvollständigen deklarierten Body nach dem
Schließen nur dieser Verbindung, Exactly-once-Cleanup und einen gesunden,
unabhängigen Folge-Request. Sie darf nur den aktuellen begrenzten Chunk
zurückhalten, niemals den vollständigen Response. HTTP/2 benötigt einen
eigenen request-lokalen Reset-Hook und ein beobachtetes `RST_STREAM`; ein
Hijack-Ergebnis darf dafür nicht wiederverwendet werden.

## Implementierte begrenzte Transport-Sicherungen

`responseWriter` markiert einen Response nun als unvollständig, wenn der
umschlossene Writer einen Fehler/Kurzschreibvorgang liefert oder `ReadFrom`
einen Fehler liefert. `finish()` überspringt dann den Response-EOS-Callback. Die
Transaktion wird weiterhin genau einmal geschlossen, aber ein Downstream-
Disconnect oder ein Upstream-Lesefehler kann nicht als normales Response-EOS
oder späte Strict-Intervention umetikettiert werden.

Der isolierte native Host-Probe verwendet außerdem eine tatsächliche
HTTP/1.1-Verbindung für den P4-Safe-`log_only`-Request und einen anschließenden
Allow-Request. Er verlangt für beide Requests denselben Socket und schreibt
ein payload-freies, nicht promotendes `transport-observations.diagnostic.json` mit:

- clientseitig beobachtetem `response_committed`, `first_byte_received` und
  `eos_received`;
- `connection_reused` und dem unabhängigen Folgeergebnis;
- einem Diagnosefall-Label, aber ohne synthetische kanonische Korrelationsfelder;
  sowie
- der expliziten Grenze `strict.state = NOT_EXECUTED`.

Dieses Diagnose-Sidecar ist kein kanonisches Promotion-Artefakt und reicht nicht aus,
Keep-Alive-, Strict-, Cancel-, HTTP/2- oder HTTP/3-Capabilities zu promoten.

## Ausführung und Nicht-Claims

Führe den ausgewählten Host-Probe nur mit einem lokal bereitgestellten
gepinnten Binary und libmodsecurity-Eingaben aus:

```sh
make -C connectors/traefik runtime-smoke-traefik-native
```

Die Source-/Unit-Tests decken den Pfad ohne erfundenes EOS ab und beweisen, dass
eine späte Entscheidung nicht stillschweigend eine Hostverbindung hijackt. Sie
sind kein Client-Abbruchnachweis. Client-Cancel, Upstream-Reset, Timeout,
HTTP/2-Reset und HTTP/3-Reset werden hier nicht promotet.
