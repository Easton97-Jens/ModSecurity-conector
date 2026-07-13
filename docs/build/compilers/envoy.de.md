<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: Envoy

**Sprache:** [English](envoy.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `ext_proc` bei Envoy. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, ein offizielles Envoy-Binary oder optionaler Bazel-Build, der repository-eigene ext_proc-Service, seine CGo-/Common-Bridge, gRPC-Konfiguration, eine lokale Regeldatei und Loopback-Listener für Envoy/Upstream.

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
- **Quelle und Umfang:** [ModSecurity repository](https://github.com/owasp-modsecurity/ModSecurity)
  Die libmodsecurity-v3-Enginequelle. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The selected tag/commit is shown in the shared build section.)

## 4. Voraussetzungen

Benötigt werden Git, ein C-Compiler, ein C++-Compiler, GNU Make, Autotools, libtool, pkg-config, PCRE2-Entwicklungsdateien, libxml2-Entwicklungsdateien, YAJL, LMDB und libcurl. Paketnamen sind distributions- und releaseabhängig: vor einer Installation die offizielle Distributionsdokumentation und die lokale Verfügbarkeit prüfen.

```sh
command -v git cc c++ make autoreconf libtool pkg-config
pkg-config --exists libpcre2-8
pkg-config --exists libxml-2.0
pkg-config --exists yajl
pkg-config --exists lmdb
pkg-config --exists libcurl
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

## 5. libmodsecurity v3 aus Source bauen

Dieser Ablauf verwendet einen festen, überprüfbaren Git-Tag und dessen aufgelösten Commit. `v3/master` ist kein reproduzierbarer Pin und wird deshalb nicht als solcher dargestellt. `build.sh` regeneriert beziehungsweise aktualisiert die Autotools-Eingaben; es kompiliert die Bibliothek noch nicht.

```sh
export BUILD_BASE="$HOME/src/modsecurity-build"
export MODSECURITY_SRC="$BUILD_BASE/ModSecurity"
export MODSECURITY_PREFIX="$HOME/.local/modsecurity"
export MODSECURITY_REF="v3.0.16"
export MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"
mkdir -p "$BUILD_BASE"
git clone --recurse-submodules https://github.com/owasp-modsecurity/ModSecurity.git "$MODSECURITY_SRC"
git -C "$MODSECURITY_SRC" checkout --detach "$MODSECURITY_REF"
git -C "$MODSECURITY_SRC" submodule update --init --recursive
test "$(git -C "$MODSECURITY_SRC" rev-parse HEAD)" = "$MODSECURITY_COMMIT"
git -C "$MODSECURITY_SRC" rev-parse HEAD
cd "$MODSECURITY_SRC"
./build.sh
./configure --help | grep -E -- "--with-(lmdb|libxml|curl|yajl)"
./configure --prefix="$MODSECURITY_PREFIX" --with-lmdb --with-libxml --with-curl --with-yajl
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf 2)"
make -j"$jobs"
make check
make install
export PKG_CONFIG_PATH="$MODSECURITY_PREFIX/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export LD_LIBRARY_PATH="$MODSECURITY_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

Beim ausgewählten Stand wird PCRE2 standardmäßig erkannt; `--with-pcre2` wird nicht erfunden. Die optionalen Schalter werden vor der Verwendung mit `./configure --help` geprüft. Wenn der gewählte Release einen Schalter nicht anbietet, ihn aus dem Aufruf entfernen statt einen nicht akzeptierten Befehl zu dokumentieren.

`PKG_CONFIG_PATH` ermöglicht Buildsystemen, die benutzerlokale Installation zu
finden. `LD_LIBRARY_PATH` ist nur für lokale Entwicklung und Tests; für eine
dauerhafte Systeminstallation bewusstes Loader-Setup oder rpath prüfen.

```sh
test -d "$MODSECURITY_PREFIX/include"
test -d "$MODSECURITY_PREFIX/lib"
find "$MODSECURITY_PREFIX" -maxdepth 3 -type f | sort
pkg-config --modversion libmodsecurity 2>/dev/null || true
find "$MODSECURITY_PREFIX/lib" -type f \( -name "libmodsecurity.so*" -o -name "libmodsecurity.a" \) -print
```

## 6. Host oder Proxy vorbereiten beziehungsweise bauen

