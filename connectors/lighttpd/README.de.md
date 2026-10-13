# lighttpd-Connector

**Sprache:** [English](README.md) | Deutsch

Status: kanonisches Stock-Sidecar-Komponent plus getrennte native/gepatchte Hostpfade

## Kanonische Stock-Lösung

Die kanonische `lighttpd-stock`-Lösung ist das traffic-owning
`stock-lighttpd-sidecar` in `stock_sidecar/`. Es bindet ausschließlich an eine
ausdrücklich konfigurierte wörtliche `127.0.0.1`-Adresse, spricht begrenztes
HTTP/1.1, besitzt den vollständigen Austausch zwischen Client und privatem
Stock-Backend und führt P1, P2, P3 und P4 über den Common-Runtime-Vertrag aus.
Ein begrenzter Worker besitzt Transaktion und deterministisches Cleanup, daher
benötigt diese Topologie weder prozessübergreifende Korrelation noch eine
TTL-Registry. Event-JSONL enthält nur begrenzte Metadaten und Zähler; Request-
und Response-Body-Payloads werden niemals ausgegeben.

Für P4 verwendet der Sidecar jeweils genau einen begrenzten Response-Chunk: Er
hängt diesen Chunk einmal an Common/libModSecurity an und reicht ihn sofort an
den Client weiter; nur Response-EOS ruft die finale P4-Entscheidung auf. Nach
einem committed Präfix erfasst Safe `log_only` und setzt fort, während Strict
die Client-Verbindung beendet. Das ist Sidecar-Komponentenverhalten und keine
Behauptung nativer Body-Hooks im unveränderten Stock-lighttpd-Prozess.

Die unveränderte native Stock-Modulroute (`stock-lighttpd`) bleibt nur eine
ausdrückliche nichtkanonische P1/P3-Kompatibilitätsübersetzung. Sie besitzt
keine sicheren Body- oder EOS-Callbacks, ist niemals ein stiller Capability-
Fallback und darf nicht als zweiter Traffic-Eigentümer neben dem Sidecar
aktiviert werden. Die gepatchte Route ist eine getrennte logische Lösung.

Die primäre Integration ist ein Repository-eigenes natives lighttpd-Modul. Es
lädt die connector-neutrale Laufzeit aus `common/runtime`, überführt echte
lighttpd-Anfrage- und Antwortheader in Common-SDK-Modelle, wertet ModSecurity
aus und bildet eine disruptive Phase-1-Entscheidung mit `http_status_set_err()`
auf lighttpd ab.

Lokal gegen die damals ausgewählte Framework-lighttpd-Komponente und
libmodsecurity geprüft:

- C17-Kompilierung und Linken von `mod_msconnector.so` mit Warnungen als Fehler;
- echtes Laden des lighttpd-Moduls und Konfigurationsprüfung;
- echter Vordergrundstart, PID-Prüfung und sauberer Stopp ohne Anfrage;
- separater echter Host-Runtime-Smoke: Baseline `OPTIONS *` liefert 200 und
  `X-Modsec-Smoke: block` wird durch Regel `1000001` mit 403 abgelehnt;
- JSONL-Entscheidungsmetadaten enthalten Connector und Regel-ID, aber keine
  Body-Payloads.

Dies ist ein schmaler, teilweiser Runtime-Pfad. Im Standard-Stock-Build sind
Anfrage- und Antwortbodys nicht implementiert und werden nie an die Laufzeit
übergeben. Das separat gepatchte, Framework-synchronisierte Paar besitzt einen
Quell-/Build-Vertrag für geliehene HTTP/1.1-Anfragebereiche und
Identity-Response-Entity-Bereiche, doch dieser Vertrag ist kein
Response-Body-Runtime-Nachweis. CRS, Produktionshärtung, Security-Verifikation
und Vollmatrix-Verifikation werden nicht beansprucht.

Das Full-Lifecycle-Profil wählt ein separates,
Framework-synchronisiertes, gepatchtes lighttpd-Hostziel, das einen passenden
Core und ein passendes Modul gemeinsam kopiert, patcht, konfiguriert, baut,
installiert und bereitstellt. `runtime-smoke-lighttpd-patched` führt ein
isoliertes Laden von gepatchtem Core und Modul sowie denselben schmalen
Phase-1-200/403-Smoke aus. Es bleibt vom generischen Stock-No-CRS-Ziel getrennt
und fördert keine Capability. Das gepatchte ABI ruft seinen Response-Callback
in `http_chunk.c` für den aktuellen geliehenen HTTP/1.1-Entity-Bereich vor dem
Transfer-Framing und vor jedem Socket-Schreiben auf. Der ausgewählte
Konfigurationsumfang ist auf Identity beschränkt: HTTP/2 und gzip/br sind
ausgeschlossen; kein Datei-/Zero-Copy- oder Content-Encoding-Pfad wird als
untersuchter Response-Pfad beansprucht.

