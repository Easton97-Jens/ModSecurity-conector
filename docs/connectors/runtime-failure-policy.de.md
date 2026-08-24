# Laufzeit-Fehlerpolicy der Connectoren

**Sprache:** [English](runtime-failure-policy.md) | Deutsch

**Scope:** Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy `ext_authz`,
Envoy `ext_proc`, Traefik `forwardAuth`, Traefik Native UDS, lighttpd Stock
und lighttpd Patched.

Dieses Dokument ist der gemeinsame Vertrag für Fehler-, Verfügbarkeits- und
Cleanup-Pfade. Es trennt die beabsichtigte Policy (`implemented policy`) von
dem, was in diesem Checkout tatsächlich ausgeführt wurde (`local evidence`).
Ein Source-Check oder Connector-Selbsttest ist kein Nachweis, dass jeder
ausgewählte Host und jedes Protokoll ausgeführt wurde.

## Entscheidungsregeln

Die Standardsicherheitsentscheidung ist fail-closed. Ein protokollbezogener
Peer-Fehler darf nur den betroffenen Peer schließen, aber niemals für eine
Transaktion zu einer Allow-Entscheidung führen. Eine ausdrückliche
Produkteinstellung wie SPOP `fail-mode=open` bleibt ein Betreiber-Override und
wird als solcher ausgewiesen; sie ist kein stillschweigender Fallback.

In den vom Projekt gelieferten HAProxy-SPOE/SPOP-Beispielen mit geschlossenem
Default darf HAProxy `option continue-on-error` nicht gesetzt werden. Dieses
HAProxy-Opt-in ist mit `fail-mode=closed` inkompatibel: Ein nicht verfügbarer
oder fehlerhafter Agent könnte sonst als Allow behandelt werden. Der gelieferte
Harness lässt die Option weg. Ein Admission- oder Handshake-Fehler ohne ACK ist
ein geschlossener SPOP-Transportfehler für diesen Peer; ein explizites
Failure-ACK wird auf `503` abgebildet. Der genaue native-HAProxy-Clientstatus
für ein unbestätigtes Admission-Close ist `NOT_EXECUTED`; er wird niemals als
Allow dokumentiert. Ein Peer-lokaler Admission- oder Handshake-Fehler schließt
nur diesen Peer und blockiert niemals die globale Accept-/HELLO-Schleife.

Die SPOP-Response-Verarbeitung ist zustandsbehaftet. Fehlt ihre passende
Request-Transaktion nach begrenzter Cache-Eviction, Teardown oder einem
nicht zuordenbaren Response-NOTIFY, liefert sie immer `deny`/`503`,
`disruptive=1`, `fail-closed` und
`stateful_response_transaction_missing_closed`. Dieses eng begrenzte
closed-Verhalten gilt auch, wenn gewöhnliche Engine-Fehler ausdrücklich mit
`fail-mode=open` konfiguriert wurden: Bei Korrelationsverlust ist
Response-Enforcement nicht entscheidbar und darf nie still zu `pass`/`200`
werden.

Jede fehlgeschlagene Transaktion bzw. jeder Stream muss Transaktionszustand,
Buffer, Dateideskriptoren, Goroutines/Threads sowie eigene Socket-/Port-
Ressourcen freigeben. Cleanup ist idempotent. Eine legitime Anfrage auf einer
neuen oder wiederverwendeten Verbindung muss nach einem Fehler möglich sein,
sofern der Host nicht absichtlich beendet wurde. Wenn ein nativer Engine-Aufruf
nicht unterbrechbar ist, verwendet der begrenzte Shutdown-Pfad einen
definierten kontrollierten Neustart, statt von einem Worker noch verwendeten
Zustand zu zerstören.

### Verhaltensklassen

