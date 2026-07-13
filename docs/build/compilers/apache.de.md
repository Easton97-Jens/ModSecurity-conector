<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: Apache HTTP Server

**Sprache:** [English](apache.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-httpd-module` bei Apache HTTP Server. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, Apache HTTP Server 2.4, APR/APR-util, PCRE2, der Repository-Apache-Adapter, APXS, eine lokale Regeldatei und eine httpd-Instanz auf Loopback.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Compiling and Installing](https://httpd.apache.org/docs/2.4/install.html)
  Offizieller Apache-Quellrelease sowie Voraussetzungen für APR/APR-util und PCRE2, Configure, Make, Installation, Start und Stop. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (HTTP Server 2.4; choose and verify the release again before building.)
- **Quelle und Umfang:** [APXS](https://httpd.apache.org/docs/2.4/programs/apxs.html)
  Die DSO-Build-/Installationsschnittstelle und die Abfragen, die ein Modul an genau einen httpd-Build binden. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (HTTP Server 2.4 APXS reference.)
- **Quelle und Umfang:** [Apache HTTP Server Download](https://httpd.apache.org/download.cgi)
  Offizielle Releasearchive, PGP-Signaturen, Prüfsummen und Apache KEYS. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The page changes when Apache publishes a release.)
- **Quelle und Umfang:** [ModSecurity repository](https://github.com/owasp-modsecurity/ModSecurity)
  Die libmodsecurity-v3-Quelle und ihre Autotools-Buildanleitung. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The selected Git tag/commit is recorded below.)

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

Zuerst dem Apache-Source-Release-Ablauf folgen. Entweder passende System-Entwicklungseingaben für APR/APR-util bereitstellen oder geprüfte APR- und APR-util-Bäume vor dem Configure als `srclib/apr` und `srclib/apr-util` entpacken. Letzteres ist das von Apache dokumentierte Bundled-APR-Layout.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/apache"
export HTTPD_VERSION="2.4.68"
export HTTPD_ARCHIVE="httpd-$HTTPD_VERSION.tar.gz"
export HTTPD_URL="https://downloads.apache.org/httpd/$HTTPD_ARCHIVE"
export HTTPD_PREFIX="$HOME/.local/httpd-modsecurity"
export HTTPD_SRC="$HOST_BUILD_BASE/httpd-$HTTPD_VERSION"
export APXS="$HTTPD_PREFIX/bin/apxs"
mkdir -p "$HOST_BUILD_BASE"
cd "$HOST_BUILD_BASE"
curl -fLO "$HTTPD_URL"
curl -fLO "$HTTPD_URL.asc"
curl -fLO "$HTTPD_URL.sha256"
sha256sum -c "${HTTPD_ARCHIVE}.sha256"
# Import Apache KEYS through the official download page before this verification.
gpg --verify "${HTTPD_ARCHIVE}.asc" "$HTTPD_ARCHIVE"
tar -xzf "$HTTPD_ARCHIVE"
cd "$HTTPD_SRC"
# If APR/APR-util are not supplied by the system, place verified trees in srclib/apr and srclib/apr-util.
./configure --help | grep -E -- "--prefix|--with-included-apr|--with-pcre|--enable-mods-shared"
./configure --prefix="$HTTPD_PREFIX" --enable-mods-shared=most --with-pcre="$(command -v pcre2-config)"
make -j"$jobs"
make install
test -x "$HTTPD_PREFIX/bin/httpd"
test -x "$HTTPD_PREFIX/bin/apachectl"
test -x "$APXS"
```

## 7. Connector bauen und einbinden

Der Repository-Adapter ist ein Autotools-/APXS-Projekt. Ihn mit genau dem soeben gebauten APXS und httpd konfigurieren; APXS liest Compiler-, Include- und Modulverzeichniswerte genau dieses Hosts.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export CONNECTOR_SRC="$CONNECTOR_ROOT/connectors/apache"
cd "$CONNECTOR_SRC"
./autogen.sh
./configure --with-libmodsecurity="$MODSECURITY_PREFIX" --with-apxs="$APXS" --with-apache="$HTTPD_PREFIX/bin/httpd"
make -j"$jobs"
make install
export MODULE_PATH="$("$APXS" -q LIBEXECDIR)/mod_security3.so"
test -f "$MODULE_PATH"
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export HTTPD_CONFIG="$HOST_BUILD_BASE/httpd-local.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$HTTPD_CONFIG" <<EOF
ServerRoot "$HTTPD_PREFIX"
Listen 127.0.0.1:8080
ServerName 127.0.0.1
LoadModule security3_module "$MODULE_PATH"
DocumentRoot "$HTTPD_PREFIX/htdocs"
<Directory "$HTTPD_PREFIX/htdocs">
    Require all granted
</Directory>
<Location "/">
    modsecurity on
    modsecurity_rules_file "$RULES_FILE"
</Location>
EOF
"$HTTPD_PREFIX/bin/httpd" -t -f "$HTTPD_CONFIG"
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$HTTPD_PREFIX/bin/httpd" -v
"$HTTPD_PREFIX/bin/apachectl" -V
"$HTTPD_PREFIX/bin/httpd" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -M | grep -E "(^|[[:space:]])so_module"
"$APXS" -q PREFIX
"$APXS" -q INCLUDEDIR
"$APXS" -q LIBEXECDIR
"$APXS" -q CC
file "$MODULE_PATH"
ldd "$MODULE_PATH" | grep -F libmodsecurity
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

```sh
"$HTTPD_PREFIX/bin/httpd" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -k start
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$HTTPD_PREFIX/bin/httpd" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -k stop
```

## 11. Paketgestützter Weg

Status: `package-assisted source build`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search apache2
dnf search httpd
apache2 -v 2>/dev/null || httpd -v 2>/dev/null || true
```

Ein Pakethost kann zum Vergleich nützlich sein, aber sein APXS, seine Header, sein Modulverzeichnis, Konfigurationslayout und Servicename können von diesem Source-Prefix abweichen. Vor konkreten Paketnamen die offizielle Paketdokumentation der passenden Distribution prüfen; den Adapter mit APXS dieses Pakets neu bauen, wenn er der beabsichtigte Host ist.

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
make build-apache
make check-config-apache
make start-smoke-apache
make runtime-smoke-apache
run_id="apache-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-apache
NO_CRS_RUN_ID="$run_id" make evidence-check-apache
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

Wenn `apxs -q` auf andere Header oder ein anderes Modulverzeichnis als das laufende httpd zeigt, stoppen und den Adapter neu bauen. Ein gegen eine Apache-ABI gebautes Modul darf nicht von einer anderen geladen werden.

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
| HTTPD_VERSION | Ausgewählter Apache-2.4-Release; gegen die Downloadseite erneut validieren. |
| HTTPD_ARCHIVE | Aus HTTPD_VERSION abgeleiteter Releasearchivname. |
| HTTPD_URL | Offizielle Apache-Archiv-URL. |
| HTTPD_PREFIX | Privater httpd-Installationsprefix. |
| HTTPD_SRC | Entpackter Apache-Source-Baum. |
| APXS | APXS desselben Hosts, der das Modul lädt. |
| CONNECTOR_SRC | Aus CONNECTOR_ROOT ausgewählte Repository-Source des Apache-Connectors. |
| MODULE_PATH | Durch APXS aufgelöstes installiertes Repository-DSO. |
| HTTPD_CONFIG | Lokale eigenständige httpd-Konfiguration. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