## Implementierter Pfad

Das native Modul liegt unter `module/mod_msconnector.c`. Es bietet:

- Initialisierung, Bereinigung und Konfigurationsregistrierung des
  lighttpd-Plugins;
- Anfrageheader-Verarbeitung über `handle_uri_clean`;
- Antwortheader-Verarbeitung über `handle_response_start`;
- im durch den Framework-Vertrag ausgewählten gepatchten ABI synchrone,
  geliehene Anfrage- und Identity-Entity-Response-Callbacks mit monotonen
  Offsets und genau einem Response-EOS;
- genau eine Common-Runtime-Transaktion pro lighttpd-Anfrage;
- Abbildung von Phase-1-Block-/Fehlerstatus;
- Transaktionsabschluss und Speicherbereinigung in `handle_request_reset`.

`src/lighttpd_modsecurity_mapper.c` besitzt alle lighttpd-spezifischen
Zuordnungen. Host-Typen gelangen nicht nach `common/`. Zuordnete Header-Arrays
bleiben bis zum Request-Reset erhalten, weil die Common Runtime Anfrage- und
Antwortdaten für die gesamte Transaktionsdauer leiht.

## Konfiguration

Die lighttpd-Hostkonfiguration enthält diese serverweiten Direktiven:

```lighttpd
server.modules += ( "mod_msconnector" )
msconnector.enabled = "enable"
msconnector.config-file = "/absolute/path/msconnector-runtime.conf"
# Required only when request_body_mode=streaming in the patched profile:
# msconnector.request-body-gate = "pre-upstream"
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
`Content-Length` weitergeleitet werden. Das Modul verlangt zusätzlich die
explizite Serverdirektive `msconnector.request-body-gate = "pre-upstream"`
und setzt in diesem Profil niemals `FDEVENT_STREAM_REQUEST`: Anfragebereiche
werden durch den gepatchten geliehenen Anfrage-Hook untersucht, und
Proxy-/Upstream-Dispatch bleibt gesperrt, bis Anfrage-Body-EOS die Common-P2-
Entscheidung erzeugt hat. Eine disruptive Entscheidung sowie ein Body-Limit-,
Engine-, Mapping- oder Hostfehler beenden die Anfrage, bevor ein Byte zum
Upstream gelangt. Jeder geliehene MEM/FILE-Bereich erreicht die native Engine
über begrenzte Arbeitsbuffer. Das Modul besitzt kein kumuliertes Bytelimit und
wählt weder Reject noch ProcessPartial. Der
Response-Streaming-Vertrag bleibt auf HTTP/1.1-Identity-Entity-Bytes
beschränkt. Dieser Quell-/Build-Vertrag ist weiterhin keine echte
Host-Promotion.
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

Dieses Profil verlangt `mod_proxy` vor `mod_msconnector` in
`server.modules`, HTTP/1.1 und das gepatchte Host-/Modulpaar. Der Connector
unterdrückt Host-Request-Streaming bis zum nativen P2-Abschluss bei EOS. Die
Host-Queue kann Memory-/File-Chunks für die spätere Upstream-Übergabe behalten;
der Connector setzt keine Gesamtbody-Größe. `server.max-request-size` bleibt
eine getrennte Host-Einstellung, deren effektiver Wert echte Hostbelege benötigt.

Der Repository-eigene Gate-Runner validiert einen verzögerten Phase-2-Marker
als `403` mit null Upstream-Verbindungen vor EOS sowie einen verzögerten
benignen 32-Byte-Chunked-Request als `200` erst nach EOS; lighttpd leitete
diesen erlaubten Request als `Content-Length` weiter. Vorab konfigurierte
`server.stream-request-body`, eine `Incremental`-Anfrage und eine ausdrücklich
aktivierte body-tragende `Upgrade`- plus `gw.upgrade-with-request-body`-Anfrage
werden vor einer Upstream-Verbindung mit `501` abgewiesen. Die native Direktive `SecRequestBodyLimitAction` bestimmt die Engine-Aktion. HTTP/2, HTTP/3, andere Stream-Handler,
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

# Builds and runs the traffic-owning Stock sidecar component contract.
# BUILD_ROOT must be an absolute path outside the repository.
make -C connectors/lighttpd build-lighttpd-stock-sidecar
make -C connectors/lighttpd self-test-lighttpd-stock-sidecar

# Requires LIGHTTPD_SOURCE_DIR, MODSECURITY_INCLUDE_DIR and
# MODSECURITY_LIB_DIR.  This builds a copied Framework-synchronized core and its module
# together below BUILD_ROOT/lighttpd-core-patched.
make -C connectors/lighttpd build-lighttpd-patched-host
make -C connectors/lighttpd check-lighttpd-patched-host
make -C connectors/lighttpd runtime-smoke-lighttpd-patched
```