| Klasse | Fail-Modus | Hostaktion | HTTP-/Protokollstatus | Event | Wirkung | Cleanup | Folgeanfrage |
|---|---|---|---|---|---|---|---|
| E — Engine-Fehler | closed | Aktuelle Entscheidung abbrechen und Transaktion beenden | Apache/NGINX/lighttpd: `500`; HAProxy/Traefik: `500`/`503`; Envoy: gRPC `Unavailable`/`DeadlineExceeded` | `engine_error` plus Fehlerlog | Anfrage scheitert sichtbar; Betreiber erhält Fehler | Engine-Transaktion, Buffer und fehlerhaften Stream freigeben | Neue Anfrage darf starten |
| P — Peer-/Protokollabbruch | closed für betroffene Transaktion | Nur betroffenen Peer/Stream schließen; keine Teilentscheidung fortsetzen | HTTP `400`/`502`/`503`; gRPC `Cancelled`/`Unavailable`; SPOP disconnect/closed ACK | `peer_error` oder `protocol_error` | Ein Peer scheitert, andere bleiben verfügbar | Cancel, FD schließen, Teilframe verwerfen, Transaktionszustand entfernen | Frischer Peer wird angenommen; keine globale Blockade |
| I — Ungültiges/unvollständiges Ergebnis | closed | Ergebnis verwerfen und aktuelle Transaktion abbrechen | Wie E; kein teilweises Allow | `invalid_engine_response`/`incomplete_engine_response` | Fehlerhafte Engine-Daten werden nie vertraut | Parser-/Ergebnisbuffer freigeben, genau einmal zerstören | Neue Engine-Transaktion |
| C — Cancel/Shutdown | closed für laufende Arbeit | Cancel weitergeben, Stream schließen, neue Arbeit stoppen | HTTP `499`/`503`; gRPC `Cancelled` | `cancelled` oder `shutdown` | Laufende Arbeit endet; begrenzter Shutdown oder Neustart | Idempotentes Cancel, Worker-/FD-/UDS-Cleanup; ggf. Neustart | Nach Neustart neue Kontrollanfrage |
| L — Limit/Admission | closed | Überlimit vor unbounded State-Allokation ablehnen | HTTP `413`/`431`/`503`; gRPC `ResourceExhausted` | `limit_rejected` | Begrenzte Ablehnung; Dienst bleibt verfügbar | Admission-Slot und Teilbuffer freigeben | Anfrage innerhalb des Limits gelingt |
| A — Legitime Kontrolle | konfigurierte Entscheidung | Allow-/Block-Entscheidung unverändert bewahren | Normaler konfigurierter Status | `decision` | Positiv bleibt positiv, Block bleibt blockiert | Normales Erfolgs-Cleanup | Muss nach Fehlern gelingen |
| U — Cleanup-Nachweis | n/a | Prozess, Port, UDS, Stream und Zustand prüfen | Kein veralteter Listener/Stream | `cleanup_complete`/`cleanup_error` | Sicherer Retry/Reload; Leaks sind Findings | Doppelte Bereinigung ist harmlos | Kein alter Zustand blockiert Folgeanfrage |

`SELF_TEST_PASS` bedeutet: lokaler Runtime-/Selbsttest lief erfolgreich.
`SOURCE_VALIDATED` bedeutet: fokussierter Source-/Contract-Test bestanden.
`BLOCKED_ENVIRONMENT` bezeichnet eine fehlende Host-/Runtime-Voraussetzung;
`NOT_EXECUTED` macht keinen Erfolgsclaim. `NOT_APPLICABLE` bezeichnet einen
Vektor, den die betreffende Protokollroute nicht besitzt.

## Connector-spezifische Policy und Evidence

Die folgenden Tabellen wiederholen die 17 Vektoren je Connector. Die
Klassen-Spalte verweist auf Host-Aktion, Status, Event, Auswirkung, Cleanup und
Folgeanfrage im vollständigen Vertrag oben. Die Evidence ist auf dieses
Repository begrenzt.

### Vektoren

| ID | Fehlervektor |
|---|---|
| V1 | Engine beim Start nicht verfügbar |
| V2 | Engine fällt während einer Transaktion aus |
| V3 | Engine überschreitet Operation-Timeout |
| V4 | Engine liefert ungültige Antwort |
| V5 | Engine liefert unvollständige Antwort |
| V6 | Client schließt vorzeitig |
| V7 | Backend/Upstream schließt vorzeitig |
| V8 | Peer sendet unvollständigen Handshake |
| V9 | TCP-, TLS-, UDS- oder gRPC-Verbindung wird zurückgesetzt |
| V10 | Request-Body endet vorzeitig |
| V11 | Response-Body endet vorzeitig |
| V12 | Host wird während aktiver Anfragen beendet |
| V13 | Connector oder Agent wird während aktiver Anfragen beendet |
| V14 | Mehrere Anfragen oder Streams laufen parallel |
| V15 | Größen-/Ressourcenlimits werden überschritten |
| V16 | Legitime Kontrollanfrage folgt dem Fehler |
| V17 | Cleanup nach Erfolg, Fehler, Timeout und Cancel |

