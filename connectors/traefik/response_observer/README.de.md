# Traefik-Response-Observer

**Sprache:** [English](README.md) | Deutsch

Standardmäßig ist dieses lokale Plugin der reine Response-Adapter des kanonischen
Transaktionsvertrags und wird hinter dem C-`forwardAuth`-Dienst eingesetzt.
In `authResponseHeaders` darf ausschließlich der Handle-Header freigegeben
werden. Das Plugin akzeptiert genau einen serverseitig erzeugten
`X-Msconnector-Response-Handle`, entfernt ihn vor dem Upstream-Aufruf und
überträgt P3/P4 über den konfigurierten privaten Unix-Socket.

Der optionale Modus für vertrauenswürdige Provenienz läuft stattdessen
**ganz außen**, vor der eingebauten ForwardAuth-Middleware. Setze
`provenanceSocketPath`, `runID` und `transportCaseID` gemeinsam sowie
`MSCONNECTOR_TRAEFIK_PROVENANCE_SOCKET` auf denselben benachbarten Socket im
C-ForwardAuth-Dienst für Traefik. Ein separater, ausschließlich Traefik
gehörender `MTP1`-v1-Listener übernimmt die Reservierung; das kanonische
MRC1-Wire-Protokoll und die gewöhnlichen/standardmäßigen Aufrufpfade bleiben unverändert.
Beide Prozesse müssen dieselbe erwartete effektive Unix-UID/GID verwenden.
Der Socket darf noch nicht existieren; sein kanonisches Elternverzeichnis
muss dem Dienst gehören und Modus 0700 haben.

Die Reihenfolge ist verbindlich: äußerer Observer → eingebautes ForwardAuth →
innerer Observer mit `confirmProvenance: true` → Backend. Die innere Instanz
darf `provenanceSocketPath`, `runID` und `transportCaseID` nicht setzen. Die
explizite `authRequestHeaders`-Liste von ForwardAuth muss
`X-Msconnector-Trusted-Reservation` enthalten. Der innere Observer bestätigt
die private Antwort vor dem Backend-Aufruf und entfernt diesen Header sowie
`X-Msconnector-Response-Handle`, einschließlich Trailer-Deklarationen.
Der Observer entfernt vom Client gelieferte
Reservierungsheader/-trailer und Handles, reserviert vor dem nächsten Handler
privat und setzt nur eine zufällige Einmal-Capability für den unmittelbaren
Autorisierungsschritt. Seine abschließende Bereinigung ersetzt die innere
Bestätigungsinstanz nicht.

MTP1 akzeptiert drei begrenzte, nicht leere ASCII-IDs mit höchstens je 128
Bytes und ein Reuse-Byte mit Wert null. Höchstens 128 Reservierungen leben
jeweils fünf Sekunden. Schließen, Ablauf, ungültige oder doppelte Frames,
fehlende/doppelte/gefälschte sowie bereits verbrauchte Tokens schlagen
fail-closed fehl. Der C-Dienst beansprucht die Reservierung atomar und kopiert
die privaten Metadaten vor nativem P1. Die Capability wird aus den nativen
Request-Headern entfernt. Eine private Abschlussabfrage bindet den tatsächlichen
Status der Autorisierungsantwort oder den Response-Companion-Handle an
dieselbe Lease. Der paketprivate Request-Kontext bindet die innere Bestätigung
an ihre äußere Reservierung; fehlende oder doppelte Bestätigung schlägt
fail-closed fehl. Die zwischengespeicherte private Bestätigung hält Backend-
Wartezeit außerhalb des Fünf-Sekunden-Reservierungsfensters. MRC1 läuft initial
nach höchstens fünf Sekunden ab. Vor Ausgabe eines Allow-Handles bestätigt
die peer-authentisierte innere MTP1-Abfrage genau einmal unter dem Common-
Registry-Lock diesen unbenutzten, noch gültigen Handle. Nur sein Ablauf wird
auf den ursprünglichen konfigurierten Handoff-Endzeitpunkt erweitert (bei
Traefik 30 Sekunden). Dies gewährt nur die verbleibende Handoff-Laufzeit,
keine neuen 30 Sekunden. Backend-Wartezeit verbraucht diese verbleibende
absolute Laufzeit; bei Ablauf des konfigurierten Handoff-Endzeitpunkts schlägt
der Claim fail-closed fehl. Abgelaufene, beanspruchte, wiederholte, fremde oder
Shutdown-Einträge sowie Callback-Fehler schlagen vor Backend-Eintritt
fail-closed fehl. Deny/leere Handles verlängern keinen Eintrag. Normale MRC1-
Clients behalten das Fünf-Sekunden-Preclaim-Limit. Der separate MRC1-`CLAIM`
erfolgt normal beim ersten Response-Header. Panic,
Abbruch oder Return vor jedem Header beansprucht den bestätigten Handle
stattdessen ausschließlich für sofortiges typisiertes `CANCEL` mit eigenem
begrenzten Cleanup-Kontext. Cleanup-Fehler bleiben erhalten und erzeugen ein
festes payloadfreies physisches Logsignal; der begrenzte Ablauf des bestätigten
Handles bleibt der Fallback.
Eine terminale Autorisierungsantwort wird nur bei gleichem
privat bestätigtem Status weitergegeben; Allow öffnet den bestätigten
MRC1-Handle. Kein Client-HTTP-Feld liefert IDs oder diese Bestätigung.

