# Gemeinsamer Transaktions- und Phasenvertrag

**Sprache:** [English](transaction-phase-contract.md) | Deutsch

Status: aktueller Common-Vertrag; quellengestützte Adaptergrenze

Architekturbegründung: [ADR-003](../../docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.de.md)

## Autorität und abgeleitete P1–P4-Bedeutung

Dieser Vertrag konsolidiert die bestehenden neutralen Phasen in
<code>common/include/msconnector/phase.h</code>, dem Common-Engine-Wrapper,
der Common Runtime, nativen Adapter-Hooks, Tests und dem Architekturleitfaden.
Er führt keine neue Rule-Engine-Phase ein.

| Fachphase | Bestehende Bedeutung | Abschlusszeitpunkt |
| --- | --- | --- |
| P1 | Request-Header nach den Voraussetzungen Connection und URI sowie vor dem Request-Commit. | Genau eine Request-Header-Entscheidung. |
| P2 | Aufnahme des Request-Body. | Genau eine Request-End-of-Stream-Entscheidung. |
| P3 | Response-Header vor dem Response-Commit, während der ursprüngliche Status veränderbar bleibt. | Genau eine Response-Header-Entscheidung. |
| P4 | Begrenzte Aufnahme des Response-Body. | Genau eine Response-End-of-Stream-Entscheidung. |

Connection, URI und Logging bleiben native Voraussetzungen oder Epilogoperationen
des Lebenszyklus und keine fünfte Fachphase. P2/P4 empfangen null oder viele
Chunks, besitzen jedoch jeweils genau eine EOS-Finalisierung.

Eine disruptive URI-Voraussetzung kann die Transaktion terminieren, bevor P1
begonnen hat. Der Adapter zeichnet die begrenzte regelkorrelierte terminale
Entscheidung auf, ohne einen P1-Beginn/-Abschluss zu erfinden; sein
Adapter-Event muss diese Pre-P1-Herkunft explizit kennzeichnen. Eine folgende
Request-Header-Entscheidung ist nur dann P1, wenn P1 tatsächlich begonnen und
abgeschlossen wurde.

## Kanonischer begrenzter Zustand und FSM

<code>msconnector_transaction_contract</code> ist der kanonische Metadaten-only-
Datensatz. Er enthält eine begrenzte Transaktions-ID, Connector-ID,
Host-/Hostinstanz-ID, aktuelle/letzte Phase, Request- und Response-Metadaten,
Bodyzähler und -limits, Engineentscheidung, Regel-ID, Hostaktion, Safe-/Strict-
Modus, Fehlerklasse, Zeitstempel, Response-Commit-Status und Cleanupstatus. Er
enthält weder Bodyzeiger noch Payload; Chunks werden nur für ihren Callback
geborgt.

Der Common-Vertrag behält keinen Zeitstempel null als Lifecycle-Wert. Wenn ein
Adapter für einen Übergang keinen Uhrwert besitzt, setzt der Vertrag einen
nichtnull lokalen Wert und begrenzt ihn auf mindestens den zuletzt
gespeicherten Lifecycle-Zeitstempel. Damit bleiben Receipt-Zeitstempel
nichtfallend, ohne einen expliziten Adapterzeitstempel umzudeuten oder eine
Uhrensynchronisierung zwischen verschiedenen Hosts zu behaupten.

Der Vertrag hält zwei bewusst getrennte begrenzte Identitäten. Seine
<code>transaction_id</code> ist der byte-identische, validierte
Host-/Request-Korrelationsschlüssel für MRC1 und Response-Companions. Seine
<code>canonical_transaction_id</code> wird einmal je Common-Prozess als
<code>txc-&lt;monotonic-time&gt;-&lt;atomic-sequence&gt;</code> erzeugt und ist für die
Vertrags-Ownership eindeutig, auch wenn ein Host dieselbe externe Request-ID
wiederverwendet. Ein Überlauf der atomaren Sequenz lässt die
Transaktionserzeugung fehlschlagen, statt auf eine verlustbehaftete oder
gemeinsam genutzte ID zurückzufallen. Keine der beiden IDs überschreitet die
Response-Observer-Grenze.

