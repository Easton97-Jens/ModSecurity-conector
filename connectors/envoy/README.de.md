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

## Separates, nicht hochgestuftes `ext_proc`-Grundgerüst

`ext_proc/` ergänzt einen separaten Go-Dienst mit Envoys offiziellen generierten
Go-Protobuf-/gRPC-APIs. Seine Envoy-Vorlage verwendet `STREAMED` für Request-
und Response-Bodies, begrenzte Pro-Stream-Zähler und inkrementelle Callbacks;
sie verwendet niemals `BUFFERED`. Das gepinnte Modul und der Envoy-Release sind
in `ext_proc/go.mod`, `ext_proc/go.sum` und
`config/envoy-ext-proc-versions.env` festgelegt.

`runtime-smoke-envoy-ext-proc` liefert zusätzlich einen separaten echten
Envoy-Transport-Smoke: Er validiert die materialisierte YAML, startet Envoy,
den gRPC-Dienst und einen Upstream und schreibt payload-freie Request-/Response-
Streamzähler. `PassthroughEngine` bleibt eine explizite Nahtstelle für eine
spätere Common/libmodsecurity-Anbindung, nicht diese Anbindung selbst. Der
Smoke beweist nur Filterauswahl und Callback-Zustellung; der kanonische
`ext_authz`-Capability- und Runtime-Status bleibt unverändert. Nach beobachteten
Response-Headern notieren `minimal` und `safe` nur `log_only`; `strict` notiert
`strict_abort_not_attempted`.

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
- `ext_proc/` enthält den separat baubaren Go-ext_proc-Stream-Dienst und
  fokussierte Unit-Tests; `config/envoy-ext-proc-streaming.yaml.in` ist seine
  nicht hochgestufte Vorlage im Streaming-Modus.

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

Das unabhängige ext_proc-Grundgerüst verwendet eigene Befehle und benötigt beim
Build noch kein libmodsecurity:

```sh
make -C connectors/envoy build-envoy-ext-proc
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc ENVOY_BIN=/absoluter/pfad/envoy
```

Die ersten vier Befehle kompilieren/testen den gepinnten Go-Quelltext,
validieren dessen Service-JSON und materialisieren YAML außerhalb des Checkouts.
Der Runtime-Target beweist zusätzlich lokale Envoy-zu-ext_proc-Streamzustellung,
aber keine Common-/libmodsecurity-Regelauswertung.

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
  `ext_proc`-Transportpfad testet.
- Der ältere Framework-Python-Decision-Service ist von diesem Connector-Binary
  getrennt und darf nicht als Evidence dafür gelten.
- Keine Production-, Security-, CRS-Complete-, Full-Matrix-, Response-Header-
  oder Response-Body-Verifikation wird behauptet.
- Der ext_proc-Dienst hat einen isolierten echten Envoy-Transport-Smoke mit
  metadata-only Stream-Evidence, aber keine Common/libmodsecurity-, Regelaktion-,
  Timeout-, Reset-, First-Byte-, HTTP/2- oder Capability-Promotion-Evidence.

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
