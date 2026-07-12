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
[Strict-Profilgrenze](#strict-profilgrenze) dokumentiert die optionale Grenze,
ohne ein striktes Transportergebnis zu behaupten.

Das [ext_authz-Kompatibilitätsbeispiel](#ext_authz-kompatibilität) ist
ausdrücklich nur für die Request-Phase. Es darf nicht zur Beschreibung von
P3/P4-Abdeckung verwendet werden.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in) | Template | Minimale gestreamte ext_proc-Transportform. |
| [minimal/envoy-ext-proc-service.json](minimal/envoy-ext-proc-service.json) | Service-Konfiguration | Validierte Prozessorlimits für das Minimalprofil. |
| [minimal/msconnector-runtime.conf](minimal/msconnector-runtime.conf) | Runtime-Konfiguration | Common-Runtime-Profil mit `phase4_mode=minimal`. |
| [safe/envoy-ext-proc-streaming.yaml.in](safe/envoy-ext-proc-streaming.yaml.in) | Template | Envoy-Listener, ext_proc-Filter und gRPC-/Upstream-Cluster. |
| [safe/envoy-ext-proc-service.json](safe/envoy-ext-proc-service.json) | Service-Konfiguration | Grenzen und Safe-Late-Action-Policy des Prozessors. |
| [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Runtime-Konfiguration | DetectionOnly-Regeln mit dem ausgewählten ext_proc-Transport; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/msconnector-runtime.conf](disabled/msconnector-runtime.conf) | Runtime-Konfiguration | Runtime deaktiviert, Host-YAML bleibt transportorientiert; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | No-CRS-Regelquelle und Phasen-IDs. |
| [P1--P4-Safe-Absicht](#p1-p4-safe-absicht) | Dokumentation | Konfigurationsabsicht, keine Run-Evidence. |
| [Minimale ext_proc-Referenz](#minimale-ext_proc-referenz) | Dokumentation | Vollständige minimale gestreamte Transportform. |
| [ext_authz-Kompatibilität](#ext_authz-kompatibilität) | Kompatibilität | Frühere Request-Authorization-Route. |

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

## Profile

### DetectionOnly-Profil

`detection-only/msconnector-runtime.conf` wird mit dem ausgewählten ext_proc-
YAML verwendet und wählt DetectionOnly-Regeln. DetectionOnly lädt und bewertet
Engine-Regeln und zeichnet Treffer auf, führt aber keine disruptiven Engine-
Aktionen aus.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/msconnector-runtime.conf` setzt `enabled=off`; Host-YAML bleibt eine
getrennte ext_proc-Transportkonfiguration. Dies unterscheidet sich von
`SecRuleEngine Off`, das bei aktivem Hostconnector die Regelauswertung
innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Safe-Absicht

Die ext_proc-Referenz setzt beide Body-Modi auf STREAMED und die Service-Policy
auf safe. Sie ist die native Full-Lifecycle-Referenz. Ein P4-Ergebnis nach dem
Start der Response wird als Safe-Log-only dargestellt, nicht als behaupteter
später HTTP-Statuswechsel oder deterministischer Stream-Reset.

Die separate ext_authz-Konfiguration kann weder Upstream-Response-Header noch
-Bodies sehen und wird deshalb absichtlich nicht als P3/P4-Kernpfad
beschrieben. Es gibt kein Strict-Beispiel.

## No-CRS-Regeln

Der ext_proc-Service lädt die geprüfte installierte Regeldatei aus seiner
Runtime-Konfiguration. Die Repositoryquelle für das No-CRS-Profil ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

## Minimale ext_proc-Referenz

Der ausgewählte Envoy-Kern benötigt gestreamte ext_proc-Eingaben in beiden
Richtungen. Die Minimaldateien liefern eine vollständige Transportform in
[envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in),
ihren validierten Service-Vertrag und eine passende Common-Runtime-Datei mit
`phase4_mode=minimal`. Es ist kein nativer Request-only-Pfad: Die Bridge
benötigt weiterhin STREAMED-Request- und Response-Body-Modi. Das getrennte
[ext_authz-Request-only-Material](#ext_authz-kompatibilität) bleibt
Kompatibilitätsmaterial.

## ext_authz-Kompatibilität

Die bewahrte Datei ist das frühere Envoy-Request-Phasen-Beispiel. Sie
konfiguriert einen HTTP-ext_authz-Aufruf vor dem Routing zum Upstream und bleibt
vom gestreamten ext_proc-Kern unter [safe/](safe/) getrennt.

### Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- |
| Listener-Socket-Adresse und port_value | TCP-Listener-Adresse und dezimaler Port | Pflicht; YAML static resources; Listener-Scope | 0.0.0.0:8080. Für lokale Übungen Loopback binden, sofern keine Freigabe beabsichtigt ist. |
| modsecurity_authz | ext_authz-Clustername | Pflicht; YAML-Cluster und Filter; Filter-Scope | Endpunkt 127.0.0.1:9000. Muss ein vertrauenswürdiger Authorization-Service sein. |
| server_uri und timeout | Authorization-HTTP-URI und positive Dauer | Pflicht; ext_authz-Filter; Request-Scope | http://127.0.0.1:9000 und 0.2s. Ein Timeout ist keine Response-Phasen-Evidence. |
| authorization und content-type | Erlaubte Request-Headernamen | Optionaler Filter-Allow-List; Request-Scope | Nur Headernamen, keine Geheimwerte. Keine Credentials in diese Datei schreiben. |
| app_backend | Upstream-Clustername und Endpunkt | Pflicht; Route und Cluster; Route-Scope | 127.0.0.1:8081. Durch gewünschten Application-Endpunkt ersetzen. |

Die [ext_authz-Konfiguration](compatibility-ext-authz/envoy-ext-authz.yaml)
macht die spätere Upstream-Response diesem Service nicht zugänglich. Sie ist
keine P3/P4-, Safe-Late-Intervention-, Strict-, First-Byte- oder
No-Buffer-Evidence.

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

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Der ext_proc-Service akzeptiert `late_action_policy: strict`, zeichnet nach
der Commit-Grenze aber aktuell `strict_abort_not_attempted` auf. Strict ist
optional und es wird keine Late-Reset-Konfiguration behauptet.

Safe-ext_proc-Template und Service-Vertrag verwenden, generiertes YAML und
Service-JSON validieren und Host-Evidenz ergänzen, bevor auf ein striktes
Transportergebnis vertraut wird.

## Verwandtes Material

- [Envoy-Connector-Quellcode und ext_proc-Grenze](../../connectors/envoy/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
