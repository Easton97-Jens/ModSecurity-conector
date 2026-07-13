<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: Traefik

**Sprache:** [English](traefik.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-middleware` bei Traefik. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, Traefik, die repository-eigene native Go-Middleware, der C/C++-Engine-Service, Common/libmodsecurity, ein privater Unix-Domain-Socket, statische und dynamische File-Provider-Konfiguration sowie HTTP-Traffic auf Loopback.

## Connector in diesem Repository

- [Traefik-Connector](../../../connectors/traefik/README.de.md)
- [Native Middleware-Quelle](../../../connectors/traefik/native_middleware/)
- [Engine-Service-Quellen](../../../connectors/traefik/src/)
- [Native-Middleware-Builder](../../../connectors/traefik/build/build-native-middleware.sh)
- [Engine-Service-Builder](../../../connectors/traefik/build/build-engine-service.sh)
- [Source-Zuordnung](../../../connectors/traefik/SOURCE_MAP.json)
- [Statische Konfiguration der nativen Middleware](../../../connectors/traefik/config/traefik-native-middleware-static.yaml)
- [Dynamische Konfiguration der nativen Middleware](../../../connectors/traefik/config/traefik-native-middleware-dynamic.yaml)

Dies ist der primäre Connectorpfad dieser Anleitung: connectors/traefik/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.

Abschnitt 7 baut die repository-eigene native Middleware und ihren Engine-Service; das offizielle Traefik-Material dokumentiert nur den Host.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Traefik Getting Started](https://doc.traefik.io/traefik/getting-started/)
  Offizielle Installationsoptionen, EntryPoints, Router, Services und sicherer lokaler Startkontext. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Confirm the documentation version for the selected Traefik release.)
- **Quelle und Umfang:** [Building and Testing](https://doc.traefik.io/traefik/contributing/building-testing/)
  Offizieller Source-Checkout sowie Go-/Tooling-, Build- und Testablauf. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The required Go version is defined by the selected release's `go.mod`.)
- **Quelle und Umfang:** [Traefik v3.7 configuration overview](https://doc.traefik.io/traefik/v3.7/getting-started/configuration-overview/)
  Die Unterscheidung zwischen statischer Installations- und dynamischer Routing-Konfiguration. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Use one static configuration method and recheck it for another release.)
- **Quelle und Umfang:** [Traefik v3.7 EntryPoints](https://doc.traefik.io/traefik/v3.7/reference/install-configuration/entrypoints/)
  Statische Konfiguration der Loopback-EntryPoints. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Field names are release-specific.)
- **Quelle und Umfang:** [Traefik v3.7 File Provider](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/other-providers/file/)
  Dynamische Router, Middleware und Services des File Providers. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Recheck the selected version before using another release.)
- **Quelle und Umfang:** [Traefik v3.7 health check](https://doc.traefik.io/traefik/v3.7/reference/install-configuration/observability/healthcheck/)
  Der Loopback-Ping-Endpunkt zur Bestätigung des lokalen Hoststarts. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Do not enable an insecure dashboard for this local check.)
- **Quelle und Umfang:** [Traefik v3.7.5 release](https://github.com/traefik/traefik/releases/tag/v3.7.5)
  Offizielles festes Releasematerial und Prüfsummenquelle. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (This guide selects v3.7.5 as the repository-compatible host input.)
- **Quelle und Umfang:** [Traefik v3.7.5 source](https://github.com/traefik/traefik/tree/v3.7.5)
  Offizieller ausgewählter Source-Baum; sein go.mod definiert die benötigte Go-Version des Hosts. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The host's Go requirement is distinct from the repository middleware module's requirement.)



## 4. Voraussetzungen

Zuerst libmodsecurity mit der gemeinsamen Anleitung bauen. Danach die dokumentierten Entwicklungswerkzeuge des ausgewählten Hosts installieren und Host, Connector, Header sowie Libraries kompatibel halten.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

Das repository-eigene native Middleware-Modul verlangt Go 1.24.0; dies unterscheidet sich von der optionalen Traefik-v3.7.5-Host-Source-Anforderung in Abschnitt 6.

```sh
go version
grep -Fx "go 1.24.0" "$CONNECTOR_ROOT/connectors/traefik/native_middleware/go.mod"
```

## 5. ModSecurity vorbereiten

Baue zuerst libmodsecurity v3 nach der gemeinsamen Anleitung:

[libmodsecurity v3 bauen](libmodsecurity.de.md)

Der folgende Handoff verwendet den offiziellen Standard des einfachen Builds `/usr/local/modsecurity`. MODSECURITY_PREFIX, MODSECURITY_INCLUDE_DIR oder MODSECURITY_LIB_DIR nur für eine bewusst gewählte Installation überschreiben. Er prüft den Header und wählt `lib64` nur, wenn `lib` libmodsecurity nicht enthält.

```sh
export MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-/usr/local/modsecurity}"
export MODSECURITY_INCLUDE_DIR="${MODSECURITY_INCLUDE_DIR:-$MODSECURITY_PREFIX/include}"
export MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$MODSECURITY_PREFIX/lib}"
if [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] && [ -f "$MODSECURITY_PREFIX/lib64/libmodsecurity.so" ]; then
    MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib64"
