# Envoy Connector-Architektur

**Sprache:** [English](architecture.md) | Deutsch

Status: Der angestrebte ext_authz-Anforderungspfad ist `minimal_runtime_smoke` /
`connector-gap`. Der separate ext_proc-Pfad verfügt über Connector-Local Real-Envoy
Common/libmodsecurity-Hostbeweise, aber keine Leistungsförderung.

## Ausgewähltes Hostmodell

Der ausgewählte, kanonische Connector-Pfad implementiert das externe HTTP von Envoy
`ext_authz`-Modell. Gesandter sendet
Anfragemetadaten, ausgewählte Header und eine optionale begrenzte gepufferte Anfrage
Körper zu einem Connector-eigenen Dienst. Es werden keine Envoy-SDK-Typen in Common übernommen.

`src/envoy_ext_authz_service_main.c` besitzt das Envoy-spezifische Profil:

- Connector-Name `envoy`;
- Integrationsmodus `ext_authz`;
- Einstellungen für Original-URI-Header;
- Request- und Response-Mapper-Rückrufe.

`src/envoy_modsecurity_mapper.c` ist ein dünner C17-Adapter gegenüber dem Common-Generikum
Mapper. `common/runtime` ist Eigentümer der Konfigurationsanalyse und -validierung sowie der Ressource/des Körpers
Grenzwerte, Regelladen, libmodsecurity-Engine/Transaktionslebenszyklus, Transaktion
IDs, Entscheidungs-/Aktionszuordnung und Nur-Metadaten-Ereignis-JSONL.

## Anforderungsablauf

```text
client -> Envoy HTTP connection manager -> ext_authz HTTP request
       -> msconnector_envoy_ext_authz -> Common mapper/runtime
       -> libmodsecurity decision -> ext_authz allow/deny
       -> upstream or local 403
```

Die eingecheckte Envoy Smoke-Konfiguration leitet `content-length`, `content-type`,
`x-modsec-smoke` und `x-request-id`; puffert höchstens 4096 Anforderungsbytes und tut dies auch
Teilkörper sind nicht zulässig. Die Connector-Konfiguration erzwingt unabhängig voneinander Header, Body,
Ereignis- und Transaktionsbeschränkungen.

## Antwortgrenze

HTTP `ext_authz` wird vor dem Upstream-Routing ausgeführt. Es kann nicht überprüft werden
Upstream-Antwort. Der Antwort-Mapper ist verknüpft und vertragsgeprüft für die API
Der Vollständigkeit halber, aber Antwortheader und -körper werden in diesem Host nicht unterstützt
Modell. Eine spätere Implementierung in der Reaktionsphase würde einen gesonderten Nachweis erfordern
Modell wie `ext_proc`; es darf nicht aus diesem Anschluss abgeleitet werden.

## Separate ext_proc Common-Runtime-Grenze

`ext_proc/cmd/msconnector-envoy-ext-proc` implementiert das offizielle Go
`ExternalProcessor` gRPC-Dienst mit einem `streamState` pro `Process`-Stream.
Der normale CGo-Build wählt `CommonRuntimeEngine` aus, dessen Connector-lokaler C-ABI
Öffnet eine echte Common/libmodsecurity-Transaktion aus der tatsächlichen Envoy-Anfrage
Kopfzeilen. `config/envoy-ext-proc-streaming.yaml.in` wählt die `STREAMED`-Anfrage aus
und Antwortkörpermodi. Der Go-Adapter begrenzt Header/Chunks/Summen vorwärts
jeden Block sofort und behält nur Zähler. Es ordnet die vom Envoy angeforderten Karten zu
Protokoll- und Endpunktattribute, anstatt die gRPC-Peer-Adresse zu erfinden.
EOS, gRPC-Abbruch, Prozessorausfall und ordnungsgemäßes Herunterfahren bereinigen das
native Transaktion. Envoy-spezifische Protobuf-Typen bleiben unten
`connectors/envoy/ext_proc`; Keine werden zu `common/` hinzugefügt.Raw Common Decision JSONL wird in einen Ereignispfad pro Lauf geschrieben und ist der
kanonischer Anschluss – lokale Beweisquelle. Das separate Abschlussprotokoll enthält
nur Stream-Metadaten. Störende P1/P2/P3-Entscheidungen vor der Festschreibung bilden eine
`ImmediateResponse`; Das Common-Host-Ergebnis wird erst nach dem aufgezeichnet
Der passende gRPC-Versand ist erfolgreich. Ein erfolgreicher Antwort-Header `CONTINUE` ist der
Konservative Commit-Grenze des Adapters. Eine späte P4-Entscheidung in `minimal`/`safe`
wird als `log_only` aufgezeichnet; `strict` zeichnet `strict_abort_not_attempted` auf. A
Ein gRPC-Fehler wird nicht als Stream-Reset dargestellt und ein Abbruch auch nicht
wird dem Kunden gegenüber dem Upstream zugeschrieben.

`runtime-smoke-envoy-ext-proc` validiert das generierte YAML mit echtem Envoy und
Führt lokalen HTTP/1.1 P1/P2/P3/P4-Verkehr durch. Es überprüft rohe Common-Regelereignisse
und vom Host bestätigte Ablehnungs-, Umleitungs- und sichere Nur-Protokoll-Ergebnisse. Es beweist es nicht
Timeout-/Reset-Semantik, First-Byte- oder Client-Byte-Verhalten, HTTP/2-Verhalten,
kanonische Ergebnissammlung oder eine geförderte Antwortkörperfunktion.

## Lebenszyklus und Beweise

- `build-envoy-connector`: Nur kompilieren/verknüpfen.
- `check-envoy-config`: Konfiguration laden, Laufzeit/Regeln initialisieren, dann bereinigen.
- `start-smoke-envoy`: Envoy plus Connector-Dienst validieren und starten/stoppen
  ohne Anfragen.
- `runtime-smoke-envoy`: echter Envoy 200/403-Anforderungspfad mit sauberem Herunterfahren.
- `build-envoy-ext-proc`, `test-envoy-ext-proc` und
  `check-envoy-ext-proc-config`: Go-Source-/Build-/Config-Gates angepinnt; mit
  libmodsecurity-Pfade führt das Build-/Testziel auch die CGo Common Bridge aus.
- `runtime-smoke-envoy-ext-proc`: echter Envoy ext_proc/Common/libmodsecurity
  Host-Smoke-Test, explizit gekennzeichnet als `common_libmodsecurity_nonpromoted`.

Der alte `envoy_bridge` dient weiterhin nur dem Selbsttest und ist nicht Teil dieses Ablaufs.