In den Tabellen sind die Statusbegriffe technische Evidence-Literale und keine
Übersetzungsvarianten.

### Apache

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Startup-Fehler liefert `500` und `AP_CONN_CLOSE` |
| V2 | E | SOURCE_VALIDATED: Native-API-Erfolg muss `1` sein |
| V3 | E | SOURCE_VALIDATED: terminaler Fehler; Timeout BLOCKED_ENVIRONMENT |
| V4 | I | NOT_EXECUTED: ungültiges Engine-Ergebnis |
| V5 | I | NOT_EXECUTED: unvollständiges Engine-Ergebnis |
| V6 | P | SOURCE_VALIDATED: Connection-/URI-Fehler schließen Anfrage |
| V7 | P | NOT_EXECUTED: Live-Backend-/Upstream-Close |
| V8 | P | NOT_APPLICABLE: kein Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-TCP-/TLS-Reset |
| V10 | I | SOURCE_VALIDATED: Request-Body-Append-/File-Fehler schließen mit `500` |
| V11 | I | SOURCE_VALIDATED: Response-Body-Append-Fehler schließen mit `500` |
| V12 | C | NOT_EXECUTED: Live-Host-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | SOURCE_VALIDATED: Poolpfade begrenzt; paralleler Host-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: Limitpfade begrenzt; vollständiger Host-Limit-Run NOT_EXECUTED |
| V16 | A | NOT_EXECUTED: Same-Host-Folgeanfrage nach Fehler; isolierte aktuelle Host-Allow-`200`- und P1/P2-Block-`403`-Kontrollen bestanden |
| V17 | U | SELF_TEST_PASS: task-eigene Apache-Ports/-Prozesse fehlten nach jedem aktuellen Hostfall; Live-FD-Audit NOT_EXECUTED |

### NGINX

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Startup-Enginefehler finalisieren mit `500` |
| V2 | E | SOURCE_VALIDATED: Native-Enginefehler finalisieren mit `500` |
| V3 | E | SOURCE_VALIDATED: terminaler Fehler; Timeout BLOCKED_ENVIRONMENT |
| V4 | I | SOURCE_VALIDATED: ungültiges Ergebnis finalisiert mit `500` |
| V5 | I | SOURCE_VALIDATED: unvollständiges Ergebnis finalisiert mit `500` |
| V6 | P | SOURCE_VALIDATED: Request-Mapping-Fehler finalisieren Anfrage |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | NOT_APPLICABLE: NGINX-Modul hat keinen Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-TCP-/TLS-Reset |
| V10 | I | SOURCE_VALIDATED: Request-Body-Fehler finalisieren `500` |
| V11 | I | SOURCE_VALIDATED: Response-Body-Fehler finalisieren `500` |
| V12 | C | NOT_EXECUTED: Live-Worker-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | SOURCE_VALIDATED: Worker-Pfade begrenzt; paralleler Host-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: Body-Pfade begrenzt; vollständiger Host-Limit-Run NOT_EXECUTED |
| V16 | A | SELF_TEST_PASS: aktueller nativer NGINX-Host lieferte Allow `200` nach Header-Block `403` |
| V17 | U | SELF_TEST_PASS: aktueller nativer Port `29183` wurde entfernt; ein früherer Sandbox-Harness-Listener `29182` wurde als task-eigen verifiziert und kontrolliert bereinigt; Live-FD-Audit NOT_EXECUTED |

### HAProxy HTX

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Binding weist Startup-Native-Fehler ab |
| V2 | E | SOURCE_VALIDATED: direkte Native-API erfordert Ergebnis `1` |
| V3 | E | SOURCE_VALIDATED: terminaler Binding-Fehler; Live-Timeout BLOCKED_ENVIRONMENT |
| V4 | I | SOURCE_VALIDATED: ungültiges Native-Ergebnis wird abgewiesen |
| V5 | I | SOURCE_VALIDATED: unvollständiges Ergebnis wird abgewiesen |
| V6 | P | SOURCE_VALIDATED: Transaktionslokaler Binding-Fehler |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | NOT_APPLICABLE: HTX-Route hat keinen SPOE-Handshake |
| V9 | P | NOT_EXECUTED: Live-TCP-/TLS-Reset |
| V10 | I | SOURCE_VALIDATED: Request-Body-Append-Fehler ist terminal |
| V11 | I | SOURCE_VALIDATED: Response-Body-Append-Fehler ist terminal |
| V12 | C | NOT_EXECUTED: Live-HAProxy-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Filter-Terminierung |
| V14 | L | SOURCE_VALIDATED: Binding-Selftest bestanden; paralleler Host-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: begrenztes Binding-Input; Host-Limit-Run NOT_EXECUTED |
| V16 | A | SELF_TEST_PASS: `self-test-modsecurity-binding` erhält Block `403` |
| V17 | U | SOURCE_VALIDATED: Transaktions-Cleanup; Live-FD-Audit NOT_EXECUTED |

