# lighttpd-Connector

Status: `minimal_runtime_smoke` für den nativen Phase-1-Headerpfad

Der primäre Integrationspfad ist jetzt ein Repository-eigenes natives
lighttpd-Modul. Es bindet die connector-neutrale Runtime aus `common/runtime`
ein, überführt echte lighttpd-Request- und Response-Header in Common-SDK-Modelle
und setzt disruptive Phase-1-Entscheidungen mit `http_status_set_err()` um.

Gegen das gepinnte lighttpd 1.4.84 und libmodsecurity lokal belegt sind:

- C17-Compile und Link von `mod_msconnector.so` mit Warnungen als Fehler;
- echtes Laden des Moduls und erfolgreiche lighttpd-Konfigurationsprüfung;
- echter Vordergrundstart, PID-Prüfung und sauberes Stoppen ohne Request;
- separater Host-Runtime-Smoke: `OPTIONS *` liefert 200, während
  `X-Modsec-Smoke: block` durch Regel `1000001` mit 403 blockiert wird;
- JSONL-Metadaten mit Connector und Regel-ID, ohne Body-Payload.

Dies ist bewusst ein enger, partieller Runtime-Pfad. Im Stock-Build sind
Request- und Response-Bodies nicht implementiert und werden niemals an die
Runtime übergeben. Das getrennte gepatchte 1.4.84-Paar besitzt einen
Source-/Build-Vertrag für geliehene HTTP/1.1-Request-Ranges und Identity-
Response-Entity-Ranges, aber keinen Response-Body-Runtime-Nachweis. Es gibt
keine Behauptung zu CRS, Produktionsreife, Security-Verifikation oder Full
Matrix.

Das Full-Lifecycle-Profil wählt ein separates Ziel für einen gepatchten Host,
das einen passenden lighttpd-1.4.84-Core zusammen mit dem Modul kopiert,
patcht, konfiguriert, baut, installiert und staged.
`runtime-smoke-lighttpd-patched` prüft das Laden dieses isolierten
Core/Modul-Paars und denselben engen Phase-1-200/403-Smoke. Es bleibt vom
generischen Stock-No-CRS-Ziel getrennt und promotet keine Capability. Die
Response-ABI des Patches wird in `http_chunk.c` mit dem aktuellen geliehenen
HTTP/1.1-Entity-Range vor Transfer-Framing und vor jedem Socket-Write
aufgerufen. Der ausgewählte Konfigurationsumfang ist Identity: HTTP/2 und
gzip/br sind ausgeschlossen; Datei-/Zero-Copy- und Content-Encoding-Pfade
werden nicht als inspizierter Response-Pfad behauptet.

## Implementierter Pfad

`module/mod_msconnector.c` implementiert Plugin-Initialisierung, Cleanup,
Config-Registrierung, Request-Header-Hook, Response-Start-Hook,
Transaction-Lifecycle, Block-/Fehlerstatus und Cleanup beim Request-Reset.
Im gepatchten 1.4.84-ABI kommen synchrone geliehene Request- und Identity-
Entity-Response-Callbacks mit monotonen Offsets und genau einem Response-EOS
hinzu.

`src/lighttpd_modsecurity_mapper.c` kapselt sämtliche lighttpd-Typen. Die
gemappten Header bleiben bis zum Request-Reset gültig, da die Common Runtime
Request und Response während der Transaktion nur ausleiht.

## Konfiguration

```lighttpd
server.modules += ( "mod_msconnector" )
msconnector.enabled = "enable"
msconnector.config-file = "/absoluter/pfad/msconnector-runtime.conf"
```

Die referenzierte Common-Runtime-Datei verwendet `key=value`. Sie bildet unter
anderem Regelquellen, Transaction-ID, Body-Modi und Limits, Block-/Fehlerstatus,
Event-Pfad und Header-Limits ab. Für den aktuellen nativen Stock-Phase-1-Pfad
müssen beide Body-Modi `none` sein. Der vom Full-Lifecycle-Profil separat
gewählte gepatchte Build akzeptiert je Richtung `none` oder `streaming`, sein
Response-Streaming-Vertrag gilt aber nur für HTTP/1.1-Identity-Entity-Bytes.
Der eingecheckte gepatchte Smoke nutzt weiter beide Modi als `none`; ein
Response-Streaming-Wert im Preparer ist ein Konfigurations-/Source-Vertrag,
keine Phase-4-Promotion. `LIGHTTPD_PATCHED_ENTITY_ENCODING=gzip` oder `br`
wird blockiert, bis Filterreihenfolge und Dekompression echten Host-Nachweis
haben.

`config/lighttpd-native.conf` ist ein Beispiel; seine beiden absoluten
Platzhalterpfade müssen ersetzt werden. Der native Harness erzeugt selbst eine
ausführbare Konfiguration mit verwalteten absoluten Pfaden.

## Build und Nachweise

