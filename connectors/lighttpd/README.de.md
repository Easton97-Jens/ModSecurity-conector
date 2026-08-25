# lighttpd-Connector

**Sprache:** [English](README.md) | Deutsch


Status: `minimal_runtime_smoke` für den nativen Phase-1-Header-Pfad

Die primäre Integration ist jetzt ein Repository-eigenes natives Lighttpd-Modul. Es
Lädt die connector-neutrale Laufzeit von `common/runtime`, bildet echtes Lighttpd ab
Anfrage- und Antwortheader in Common SDK-Modelle, wertet ModSecurity aus und
bildet mit `http_status_set_err()` eine disruptive Phase-1-Entscheidung für lighttpd ab.

Lokal überprüft gegen die damals ausgewählte Framework-Lighttpd-Komponente und libmodsecurity:

- C17-Kompilierung und Link von `mod_msconnector.so` mit Warnungen als Fehler;
- Echte Lighttpd-Modullade- und Konfigurationsprüfung;
- echter Vordergrundstart, PID-Prüfung und sauberer Stopp ohne Senden einer Anfrage;
- Separater Laufzeitrauch für den realen Host: Baseline `OPTIONS *` gibt 200 zurück und
  `X-Modsec-Smoke: block` wird mit 403 durch die Regel `1000001` abgelehnt;
- JSONL-Entscheidungsmetadaten enthalten den Connector und die Regel-ID, keine Hauptnutzdaten.

Dies ist ein schmaler, teilweiser Laufzeitpfad. Im Standard-Stock-Build, Anfrage und
Antworttexte werden nicht implementiert und niemals an die Laufzeit übergeben. Die
Das separate Framework-synchronisierte gepatchte Paar verfügt über einen Quell-/Build-Vertrag für geliehenes HTTP/1.1
Anforderungsbereiche und Identitätsantwort-Entitätsbereiche, aber dieser Vertrag ist kein
Antworttext-Laufzeitnachweis. CRS, Produktionshärtung, Sicherheitsüberprüfung,
und Vollmatrixverifizierung werden nicht beansprucht.

Das Full-Lifecycle-Profil wählt ein separates Framework-synchronisiertes Lighttpd aus
Patched-Host-Ziel, das kopiert, patcht, konfiguriert, erstellt, installiert und
stellt einen passenden Kern und ein passendes Modul zusammen.
`runtime-smoke-lighttpd-patched` führt einen isolierten Patch-Core-/Modul-Ladevorgang durch
und der gleiche schmale Phase-1-200/403-Smoke-Test; es bleibt von der getrennt
generisches No-CRS-Ziel für Lagerbestände und fördert keine Fähigkeit. Das gepatchte
ABI ruft seinen Antwortrückruf in `http_chunk.c` für die aktuelle Ausleihe auf
HTTP/1.1-Entitätsbereich vor dem Transfer-Framing und vor jedem Socket-Schreiben. Die
Der ausgewählte Konfigurationsbereich ist nur Identität: HTTP/2 und gzip/br sind ausgeschlossen.
und es wird keine Datei-/Zero-Copy- oder Content-Encoding-Route als überprüft geltend gemacht
Antwortpfad.

## Implementierter Pfad

Das native Modul befindet sich in `module/mod_msconnector.c`. Es bietet:

- Lighttpd-Plugin-Initialisierung, Bereinigung und Konfigurationsregistrierung;
- `handle_uri_clean` Request-Header-Verarbeitung;
- `handle_response_start` Antwort-Header-Verarbeitung;
- im durch den Framework-Vertrag ausgewählten gepatchten ABI, synchrone geliehene Anfrage und Identität
  Entity-Response-Callbacks mit monotonen Offsets und einem Response-EOS;
- eine gemeinsame Laufzeittransaktion pro Lighttpd-Anfrage;
- Zuordnung des Block-/Fehlerstatus der Phase 1;
- Transaktionsabschluss und Speicherbereinigung in `handle_request_reset`.

`src/lighttpd_modsecurity_mapper.c` besitzt alle Lighttpd-spezifischen Zuordnungen. Gastgeber
Typen geben nicht `common/` ein. Zugeordnete Header-Arrays bleiben bis zur Anforderung aktiv
zurückgesetzt, da die Common Runtime Anforderungs- und Antwortdaten für die ausleiht
Transaktionsdauer.

## Konfiguration

Die Lighttpd-Hostkonfiguration verfügt über zwei serverbezogene Anweisungen:

```lighttpd
server.modules += ( "mod_msconnector" )
msconnector.enabled = "enable"
msconnector.config-file = "/absolute/path/msconnector-runtime.conf"
```

