# Native Traefik-Streaming-Middleware-Quelle

**Sprache:** [English](README.md) | Deutsch

Dies ist ein repository-eigenes Go-Paket für die Go-Middleware-Einstiegspunkte
von Traefik: `CreateConfig`, `New` und `ServeHTTP`. `New` hat die erforderliche
Signatur `(http.Handler, error)`, und `.traefik.yml` enthält
Plugin-Metadaten und Testdaten. Das Paket verwendet nur die Go-Standardbibliothek;
Traefik liefert beim Laden eines Plugins den nächsten `http.Handler`. Der
Full-Lifecycle-Runner staged das Paket unterhalb eines gepinnten lokalen
Traefik-Plugin-Arbeitsbereichs. Es ersetzt weder den bestehenden C-
`forwardAuth`-Kompatibilitätsdienst noch ändert es dessen
Capability-Erklärung.

## Was die Quelle tut

- Sie umschließt den Request-Body, begrenzt Lesevorgänge auf
  `maxRequestChunkBytes` und sendet sie synchron an eine
  `Transaction`-Nahtstelle pro Request.
- Sie umschließt den ResponseWriter, wertet Response-Header vor dem Commit aus
  und teilt jedes `Write` vor der Weiterleitung in
  `maxResponseChunkBytes`-Callbacks auf.
- Sie implementiert `http.Flusher`, `http.Hijacker`, `http.Pusher`,
  `io.ReaderFrom` und `Unwrap`; `ReadFrom` behält nach einem begrenzten ersten
  Chunk den schnellen Pfad des umschlossenen Writers.
- In `Summary` verbleiben nur Metadaten sowie Byte-/Chunk-Zähler, niemals ein
  vollständiger Request- oder Response-Body.
- Ein disruptives Ergebnis nach dem Response-Commit wird als `log_only`
  behandelt; es wird kein geänderter Status, Reset oder Client-Abbruch
  behauptet.

Die Engine ist standardmäßig fail-closed: Ein ausgelassenes `engineMode`
wählt `uds`, und `New` verlangt einen gültigen privaten Unix-Domain-Socket-Pfad,
bevor es den persistenten Common/libmodsecurity-Engine-Dienst erreichen kann.
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

Das UDS-Protokoll lehnt unbekannte Engine-Aktionen ab, statt sie als
HTTP-Ablehnung umzudeuten. Es meldet ein disruptives Ergebnis erst nach einem
erfolgreichen tatsächlichen `ResponseWriter`-Schreibvorgang. Nach dem
Response-Commit ist ein disruptives Phase-4-Ergebnis bewusst `log_only`; es
erzeugt keinen geänderten Status, Reset oder Client-Abbruch-Anspruch.
Dabei handelt es sich um ein Repository-eigenes Go-Paket für Traefiks
Go-Middleware-Einstiegspunkte `CreateConfig`, `New` und `ServeHTTP`. `New`
verwendet die erforderliche Signatur `(http.Handler, error)`, und `.traefik.yml`
enthält Plugin-Metadaten und Testdaten. Das Paket verwendet ausschließlich die
Go-Standardbibliothek; beim Laden des Plugins liefert Traefik den nächsten
`http.Handler`. Der Full-Lifecycle-Runner legt dieses Paket in einem
angehefteten lokalen Traefik-Plugin-Arbeitsbereich ab. Er ersetzt weder den
vorhandenen C-`forwardAuth`-Kompatibilitätsdienst noch ändert er dessen
Capability-Deklaration.

## Was die Quelle tut

- umschließt den Request-Body, sodass Lesevorgänge auf
  `maxRequestChunkBytes` begrenzt und synchron an eine
  `Transaction`-Nahtstelle pro Request übergeben werden;
- umschließt den ResponseWriter, wertet Response-Header vor dem Commit aus
  und teilt jeden `Write` vor der Weiterleitung in
  `maxResponseChunkBytes`-Callbacks auf;
- implementiert `http.Flusher`, `http.Hijacker`, `http.Pusher`, `io.ReaderFrom`
  und `Unwrap`; `ReadFrom` behält nach einem begrenzten ersten Chunk den
  schnellen Pfad des umschlossenen Writers bei;
- speichert in `Summary` nur Metadaten sowie Byte-/Chunk-Zähler und niemals
  einen vollständigen Request- oder Response-Body;
- behandelt ein disruptives Ergebnis nach dem Response-Commit als `log_only`.
  Es wird kein geänderter Status, kein Reset und kein Client-Abbruch-Claim
  synthetisiert.

Die Form des optionalen Engines ist beabsichtigt. `New` verwendet für eine
reine Source-Konfiguration standardmäßig `PassthroughEngine`, während
`engineMode: uds` pro `ServeHTTP` eine private Unix-Domain-Socket-Sitzung zum
persistenten Common-/libmodsecurity-Engine-Service öffnet. Der ausgewählte
Host-Läufer verwendet dafür einen eigenen privaten Socket und einen
laufbezogenen Event-Pfad; ein eingecheckter Socket-Pfad wird nicht
wiederverwendet. Damit wird gezieltes P1--P4-Hostverhalten geprüft, ohne einen
Capability-, CRS-Vollständigkeits-, Safe-/Strict- oder Produktions-Claim zu
fördern.

Das UDS-Protokoll lehnt unbekannte Engine-Aktionen ab, statt sie als
HTTP-Ablehnung umzudeuten. Ein disruptives Ergebnis wird erst gemeldet, wenn
der tatsächliche `ResponseWriter`-Write erfolgreich war. Nach dem Response-
Commit ist ein disruptives Ergebnis aus Phase 4 bewusst `log_only`; es
synthetisiert weder einen geänderten Status noch Reset oder Client-Abbruch.