Für den normalen lokalen Connectorweg das offizielle Envoy-Releasebinary verwenden und es vor der Konfiguration des ext_proc-Service validieren. Ein vollständiger Envoy-Source-Build ist optional, nicht der Standard: Der offizielle Bazel-Weg ist ressourcenintensiv und muss vor der Nutzung gegen `bazel/README.md` des ausgewählten Releases geprüft werden.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/envoy"
export ENVOY_VERSION="1.38.2"
export ENVOY_BIN="$HOST_BUILD_BASE/bin/envoy"
export ENVOY_DOWNLOAD_URL="https://github.com/envoyproxy/envoy/releases/download/v$ENVOY_VERSION/envoy-$ENVOY_VERSION-linux-x86_64"
export ENVOY_SHA256="87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899"
mkdir -p "$HOST_BUILD_BASE/bin"
curl -fL "$ENVOY_DOWNLOAD_URL" -o "$ENVOY_BIN"
printf "%s  %s\n" "$ENVOY_SHA256" "$ENVOY_BIN" | sha256sum -c -
chmod 755 "$ENVOY_BIN"
"$ENVOY_BIN" --version
# Optional only after reading the matching upstream Bazel guide: bazel build -c opt //source/exe:envoy-static
```

## 7. Connector bauen und einbinden

Das repository-eigene ext_proc-Executable ist die aus Source gebaute Komponente. Es linkt die Common-/libmodsecurity-Bridge und ist nicht Teil eines offiziellen Envoy-Binaries. Die erzeugte Hostkonfiguration verwendet `envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor`, einen HTTP/2-gRPC-Cluster und einen Router nach diesem Filter. Den Service in einen externen Root bauen und danach beide Konfigurationen erzeugen.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/envoy/build/build_ext_proc.sh
export EXT_PROC_BIN="$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
test -x "$EXT_PROC_BIN"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/envoy/build/test_ext_proc.sh
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export ENVOY_CONFIG="$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.yaml"
export EXT_PROC_RUNTIME_CONFIG="$BUILD_ROOT/envoy-ext-proc/runtime/ext-proc.conf"
export ENVOY_PORT=18080
export ENVOY_UPSTREAM_PORT=18081
export EXT_PROC_PORT=18083
export ENVOY_ADMIN_PORT=19001
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$ENVOY_PORT" UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" EXT_PROC_PORT="$EXT_PROC_PORT" ADMIN_PORT="$ENVOY_ADMIN_PORT" sh connectors/envoy/config/prepare_envoy_ext_proc_config.sh
OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$BUILD_ROOT/envoy-ext-proc/runtime/events.jsonl" sh connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh
"$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG"
"$EXT_PROC_BIN" --check-config --config connectors/envoy/config/envoy-ext-proc-service.json
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$ENVOY_BIN" --version
test -x "$EXT_PROC_BIN"
file "$EXT_PROC_BIN"
ldd "$EXT_PROC_BIN" | grep -F libmodsecurity
grep -F "envoy.filters.http.ext_proc" "$ENVOY_CONFIG"
grep -F "request_body_mode: STREAMED" "$ENVOY_CONFIG"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Das begrenzte Repository-Harness startet Envoy, ext_proc und seinen Upstream und sendet dann HTTP/1.1-Allow- und lokale Deny-Probes durch die erzeugte `ext_proc`-Route. Sein Admin-Endpunkt ist nur auf Loopback gebunden und dient lokalen Readiness-Diagnosen. Seine Ergebnisse gelten nur für diese beobachteten Requests.

```sh
RUNTIME_ROOT="$BUILD_ROOT/envoy-ext-proc/runtime-smoke" ENVOY_BIN="$ENVOY_BIN" RULES_FILE="$RULES_FILE" ENVOY_SMOKE_PORT="$ENVOY_PORT" ENVOY_UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" ENVOY_EXT_PROC_PORT="$EXT_PROC_PORT" ENVOY_ADMIN_PORT="$ENVOY_ADMIN_PORT" sh connectors/envoy/harness/run_envoy_ext_proc_runtime.sh
# The bounded runner starts Envoy, ext_proc, and a loopback upstream, sends local HTTP/1.1 requests, and stops them.
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
git -C "$MODSECURITY_SRC" fetch --tags origin
git -C "$MODSECURITY_SRC" checkout --detach "$MODSECURITY_REF"
git -C "$MODSECURITY_SRC" submodule update --init --recursive
git -C "$MODSECURITY_SRC" rev-parse HEAD
cd "$MODSECURITY_SRC"
make clean
make -j"$jobs"
```

## 14. Deinstallation und Cleanup

Keine Dateien pauschal nach `/usr/lib` kopieren und keine globalen Verzeichnisse entfernen. Bei einem Benutzer-Prefix ist kein `sudo` nötig. Evidence oder Logs erst nach bewusster Prüfung entfernen.

```sh
find "$BUILD_BASE" -maxdepth 2 -mindepth 1 -print
# Review the listed paths first; remove only a chosen private prefix or external build directory.
rmdir "$MODSECURITY_PREFIX" 2>/dev/null || true
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zuerst `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, den ausgewählten Prefix und die Ausgabe von `pkg-config` prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Ein offizielles Envoy-Binary ist nur der Host. Schlägt die Validierung fehl, erzeugtes ext_proc-YAML, Besitz der gRPC-Ports, ext_proc-Servicekonfiguration und libmodsecurity-Loaderpfad prüfen; ext_proc nicht durch den separaten ext_authz-Kompatibilitätsservice ersetzen.

## 16. Variablen und Platzhalter

| Variable/Platzhalter | Bedeutung |
| --- | --- |
| BUILD_BASE | Portabler Source-/Build-Stamm, z. B. `$HOME/src/modsecurity-build`. |
| CONNECTOR_ROOT | Git-Top-Level dieses Repository-Checkouts; die Connector-Skripte werden von dort aus aufgerufen. |
| HOST_BUILD_BASE | Connector-spezifisches externes Unterverzeichnis unter BUILD_BASE für Quellen, Builds, Konfiguration und lokale Logs. |
| BUILD_ROOT | Externer Build- und Laufzeitstamm der repository-eigenen Connector-Komponenten. |
| MODSECURITY_SRC | Checkout der ModSecurity-v3-Engine unter BUILD_BASE. |
| MODSECURITY_PREFIX | Isolierter Benutzer-Prefix für Header, Libraries und pkg-config-Metadaten. |
| MODSECURITY_REF | Fester Git-Tag der Engine; kein beweglicher Branch. |
| MODSECURITY_COMMIT | Erwarteter Commit, auf den MODSECURITY_REF aufgelöst werden muss. |
| MODSECURITY_INCLUDE_DIR | Include-Verzeichnis unter MODSECURITY_PREFIX für Repository-Komponenten. |
| MODSECURITY_LIB_DIR | Library-Verzeichnis unter MODSECURITY_PREFIX für Repository-Komponenten. |
| PKG_CONFIG_PATH | Temporärer Suchpfad für die lokale libmodsecurity-pc-Datei. |
| LD_LIBRARY_PATH | Nur temporärer Loaderpfad für lokale Tests, kein globales Installationsrezept. |
| RULES_FILE | Lokale Testregeldatei; keine CRS-Regeldatei. |
| jobs | Lokale Anzahl paralleler Buildjobs aus `getconf`; bei wenig RAM reduzieren. |
| VERIFIED_RUN_PARENT | Externer Elternordner eines frischen Repository-Testcheckouts und seiner Testartefakte. |
| run_id | Eindeutige Kennung eines repository-gesteuerten Full-Lifecycle-Laufs. |
| NO_CRS_RUN_ID | Exportierte Full-Lifecycle-Kennung für den nachfolgenden Make-Aufruf; sie hält Evidence und Laufzeitdaten getrennt. |
| upstream_pid | Lokale Prozess-ID des Test-Upstreams aus `$!`; nur im selben Shell-Lauf verwenden. |
| haproxy_pid | Lokale Prozess-ID des gestarteten HAProxy aus `$!`; nur im selben Shell-Lauf verwenden. |
| engine_pid | Lokale Prozess-ID des gestarteten Traefik-Engine-Service aus `$!`; nur im selben Shell-Lauf verwenden. |
| traefik_pid | Lokale Prozess-ID des gestarteten Traefik aus `$!`; nur im selben Shell-Lauf verwenden. |
| lighttpd_pid | Lokale Prozess-ID des gestarteten lighttpd aus `$!`; nur im selben Shell-Lauf verwenden. |
| ENVOY_VERSION | Ausgewählter offizieller Envoy-Release für den Binary-Weg. |
| ENVOY_BIN | Verifiziertes Envoy-Executable. |
| ENVOY_DOWNLOAD_URL | Offizielle Envoy-Releasebinary-URL. |
| ENVOY_SHA256 | Erwartete Binary-Prüfsumme des ausgewählten Releases. |
| BUILD_ROOT | Externer Build-Root des Repository-Connectors. |
| EXT_PROC_BIN | Repository-gebautes ext_proc-Service-Executable. |
| ENVOY_CONFIG | Erzeugte Loopback-Envoy-Konfiguration. |
| EXT_PROC_RUNTIME_CONFIG | Erzeugte Common-Laufzeitkonfiguration für ext_proc. |
| OUTPUT_CONFIG | Ausgabepfad eines Konfigurationsmaterialisierungsbefehls. |
| EVENT_PATH | Absoluter lokaler Eventlog-Pfad für den ext_proc-Laufzeitkonfigurationsgenerator. |
| RUNTIME_ROOT | Externer temporärer Root des begrenzten Envoy-Laufzeitharnesses. |
| ENVOY_PORT | Loopback-Listenerport von Envoy. |
| ENVOY_UPSTREAM_PORT | Vom Test genutzter Loopback-Upstream-Port. |
| EXT_PROC_PORT | Loopback-gRPC-Port des ext_proc-Service. |
| ENVOY_ADMIN_PORT | Loopback-Adminport von Envoy. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
