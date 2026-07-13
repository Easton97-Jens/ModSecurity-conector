<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: HAProxy

**Sprache:** [English](haproxy.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-htx-filter` bei HAProxy. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, HAProxy-3.2.21-Source, der repository-eigene native HTX-Filter/Overlay, die Common-Bridge, eine lokale Regeldatei, ein Loopback-Frontend und ein Loopback-Upstream.

## Connector in diesem Repository

- [HAProxy-Connector](../../../connectors/haproxy/README.de.md)
- [Produktive HAProxy-Quellen](../../../connectors/haproxy/src/)
- [Nativer HTX-Overlay](../../../connectors/haproxy/htx-overlay/)
- [HTX-Overlay-Builder](../../../connectors/haproxy/htx-overlay/build-overlay.sh)
- [Source-Zuordnung](../../../connectors/haproxy/SOURCE_MAP.json)
- [Native-HTX-Laufzeitkonfigurationshelper](../../../connectors/haproxy/harness/run_haproxy_htx_runtime.sh)

Dies ist der primäre Connectorpfad dieser Anleitung: connectors/haproxy/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.

Abschnitt 7 wendet den repository-eigenen HTX-Overlay auf die ausgewählte Hostquelle an und baut die Common-/libmodsecurity-Integration.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [HAProxy INSTALL](https://github.com/haproxy/haproxy/blob/master/INSTALL)
  Offizielle Anleitung zur Target-Auswahl, Buildoptionen, Kompilierung und Installation. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Read the INSTALL file for the exact selected HAProxy release.)
- **Quelle und Umfang:** [HAProxy Documentation](https://docs.haproxy.org/)
  Konfigurationssyntax und CLI-Dokumentation für `haproxy -c` und den Laufzeitbetrieb. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Use documentation matching the selected major/minor series.)
- **Quelle und Umfang:** [HAProxy Releases](https://www.haproxy.org/download/)
  Offizielle Source-Downloads und Auswahl der Release-Serie. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The repository overlay currently fixes its compatible source to 3.2.21.)



## 4. Voraussetzungen

Zuerst libmodsecurity mit der gemeinsamen Anleitung bauen. Danach die dokumentierten Entwicklungswerkzeuge des ausgewählten Hosts installieren und Host, Connector, Header sowie Libraries kompatibel halten.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
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

Den exakten HAProxy-Release bauen, den der native HTX-Overlay verlangt. Dies ist ein gewöhnlicher Upstream-Hostbuild; der Repository-Overlay bleibt Arbeit für Abschnitt 7.

```sh
WORKDIR="$HOME/connector-build/haproxy"
VERSION="3.2.21"
JOBS=2
```

#### HAProxy herunterladen und entpacken

Dies lädt die ausgewählte offizielle Hostquelle in ein isoliertes Arbeitsverzeichnis.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://www.haproxy.org/download/3.2/src/haproxy-$VERSION.tar.gz"
curl -fLO "https://www.haproxy.org/download/3.2/src/haproxy-$VERSION.tar.gz.sha256"
sha256sum -c "haproxy-$VERSION.tar.gz.sha256"
tar -xzf "haproxy-$VERSION.tar.gz"
```

#### Upstream-Host bauen

Die ausgewählten Buildoptionen aktivieren die Libraries dieses lokalen Hostbuilds. Sie fügen nicht den Repository-HTX-Filter hinzu.

```sh
cd "$WORKDIR/haproxy-$VERSION"
make -j"$JOBS" TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_PCRE2=1
```

### Was wurde installiert oder gebaut?

Das Upstream-haproxy-Executable wird im entpackten Source-Baum gebaut. Kein Staging-Prefix und kein Connector-Overlay gehören zum einfachen Weg.

### Erfolg prüfen

Die ausführliche Versionsausgabe identifiziert das ausgewählte Upstream-Binary und seine aktivierten Buildfeatures.

```sh
"$WORKDIR/haproxy-$VERSION/haproxy" -vv
```

### Source-Build und Integritätsprüfung

#### Optional: gewöhnlichen Host stagen

Eine gestagte Installation ist für die Prüfung nützlich, aber nicht der native HTX-Connectorbuild.

```sh
cd "$WORKDIR/haproxy-$VERSION"
INSTALL_DIR="$HOME/.local/haproxy-modsecurity"
STAGE="$WORKDIR/stage"
make install-bin DESTDIR="$STAGE" PREFIX="$INSTALL_DIR"
"$STAGE$INSTALL_DIR/sbin/haproxy" -vv
```

## 7. Connector bauen und einbinden

Der offizielle HAProxy-Release enthält diesen Connector nicht. Die repository-eigene native HTX-Integration kopiert die kompatible Quelle in einen frischen externen Worktree, prüft und wendet ihren Overlay an, fügt HTX-Filter sowie Common-/libmodsecurity-Bridge hinzu und baut den Host neu. Der Zeitstempel-Worktree vermeidet versehentliche Wiederverwendung, weil der Builder einen vorhandenen Worktree verweigert. SPOE/SPOP ist ein separater Kompatibilitätsweg und keine Evidence für diesen nativen Filter.

Der Hostpfad wird hier nur erneut gesetzt, damit die Connectorbefehle den Host aus Abschnitt 6 verwenden können, ohne ihn erneut zu bauen.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/haproxy"
export HAPROXY_SRC="$HOST_BUILD_BASE/haproxy-3.2.21"
export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay"
cd "$CONNECTOR_ROOT"
export HAPROXY_HTX_SOURCE_DIR="$HAPROXY_SRC"
export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay-$(date -u +%Y%m%dT%H%M%SZ)"
export MAKE_JOBS=2
CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$CONNECTOR_ROOT/connectors/haproxy/htx-overlay/build-overlay.sh"
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
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$HAPROXY_HTX_BIN" -c -f "$HAPROXY_CONFIG"
"$HAPROXY_HTX_BIN" -vv
file "$HAPROXY_HTX_BIN"
ldd "$HAPROXY_HTX_BIN" | grep -F libmodsecurity | grep -Fv "not found"
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
attempt=0
while [ "$attempt" -lt 50 ]; do
    if ! kill -0 "$upstream_pid" 2>/dev/null || ! kill -0 "$haproxy_pid" 2>/dev/null; then
        exit 1
    fi
    if [ "$(curl -sS --connect-timeout 1 -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ 2>/dev/null)" = "200" ]; then
        break
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done
test "$attempt" -lt 50
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"
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
git -C "$CONNECTOR_ROOT" pull --ff-only
git -C "$CONNECTOR_ROOT" submodule update --init --recursive
# Rebuild the selected host and connector with the commands above.
```

## 14. Deinstallation und Cleanup

Keine Dateien pauschal nach `/usr/lib` kopieren und keine globalen Verzeichnisse entfernen. Bei einem Benutzer-Prefix ist kein `sudo` nötig. Evidence oder Logs erst nach bewusster Prüfung entfernen.

```sh
test ! -e "$HOME/connector-build/haproxy" || find "$HOME/connector-build/haproxy" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/.local/haproxy-modsecurity" || find "$HOME/.local/haproxy-modsecurity" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Der Overlay verweigert eine andere Version als 3.2.21, ein In-Tree-Buildverzeichnis, fehlende libmodsecurity-Header oder eine fehlende Bibliothek. Das als Kompatibilitätsgrenze behandeln, nicht als Grund, ein SPOA-Ergebnis einzusetzen.

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
| LD_LIBRARY_PATH | Nur für einen dokumentierten lokalen Modul- oder Servicecheck verwendeter Prozess-Loaderpfad; nicht global setzen. |
| upstream_pid | Lokale Prozess-ID des Test-Upstreams aus $!; nur im selben Shell-Lauf verwenden. |
| haproxy_pid | Lokale Prozess-ID des gestarteten HAProxy aus $!; nur im selben Shell-Lauf verwenden. |
| HAPROXY_SRC | Verifizierter Upstream-Source-Baum. |
| HAPROXY_HTX_SOURCE_DIR | Vom Overlay-Builder verwendete verifizierte Quelle. |
| HAPROXY_HTX_BUILD_DIR | Externes disponierbares Overlay-Worktree- und Provenienzverzeichnis. |
| HAPROXY_HTX_BIN | Repository-gebautes natives HTX-Hostbinary. |
| MAKE_JOBS | An den Repository-Overlay-Builder übergebener Parallel-Job-Wert. |
| HAPROXY_CONFIG | Lokale Loopback-HAProxy-Konfiguration. |
| WORKDIR | Externes HAProxy-Source-Arbeitsverzeichnis. |
| VERSION | Vom HTX-Overlay verlangte exakte HAProxy-Version. |
| JOBS | Bewusst kleine Anzahl paralleler HAProxy-Buildjobs. |
| TARGET | An make übergebenes HAProxy-Hosttarget; dieser Guide verwendet linux-glibc. |
| USE_OPENSSL | Aktiviert OpenSSL-Unterstützung für den optionalen gewöhnlichen Hostbuild. |
| USE_ZLIB | Aktiviert zlib-Unterstützung für den optionalen gewöhnlichen Hostbuild. |
| USE_PCRE2 | Aktiviert PCRE2-Unterstützung für den optionalen gewöhnlichen Hostbuild. |
| INSTALL_DIR | Optionaler privater Installationsprefix des gewöhnlichen HAProxy. |
| STAGE | Optionaler Staging-Root der gewöhnlichen Hostinstallation. |
| DESTDIR | Direkt an das HAProxy-Installationsziel übergebener Staging-Root. |
| PREFIX | Direkt an das HAProxy-Installationsziel übergebener Installationsprefix. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