Die referenzierte Common-Runtime-Datei verwendet die `key=value`-Syntax. Zu
den unterstützten Werten gehören Regelquellen, Transaktions-ID-Einstellungen,
Body-Richtlinien und -Limits, Block-/Fehlerstatus, Ereignispfad sowie Header-
und Ressourcengrenzen. Für das Stock-Phase-1-Modul müssen beide Body-Modi
`none` sein. Der separat ausgewählte gepatchte Build akzeptiert `none` oder
`streaming` für eine Body-Richtung nur im dokumentierten ausgewählten Scope.
Für `request_body_mode=streaming` ist das ausgewählte HTTP/1.1-`mod_proxy`-
Profil ein Pre-Upstream-Phase-2-Gate und kein Upstream-Request-Streaming:
lighttpd puffert Client-Bytes bis zum terminalen EOS und zur Phase-2-
Entscheidung. Ein erlaubter Chunked-Request kann danach als
`Content-Length` weitergeleitet werden. Weil dieses Gate die Host-Queue bis
EOS behält, verlangt sein Streaming-Profil `body_limit_action=reject`;
`process_partial` wird bei ausgewähltem Request-Streaming abgewiesen. Der
Response-Streaming-Vertrag bleibt auf HTTP/1.1-Identity-Entity-Bytes
beschränkt.
Der eingecheckte gepatchte Smoke-Test verwendet weiterhin beide Modi als
`none`; eine Umstellung seines Preparers auf Response-Streaming ist eine
Konfigurations-/Quellvertragsprüfung und keine Phase-4-Promotion.
`LIGHTTPD_PATCHED_ENTITY_ENCODING=gzip` oder `br` bleibt blockiert, bis
Filterreihenfolge und Dekomprimierungsverhalten durch echte Host-Beweise
belegt sind.

`config/lighttpd-native.conf` ist ein dokumentiertes Beispiel; seine zwei
absoluten Platzhalterpfade müssen ersetzt werden. Der native Harness erzeugt
eine ausführbare Konfiguration mit verwalteten absoluten Pfaden.

## HTTP/1.1-Pre-Upstream-Phase-2-Gate

Dieses begrenzte Profil verlangt `mod_proxy` vor `mod_msconnector` in
`server.modules`, HTTP/1.1, ein positives Common-Request-Body-Limit,
`body_limit_action=reject` sowie das gepatchte Host-/Modulpaar. Der Connector
unterdrückt aktives Host-Request-Streaming vor jedem Body-Lesen. ModSecurity
erhält weiterhin geliehene Body-Ranges, aber kein Request-Byte darf den Proxy-
Upstream verbinden oder erreichen, bevor terminales EOS eine Allow-
Entscheidung erzeugt hat.
Die Grenze für den zurückgehaltenen Body ergibt sich aus dem positiven Common-
`request_body_limit` (standardmäßig 1 MiB) und dem ablehnenden Lesezyklus;
das Modul setzt `server.max-request-size` nicht, sodass dieser Wert eine
zusätzliche Host-seitige Defense-in-Depth-Grenze bleibt.

Der Repository-eigene Gate-Runner validiert einen verzögerten Phase-2-Marker
als `403` mit null Upstream-Verbindungen vor EOS sowie einen verzögerten
benignen 32-Byte-Chunked-Request als `200` erst nach EOS; lighttpd leitete
diesen erlaubten Request als `Content-Length` weiter. Vorab konfigurierte
`server.stream-request-body`, eine `Incremental`-Anfrage und eine ausdrücklich
aktivierte body-tragende `Upgrade`- plus `gw.upgrade-with-request-body`-Anfrage
werden vor einer Upstream-Verbindung mit `501` abgewiesen. Der Runner prüft
außerdem, dass eine Streaming-Konfiguration mit
`body_limit_action=process_partial` vor einem Listener oder einer Upstream-
Verbindung nicht geladen wird. HTTP/2, HTTP/3, andere Stream-Handler,
Response-Body-P4 und unbeschränktes Upstream-Request-Streaming bleiben
außerhalb dieses Profils.

## Build und Validierung

Build, Bridge-Selbsttest, Konfigurationsprüfung, Start-Smoke und Runtime-Smoke
sind getrennte Vorgänge:

```sh
make -C connectors/lighttpd build-lighttpd-bridge
make -C connectors/lighttpd self-test-lighttpd-bridge
make -C connectors/lighttpd build-lighttpd-connector
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd

# Requires LIGHTTPD_SOURCE_DIR, MODSECURITY_INCLUDE_DIR and
# MODSECURITY_LIB_DIR.  This builds a copied Framework-synchronized core and its module
# together below BUILD_ROOT/lighttpd-core-patched.
make -C connectors/lighttpd build-lighttpd-patched-host
make -C connectors/lighttpd check-lighttpd-patched-host
make -C connectors/lighttpd runtime-smoke-lighttpd-patched
```

Der native Build erfordert absolutes `LIGHTTPD_SOURCE_DIR`,
`MODSECURITY_INCLUDE_DIR`- und `MODSECURITY_LIB_DIR`-Pfade sowie die generierten
lighttpd `config.h` bis `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_BUILD_DIR` oder
`LIGHTTPD_CONFIG_DIR`. Für die Validierung ist außerdem `LIGHTTPD_BIN` erforderlich.