Die Admission schlägt fail-closed fehl. Eine übergebene Transaktions-ID, die
sich nicht als begrenzte kanonische ID kopieren lässt (beispielsweise leere,
Control-Byte-, umgebende-Whitespace- oder zu lange Eingabe), allokiert keine
native Engine-Transaktion und hinterlässt keinen nutzbaren Legacy-Phasenzustand.
Der Legacy-Kompatibilitätseingabewert `NULL` ist absichtlich davon getrennt: Er
erzeugt die interne begrenzte Vertrags-ID `common-transaction`, ohne eine
ungültig übergebene ID zu normalisieren. Nach fehlgeschlagener Admission lehnen
Legacy-Phasen-, Buchhaltungs-, Metadaten-, Entscheidungs- und Cleanup-Aufrufe
ab, statt einen Null-Datensatz als Transaktion zu behandeln.

Die Routen-ID eines Adapterprofils (zum Beispiel <code>ext_authz</code>) wählt
die Implementierung; sie ist nicht die Host-ID der Transaktion. Die Common
Runtime leitet Letztere aus dem vertrauenswürdigen gemappten Serverendpunkt als
<code>&lt;route&gt;@&lt;server-address&gt;:&lt;port&gt;</code> ab und fällt nur dann auf die
stabile Routen-ID zurück, wenn der Host keinen Endpunkt liefert. Transaktions-
und Host-ID bleiben interne Metadaten. Ein requestorientierter Service gibt
nur <code>x-msconnector-response-handle</code> zurück: eine servergenerierte
zufällige 32-Byte-Capability als 64 klein geschriebene Hex-Zeichen. Sie wird
nicht aus <code>x-request-id</code> abgeleitet; weder Transaktions- noch Host-
ID überschreiten die Response-Observer-Grenze.

Die explizite FSM erlaubt nur P1 -> P2 -> P3 -> P4. P2/P4 bleiben vom ersten
Chunk bis EOS aktiv. Sie verwirft doppelte, übersprungene, verspätete,
konfligierende, terminale und bereinigte Phasen. Cancel, Timeout,
Body-/Header-/Eventlimit und Connector-/Protokollfehler werden zu terminalen
Entscheidungen. Frühes Cleanup zeichnet zuerst einen terminalen
<code>connector_error</code> mit <code>cleanup_incomplete</code> auf und
markiert die Transaktion anschließend als bereinigt; es wird niemals still
akzeptiert.

Für P2/P4 ist ein erfolgreicher Body-Append die Aufnahme in die bereits aktive
Phase, kein neuer Phasenstart: spätere begrenzte Chunks setzen diese Phase fort,
und nur die zugehörige Finish-Operation erzeugt EOS. Ein Adapter borgt einen
Chunk nur für den Common-Aufruf. Wo sein Host Body-Daten weiterleiten kann,
leitet er den begrenzten Chunk nach erfolgreichem Append sofort weiter; weder
Common noch Adapter halten einen callbackübergreifenden vollständigen Body.
Der erste erfolgreiche Next-Stage-Write oder Host-Commit ist die monotone
P4-Commit-Grenze. Ein EOS-only-Ergebnis nach dieser Grenze ist spät: Safe
zeichnet <code>log_only</code> auf; ein zugelassenes Strict-Profil darf einen
tatsächlichen, hostbewiesenen Abort verwenden, aber keinen Ersatz-HTTP-Status
erfinden.

Runtime-gestützte Adapter verwenden vor der Bedienung von Traffic ein
explizites Strict-Zulassungsgate. Eine Runtime mit
<code>phase4_mode=strict</code> lehnt ein ausgewähltes Profil ab, dessen
unveränderliche Capability <code>strict_post_commit_action</code> null ist.
Dies ist ein Konfigurationsfehler beim Start und kein später
<code>log_only</code>-Fallback. Die Capability wird nur für eine
quellenbelegte Hostaktion gesetzt; ein direkter Adapter ohne Common Runtime
muss dieselbe Bedingung an seiner eigenen Startgrenze erzwingen.