fi
test -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h"
test -f "$MODSECURITY_LIB_DIR/libmodsecurity.so"
```

## 6. Host oder Proxy bereitstellen

### Einfacher Weg

Das repository-kompatible offizielle Traefik-Releasebinary verwenden. Native Middleware und Engine-Service bleiben getrennte Komponenten von Abschnitt 7.

```sh
WORKDIR="$HOME/connector-build/traefik"
VERSION="3.7.5"
```

#### Traefik herunterladen und entpacken

Das offizielle linux_amd64-Releasearchiv enthält das Hostbinary; hier wird keine Repository-Middleware gebaut.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz"
curl -fLO "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_checksums.txt"
grep "traefik_v${VERSION}_linux_amd64.tar.gz" "traefik_v${VERSION}_checksums.txt" | sha256sum -c -
tar -xzf "traefik_v${VERSION}_linux_amd64.tar.gz"
```

### Was wurde installiert oder gebaut?

Das Releasearchiv stellt nur das Traefik-Hostbinary bereit. Repository-native Middleware, CGo-/Common-Bridge und UDS-Engine-Service werden später gebaut.

### Erfolg prüfen

Diese Prüfungen identifizieren das entpackte Hostbinary, bevor der Connectorbuild beginnt.

```sh
test -x "$WORKDIR/traefik"
"$WORKDIR/traefik" version
```

### Source-Build und Integritätsprüfung

#### Optional: Traefik aus Source bauen

Die ausgewählte Traefik-v3.7.5-Quelle deklariert Go 1.25.0 in go.mod; diese exakte Anforderung vor dem Klonen prüfen. Dieser Weg baut nur den Traefik-Host; Repository-Middleware und Engine bleiben Abschnitt 7.

```sh
go version
git clone https://github.com/traefik/traefik.git "$WORKDIR/traefik-source"
cd "$WORKDIR/traefik-source"
git checkout --detach "v$VERSION"
grep -E "^go " go.mod
grep -Fx "go 1.25.0" go.mod
git rev-parse HEAD
```

#### Traefik-Source-Host bauen

Der offizielle Buildbefehl und die Versionsausgabe bestätigen das Source-Host-Ergebnis. Repository-Middleware und Engine bleiben Arbeit für Abschnitt 7.

```sh
cd "$WORKDIR/traefik-source"
make binary
export TRAEFIK_BIN="$WORKDIR/traefik-source/dist/traefik"
"$WORKDIR/traefik-source/dist/traefik" version
```

## 7. Connector bauen und einbinden

Ein Standard-Traefik-Binary enthält weder die native ModSecurity-Middleware noch den persistenten Engine-Service. Abschnitt 7 kompiliert und testet das repository-eigene Go-Middleware-Paket und baut danach den C/C++-Service außerhalb dieses Checkouts; Abschnitt 8 stellt die Pluginquelle für den lokalen Lauf bereit. Der Engine-Socket muss für den lokalen Run privat sein und darf nicht als geteilter Systemendpunkt wiederverwendet werden.

Der Hostpfad wird hier nur erneut gesetzt, damit die Connectorbefehle den Host aus Abschnitt 6 verwenden können, ohne ihn erneut zu bauen.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/traefik"
export TRAEFIK_BIN="${TRAEFIK_BIN:-$HOST_BUILD_BASE/traefik}"
cd "$CONNECTOR_ROOT"
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$BUILD_ROOT/traefik-native-middleware"
export TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$BUILD_ROOT/traefik-engine-service"
export TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR/traefik-engine-service"
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-native-middleware.sh" build
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-native-middleware.sh" test
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-engine-service.sh" build
test -x "$TRAEFIK_ENGINE_SERVICE_BIN"
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-engine-service.sh" test
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.