## Lokale Quellenprüfungen

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

Das Build-Skript führt `go test ./...`, `go vet ./...` und (für `build`)
`go build ./...` aus. Es schreibt nur einen Kompilierungsbericht außerhalb des
Checkouts, standardmäßig nach
`$BUILD_ROOT/traefik-native-middleware/build.txt`. Es installiert kein
Traefik-Plugin, startet nicht die persistente Engine, ruft nicht
Common/libmodsecurity auf und schreibt keine Runtime-Evidenz.

## Begrenztes Fuzzing des UDS-Parsers

`FuzzUDSFrameAndResult` prüft den eigenen UDS-Frame-Reader und Result-Parser
mit abgeschnittenen, fehlerhaften, Allow-, Deny- und Redirect-Seeds sowie
beliebigen begrenzten Frames. Es verwendet nur einen In-Memory-Reader: Es
öffnet keinen Socket, startet keine Engine und ruft weder CGo noch Common auf.
Ein fehlerhafter Frame muss ohne Panic einen Fehler liefern. Jeder erfolgreich
geparste Frame muss zu seinen konsumierten Bytes unverändert round-trippen
können (weitere Stream-Frames können folgen), und ein erfolgreich geparstes
Result muss eine erkannte Aktion enthalten.
Das Build-Skript führt `go test ./...`, `go vet ./...` und (für `build`) `go
build ./...` aus. Standardmäßig schreibt es nur einen Kompilierungsbericht
außerhalb des Checkouts nach
`$BUILD_ROOT/traefik-native-middleware/build.txt`. Es installiert kein
Traefik-Plugin, startet keine persistente Engine, ruft Common/libmodsecurity
nicht auf und schreibt keine Laufzeitnachweise.

## Begrenztes Fuzzing des UDS-Parsers

`FuzzUDSFrameAndResult` prüft den benutzerdefinierten UDS-Frame-Reader und
Result-Parser mit abgeschnittenen, fehlerhaften sowie Allow-, Deny- und
Redirect-Seeds und beliebigen begrenzten Frames. Es wird nur ein
In-Memory-Reader verwendet: Der Test öffnet keinen Socket, startet keine
Engine und ruft weder CGo noch Common auf. Ein fehlerhafter Frame muss ohne
Panic einen Fehler liefern. Jeder erfolgreich geparste Frame muss unverändert
auf die von ihm verbrauchten Bytes zurückführbar sein (weitere Stream-Frames
können folgen), und ein erfolgreich geparstes Result muss eine bekannte Aktion
enthalten.

Führen Sie dieselbe begrenzte Prüfung aus diesem Modulverzeichnis aus:

```sh
GOTOOLCHAIN=local go test -mod=readonly -run='^$' -fuzz='^FuzzUDSFrameAndResult$' -fuzztime=15s -parallel=1 .
```

Der repositoryeigene Source-Level-Runner führt diese Kontrolle mit derselben
15-Sekunden- und Single-Worker-Grenze aus. Sie ist Parser-Evidenz auf
Source-Level, keine Traefik-Host-Runtime- oder Capability-Promotion-Evidenz.
Der `traefik-go`-CodeQL-Job führt diese Prüfung mit derselben Begrenzung von
15 Sekunden und einem Worker aus. Dies ist ein Source-Level-Nachweis für den
Parser, kein Nachweis für Traefik-Host-Runtime oder Capability-Promotion.

## Konfigurationsgrenze

`../config/traefik-native-middleware-static.yaml` und
`../config/traefik-native-middleware-dynamic.yaml` sind passende Formen für
ein lokales Plugin und einen File Provider mit einer vom Operator angelegten
Registrierung namens `modsecurityNative`. Sie sind bewusst von
`../config/traefik-forwardauth-dynamic.yaml` getrennt. Das Hostziel
`full-lifecycle-traefik-native` staged unabhängig einen äquivalenten
wegwerfbaren Arbeitsbereich, baut und startet den lokalen Engine-Dienst und
prüft das Laden des Plugins im gepinnten Host. Es verwendet weder diese
eingecheckten Referenzdateien noch einen gemeinsam genutzten Engine-Socket.
Eine Operator-Bereitstellung muss das Modul weiterhin im lokalen
Plugin-Arbeitsbereich der installierten Traefik-Version bereitstellen. Der
Probe-Lauf ist kein Einsatz- oder Capability-Promotion-Nachweis.
`../config/traefik-native-middleware-dynamic.yaml` sind passende
Local-Plugin- und File-Provider-Formen für eine vom Betreiber angelegte
Registrierung namens `modsecurityNative`. Sie sind bewusst getrennt von der
ausgewählten `../config/traefik-forwardauth-dynamic.yaml`. Das Hostziel
`full-lifecycle-traefik-native` richtet unabhängig davon einen gleichwertigen
temporären Arbeitsbereich ein, baut und startet den lokalen Engine-Service und
prüft das Laden des Plugins im angehefteten Host. Es verwendet weder diese
eingecheckten Referenzdateien noch einen gemeinsam genutzten Engine-Socket.
Für einen Betreibereinsatz muss das Modul weiterhin im Local-Plugin-
Arbeitsbereich der installierten Traefik-Version abgelegt werden. Die Prüfung
ist kein Deployment- oder Capability-Promotion-Nachweis.