Headeraggregate sind auf 256 Felder und 65536 Bytes begrenzt. Bodylimits müssen
ungleich null sein. Die Response-Companion-Registry besitzt 64 feste Slots und
eine monotone TTL (30 Sekunden bei den bereitgestellten requestorientierten
Adaptern). Sie erzeugt beim Handoff ein zufälliges opaques Handle, erlaubt
atomar genau einen Claim und entfernt den Eintrag bei Ablauf, Cancel, Release
oder Shutdown. Ein fehlendes, abgelaufenes, fehlerhaftes oder wiederverwendetes
Handle liefert dem Peer denselben begrenzten Korrelationsfehler; die
Implementierung verrät nicht, welche Bedingung zutraf. Event-JSONL bleibt
metadaten-only und hat ein separates 16384-Byte-Limit.

Eine exakte P2-Bodylimit-Ablehnung ist ein kanonisches Deny ohne Regel-ID: Sie
verwendet HTTP 413, erzeugt die begrenzte
<code>MSCONN_EVENT_BODY_LIMIT</code>-Eventidentität, trägt keinen Redirect und
terminalisiert die Transaktion. Die Hostaktion muss dieselbe
HTTP-413-Ablehnung sein; eine Regelkorrelation aus einer früheren Phase darf
nicht geerbt werden.

Ein Live-Handoff zeichnet <code>handed_off</code> auf, bis der vertrauenswürdige
Observer die Transaktion atomar für P3 claimt; erst dann dürfen companion-only
P3/P4 die FSM fortschreiben. Registry-Sperren schützen nur kurze
Ownershipwechsel, keine nativen Engine-Aufrufe. Die Common Runtime serialisiert
ihren gemeinsamen nativen Engine- und Integrity-Chain-Eventzustand unabhängig.
Bei Ablauf, Cancel, Freigabe oder Shutdown wird der Eintrag vor dem nativen
Cleanup abgetrennt; Shutdown verweigert das Freigeben eines gerade verwendeten
Eintrags, daher muss der Observer zuvor quiescen. Das private
<code>MRC1</code>-UDS-Protokoll verwendet einen festen 12-Byte-Frame-Header,
begrenzte Frames, zwingendes erstes <code>CLAIM</code>, P3-Header, monotonen
Commit, begrenzte P4-Chunks, genau ein EOS sowie Outcome und Release/Cancel.
Nur beim CLAIM transportiert es das opaque Handle.
Sein generisches Payloadmaximum bleibt 65536 Byte. Nur
<code>RESPONSE_HEADERS</code> darf einen Payload von bis zu 66630 Byte verwenden,
damit die festen MRC1-Felder und bis zu 256 Feldlängenpräfixe Commons
logisches 65536-Byte-Namens-/Wertaggregat transportieren können. Das erhöht
das logische Headerlimit nicht: Decoder weisen weiterhin mehr als 256 Felder
oder mehr als 65536 aggregierte Namens-/Wertbytes zurück, und jeder andere
Opcode bleibt auf 65536 Payloadbytes begrenzt.
Die MRC1-Familie erfordert derzeit Protokollversion 2. Ihr ein Byte großer
<code>CANCEL</code>-Payload ist eine kanonische terminale Ursache:
<code>0=client_cancel</code>, <code>1=upstream_disconnect</code>,
<code>2=connector_error</code>, <code>3=protocol_error</code>,
<code>4=engine_timeout</code>, <code>5=engine_unavailable</code> und
<code>6=invalid_engine_response</code>. Die Werte 0 und 1 behalten ihre
Lifecycle-Bedeutung; die Werte 2--6 rufen den Common-Fehlerpfad mit genau
dieser Fehlerklasse auf. Ein Versionskonflikt zwischen Observer und Listener,
eine unbekannte Ursache oder ein Observer ohne v2-Unterstützung schlägt fail
closed fehl: Es gibt keinen v1- oder Capability-Fallback. Ein unerwartetes EOF
des privaten Sockets ist ein Connector-Fehler und wird niemals als
Upstream-Disconnect geraten; ein tatsächlicher Upstream-Disconnect muss vor
dem Schließen explizit als Ursache 1 gesendet werden.
Ein MRC1-Ergebnis transportiert den kanonischen HTTP-Status der Entscheidung,
nicht einen Acknowledgement-Status: Erfolgreiche <code>allow</code>,
<code>log_only</code>, <code>drop</code> und <code>connection_abort</code>
dürfen daher <code>0</code> tragen, wenn keine HTTP-Antwort existiert. Ein
Empfänger muss genau diese statuslosen Erfolgsfälle bei einer
entscheidungsführenden Operation akzeptieren und eine statuslose erfolgreiche
<code>deny</code>-, <code>redirect</code>-, <code>error</code>- oder
<code>unsupported</code>-Entscheidung ablehnen. Die einzige
Protokollausnahme ist das erfolgreiche ACK von <code>CANCEL</code> oder
<code>RELEASE</code>: Es besitzt keine Engineentscheidung und verwendet daher
den statuslosen <code>error</code>-Sentinel. Ein Adapter darf diesen Sentinel
nur bei diesen beiden Cleanup-Operationen akzeptieren, niemals bei P1--P4.
Von null verschiedene MRC1-Statuswerte sind kanonische HTTP-Statuswerte von
<code>100</code> bis <code>599</code>, niemals ein Acknowledgement-Code oder
ein beliebiger dreistelliger Wert.
Der Common-Listener verlangt einen absoluten kanonischen owner-only-Parent,
erstellt einen 0600-
Socket, speichert dessen exakte Inode für Cleanup und prüft unter Linux für
jeden Peer <code>SO_PEERCRED</code>; Plattformen ohne diese Identitätsprüfung
schlagen fehl, statt auf TCP oder bloße Mode-Bits zurückzufallen.