```sh
make -C connectors/lighttpd build-lighttpd-bridge
make -C connectors/lighttpd self-test-lighttpd-bridge
make -C connectors/lighttpd build-lighttpd-connector
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd

# Benötigt LIGHTTPD_SOURCE_DIR, MODSECURITY_INCLUDE_DIR und
# MODSECURITY_LIB_DIR. Der gepatchte Core und das passende Modul landen unter
# BUILD_ROOT/lighttpd-core-patched.
make -C connectors/lighttpd build-lighttpd-patched-host
make -C connectors/lighttpd check-lighttpd-patched-host
make -C connectors/lighttpd runtime-smoke-lighttpd-patched
```

Der native Build benötigt absolute Pfade in `LIGHTTPD_SOURCE_DIR`,
`MODSECURITY_INCLUDE_DIR` und `MODSECURITY_LIB_DIR`. Das erzeugte lighttpd
`config.h` wird über `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_BUILD_DIR` oder
`LIGHTTPD_CONFIG_DIR` gefunden. Für die Host-Nachweise ist zusätzlich
`LIGHTTPD_BIN` erforderlich.

`start-smoke-lighttpd` sendet ausdrücklich keine Requests. Nur der separate
`runtime-smoke-lighttpd` führt den 200/403-Requestpfad aus. Der gepatchte
Pfad schreibt Core- und Host-Manifeste mit Patch-SHA-256, Binary-/Modulpfaden
und Artefakt-Hashes und verweigert ein Mischen mit einem Stock-Host. Der ältere
Bridge-Starter und der Framework-Sidecarpfad bleiben getrennte Alternativen;
deren Self-Tests sind kein Nachweis für den nativen Hostpfad.

## Claim-Grenzen

Als Runtime belegt ist ausschließlich `minimal_runtime_smoke` beziehungsweise
ein `partial_runtime_path` für Header und Phase-1-Deny. Gepatchter-Core-Compile
und Modulobjektprüfung belegen einen release-gebundenen Source-/Build-Vertrag,
keinen echten Response-Body-Hostlauf. Nicht belegt sind client-sichtbare
Phase-4-Regelergebnisse oder Durchsetzung, Late Intervention, First-Byte-,
No-Full-Buffer-, CRS-, Produktionshärtungs-, Security- und vollständige
Matrix-Nachweise.

## Kanonische Grenze für Phase 4

Der Stock-Pfad besitzt nur einen Response-Start-Header-Hook. Der
release-gebundene gepatchte Pfad ergänzt einen eigenen HTTP/1.1-Identity-
Entity-Body-Callback vor HTTP/1-Transfer-Framing: Anwendung/Backend →
ausgewählter Identity-Entity-Range → msconnector-Callback → HTTP/1-
Chunk-Framing (falls ausgewählt) → Socket. Er übergibt geliehenen Pointer und
Länge synchron, verfolgt einen monotonen Entity-Offset und sendet EOS höchstens
einmal. Socket-Short-Writes und `EAGAIN` treten danach auf, sodass ihre
Wiederholung keinen Entity-Range erneut an die Rule Engine übergeben kann. Das
ist inkrementelles Body-Ingest mit End-of-Stream-Phase-4-Auswertung, keine
Behauptung einer Regelauswertung pro Chunk.

Der ausgewählte Umfang behauptet weder gzip/br, HTTP/2 noch alle Datei-/
Zero-Copy-Ausgaberouten. Der aktuelle Harness führt keinen P4-Streaming-
Traffic aus; es gibt keinen echten Client-Nachweis für sichtbares Safe-Ergebnis,
Precommit-Deny, First Byte oder einen strikten Verbindungsabbruch. Der
Sourcepfad zeichnet eine disruptive Safe-/Minimal-Entscheidung als `log_only`
auf; Strict loggt bewusst `NOT EXECUTED` und setzt fort, da kein
client-validiertes Abort-Primitiv belegt ist. Deshalb bleiben die
Phase-4-bezogenen Capability-Zustände für das ausgewählte Evidence-Profil
`not_implemented`.

Dies ist eine Evidence-Grenze und keine Aussage, dass lighttpd
Response-Body-Verarbeitung grundsätzlich nie unterstützen kann. Phase-4-Fälle
bleiben `NOT_EXECUTED` (oder werden durch die Capability-Auswahl nicht gewählt),
bis ein echter Hostlauf die fehlenden Client- und Transportartefakte liefert.
Ohne Architekturbeleg dürfen sie nicht `UNSUPPORTED` heißen. Folglich gibt es
noch keinen client-verifizierten Phase-4-Nachweis für getrennte ursprüngliche,
angeforderte und sichtbare Statuswerte, späte Aktionen oder
Verbindungsabbruch.

Der vorhandene Phase-1-Header-Deny ist ein getrenntes Nachweisergebnis.
Ereignisse und Berichte bleiben metadatenbasiert und enthalten niemals
Response-Body-Payloads.
