# Envoy-Connector

**Sprache:** [English](README.md) | Deutsch

Status: `minimal_runtime_smoke` / `connector-gap`

Das implementierte Hostmodell ist ein externer HTTP-Autorisierungsdienst für
Envoys `ext_authz`-Filter. Der Connector besitzt das Envoy-Hostprofil und dünne
Common-SDK-Mapper-Callbacks; Engine und HTTP-Service-Lifecycle bleiben
connector-neutral unter `common/runtime/`.

Dies ist eine Request-Phasen-Integration. Sie kann begrenzte Request-Header und
einen gepufferten Request-Body empfangen und eine Common-Entscheidung in eine
Autorisierungsantwort übertragen. `ext_authz` liefert dem Dienst keine
Upstream-Response-Header oder -Bodies. Response-Inspektion bleibt deshalb
nicht unterstützt und es wird kein Response-Body-Claim erhoben.

## Separater, nicht hochgestufter `ext_proc`-Full-Lifecycle-Hostpfad

`ext_proc/` ergänzt einen vom Full-Lifecycle-Profil ausgewählten separaten
Go-Dienst mit Envoys offiziellen generierten Go-Protobuf-/gRPC-APIs. Seine
Envoy-Vorlage verwendet `STREAMED` für Request-
und Response-Bodies, begrenzte Pro-Stream-Zähler und inkrementelle Callbacks;
sie verwendet niemals `BUFFERED`. Das gepinnte Modul und der Envoy-Release sind
in `ext_proc/go.mod`, `ext_proc/go.sum` und
`config/envoy-ext-proc-versions.env` festgelegt.

Der normale `ext_proc`-Build erzeugt ein CGo-Binary, das eine connector-lokale
ABI mit Common Runtime und libmodsecurity verlinkt. Jeder echte Envoy-`Process`-
Stream öffnet aus den Envoy-Request-Headern eine Common-Transaction, übergibt
begrenzte inkrementelle Request-/Response-Daten und schließt sie bei EOS,
Abbruch oder Processor-Fehler. Das run-lokale rohe Common-Decision-JSONL ist
die kanonische Ereignisquelle; das payload-freie Stream-Completion-JSONL ist
nur ergänzend.

`runtime-smoke-envoy-ext-proc` validiert die materialisierte YAML, startet
Envoy, den CGo/Common-gRPC-Dienst und einen Upstream und testet P1, P2, P3
Deny, P3 Redirect sowie P4 Safe nach Commit als `log_only`. Er validiert rohe
Common-Ereignisse und erst nach erfolgreichem gRPC-Senden bestätigte
Host-Aktionen. Das ist echte lokale Host-Evidence, bleibt aber nicht
hochgestuft und ändert weder die kanonischen `ext_authz`-Capabilities noch
deren Runtime-Status. Eine späte P4-Entscheidung in `minimal`/`safe` wird als
host-bestätigtes `log_only` notiert; `strict` bleibt
`strict_abort_not_attempted`. Es wird kein später Statuswechsel,
deterministischer Reset, Client-Reset oder Upstream-Reset behauptet.

## Quellstruktur

- `src/envoy_ext_authz_service_main.c` definiert Hostprofil,
  URI-Header-Präferenzen und Service-Einstiegspunkt.
- `src/envoy_modsecurity_mapper.c` enthält dünne C17-Aufrufe der generischen
  Common-Request-/Response-Mapper.
- `config/envoy-ext-authz.conf` ist die eingecheckte Config-Vorlage.
- `config/prepare_envoy_config.sh` erzeugt außerhalb des Checkouts eine konkrete
  Laufzeit-Config und ersetzt Regel-/Eventpfade.
- `build/build_connector.sh` ist ein reiner C17-Compile-/Link-Build.
- `harness/start_envoy_connector.sh` validiert die Envoy-Config, startet Envoy
  und Connector-Dienst und stoppt beide ohne Request.
- `ext_proc/` enthält den separat baubaren CGo/Common-ext_proc-Stream-Dienst
  und fokussierte Unit-/CGo-Lifecycle-Tests;
  `config/envoy-ext-proc-streaming.yaml.in` ist seine nicht hochgestufte
  Streaming-Vorlage.

Die ältere `envoy_bridge`-CLI bleibt ein lokaler Decision-Self-Test. Sie wird
vom `ext_authz`-Dienst nicht verwendet und ist keine Runtime-Evidence.

## Getrennte Build-, Config- und Startpfade

```sh
make -C connectors/envoy build-envoy-connector \
  MODSECURITY_INCLUDE_DIR=/absolutes/praefix/include \
  MODSECURITY_LIB_DIR=/absolutes/praefix/lib

make -C connectors/envoy check-envoy-config \
  RULES_FILE=/absoluter/pfad/regeln.conf

make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absoluter/pfad/envoy \
  RULES_FILE=/absoluter/pfad/regeln.conf

make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absoluter/pfad/envoy \
  RULES_FILE=/absoluter/pfad/regeln.conf
```

