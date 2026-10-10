# Native Traefik-Middleware-Quelle

**Sprache:** [English](README.md) | Deutsch

Dies ist ein repository-eigenes Go-Paket für die Go-Middleware-Einstiegspunkte
von Traefik: `CreateConfig`, `New` und `ServeHTTP`. `New` hat die erforderliche
Signatur `(http.Handler, error)`, und `.traefik.yml` enthält Plugin-Metadaten
und Testdaten. Es verwendet ausschließlich die Go-Standardbibliothek; Traefik
stellt beim Laden eines Plugins den nächsten `http.Handler` bereit. Der
Full-Lifecycle-Runner staged dieses Paket unter einem gepinnten lokalen
Traefik-Plugin-Arbeitsbereich. Es ersetzt weder den bestehenden C-
`forwardAuth`-Kompatibilitätsdienst noch ändert es dessen
Capability-Erklärung.

## Was die Quelle tut

- Sie liest den vollständigen Request-Body vor dem nächsten Handler ein,
  begrenzt Lesevorgänge auf `maxRequestChunkBytes` und sendet sie synchron an
  die `Transaction` pro Request. Erst ein vollständig erlaubtes Request-EOS
  gibt den Handler frei.
- Sie puffert höchstens `maxRequestBodyBytes` (harte Obergrenze: 1 MiB) für
  bytegenaue Wiedergabe an den nächsten Handler, ohne die Bytes erneut zu prüfen.
- `requestBodyIdleTimeoutMillis` ist unabhängig von Engine-Timeout und
  `maxRequestBodyBytes`. Bei Inaktivität oder Cancel wird vor dem nächsten
  Handler fail-closed beendet und die eigene Quelle geschlossen.
- Erst bei Idle/Cancel verkürzt sie die Read-Deadline über den
  ResponseController des Hosts: `Close` allein löst einen laufenden `Read`
  des Server-Bodys nicht. Erfolgreiche Reads ersetzen oder löschen niemals den
  absoluten ReadTimeout des Operators. Eigene Quellen ohne Host-Deadline-Unterstützung
  müssen ihre Lesevorgänge bei `Close` lösen. Der Controller folgt Wrappern mit
  `Unwrap`. Verbirgt ein Wrapper Deadlines und `Unwrap`, liefert er
  `ErrNotSupported`; bei einem echten HTTP-Body hinter einem solchen Wrapper
  benötigt die Idle-Grenze einen Host-Read-Timeout und ist durch Quelltests
  nicht belegt.
- Die endliche Grenze `maxRequestBodyBytes` (Standard und harte Obergrenze:
  1 MiB) greift, bevor ein überschreitender Chunk die Engine erreicht. Die
  Aktion vor dem Commit ist HTTP 413; danach werden keine weiteren Request-Bytes
  geprüft oder weitergeleitet. Das hosteigene `Body.Close` darf Restbytes bis zur
  konfigurierten Idle-Deadline einlesen.
- Abgeschnittene deklarierte Bodies (auch nil/`NoBody` bei positiver Content-Length)
  sowie Lese-/Enginefehler führen zum
  geschlossenen HTTP-500-Pfad, ohne Handler-Aufruf oder erfundenes Request-EOS.
- Sie umschließt den ResponseWriter, wertet Response-Header vor dem Commit aus
  und teilt jedes `Write` vor der Weiterleitung in
  `maxResponseChunkBytes`-Callbacks auf.
- Sie implementiert `http.Flusher`, `http.Hijacker`, `http.Pusher`,
  `io.ReaderFrom` und `Unwrap`; `ReadFrom` behält nach einem begrenzten ersten
  Chunk den schnellen Pfad des umschlossenen Writers bei.
- In `Summary` verbleiben nur Metadaten sowie Byte-/Chunk-Zähler, niemals ein
  vollständiger Request- oder Response-Body.