Ein erfolgreicher MRC1-Handoff erfordert außerdem, dass dieser private Listener
im Moment des Ownership-Übergangs lebt.
<code>msconnector_response_companion_transport_ensure_running</code> ist die
gemeinsame Vorbedingung: Nach einem terminalen <code>poll</code>- oder
<code>accept4</code>-Exit joint und bereinigt sie den vorherigen Listener,
bevor sie einen frischen privaten Socket startet. Envoy ext_authz und Traefik
forwardAuth dürfen ein gecachtes Ready-Flag nicht als Nachweis behandeln, und
der direkte HAProxy-SPOE/SPOP-Handoff verwendet dieselbe Vorbedingung vor der
Backend-Admission. Unvollständiger Cleanup oder fehlgeschlagener Neustart ist
ein fehlgeschlossener Connector-Fehler: Es wird kein opakes Handle ausgegeben,
keine Transaktion übergeben und kein Transport-, Versions- oder Capability-
Fallback erlaubt.

## Einheitliche Entscheidungen

| Entscheidung | Hostaktion | Eventtyp | Regel-ID | Fehlerrichtlinie | Cleanup |
| --- | --- | --- | --- | --- | --- |
| Allow | allow | <code>allow</code> | keine | keine | normaler Abschluss |
| Block | deny | <code>rule_block</code> | erforderlich | fail closed | terminal, dann Cleanup |
| Redirect | redirect | <code>rule_redirect</code> | erforderlich | fail closed | terminal, dann Cleanup |
| Rate limit | rate-limit | <code>rule_rate_limit</code> | erforderlich | fail closed | terminal, dann Cleanup |
| Log-only / Safe | log-only | <code>log_only</code> | optional | fail open | normaler oder terminaler Cleanup |
| Enforce / Strict | Runtime-gestützter Adapter: Start ohne bewiesene Post-Commit-Hostaktion ablehnen; andernfalls vor Commit deny und nur die bewiesene Post-Commit-Aktion verwenden | <code>enforce</code>; die Startablehnung hat kein Transaktions-Event | erforderlich | fail closed | terminal, dann Cleanup |
| Engine timeout oder unavailable | deny in Strict vor Commit, sonst log-only | <code>engine_timeout</code> / <code>engine_unavailable</code> | keine | abhängig von Modus/Commit | terminal, dann Cleanup |
| Invalid engine response | deny in Strict vor Commit, sonst log-only | <code>invalid_engine_response</code> | keine | abhängig von Modus/Commit | terminal, dann Cleanup |
| Body- oder Ressourcenlimit | konfigurierte begrenzte Ablehnung vor unsicherem Forwarding (bei Bodylimit normalerweise HTTP 413) | <code>body_limit</code> | keine | fail closed | terminal, dann Cleanup |
| Connector/protocol/Frühcleanupfehler | deny in Strict vor Commit, sonst log-only | <code>connector_error</code> / <code>protocol_error</code> | keine | abhängig von Modus/Commit | terminal, dann Cleanup |
| Client cancel / upstream disconnect | betroffene Verbindung oder Stream abbrechen | <code>client_cancel</code> / <code>upstream_disconnect</code> | keine | stop I/O | terminal, dann Cleanup |

