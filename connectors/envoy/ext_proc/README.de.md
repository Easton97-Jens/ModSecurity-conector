# Envoy `ext_proc` Common/libmodsecurity Pfad für den gesamten Lebenszyklus

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis ist eine angeheftete Go-Implementierung des Beamten von Envoy
`envoy.service.ext_proc.v3.ExternalProcessor` gRPC-Schnittstelle. Es ist getrennt
vom vorhandenen C `ext_authz`-Dienst und ändert den ausgewählten nicht,
laufzeitnachweisbarer Nur-Anfrage-Pfad.

Der kanonische Full-Lifecycle-Dispatcher wählt diesen Dienst aus
`full-lifecycle-envoy-ext-proc`; es entspricht nicht dem Standard
`ext_authz` Kompatibilitätsläufer. Die ausführbare Datei verknüpft ein Connector-lokales CGo
ABI zu Common Runtime und libmodsecurity, während die Funktionserweiterung weiterhin besteht
gesonderte Entscheidung zur Beweiswürdigung.

## Was hier implementiert ist

– ein unabhängiger `streamState` und Transaktions-Seam pro gRPC `Process`-Aufruf;
– eine echte Common/libmodsecurity-Transaktion pro Stream, geöffnet von Envoy
  Tatsächliche Anforderungsheader werden gelöscht und bei EOS, Abbruch oder Prozessor vernichtet
  Scheitern;
- begrenzte Anforderungs-/Antwort-Header-Zuordnung und inkrementelle Body-Callbacks;
- keine vollständige Sammlung von Anfrage- oder Antworttexten; Staat behält nur Zähler;
- explizite Anforderungs-/Antwort-Body-Finish-Aufrufe für Header-EOS, Body-EOS und
  Anhänger EOS;
- Downstream-Protokoll und Endpunkte, die den angeforderten Envoy-Attributen zugeordnet sind,
  niemals aus dem Envoy-to-Service-gRPC-Socket abgeleitet;
- passende `HeadersResponse`-/`BodyResponse`-Nachrichten für den `STREAMED`-Modus;
- eine prozessweite Obergrenze von 128 aktiven `Process`-Streams, die vor der
  Allokation von Streamzustand oder Common-Transaktion greift; überzählige
  Streams erhalten gRPC-`ResourceExhausted`, statt die native
  Transaktionskapazität über mehrere Transporte zu vervielfachen;
- EOS-Bereinigung, Bereinigung des gRPC-Kontextabbruchs und begrenzter, ordnungsgemäßer Stopp;
- Pre-Commit-Anfrage- und Antwortentscheidungen, die `ImmediateResponse` zugeordnet sind,
  wobei allgemeine Host-Aktionsmetadaten erst nach dem passenden gRPC-Versand aufgezeichnet werden
  gelingt;
- rohes Common-Decision-JSONL unter dem Runtime-Root pro Lauf plus einem separaten
  nutzlastfreies Abschlussprotokoll; Letzteres ist ergänzend und ersetzt niemals
  der gemeinsame Ereignisstrom;
- Unit- und CGo-Lebenszyklustests für P1/P2/P3/P4, inkrementelles EOS,
  Stornierung, Commit-Reihenfolge und parallele Transaktionen.

## Sicherheit von Listener und Stream-Zulassung

Der nicht authentifizierte ext_proc-gRPC-Endpunkt akzeptiert nur numerische
Loopback-Listener-Adressen (`127.0.0.0/8` oder `::1`). Hostnamen, Wildcard-
Adressen und andere Schnittstellenadressen schlagen die
Konfigurationsvalidierung fehl, auch über die `--listen`-Überschreibung. Die
obligatorischen Service-JSON-Felder `max_concurrent_streams` (1–1024) und
`stream_idle_timeout_ms` liefern zwei unabhängige Verfügbarkeitsgrenzen. Die
erste gilt sowohl pro HTTP/2-Verbindung als auch für die prozessweite
`Process`-Zulassung. Eine prozessweite Zurückweisung liefert
`ResourceExhausted`, bevor Stream-Zustand oder eine Common-Transaktion angelegt
wird.

