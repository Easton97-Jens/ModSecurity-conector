# Envoy-Beispiele

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

`ext_proc` verwendet den repository-eigenen gRPC-Prozessor. `ext_authz`
benötigt zusätzlich seinen privaten UDS-Response-Observer. Beide logischen
Lösungen besitzen vollständige Bündel für die vier Beispielvarianten.

## Vollständige logische Profilmatrix

| Logische Lösung | Off | Safe | Strict | All | P1/P2 | P3/P4 |
| --- | --- | --- | --- | --- | --- | --- |
| ext_proc | [Bündel](ext-proc/off/) | [Bündel](ext-proc/safe/) | [Bündel](ext-proc/strict/) | [Bündel](ext-proc/all/) | ext_proc | ext_proc |
| ext_authz | [Bündel](ext-authz/off/) | [Bündel](ext-authz/safe/) | [Bündel](ext-authz/strict/) | [Bündel](ext-authz/all/) | ext_authz | Privater UDS-ext_proc-Observer |

Der ext_authz-Observer beansprucht ein einmaliges undurchsichtiges Handle für
die Response-Verarbeitung. Fehlende, abgelaufene oder abweichende Handles
werden fail-closed behandelt. Der Harness legt seinen Socket in einem privaten,
nur dem Eigentümer zugänglichen Runtime-Verzeichnis ab. Der Quelltext-Default
ist `/run/modsecurity/envoy-ext-authz-companion.sock`. Der Observer entfernt
`x-msconnector-response-handle` vor dem Upstream-Routing.

## Dateien

Das eigenständige [Safe-Template](safe/envoy-ext-proc-streaming.yaml.in) und
[Service-JSON](safe/envoy-ext-proc-service.json) bilden die ext_proc-Referenz
für die folgenden Validierungsbefehle. Das [Off-Template](off/envoy-ext-proc-streaming.yaml.in),
[Service-JSON](off/envoy-ext-proc-service.json) und die
[Runtime-Datei](off/msconnector-runtime.conf) bilden ihr Off-Gegenstück.

### DetectionOnly-Profil

[detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf)
mit dem gewählten ext_proc-YAML verwenden. Die [Regeln](rules/detection-only.conf)
bewerten und protokollieren Treffer bei deaktivierten disruptiven Engine-Aktionen.

### Deaktiviertes Profil

[disabled/msconnector-runtime.conf](disabled/msconnector-runtime.conf) setzt
`enabled=off`. Das YAML beschreibt weiterhin den Transport. Dagegen lassen
[Engine-Off-Regeln](rules/engine-off.conf) den Connector bei deaktivierter
Engine-Regelauswertung aktiv.

## Template-Werte und Service-Felder

Listener-, Upstream-, Prozessor- und Administrationsendpunkte, installierte
Regelpfade sowie private Runtime-/Logpfade anpassen. Prozessor- und
Admin-Endpunkte innerhalb ihrer vertrauenswürdigen Service-Grenze halten.
`listen_address` des Prozessors muss zum ext_proc-Cluster passen. Der
Repository-Materializer ersetzt Template-Marker und weist ungelöste Marker ab.

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md) beschreibt
YAML-Felder, Service-JSON, CLI-Flags, Template-Marker und einzelne
Header-/Chunk-/gRPC-Nachrichtenlimits. Kumulative Body-Inspektionslimits und
Aktionen in Engine-Regeln gemäß [Konfiguration](../../docs/configuration.de.md)
festlegen.

## P1--P4-Safe-Absicht

Die HTTP/1.1-ext_proc-Referenz verwendet STREAMED für Request- und Response-Body.
Safe protokolliert eine P4-Entscheidung nach Beginn der Response-Ausgabe als
Log-only. Eine Konfigurationsdatei belegt die Konfigurationsabsicht.
Clientbeobachtbares Verhalten benötigt einen passenden Hostlauf.

## Off-ext_proc-Referenz

`phase4_mode=off` bewahrt native Interventions- und Fehlerbehandlung bei
deaktivierter zusätzlicher Late-Policy. Beide Body-Richtungen benötigen
weiterhin STREAMED-Eingaben. `all` wählt einen echten Policy-Wert wie `strict`.

## No-CRS-Regeln

Eine geprüfte Regeldatei installieren und in der Runtime-Konfiguration wählen.
Die [No-CRS-Baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
ist die Quelle des Repository-Testprofils. Phasen-IDs und Engine-Modi erläutern
die [Beispielübersicht](../README.de.md) und [Regelbeispiele](../common/rule-examples.de.md).

## ext_authz-Kompatibilität

Das ältere [HTTP-ext_authz-Beispiel](compatibility-ext-authz/envoy-ext-authz.yaml)
autorisiert ausschließlich Requests. Listener, vertrauenswürdigen
Authorization-Service, Timeout, Header-Allow-List und Application-Upstream
anpassen. Für Response-Prüfung die vollständigen `ext-authz/`-Bündel oben verwenden.

## Validierung

Aus `examples/envoy` einen absoluten beschreibbaren externen `BUILD_ROOT` und
das Repository-Preparation-Skript verwenden. OpenSSL erzeugt private eintägige
Loopback-Test-Credentials für dieses Beispiel.

~~~sh
export TLS_CERTIFICATE="$BUILD_ROOT/envoy-ext-proc/runtime-smoke/envoy-loopback.crt"
export TLS_PRIVATE_KEY="$BUILD_ROOT/envoy-ext-proc/runtime-smoke/envoy-loopback.key"
umask 077
mkdir -p "$(dirname "$TLS_CERTIFICATE")"
openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 1 \
  -subj /CN=127.0.0.1 -addext subjectAltName=IP:127.0.0.1 \
  -keyout "$TLS_PRIVATE_KEY" -out "$TLS_CERTIFICATE"
TEMPLATE="$PWD/safe/envoy-ext-proc-streaming.yaml.in" \
  TLS_CERTIFICATE="$TLS_CERTIFICATE" TLS_PRIVATE_KEY="$TLS_PRIVATE_KEY" \
  sh ../../connectors/envoy/config/prepare_envoy_ext_proc_config.sh
~~~

Das Skript gibt den erzeugten Konfigurationspfad aus. Mit dem installierten
Envoy-Binary den folgenden Default-Ausgabepfad prüfen oder bei einer
Überschreibung den tatsächlich ausgegebenen Pfad verwenden.

~~~sh
envoy --mode validate -c "$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml"
~~~

Materialisierung und Syntaxprüfung belegen Dateivorbereitung und Host-Laden.
Die [Testanleitung](../../docs/testing-and-evidence.de.md) beschreibt Runtime-Validierung.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Der ext_proc-Service akzeptiert `late_action_policy: strict` mit passendem
`phase4_mode=strict`. Eine späte ImmediateResponse verwendet den Local-Reply-Pfad
des gepinnten Envoy-Hosts, der nach kodierten Headern den betroffenen
Downstream-Stream zurücksetzt. Der Framework-H2-Adapter prüft den Reset zusammen
mit einem gesunden Peer und Folgezugriff. Dieses Hostergebnis für den gewählten
Lauf nachweisen.

## Verwandtes Material

- [Envoy-Connector-Anleitung](../../connectors/envoy/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