### HAProxy SPOE/SPOP

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Engine-Startupfehler ist für den Agenten terminal |
| V2 | E | SOURCE_VALIDATED: Enginefehler bleibt auf den Peer-Worker begrenzt |
| V3 | E | SOURCE_VALIDATED: Handshake-/Operations-Deadlines sind begrenzt |
| V4 | I | SOURCE_VALIDATED: fehlerhaftes Protokoll-/Ergebnis wird geschlossen; Default closed |
| V5 | I | SOURCE_VALIDATED: unvollständiges Ergebnis/Handshake wird geschlossen |
| V6 | P | SELF_TEST_PASS: Peer-Close beendet Agent nicht |
| V7 | P | NOT_APPLICABLE: Agent-Selbsttest hat keinen HTTP-Upstream |
| V8 | P | SELF_TEST_PASS: unvollständiges/langsames HELLO wird per Deadline abgewiesen |
| V9 | P | SELF_TEST_PASS: `MSG_NOSIGNAL`-/Peer-Reset-Pfad erholt sich |
| V10 | P | NOT_APPLICABLE: SPOP hat keine HTTP-Request-Body-Hooks |
| V11 | P | NOT_APPLICABLE: SPOP hat keine HTTP-Response-Body-Hooks |
| V12 | C | SOURCE_VALIDATED: begrenztes Worker-Reaping und Listener-Shutdown |
| V13 | C | SOURCE_VALIDATED: Worker-Isolation verhindert Prozessfehler durch Peer |
| V14 | L | SELF_TEST_PASS: parallele Peers; gesättigter Peer wird lokal geschlossen und der Parent-Accept-Loop bleibt frei |
| V15 | L | SELF_TEST_PASS: Worker `1..64`, begrenzte Handshake-/Socket-Deadlines und sofortiger Peer-lokaler Close bei Sättigung |
| V16 | A | SELF_TEST_PASS: auf Cache-Miss `503` folgen Block-ACK `403` und frische Allow-Kontrolle `200` |
| V17 | U | SELF_TEST_PASS: direkter Cache-Miss-Agent und Selbsttest-Listener sind geschlossen; Peer-FDs sind geschlossen |

SPOP-Schreibvorgänge verwenden pro Send `MSG_NOSIGNAL` (und, wenn verfügbar,
`SO_NOSIGPIPE`); `SIGPIPE` wird nicht global ignoriert. Jeder Peer ist in einem
begrenzten Worker isoliert; fehlerhafte Eingaben verwenden standardmäßig
closed. `fail-mode=open` ist nur ein sichtbarer Betreiber-Override.

Der aktuelle direkte Protokolllauf nutzt `max-transactions=1`, um Request A
durch Request B zu evicten. Das spätere Response-NOTIFY für A ergab
`deny`/`503`/`stateful_response_transaction_missing_closed`; ein echter
Rule-Block blieb `403`, frisches Allow blieb `200`. Das ist Evidence des
Produktionsagenten, keine Behauptung zum nativen HAProxy-Clientstatus oder
FD-Audit.

`connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh` reproduziert
dieselbe Sequenz gegen einen aktuellen Agenten, wenn Build- und Runtime-Root
explizit task-eigen sind. Der Harness prüft Cache-Miss `503`, echten Block
`403` und frisches Allow `200` und beendet den Agenten anschließend im
Cleanup-Pfad.