Der native Build benötigt absolute Pfade für `LIGHTTPD_SOURCE_DIR`,
`MODSECURITY_INCLUDE_DIR` und `MODSECURITY_LIB_DIR` sowie die generierte
lighttpd-`config.h` über `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_BUILD_DIR` oder
`LIGHTTPD_CONFIG_DIR`. Für die Validierung wird außerdem `LIGHTTPD_BIN`
benötigt.

`start-smoke-lighttpd` sendet keine Anfragen. Nur
`runtime-smoke-lighttpd` sendet Baseline- und Blockierungsanfragen. Build,
Selbsttest, Prozessstart und Runtime-Evidenz dürfen daher nicht verwechselt
werden.

Das gepatchte Ziel schreibt Core- und Host-Manifeste mit Patch-SHA-256,
Binär-/Modulpfaden und Artefakt-Hashes. Es lehnt eine Mischung aus
Stock-Binärdatei und Stock-Modul ab. Der ältere Bridge-Starter und der
Framework-Sidecar-Smoke bleiben getrennte historische/alternative Pfade. Ihre
Selbsttests sind kein nativer Host-Runtime-Nachweis.

## Aussagegrenzen

Die aktuelle Runtime-Evidenz unterstützt nur `minimal_runtime_smoke` bzw. einen
`partial_runtime_path` für Anfrage- und Antwortheader sowie ein Phase-1-Deny.
Sie unterstützt zusätzlich das oben beschriebene eng begrenzte HTTP/1.1-
`mod_proxy`-Pre-Upstream-Phase-2-Gate; dies fördert keinen allgemeinen
Request-Streaming-, Protokoll-, P4-, CRS- oder Produktionsreife-Claim. Die
Kompilierung des gepatchten Core und die Modulobjektprüfungen etablieren einen
release-gebundenen Quell-/Build-Vertrag, keinen echten Response-Body-Hostlauf.
Sie belegen nicht:

- ein clientbeobachtetes Phase-4-Regelergebnis oder eine
  Response-Body-Durchsetzung;
- Response-Body-Blockierung, Late-Intervention-Verhalten, First-Byte-Timing
  oder Client-Evidenz ohne Vollpuffer;
- CRS-Vollständigkeit oder einen CRS-Anspruch;
- Produktionsreife, Security-Verifikation oder Vollmatrix-Verifikation.

## Kanonische Phase-4-Grenze

Der native Stock-Pfad besitzt nur einen Response-Start-Header-Hook. Der
release-gebundene gepatchte Pfad fügt vor HTTP/1-Transfer-Framing einen
eigenständigen HTTP/1.1-Identity-Entity-Body-Callback hinzu:
Anwendungs-/Backend-Ausgabe → ausgewählter Identity-Entity-Bereich →
msconnector-Callback → HTTP/1-Chunk-Framing (falls gewählt) → Socket. Er
übergibt synchron einen geliehenen Zeiger und eine geliehene Länge, verfolgt
einen monotonen Entity-Offset und emittiert EOS höchstens einmal. Kurze
Socket-Schreibvorgänge und `EAGAIN` treten später auf; ihre Wiederholungen
können den Entity-Bereich deshalb nicht erneut übergeben. Dies ist inkrementelle
Body-Aufnahme mit Phase-4-Auswertung am End-of-Stream; es ist nicht die
Behauptung, dass Regeln pro Chunk laufen.