Eine disruptive Regelentscheidung ohne begrenzte Regel-ID wird zu
<code>invalid_engine_response</code>, niemals zu Allow. Ein Host nach Commit
darf keinen neuen Status erfinden oder Safe still zu Enforcement hochstufen.

## Normalisierung nativer Interventionen

Wenn ein nativer Adapter eine disruptive <code>msc_intervention</code> erhält,
normalisiert er den Status vor dem Aufzeichnen der Common-Entscheidung und vor
dem Aufruf des Host-Sinks. Dies kanonisiert eine native Regelentscheidung; es
ist vom <code>invalid_engine_response</code>-Fehlerpfad für einen Engine-,
Connector- oder Protokollfehler getrennt.

| Form der nativen Intervention | Kanonischer Status |
| --- | --- |
| Nichtleere Redirect-URL und ein 3xx-Status | Diesen 3xx-Status beibehalten. |
| Nichtleere Redirect-URL und jeder Nicht-3xx-Status | HTTP 302. |
| Keine Redirect-URL und ein erlaubter Blockstatus | Diesen Blockstatus beibehalten. |
| Keine Redirect-URL und jeder andere Status | Der konfigurierte erlaubte <code>default_block_status</code>, andernfalls HTTP 403. |

Adapter validieren weiterhin jede Engine-bereitgestellte Redirect-URL und
kopieren sie in Request-Ownership vor dem nativen Cleanup. Sie dürfen eine
leere URL nicht als Redirect ausgeben, für eine reine Statusintervention keinen
erfolgreichen oder beliebigen 3xx-Status zurückgeben und nach dieser
Kanonisierung die normale Safe-/Strict- und Response-Commit-Policy nicht
umgehen.

## Zehn logische Connectorlösungen

| Lösung | P1/P2-Pfad | P3/P4-Pfad | Aktuelle Grenze |
| --- | --- | --- | --- |
| Apache | natives Modul | native Filter | Direkter Vertrag; jeder begrenzte Response-Daten-Bucket vor EOS wird genau einmal angehängt und sofort an den nächsten Filter weitergereicht. Das terminale EOS-Fragment schließt P4 genau einmal ab; ein späteres Ergebnis folgt der gemeinsamen Post-Commit-Policy. |
| NGINX | native Access-/Body-Callbacks | native Header-/Body-Filter | Direkter Vertrag; dateibasierte Request-Bodies tragen ihren tatsächlichen File-Offset zu P2s begrenztem Zähler bei. File-only-P4-Buffer werden in genau einen wiederverwendeten 32-KiB-Scratch-Bereich gelesen und genau einmal angehängt; fehlerhafte oder kurze Dateilesungen schlagen vor dem Forwarding fail-closed fehl. |
| HAProxy HTX | HTX-Filter | HTX-Filter | Direktes Profil <code>haproxy-htx</code> / <code>htx-filter</code>. |
| HAProxy SPOE/SPOP | SPOP-Notifications | verpflichtende native-HTX-Response-Begleitkomponente | Das Common-Profil <code>haproxy-spoe-spop</code> / <code>spoe-spop-agent</code> routet P1/P2 direkt und P3/P4 über die Begleitkomponente. Rohe SPOP-Notifications, auch optionale Response-Header, sind keine Response-DATA/EOS-Grenze; native-HTX wird nur über ein explizites Fail-Closed-Gate für Private-UDS, Peer-Identity und Body-Limit ausgewählt und besitzt Current-Source-lokale Harness-Evidenz. |
| Envoy ext_authz | Authorization-Service | verpflichtender MRC1-Response-Companion | Dieselbe lebende Common-/native Transaktion bleibt hinter einem opaque Single-Claim-Handle; der Envoy-Response-Observer liefert P3/P4. |
| Envoy ext_proc | ext_proc-CGo-Common-Bridge | ext_proc-CGo-Common-Bridge | Direktes Streamingprofil <code>envoy-ext-proc</code> / <code>ext_proc</code>. |
| Traefik forwardAuth | Authorization-Service | verpflichtender MRC1-Response-Companion | Dasselbe Modell aus lebender Transaktion, fester Kapazität sowie TTL-begrenztem opaque-Handle-P3/P4 wie ext_authz; die Response-Observer-Middleware liefert P3/P4. |
| Traefik Native UDS | native Middleware | native Middleware | Direktes Profil <code>traefik-native-uds</code> / <code>native-traefik-middleware</code>. |
| lighttpd Stock | traffic-owning Common-Runtime-Sidecar | dasselbe Sidecar | Kanonisches Profil `lighttpd-stock` / `stock-lighttpd-sidecar`: Ein privates Loopback-HTTP/1.1-Sidecar besitzt den vollständigen Austausch, leitet jeden begrenzten P4-Chunk nach dem Append sofort weiter und schließt P4 einmal bei EOS ab. Die native Route `stock-lighttpd` ist eine ausdrücklich nichtkanonische P1/P3-Kompatibilitätsübersetzung und niemals ein Fallback. |
| lighttpd Patched | gepatchter Request-Range-Hook | gepatchter Response-Entity-Hook | Direktes Profil <code>lighttpd-patched</code> / <code>patched-native-lighttpd</code>. |

