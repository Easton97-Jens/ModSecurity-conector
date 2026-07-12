# Envoy-ext_proc-Beispiele

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: Envoy ext_proc mit einem repository-eigenen gRPC-Prozessor.
Das [Safe-Template](safe/envoy-ext-proc-streaming.yaml.in) verwendet STREAMED
für Request- und Response-Body. Zusammen mit
[safe/envoy-ext-proc-service.json](safe/envoy-ext-proc-service.json) ist es die
native HTTP/1.1-P1--P4-Safe-Referenz.

P1 sind Request-Header, P2 Request-Body, P3 Response-Header und P4
Response-Body. Safe bedeutet, dass ein spätes P4-Ergebnis als Log-only
aufgezeichnet wird und nicht als später HTTP-Statuswechsel oder
deterministischer Stream-Reset behauptet wird. Das Template verspricht weder
einen vollständigen Connector-Response-Buffer noch ein clientbeobachtetes First
Byte oder einen Strict-Abbruch nach dem Commit. Das
[Strict-Verzeichnis](strict/README.de.md) dokumentiert die optionale Grenze,
ohne ein striktes Transportergebnis zu behaupten.

Das alte [ext_authz-Kompatibilitätsbeispiel](compatibility-ext-authz/README.de.md)
ist ausdrücklich nur für die Request-Phase. Es darf nicht zur Beschreibung von
P3/P4-Abdeckung verwendet werden.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in) | Template | Minimale gestreamte ext_proc-Transportform. |
| [minimal/envoy-ext-proc-service.json](minimal/envoy-ext-proc-service.json) | Service-Konfiguration | Validierte Prozessorlimits für das Minimalprofil. |
| [minimal/msconnector-runtime.conf](minimal/msconnector-runtime.conf) | Runtime-Konfiguration | Common-Runtime-Profil mit `phase4_mode=minimal`. |
| [safe/envoy-ext-proc-streaming.yaml.in](safe/envoy-ext-proc-streaming.yaml.in) | Template | Envoy-Listener, ext_proc-Filter und gRPC-/Upstream-Cluster. |
| [safe/envoy-ext-proc-service.json](safe/envoy-ext-proc-service.json) | Service-Konfiguration | Grenzen und Safe-Late-Action-Policy des Prozessors. |
| [rules/README.de.md](rules/README.de.md) | Dokumentation | No-CRS-Regelquelle und Phasen-IDs. |
| [expected/p1-p4-safe.de.md](expected/p1-p4-safe.de.md) | Dokumentation | Konfigurationsabsicht, keine Run-Evidence. |
| [compatibility-ext-authz/](compatibility-ext-authz/README.de.md) | Kompatibilität | Frühere Request-Authorization-Route. |

Alle obigen Pfade sind ab examples/envoy repository-relativ. Die erzeugte
Runtime-Konfiguration muss außerhalb des Checkouts geschrieben werden.

