# Native Traefik-Streaming-Middleware-Quelle

**Sprache:** [English](README.md) | Deutsch

Dabei handelt es sich um ein Repository-eigenes Go-Paket, das für die Go-Middleware von Traefik konzipiert ist
Einstiegspunkte: `CreateConfig`, `New` und `ServeHTTP`. `New` verfügt über die erforderlichen
`(http.Handler, error)`-Signatur und `.traefik.yml` zeichnen Plugin-Metadaten auf
und Testdaten. Es verwendet nur die Go-Standardbibliothek. Traefik liefert den nächsten
`http.Handler`, wenn ein Plugin geladen wird. Der Full-Lifecycle-Runner führt dies durch
Paket unter einem angehefteten lokalen Traefik-Plugin-Arbeitsbereich; es ersetzt nicht das
Sie können den vorhandenen C `forwardAuth`-Kompatibilitätsdienst deaktivieren oder dessen Leistungsfähigkeit ändern
Erklärung.

## Was die Quelle tut

- Umschließt den Anforderungstext, sodass Lesevorgänge auf `maxRequestChunkBytes` begrenzt und gesendet werden
  synchron zu einer `Transaction`-Naht pro Anforderung;
- umschließt den Antwortschreiber, wertet Antwortheader vor dem Commit aus und
  schneidet jeden `Write` vor der Weiterleitung in `maxResponseChunkBytes`-Rückrufe
  jede Scheibe;
- implementiert `http.Flusher`, `http.Hijacker`, `http.Pusher`, `io.ReaderFrom`,
  und `Unwrap`; `ReadFrom` behält den schnellen Pfad des umschlossenen Autors nach einem bei
  begrenzter erster Block;
- Behält nur Metadaten und Byte-/Chunk-Zähler in `Summary`, niemals einen vollständigen
  Anfrage- oder Antworttext;
- behandelt ein störendes Ergebnis nach der Reaktionsverpflichtung als `log_only`; das tut es
  einen geänderten Status, eine Zurücksetzung oder einen Client-Abbruch-Anspruch nicht synthetisieren.

Die Form des optionalen Motors ist beabsichtigt. `New` ist standardmäßig auf
`PassthroughEngine` für eine reine Quellkonfiguration, während `engineMode: uds`
Öffnet eine private Unix-Domain-Socket-Sitzung pro `ServeHTTP` für den Persistenten
Common/libmodsecurity-Engine-Dienst. Der ausgewählte Host-Läufer stellt seine bereit
eigener privater Socket und lauflokaler Ereignispfad; Ein eingechecktes Objekt wird nicht wiederverwendet
Socket-Pfad. Es beweist gezieltes P1--P4-Wirtsverhalten, ohne a zu fördern
Fähigkeit, CRS-Vollständigkeit, sicher/streng oder Produktionsbereitschaft.

Das UDS-Protokoll lehnt unbekannte Engine-Aktionen ab, anstatt sie als neu zu kennzeichnen
eine HTTP-Ablehnung. Es meldet ein störendes Ergebnis erst nach dem tatsächlichen
`ResponseWriter`-Schreibvorgang erfolgreich. Nach Reaktionseinsatz eine disruptive Phase
4 Ergebnis ist bewusst `log_only`; es stellt keinen geänderten Status dar,
Reset oder Client-Abbruch-Anspruch.

## Lokale Quellenprüfungen

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

Das Build-Skript führt `go test ./...`, `go vet ./...` und (für `build`) „go“ aus
build ./...`. Standardmäßig wird nur ein Kompilierungsbericht außerhalb des Checkouts geschrieben
an `$BUILD_ROOT/traefik-native-middleware/build.txt`. Es wird kein installiert
Traefik-Plugin, starten Sie die persistente Engine, rufen Sie Common/libmodsecurity auf, oder
Laufzeitbeweise schreiben.

## Begrenztes Fuzzing des UDS-Parsers

`FuzzUDSFrameAndResult` übt den eigenen UDS-Frame-Reader und Result-Parser mit
abgeschnittenen, fehlerhaften, Allow-, Deny- und Redirect-Seeds sowie beliebigen
begrenzten Frames aus. Er verwendet nur einen In-Memory-Reader: Er öffnet keinen
Socket, startet keine Engine und ruft weder CGo noch Common auf. Ein fehlerhafter
Frame muss ohne Panic einen Fehler liefern; jeder erfolgreich geparste Frame muss
zu seinen konsumierten Bytes unverändert round-trippen dürfen (weitere Stream-Frames
können folgen), und ein erfolgreich geparstes Result muss eine erkannte Aktion haben.

Führen Sie dieselbe begrenzte Kontrolle aus diesem Modulverzeichnis aus:

```sh
GOTOOLCHAIN=local go test -mod=readonly -run='^$' -fuzz='^FuzzUDSFrameAndResult$' -fuzztime=15s -parallel=1 .
```

Der `traefik-go`-CodeQL-Job führt diese Kontrolle mit derselben 15-Sekunden-
und Single-Worker-Grenze aus. Es handelt sich um Source-Level-Parser-Evidence,
nicht um Traefik-Host-Runtime- oder Capability-Promotion-Evidence.

## Konfigurationsgrenze`../config/traefik-native-middleware-static.yaml` und
`../config/traefik-native-middleware-dynamic.yaml` sind passende lokale Plugins
und Dateianbieterformen für eine vom Bediener erstellte Registrierung mit dem Namen
`modsecurityNative`. Sie sind bewusst von den Auserwählten getrennt
`../config/traefik-forwardauth-dynamic.yaml`. Die
Das `full-lifecycle-traefik-native`-Hostziel stellt unabhängig ein Äquivalent bereit
Verfügbarer Arbeitsbereich, erstellt und startet den lokalen Engine-Dienst und bestätigt
Laden des Plugins im angepinnten Host. Diese eingecheckten Referenzen werden nicht wiederverwendet
Dateien oder einen gemeinsam genutzten Engine-Socket. Eine Betreiberbereitstellung muss weiterhin durchgeführt werden
Modul unter dem lokalen Plugin-Arbeitsbereich, der von der installierten Traefik-Version verwendet wird.
Bei der Untersuchung handelt es sich nicht um einen Einsatz- oder Fähigkeitsförderungsbeweis.
