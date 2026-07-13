<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: HAProxy

**Sprache:** [English](haproxy.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-htx-filter` bei HAProxy. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, HAProxy-3.2.21-Source, der repository-eigene native HTX-Filter/Overlay, die Common-Bridge, eine lokale Regeldatei, ein Loopback-Frontend und ein Loopback-Upstream.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [HAProxy INSTALL](https://github.com/haproxy/haproxy/blob/master/INSTALL)
  Offizielle Anleitung zur Target-Auswahl, Buildoptionen, Kompilierung und Installation. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Read the INSTALL file for the exact selected HAProxy release.)
- **Quelle und Umfang:** [HAProxy Documentation](https://docs.haproxy.org/)
  Konfigurationssyntax und CLI-Dokumentation für `haproxy -c` und den Laufzeitbetrieb. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Use documentation matching the selected major/minor series.)
- **Quelle und Umfang:** [HAProxy Releases](https://www.haproxy.org/download/)
  Offizielle Source-Downloads und Auswahl der Release-Serie. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The repository overlay currently fixes its compatible source to 3.2.21.)
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

Zuerst ein offizielles HAProxy bauen und `haproxy -vv` prüfen. Die ausgewählte Repository-Integration hat eine strengere Kompatibilitätsgrenze: Ihr nativer HTX-Overlay erfordert ausdrücklich HAProxy 3.2.21. Der normale HAProxy-Build belegt den Upstream-Hostbuild; der folgende Overlay-Build erzeugt die ausgewählte Hostkopie und linkt sie mit libmodsecurity.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/haproxy"
export HAPROXY_VERSION="3.2.21"
export HAPROXY_ARCHIVE="haproxy-$HAPROXY_VERSION.tar.gz"
export HAPROXY_URL="https://www.haproxy.org/download/3.2/src/$HAPROXY_ARCHIVE"
export HAPROXY_SHA256="0cb8818a26c5f888e0cb1c40f1b3acb9fb952527d1733f769ce688fedd680339"
export HAPROXY_SRC="$HOST_BUILD_BASE/haproxy-$HAPROXY_VERSION"
export HAPROXY_PREFIX="$HOME/.local/haproxy-modsecurity"
export HAPROXY_STAGE="$HOST_BUILD_BASE/stage"
mkdir -p "$HOST_BUILD_BASE"
cd "$HOST_BUILD_BASE"
curl -fLO "$HAPROXY_URL"
printf "%s  %s\n" "$HAPROXY_SHA256" "$HAPROXY_ARCHIVE" | sha256sum -c -
tar -xzf "$HAPROXY_ARCHIVE"
cd "$HAPROXY_SRC"
make help
make -j"$jobs" TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_PCRE2=1
make install-bin DESTDIR="$HAPROXY_STAGE" PREFIX="$HAPROXY_PREFIX"
export HAPROXY_BIN="$HAPROXY_STAGE$HAPROXY_PREFIX/sbin/haproxy"
"$HAPROXY_BIN" -vv
```

## 7. Connector bauen und einbinden

Der offizielle HAProxy-Release enthält diesen Connector nicht. Die repository-eigene native HTX-Integration kopiert die kompatible Quelle in einen externen Worktree, prüft und wendet ihren Overlay an, fügt HTX-Filter sowie Common-/libmodsecurity-Bridge hinzu und baut den Host neu. SPOE/SPOP ist ein separater Kompatibilitätsweg und keine Evidence für diesen nativen Filter.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export HAPROXY_HTX_SOURCE_DIR="$HAPROXY_SRC"
export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
export MAKE_JOBS="$jobs"
CONNECTOR_ROOT="$CONNECTOR_ROOT" sh connectors/haproxy/htx-overlay/build-overlay.sh
export HAPROXY_HTX_BIN="$HAPROXY_HTX_BUILD_DIR/worktree/haproxy"
test -x "$HAPROXY_HTX_BIN"
"$HAPROXY_HTX_BIN" -vv
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export HAPROXY_CONFIG="$HOST_BUILD_BASE/haproxy-local.cfg"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$HAPROXY_CONFIG" <<EOF
global
    daemon
defaults
    mode http
    timeout connect 5s
    timeout client 30s
    timeout server 30s
frontend local
    bind 127.0.0.1:8080
    filter modsecurity-htx rules-file "$RULES_FILE" phase4-mode safe
    default_backend local_upstream
backend local_upstream
    server app 127.0.0.1:8081
EOF
"$HAPROXY_HTX_BIN" -c -f "$HAPROXY_CONFIG"
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$HAPROXY_HTX_BIN" -vv
file "$HAPROXY_HTX_BIN"
ldd "$HAPROXY_HTX_BIN" | grep -F libmodsecurity
test -f "$HAPROXY_HTX_BUILD_DIR/overlay-build.env"
sha256sum "$HAPROXY_HTX_BIN"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

```sh
mkdir -p "$HOST_BUILD_BASE/www"
printf "haproxy local upstream\n" > "$HOST_BUILD_BASE/www/index.html"
python3 -m http.server 8081 --bind 127.0.0.1 --directory "$HOST_BUILD_BASE/www" > "$HOST_BUILD_BASE/upstream.log" 2>&1 &
upstream_pid=$!
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HAPROXY_HTX_BIN" -db -f "$HAPROXY_CONFIG" > "$HOST_BUILD_BASE/haproxy.log" 2>&1 &
haproxy_pid=$!
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
kill "$haproxy_pid" "$upstream_pid"
```

## 11. Paketgestützter Weg

Status: `package-assisted source build`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search haproxy
dnf search haproxy
haproxy -vv 2>/dev/null || true
```

Ein Paket kann ein gewöhnliches HAProxy zum Vergleich bereitstellen, trägt aber nicht den repository-eigenen HTX-Overlay. Es kann daher den ausgewählten nativen Filterweg nicht ersetzen; die exakt kompatible Quelle und den Overlay-Build verwenden.

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
make build-haproxy
make check-config-haproxy
make start-smoke-haproxy
make runtime-smoke-haproxy
run_id="haproxy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-haproxy-htx
NO_CRS_RUN_ID="$run_id" make evidence-check-haproxy
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

Der Overlay verweigert eine andere Version als 3.2.21, ein In-Tree-Buildverzeichnis, fehlende libmodsecurity-Header oder eine fehlende Bibliothek. Das als Kompatibilitätsgrenze behandeln, nicht als Grund, ein SPOA-Ergebnis einzusetzen.

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
| HAPROXY_VERSION | Von der aktuellen HTX-Overlay verlangte Version. |
| HAPROXY_ARCHIVE | Aus HAPROXY_VERSION abgeleiteter Archivname. |
| HAPROXY_URL | Offizielle HAProxy-Sourcearchiv-URL. |
| HAPROXY_SHA256 | Erwartete SHA-256 des ausgewählten Sourcearchivs. |
| HAPROXY_SRC | Verifizierter Upstream-Source-Baum. |
| HAPROXY_PREFIX | Privater Upstream-Host-Installationsprefix. |
| HAPROXY_STAGE | Mit DESTDIR verwendeter Staging-Root. |
| HAPROXY_BIN | Gestagtes gewöhnliches HAProxy-Binary. |
| HAPROXY_HTX_SOURCE_DIR | Vom Overlay-Builder verwendete verifizierte Quelle. |
| HAPROXY_HTX_BUILD_DIR | Externes disponierbares Overlay-Worktree- und Provenienzverzeichnis. |
| HAPROXY_HTX_BIN | Repository-gebautes natives HTX-Hostbinary. |
| MAKE_JOBS | An den Repository-Overlay-Builder übergebener Parallel-Job-Wert. |
| HAPROXY_CONFIG | Lokale Loopback-HAProxy-Konfiguration. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
