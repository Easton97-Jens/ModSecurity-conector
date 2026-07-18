# Traefik-Anschluss

**Sprache:** [English](README.md) | Deutsch


Status: ForwardAuth-Kompatibilitätsrauch plus eine nicht beworbene Host-Probe für native lokale Plugins
Laufzeitstatus: gezielte lokale Traefik/Common-Runtime-Zulassung 200/Block 403
Verifizierungsstatus: not_verified / Connector-Gap

Die ausgewählte Connector-Architektur ist ein externer HTTP-Dienst `forwardAuth`.
`src/traefik_forwardauth_service_main.c` registriert ein Traefik-Hostprofil bei
die connector-neutrale Common Runtime, während `traefik_modsecurity_mapper.c`
Bietet echte Thin-Mapper-Funktionen. Es bleibt der ausgewählte Pfad und tut dies nicht
Herstellung der Produktionsbereitschaft.

Die Repository-Build-Oberflächen kompilieren nur Repository-eigenen und gemeinsam genutzten C-Code
Gemeinsame Helfer:

- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/src/traefik_build_starter.c`
- `connectors/traefik/src/traefik_decision_service.*`
- `connectors/traefik/src/traefik_modsecurity_mapper.*`
- `connectors/traefik/src/traefik_forwardauth_service_main.c`
- `connectors/traefik/native_middleware/` (native lokale Plugin-Hostquelle)
- Gemeinsame Helfer von `common/src/` und `common/include/msconnector/`
- Gemeinsame Laufzeitimplementierung von `common/runtime/`

Der `forwardAuth`-Pfad bleibt der Nur-Anfrage-Kompatibilitätspfad. Die
Repository-eigene Go-Middleware unter `native_middleware/` wird von ausgewählt
`full-lifecycle-traefik-native` über den lokalen Plugin-Arbeitsbereich von Traefik. Es ist
Die isolierte Host-Probe wählt `engineMode: uds`, also eine persistente lokale
Der Common/libmodsecurity-Dienst wird in einer UDS-Sitzung pro Host wiederverwendet
Anfrage. Es zielt auf P1--P4-Beweise auf realen Wirten ab, ändert jedoch nichts daran
Deklaration der eingecheckten Fähigkeit, CRS-Status, sicherer/strikter Status oder Produktion
Bereitschaft. Upstream-Antwortheader und -körper werden in der weiterhin nicht unterstützt
separates `forwardAuth`-Kompatibilitätsprotokoll.

## Persistenter nativer UDS-Engine-Dienst

`src/traefik_engine_service.c` und
`src/traefik_engine_protocol.h` fügt einen dauerhaften lokalen Unix-Domänen-Socket hinzu
Common/libmodsecurity-Dienst für die Yaegi-kompatible Go-Bridge. Es hat
begrenzte Metadaten/Chunk-Frames und explizite Transaktion EOS, Fertigstellen und Zerstören
Operationen. Die native Host-Probe stellt ihren privaten Socket und Run-Local bereit
Ereignispfad; Es zeichnet ein Host-Ergebnis erst nach dem eigentlichen ResponseWriter auf
Aktion gelingt. Nach der Reaktionszusage erfolgt eine P4-disruptive Entscheidung
wird nur als `LOG_ONLY` mit dem tatsächlich sichtbaren Status akzeptiert.

```sh
TRAEFIK_ENGINE_SOCKET_TEST_PARENT=/absolute/private/short-socket-parent \
MODSECURITY_INCLUDE_DIR=/local/include \
MODSECURITY_LIB_DIR=/local/lib \
make -C connectors/traefik test-engine-service
```

Der fokussierte Test startet nur den lokalen Motorservice und ist kein Traefik
Host-Laufzeittest. Siehe den [kanonischen Traefik-Guide](../../docs/connectors/traefik.de.md)
für Lebenszyklus, Konfiguration, kanonische Regelauswahl und Ergebnisgrenzen.
Nur für einen lokalen Sandbox-Test ist `TRAEFIK_ENGINE_SOCKET_TEST_PARENT`
erforderlich und muss einen bestehenden kanonischen, symlinkfreien, dem
aktuellen Benutzer gehörenden `0700`-Elternpfad benennen, dessen vollständige
Vorfahrenkette nicht von einer anderen UID ersetzt werden kann. Ein gruppen-
oder weltbeschreibbarer Vorfahr ist nur zulässig, wenn er sticky ist und der
nächste Kindeintrag der effektiven UID gehört. Dies ändert die Konfiguration
der Host-Probe nicht und besitzt keinen öffentlich beschreibbaren Fallback.

## Native Go-Streaming-Host-Probe (nicht beworben)

`native_middleware/` implementiert Traefik-förmige `CreateConfig`, `New` und
`ServeHTTP`-Einstiegspunkte unter Verwendung der Go `net/http`-Schnittstellen. Seine Antwort
Der Autor behält `Flush`, `Hijack`, `Push`, `ReadFrom` und `Unwrap` bei; es sendet
Begrenzte Anforderungs- und Antwortkörperabschnitte an eine explizite Engine-Naht und niemals
sammelt eine ganze Antwort. Der Quellstandard ist bewusst Pass-Through;
Die isolierte Host-Probe wählt das separat erstellte persistente UDS aus
Common/libmodsecurity-Engine.

Führen Sie nur die lokalen Quellprüfungen aus mit:

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

Diese Befehle kompilieren und testen die Repository-Quelle. Der separate Host
Die Sondenstufen, die unterhalb eines verfügbaren `plugins-local`-Arbeitsbereichs liegen, werden gestartet
Die angeheftete Traefik-Binärdatei erfordert die Ladebestätigung des Plugins und sendet eine
Body-Lager-Anfrage über einen Router, der die Middleware auswählt:

```sh
TRAEFIK_BIN=/absolute/local/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absolute/runtime-root \
TRAEFIK_ENGINE_SOCKET_PARENT=/absolute/private/short-socket-parent \
MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
MSCONNECTOR_RULES_FILE=/absolute/no-crs-baseline.conf \
make -C connectors/traefik runtime-smoke-traefik-native
```

`TRAEFIK_ENGINE_SOCKET_PARENT` ist der private Elternpfad für das kurzlebige
Engine-UDS-Kind der nativen Probe. Der Runner verlangt diesen expliziten Wert
und scheitert vor dem Erzeugen von Host-State, wenn er fehlt oder ungültig ist.
Der ausgewählte Parent muss ein bestehendes
absolutes, dem aktuellen Benutzer gehörendes, exakt mit `0700` privates
Verzeichnis außerhalb des Checkouts ohne Symlink-Komponente und mit einer
vollständigen Vorfahrenkette sein, die UID-übergreifende Ersetzung verhindert.
Ein gruppen- oder weltbeschreibbarer Vorfahr ist nur sicher, wenn er sticky ist
und sein nächster Kindeintrag der effektiven UID gehört; breite Wurzeln wie `/`,
`/tmp`, `/var` und `/var/tmp` erfüllen diesen Vertrag nicht. Steuerzeichen
werden vor der Pfadverarbeitung abgelehnt und die erzeugte YAML serialisiert
den Socket-Pfad als quotierten Skalar. Der zentrale Remaining-Connector-
Dispatcher übergibt nur den exakten Wert des Aufrufers als Prozess-Environment-
Daten, und das native Make-Target bewahrt ihn mit Raw-GNU-Make-Value-Transport
und Export statt mit einem Recipe-Shell-Assignment. Quotes, Semikolons und
Make-Ausdrücke werden daher nicht vor der Python-Validierung ausgewertet. Es
wird kein Parent aus einem Runtime- oder Temporary-Root abgeleitet. Ein CI-
oder direkter Aufrufer muss daher vor dem nativen Target einen ausreichend
kurzen geschützten Parent erzeugen und bereitstellen; ein fehlender Wert ist
eine fail-closed BLOCKED-Voraussetzung und kein Fallback.
Der Runner erzeugt ein eindeutiges privates Kind unter dem ausgewählten Parent,
erzwingt die Socket-Pfadgrenze von
100 Byte vor und nach der Allokation und entfernt dieses Kind nach dem Stoppen
der Host-Prozesse nur dann, wenn es unverändert und leer ist. Die C-Engine
validiert unabhängig denselben Private-Parent- und Vorfahrenketten-Vertrag; sie
stützt sich auf diese Directory-Grenze statt auf eine prozessglobale `umask`
oder eine pfadbasierte Socket-Berechtigungsänderung. Der Engine-Service führt unter Linux vor der
Bereitschaft über den konfigurierten Pfad eine lokale Selbstprüfung aus und
verlangt, dass PID und UID des akzeptierten `SO_PEERCRED`-Peers den
Engine-Prozess bezeichnen. Ein Ersatz nach `bind` innerhalb dieser begrenzten
Pre-Readiness-Capture-Sequenz scheitert damit beim Start, statt als service-
owned erfasst zu werden. Diese Capture bindet spätere Middleware-Dials nicht an
den erfassten Listener: Ein bösartiger Prozess mit derselben UID kann den live
Pfad nach Bereitschaft weiterhin ersetzen; dieser Pfad ist daher keine
Same-UID-Endpoint-Integrity-Grenze. Der Engine-Service prüft beim Cleanup die
erfasste Socket-Identität und meldet einen beobachteten Ersatz als
unvollständiges Cleanup, statt ihn zu entfernen. Ein privates `0700`-
Verzeichnis ist eine UID-übergreifende Grenze, jedoch keine Isolation gegenüber
einem bösartigen Prozess mit derselben UID: POSIX kennt kein atomares
„unlink nur bei dieser Inode“, und auch die Directory-Identity-/Leerheitschecks
des Runners vor `rmdir()` sind nicht atomar. Der Native-Pfadlistener scheitert
auf einer Plattform ohne die erforderliche Linux-Peer-Credential-Primitive
geschlossen. Einen vom Aufrufer ausgewählten Elternpfad oder Socket-Pfad
entfernt der Runner nie; erzeugte Allokationsverzeichnisse entfernt er nur nach
den dokumentierten Checks, nicht unter einer Same-UID-Race-Proof-Garantie.

Die Host-Probe zeichnet nur Metadaten auf, niemals Körper. Mit den kanonischen Regeln
Datei erfordert P1 `200` zulassen, P1 `403` verweigern (Regel `1100001`), P2 `403` verweigern
(`1100101`), P3 Pre-Commit Deny `403` (`1100201`) und P4 Safe/Log-Only mit
sichtbar `200` (`1100301`). P4 streng ist `NOT EXECUTED`. Der Gastgeber bestätigte
JSONL-Datensätze verwenden den Integrationsmodus `native-traefik-middleware` und kanonisch
`transport_result`-Werte `http_status` oder `log_only`. Dieser Beweis ist nicht gültig
Fördern Sie P1–P4, Safe/Strict, First-Byte, No-Full-Buffer, CRS oder Production
Fähigkeiten. Die C `forwardAuth`-Befehle behalten die ausgewählte Kompatibilität bei
Pfad. Die genaue native Transport-/API-Grenze, einschließlich der nicht hochstufenden Grenze
Keep-Alive-Beobachtung und Strict `NOT EXECUTED` Begründung stehen im
[kanonischen Traefik-Guide](../../docs/connectors/traefik.de.md).

## Connector-Service-Build

Der eigentliche Service-Build ist nur kompilierbar/verknüpfbar und erfordert explizites Lokal
libmodsecurity-Pfade:

```sh
MODSECURITY_INCLUDE_DIR=/local/include \
MODSECURITY_LIB_DIR=/local/lib \
make -C connectors/traefik build-connector
```

Build, Konfigurationsvalidierung und Prozessstart sind separate Vorgänge:

```sh
make -C connectors/traefik check-config
make -C connectors/traefik start-smoke
make -C connectors/traefik runtime-smoke
```

`check-config` ruft `--check-config` auf; `start-smoke` ruft `--serve` auf und startet
ein echter lokaler Traefik-Prozess mit einer temporären ForwardAuth-Dateianbieterkonfiguration,
beweist, dass beide Prozesse am Leben bleiben, und stoppt sie, ohne ein zu senden
Anfrage. Keines der Ziele baut den Dienst stillschweigend neu auf.

`runtime-smoke` ist der separate Verkehrsnachweis. Es startet den erstellten Dienst, a
minimaler Upstream und eine lokale Traefik-Binärdatei mit einem temporären Dateianbieter
Konfiguration. Es erfordert eine zulässige Anfrage zur Rückgabe von 200 und
`X-Modsec-Smoke: block`, um 403 über die Common Runtime zurückzugeben. Lokal fehlt
Binärdateien geben Exit 77 zurück; Konfigurations-, Start-, Zuordnungs- oder Statusfehler geben FAIL zurück.

## Globaler Vertrag

Siehe den kanonischen [Connector-Vertrag](../../docs/connectors/README.de.md)
und den [Test-/Evidence-Guide](../../docs/testing-and-evidence.de.md).

## Traefik-spezifischer Staat

- Herkunft/Lizenz: dokumentiert für Repo-eigene Starter; Upstream-Traefik-Quelle nicht ausgewählt
- Metadaten: Repo-eigene Metadaten zur Kompilierungszeit vorhanden
- Build: C17 Common-Runtime-Dienst sowie ältere Starterbefehle vorhanden
- Selbsttest: Starter-Selbsttest des lokalen Entscheidungsdienstes vorhanden
- Harness: bedingter lokaler Traefik-ForwardAuth-Smoke plus ein isolierter Native
  UDS-Host-Prüfung, wenn lokale Traefik- und libmodsecurity-Eingaben verfügbar sind
- Gezielte native No-CRS-Laufzeit: echte lokale P1--P4-sichere Beweise; vollständige Matrix
  und Fähigkeitsförderung nicht ausgeführt
- With-CRS-Laufzeit: nicht ausgeführt
- RESPONSE_BODY-Blockierung: `unsupported_by_host_model` für `forwardAuth`; die
  Die separate native UDS-Probe verfügt nur über nicht geförderte P4-sichere/nur-Protokoll-Beweise

## Erstellen und Selbsttest

Führen Sie den Metadaten-Build-Starter aus mit:

```sh
connectors/traefik/build/build-starter.sh
```

Führen Sie den lokalen Decision-Service-Starter-Selbsttest aus mit:

```sh
make -C connectors/traefik self-test-decision-service
```

Ein erfolgreicher Selbsttest beweist nur die lokale Entscheidungslogik zum Zulassen/Blockieren im Speicher
Anforderungsstrukturen. Es handelt sich nicht um eine Traefik-Laufzeitumgebung, `forwardAuth`, CRS oder
libmodsecurity-Validierung.

## Tests

Es wird kein lokaler Ordner `connectors/traefik/tests` verwendet. Ausführbare Tests sind
Framework-eigene.

Framework-eigene Pfade und Ziele zur Verwendung nach einem echten Traefik-Build und der Nutzung
werden umgesetzt:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Der Starter selbst beansprucht kein No-CRS, With-CRS, RESPONSE_BODY, negativ/
Pass-Through, Audit/Log oder Traefik-Laufzeitergebnis. Das separate native UDS
Die Host-Probe zeichnet nur die gezielten Metadaten-Beweise auf.

## Parallele Laufzeit-Smoke-Phase

Kompatibilitätsziele der Phase 1 sind Traefik `forwardAuth`. Die native Go-Middleware
verfügt über eine separate UDS-Prüfung für den angehefteten Host mit Ausführung der Common/libmodsecurity-Regel;
Für dieses Zielergebnis gibt es keine Laufzeitförderung.

Die connector-spezifische Oberfläche von Traefik ist beschränkt auf:

- Integration und Konfiguration der ForwardAuth-Kompatibilität;
- nativer lokaler Plugin-UDS-Engine-Dienst und Host-Harness;
- Traefik-Smoke-Harness-Einstiegspunkte und lokaler Entscheidungsdienst-Startercode.

Gemeinsame Anfrage, Antwort, Intervention, Status, Protokollierung, Fähigkeiten, Herkunft,
und Transaktionskonzepte stammen von `common/include/msconnector/`. Laufzeitrauch
Beweise werden über `common/scripts/write_smoke_result.py` geschrieben, so Traefik
unterhält keinen eigenen JSON-Ergebnisschreiber.

`make smoke-traefik` liefert den Framework-Common-Smoke-Wrapper, der Quellen enthält
`modules/ModSecurity-test-Framework/ci/lib/common.sh`. Laufzeitabhängigkeiten sind nicht vorhanden
global installiert und der Harness geht nicht davon aus, dass `traefik` im vorhanden ist
global `PATH`.

Die Binärsuche von Traefik verwendet:

1. `TRAEFIK_BIN`;
2. lokale, von common.sh verwaltete Pfade wie `$CONNECTOR_COMPONENT_CACHE`,
   `$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
   `$VERIFIED_RUN_ROOT` und `$SOURCE_ROOT`;
