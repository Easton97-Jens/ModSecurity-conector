# Envoy-Connector

**Sprache:** [English](README.md) | Deutsch


Status: `minimal_runtime_smoke` / `connector-gap`

Das implementierte Hostmodell ist ein externer HTTP-Autorisierungsdienst für
Der `ext_authz`-Filter von Envoy. Der Connector besitzt das Envoy-Profil und Thin Common
SDK-Mapper-Rückrufe; die Connector-neutrale Engine und der HTTP-Service-Lebenszyklus
bleiben in `common/runtime/`.

Dies ist eine Integration in der Anfragephase. Es kann begrenzte Anforderungsheader empfangen und
einen gepufferten Anfragetext und übersetzen eine gemeinsame Entscheidung in eine Autorisierung
Antwort. `ext_authz` stellt keine Upstream-Antwortheader oder -Antworten bereit
Stellen für diesen Dienst zur Verfügung, so dass die Reaktionskontrolle weiterhin nicht unterstützt wird und nein
Es wird ein Response-Body-Anspruch erhoben.

## Separater, nicht hochgestufter `ext_proc`-Hostpfad für den gesamten Lebenszyklus

`ext_proc/` fügt einen separaten Go-Dienst hinzu, der vom Profil für den gesamten Lebenszyklus ausgewählt wird.
Basierend auf der offiziell generierten Go-Protobuf/gRPC-API von Envoy. Sein eingecheckter Gesandter
Vorlage verwendet `STREAMED`-Anfrage und
Antwortkörpermodi mit begrenzten Zählern pro Stream und inkrementellem Rückruf
Lieferung; Es wird niemals die `BUFFERED`-Verarbeitung ausgewählt. Das angeheftete Modul und Envoy
Der Release-Datensatz befindet sich in `ext_proc/go.mod`, `ext_proc/go.sum` und
`config/envoy-ext-proc-versions.env`.

Der normale `ext_proc`-Build ist eine ausführbare CGo-Datei, die einen lokalen Connector verknüpft
ABI zu Common Runtime und libmodsecurity. Jeder echte Envoy `Process`-Stream
Öffnet eine gemeinsame Transaktion aus den Anforderungsheadern von Envoy, vorwärts begrenzt
inkrementelle Anforderungs- und Antwortdaten und schließt sie bei EOS, Abbruch oder
Prozessorfehler. Common's Run-Local-Rohentscheidung JSONL ist kanonisch
Ereignisquelle; Das nutzlastfreie Stream-Completion-JSONL ist nur eine Ergänzung.

`runtime-smoke-envoy-ext-proc` validiert das materialisierte YAML, startet Envoy,
der CGo/Common gRPC-Dienst und ein Upstream, dann Übungen P1, P2, P3 verweigern,
P3-Umleitung und P4-sicheres Post-Commit-Nur-Protokollverhalten. Es validiert das Rohmaterial
Allgemeine Ereignisse und die vom Host bestätigten Aktionen nach erfolgreichen gRPC-Versendungen. Dies
ist ein echter lokaler Host-Beweis, bleibt jedoch nicht beworben und ändert sich nicht
die kanonischen `ext_authz`-Funktionen oder den Laufzeitstatus. Eine späte P4-Entscheidung
in `minimal`/`safe` wird als vom Host bestätigtes `log_only` aufgezeichnet; `strict` bleibt bestehen
`strict_abort_not_attempted`. Es wird niemals eine verspätete Statusänderung behauptet,
deterministischer Reset, Client-Reset oder Upstream-Reset.

Die genaue ext_proc-API-Grenze, Opt-in-Client-Abbruchbeobachtung und
Nichtförderungsbedingungen stehen im
[kanonischen Envoy-Guide](../../docs/connectors/envoy.de.md).

## Quelllayout

- `src/envoy_ext_authz_service_main.c` definiert das Envoy-Hostprofil, Original
  URI-Header-Einstellungen und der Service-Einstiegspunkt.
- `src/envoy_modsecurity_mapper.c` enthält dünne C17-Aufrufe an das Common-Generikum
  Anfrage- und Antwort-Mapper.
- `config/envoy-ext-authz.conf` ist die eingecheckte Konfigurationsvorlage.
- `config/prepare_envoy_config.sh` erstellt eine konkrete Laufzeitkopie außerhalb des
  Checkout und ersetzt Regel-/Ereignispfade.
- `build/build_connector.sh` führt einen C17-Build nur zum Kompilieren/Linken durch.
- `harness/start_envoy_connector.sh` validiert die Envoy-Konfiguration, startet und beobachtet
  sowohl Envoy als auch den Dienst und stoppt beide, ohne eine Anfrage zu senden.
- `ext_proc/` enthält den separat erstellbaren CGo/Common ext_proc-Stream
  Service und seine fokussierten Unit-/CGo-Lebenszyklustests;
  `config/envoy-ext-proc-streaming.yaml.in` ist der nicht beworbene Streaming-Modus
  Vorlage.

Die ältere `envoy_bridge`-CLI bleibt ein lokaler Entscheidungsselbsttest. Es wird nicht verwendet
Wird vom `ext_authz`-Dienst bereitgestellt und ist kein Laufzeitbeweis.

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
Connector-Dienst und Envoy erfordern dann ein zulässiges HTTP 200 und ein
Regelgestützter `X-Modsec-Smoke: block` HTTP 403. Fehlende Binärdateien sind GESPERRT;
Konfigurations-, Prozess-, Zuordnungs- und Statusfehler scheitern. Alle Prozesse sind
bei Erfolg oder Misserfolg gestoppt.

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

## Kanonische Phase-4-Grenze

Das ausgewählte Hostmodell ist Envoy HTTP `ext_authz`.  Es fragt nach der Autorisierung
Service vor der Upstream-Verarbeitung und macht niemals die spätere Upstream-Antwort verfügbar
zu diesem Dienst.  `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` sind daher
`unsupported_by_host_model`, nicht nur ungeprüft.

Jeder freigegebene Phase-4-Fall für diese Integration muss `UNSUPPORTED` sein, mit dem
Grund dafür, dass die ausgewählte ext_authz-Integration vor dem Upstream ausgeführt wird
Antwort und legt keine Upstream-Antworttextdaten offen.  Eine Anfragephase
Zulassen oder verweigern, einschließlich einer echten Anfrage-Seite 200 oder 403, ist keine Antwortphase
Beweise.  Der Dienst kann den ursprünglichen Upstream-Status (sichtbarer Client) nicht bereitstellen
Status nach einem späten Eingriff oder einer Post-Commit-Aktion, da kein solcher Host vorhanden ist
Ereignis erreicht es.

`UNSUPPORTED` beschreibt diese gewählte Architektur; es zählt nie als `PASS`.
In Ereignisse oder Berichte wird keine Antworttext-Nutzlast geschrieben.