`stream_idle_timeout_ms` ist ein serverseitiges Inaktivitätslimit und kein
Engine-Timeout. Seine Uhr läuft, während der Service auf die erste oder nächste
vollständige Envoy-`ProcessingRequest` wartet; jede empfangene Request ist
Stream-Aktivität, und das nächste Intervall beginnt erst nach Engine-Verarbeitung
und dem Senden der zugehörigen Antwort. Ein langlebiger gestreamter Request oder
Response bleibt daher zulässig, wenn er innerhalb des Intervalls weiter
Nachrichten liefert. Bei Ablauf liefert der Service gRPC `DeadlineExceeded`,
zeichnet `grpc_stream_idle_timeout` auf, schließt die Transaktion mit dem
getrennten `cleanup_timeout_ms` und gibt die Zulassung für einen Folgestream
frei. `engine_timeout_ms` begrenzt unabhängig jede Engine-Operation: sowohl
das Warten auf den serialisierten Common-Runtime-Mutex als auch die
verbleibende Callback-Ausführung nach dessen Erwerb. Er ersetzt oder startet
die Stream-Idle-Uhr nicht neu. Läuft dieser Context vor dem nativen Eintritt
ab, erhält der aktuelle Stream gRPC `DeadlineExceeded`, seine Abschluss-
Evidence lautet `processor_error`, er emittiert keine Allow-Antwort, und der
reguläre Stream-Cleanup mit Freigabe der Zulassung erlaubt einen Folgestream.
Ein nativer CGo-Aufruf, der bereits einen nicht unterbrechbaren Abschnitt
betreten hat, bleibt ein getrennter kontrollierter Restart-Fall; der Timeout
behauptet nicht, ihn in-process abzubrechen.

`stream_max_lifetime_ms` ist eine separate absolute serverseitige Lebensdauer
für jeden zugelassenen Stream. Sie beginnt bei der Zulassung und wird durch
Aktivität nicht verlängert. Dadurch kann ein Peer keinen
Parallelitäts-Slot unbegrenzt halten, indem er kurz vor jedem Idle-Ablauf eine
Nachricht sendet. Beim Ablauf liefert der Dienst gRPC `DeadlineExceeded`,
zeichnet `grpc_stream_max_lifetime` auf, bricht Receive- und Engine-Arbeit ab,
führt die normale begrenzte Bereinigung aus und gibt den Slot für einen
Folgestream frei. Ein beim Ablauf bereits laufendes gRPC-`Send` erhält höchstens
die getrennte Gnadenfrist `cleanup_timeout_ms`, um sein Ergebnis zu liefern.
Bei einem bestätigten erfolgreichen späten `Send` schreibt der Service zunächst
die zugehörige Response-Commit- oder Hostaktions-Evidence über einen begrenzten
Post-Send-Context, liefert danach `DeadlineExceeded` und wechselt in den
kontrollierten Restart-Zustand; ein nach dieser Frist weiter unaufgelöstes Send
löst denselben Zustand aus, ohne eine Aktion zu behaupten. In beiden terminalen
Fällen erhalten neue Streams gRPC `Unavailable`, während `main` den Listener
stoppt. Der Wert muss für legitime gestreamte Transaktionen ausreichen; er
ersetzt weder das Idle-Limit noch das Timeout einzelner Engine-Operationen.

Der Lebenszyklus eines ausstehenden `Recv` ist durch einen echten gRPC-
bufconn-Test abgedeckt: Ein inaktiver Stream hinterlässt genau ein begrenztes
Receive-Warten, eine Stornierung gibt es frei und ein Folgestream wird
erfolgreich zugelassen. Der Server-Shutdown storniert aktive Streams, gibt
Transaktionen und Zulassungsslots frei, und der erzwungene Stop besitzt eine
eigene Deadline. Auch Lock-Erwerb und Cleanup sind deadline-begrenzt. Ein
nativer CGo-Aufruf oder Destruktor, der bereits in einen nicht unterbrechbaren
nativen Abschnitt eingetreten ist, kann nicht innerhalb des Prozesses storniert
werden; der Service meldet einen terminalen Cleanup-Fehler an `main`. Der
aktuelle Stream schlägt fehl, neue Streams erhalten gRPC `Unavailable`, `main`
stoppt den gRPC-Listener über seinen begrenzten Forced-Stop-Pfad, und der
Prozess endet mit Nonzero für den Supervisor-Restart, statt eine In-Process-
Stornierung oder Wiederverwendung nativen States zu behaupten.

Eine gRPC-Context-Stornierung (einschließlich Server-Shutdown) folgt demselben
Cleanup-Pfad pro Stream und wird als
`grpc_context_canceled_unattributed` aufgezeichnet. Das Label behauptet nicht,
ob Envoy einen Downstream-Client- oder Upstream-Reset gesehen hat.

Die angeheftete Abhängigkeit ist das offiziell generierte Envoy Go API-Modul in
`go.mod`/`go.sum`. `../config/envoy-ext-proc-versions.env` zeichnet das beabsichtigte auf
Framework-synchronisierte Envoy-Version und `../config/envoy-ext-proc-streaming.yaml.in` werden verwendet
nur `STREAMED` Körpermodi, niemals `BUFFERED`.

## Mindestversionen für die Abhängigkeitssicherheit