## Template-Werte und Service-Felder

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| @ENVOY_RELEASE@ | Gepinnter Envoy-Release-String | Im Template-Kommentar Pflicht; Connector-Version-Lock setzt ihn; Materialisierungs-Scope | 1.38.2. Dokumentiert die beabsichtigte API-Version; keine Runtime-Evidence. |
| @LISTEN_PORT@ | Dezimaler TCP-Listener-Port von 1 bis 65535 | Pflicht; Connector-Preparation-Skript setzt ihn; Listener-Scope | 18080. Öffentliche Adresse oder Port verändert die Exponierung. |
| @UPSTREAM_PORT@ | Dezimaler Application-Backend-Port | Pflicht; Connector-Preparation-Skript setzt ihn; Upstream-Cluster | 18081. Nur über den Materialisierungsinput ersetzen. |
| @EXT_PROC_PORT@ | Dezimaler lokaler gRPC-Prozessor-Port | Pflicht; Connector-Preparation-Skript setzt ihn; gRPC-Cluster | 18083. An der vertrauenswürdigen Envoy/Service-Grenze privat halten. |
| @ADMIN_PORT@ | Dezimaler Envoy-Administrationsport | Pflicht; Connector-Preparation-Skript setzt ihn; Admin-Listener | 19001. Admin-Endpunkte nur mit explizitem Sicherheitsdesign exponieren. |
| listen_address | Prozessor-Host:Port-String | Pflicht; explizit in JSON; Prozessor-Scope | 127.0.0.1:18083. Muss zum ext_proc-Cluster-Endpunkt passen. |
| transaction_id_header | HTTP-Headername | Pflicht; explizit in JSON; Transaction-Scope | x-request-id. Korrelationsmetadaten, kein Credential. |
| max_header_count, max_header_name_bytes, max_header_value_bytes, max_total_header_bytes | Positive Metadatenlimits | Pflicht; explizit in JSON; Prozessor-Scope | 128, 256, 8192, 32768. Kleinere Werte lehnen mehr Traffic ab; Limits nicht entfernen. |
| max_body_chunk_bytes, max_request_body_bytes, max_response_body_bytes, max_grpc_message_bytes | Positive Byte-Limits | Pflicht; explizit in JSON; Prozessor-Scope | 1048576, 10485760, 10485760, 1114112. Diese Grenzen bedeuten kein vollständiges Response-Buffering. |
| late_action_policy | Name der Late-P4-Policy | Pflicht; explizit in JSON; Prozessor-Scope | safe. Erlaubt weder synthetischen späten Response-Status noch Reset. |

Die literalen @NAME@-Werte sind Template-Marker, keine Envoy-Felder. Der
Repository-Materializer ersetzt sie und weist ungelöste Marker zurück.

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md)
dokumentiert ext_proc-YAML-Pfade, den Service-JSON-Vertrag, CLI-Flags,
Materializer-Platzhalter und den getrennten ext_authz-Kompatibilitätseintrag.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `envoy.filters.http.ext_proc` | Host / Connector | Sendet den ausgewählten Request-/Response-Lifecycle an den Prozessor. |
| `SecRuleEngine` | ModSecurity Engine | Wählt Engine-Enforcement, DetectionOnly oder Off in der Runtime-Regeldatei. |
| `request_body_mode` | Common Runtime | Wählt die erforderliche gestreamte Request-Body-Eingabe für die native Bridge. |
| `response_body_mode` | Common Runtime | Wählt die erforderliche gestreamte Response-Body-Eingabe für die native Bridge. |
| `late_action_policy` | Connector-Service | Zeichnet minimale, sichere oder strikte Post-Commit-Policy ohne erfundenen Status auf. |

Das Entfernen von `ext_proc` deaktiviert den Connector-Pfad. `SecRuleEngine Off`
lässt die Prozessorroute bestehen, deaktiviert aber die Engine-Regelauswertung.
ext_authz ist nur Kompatibilität und kein P3/P4-Ersatz.

## Validierung

Aus diesem Verzeichnis eine private erzeugte Konfiguration außerhalb des
Checkouts mit dem repository-eigenen Preparation-Skript materialisieren:

~~~sh
sh ../../connectors/envoy/config/prepare_envoy_ext_proc_config.sh
~~~

Das Skript gibt den erzeugten Konfigurationspfad aus. Diese erzeugte Datei mit
dem installierten Envoy-Binary validieren; der Standard liegt unter dem
dokumentierten `$BUILD_ROOT` außerhalb des Checkouts:

~~~sh
envoy --mode validate -c "$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml"
~~~

Erfolgreiche Materialisierung und Syntaxvalidierung beweisen weder P1--P4-
Verhalten noch Safe-Host-Ergebnisse, Strict-Verhalten, Produktionsreife oder
CRS-Abdeckung.

## Verwandtes Material

- [Envoy-Connector-Quellcode und ext_proc-Grenze](../../connectors/envoy/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
