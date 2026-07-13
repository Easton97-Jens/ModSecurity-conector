<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: lighttpd

**Sprache:** [English](lighttpd.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `patched-native` bei lighttpd. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, lighttpd-1.4.84-Source, der repository-eigene Entity-Body-Patch, ein gepatchter Host, ein passendes Connectormodul, eine lokale Laufzeitkonfiguration und HTTP/1.1-Traffic auf Loopback.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [lighttpd INSTALL](https://github.com/lighttpd/lighttpd1.4/blob/master/INSTALL)
  Offizielle Voraussetzungen sowie Autotools-/Source-Build-, Test-, Installations- und Startanleitung. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Re-check INSTALL for the selected lighttpd release.)
- **Quelle und Umfang:** [lighttpd Source Downloads](https://download.lighttpd.net/lighttpd/)
  Offizielle Releasearchive und Prüfsummenmaterial. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The latest upstream release can differ from the repository patch pin.)
- **Quelle und Umfang:** [lighttpd Documentation](https://redmine.lighttpd.net/projects/lighttpd/wiki)
  Offizielle Konfigurations- und Befehlsdokumentation, soweit sie für den ausgewählten Hostrelease gilt. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Check accessibility and release relevance before relying on a page.)
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

Der aktuelle Repository-Patch und die gepatchten Hostskripte sind auf lighttpd 1.4.84 gepinnt. Kein neueres Upstream-Archiv stillschweigend einsetzen: Ein neuerer Upstream-Release ist ein Update, das Patch, Configure, ABI und Laufzeit neu validieren muss. An einer disponierbaren Kopie arbeiten, damit die verifizierte Upstream-Quelle zum Vergleich erhalten bleibt.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/lighttpd"
export LIGHTTPD_VERSION="1.4.84"
export LIGHTTPD_ARCHIVE="lighttpd-$LIGHTTPD_VERSION.tar.xz"
export LIGHTTPD_URL="https://download.lighttpd.net/lighttpd/releases-1.4.x/$LIGHTTPD_ARCHIVE"
export LIGHTTPD_CHECKSUM_URL="https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$LIGHTTPD_VERSION.sha256sum"
export LIGHTTPD_CHECKSUM_FILE="$HOST_BUILD_BASE/lighttpd-$LIGHTTPD_VERSION.sha256sum"
export LIGHTTPD_SHA256="076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70"
export LIGHTTPD_SRC="$HOST_BUILD_BASE/lighttpd-$LIGHTTPD_VERSION"
export LIGHTTPD_PATCHED_SRC="$HOST_BUILD_BASE/lighttpd-$LIGHTTPD_VERSION-patched"
export LIGHTTPD_BUILD_DIR="$HOST_BUILD_BASE/build-$LIGHTTPD_VERSION"
export LIGHTTPD_PREFIX="$HOME/.local/lighttpd-modsecurity"
export LIGHTTPD_PATCH_FILE="$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"
mkdir -p "$HOST_BUILD_BASE"
cd "$HOST_BUILD_BASE"
curl -fLO "$LIGHTTPD_URL"
curl -fL "$LIGHTTPD_CHECKSUM_URL" -o "$LIGHTTPD_CHECKSUM_FILE"
awk -v archive="$LIGHTTPD_ARCHIVE" '$2 == archive { print }' "$LIGHTTPD_CHECKSUM_FILE" | sha256sum -c -
printf "%s  %s\n" "$LIGHTTPD_SHA256" "$LIGHTTPD_ARCHIVE" | sha256sum -c -
tar -xJf "$LIGHTTPD_ARCHIVE"
cp -a "$LIGHTTPD_SRC" "$LIGHTTPD_PATCHED_SRC"
cd "$LIGHTTPD_PATCHED_SRC"
patch --dry-run -p1 < "$LIGHTTPD_PATCH_FILE"
patch -p1 < "$LIGHTTPD_PATCH_FILE"
if test -x ./autogen.sh; then ./autogen.sh; fi
./configure --help | grep -E -- "--prefix|--bindir|--sbindir|--libdir"
mkdir -p "$LIGHTTPD_BUILD_DIR"
cd "$LIGHTTPD_BUILD_DIR"
"$LIGHTTPD_PATCHED_SRC/configure" --prefix="$LIGHTTPD_PREFIX" --bindir="$LIGHTTPD_PREFIX/bin" --sbindir="$LIGHTTPD_PREFIX/bin" --libdir="$LIGHTTPD_PREFIX/lib"
make -j"$jobs"
if make -n check >/dev/null 2>&1; then make check; fi
make install
"$LIGHTTPD_PREFIX/bin/lighttpd" -V
```

## 7. Connector bauen und einbinden

Das Repository-Modul muss dieselben gepatchten Source-Header und dieselbe generierte `config.h` wie der Host verwenden. Das Source-Buildskript linkt es mit libmodsecurity und schreibt das Modul in ein externes Verzeichnis. Ein normales lighttpd-Paket besitzt den Entity-Body-Hook nicht und kann dieses ausgewählte Modul nicht als gleichwertigen Weg laden.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export LIGHTTPD_MODULE_DIR="$BUILD_ROOT/modules"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_CONNECTOR_OUT_DIR="$BUILD_ROOT/connector" LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" LIGHTTPD_MSCONNECTOR_CORE_MODE=patched LIGHTTPD_SOURCE_DIR="$LIGHTTPD_PATCHED_SRC" LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_DIR" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/lighttpd/build/build_module.sh
export LIGHTTPD_MODULE="$LIGHTTPD_MODULE_DIR/mod_msconnector.so"
test -f "$LIGHTTPD_MODULE"
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export LIGHTTPD_RUNTIME_CONFIG="$HOST_BUILD_BASE/msconnector-runtime.conf"
export LIGHTTPD_CONFIG="$HOST_BUILD_BASE/lighttpd-local.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$LIGHTTPD_RUNTIME_CONFIG" <<EOF
rules_file=$RULES_FILE
request_body_mode=none
response_body_mode=none
phase4_mode=safe
EOF
cat > "$LIGHTTPD_CONFIG" <<EOF
server.compat-module-load = "disable"
server.modules = ( "mod_msconnector" )
server.bind = "127.0.0.1"
server.port = 8080
server.document-root = "$LIGHTTPD_PREFIX/htdocs"
server.pid-file = "$HOST_BUILD_BASE/lighttpd.pid"
server.errorlog = "$HOST_BUILD_BASE/lighttpd-error.log"
msconnector.enabled = "enable"
msconnector.config-file = "$LIGHTTPD_RUNTIME_CONFIG"
EOF
"$LIGHTTPD_PREFIX/bin/lighttpd" -tt -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR"
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$LIGHTTPD_PREFIX/bin/lighttpd" -V
file "$LIGHTTPD_MODULE"
ldd "$LIGHTTPD_MODULE" | grep -F libmodsecurity
nm -D "$LIGHTTPD_MODULE" | grep -E "mod_msconnector_plugin_init$"
grep -F LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$LIGHTTPD_PATCHED_SRC/src/plugin.h"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

```sh
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$LIGHTTPD_PREFIX/bin/lighttpd" -D -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR" &
lighttpd_pid=$!
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
kill "$lighttpd_pid"
```

## 11. Paketgestützter Weg

Status: `selected profile not available package-only`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search lighttpd
dnf search lighttpd
lighttpd -V 2>/dev/null || true
```

Ein Paket kann einen Vergleichshost und Voraussetzungen liefern, aber nicht den versionierten Entity-Body-Patch dieses Repositorys oder ein Modul mit passenden gepatchten Headern. Es ist keine package-only-Version des ausgewählten Weges.

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
make build-lighttpd
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
run_id="lighttpd-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
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

Wenn der Patch-Dry-Run fehlschlägt, ihn nicht erzwingen: die exakte 1.4.84-Quelle und Patch-Prüfsumme prüfen. Kann das Modul nicht geladen werden, gepatchten Core und Modul aus demselben Source-/Header-/Konfigurationssatz neu bauen.

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
| LIGHTTPD_VERSION | Vom Repository-Patch verlangte exakte Upstream-Version. |
| LIGHTTPD_ARCHIVE | Aus LIGHTTPD_VERSION abgeleiteter Archivname. |
| LIGHTTPD_URL | Offizielle lighttpd-Sourcearchiv-URL. |
| LIGHTTPD_CHECKSUM_URL | Offizielle Prüfsummen-URL des ausgewählten Releases. |
| LIGHTTPD_CHECKSUM_FILE | Geladene offizielle Prüfsummendatei für das ausgewählte Archiv. |
| LIGHTTPD_SHA256 | Erwartete Prüfsumme des ausgewählten Archivs. |
| LIGHTTPD_SRC | Verifizierter unveränderter Upstream-Source-Baum. |
| LIGHTTPD_PATCHED_SRC | Disponierbare gepatchte Kopie der ausgewählten Quelle. |
| LIGHTTPD_BUILD_DIR | Out-of-tree-Buildverzeichnis des gepatchten lighttpd. |
| LIGHTTPD_PREFIX | Privater Installationsprefix des gepatchten Hosts. |
| LIGHTTPD_PATCH_FILE | Versionierter Entity-Body-Patch des Repositorys. |
| LIGHTTPD_MODULE_DIR | Externes Verzeichnis für das passende Connectormodul. |
| LIGHTTPD_MODULE | Pfad des gebauten passenden Moduls. |
| LIGHTTPD_RUNTIME_CONFIG | Connector-Laufzeitkonfiguration für Regeln/Modus. |
| LIGHTTPD_CONFIG | Lokale lighttpd-Serverkonfiguration. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