3. Verlassen Sie 77 mit dem Beweis BLOCKED, wenn keine lokale Binärdatei gefunden wird.

Beispiel:

```sh
TRAEFIK_BIN=/lokaler/pfad/traefik make smoke-traefik
```

Lokaler Bereitstellungshelfer:

```sh
make prepare-traefik-runtime
```

Der Helfer bereitet `$CONNECTOR_COMPONENT_CACHE/traefik/bin` vor und meldet
`$CONNECTOR_COMPONENT_CACHE/traefik/bin/traefik`, falls vorhanden. Wenn die Binärdatei ist
fehlt und `ALLOW_RUNTIME_DOWNLOADS=1` nicht gesetzt ist, wird 77 ohne beendet
Traefik installieren oder herunterladen. Mit expliziter Einwilligung wird die Datei heruntergeladen
Angehefteter Linux AMD64-Tarball, überprüft `TRAEFIK_SHA256` und extrahiert nur die
`traefik`-Binärdatei und stellt sie lokal bereit:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
make smoke-traefik
```

Der Standard-Smoke beweist die lokale Traefik-Laufzeit, generierte forwardAuth
Konfiguration, Upstream und einfaches Entscheidungsdienst-200/403-Verhalten. Es ist kein
libmodsecurity-Kompatibilitätsanspruch.

Behalten Sie für den optionalen gezielten, von libmodsecurity unterstützten Smoke den gleichen lokalen Wert bei
Traefik-Binärdatei und wählen Sie das Entscheidungs-Backend libmodsecurity aus:

```sh
DECISION_BACKEND=libmodsecurity make smoke-traefik
make smoke-traefik-modsecurity
```

Dieser Modus löst lokale libmodsecurity-Header/-Bibliotheken aus common.sh-verwaltet auf
Komponenten-Caches oder explizite lokale `MODSECURITY_INCLUDE_DIR` /
`MODSECURITY_LIB_DIR` überschreibt, lädt
`common/rules/modsecurity_targeted_smoke.conf` und Blöcke
`X-Modsec-Smoke: block` mit Regel `1000001`. Fehlende lokale libmodsecurity
Abhängigkeiten erzeugen Exit 77/BLOCKED-Beweise mit
`decision_backend=libmodsecurity` und `modsecurity_backend_verified=false`.

Der minimale CRS-Smoke verwendet dieselbe lokale Traefik-Laufzeitumgebung und libmodsecurity
Backend, schaltet aber den Regelsatz auf CRS um:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-traefik
make smoke-traefik-crs
make smoke-traefik-crs-secondary
```