### Envoy `ext_authz`

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Common-Authorization-Service weist nicht verfügbare Engine ab |
| V2 | E | SOURCE_VALIDATED: Worker liefert geschlossenes Authorization-Ergebnis |
| V3 | E | SOURCE_VALIDATED: begrenztes Connection-/Worker-Warten; Live-Envoy NOT_EXECUTED |
| V4 | I | SOURCE_VALIDATED: ungültige Authorization-Antwort ist kein Allow |
| V5 | I | SOURCE_VALIDATED: unvollständige Antwort schließt Authorization-Anfrage |
| V6 | P | SOURCE_VALIDATED: Peer-lokaler Read-/`send_all`-Fehler schließt Worker |
| V7 | P | NOT_EXECUTED: Live-Envoy-Upstream-Close |
| V8 | P | NOT_APPLICABLE: HTTP-Authorization, kein SPOE-HELLO |
| V9 | P | SOURCE_VALIDATED: `MSG_NOSIGNAL`; Live-Reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: unvollständige Authorization-Anfrage abgewiesen |
| V11 | P | NOT_APPLICABLE: kein Upstream-Response-Body |
| V12 | C | SOURCE_VALIDATED: begrenzter Worker-Shutdown |
| V13 | C | SOURCE_VALIDATED: Worker-Ende ist kein Allow |
| V14 | L | SOURCE_VALIDATED: begrenzte Worker-Aufnahme; paralleler Envoy-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: Header-/Body-Grenzen vor Allokation |
| V16 | A | SOURCE_VALIDATED: Security-Header-Kontrollen erhalten |
| V17 | U | SOURCE_VALIDATED: Worker-Sockets; Live-Prozess-/FD-Audit NOT_EXECUTED |

### Envoy `ext_proc`

Das aktuelle Follow-up-Testfixture prüft nach Rückkehr des Idle-Handlers
`pendingReceives == 0`; Mutex- und Forced-Stop-Wartezeiten sind durch Deadlines
begrenzt. Ein bereits laufender, nicht unterbrechbarer nativer C-Destruktor
wird weiterhin als kontrollierter Nonzero-Restart behandelt, nicht als
in-process abbrechbar.

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Service-Konfiguration/Startup weist ungültige Engine ab |
| V2 | E | SOURCE_VALIDATED: Enginefehler liefert gRPC-Fehler, kein Allow |
| V3 | E | SOURCE_VALIDATED: Engine-Operation-Timeout getrennt von Stream-Idle |
| V4 | I | SOURCE_VALIDATED: ungültige Processing-Antwort schlägt Stream fehl |
| V5 | I | SOURCE_VALIDATED: unvollständige Processing-Nachricht schlägt Stream fehl |
| V6 | P | SOURCE_VALIDATED: Stream-Cancel gibt Zustand frei |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | NOT_APPLICABLE: gRPC-Stream ohne HTTP-Agent-HELLO |
| V9 | P | SOURCE_VALIDATED: gRPC-Reset ist Streamfehler; Live-Reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: Request-Body-EOF ist unvollständiger Stream |
| V11 | P | SOURCE_VALIDATED: Response-Body-EOF ist unvollständiger Stream |
| V12 | C | SELF_TEST_PASS: `TestCommonRuntimeEngineCloseHonorsShutdownContext` hält den Mutex, liefert innerhalb der Deadline `ErrCommonRuntimeShutdownTimeout`, und main beendet kontrolliert mit Exit `1` |
| V13 | C | SELF_TEST_PASS: Connector-/Agent-Terminierung nutzt den begrenzten kontrollierten Exit `1`; solange der Engine-Aufruf blockiert, erfolgt keine native Freigabe |
| V14 | L | SELF_TEST_PASS: `go test -race ./...`; parallele Streams begrenzt |
| V15 | L | SOURCE_VALIDATED: `max_concurrent_streams <= 1024`, Überbelegung `ResourceExhausted` |
| V16 | A | SELF_TEST_PASS: gültiger Stream nach Idle-Cleanup |
| V17 | U | SOURCE_VALIDATED: getaggter nativer Common-Runtime-Test `TestCommonRuntimeEngineCloseHonorsShutdownContext` belegt deadline-begrenztes Cleanup ohne native Freigabe; Live-Envoy-FD-Audit NOT_EXECUTED |

Engine-Operation-Timeout und serverseitiges Stream-Idle-Timeout sind getrennt.
Eine vollständige `ProcessingRequest` plus Antwort zählt als Aktivität und setzt
den Idle-Timer zurück. Aktive Langzeitstreams werden daher bei regelmäßiger
Aktivität nicht wegen des Engine-Timeouts beendet. Admission ist durch
`MaxConcurrentStreams` und das Service-Limit begrenzt.