Der ausgewählte Umfang beansprucht weder gzip/br noch HTTP/2 oder jeden
Datei-/Zero-Copy-Ausgabepfad. Der aktuelle Harness führt keinen Streaming-P4-
Traffic aus; es gibt keinen Real-Client-Nachweis für ein sichtbares Safe-Ergebnis,
ein Pre-Commit-Deny, First-Byte-Auslieferung oder einen strikten
Verbindungsabbruch. Der Quellpfad zeichnet ein disruptives Ergebnis im Safe-Modus
als `log_only` auf. Off bewahrt die native Behandlung ohne zusätzliche Late-Policy. Der gepatchte Callback gibt bei einer
verbindungsbehafteten Strict-Intervention jetzt
`PLUGIN_BODY_HOOK_ABORT` an den Response-Fehlerpfad des gepatchten Cores
zurück; die gemeinsame Runtime weist Strict für dieses Profil bei der
Adapteraktivierung zurück, bis ein client-sichtbarer Abbruch und ein
Follow-up-Health-Nachweis vorliegen. Entsprechend bleiben die eingecheckten
Phase-4-bezogenen Capability-Zustände für das ausgewählte Evidenzprofil
`not_implemented`.

Dies ist eine Evidenzgrenze, nicht die Aussage, dass lighttpd niemals
Response-Body-Verarbeitung unterstützen kann. Phase-4-Fälle bleiben
unverifiziert (oder werden durch die Capability-Auswahl ausgelassen), bis ein
echter Hostlauf die fehlenden Client- und Transportartefakte liefert. Ohne
Architekturbeleg dürfen sie nicht `UNSUPPORTED` heißen. Folglich gibt es noch
keinen clientverifizierten Nachweis einer Phase-4-Aufteilung von originalem,
angefordertem und sichtbarem Status, einer späten Aktion oder eines
Verbindungsabbruchs.

Das vorhandene Phase-1-Header-Deny ist getrennte Evidenz. Ereignisse und
Berichte bleiben reine Metadaten und enthalten niemals eine
Response-Body-Payload.

## Phase-4-Modus und Eigentümerschaft von Response-Body-Limits

Der Standardmodus ist `off`; erlaubt sind `off`, `safe` und `strict`. Kein
gültiger Phase-4-Modus fügt ein Connector-eigenes kumuliertes
Response-Inspection-Budget hinzu. libModSecurity besitzt die WAF-Auswahl und
-Limits über `SecResponseBodyAccess`, `SecResponseBodyMimeType`,
`SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit` und
`SecResponseBodyLimitAction`.

Diese Regel gilt für native Integrationen und Response-Pfade über die Common
Runtime. Eine reine Request-Route benötigt für Phase 4 weiterhin den
unterstützten Response-Observer beziehungsweise Companion; die Wahl eines
Modus erzeugt keinen fehlenden Response-Pfad.

Kumulierte Connector-/Runtime-Response-Größeneinstellungen wurden entfernt;
unbekannte alte Schlüssel werden beim Konfigurationsladen abgewiesen.
Unabhängige Chunk-/Message-/Frame-, Timeout-, Überlauf- und Transportlimits
bleiben in jedem Modus aktiv. Der Stock-Sidecar verwendet begrenzte
Response-Blöcke und hält keinen vollständigen Response-Body im Speicher.

Der [connectorübergreifende Vertrag zur Eigentümerschaft von Response-Limits](../../docs/phase4-mode-budget.de.md)
beschreibt den genauen Geltungsbereich, die Kompatibilitätsgrenze und die
Grenzen der Validierung.

## Native Body-Policy und verbleibende Hostgrenzen

Request-Limit/-Aktion gehören ausschließlich zu `SecRequestBodyLimit` und
`SecRequestBodyLimitAction`, Response-Limit/-Aktion ausschließlich zu
`SecResponseBodyLimit` und `SecResponseBodyLimitAction`. Der Connector ergänzt
keine Body-Größenoption, keinen Default und keine kumulierte Durchsetzung.
Begrenzte IO-Blöcke und geprüfte Zähler wählen kein Engine-Limit und keine Aktion.

Der Stock-Sidecar übergibt Request-Blöcke an die native Engine und eine private,
sofort unlinked Spooldatei. Er spielt die Datei erst nach nativem P2-Allow ab.
Dateisystemfehler führen zum Abbruch; Vollbody-RAM-Allokation und eigene
Gesamtbody-Grenze entfallen. Gepatchte Host-Queue und die eigene Einstellung
`server.max-request-size` benötigen unabhängige Hostbelege.

