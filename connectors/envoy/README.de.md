# Envoy-Connector

**Sprache:** [English](README.md) | Deutsch


Status: `minimal_runtime_smoke` / `connector-gap`

Das implementierte Hostmodell ist ein externer HTTP-Autorisierungsdienst für
Envoys `ext_authz`-Filter. Der Connector besitzt das Envoy-Profil und schlanke
Common-SDK-Mapper-Callbacks; die connector-neutrale Engine und der Lebenszyklus
des HTTP-Dienstes bleiben in `common/runtime/`.

Das direkte `ext_authz`-Protokoll ist eine Integration in der Request-Phase.
Es kann begrenzte Request-Header und einen gepufferten Request-Body empfangen
und eine Common-Entscheidung in eine Autorisierungsantwort übersetzen. Allein
stellt `ext_authz` keine Upstream-Response-Header oder Response-Bodies bereit;
das direkte Protokoll ist daher kein P3/P4-fähiger Hostadapter.

Die benannte logische Connectorlösung `envoy-ext-authz` benötigt deshalb den im
[kanonischen Envoy-Guide](../../docs/connectors/envoy.de.md) beschriebenen
privaten MRC1-Response-Companion. Er behält dieselbe lebende Common-/native
Transaktion von abgeschlossenem P2 bis P3/P4, statt einen Request-Snapshot zu
rekonstruieren. Der Observer ist verpflichtend: Sein Weglassen ist ein
Konfigurationsfehler; Observer- oder Korrelationsfehler sind fail-closed. Dies
ist Source-/Component-Wiring mit Status `implemented_not_asserted`, kein
Nachweis, dass eine beliebige Envoy-Deployment die benötigten Templates geladen
hat.

## Separater, nicht hochgestufter `ext_proc`-Hostpfad für den gesamten Lebenszyklus

`ext_proc/` fügt einen separaten Go-Dienst hinzu, der vom Full-Lifecycle-Profil
ausgewählt wird und auf Envoys offiziell generierter Go-Protobuf-/gRPC-API
basiert. Die eingecheckte Envoy-Vorlage verwendet für Request- und
Response-Bodies `STREAMED`-Modi mit begrenzten Zählern pro Stream und
inkrementeller Callback-Auslieferung; sie wählt niemals `BUFFERED`-Verarbeitung.
Der angeheftete Modul- und Envoy-Release-Datensatz steht in `ext_proc/go.mod`,
`ext_proc/go.sum` und `config/envoy-ext-proc-versions.env`.

Der normale `ext_proc`-Build erzeugt eine CGo-Datei, die ein Connector-lokales
ABI mit Common Runtime und libmodsecurity verbindet. Jeder echte Envoy-
`Process`-Stream eröffnet eine Common-Transaktion aus Envoys Request-Headern,
leitet begrenzte inkrementelle Request- und Response-Daten weiter und schließt
sie bei EOS, Cancel oder Prozessorfehler. Commons run-lokales Rohentscheidungs-
JSONL ist die kanonische Ereignisquelle; das payload-freie Stream-Completion-
JSONL ist nur ergänzend.

`runtime-smoke-envoy-ext-proc` validiert das materialisierte YAML, startet
Envoy, den CGo/Common-gRPC-Dienst und einen Upstream und übt anschließend P1,
P2, P3-Deny, P3-Redirect und sicheres P4-Post-Commit-Log-only-Verhalten aus.
Es validiert die rohen Common-Ereignisse und die vom Host bestätigten Aktionen
nach erfolgreichen gRPC-Sends. Dies ist echter lokaler Hostnachweis, bleibt
aber nicht hochgestuft und verändert weder die kanonischen `ext_authz`-
Fähigkeiten noch den Laufzeitstatus. Eine späte P4-Entscheidung in
`minimal`/`safe` wird als hostbestätigtes `log_only` aufgezeichnet; `strict`
Der Service-Decoder kann `late_action_policy: strict` darstellen, aber ein
regelauswertender CGo-Service mit `phase4_mode=strict` weist das Profil
`envoy-ext-proc` beim Start ab, bis eine deterministische Post-Commit-
Hostaktion nachgewiesen ist. Es werden weder eine späte Statusänderung noch
ein deterministischer Reset, Client-Reset oder Upstream-Reset behauptet.