Die CRS-Quelle der Wahrheit bleibt `common.sh` (`CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR` und `CRS_RUNTIME_DIR`). Der Smoke-Test schreibt einen Connector-Local
CRS-Konfiguration unter `$TRAEFIK_RESULT_ROOT/crs-smoke` sendet ein normales zulässiges Signal
Anfrage und die vorhandene minimale SQLi CRS-Probe
`/?id=1%20UNION%20SELECT%20password%20FROM%20users` und erfordert CRS-Unterstützung
HTTP 403-Beweis. Es darf nur ein erfolgreicher CRS-Nachweis erfolgen
`crs_minimal_smoke_verified=true`; es behält immer noch `crs_complete=false`,
`production_ready=false`, `full_matrix_ready=false` und
`response_body_verified=false`. CRS-Beweise werden ebenfalls kopiert
`$TRAEFIK_RESULT_ROOT/crs-result.json` mit Anmeldungen
`$TRAEFIK_LOG_ROOT/crs-decision.log`.

Der sekundäre CRS-Smoke verwendet denselben CRS-Resolver und Laufzeitpfad wieder
`CRS_SMOKE_CASE=secondary`. Es sendet
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`, schreibt
`$TRAEFIK_RESULT_ROOT/crs-secondary-result.json` und Datensätze
`$TRAEFIK_LOG_ROOT/crs-secondary-decision.log` plus
`$TRAEFIK_LOG_ROOT/crs-secondary-audit.log`. Es darf nur ein PASS gesetzt werden
`crs_secondary_smoke_verified=true` nach dem Extrahieren der eigentlichen CRS-Regel
ID/Nachricht aus Beweismitteln. Wenn CRS, libmodsecurity und Traefik vorhanden sind, aber
Wenn die Sekundärsonde nicht blockiert ist, lautet das Ergebnis FAIL, nicht PASS oder BLOCKED.

Alle CRS-Smoke-Tools mit offenem Anschluss können betrieben werden mit:

```sh
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