<code>ext_authz</code> und <code>forwardAuth</code> sind jeweils eine logische
Connectorlösung. Der Companion behält dieselbe native Regeltransaktion, keinen
rekonstruierten P1/P2-Snapshot, sodass P3/P4 mit demselben Request-Kontext
ausgewertet werden. Das Authorization-Response-Handle darf nur entlang der
lokalen Response-Observer-Kette weitergegeben werden. Bei Envoy ist dies sein
interner Upstream-Header-Pfad zum unmittelbar folgenden Observer, der den
Header vor dem tatsächlichen Anwendungs-Upstream entfernt; Traefik behält ihn
innerhalb der lokalen Observer-Kette. Envoy verwendet den bereitgestellten
ext_proc-Response-Observer über privaten UDS. Traefik verwendet die
bereitgestellte lokale Response-Observer-Middleware nach forwardAuth. Beide
Observer senden P3 vor dem Host-Commit, P4/EOS danach,
zeichnen ein spätes Ergebnis nur als log-only auf und schließen/canceln bei
fehlerhaften Ergebnissen oder Cleanup-Fehlern. Eine Konfiguration ohne einen
dieser Observer hat keine P3/P4-Abdeckung und ist ein Konfigurationsfehler,
kein Grund, P3/P4 als not_applicable zu bezeichnen. Das bereitgestellte
Envoy-Harness verlangt Observer-Binary und owner-only Socket; der Live-Filter
schlägt fail-closed fehl, wenn der Observer einen Request nicht bedienen kann.

Der Source enthält den Common-MRC1-Listener sowie die Envoy-/Traefik-Observer-
Artefakte und Wiring-Templates. Dies ist Source-/Komponentennachweis, aber
kein Nachweis, dass eine bestimmte Envoy- oder Traefik-Deployment die Templates
geladen oder Live-Hostverkehr erzeugt hat. Betreiber müssen das private Parent-
Verzeichnis erstellen, den Handle-Header ausschließlich entlang der lokalen
Kette verdrahten, den Response-Observer vor dem requestorientierten
Authorization-Service starten und Observer sowie Companion vor Runtime-Shutdown
quiescen.