Das optionale technische CLI-Argument `--spool-directory /var/lib/msconnector/lighttpd-stock/safe`
wählt den Speicherort für Request-Spooldateien. Ohne dieses Argument verwendet
der Sidecar das Elternverzeichnis von `--config`. Es muss bereits existieren,
kanonisch, beschreibbar, Eigentum der effektiven Service-UID und im Modus 0700
sein. Beim Start werden die Vorfahren geprüft, Verzeichnisdeskriptoren ohne
Symlink-Verfolgung festgehalten und die Dateierstellung geprüft. Für eine
Konfiguration unter `/etc` ist ein separates privates Laufzeitverzeichnis
anzugeben. Es gibt keinen Fallback auf Umgebungsvariablen oder öffentliche
Temporärverzeichnisse. Request-Dateien werden exklusiv im Modus 0600 unter dem
festgehaltenen Verzeichnis erstellt und sofort unlinked; diese Speicheroption
führt kein Gesamtbody-Limit ein.

Die ausgelieferten argv-Dateien wählen separate private, diskgestützte
Verzeichnisse unter `/var/lib/msconnector/lighttpd-stock/{all,off,safe,strict}`.
Ein Profil wird als Service-UID mit
`python3 connectors/lighttpd/launch_stock_sidecar.py --profile safe` gestartet.
Der Launcher akzeptiert ausschließlich `all`, `off`, `safe` und `strict`, liest
deren feste repository-eigene argv-Dateien und startet die installierte native
Komponente unter `/usr/libexec/msconnector/lighttpd-stock-sidecar`. Beliebige
Programm- oder argv-Dateipfade und zusätzliche Optionen sind nicht unterstützt.
Er prüft Eigentümer, Berechtigungen und nativen Artefakttyp und führt das Programm
über einen festgehaltenen Deskriptor aus. Der Launcher erstellt
fehlende Spoolverzeichnisse und verwirft unsichere bestehende Pfade ohne Änderung
ihrer Berechtigungen. Konfigurationsverzeichnisse wie `/etc/lighttpd` dürfen 0755
behalten; Spoolverzeichnisse müssen der effektiven UID gehören und 0700 haben.
`--install-root` verlagert den festen Komponentenpfad sowie absolute
Konfigurations- und Spoolpfade für gestufte Installationen. Externe Builds müssen
an diesem festen Komponentenpfad bereitgestellt werden. Regel- und
Ereignispfade im Konfigurationsinhalt sind weiterhin
an die Installation anzupassen.

`--spool-capacity-bytes` verwendet standardmäßig 268435456 (256 MiB) für die
Summe offener, auf Dateisystemblöcke gerundeter Reservierungen pro Prozess.
`--spool-free-reserve-bytes` verwendet standardmäßig 67108864 (64 MiB) für den
unprivilegiert verfügbaren freien Speicher. Dies sind technische Kapazitäten der
Disk-Zulassung, unabhängig von nativer WAF-Body-Policy. Nach P1-Allow prüft die
Zulassung das festgehaltene Dateisystem, allokiert die vollständige deklarierte
Request-Länge mit `posix_fallocate` und prüft den freien Speicher erneut, bevor
ein Body-Chunk an die native Engine gelangt. Fehler liefern 503 und einen
technischen Connector-Ressourcenfehler, niemals ein WAF-BODY_LIMIT-Ereignis.
Es gibt keinen Sparse-Datei-Fallback. Reservierungen bleiben bis zum Schließen
des Deskriptors auf jedem Ausgang bestehen, auch bei Replay, Abbruch und
Receipt-Fehlern. Eine Verzeichnissperre für die Prozesslebensdauer verwirft einen
zweiten Sidecar für dasselbe Verzeichnis. Deadline-Prüfungen vor und nach der
Allokation machen synchrone Aufrufe für reguläre Dateien nicht abbrechbar.

Ein Administrator muss root-eigene, nicht beschreibbare Vorfahren bereitstellen,
bevor ein unprivilegierter Dienst `/var/lib` verwenden kann, beispielsweise mit
`install -d -o root -g root -m 0755 /var/lib/msconnector /var/lib/msconnector/lighttpd-stock`
und anschließend `install -d -o SERVICE_UID -g SERVICE_GID -m 0700 /var/lib/msconnector/lighttpd-stock/safe`
(sowie den weiteren ausgewählten Profilen). Diese Befehle beschreiben die
Erstbereitstellung; bestehende unsichere Pfade dürfen damit nicht implizit
repariert werden. Der Launcher erstellt fehlende Kinder nur dort, wo seine
effektive UID Schreibrechte besitzt; administratorseitig bereitgestellte Pfade
prüft er ohne Rechteerhöhung.