### Traefik `forwardAuth`

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Common-Service schlägt bei nicht verfügbarer Engine fail-closed fehl |
| V2 | E | SOURCE_VALIDATED: Worker-/Authorization-Fehler ist kein Allow |
| V3 | E | SOURCE_VALIDATED: begrenztes Worker-Timeout; Live-Traefik NOT_EXECUTED |
| V4 | I | SOURCE_VALIDATED: ungültige Authorization-Antwort wird abgewiesen |
| V5 | I | SOURCE_VALIDATED: unvollständige Authorization-Antwort wird abgewiesen |
| V6 | P | SOURCE_VALIDATED: Peer-lokale Authorization-Verbindung wird geschlossen |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | NOT_APPLICABLE: kein SPOE-HELLO |
| V9 | P | SOURCE_VALIDATED: `MSG_NOSIGNAL`; Live-Reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: unvollständige Authorization-Anfrage abgewiesen |
| V11 | P | NOT_APPLICABLE: kein Upstream-Response-Body |
| V12 | C | SOURCE_VALIDATED: begrenzter Authorization-Worker-Shutdown |
| V13 | C | SOURCE_VALIDATED: Worker-Ende kann kein Allow werden |
| V14 | L | SOURCE_VALIDATED: begrenzte Worker-Aufnahme; paralleler Traefik-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: begrenzte Header-/Body-Behandlung |
| V16 | A | SOURCE_VALIDATED: normale Authorization-Kontrolle unverändert |
| V17 | U | SOURCE_VALIDATED: Worker-Sockets; Live-Traefik-FD-Audit NOT_EXECUTED |

### Traefik Native UDS

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SELF_TEST_PASS: Engine-Service-Startup/-Konfiguration ist begrenzt |
| V2 | E | SELF_TEST_PASS: Enginefehler wird als Protokollfehler zurückgegeben |
| V3 | E | SOURCE_VALIDATED: Worker-/Engine-Warten hat begrenzten Shutdown |
| V4 | I | SELF_TEST_PASS: fehlerhafte Engine-Antwort wird abgewiesen |
| V5 | I | SELF_TEST_PASS: unvollständige Antwort wird abgewiesen |
| V6 | P | SELF_TEST_PASS: Reset-Peer bleibt lokal; Folgeanfrage gelingt |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | SELF_TEST_PASS: unvollständiges Framing wird abgewiesen |
| V9 | P | SELF_TEST_PASS: UDS-Reset und RESULT-Writes von 64 nicht lesenden Peers beenden Service nicht |
| V10 | P | SOURCE_VALIDATED: unvollständiger Request-Frame wird abgewiesen |
| V11 | P | SELF_TEST_PASS: unvollständige/überlange Response wird abgewiesen |
| V12 | C | SOURCE_VALIDATED: aktive Sockets werden beim Service-Stop beendet |
| V13 | C | SOURCE_VALIDATED: festhängende Engine nutzt kontrollierten Neustart |
| V14 | L | SELF_TEST_PASS: 64 nicht lesende Peers füllen die Worker-Grenze; ein zusätzlicher Peer wird vor der Write-Deadline nicht bedient |
| V15 | L | SELF_TEST_PASS: Response- und Frame-Limits werden erzwungen |
| V16 | A | SELF_TEST_PASS: gültige Anfrage gelingt nach Reset und nach 31,0-Sekunden-Deadline eines nicht lesenden Peers |
| V17 | U | SELF_TEST_PASS: Reset-, Write-Deadline- und Ownership-Replacement-Pfade hinterlassen keinen eigenen UDS oder Prozess |

Der UDS-Shutdown begrenzt das Worker-Warten. Bei einem nicht unterbrechbaren
Engine-Aufruf entfernt der Service seinen eigenen Socket und beendet sich über
den kontrollierten Neustartpfad, ohne Worker-erreichbaren Zustand freizugeben.

Die Peer-Output-Write-Deadline ist eine eigene monotone 30-Sekunden-Deadline,
kein Engine-Operations- oder Receive-Timeout. `poll(POLLOUT)` plus
nicht-blockierendes `MSG_NOSIGNAL | MSG_DONTWAIT` schließt bei Ablauf nur den
nicht lesenden Peer. Der aktuelle native Service-Test füllte alle 64 Worker,
beobachtete vor Ablauf keinen bedienten Folgepeer, danach bei 31,0 Sekunden
eine frische Anfrage sowie vollständiges Socket-/Prozess-Cleanup; derselbe
Fall bestand unter ASan/UBSan.