Die Envoy-Deployment-Konfiguration transportiert zusätzlich auf einer
terminalen ext_authz-P1/P2-Antwort den festen lokalen Marker
<code>x-msconnector-terminal-authz: 1</code>. Der Response-Observer lässt
einen reinen Response-Callback nur durch, wenn genau dieser Marker vorhanden
ist und zuvor keine Observer-Request-Phase gesehen wurde; er entfernt den
Marker vor dem Client. Ein fehlendes Handle allein schlägt immer fail-closed
fehl. Vor dem Response-Commit besitzt weder der bereitgestellte Envoy- noch
der Traefik-Response-Observer über seinen Hostadapter eine nachgewiesene
Stream-Reset-Primitive: Ein statusloses <code>drop</code> oder
<code>connection_abort</code> wird daher als tatsächlich ausgeführtes
fail-closed HTTP-Deny aufgezeichnet und als HTTP 503 zurückgegeben, niemals
als Reset behauptet oder still zu HTTP 200 umgewandelt. Nach dem Commit gilt
weiterhin die kanonische Safe-/log-only-Regel für späte Ergebnisse.

lighttpd Stock unterscheidet sich von diesen request-only Protokollen: Das
ausgewählte `stock-lighttpd-sidecar` ist der Traffic-Eigentümer. Es akzeptiert
nur ausdrücklich konfigurierte, wörtliche Loopback-Adressen (`127.0.0.1`) über
HTTP/1.1, hält einen begrenzten Worker-Austausch und leitet an das private,
unveränderte Stock-Backend weiter. Der Worker besitzt P1--P4 und Cleanup in
einem Prozess; deshalb sind keine prozessübergreifende Korrelation und kein
TTL-Registry nötig. Die native Stock-Modulroute bleibt eine ausdrücklich
nichtkanonische P1/P3-Kompatibilitätsübersetzung und darf weder stillschweigend
neben dem Sidecar aktiviert noch durch es ersetzt werden. Das Sidecar-Event-
JSONL enthält nur begrenzte Metadaten und Zähler; Request- oder Response-Body-
Payloads gelangen niemals in Events.

## P4-Implementierungs- und Evidenzmatrix

Diese Matrix dokumentiert die zehn logischen Lösungen, nicht ein
Ersatz-Hostprofil. <code>implemented</code> bedeutet, dass der gemeinsame
Vertrag in der ausgewählten Source-/Adaptergrenze vorhanden ist;
<code>verified</code> bedeutet, dass dieser Task den genannten begrenzten
Komponententest tatsächlich ausgeführt hat; <code>pending</code> bedeutet,
dass direkte Host-/Runtime-Evidence noch erforderlich ist. Sie promoted keine
Source-Evidence zu einer Production-Behauptung.

| Logische Lösung | P4-Status | Aktuelle Evidenz und Grenze |
| --- | --- | --- |
| Apache | implemented | Progressives Pre-EOS-Filter-Forwarding und ein EOS-Finish sind quellenverkabelt und vom fokussierten Wiring-Test erfasst; ein aktueller nativer Apache-Hostlauf wird nicht behauptet. |
| NGINX | implemented | Sein nativer Filter hängt NGINXs speichermaßgeblichen aktuellen Bereich oder begrenzte file-only Scratch-Chunks an, leitet die Chain ohne connector-eigenen vollständigen Response-Buffer weiter und beendet P4 am tatsächlichen EOS. Eine fehlerhafte oder kurze Dateilesung schlägt vor dem Forwarding fail-closed fehl; frische Native-Host-Runtime-Evidence steht aus. |
| HAProxy HTX | implemented | Das native HTX-Profil mappt aktuelle Body-Blöcke und HTTP-End-of-Message auf den gemeinsamen Vertrag; Strict-Post-Commit-Wire-Verhalten bleibt getrennte Host-Evidence. |
| HAProxy SPOE/SPOP | implemented | Die logische Lösung verlangt die verpflichtende private HTX-P3/P4-Begleitkomponente. Reines SPOP ist für Response-DATA/EOS unsupported und niemals ein P4-Fallback. |
| Envoy ext_authz | implemented | Die logische Lösung verlangt ihren Single-Claim-Response-Observer. Reines ext_authz ist für Upstream-Response-Phasen unsupported und wird niemals als not_applicable markiert. Seine Runtime lehnt Strict-Zulassung ab, bis eine Post-Commit-Hostaktion bewiesen ist. |
| Envoy ext_proc | implemented | Das gestreamte ext_proc-Profil mappt Response-Header, begrenzte Body-Chunks und EOS auf den gemeinsamen Vertrag. Seine Runtime lehnt Strict-Zulassung ab, bis eine Post-Commit-Hostaktion bewiesen ist. |
| Traefik forwardAuth | implemented | Die logische Lösung verlangt ihre Response-Observer-Middleware. Reines forwardAuth ist für Upstream-Response-Phasen unsupported und wird niemals als not_applicable markiert. Seine Runtime lehnt Strict-Zulassung ab, bis eine Post-Commit-Hostaktion bewiesen ist. |
| Traefik Native UDS | implemented | Das direkte native UDS-Profil besitzt P3/P4 und EOS unter dem gemeinsamen Vertrag. Seine Runtime lehnt Strict-Zulassung ab, bis eine Post-Commit-Hostaktion bewiesen ist. |
| lighttpd Stock | verified | Der tatsächliche 11-Test-Komponentenlauf des traffic-owning Private-Loopback-Sidecars deckt mehrteilige P2/P4, EOS, Safe-/Strict-Late-Verhalten, Limits, Cancel, Cleanup und Reuse ab; er ist kein unveränderter nativer Stock-Hostlauf. |
| lighttpd Patched | pending | Der gepatchte Identity-Entity-Source-/Buildpfad besitzt den gemeinsamen Hook-Vertrag, aber keine aktuelle ausgewählte Host-P4-Runtime-Evidence. Seine Runtime lehnt Strict-Zulassung ab, bis eine Post-Commit-Hostaktion bewiesen ist. |