Traefik-Quellmetadaten sind in `common.sh` zentralisiert: `TRAEFIK_VERSION=3.7.5`,
die offizielle GitHub-Release-URL, die Installationsdokument-URL, das Linux amd64
Download-URL, `TRAEFIK_SHA256_URL`, und der angeheftete SHA256. Die
maschinenlesbarer Spiegel ist
`modules/ModSecurity-test-Framework/ci/provisioning/runtime-components.manifest.json`.
Downloads werden standardmäßig nicht ausgeführt und, wenn sie aktiviert sind, nur unter bereitgestellt
`$CONNECTOR_COMPONENT_CACHE/traefik`.

Aktuelle Verwendungen fehlender binärer Beweise
`skipped_reason="traefik runtime dependency not available in local common.sh-managed paths"`
und `missing_dependencies=["traefik"]`. Beweise werden angeschrieben
`$VERIFIED_RUN_ROOT/traefik-smoke/`; Wenn `VERIFIED_RUN_ROOT` nicht festgelegt ist, wird die
Fallback ist `$BUILD_ROOT/results/traefik-smoke/`.

Wenn eine lokale Binärdatei aufgelöst wird, kann `make smoke-traefik` PASS erst nach a zurückgeben
Echter HTTP-Smoke beobachtet einen zulässigen Anforderungsstatus von 200 und eine blockierte Anforderung
Status von 403 durch Traefik. Dieser PASS beansprucht immer noch keine Produktion
Bereitschaft, vollständige Matrixbereitschaft, CRS-Vollständigkeit oder Antworttext
Überprüfung. `modsecurity_backend_verified=true` wird nur von der beansprucht
gezielter Smoke-Test von libmodsecurity, wenn im Entscheidungsprotokoll angezeigt wird, dass libmodsecurity geladen ist
die angestrebte Regel und gab die 403-Intervention zurück.

