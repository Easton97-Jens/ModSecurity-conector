<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: lighttpd

**Sprache:** [English](lighttpd.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `patched-native` bei lighttpd. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, lighttpd-1.4.84-Source, der repository-eigene Entity-Body-Patch, ein gepatchter Host, ein passendes Connectormodul, eine lokale Laufzeitkonfiguration und HTTP/1.1-Traffic auf Loopback.

## Connector in diesem Repository

- [lighttpd-Connector](../../../connectors/lighttpd/README.de.md)
- [Connectormodul-Quelle](../../../connectors/lighttpd/module/mod_msconnector.c)
- [Produktive lighttpd-Quellen](../../../connectors/lighttpd/src/)
- [Patched-Host-Builder](../../../connectors/lighttpd/build/build_patched_host.sh)
- [Connectormodul-Builder](../../../connectors/lighttpd/build/build_module.sh)
- [Entity-Body-Patch](../../../connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch)
- [Source-Zuordnung](../../../connectors/lighttpd/SOURCE_MAP.json)
- [Native-lighttpd-Konfiguration](../../../connectors/lighttpd/config/lighttpd-native.conf)

Dies ist der primäre Connectorpfad dieser Anleitung: connectors/lighttpd/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.

Abschnitt 7 baut das Repository-Modul gegen den passenden gepatchten Host; die offizielle lighttpd-Dokumentation stellt nur Hostquelle und Hostanleitung bereit.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [lighttpd INSTALL](https://github.com/lighttpd/lighttpd1.4/blob/master/INSTALL)
  Offizielle Voraussetzungen sowie Autotools-/Source-Build-, Test-, Installations- und Startanleitung. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Re-check INSTALL for the selected lighttpd release.)
- **Quelle und Umfang:** [lighttpd Source Downloads](https://download.lighttpd.net/lighttpd/)
  Offizielle Releasearchive und Prüfsummenmaterial. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The latest upstream release can differ from the repository patch pin.)
- **Quelle und Umfang:** [lighttpd Documentation](https://redmine.lighttpd.net/projects/lighttpd/wiki)
  Offizielle Konfigurations- und Befehlsdokumentation, soweit sie für den ausgewählten Hostrelease gilt. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Check accessibility and release relevance before relying on a page.)



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

Der ausgewählte Weg benötigt einen gepatchten lighttpd-Source-Host. Die ersten Schritte laden die vom Repository-Patch verlangte exakte Version; Patch und Hostbuild folgen unter der Source-Build-Überschrift. Für einen neuen Patchlauf einen frischen externen Workspace verwenden, damit eine geprüfte gepatchte Kopie nie still verschachtelt oder wiederverwendet wird.

```sh
WORKDIR="$HOME/connector-build/lighttpd"
VERSION="1.4.84"
INSTALL_DIR="$HOME/.local/lighttpd-modsecurity"
```

#### lighttpd herunterladen

Dadurch bleibt die verifizierte Upstream-Quelle unverändert; der Patch wird nur auf eine disponierbare Kopie angewendet.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.tar.xz"
curl -fL "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.sha256sum" -o "lighttpd-$VERSION.sha256sum"
awk -v archive="lighttpd-$VERSION.tar.xz" '$2 == archive { print }' "lighttpd-$VERSION.sha256sum" | sha256sum -c -
printf "%s  %s\n" "076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70" "lighttpd-$VERSION.tar.xz" | sha256sum -c -
tar -xJf "lighttpd-$VERSION.tar.xz"
```

### Was wurde installiert oder gebaut?

Der private Prefix enthält den gepatchten lighttpd-Host. Er enthält noch nicht das repository-eigene Connectormodul.

### Source-Build und Integritätsprüfung

#### Arbeitskopie erstellen und Patch testen

Der erste Patchbefehl testet nur, ob die ausgewählte Quelle den Patch akzeptiert. Der zweite Befehl verändert die disponierbare Arbeitskopie.

```sh
cd "$WORKDIR"
export LIGHTTPD_PATCHED_SRC="$WORKDIR/lighttpd-$VERSION-patched"
test ! -e "$LIGHTTPD_PATCHED_SRC"
cp -a "lighttpd-$VERSION" "$LIGHTTPD_PATCHED_SRC"
cd "$LIGHTTPD_PATCHED_SRC"
patch --dry-run -p1 < "$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"
patch -p1 < "$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"
```

#### Gepatchten Host bauen

Dies baut nur den gepatchten lighttpd-Host. Das Connectormodul wird bewusst auf Abschnitt 7 verschoben.

```sh
test -x ./autogen.sh && ./autogen.sh
./configure --prefix="$INSTALL_DIR"
make -j2
make install
```

#### Optional: Out-of-tree-Hostbuild verwenden

Diese fortgeschrittene Alternative für Vergleich oder reproduzierbare Buildlayouts beibehalten; sie baut weiterhin nur den gepatchten Host.

```sh
cd "$WORKDIR/lighttpd-$VERSION-patched"
./autogen.sh
export LIGHTTPD_BUILD_DIR="$WORKDIR/build-$VERSION"
mkdir -p "$LIGHTTPD_BUILD_DIR"
cd "$LIGHTTPD_BUILD_DIR"
"$WORKDIR/lighttpd-$VERSION-patched/configure" --prefix="$INSTALL_DIR"
make -j2
make check
make install
```

### Erfolg prüfen

Das Upstream-Installationslayout von 1.4.84 legt lighttpd für diesen Prefix unter sbin ab.

```sh
"$INSTALL_DIR/sbin/lighttpd" -V
```

## 7. Connector bauen und einbinden

Das Repository-Modul muss dieselben gepatchten Source-Header und dieselbe generierte `config.h` wie der Host verwenden. Das Source-Buildskript linkt es mit libmodsecurity und schreibt das Modul in ein externes Verzeichnis. Der ausgewählte Source-Host baut seine Index- und Static-File-Module in das Binary ein; Abschnitt 8 nennt sie ausdrücklich, weil das Kompatibilitätsladen deaktiviert bleibt. Ein normales lighttpd-Paket besitzt den Entity-Body-Hook nicht und kann dieses ausgewählte Modul nicht als gleichwertigen Weg laden.

Der Hostpfad wird hier nur erneut gesetzt, damit die Connectorbefehle den Host aus Abschnitt 6 verwenden können, ohne ihn erneut zu bauen.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/lighttpd"
export LIGHTTPD_PATCHED_SRC="$HOST_BUILD_BASE/lighttpd-1.4.84-patched"
export LIGHTTPD_BUILD_DIR="${LIGHTTPD_BUILD_DIR:-$LIGHTTPD_PATCHED_SRC}"
export LIGHTTPD_PREFIX="$HOME/.local/lighttpd-modsecurity"
cd "$CONNECTOR_ROOT"
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export LIGHTTPD_MODULE_DIR="$BUILD_ROOT/modules"
BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_CONNECTOR_OUT_DIR="$BUILD_ROOT/connector" LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" LIGHTTPD_MSCONNECTOR_CORE_MODE=patched LIGHTTPD_SOURCE_DIR="$LIGHTTPD_PATCHED_SRC" LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_DIR" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/lighttpd/build/build_module.sh"
export LIGHTTPD_MODULE="$LIGHTTPD_MODULE_DIR/mod_msconnector.so"
test -f "$LIGHTTPD_MODULE"
```

## 8. Konfiguration

Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.

```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export LIGHTTPD_RUNTIME_CONFIG="$HOST_BUILD_BASE/msconnector-runtime.conf"
export LIGHTTPD_CONFIG="$HOST_BUILD_BASE/lighttpd-local.conf"
export LIGHTTPD_DOCUMENT_ROOT="$HOST_BUILD_BASE/htdocs"
mkdir -p "$LIGHTTPD_DOCUMENT_ROOT"
printf "lighttpd modsecurity test\n" > "$LIGHTTPD_DOCUMENT_ROOT/index.html"
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
server.modules = ( "mod_indexfile", "mod_msconnector", "mod_staticfile" )
index-file.names = ( "index.html" )
server.bind = "127.0.0.1"
server.port = 8080
server.document-root = "$LIGHTTPD_DOCUMENT_ROOT"
server.pid-file = "$HOST_BUILD_BASE/lighttpd.pid"
server.errorlog = "$HOST_BUILD_BASE/lighttpd-error.log"
msconnector.enabled = "enable"
msconnector.config-file = "$LIGHTTPD_RUNTIME_CONFIG"
EOF
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$LIGHTTPD_PREFIX/sbin/lighttpd" -tt -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR"
"$LIGHTTPD_PREFIX/sbin/lighttpd" -V
file "$LIGHTTPD_MODULE"
ldd "$LIGHTTPD_MODULE" | grep -F libmodsecurity | grep -Fv "not found"
nm -D "$LIGHTTPD_MODULE" | grep -E "mod_msconnector_plugin_init$"
nm "$LIGHTTPD_PREFIX/sbin/lighttpd" | grep -E "mod_(indexfile|staticfile)_plugin_init$"
grep -F LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$LIGHTTPD_PATCHED_SRC/src/plugin.h"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

```sh
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$LIGHTTPD_PREFIX/sbin/lighttpd" -D -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR" &
lighttpd_pid=$!
attempt=0
while [ "$attempt" -lt 50 ]; do
    if ! kill -0 "$lighttpd_pid" 2>/dev/null; then
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
git -C "$CONNECTOR_ROOT" pull --ff-only
git -C "$CONNECTOR_ROOT" submodule update --init --recursive
# Rebuild the selected host and connector with the commands above.
```

## 14. Deinstallation und Cleanup

Keine Dateien pauschal nach `/usr/lib` kopieren und keine globalen Verzeichnisse entfernen. Bei einem Benutzer-Prefix ist kein `sudo` nötig. Evidence oder Logs erst nach bewusster Prüfung entfernen.

```sh
test ! -e "$HOME/connector-build/lighttpd" || find "$HOME/connector-build/lighttpd" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/.local/lighttpd-modsecurity" || find "$HOME/.local/lighttpd-modsecurity" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Wenn der Patch-Dry-Run fehlschlägt, ihn nicht erzwingen: die exakte 1.4.84-Quelle und Patch-Prüfsumme prüfen. Kann das Modul nicht geladen werden, gepatchten Core und Modul aus demselben Source-/Header-/Konfigurationssatz neu bauen.

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
| lighttpd_pid | Lokale Prozess-ID des gestarteten lighttpd aus $!; nur im selben Shell-Lauf verwenden. |
| LIGHTTPD_PATCHED_SRC | Disponierbare gepatchte Kopie der ausgewählten Quelle. |
| LIGHTTPD_BUILD_DIR | Out-of-tree-Buildverzeichnis des gepatchten lighttpd. |
| LIGHTTPD_PREFIX | Privater Installationsprefix des gepatchten Hosts. |
| LIGHTTPD_SOURCE_DIR | Dem Connectormodul-Builder übergebener gepatchter lighttpd-Source-Baum. |
| LIGHTTPD_BUILD_ROOT | Passender gepatchter lighttpd-Buildbaum mit generierten Headern und config.h. |
| LIGHTTPD_CONNECTOR_OUT_DIR | Externes Zwischen-Ausgabeverzeichnis des Connectormodul-Builds. |
| LIGHTTPD_MSCONNECTOR_CORE_MODE | Builder-Modus, der die ABI des gepatchten lighttpd-Cores verlangt. |
| LIGHTTPD_MODULE_DIR | Externes Verzeichnis für das passende Connectormodul. |
| LIGHTTPD_MODULE | Pfad des gebauten passenden Moduls. |
| LIGHTTPD_RUNTIME_CONFIG | Connector-Laufzeitkonfiguration für Regeln/Modus. |
| LIGHTTPD_DOCUMENT_ROOT | Externes Document-Root mit der expliziten Loopback-Testseite. |
| LIGHTTPD_CONFIG | Lokale lighttpd-Serverkonfiguration. |
| WORKDIR | Externes lighttpd-Source-Arbeitsverzeichnis. |
| VERSION | Vom Repository-Patch verlangte exakte lighttpd-Version. |
| INSTALL_DIR | Privater Installationsprefix des gepatchten lighttpd. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