Der Build führt weder Service noch Self-Test aus. Die Vorlage aktiviert
Request-Verarbeitung, verwendet `x-request-id` als Host-Transaction-ID-Header,
begrenzt Request-Bodies auf 4096 Bytes, deaktiviert Response-Body-Verarbeitung,
verwendet 403/500 als Block-/Fehlerstatus und schreibt metadaten-only JSONL
außerhalb des Checkouts.

Der unabhängige ext_proc-Full-Lifecycle-Dienst verwendet eigene Befehle. Sein
normales Binary benötigt explizite libmodsecurity-Header- und Bibliothekspfade:

```sh
make -C connectors/envoy build-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolutes/praefix/include \
  MODSECURITY_LIB_DIR=/absolutes/praefix/lib
make -C connectors/envoy test-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolutes/praefix/include \
  MODSECURITY_LIB_DIR=/absolutes/praefix/lib
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-runtime-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc \
  ENVOY_BIN=/absoluter/pfad/envoy \
  MODSECURITY_INCLUDE_DIR=/absolutes/praefix/include \
  MODSECURITY_LIB_DIR=/absolutes/praefix/lib
```

Die source-only Go-Tests bleiben für Protobuf- und Transportverhalten nützlich;
mit den expliziten Pfaden kompiliert und testet der Build/Test-Target zusätzlich
das Common-Archiv, verlinkt libmodsecurity und führt die getaggten CGo-
Lifecycle-Tests aus. Der Runtime-Target schreibt seine effektive Common-Config
und rohe Common-Ereignisse unter einen run-lokalen Root. Er liefert
connector-lokale Regel-/Action-Evidence, aber keine Capability-Hochstufung und
keinen Ersatz für kanonische Collection.

Der Runtime-Smoke validiert eine temporäre Envoy-Config, startet Upstream,
Connector-Dienst und Envoy und verlangt HTTP 200 für den erlaubten Request sowie
einen regelbasierten HTTP 403 für `X-Modsec-Smoke: block`. Fehlende Binärdateien
sind BLOCKED; Config-, Prozess-, Mapping- und Statusfehler führen zu FAIL. Alle
Prozesse werden bei Erfolg und Fehler beendet.

## Aktuelle Evidence-Grenze

- Der Dienst ist mit C17 compile-/link-verifiziert und der gezielte echte
  Envoy-Requestpfad besitzt `minimal_runtime_smoke`-Evidence. Außerhalb dieses
  engen Scopes bleibt die Verifikation `connector-gap`.
- Build oder request-freier Start beweisen keinen Envoy-Runtime-Request.
  `runtime-smoke-envoy` testet den ausgewählten `ext_authz`-Hostpfad, während
  `runtime-smoke-envoy-ext-proc` separat den nicht hochgestuften
  Common/libmodsecurity-`ext_proc`-Hostpfad testet.
- Der ältere Framework-Python-Decision-Service ist von diesem Connector-Binary
  getrennt und darf nicht als Evidence dafür gelten.
- Keine Production-, Security-, CRS-Complete-, Full-Matrix-, Response-Header-
  oder Response-Body-Verifikation wird behauptet.
- Der ext_proc-Dienst hat isolierte echte Envoy/Common/libmodsecurity-
  Host-Evidence für begrenzte HTTP/1.1-P1/P2/P3/P4-Probes einschließlich roher
  Common-Regelentscheidungen und host-bestätigter Deny-/Redirect-/Log-only-
  Actions. Es gibt keine Timeout-, Reset-, First-Byte-, HTTP/2-, Client-Byte-,
  kanonische-Collector- oder Capability-Promotion-Evidence.

## Kanonische Grenze für Phase 4

Das gewählte Host-Modell ist Envoy HTTP `ext_authz`. Es fragt den
Autorisierungsdienst vor der Upstream-Verarbeitung und stellt diesem Dienst die
spätere Upstream-Antwort niemals bereit. Deshalb sind
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` als `unsupported_by_host_model` und nicht
lediglich als unbelegt deklariert.

Jeder gemeinsame Phase-4-Fall für diese Integration muss `UNSUPPORTED` sein:
Die ausgewählte ext_authz-Integration wird vor der Upstream-Antwort ausgeführt
und stellt keine Upstream-Response-Body-Daten bereit. Eine Request-Phase-
Freigabe oder -Sperre, auch ein echter requestseitiger Status 200 oder 403, ist
kein Response-Phase-Nachweis. Der Dienst kann weder ursprünglichen
Upstream-Status noch sichtbaren Client-Status nach einer späten Intervention
oder eine Aktion nach dem Commit liefern, weil ihn kein solches Host-Ereignis
erreicht.

`UNSUPPORTED` beschreibt diese gewählte Architektur und zählt nie als `PASS`.
Response-Body-Payloads werden nicht in Ereignisse oder Berichte geschrieben.