`start-smoke-lighttpd` sendet keine Anfragen. Nur
`runtime-smoke-lighttpd` sendet die Baseline- und Blockierungsanforderungen, also erstellen Sie,
Selbsttest, Prozessstart und Laufzeitnachweis dürfen nicht verwechselt werden.

Das gepatchte Ziel schreibt Kern- und Hostmanifeste mit dem Patch SHA-256,
Binär-/Modulpfade und Artefakt-Hashes. Es lehnt eine Standard-Binärdatei/ein Standardmodul ab
mischen. Der ältere Brückenstarter und der Smoke-Test des Rahmenbeiwagens bleiben getrennt
historische/alternative Wege. Ihre Selbsttests sind keine native Host-Laufzeit
Beweise.

## Grenzen beanspruchen

Der aktuelle Laufzeitnachweis unterstützt nur `minimal_runtime_smoke` / a
`partial_runtime_path` für Anforderungs- und Antwortheader und eine Phase-1-Verweigerung.
Er unterstützt zusätzlich das oben beschriebene eng begrenzte HTTP/1.1-
`mod_proxy`-Pre-Upstream-Phase-2-Gate; dies fördert keinen allgemeinen
Request-Streaming-, Protocol-, P4-, CRS- oder Production-Readiness-Claim.
Die Patched-Core-Kompilierung und die Modulobjektprüfungen stellen eine Release-Anheftung her
Quell-/Build-Vertrag, kein echter Antworttext-Hostlauf. Es stellt nicht fest:

- ein vom Kunden beobachtetes Phase-4-Regelergebnis oder eine Durchsetzung durch die Antwortstelle;
- Blockierung des Antwortkörpers, Verhalten bei später Intervention, Timing des ersten Bytes oder
  kein Vollpuffer-Client-Nachweis;
- CRS-Vollständigkeit oder jeglicher CRS-Anspruch;
- Produktionsbereitschaft, Sicherheitsüberprüfung oder vollständige Matrixüberprüfung.

## Kanonische Phase-4-Grenze

Der standardmäßige native Pfad verfügt nur über einen Response-Start-Header-Hook. Die Veröffentlichung angepinnt
Der gepatchte Pfad fügt zuvor einen eindeutigen HTTP/1.1-Identitäts-Entity-Body-Callback hinzu
HTTP/1-Übertragungsrahmen: Anwendungs-/Backend-Ausgabe → ausgewählte Identitätsentität
Bereich → msconnector-Rückruf → HTTP/1-Chunk-Framing (falls ausgewählt) → Socket.
Es übergibt einen geliehenen Zeiger und eine geliehene Länge synchron und verfolgt eine Monotonie
Entitätsoffset und gibt höchstens einmal EOS aus. Socket-Kurzschreibvorgänge und `EAGAIN`
treten später auf, sodass ihre Wiederholungsversuche den Entitätsbereich nicht erneut übermitteln können. Das ist
schrittweise Körperaufnahme mit End-of-Stream-Phase-4-Bewertung; es ist kein
behaupten, dass Regeln pro Block ausgeführt werden.

Der ausgewählte Bereich aktiviert nicht gzip/br, HTTP/2 oder jede Datei/Zero-Kopie
Ausgaberoute. Der aktuelle Harness führt keinen Streaming-P4-Verkehr aus und
Es gibt keinen echten Client-Beweis für ein sichtbares sicheres Ergebnis, eine Pre-Commit-Verweigerung.
Zustellung im ersten Byte oder ein strikter Verbindungsabbruch. Der Quellpfad zeichnet a auf
sicheres/minimal störendes Ergebnis wie `log_only`; streng absichtlich protokolliert
`NOT EXECUTED` und wird fortgesetzt, da kein vom Client validiertes Abbruchgrundelement vorhanden ist
nachgewiesen worden. Dementsprechend die eingecheckten Phase-4-bezogenen Fähigkeitszustände
bleiben `not_implemented` für das ausgewählte Beweisprofil.

Dies ist eine Beweisgrenze, keine Aussage, die lighttpd niemals unterstützen kann
Antwortkörperverarbeitung. Phase-4-Fälle bleiben `NOT_EXECUTED` (oder werden weggelassen).
nach Fähigkeitsauswahl), bis ein echter Host-Lauf den fehlenden Client bereitstellt und
Transportartefakte; Sie dürfen nicht ohne `UNSUPPORTED` heißen
Architekturbeweis. Es gibt daher keine vom Kunden verifizierte Phase 4
ursprüngliche/angeforderte/sichtbare Statusaufteilung, verspätete Aktion oder Verbindungsabbruch
Beweise, die noch zu melden sind.

Das bestehende Phase-1-Header-Deny ist ein separater Beweis.  Veranstaltungen und Berichte
bleiben nur Metadaten und enthalten niemals eine Antworttext-Nutzlast.