- `Metadata.ServerAddress` und `Metadata.ServerPort` werden ausschließlich aus
  dem vom Host bereitgestellten `http.LocalAddrContextKey` abgeleitet; ein
  fehlender, nicht-IP- oder ungültiger Port-Endpunkt liefert HTTP 500, bevor
  die Engine geöffnet wird, während die client-kontrollierte Request-Authority
  ausschließlich `Metadata.Hostname` bleibt.
- Ein disruptives Ergebnis nach dem Response-Commit wird als `log_only`
  behandelt; es wird kein geänderter Status, Reset oder Client-Abbruch
  behauptet.

Die Engine ist standardmäßig fail-closed: Ein ausgelassenes `engineMode`
wählt `uds`, und `New` verlangt einen gültigen privaten Unix-Domain-Socket-Pfad,
bevor es den persistenten Common-/libmodsecurity-Engine-Dienst erreichen kann.
Der ausgewählte Host-Runner stellt einen privaten Socket und einen
laufzeitlokalen Event-Pfad bereit. Das eingecheckte dynamische Beispiel benennt
einen erwarteten privaten Laufzeitpfad, materialisiert oder verwendet jedoch
kein Socket-Objekt wieder. Der produktive Plugin-Konstruktor akzeptiert nur
`engineMode: uds`; eine Always-Allow-Passthrough-Auswahl wird vor der
Handler-Erzeugung abgelehnt. Die injizierbare Engine-Naht ist paketprivater
Testcode und kein Operator-Konfigurationspfad. Das Paket belegt gezieltes
P1--P4-Hostverhalten, ohne Capability-, CRS-, Safe/Strict- oder
Produktionsreife zu behaupten.

Der Go-Client validiert den Socket-Pfad lexikalisch und begrenzt jeden Frame,
beansprucht aber keine portable Peer-Credential-Authentifizierung. Wenn die
Hostumgebung eine getrennte Dienstidentität verlangt, muss die Laufzeit diese
über den privaten Socket-Elternpfad und die Bereitstellungsberechtigungen
erzwingen. Eine plattformspezifische `SO_PEERCRED`-Prüfung benötigt einen
ausdrücklich unterstützten Plattformvertrag und wird von diesem Paket nicht
impliziert.

Die Zuordnung des vertrauenswürdigen lokalen Endpunkts schützt nur die
Provenienz des Server-Endpunkts. Sie authentifiziert keinen späteren UDS-Peer
und löst daher nicht das Socket-Ersetzungsrisiko aus FND-PARENT-0015.

Das UDS-Protokoll lehnt unbekannte Engine-Aktionen ab, statt sie als
HTTP-Ablehnung umzudeuten. Es meldet ein disruptives Ergebnis erst nach einem
erfolgreichen tatsächlichen `ResponseWriter`-Schreibvorgang. Nach dem
Response-Commit ist ein disruptives Phase-4-Ergebnis bewusst `log_only`; es
erzeugt keinen geänderten Status, Reset oder Client-Abbruch-Anspruch.

## UDS-Cancellation-, Timeout- und Cleanup-Grenze

Jede `ServeHTTP`-Transaktion besitzt genau eine private UDS-Verbindung; sie
wird nie von einer Folgeanfrage wiederverwendet. Jeder Austausch während
Request/Streaming verwendet das
kleinere von konfiguriertem Engine-Timeout und Request-Context-Deadline. Eine
Context-Cancellation verkürzt die Verbindungs-Deadline sofort, löst einen
wartenden Read oder Write und verbindet ihren Watcher vor Rückkehr des Aufrufs.
Ein Timeout, Cancel, Peer-Reset, ungültiges oder unvollständiges Resultat
verwirft die Verbindung, schließt ihren FD und beendet nur diese Transaktion;
kein Teilframe darf wiederverwendet werden. `Close` bleibt idempotent, auch
wenn ein früherer Austausch die Verbindung bereits verworfen hat.