Die Konfiguration verwendet bewusst nur Loopback-EntryPoints und aktiviert kein unsicheres Dashboard oder API. Jedes Dashboard oder jeden Administrationsendpunkt nur optional verwenden und für einen echten Betrieb separat absichern.

```sh
export TRAEFIK_RUNTIME_ROOT="$BUILD_ROOT/traefik-native-runtime-$(date -u +%Y%m%dT%H%M%SZ)"
export RULES_FILE="$TRAEFIK_RUNTIME_ROOT/traefik-native-rules.conf"
export TRAEFIK_STATIC_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-static.yaml"
export TRAEFIK_DYNAMIC_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-dynamic.yaml"
export TRAEFIK_ENGINE_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-engine.conf"
export TRAEFIK_SOCKET_DIR="$(mktemp -d /tmp/msconnector-traefik-uds.XXXXXX)"
chmod 700 "$TRAEFIK_SOCKET_DIR"
export TRAEFIK_ENGINE_SOCKET="$TRAEFIK_SOCKET_DIR/engine.sock"
test "${#TRAEFIK_ENGINE_SOCKET}" -lt 108
export TRAEFIK_PORT=18080
export TRAEFIK_UPSTREAM_PORT=18081
export TRAEFIK_PING_PORT=18082
export TRAEFIK_PLUGIN_MODULE="github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware"
export TRAEFIK_PLUGIN_SOURCE="$TRAEFIK_RUNTIME_ROOT/plugins-local/src/$TRAEFIK_PLUGIN_MODULE"
mkdir -p "$TRAEFIK_PLUGIN_SOURCE" "$TRAEFIK_RUNTIME_ROOT/logs"
cp -a "$CONNECTOR_ROOT/connectors/traefik/native_middleware/." "$TRAEFIK_PLUGIN_SOURCE/"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_HEADERS:X-Modsec-Smoke "@streq block" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$TRAEFIK_STATIC_CONFIG" <<EOF
entryPoints:
  web:
    address: "127.0.0.1:$TRAEFIK_PORT"
  health:
    address: "127.0.0.1:$TRAEFIK_PING_PORT"
providers:
  file:
    filename: "$TRAEFIK_DYNAMIC_CONFIG"
    watch: false
ping:
  entryPoint: health
experimental:
  localPlugins:
    modsecurityNative:
      moduleName: $TRAEFIK_PLUGIN_MODULE
      settings:
        envs: []
EOF
cat > "$TRAEFIK_DYNAMIC_CONFIG" <<EOF
http:
  routers:
    native:
      entryPoints: [web]
      rule: "PathPrefix(`/`)"
      middlewares: [native]
      service: upstream
  middlewares:
    native:
      plugin:
        modsecurityNative:
          maxHeaderCount: 128
          maxHeaderBytes: 65536
          maxRequestChunkBytes: 32768
          maxResponseChunkBytes: 32768
          transactionIDHeader: X-Request-Id
          engineMode: uds
          engineSocketPath: $TRAEFIK_ENGINE_SOCKET
  services:
    upstream:
      loadBalancer:
        servers:
          - url: http://127.0.0.1:$TRAEFIK_UPSTREAM_PORT
EOF
cat > "$TRAEFIK_ENGINE_CONFIG" <<EOF
enabled=on
rules_file=$RULES_FILE
transaction_id_header=x-request-id
request_body_mode=streaming
response_body_mode=streaming
request_body_limit=4096
response_body_limit=4096
body_limit_action=reject
phase4_mode=safe
default_block_status=403
default_error_status=500
use_error_log=off
event_path=$TRAEFIK_RUNTIME_ROOT/logs/traefik-events.jsonl
max_header_count=100
max_header_name_size=256
max_header_value_size=8192
max_total_header_bytes=65536
max_event_json_bytes=16384
EOF
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
( cd "$TRAEFIK_RUNTIME_ROOT" && "$TRAEFIK_BIN" check --configFile="$TRAEFIK_STATIC_CONFIG" )
"$TRAEFIK_ENGINE_SERVICE_BIN" --check-config --config "$TRAEFIK_ENGINE_CONFIG"
"$TRAEFIK_BIN" version
test -f "$TRAEFIK_STATIC_CONFIG"
test -f "$TRAEFIK_DYNAMIC_CONFIG"
test -x "$TRAEFIK_ENGINE_SERVICE_BIN"
ldd "$TRAEFIK_ENGINE_SERVICE_BIN" | grep -F libmodsecurity | grep -Fv "not found"
grep -F "modsecurityNative" "$TRAEFIK_STATIC_CONFIG"
grep -F "engineSocketPath" "$TRAEFIK_DYNAMIC_CONFIG"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. `/ping` bestätigt den Hoststart; der normale Request auf `/native` nutzt den privaten UDS-Weg, und der Testheader `X-Modsec-Smoke: block` löst die lokale 403-Regel aus. Diese Beobachtungen begründen keinen weitergehenden Claim.

```sh
python3 -m http.server "$TRAEFIK_UPSTREAM_PORT" --bind 127.0.0.1 --directory "$TRAEFIK_RUNTIME_ROOT" > "$TRAEFIK_RUNTIME_ROOT/logs/upstream.log" 2>&1 &
upstream_pid=$!
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_ENGINE_SERVICE_BIN" --serve --config "$TRAEFIK_ENGINE_CONFIG" --socket "$TRAEFIK_ENGINE_SOCKET" > "$TRAEFIK_RUNTIME_ROOT/logs/engine.log" 2>&1 &
engine_pid=$!
attempt=0
while [ "$attempt" -lt 50 ] && [ ! -S "$TRAEFIK_ENGINE_SOCKET" ]; do
    attempt=$((attempt + 1))
    sleep 0.1
