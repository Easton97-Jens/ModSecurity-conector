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
| P — Peer-/Protokollabbruch | closed für betroffene Transaktion | Nur betroffenen Peer/Stream schließen; keine Teilentscheidung fortsetzen | HTTP `400`/`502`/`503`; gRPC `Cancelled`/`Unavailable`; SPOP disconnect/closed ACK. Sind HTTP-Header bereits committed, den unvollständigen Transfer mit diesem committed Status beenden; keinen rückwirkenden Statuswechsel erfinden. | Connector-eigener Peer: `peer_error` oder `protocol_error`; host-eigener Upstream: transaktionsgebundener Host-/Proxy-Error-Record. Fehlender Record ist eine Evidenzlücke und wird nie abgeleitet. | Ein Peer scheitert, andere bleiben verfügbar | Cancel, FD schließen, Teilframe verwerfen, Transaktionszustand entfernen | Frischer Peer wird angenommen; keine globale Blockade |
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
| V4 | I | SOURCE_VALIDATED: ungültiges Native-Ergebnis wird abgewiesen |
| V5 | I | SOURCE_VALIDATED: unvollständiges Body-/Header-Ergebnis wird abgewiesen |
| V6 | P | SOURCE_VALIDATED: Connection-/URI-Fehler schließen Anfrage |
| V7 | P | BLOCKED_ENVIRONMENT: diagnostisches Early-Close lieferte Proxy-`502`, aber valides Follow-up und Owner-verifizierbarer Cleanup sind durch nicht zuordenbare Listener auf den Task-Ports `29471/29472` blockiert |
| V8 | P | NOT_APPLICABLE: kein Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-TCP-/TLS-Reset |
| V10 | I | SOURCE_VALIDATED: Request-Body-Append-/File-Fehler schließen mit `500` |
| V11 | I | SOURCE_VALIDATED: Response-Body-Append-Fehler schließen mit `500` |
| V12 | C | NOT_EXECUTED: Live-Host-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | SOURCE_VALIDATED: Poolpfade begrenzt; paralleler Host-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: Limitpfade begrenzt; vollständiger Host-Limit-Run NOT_EXECUTED |
| V16 | A | BLOCKED_ENVIRONMENT: das V7-Diagnose-Follow-up-Backend war fehlerhaft geframt; keine valide Same-Host-Post-Fault-Kontrolle wird behauptet |
| V17 | U | BLOCKED_ENVIRONMENT: nach der V7-Diagnose blieben die Task-Ports `29471/29472` ohne zuordenbare PID im Listen; kein unsicheres Signal wurde gesendet und Live-FD-Audit bleibt NOT_EXECUTED |

Das beobachtete Apache-`502` ist nur diagnostische Evidence für den erwarteten
Proxy-Fehlermodus. Es ist kein V7-Abnahmeresultat: Die Follow-up-Fixture war
ungültig und die aktuelle Sandbox kann die zwei verbliebenen Listener nicht
sicher zuordnen oder bereinigen. Frühere isolierte Allow/Block-Fälle ersetzen
diese V7-spezifische Cleanup-Lücke nicht; sie wird als `FND-HOST-0007`
verfolgt.