`connection_id` ist ein instanzlokaler HMAC über die vertrauenswürdigen lokalen
und entfernten Go-Socket-Tupel. Das ist eine opake Korrelation: Tupel können
wiedervergeben werden und dem Plugin fehlt ein ConnState-Schließhook.
`connection_reused` bleibt deshalb false. Ein Keepalive-Nachweis braucht
weiterhin unabhängige physische Belege für denselben lebenden Socket.
Forwarded-Header und der Loopback-Socket des Autorisierungsdienstes bestimmen
die Downstream-Verbindungsidentität nicht. Common kopiert IDs vor P1, leitet
`eos_seen` vom tatsächlichen Body-Finish-Zustand ab und schreibt den letzten
integritätsverketteten Cleanup-Datensatz erst nach nativem Free und
Vertrags-Cleanup. Dieser Datensatz belegt Runtime-Cleanup, weder Clientzustellung
noch natives EOS durch TCP-EOF. Das bestehende `maxResponseBodySize=32768`
bleibt ausschließlich Kapazität der Autorisierungsantwort und muss konfiguriert bleiben.

Das begrenzte `MRC1`-Protokoll verwendet Version 2, 12-Byte-Header und
maximal 32 KiB je Response-Chunk. Alle Nicht-P3-Frames bleiben auf 64 KiB
begrenzt. Ein P3-`RESPONSE_HEADERS`-Frame darf zwischen MRC1-Peers einen Payload
von bis zu 66.630 Bytes verwenden; dieser HTTP/1.1-Observer emittiert höchstens
66.574 Payload-Bytes, während das logische Header-Namens-/Wertaggregat auf 64 KiB
begrenzt bleibt. Sein ein Byte großer `CANCEL`-Payload transportiert die
kanonische terminale Ursache (Client-Cancel, Upstream-Disconnect, Connector-
oder Protokollfehler, Engine-Timeout/Unavailable oder ungültige Engineantwort).
Es gibt keinen Version-1-Fallback: ein nicht passender Listener schlägt
fail-closed fehl. Das Plugin überträgt
im Standardmodus weder Transaktions- noch Host-IDs, öffnet P1/P2 nicht und besitzt keinen
zweiten Automaten. Fehlende, ungültige, wiederverwendete oder nicht erreichbare
Handles werden vor dem Commit fail-closed behandelt. Nach dem Commit wird eine
disruptive Entscheidung nur als Log-only gemeldet. Der Wrapper bietet weder
`Unwrap` noch `Hijacker`.

Vor dem ersten `CLAIM`-Frame authentisiert der Observer den verbundenen
Response-Companion-Server unter Linux mit `SO_PEERCRED`. Standardmäßig
erwartet er die effektive UID und GID des Observer-Prozesses. Wenn der
Companion mit einer anderen Identität läuft, müssen in der Plugin-Konfiguration
`expectedPeerUID` und `expectedPeerGID` gemeinsam gesetzt werden; auch der
Wert `0` ist ausdrücklich möglich. Fehlende Credentials, abweichende
Identitäten und Nicht-Linux-Plattformen schlagen vor dem Upstream-Aufruf
fail-closed fehl. Das private Socket-Verzeichnis des Companion und seine
vollständige Ancestor-Chain müssen zudem gegen Austausch durch andere UIDs
geschützt sein. Gleiche Unix-IDs bilden eine gemeinsame Vertrauensdomäne:
`SO_PEERCRED` belegt weder Binärintegrität noch Security-Labels oder die
Zuordnung von User-Namespaces.

Führe `../build/build-response-observer.sh test` aus diesem Repository aus,
um die lokalen Unit- und Vet-Prüfungen auszuführen. Dies ist Source-Level-
Evidence und beansprucht keinen Traefik-Hostlauf.