Die rohen response-blinden Protokollgrenzen (SPOP, reines ext_authz und reines
forwardAuth) sind für P4 <code>unsupported</code>, nicht
<code>not_applicable</code>. Ihre verpflichtenden Begleitkomponenten machen
die aufgeführte logische Connectorlösung P1--P4-vollständig, ohne eine
Transaktion zu rekonstruieren oder still zurückzufallen.

## Sicherheits- und Validierungsgrenze

- Header-, Body-, Registry- und Eventlimits schlagen fehl, statt unbeschränkten Zustand zu behalten.
- Event-JSONL enthält ausschließlich Zähler und begrenzte Metadaten, niemals Body-Payloads.
- Event-JSONL und der zugehörige Integrity-Hash ersetzen eine nichtleere
  wörtliche Query durch `?<redacted>`, während die rohe URI für die WAF-
  Verarbeitung erhalten bleibt. Historische Event- oder Audit-Logs können
  weiterhin Query-Geheimnisse enthalten; ihren Zugriff beschränken und sie
  gemäß der Aufbewahrungsrichtlinie rotieren.
- P3 endet vor dem Response-Commit; Commit ist monoton und nach finish unzulässig.
- Benannte Integrationsmodi werden auf ein exaktes Profil aufgelöst; unbekannte Modi fallen nicht zurück.
- Alle Fehler-, Cancel-, Timeout-, Ablauf- und Normalpfade verwenden kanonisches Cleanup.

Der fokussierte Vertragstest prüft die zehn Profile, gültige und ungültige
Sequenzen, doppelte und fehlende Phasen, Body-/Header-/Eventlimit-Richtlinie,
ungültige Entscheidungen, Cancel, Timeout, Cleanup, parallele Registrierung
und Wiederverwendung. Der Live-Companion-Komponententest prüft zusätzlich
Ownership-Handoff und Claim, P3/P4, TTL-Ablauf, Cancel, parallele
Transaktionen, Stream-Wiederverwendung und Shutdown-Cleanup. Native
Hostkompilierung und Live-Transportnachweise bleiben getrennt von diesen
Unit-/Komponentenchecks.

## Verwandte Referenzen

- [Gemeinsames Design](design.de.md)
- [Architektur](../../docs/architecture.de.md)
- [Envoy-Connectorleitfaden](../../docs/connectors/envoy.de.md)
- [Traefik-Connectorleitfaden](../../docs/connectors/traefik.de.md)
- [lighttpd-Connectorleitfaden](../../docs/connectors/lighttpd.de.md)
