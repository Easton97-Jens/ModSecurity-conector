<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: Envoy

**Sprache:** [English](envoy.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `ext_proc` bei Envoy. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, ein offizielles Envoy-Binary oder optionaler Bazel-Build, der repository-eigene ext_proc-Service, seine CGo-/Common-Bridge, gRPC-Konfiguration, eine lokale Regeldatei und Loopback-Listener für Envoy/Upstream.

## Connector in diesem Repository

- [Envoy-Connector](../../../connectors/envoy/README.de.md)
- [Produktiver ext_proc-Service](../../../connectors/envoy/ext_proc/)
- [Connector-Konfiguration](../../../connectors/envoy/config/)
- [ext_proc-Build-Helper](../../../connectors/envoy/build/build_ext_proc.sh)
- [Source-Zuordnung](../../../connectors/envoy/SOURCE_MAP.json)

Dies ist der primäre Connectorpfad dieser Anleitung: connectors/envoy/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.

Abschnitt 7 baut den repository-eigenen ext_proc-Service; die offizielle Envoy-Dokumentation erläutert nur Hostbinary und Hostkonfiguration.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Installing Envoy](https://www.envoyproxy.io/docs/envoy/latest/start/install)
  Offizielle Auswahl von Binary-, Paket- und Containerinstallation sowie Versionsprüfung. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The page is version-sensitive; use the docs matching the selected Envoy release.)
- **Quelle und Umfang:** [Run Envoy](https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/run-envoy.html)
  Die offiziellen Befehle für Version, Konfigurationsvalidierung und lokalen Start. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Use the selected Envoy release documentation.)
- **Quelle und Umfang:** [Static configuration](https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/configuration-static)
  Listener-, HTTP-Connection-Manager-, Route- und Clusterkonfiguration des Loopback-Beispiels. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Verify field names against the selected release.)
- **Quelle und Umfang:** [HTTP external processing filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter)
  Der offizielle ext_proc-Filter und der Vertrag für bidirektionale gRPC-Konfiguration. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Filter fields and semantics are release-dependent.)
- **Quelle und Umfang:** [Envoy admin interface](https://www.envoyproxy.io/docs/envoy/latest/operations/admin.html)
  Nur auf Loopback gebundene Admin-Endpunkte und ihren lokalen Diagnosezweck. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Do not expose the local example as a general management interface.)