## Status der allgemeinen SDK-Einführung

Dieser Connector ist für das Common SDK vorbereitet, bleibt aber `not_verified` / `connector-gap`.

- Die allgemeine Konfiguration wird über `traefik_modsecurity_config_init()` initialisiert und auf `msconnector_config` abgebildet.
- Request- und Response-Mapper-Verträge verwenden dünne C17-Funktionen in `connectors/traefik/src/traefik_modsecurity_mapper.*`; Inaktive Makro-Aliase werden nicht verwendet.
- Das Diensthostprofil wählt `integration_mode=forwardAuth` aus, bevorzugt `X-Forwarded-Uri` statt `X-Original-Uri` und übergibt die Mapper-Rückrufe an den neutralen HTTP-Autorisierungsdienst.
- Laufzeitentscheidungen nutzen gemeinsame Entscheidungs-/Interventionsmodelle; Der gezielte Smoke überprüft einen Common Blocked-Event-JSONL-Datensatz ohne Body-Payload-Felder.
- Das ausgewählte native Host-Probe setzt den allgemeinen Integrationsmodus auf
  `native-traefik-middleware` sendet Host-Ergebnisse erst nach ResponseWriter
  Bestätigung und behält separate Rohentscheidungs- und Host-Ergebnisereignisse bei.