### NGINX

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Startup-Enginefehler finalisieren mit `500` |
| V2 | E | SOURCE_VALIDATED: Native-Enginefehler finalisieren mit `500` |
| V3 | E | SOURCE_VALIDATED: terminaler Fehler; Timeout BLOCKED_ENVIRONMENT |
| V4 | I | SOURCE_VALIDATED: ungültiges Ergebnis finalisiert mit `500` |
| V5 | I | SOURCE_VALIDATED: unvollständiges Ergebnis finalisiert mit `500` |
| V6 | P | SELF_TEST_PASS: deklarierter 100-Byte-Upload sendete 5 Byte und dann FIN; der Client erhielt keine Response-Bytes, NGINX loggte `400`, der Host überlebte und Same-Host-Controls blieben nutzbar |
| V7 | P | SELF_TEST_PASS: begrenzter Native-Host-Upstream sendete 21 von deklarierten 128 Byte; NGINX loggte frühes Upstream-Close, der Client sah committed `200` und danach Transferfehler (`curl_exit=18`, 107 Byte fehlend), der Host überlebte und valide `200 -> 403 -> 200`-Kontrollen folgten |
| V8 | P | NOT_APPLICABLE: NGINX-Modul hat keinen Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-TCP-/TLS-Reset |
| V10 | P | SELF_TEST_PASS: deklarierter 100-Byte-Upload sendete 5 Byte und dann TCP-RST; der Client erhielt keine Response-Bytes, NGINX loggte `400`, der Host überlebte und Same-Host-Controls blieben nutzbar; dies beweist V9 nicht separat |
| V11 | I | SOURCE_VALIDATED: Response-Body-Fehler finalisieren `500` |
| V12 | C | NOT_EXECUTED: Live-Worker-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | SELF_TEST_PASS: ein direkter Native-Host-Run bediente 16 parallele HTTP/1.1-Requests (8 Allow `200`, 8 Block `403`) in einem weiterlaufenden Prozess; dies ist nur Direct-Host-Evidence, während der Worker-Identity-Harness `BLOCKED_ENVIRONMENT` bleibt |
| V15 | L | SOURCE_VALIDATED: Body-Pfade begrenzt; vollständiger Host-Limit-Run NOT_EXECUTED |
| V16 | A | SELF_TEST_PASS: der V6/V10-Native-Host und der V7-Native-Host lieferten nach ihren fehlgeschlagenen Transfers jeweils Allow `200`, Block `403`, dann Allow `200`; derselbe Direct-Host bewahrte auch nach dem parallelen 16-Request-Batch `200 -> 403 -> 200` |
| V17 | U | SELF_TEST_PASS: V6/V10-Prozesse und -Port `29583`, V7-Prozesse und -Ports `29371/29372` sowie Direct-Parallel-Host/Prozess/Port `29671` fehlten nach begrenztem Stop; der separate aktuelle Port `29183` wurde ebenfalls freigegeben und ein späterer Recheck fand weder `29182` noch `29183` als Listener; Live-FD-Audit NOT_EXECUTED |

Für die NGINX-V7-Fixture hatte der Upstream bereits HTTP-`200`-Header
committed, bevor er schloss. Der Client beobachtet daher einen beendeten,
unvollständigen HTTP-Transfer statt eines nachträglich umgeschriebenen
`502`; `curl_exit=18` und die fehlenden Bytes sind die Fehler-Evidence.
Dies ist ein peer-lokales geschlossenes Transportergebnis, keine
fail-open-Autorisierungsentscheidung und keine stille Änderung des
ModSecurity-Sicherheitsmodells.

Bei der NGINX-V6/V10-Upload-Fixture hatte der Client bereits geschlossen,
bevor NGINX das serverseitige `400` senden konnte; null Client-Response-Bytes
und das Access-Log-`400` sind daher konsistent. Das Request-Level-TCP-RST
verwendet dieselbe unvollständige Upload-Form und wird nicht als separater
Transport-Reset-Nachweis V9 hochgestuft.

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
| V10 | I | SELF_TEST_PASS: Ein aus `ProcessPartial` abgeleiteter nativer Append-Fehler liefert `-1`; aktuelle HAProxy-`3.2.22`-HTTP/1.1-Host-Evidence beobachtete `400`, null Backend-Dispatches, Same-Process-One-Byte-POST-Allow `200` und Listener-Cleanup |
| V11 | I | SELF_TEST_PASS: Ein aus `ProcessPartial` abgeleiteter nativer Append-Fehler liefert `-1`; aktuelle HAProxy-`3.2.22`-HTTP/1.1-Host-Evidence beobachtete ein Close des betroffenen Streams ohne HTTP-Response (`000`, `curl_exit=52`), einen Upstream-Fehlerrequest, Same-Process-HEAD-Allow `200` und Listener-Cleanup |
| V12 | C | NOT_EXECUTED: Live-HAProxy-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Filter-Terminierung |
| V14 | L | SOURCE_VALIDATED: Binding-Selftest bestanden; paralleler Host-Run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: begrenztes Binding-Input; Host-Limit-Run NOT_EXECUTED |
| V16 | A | SELF_TEST_PASS: `self-test-modsecurity-binding` erhält Block `403` |
| V17 | U | SOURCE_VALIDATED: Transaktions-Cleanup; Live-FD-Audit NOT_EXECUTED |