Die genaue ext_proc-API-Grenze, die Opt-in-Beobachtung von Client-Cancel und
die Nichtförderungsbedingungen stehen im
[kanonischen Envoy-Guide](../../docs/connectors/envoy.de.md).

## Quelllayout

- `src/envoy_ext_authz_service_main.c` definiert das Envoy-Hostprofil,
  Original-URI-Header-Präferenzen und den Service-Einstiegspunkt.
- `src/envoy_modsecurity_mapper.c` enthält schlanke C17-Aufrufe an die
  generischen Common-Request- und Response-Mapper.
- `config/envoy-ext-authz.conf` ist die eingecheckte Konfigurationsvorlage.
- `config/prepare_envoy_config.sh` erzeugt außerhalb des Checkouts eine
  konkrete Laufzeitkopie und ersetzt Regel-/Ereignispfade.
- `build/build_connector.sh` führt einen C17-Build nur zum Kompilieren und
  Linken aus.
- `harness/start_envoy_connector.sh` validiert die Envoy-Konfiguration,
  startet und beobachtet Envoy und den Dienst und stoppt beide ohne Request.
- `ext_proc/` enthält den separat baubaren CGo/Common-ext_proc-Streamdienst
  und seine fokussierten Unit-/CGo-Lebenszyklustests;
  `config/envoy-ext-proc-streaming.yaml.in` ist die nicht hochgestufte
  Streaming-Modus-Vorlage.

Die ältere `envoy_bridge`-CLI bleibt ein lokaler Entscheidungs-Selbsttest. Sie
wird nicht vom `ext_authz`-Dienst verwendet und ist kein Laufzeitnachweis.

## Erstellen, konfigurieren und Trennung starten

Stellen Sie lokale libmodsecurity-Pfade direkt oder über das vom Framework verwaltete bereit
Umgebung:

```sh
make -C connectors/envoy build-envoy-connector \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

Das Build-Ziel kompiliert und verknüpft nur. Der Dienst wird nicht ausgeführt oder a
Selbsttest.

Validieren Sie eine konkrete Konfiguration und überschreiben Sie optional die Regeldatei aus der
Befehlszeile:

```sh
make -C connectors/envoy check-envoy-config \
  RULES_FILE=/absolute/path/to/rules.conf
```

Führen Sie den anforderungsfreien Envoy-plus-Service Start Smoke aus:

```sh
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/to/envoy \
  RULES_FILE=/absolute/path/to/rules.conf
```

Führen Sie den echten Envoy-Hostpfad-Smoke mit einer vorbereiteten Envoy-Binärdatei aus:

```sh
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/to/envoy \
  RULES_FILE=/absolute/path/to/rules.conf
```

Dieses Ziel validiert eine generierte temporäre Envoy-Konfiguration, startet den Upstream,
den Connector-Dienst und Envoy und verlangt anschließend ein zulässiges HTTPS 200
sowie ein regelgestütztes `X-Modsec-Smoke: block` HTTPS 403 über einen flüchtigen,
privaten Loopback-TLS-Listener. Der lokale `ext_authz`-Sidecar bleibt ein interner
Loopback-HTTP-Dienst. Fehlende Binärdateien sind GESPERRT; Konfigurations-, Prozess-,
Zuordnungs- und Statusfehler lassen den Smoke fehlschlagen. Alle Prozesse werden bei
Erfolg oder Misserfolg gestoppt.

Für einen vom Bediener gesteuerten Vordergrunddienst:

```sh
make -C connectors/envoy serve-envoy-connector \
  RULES_FILE=/absolute/path/to/rules.conf \
  LISTEN_ADDRESS=127.0.0.1 LISTEN_PORT=18082
```

Die Vorlagenkonfiguration ermöglicht die Anforderungsverarbeitung und verwendet `x-request-id` als Host
Transaktions-ID-Header, begrenzt den Anforderungstext auf 4096 Bytes und deaktiviert den Antworttext
Verarbeitung, verwendet 403/500-Block-/Fehler-Standardwerte, wendet explizite Header/Ereignisse an
begrenzt und schreibt JSONL, das nur Metadaten enthält, außerhalb des Checkouts.

Der unabhängige ext_proc-Volllebenszyklusdienst verfügt über eigene Befehle. Es ist
Eine normale ausführbare Datei erfordert explizite libmodsecurity-Header und Bibliothekspfade:

```sh
make -C connectors/envoy build-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy test-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-runtime-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc \
  ENVOY_BIN=/absolute/path/to/envoy \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