- **Quelle und Umfang:** [Envoy v1.38.2 release](https://github.com/envoyproxy/envoy/releases/tag/v1.38.2)
  Offizielle Seite des ausgewählten Releases, Binary-Asset und Prüfsummenmaterial. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (This guide pins the binary route to v1.38.2.)
- **Quelle und Umfang:** [Envoy source/Bazel guidance](https://github.com/envoyproxy/envoy/blob/v1.38.2/bazel/README.md)
  Offizielle optionale Source-Build-Anleitung; sie ist ressourcenintensiv und nicht der Standardweg. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Use only with the selected tag and sufficient CPU, memory, and storage.)



## 4. Voraussetzungen

Zuerst libmodsecurity mit der gemeinsamen Anleitung bauen. Danach die dokumentierten Entwicklungswerkzeuge des ausgewählten Hosts installieren und Host, Connector, Header sowie Libraries kompatibel halten.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

Das repository-eigene ext_proc-Modul verlangt Go 1.26.5; die gepinnte Moduldeklaration vor dem Build in Abschnitt 7 prüfen.

```sh
go version
grep -Fx "go 1.26.5" "$CONNECTOR_ROOT/connectors/envoy/ext_proc/go.mod"
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

Das repository-kompatible offizielle Envoy-Releasebinary verwenden. Der ext_proc-Service ist eine getrennte Repository-Komponente und wird in Abschnitt 7 gebaut.

```sh
WORKDIR="$HOME/connector-build/envoy"
```

#### Releasebinary herunterladen

Das offizielle x86_64-Artefakt wird in ein lokales Arbeitsverzeichnis geschrieben und ausführbar gemacht.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fL "https://github.com/envoyproxy/envoy/releases/download/v1.38.2/envoy-1.38.2-linux-x86_64" -o envoy
printf "%s  %s\n" "87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899" "envoy" | sha256sum -c -
chmod 755 envoy
./envoy --version
```

### Was wurde installiert oder gebaut?

Es ist nur das offizielle Envoy-Hostbinary vorhanden. Es enthält weder das repository-eigene ext_proc-Executable noch seine Common-Bridge oder Konfiguration.

### Erfolg prüfen

Datei- und Versionsprüfung bestätigen, dass das beabsichtigte lokale Hostbinary für Abschnitt 7 bereit ist.

```sh
test -x "$WORKDIR/envoy"
"$WORKDIR/envoy" --version
```

### Source-Build und Integritätsprüfung

#### Optional: Envoy aus Source bauen

Ein vollständiger Bazel-Build ist ressourcenintensiv und absichtlich nicht Teil des Einsteigerwegs. Vor der Nutzung als Host-Override die [offizielle Envoy-Source-Build-Anleitung](https://www.envoyproxy.io/docs/envoy/latest/start/building/local_docker_build.html) für den ausgewählten Release befolgen.

## 7. Connector bauen und einbinden

Das repository-eigene ext_proc-Executable ist die aus Source gebaute Komponente. Es linkt die Common-/libmodsecurity-Bridge und ist nicht Teil eines offiziellen Envoy-Binaries. Die erzeugte Hostkonfiguration verwendet `envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor`, einen HTTP/2-gRPC-Cluster und einen Router nach diesem Filter. Den Service in einen externen Root bauen und danach beide Konfigurationen erzeugen.

Der Hostpfad wird hier nur erneut gesetzt, damit die Connectorbefehle den Host aus Abschnitt 6 verwenden können, ohne ihn erneut zu bauen.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/envoy"
export ENVOY_BIN="$HOST_BUILD_BASE/envoy"
cd "$CONNECTOR_ROOT"
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/envoy/build/build_ext_proc.sh"
export EXT_PROC_BIN="$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
test -x "$EXT_PROC_BIN"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/envoy/build/test_ext_proc.sh"
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.

```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export ENVOY_CONFIG="$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.yaml"
export EXT_PROC_CONFIG="$CONNECTOR_ROOT/connectors/envoy/config/envoy-ext-proc-service.json"
export RUNTIME_ROOT="$BUILD_ROOT/envoy-ext-proc/runtime-smoke"
export EXT_PROC_RUNTIME_CONFIG="$RUNTIME_ROOT/envoy-ext-proc-runtime.conf"
export ENVOY_PORT=18080
export ENVOY_UPSTREAM_PORT=18081
export EXT_PROC_PORT=18083
export ENVOY_ADMIN_PORT=19001
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$ENVOY_PORT" UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" EXT_PROC_PORT="$EXT_PROC_PORT" ADMIN_PORT="$ENVOY_ADMIN_PORT" sh "$CONNECTOR_ROOT/connectors/envoy/config/prepare_envoy_ext_proc_config.sh"
OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$RUNTIME_ROOT/events.jsonl" sh "$CONNECTOR_ROOT/connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh"
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG"
"$EXT_PROC_BIN" --check-config --config "$EXT_PROC_CONFIG" --runtime-config "$EXT_PROC_RUNTIME_CONFIG"
"$ENVOY_BIN" --version
test -x "$EXT_PROC_BIN"
file "$EXT_PROC_BIN"
ldd "$EXT_PROC_BIN" | grep -F libmodsecurity | grep -Fv "not found"
grep -F "envoy.filters.http.ext_proc" "$ENVOY_CONFIG"
grep -F "request_body_mode: STREAMED" "$ENVOY_CONFIG"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Das begrenzte Repository-Harness startet Envoy, ext_proc und seinen Upstream und sendet dann HTTP/1.1-Allow- und lokale Deny-Probes durch die erzeugte `ext_proc`-Route. Sein Admin-Endpunkt ist nur auf Loopback gebunden und dient lokalen Readiness-Diagnosen. Seine Ergebnisse gelten nur für diese beobachteten Requests.

```sh
RUNTIME_ROOT="$RUNTIME_ROOT" ENVOY_BIN="$ENVOY_BIN" RULES_FILE="$RULES_FILE" ENVOY_SMOKE_PORT="$ENVOY_PORT" ENVOY_UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" ENVOY_EXT_PROC_PORT="$EXT_PROC_PORT" ENVOY_ADMIN_PORT="$ENVOY_ADMIN_PORT" EXT_PROC_RUNTIME_CONFIG="$EXT_PROC_RUNTIME_CONFIG" sh "$CONNECTOR_ROOT/connectors/envoy/harness/run_envoy_ext_proc_runtime.sh"
# The bounded runner regenerates its run-local Envoy and ext_proc runtime files, then starts Envoy, ext_proc, and a loopback upstream, sends local HTTP/1.1 requests, and stops them.
```

## 11. Paketgestützter Weg

Status: `package-assisted source build`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search envoy
dnf search envoy
envoy --version 2>/dev/null || true
```

Pakete können ein Hostbinary oder Buildabhängigkeiten liefern, enthalten aber nicht den repository-eigenen ext_proc-Service oder seine Common-/libmodsecurity-Bridge. Ein Paketbinary getrennt validieren und den aus Source gebauten Service beibehalten.

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
make build-envoy
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
run_id="envoy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
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
test ! -e "$HOME/connector-build/envoy" || find "$HOME/connector-build/envoy" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Ein offizielles Envoy-Binary ist nur der Host. Schlägt die Validierung fehl, erzeugtes ext_proc-YAML, Besitz der gRPC-Ports, ext_proc-Servicekonfiguration und libmodsecurity-Loaderpfad prüfen; ext_proc nicht durch den separaten ext_authz-Kompatibilitätsservice ersetzen.

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
| ENVOY_BIN | Verifiziertes Envoy-Executable. |
| EXT_PROC_BIN | Repository-gebautes ext_proc-Service-Executable. |
| ENVOY_CONFIG | Erzeugte Loopback-Envoy-Konfiguration. |
| EXT_PROC_CONFIG | Repository-ext_proc-Servicekonfiguration, die zusammen mit der erzeugten Laufzeitkonfiguration validiert wird. |
| EXT_PROC_RUNTIME_CONFIG | Erzeugte Common-Laufzeitkonfiguration für ext_proc. |
| OUTPUT_CONFIG | Ausgabepfad eines Konfigurationsmaterialisierungsbefehls. |
| EVENT_PATH | Absoluter lokaler Eventlog-Pfad für den ext_proc-Laufzeitkonfigurationsgenerator. |
| RUNTIME_ROOT | Externer temporärer Root des begrenzten Envoy-Laufzeitharnesses. |
| LISTEN_PORT | An den Envoy-Konfigurationsgenerator übergebener Loopback-Listenerport. |
| UPSTREAM_PORT | An den Envoy-Konfigurationsgenerator übergebener Loopback-Upstream-Port. |
| ADMIN_PORT | An den Envoy-Konfigurationsgenerator übergebener Loopback-Adminport. |
| ENVOY_PORT | Loopback-Listenerport von Envoy. |
| ENVOY_UPSTREAM_PORT | Vom Test genutzter Loopback-Upstream-Port. |
| EXT_PROC_PORT | Loopback-gRPC-Port des ext_proc-Service. |
| ENVOY_SMOKE_PORT | An das begrenzte Repository-Envoy-Harness übergebener Loopback-Listenerport. |
| ENVOY_EXT_PROC_PORT | An das begrenzte Repository-Envoy-Harness übergebener Loopback-gRPC-Port. |
| ENVOY_ADMIN_PORT | Loopback-Adminport von Envoy. |
| WORKDIR | Externes Envoy-Binary-Arbeitsverzeichnis. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