Der begrenzte Host-Lauf
`runtime-continuation/haproxy-htx-current-retry-20260825T073000Z` ist als
`native_host_runtime_nonpromoted` erfasst und keine vollständige
17-Vektor-Abnahme. Seine P1--P4-Evidence ist auf folgende Sequenz begrenzt:
Legitimes Allow lieferte `200`; P1 lieferte `403`/`429`; P2 lieferte `403`
ohne Upstream-Anfrage; P3 lieferte `403` nach einer Upstream-Anfrage; und P4
lieferte ein committed safe `log_only` `200`. Der Host-Receipt zeichnete
`processes_stopped=yes` und task-owned Cleanup auf. Diese Evidence hebt keinen
nicht ausgeführten Vektor hoch und belegt keinen vollständigen nativen
HAProxy-FD-/Leak-Audit.

Ein nativer HTX-Payload-Append-Fehler hat einen expliziten separaten Fail-Modus.
Das Binding betrachtet nur exakten nativen Append-Erfolg als inspizierbar;
jedes andere Ergebnis bricht die betroffene Transaktion ab und liefert `-1`,
niemals eine positive Payload-Länge. Für V10 ist dies im aufbewahrten Run ein
pre-commit fail-closed `400` ohne Backend-Dispatch. Für V11 können Header
bereits committed sein; die fail-closed Hostaktion ist dann peer-lokale
Transportterminierung statt einer synthetischen HTTP-Response. Für keinen der
beiden Callback-Fehler existiert derzeit ein dediziertes strukturiertes
Connector-Error-Event; der payload-freie Host-Receipt liefert die Event-Evidence.
Run `haproxy-htx-append-failure-20260825T131500Z`, SHA-256
`12e4d30c68ff46f45f2f8481d810eb53099f6512f384520e3942fadb0434da9c`, belegt
Same-Process-Controls und Listener-Cleanup nur für diese HTTP/1.1-Fälle. Er
hebt keine H2/H3-, Reload-, Full-FD-, Engine-Timeout- oder vollständige
17-Vektor-Coverage hoch.

### HAProxy SPOE/SPOP

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Engine-Startupfehler ist für den Agenten terminal |
| V2 | E | SOURCE_VALIDATED: Enginefehler bleibt auf den Peer-Worker begrenzt |
| V3 | E | SELF_TEST_PASS: Handshake-/Operations-Deadlines sind begrenzt; nicht unterstützter positiver Response-Body-Timeout wird bei der Konfigurationsverarbeitung abgewiesen |
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
| V14 | L | SELF_TEST_PASS: parallele Peers; Healthcheck-/Folge-HELLO gelingt, ein gesättigter Peer wird lokal geschlossen und der Parent-Accept-Loop bleibt frei |
| V15 | L | SELF_TEST_PASS: Worker `1..64`, `max-transactions` `1..4096` mit höchstens `65536` Slots über alle Worker, Headeranzahl-/Name-/Wert-/Aggregatgrenzen, begrenzte Handshake-/Socket-Deadlines und sofortiger Peer-lokaler Close bei Sättigung |
| V16 | A | SELF_TEST_PASS: deaktiviertes Response-Phasen-NOTIFY liefert `503`, danach folgen Block-ACK `403` und frische Allow-Kontrolle `200` |
| V17 | U | SELF_TEST_PASS: request-only Response-Guard-Agent und Selbsttest-Listener sind geschlossen; Selftest-Metadaten sind atomar im Besitz und entfernt, während das Log erhalten bleibt |

SPOP-Schreibvorgänge verwenden pro Send `MSG_NOSIGNAL` (und, wenn verfügbar,
`SO_NOSIGPIPE`); `SIGPIPE` wird nicht global ignoriert. Jeder Peer ist in einem
begrenzten Worker isoliert; fehlerhafte Eingaben verwenden standardmäßig
closed. `fail-mode=open` ist nur ein sichtbarer Betreiber-Override.