### lighttpd Stock

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SELF_TEST_PASS: Stock-Host-Smoke startete, lieferte Baseline `200` und zeichnete Connector-Event auf |
| V2 | E | NOT_EXECUTED: Engine-Fehler während Transaktion |
| V3 | E | NOT_EXECUTED: Live-Timeout |
| V4 | I | NOT_EXECUTED: ungültiges Engine-Ergebnis |
| V5 | I | NOT_EXECUTED: unvollständiges Engine-Ergebnis |
| V6 | P | NOT_EXECUTED: Live-Client-Close |
| V7 | P | NOT_EXECUTED: Live-Backend-Close |
| V8 | P | NOT_APPLICABLE: kein Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-Reset |
| V10 | I | NOT_EXECUTED: vorzeitiges Request-Body-Ende |
| V11 | I | NOT_EXECUTED: vorzeitiges Response-Body-Ende |
| V12 | C | NOT_EXECUTED: Live-Host-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | NOT_EXECUTED: paralleler Host-Run |
| V15 | L | NOT_EXECUTED: maximale Größen-/Ressourcenlimits |
| V16 | A | SELF_TEST_PASS: Stock-Runtime-Smoke beobachtete Baseline `200` und Regelblock `403` |
| V17 | U | SELF_TEST_PASS: Smoke beobachtete Connector-Event und Listener-Cleanup |

### lighttpd Patched

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SELF_TEST_PASS: Patched-Host-Smoke startete, lieferte Baseline `200` und zeichnete Connector-Event auf |
| V2 | E | NOT_EXECUTED: Engine-Fehler während Transaktion |
| V3 | E | NOT_EXECUTED: Live-Timeout |
| V4 | I | NOT_EXECUTED: ungültiges Engine-Ergebnis |
| V5 | I | NOT_EXECUTED: unvollständiges Engine-Ergebnis |
| V6 | P | NOT_EXECUTED: Live-Client-Close |
| V7 | P | NOT_EXECUTED: Live-Backend-Close |
| V8 | P | NOT_APPLICABLE: kein Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-Reset |
| V10 | I | NOT_EXECUTED: vorzeitiges Request-Body-Ende |
| V11 | I | NOT_EXECUTED: vorzeitiges Response-Body-Ende |
| V12 | C | NOT_EXECUTED: Live-Host-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | NOT_EXECUTED: paralleler Host-Run |
| V15 | L | NOT_EXECUTED: maximale Größen-/Ressourcenlimits |
| V16 | A | SELF_TEST_PASS: Patched-Runtime-Smoke beobachtete Baseline `200` und Regelblock `403` |
| V17 | U | SELF_TEST_PASS: Smoke beobachtete Connector-Event und Listener-Cleanup |

## Grenze der Konfigurationsdokumentation

Die generierten Dateien unter `examples/*/configuration-reference*.md` wurden
nicht geändert. Generator und CI-Prüfungen lagen außerhalb dieses Tasks. Die
SPOP-Source-/Direktdokumentation sowie Envoy-`ext_proc`-Service-JSONs und
Direktdokumentation sind für die neuen Defaults maßgeblich, bis ein separat
autorisierter CI-Task den Generator ändern darf. Das ist eine Evidence-Grenze,
kein Claim, dass generierte Referenzen aktuell sind.

## Restrisiken und Folge-Evidence

Source- und fokussierte Selbsttests decken die implementierten Kontrollen ab,
darunter SPOP-Peer-Isolation, Traefik-UDS-Runtime-Test und Envoy
`go test -race ./...`. Vollständige Live-Host-Runs für alle zehn Routen,
TLS-/HTTP/2-/HTTP/3-Matrizen sowie Prozess-/FD-Leak-Audits bleiben oben als
`BLOCKED_ENVIRONMENT` oder `NOT_EXECUTED` markiert. Ein nicht unterbrechbarer
nativer Engine-Aufruf darf erst nach host-spezifischem Nachweis als graceful
In-Process-Cancel gelten; bis dahin gilt der kontrollierte Neustartpfad.

Ein Finding wird erst geschlossen, wenn Reproducer und positive Folgekontrolle
gegen den ausgewählten Host erneut laufen und Event-/Prozess-/Port-/UDS-Evidence
aufbewahrt wurde. Danach ist der Finding-Datensatz zu aktualisieren.
