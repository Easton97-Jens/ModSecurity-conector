# Traefik-Response-Observer

**Sprache:** [English](README.md) | Deutsch

Dieses lokale Plugin ist der reine Response-Adapter des kanonischen
Transaktionsvertrags und wird hinter dem C-`forwardAuth`-Dienst eingesetzt.
In `authResponseHeaders` darf ausschließlich der Handle-Header freigegeben
werden. Das Plugin akzeptiert genau einen serverseitig erzeugten
`X-Msconnector-Response-Handle`, entfernt ihn vor dem Upstream-Aufruf und
überträgt P3/P4 über den konfigurierten privaten Unix-Socket.

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
weder Transaktions- noch Host-IDs, öffnet P1/P2 nicht und besitzt keinen
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