Der ausgewählte SPOP-Pfad hat keinen Response-Body-Stream. Bei
`response-companion=none` wird ein positiver `response-body-timeout` durch die
Konfigurationsvalidierung vor dem Serverstart mit Exit `2` abgewiesen;
Zero/Default bleibt akzeptiert und `spoe-timeout` bleibt eine per-Frame-
Peer-Deadline. Das ist ein expliziter fail-closed-Konfigurationsfehler, kein
behauptetes Stream-Idle-Limit. Selftest-PID-, Ready- und Port-Pfade werden mit
`O_CREAT|O_EXCL` (und `O_NOFOLLOW`, falls
verfügbar) geclaimt; eine Kollision wird abgewiesen, ohne einen aufrufer-
eigenen Pfad zu ändern, und Cleanup entfernt nur eigene Pfade.

`spoe-timeout` akzeptiert nur `1..60000` Millisekunden und `worker-count` nur
`1..64`; Null-, negative, überlaufende und nachgestellte Textwerte werden vor
der Konvertierung abgewiesen. Typisierte Peer-Strings, die einschließlich ihres
abschließenden NUL nicht in ihr Ziel passen, werden ebenfalls abgewiesen statt
stillschweigend gekürzt. Dies sind Peer-lokale bzw. Konfigurations-
fail-closed-Ergebnisse; reguläre Werte behalten ihr bestehendes Verhalten.

Jeder `headers_bin`-, Text-Header- und Response-Header-Parse schlägt
fail-closed fehl, bevor mehr als 256 Header, ein 256-Byte-Name, ein
8192-Byte-Wert oder insgesamt 16384 Header-Bytes alloziert werden. Der
Headervektor wächst nur geometrisch bis zu dieser Grenze; eine fehlgeschlagene
Name-/Wert-Allokation hinterlässt keinen teilweise besessenen Eintrag.
`max-transactions` akzeptiert nur `1..4096`; der Start weist außerdem jedes
`worker-count * max-transactions` oberhalb von 65536 vor der Allokation eines
Peer-Caches ab. Ein ungültiges Limit ist ein sichtbarer Konfigurationsfehler
mit Exit `2`, kein impliziter Open-Mode-Fallback. Der kompilierte
SPOP-Ressourcenlimit-Contract deckt exakte und überhöhte
Header-/Anzahl-/Cache-Kontrollen ab.

Der Default `worker-count=8` und das endliche 64-Worker-Maximum begrenzen
gleichzeitige Peer-Prozesse, Cache-Slots und native Engine-Initialisierungen,
sind aber keine Deployment-Speicherreservierung. Wiederholte Pre-HELLO-
Verbindungen können weiterhin den begrenzten Worker-Pool belegen, während
jeder Worker seine Engine initialisiert; Live-Load-Charakterisierung und ein
früheres Protokoll-Admission-Budget bleiben dokumentierte Restrisiken.

Das Default-Profil `response-companion=none` weist jede
Response-Phasen-Aktivierung (`response-body-limit > 0`,
`enable-response-headers` oder `response-phases`) mit Exit `2` ab, bevor es
einen Produktions-Listener oder Worker erzeugt. Das ist fail-closed-
Konfigurationsablehnung, kein partielles Response-Enforcement; ein gültiger
request-side-only-Start ist die legitime Folgekontrolle. Das Profil
`response-companion=native-htx` ist die begrenzte Ownership-erhaltende
P3/P4-Brücke: Es erlaubt Response-Phasen nur, nachdem seine private Socket-,
Identitäts- und Body-Limit-Validierung erfolgreich war.

Der aktuelle direkte Protokolllauf startet request-only mit
`max-transactions=1`. Ein Response-NOTIFY des Peers wird vor der
Transaktions-Cache-Verarbeitung abgewiesen und ergab
`deny`/`503`/`response_phase_disabled_closed`; ein echter Rule-Block blieb
`403`, frisches Allow blieb `200`. Die ältere Cache-Eviction-Fixture bleibt
Source-Evidence für den getrennten fail-closed-Pfad
`stateful_response_transaction_missing_closed`, ist aber kein aktueller
Produktions-Startmodus. Das ist Evidence des Produktionsagenten, keine
Behauptung zum nativen HAProxy-Clientstatus oder FD-Audit.

`connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh` reproduziert
dieselbe request-only Response-Guard-Sequenz gegen einen aktuellen Agenten,
wenn Build- und Runtime-Root explizit task-eigen sind. Der Harness prüft
Response-Guard `503`, echten Block `403` und frisches Allow `200` und beendet
den Agenten anschließend im Cleanup-Pfad.

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

Die aktuellen Follow-up-Testfixtures prüfen nach Rückkehr eines Idle-Handlers
`pendingReceives == 0` und belegen sowohl Cancel-Cleanup als auch einen gültigen
Folgestream. Der getaggte Common-Runtime-Test hält den nativen Mutex und
belegt, dass jede wartende Operation mit ihrer Engine-Context-Deadline
zurückkehrt, ohne nativen Code zu betreten; der Service ordnet dies gRPC
`DeadlineExceeded` zu, zeichnet `processor_error` auf, emittiert keine
Allow-Antwort, gibt die Zulassung frei und erlaubt einen gültigen Folgestream.
Mutex- und Forced-Stop-Wartezeiten sind durch Deadlines begrenzt. Ein bereits
laufender, nicht unterbrechbarer nativer CGo-Aufruf oder Destruktor bleibt ein
kontrollierter Nonzero-Restart, nicht als in-process abbrechbar behauptet.

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: Service-Konfiguration/Startup weist ungültige Engine ab |
| V2 | E | SELF_TEST_PASS: Enginefehler liefert gRPC-Fehler, kein Allow |
| V3 | E | SELF_TEST_PASS: getaggtes `TestCommonRuntimeEngineOperationsHonorMutexContext` begrenzt wartende native-Mutex-Operationen; `TestProcessMapsEngineTimeoutToDeadlineExceededAndAllowsFollowUp` liefert gRPC `DeadlineExceeded`, zeichnet `processor_error` auf, gibt Zulassung frei und nimmt einen gültigen Folgestream an. Getrennt von Stream-Idle. |
| V4 | I | SOURCE_VALIDATED: ungültige Processing-Antwort schlägt Stream fehl |
| V5 | I | SOURCE_VALIDATED: unvollständige Processing-Nachricht schlägt Stream fehl |
| V6 | P | SELF_TEST_PASS: `TestCancellationCleansUpWithoutAttributingTheHTTPReset` schließt als `grpc_context_canceled_unattributed`; Cancel gibt Zustand frei und erfindet keine HTTP-Reset-Attribution |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | NOT_APPLICABLE: gRPC-Stream ohne HTTP-Agent-HELLO |
| V9 | P | SOURCE_VALIDATED: gRPC-Reset ist Streamfehler; Live-Reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: Request-Body-EOF ist unvollständiger Stream |
| V11 | P | SOURCE_VALIDATED: Response-Body-EOF ist unvollständiger Stream |
| V12 | C | SELF_TEST_PASS: `TestCommonRuntimeEngineCloseHonorsShutdownContext` begrenzt einen mutexgehaltenen Shutdown; `TestCommonRuntimeEngineCloseRejectsCanceledContextBeforeDestroy` belegt keinen nativen Destroy nach bereits abgebrochenem Shutdown-Context; `TestWaitForServerTerminationStopsOnFatalCleanupFailure` belegt, dass main den Listener stoppt und für unsicheres Cleanup kontrolliert mit Exit `1` zurückkehrt |
| V13 | C | SELF_TEST_PASS: `TestGRPCServerStopCancelsIdleStreamAndReleasesAdmission` belegt Cleanup bei Connector-/Agent-Terminierung; `TestCleanupFailureTriggersControlledRestartAndRejectsFollowUp` belegt, dass unsicheres natives Cleanup main benachrichtigt, Admission freigibt, eine Folgeanfrage mit `Unavailable` abweist und den begrenzten kontrollierten Exit `1` ohne paralleles Native-Free nutzt |
| V14 | L | SELF_TEST_PASS: `go test -race ./...`; parallele Streams sind begrenzt und Cancel gibt den Zulassungsslot frei |
| V15 | L | SOURCE_VALIDATED: `max_concurrent_streams <= 1024`, Überbelegung `ResourceExhausted` |
| V16 | A | SELF_TEST_PASS: `TestProcessMapsEngineTimeoutToDeadlineExceededAndAllowsFollowUp` und Idle-Timeout-Kontrollen belegen einen gültigen Stream nach Timeout-Cleanup |
| V17 | U | SELF_TEST_PASS: getaggte native Common-Runtime-Mutex- und Shutdown-Context-Tests belegen begrenztes Cleanup/keinen Destroy bei Cancel; Live-Envoy-FD-Audit NOT_EXECUTED |

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
| V3 | E | SELF_TEST_PASS: ein stiller UDS-Peer erreicht den konfigurierten Transaktions-Timeout, schließt nur diesen FD, macht die Transaktion terminal und eine neue Allow-Transaktion gelingt |
| V4 | I | SELF_TEST_PASS: ein valide geframtes, aber ungültiges RESULT-Opcode wird abgewiesen, verworfen und von einer frischen Allow-Transaktion gefolgt |
| V5 | I | SELF_TEST_PASS: ein abgeschnittenes RESULT-Frame wird abgewiesen, verworfen und von einer frischen Allow-Transaktion gefolgt |
| V6 | P | SELF_TEST_PASS: Request-Context-Cancellation unterbricht blockierte UDS-Reads und -Writes, schließt nur diese Verbindung und eine frische Allow-Transaktion gelingt; es wird kein HTTP-Client-Reset attribuiert |
| V7 | P | NOT_EXECUTED: Live-Upstream-Close |
| V8 | P | SELF_TEST_PASS: unvollständiges Framing wird abgewiesen |
| V9 | P | SELF_TEST_PASS: UDS-Reset und RESULT-Writes von 64 nicht lesenden Peers beenden Service nicht |
| V10 | P | SOURCE_VALIDATED: unvollständiger Request-Frame wird abgewiesen |
| V11 | P | SELF_TEST_PASS: unvollständige/überlange Response wird abgewiesen |
| V12 | C | SOURCE_VALIDATED: aktive Sockets werden beim Service-Stop beendet |
| V13 | C | SOURCE_VALIDATED: festhängende Engine nutzt kontrollierten Neustart |
| V14 | L | SELF_TEST_PASS: 64 nicht lesende Peers füllen die Worker-Grenze; ein zusätzlicher Peer wird vor der Write-Deadline nicht bedient |
| V15 | L | SELF_TEST_PASS: Response- und Frame-Limits werden erzwungen |
| V16 | A | SELF_TEST_PASS: eine frische Allow-Transaktion gelingt nach Timeout, Cancel, ungültigem Result, unvollständigem Result, Reset und der 31,0-Sekunden-Deadline eines nicht lesenden Peers |
| V17 | U | SELF_TEST_PASS: Cancel-Read/-Write-, Timeout-, ungültiges/unvollständiges-Result-, Reset-, Write-Deadline- und Ownership-Replacement-Pfade hinterlassen keinen eigenen UDS oder Prozess; wiederholtes Close nach Cancel ist sicher |

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