Die reinen Quellen-Go-Tests bleiben für Protobuf- und Transportverhalten nützlich; wann
Die expliziten Pfade werden angegeben, das Build-/Testziel kompiliert die zusätzlich
Gemeinsames Archiv, verknüpft libmodsecurity und führt die getaggten CGo-Lebenszyklustests aus.
Das Laufzeitziel schreibt seine effektive Common-Konfiguration und rohe Common-Ereignisse
unter einem Run-Local-Root. Es liefert aber Connector-lokale Regel-/Aktionsnachweise
fördert keine Fähigkeit und ersetzt keine kanonische Sammlung.

## Aktuelle Beweisgrenze

- Der Dienst ist C17-kompiliert/verifiziert und die gezielte echte Envoy-Anfrage
  Der Pfad hat `minimal_runtime_smoke`-Beweise. Die Überprüfung bleibt bestehen
  `connector-gap` außerhalb dieses engen Bereichs.
- Ein Service-Build oder ein anforderungsfreier Start beweist nicht, dass es sich um eine Envoy-Laufzeitanforderung handelt.
  `runtime-smoke-envoy` übt dabei den ausgewählten `ext_authz`-Hostpfad aus
  `runtime-smoke-envoy-ext-proc` übt das nicht geförderte gesondert aus
  Common/libmodsecurity `ext_proc`-Hostpfad.
- Der ältere Python-Entscheidungsdienst `ext_authz` des Frameworks ist getrennt von
  Dieser Connector ist binär und darf nicht als Beweis für diese Implementierung verwendet werden.
- Keine Produktion, Sicherheit, CRS-vollständig, Vollmatrix, Antwort-Header oder
  Es wird ein Anspruch auf Überprüfung des Antwortkörpers geltend gemacht.
- Der ext_proc-Dienst verfügt über einen isolierten Real-Envoy Common/libmodsecurity-Host
  Beweise für seine begrenzten HTTP/1.1 P1/P2/P3/P4-Probes, einschließlich Raw Common
  Regelentscheidungen und vom Host bestätigte Deny-/Redirect-/Log-Only-Aktionen. Es hat keine
  Timeout, Zurücksetzen, erstes Byte, HTTP/2, Client-Byte-Beobachtung, kanonisch
  Sammler oder Beweismittel zur Fähigkeitsförderung.

## Direkte `ext_authz`-Grenze und logischer Phase-4-Vertrag

Das direkte Envoy-HTTP-`ext_authz`-Protokoll fragt den Autorisierungsdienst vor
der Upstream-Verarbeitung und stellt ihm die spätere Upstream-Response nie zur
Verfügung. In der Legacy-Capability-Tabelle des direkten Protokolls sind
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort` und `late_intervention_status_metadata` daher
`unsupported_by_host_model`, nicht nur ungeprüft. Ein Request-Phase-Allow oder
-Deny, auch ein realer requestseitiger 200 oder 403, ist für dieses direkte
Protokoll kein Response-Phase-Nachweis.

Diese Grenze macht P3/P4 für die vollständige logische Connectorlösung
`envoy-ext-authz` nicht not-applicable. Ihre verpflichtende Kette übergibt die
lebende Common-Transaktion nach P2 von `ext_authz` über einen servererzeugten
opaken Handle an den privaten UDS-`ext_proc`-Response-Observer. Der Observer
claimed den Handle genau einmal, entfernt ihn vor dem Upstream-Request, sendet
P3 vor dem Response-Commit, sendet begrenzte P4-Chunks mit genau einem EOS und
gibt anschließend deterministisch frei oder cancelt. Fehlende, fehlerhafte,
abgelaufene, wiederverwendete oder nicht erreichbare Korrelation ist ein
Konfigurations- oder Protokollfehler und fail-closed vor dem Response-Commit.

Ein gemeinsamer P4-Fall ist damit nur für ein ungepaartes direktes `ext_authz`
`UNSUPPORTED`. Die logische Connectorlösung muss den verpflichtenden Observer
für P3/P4 verwenden oder als fehlkonfiguriert fehlschlagen; sie darf diese
Phasen nie stillschweigend als unsupported bezeichnen. Event-JSONL und Berichte
enthalten keine Response-Body-Nutzlast.
