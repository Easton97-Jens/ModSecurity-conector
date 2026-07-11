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
- Der ältere Framework-Python-Decision-Service ist von diesem Connector-Binary
  getrennt und darf nicht als Evidence dafür gelten.
- Keine Production-, Security-, CRS-Complete-, Full-Matrix-, Response-Header-
  oder Response-Body-Verifikation wird behauptet.

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