Nach regulärer Handler-Rückkehr darf eine Response mit expliziter Content-Length,
deren sämtliche Bytes der Host-Writer akzeptiert hat, auch bei anschließendem
Client-Abbruch abgeschlossen werden. Nur dieser vollständige Stream ohne
Lese-/Schreibfehler oder Hijack verwendet für die letzte Body-Commit-Bestätigung,
Response-EOS und Cleanup einen Context mit erhaltenen Request-Werten und
unabhängiger Ein-Sekunden-Deadline. Unbekannte oder unvollständige Längen sowie
fehlerhafte Streams behalten die normale Request-Cancellation. Ein Enginefehler
wird in `Summary` niemals als erfolgreiches Response-EOS gewertet.

Vor dem Response-Commit führt ein Engine-Austauschfehler zum dokumentierten
geschlossenen HTTP-500-Pfad. Ein abgebrochener Host-Request kann seinen
Response-Kanal bereits verloren haben; der Connector erfindet daher weder
einen client-sichtbaren Status noch ein Upstream-Reset-Event. Nach dem Commit
bleibt die dokumentierte `log_only`-/unveränderte-Response-Grenze bestehen,
statt eine rückwirkende Umschreibung zu behaupten. Eine frische Anfrage öffnet
eine neue UDS-Sitzung und behält die normalen Allow/Block-Semantiken bei.

## Lokale Quellenprüfungen

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

Das Build-Skript führt `go test ./...`, `go vet ./...` und (für `build`) `go
build ./...` aus. Es schreibt nur einen Kompilierungsbericht außerhalb des
Checkouts, standardmäßig nach
`$BUILD_ROOT/traefik-native-middleware/build.txt`. Es installiert kein
Traefik-Plugin, startet keinen persistenten Engine-Dienst, ruft
Common/libmodsecurity nicht auf und schreibt keine Laufzeitnachweise.

## Begrenztes Fuzzing des UDS-Parsers

`FuzzUDSFrameAndResult` prüft den eigenen UDS-Frame-Reader und Result-Parser
mit abgeschnittenen, fehlerhaften, Allow-, Deny- und Redirect-Seeds sowie
beliebigen begrenzten Frames. Es verwendet nur einen In-Memory-Reader: Es
öffnet keinen Socket, startet keine Engine und ruft weder CGo noch Common auf.
Ein fehlerhafter Frame muss ohne Panic einen Fehler liefern. Jeder erfolgreich
geparste Frame muss zu seinen konsumierten Bytes unverändert round-trippen
können (weitere Stream-Frames können folgen), und ein erfolgreich geparstes
Result muss eine erkannte Aktion enthalten.

Führen Sie dieselbe begrenzte Prüfung aus diesem Modulverzeichnis aus:

```sh
GOTOOLCHAIN=local go test -mod=readonly -run='^$' -fuzz='^FuzzUDSFrameAndResult$' -fuzztime=15s -parallel=1 .
```

Der `traefik-go`-CodeQL-Job führt diese Kontrolle mit derselben 15-Sekunden-
und Single-Worker-Grenze aus. Sie ist Parser-Evidenz auf Source-Level, keine
Traefik-Host-Runtime- oder Capability-Promotion-Evidenz.

## Konfigurationsgrenze

`../config/traefik-native-middleware-static.yaml` und
`../config/traefik-native-middleware-dynamic.yaml` sind passende Formen für
ein lokales Plugin und einen File Provider mit einer vom Operator angelegten
Registrierung namens `modsecurityNative`. Sie sind bewusst von
`../config/traefik-forwardauth-dynamic.yaml` getrennt. Das
`full-lifecycle-traefik-native`-Hostziel staged unabhängig einen äquivalenten
wegwerfbaren Arbeitsbereich, baut und startet den lokalen Engine-Dienst und
prüft das Laden des Plugins im gepinnten Host. Es verwendet weder diese
eingecheckten Referenzdateien noch einen gemeinsam genutzten Engine-Socket.
Eine Operator-Bereitstellung muss das Modul weiterhin im lokalen
Plugin-Arbeitsbereich der installierten Traefik-Version bereitstellen. Der
Probe-Lauf ist kein Einsatz- oder Capability-Promotion-Nachweis.