Das Modul hält für die aktuell triagierten Dependency-Advisories mindestens
folgende stabile Auswahlen ein:

- `google.golang.org/grpc` `v1.83.1` oder höher;
- `golang.org/x/net` `v0.56.0` oder höher;
- `golang.org/x/sys` `v0.46.0` oder höher; und
- `golang.org/x/text` `v0.39.0` oder höher.

`tests/test_ci_security_workflows.py` prüft diese Grenzen als semantische
Versionsuntergrenzen. Damit bleibt ein späteres stabiles Sicherheitsupdate
zulässig, während ein Downgrade den fokussierten CI-Sicherheitsvertrag verletzt.
Die Grenze belegt die ausgewählten Modulversionen; sie belegt weder die
Erreichbarkeit eines Advisories noch ersetzt sie Go-Modultests oder behauptet,
dass ein gehosteter Dependabot-, OSV- oder Scorecard-Alert bereits aktualisiert
wurde.

## Explizite Nichteinforderungen und verspätetes Handeln

Der ausgelieferte Build verwendet `-tags libmodsecurity`; Ein Go-Build, der nur aus der Quelle stammt, behält a
PassthroughEngine nur für Protobuf/Unit-Entwicklung und lehnt eine Laufzeit ab
config. Der normale Build erfordert lokale libmodsecurity-Header und -Bibliotheken
Pfade und verknüpft dann Common Runtime mit der ausführbaren Datei ext_proc.

Der Dienst verwendet die konservative Antwort-Commit-Grenze: nur eine erfolgreiche
Antwortheader `CONTINUE` send markiert eine Antwort als festgeschrieben. Für eine disruptive
Entscheidung später gefunden:

- `minimal` und `safe` zeichnen ein echtes Common-Host-Ergebnis `log_only` auf
  und setzen die Antwort mit ihrem ursprünglichen sichtbaren Status fort;
- `strict` wird beim Start der Common Runtime für das Profil
  `envoy-ext-proc` abgewiesen. Dessen unveränderliche Capability
  `strict_post_commit_action` ist null, bis eine deterministische
  Post-Commit-Hostaktion bewiesen ist; es wird kein Traffic bedient und keine
  späte Entscheidung stillschweigend herabgestuft.

Der Adapter verwendet nach dem Response-Commit absichtlich weder
`ImmediateResponse` noch einen gRPC-Fehler als HTTP-Reset-Ersatz. Ein
abgebrochener gRPC-Kontext und ein beobachteter gRPC-Peer-EOF werden als
`grpc_context_canceled_unattributed` beziehungsweise `grpc_peer_eof` erfasst;
keines dieser Labels darf als Downstream- oder Upstream-Reset interpretiert
werden.

Die Grenze aktiver Streams begrenzt aggregierte Ressourcen, ist aber keine
Idle-Deadline: Ein gültiger, anschließend stiller zugelassener Stream belegt
einen begrenzten Slot, bis Envoy eine Nachricht oder EOF sendet oder den
gRPC-Kontext abbricht. Eine separate Idle-Policy darf erst ergänzt werden,
wenn legitimes Streaming sowie das Fehlen blockierter Receive-Goroutinen und
verbliebener nativer Transaktionen nachgewiesen sind.

## Lokale Quell-/Build-Befehle

```sh
make -C connectors/envoy build-envoy-ext-proc
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc ENVOY_BIN=/absolute/path/to/envoy
```

`runtime-smoke-envoy-ext-proc` startet einen echten Pinn-kompatiblen Envoy-Prozess.
der CGo/Common gRPC-Dienst und ein lokaler Upstream. Es spart effektiven Gesandten und
Gemeinsame Konfigurationen, rohes Common JSONL und eine separate Nur-Metadaten-Konfiguration
Abschlussprotokoll außerhalb der Kasse. Die Wirtsrauchübungen P1, P2, P3 verweigern,
P3-Umleitung und P4-Post-Commit-Sicherheits-/Nur-Protokoll-Verhalten. Es bleibt
nicht hochgestuft, bis der kanonische Sammler und die Fähigkeitsüberprüfung dies akzeptieren
rohe Wirtsbeweise.

## Verbleibende Promotion-Grenze

Der Dienst behauptet keinen deterministischen Post-Commit-Reset und keine
Beobachtung der Client-Bytes. Eine späte P4-Regel wird im Safe-Modus als vom
Host bestätigtes `log_only` erfasst. Strict wird absichtlich beim Start
abgewiesen, bis eine deterministische Envoy-Hostaktion nachgewiesen ist; es ist
weder `ImmediateResponse` noch ein gRPC-Fehler oder behaupteter Reset. Die
kanonische Validierung des rohen Common-JSONL bleibt eine Promotionsgrenze.