- Connector-spezifischer Code bleibt für das Hostprofil, den Build-Glue, die Beispielkonfiguration und den Prozesseinstiegspunkt verantwortlich.
- Die Antwortzuordnung ist nur zur Vertragsprüfung verknüpft. Die Upstream-Antwortinspektion wird von `forwardAuth` nicht unterstützt.
- Es wird keine Produktions-, CRS-vollständige, vollständige Matrix-, breite Laufzeit- oder RESPONSE_BODY-Verifizierung beansprucht.

## Kompatibilität und native Phase-4-Grenze

Das Kompatibilitätshostmodell ist Traefik `forwardAuth`. Es wird vorher ausgeführt
Upstream-Handhabung und kann den späteren Upstream-Antworttext nicht überprüfen.
Folglich gilt für diesen Kompatibilitätspfad:
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` sind
`unsupported_by_host_model`, nicht nur bei einem lokalen Lauf nicht vorhanden.

Die separat ausgewählte native UDS-Probe beobachtet die Upstream-Antwort. Es
hat gezielte Beweise für eine P3-Pre-Commit-Ablehnung und eine P4-Post-Commit-Verweigerung
`log_only`-Ergebnis mit ursprünglichen und sichtbaren Statusmetadaten. Es kann nicht bewiesen werden
eine späte Abtreibung; streng P4 ist `NOT EXECUTED`. Keiner der Pfade ändert eine Fähigkeit
Staat ohne den separaten kanonischen Beweis-/Beförderungsprozess.

In ein Ereignis oder einen Bericht gehört keine Antworttext-Nutzlast.