Der Go-Native-UDS-Client besitzt einen getrennten Engine-Timeout pro Exchange
und einen Request-Context-Cancellation-Pfad. Er verwendet die frühere Deadline
am Socket, bricht ein blockiertes Read oder Write bei Cancellation ab, schließt
und verwirft die fehlerhafte Transaktionsverbindung und verwendet keinen
Teilframe wieder. Component-Tests belegen Timeout, Cancel-Read, Cancel-Write,
ungültiges/abgeschnittenes RESULT, idempotentes Close, Cleanup und frische
Allow-Folgeanfragen. Sie behaupten weder ein Live-Traefik-Client-Cancel-Ereignis,
einen rückwirkenden HTTP-Status nach Commit noch einen Host-FD-Audit.

### lighttpd Stock

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SELF_TEST_PASS: aktueller Stock-Host startete und zeichnete das ABI-korrekte Connector-Event `native-lighttpd-plugin` auf |
| V2 | E | NOT_EXECUTED: Engine-Fehler während Transaktion |
| V3 | E | NOT_EXECUTED: Live-Timeout |
| V4 | I | NOT_EXECUTED: ungültiges Engine-Ergebnis |
| V5 | I | NOT_EXECUTED: unvollständiges Engine-Ergebnis |
| V6 | P | SELF_TEST_PASS (nur begrenzter Fallback): Direkte Client-Cancel-Propagation und ein Stock-Connector-Event wurden nicht beobachtet oder behauptet; ein konfiguriertes 2-Sekunden-Gateway-/Proxy-Backend-Read-Timeout begrenzte die Anfrage, loggte `read timeout on socket`, und ein Same-Host-Follow-up mit `200` gelang |
| V7 | P | SELF_TEST_PASS: Eine rohe abgeschnittene Upstream-Response wurde geschlossen und der begrenzte Harness beendete sein Cleanup; dies ist Host-/Transport-Evidence, keine Behauptung eines typisierten Stock-Connector-Events |
| V8 | P | NOT_APPLICABLE: kein Agent-Handshake |
| V9 | P | NOT_EXECUTED: Live-Reset |
| V10 | I | NOT_EXECUTED: vorzeitiges Request-Body-Ende |
| V11 | P | SELF_TEST_PASS: Eine rohe abgeschnittene Upstream-Response wurde geschlossen und der begrenzte Harness beendete sein Cleanup; dies ist Host-/Transport-Evidence, keine Behauptung eines typisierten Stock-Connector-Events |
| V12 | C | NOT_EXECUTED: Abnahme eines Live-Stock-Shutdowns |
| V13 | C | NOT_EXECUTED: Abnahme einer Live-Modul-Terminierung |
| V14 | L | NOT_EXECUTED: Parallelitätsabnahme; ein separater begrenzter Lauf mit acht HTTP/1.1-Anfragen bestand, füllt diesen Vektor aber nicht |
| V15 | L | NOT_EXECUTED: Abnahme maximaler Größen-/Ressourcenlimits |
| V16 | A | SELF_TEST_PASS: Same-Host-Follow-up nach den begrenzten Fehlerpfaden lieferte `200`, und der Identity-Control blieb `200 -> 403 -> 200` |
| V17 | U | SELF_TEST_PASS: PIDFD-/Session-/Port-/UDS-Cleanup-Receipts bestanden für den ersten und den Ersatz-Host; dies hebt die nicht ausgeführten V12--V15-Vektoren nicht hoch |