done
test -S "$TRAEFIK_ENGINE_SOCKET"
test "$(stat -c "%a" "$TRAEFIK_ENGINE_SOCKET")" = "600"
( cd "$TRAEFIK_RUNTIME_ROOT" && LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_BIN" --configFile="$TRAEFIK_STATIC_CONFIG" ) > "$TRAEFIK_RUNTIME_ROOT/logs/traefik.log" 2>&1 &
traefik_pid=$!
attempt=0
while [ "$attempt" -lt 50 ]; do
    if ! kill -0 "$traefik_pid" 2>/dev/null; then
        exit 1
    fi
    if curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping" >/dev/null; then
        break
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done
test "$attempt" -lt 50
curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping"
test "$(curl --http1.1 -sS -o /dev/null -w "%{http_code}" -H "X-Request-Id: traefik-native-allow" http://127.0.0.1:$TRAEFIK_PORT/native)" = "200"
test "$(curl --http1.1 -sS -o /dev/null -w "%{http_code}" -H "X-Modsec-Smoke: block" -H "X-Request-Id: traefik-native-deny" http://127.0.0.1:$TRAEFIK_PORT/native)" = "403"
kill "$traefik_pid" "$engine_pid" "$upstream_pid"
```

## 11. Paketgestützter Weg

Status: `package-assisted source build`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search traefik
dnf search traefik
traefik version 2>/dev/null || true
```

Ein Paket oder separat geladenes Hostbinary kann Traefik selbst bereitstellen, aber keines enthält die repository-eigene Go-Middleware, CGo-/Common-Bridge oder den UDS-Engine-Service. Diese aus Source gebauten Komponenten beibehalten und ihre Socket-Berechtigungen validieren.

## 12. Repository-gesteuerter Testweg

Dieser Abschnitt folgt nach dem manuellen Build. Die Targets automatisieren und testen die zuvor beschriebenen Build- und Integrationsschritte; sie ersetzen nicht deren technische Dokumentation. Exit `77` bedeutet eine bewusst blockierte Voraussetzung, und ein einzelner Target-Erfolg ist keine weitergehende Freigabe.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
mkdir -p "$VERIFIED_RUN_PARENT"
cd "$VERIFIED_RUN_PARENT"
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
git switch feature/all-connectors-no-crs-baseline
git submodule update --init --recursive
make check-framework
make prepare-runtime-components
make build-traefik
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
run_id="traefik-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

## 13. Aktualisieren und neu bauen

Vor einem Update immer die verlinkte Upstream-Anleitung, Releaseversion sowie Configure-/Buildoptionen erneut prüfen. Anschließend alle betroffenen Host-, Connector-, ABI- und lokalen HTTP-Tests wiederholen.

```sh
git -C "$CONNECTOR_ROOT" pull --ff-only
git -C "$CONNECTOR_ROOT" submodule update --init --recursive
# Rebuild the selected host and connector with the commands above.
```

## 14. Deinstallation und Cleanup

Keine Dateien pauschal nach `/usr/lib` kopieren und keine globalen Verzeichnisse entfernen. Bei einem Benutzer-Prefix ist kein `sudo` nötig. Evidence oder Logs erst nach bewusster Prüfung entfernen.

```sh
test ! -e "$HOME/connector-build/traefik" || find "$HOME/connector-build/traefik" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
test -z "${TRAEFIK_SOCKET_DIR:-}" || test ! -e "$TRAEFIK_SOCKET_DIR" || find "$TRAEFIK_SOCKET_DIR" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Wenn Traefik ohne Middleware startet, lokalen Plugin-Workspace, statische Registrierung, File Provider sowie Berechtigungen/Eigentümer des run-lokalen UDS-Verzeichnisses prüfen. Ein ForwardAuth-Kompatibilitätsweg diagnostiziert den ausgewählten nativen Middleware-Weg nicht.

## 16. Variablen und Platzhalter

| Variable/Platzhalter | Bedeutung |
| --- | --- |
| CONNECTOR_ROOT | Git-Top-Level dieses Repository-Checkouts; die Connector-Skripte werden von dort aus aufgerufen. |
| RULES_FILE | Lokale Testregeldatei; keine CRS-Regeldatei. |
| MODSECURITY_PREFIX | Installationsprefix von libmodsecurity. Der offizielle Standard des einfachen Builds ist /usr/local/modsecurity. |
| MODSECURITY_INCLUDE_DIR | Aus MODSECURITY_PREFIX ausgewähltes Headerverzeichnis von libmodsecurity. |
| MODSECURITY_LIB_DIR | Aus MODSECURITY_PREFIX ausgewähltes Shared-Library-Verzeichnis von libmodsecurity; der Handoff erkennt bei Bedarf lib64. |
| VERIFIED_RUN_PARENT | Externer Elternordner eines frischen Repository-Testcheckouts und seiner Testartefakte. |
| run_id | Eindeutige Kennung eines repository-gesteuerten Full-Lifecycle-Laufs. |
| NO_CRS_RUN_ID | Exportierte Full-Lifecycle-Kennung für den nachfolgenden Make-Aufruf; sie hält Evidence und Laufzeitdaten getrennt. |
| HOST_BUILD_BASE | Connector-spezifisches externes Verzeichnis für Quellen, Builds, Konfiguration und lokale Logs. |
| BUILD_ROOT | Externer Build- und Laufzeitstamm der repository-eigenen Connector-Komponenten. |
| LD_LIBRARY_PATH | Nur für einen dokumentierten lokalen Modul- oder Servicecheck verwendeter Prozess-Loaderpfad; nicht global setzen. |
| upstream_pid | Lokale Prozess-ID des Test-Upstreams aus $!; nur im selben Shell-Lauf verwenden. |
| engine_pid | Lokale Prozess-ID des gestarteten Traefik-Engine-Service aus $!; nur im selben Shell-Lauf verwenden. |
| traefik_pid | Lokale Prozess-ID des gestarteten Traefik aus $!; nur im selben Shell-Lauf verwenden. |
| TRAEFIK_BIN | Gebautes oder anderweitig verifiziertes Hostbinary. |
| TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR | Externes Go-Middleware-Buildreport-Verzeichnis. |
| TRAEFIK_ENGINE_SERVICE_BUILD_DIR | Externes C/C++-Engine-Service-Buildverzeichnis. |
| TRAEFIK_ENGINE_SERVICE_BIN | Gebautes privates Engine-Service-Executable. |
| TRAEFIK_RUNTIME_ROOT | Privates Arbeitsverzeichnis mit dem für einen manuellen Lauf bereitgestellten lokalen Plugin. |
| TRAEFIK_SOCKET_DIR | Kurzes privates Verzeichnis für den run-lokalen Unix-Domain-Socket; sein Modus ist 0700. |
| TRAEFIK_STATIC_CONFIG | Konfiguration der lokalen Pluginregistrierung. |
| TRAEFIK_DYNAMIC_CONFIG | File-Provider-Konfiguration für Router/Middleware. |
| TRAEFIK_ENGINE_CONFIG | Private Laufzeitkonfiguration des Engine-Service. |
| TRAEFIK_ENGINE_SOCKET | Privater run-lokaler UDS-Endpunkt, kein globaler Pfad. |
| TRAEFIK_PLUGIN_MODULE | Offizieller lokaler Plugin-Modulpfad unter plugins-local/src. |
| TRAEFIK_PLUGIN_SOURCE | Bereitgestelltes Source-Verzeichnis für das lokale Traefik-Plugin. |
| TRAEFIK_PORT | Loopback-Web-EntryPoint für den manuellen Test. |
| TRAEFIK_UPSTREAM_PORT | Loopback-Port des Test-Upstreams. |
| TRAEFIK_PING_PORT | Loopback-Port des Ping-Endpunkts. |
| WORKDIR | Externes Traefik-Host-Arbeitsverzeichnis. |
| VERSION | Repository-kompatibler Traefik-Release. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
