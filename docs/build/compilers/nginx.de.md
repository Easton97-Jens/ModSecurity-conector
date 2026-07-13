<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: NGINX

**Sprache:** [English](nginx.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-nginx-http-module` bei NGINX. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, ein offizieller NGINX-Source-Release, ModSecurity-nginx, die Repository-NGINX-Source-Integration, ein dynamisches Modul, eine lokale Regeldatei und eine NGINX-Instanz auf Loopback.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Building nginx from Sources](https://nginx.org/en/docs/configure.html)
  Die offiziellen Configure-Optionen einschließlich Prefix-Pfaden, Dynamic Modules, Kompatibilität sowie Compiler- und Linkerflags. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (NGINX options are release-dependent; inspect `./auto/configure --help` for the selected source.)
- **Quelle und Umfang:** [Official NGINX packages](https://nginx.org/en/linux_packages.html)
  Offizielle Distributionsrepositories und Paketinstallationskontext; kein ABI-Gleichwertigkeitsclaim für ein aus Source gebautes Modul. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Package layout changes by distribution and release.)
- **Quelle und Umfang:** [ModSecurity repository](https://github.com/owasp-modsecurity/ModSecurity)
  Die libmodsecurity-v3-Enginequelle. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The selected tag/commit is shown in the shared build section.)
- **Quelle und Umfang:** [ModSecurity-nginx](https://github.com/owasp-modsecurity/ModSecurity-nginx)
  Die offizielle NGINX-Connectorquelle, die durch `--add-dynamic-module` eingebunden wird. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Pin it to a release tag or commit matching the selected NGINX source.)

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

Dies ist der bewusst kleine NGINX-plus-libmodsecurity-Build aus den fachlich relevanten Teilen des bereitgestellten Referenzskripts: isolierte Verzeichnisse, Compiler-/Linkerpfade, gepinnte Quellen, Connector, Configure, Build, Installation, ABI-Prüfungen und Provenienz. Das externe Skript baut weitere optionale Module und Integrationen; sie sind für diesen Kernbuild nicht erforderlich und werden hier nicht behandelt.

```sh
export NGINX_BUILD_BASE="$HOME/src/nginx-modsecurity"
export NGINX_VERSION="1.31.2"
export NGINX_ARCHIVE="nginx-$NGINX_VERSION.tar.gz"
export NGINX_URL="https://nginx.org/download/$NGINX_ARCHIVE"
export NGINX_SRC="$NGINX_BUILD_BASE/nginx"
export NGINX_PREFIX="$HOME/.local/nginx-modsecurity"
export MODSECURITY_NGINX_SRC="$NGINX_BUILD_BASE/ModSecurity-nginx"
export MODSECURITY_NGINX_REF="v1.0.4"
export MODSECURITY_NGINX_COMMIT="3f4b57df10ce43b1f1c722141f7621dc64838be8"
mkdir -p "$NGINX_BUILD_BASE"
cd "$NGINX_BUILD_BASE"
curl -fLO "$NGINX_URL"
curl -fLO "$NGINX_URL.asc"
# Import the NGINX release signing key from the official release site before verifying.
gpg --verify "${NGINX_ARCHIVE}.asc" "$NGINX_ARCHIVE"
tar -xzf "$NGINX_ARCHIVE"
mv "nginx-$NGINX_VERSION" "$NGINX_SRC"
```

## 7. Connector bauen und einbinden

Den offiziellen ModSecurity-nginx-Connector klonen und pinnen, dann Host und Connector gemeinsam konfigurieren. `--add-module` bindet einen Connector statisch in NGINX ein; `--add-dynamic-module` erzeugt ein separat geladenes Modul. Diese Anleitung verwendet die dynamische Form und hält das Modul daher beim exakt dazu gebauten Binary.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git "$MODSECURITY_NGINX_SRC"
git -C "$MODSECURITY_NGINX_SRC" checkout --detach "$MODSECURITY_NGINX_REF"
test "$(git -C "$MODSECURITY_NGINX_SRC" rev-parse HEAD)" = "$MODSECURITY_NGINX_COMMIT"
git -C "$MODSECURITY_NGINX_SRC" rev-parse HEAD
cd "$NGINX_SRC"
./auto/configure --help | grep -E -- "--with-compat|--add-dynamic-module|--with-pcre-jit|--with-http_ssl_module"
./auto/configure --prefix="$NGINX_PREFIX" --sbin-path="$NGINX_PREFIX/sbin/nginx" --modules-path="$NGINX_PREFIX/modules" --conf-path="$NGINX_PREFIX/conf/nginx.conf" --pid-path="$NGINX_PREFIX/logs/nginx.pid" --http-log-path="$NGINX_PREFIX/logs/access.log" --error-log-path="$NGINX_PREFIX/logs/error.log" --with-http_ssl_module --with-pcre-jit --with-compat --add-dynamic-module="$MODSECURITY_NGINX_SRC" --with-cc-opt="-I$MODSECURITY_PREFIX/include" --with-ld-opt="-L$MODSECURITY_PREFIX/lib -Wl,-rpath,$MODSECURITY_PREFIX/lib"
./objs/nginx -V 2>&1 || true
grep -E '^(CC|LD|CORE_LIBS)' objs/Makefile || true
make -j"$jobs" V=1 2>&1 | tee nginx-build.log
make modules
make install
export NGINX_MODULE="$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so"
test -x "$NGINX_PREFIX/sbin/nginx"
test -f "$NGINX_MODULE"
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.

Für den vollständigen Direktivenvertrag vor der Anpassung dieses lokalen Beispiels die repository-eigene [NGINX-Konfigurationsreferenz](../../../examples/nginx/configuration-reference.de.md) lesen.

```sh
export RULES_FILE="$NGINX_BUILD_BASE/modsecurity-local.conf"
export NGINX_CONFIG="$NGINX_PREFIX/conf/nginx.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$NGINX_CONFIG" <<EOF
load_module modules/ngx_http_modsecurity_module.so;
events {}
http {
    server {
        listen 127.0.0.1:8080;
        location / {
            modsecurity on;
            modsecurity_rules_file "$RULES_FILE";
            return 200 "nginx modsecurity test\n";
        }
    }
}
EOF
"$NGINX_PREFIX/sbin/nginx" -t -p "$NGINX_PREFIX" -c conf/nginx.conf
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$NGINX_PREFIX/sbin/nginx" -V
file objs/nginx
ldd objs/nginx
find objs -maxdepth 2 -type f -name "*modsecurity*.so" -print
file "$NGINX_PREFIX/sbin/nginx"
ldd "$NGINX_PREFIX/sbin/nginx"
file "$NGINX_MODULE"
ldd "$NGINX_MODULE" | grep -F libmodsecurity
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

```sh
"$NGINX_PREFIX/sbin/nginx" -p "$NGINX_PREFIX" -c conf/nginx.conf
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$NGINX_PREFIX/sbin/nginx" -p "$NGINX_PREFIX" -c conf/nginx.conf -s quit
{ "$NGINX_PREFIX/sbin/nginx" -V 2>&1; git -C "$MODSECURITY_SRC" rev-parse HEAD; git -C "$MODSECURITY_NGINX_SRC" rev-parse HEAD; cc --version; c++ --version; sha256sum "$NGINX_PREFIX/sbin/nginx"; } > "$NGINX_BUILD_BASE/build-provenance.txt"
```

## 11. Paketgestützter Weg

Status: `package-assisted source build`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search nginx
dnf search nginx
nginx -V 2>&1 || true
```

Ein offizielles Paket kann einen Host bereitstellen, aber ein separat kompiliertes dynamisches Modul muss zu dessen exakten NGINX-Buildoptionen und ABI passen. Es ist nicht mit diesem aus Source gebauten Binary-/Modulpaar austauschbar. Vor einem Paket-Host-Modulbuild die offizielle NGINX-Paketseite und die Ausgabe `nginx -V` des Pakets prüfen.

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
make build-nginx
make check-config-nginx
make start-smoke-nginx
make runtime-smoke-nginx
run_id="nginx-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-nginx
NO_CRS_RUN_ID="$run_id" make evidence-check-nginx
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

Ein `load_module`-Fehler bedeutet normalerweise, dass NGINX-Binary, Configure-Argumente, Connector-Checkout oder Modul voneinander abweichen. Das Paar gemeinsam neu bauen; das Modul nicht in eine fremde Paketinstallation kopieren.

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
| NGINX_BUILD_BASE | Externes NGINX-Source-/Build-/Provenienzverzeichnis. |
| NGINX_VERSION | Ausgewählter offizieller NGINX-Release. |
| NGINX_ARCHIVE | Aus NGINX_VERSION abgeleiteter Archivname. |
| NGINX_URL | Offizielle NGINX-Archiv-URL. |
| NGINX_SRC | Entpackter NGINX-Source-Baum. |
| NGINX_PREFIX | Privater NGINX-Installationsprefix. |
| MODSECURITY_NGINX_SRC | Gepinnter ModSecurity-nginx-Checkout. |
| MODSECURITY_NGINX_REF | Für den Connector ausgewählter Release-Tag. |
| MODSECURITY_NGINX_COMMIT | Vom Connector-Tag erwarteter aufgelöster Commit. |
| NGINX_MODULE | Mit dieser NGINX-Quelle gebautes dynamisches Modul. |
| NGINX_CONFIG | Lokale NGINX-Konfiguration für den Loopback-Test. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