Der rohe Stock-Event-Identifier wird an derselben Compile-Time-ABI-Grenze wie
die Streaming-Hooks ausgewählt: ungepatchte Header erzeugen
`native-lighttpd-plugin`; die Patched-Streaming-Hook-ABI erzeugt
`patched-native-lighttpd`. Der fokussierte Identity-Run validiert nur
Provenienz, P1-Allow-/Block-/Follow-up-Verhalten sowie PID-/Listener-Cleanup;
er füllt nicht die verbleibenden Stock-Body-, Timeout-, Peer-, Shutdown- oder
Parallelitätsvektoren.
Ein aktueller begrenzter Lifecycle-Lauf unter
`lighttpd-stock-lifecycle-v6-v10-20260825T100000Z` übte Stock- und Ersatz-Host
aus. Für V6 beobachtete die Client-Close-Probe weder direkte
Client-Cancel-Propagation noch ein typisiertes Connector-Event; das
2-Sekunden-Gateway-/Proxy-Backend-Read-Timeout war der ausdrücklich begrenzte
Containment-Fallback, erzeugte den Host-Marker `read timeout on socket` und
wurde von einem Same-Host-Control mit `200` gefolgt. Das rohe V7/V11-
Upstream-Truncation-Fixture wurde abgeschlossen, acht begrenzte parallele
HTTP/1.1-Anfragen lieferten `200`, und die Host-Terminierung erzeugte
Client-EOF, gefolgt von Restart-Controls `200 -> 403 -> 200`. Dies sind
begrenzte Host-/Transport-Beobachtungen; sie heben V12--V15 oder die vollständige
17-Vektor-Abnahme nicht hoch. Die PIDFD-/Session-/Port-/UDS-Receipts bestanden
für den ersten und den Ersatz-Host. Die älteren fünfsekündigen Timeout-Receipts
bleiben als historische FND-PARENT-0311-Evidence erhalten und werden nicht
still umgeschrieben.

### lighttpd Patched

| V | Klasse | Lokaler Nachweis |
|---|---|---|
| V1 | E | SELF_TEST_PASS: Patched-Host-Smoke startete, lieferte Baseline `200` und zeichnete Connector-Event auf |
| V2 | E | NOT_EXECUTED: Engine-Fehler während Transaktion |
| V3 | E | NOT_EXECUTED: Live-Timeout |
| V4 | I | NOT_EXECUTED: ungültiges Engine-Ergebnis |
| V5 | I | NOT_EXECUTED: unvollständiges Engine-Ergebnis |
| V6 | P | SELF_TEST_PASS: 27/64 benigne und P2-Marker-TCP-RST-Fälle lassen den Host am Leben und ein frisches Follow-up liefert `200` |
| V7 | P | NOT_EXECUTED: kontrollierter Upstream-Receipt zeichnete 5/64 Byte und danach fünfsekündigen Frontend-Timeout auf, nicht EOF/definierten Fehler oder unmittelbares Cleanup vor Host-Stop; FND-PARENT-0311 |
| V8 | P | NOT_APPLICABLE: kein Agent-Handshake |
| V9 | P | SELF_TEST_PASS: TCP-RST während Request-Verarbeitung bleibt enthalten; normale und ASan/UBSan-Hosts haben keinen Abort/keine Sanitizer-Diagnostik |
| V10 | I | SELF_TEST_PASS: vorzeitiger Request-Body-TCP-RST erzeugt keinen synthetischen P2-Abbruch; unabhängiges Follow-up liefert `200` |
| V11 | P | NOT_EXECUTED: partieller Response-Receipt belegt nicht, dass der Frontend-Stream vor Host-Stop abschloss oder transaktionslokalen Zustand freigab; FND-PARENT-0311 |
| V12 | C | NOT_EXECUTED: Live-Host-Terminierung |
| V13 | C | NOT_EXECUTED: Live-Modul-Terminierung |
| V14 | L | NOT_EXECUTED: paralleler Host-Run |
| V15 | L | SELF_TEST_PASS: Request-Body mit 33/64 Byte überschreitet das konfigurierte 32-Byte-Limit und liefert `413`; 32 Byte bleibt `200` |
| V16 | A | SELF_TEST_PASS: Baseline-/32-Byte-Allow `200`, gewöhnlicher P2-Marker `403`, gleichlautende gewöhnliche `403`/`451` und Follow-up-Controls bestehen; V7/V11-Post-Fault-Control bleibt NOT_EXECUTED |
| V17 | U | SELF_TEST_PASS: normale und ASan/UBSan-Runs behalten Event-Evidence und entfernen PID/Listener nach RST-, Erfolgs- und Limit-Pfaden; V7/V11-unmittelbares Cleanup bleibt NOT_EXECUTED |

Der Resume-Callback des gepatchten Hosts erhöht `resp_fn_step` um
`sizeof(*plfd)` und entspricht damit dem Record-Pointer-Stride. Die Common
Runtime mappt nur eine roh disruptive Request-Body-Intervention mit
ursprünglichem `403`, keinem Redirect und exaktem Engine-Log
`Request body limit is marked to reject the request` auf `413`; gewöhnliche
`403`- und `451`-Rules behalten ihren Status. Dieser Nachweis ist Evidence des
aktuellen gepatchten-lighttpd-Hosts, keine vollständige
Cross-Connector-Common-Runtime-Consumer-Matrix.

Das schmale Patched-V7/V11-Fixture bewahrte in seinem JSONL nur ein
nachfolgendes legitimes Block-Event auf. Es beobachtete vor dem kontrollierten
Host-Stop weder Frontend-EOF/definierten Fehler noch ein separates Connector-
`peer_error`-Event oder unmittelbares Stream-/FD-/Transaktions-Cleanup. Seine
partielle Response, späteren Controls und Post-Stop-Cleanup sind keine V7/V11-
Hochstufungs-Evidence; FND-PARENT-0311 verfolgt den erforderlichen rohen
Upstream-/Frontend-Closure-Harness.

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
