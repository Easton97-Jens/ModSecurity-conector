<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: NGINX

**Sprache:** [English](nginx.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-nginx-http-module` bei NGINX. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, ein offizieller NGINX-Source-Release, der repository-eigene dynamische NGINX-Connector, die Common-Integration, eine lokale Regeldatei und eine NGINX-Instanz auf Loopback.

## Connector in diesem Repository

- [NGINX-Connector](../../../connectors/nginx/README.de.md)
- [NGINX-Modulkonfiguration](../../../connectors/nginx/config)
- [Produktive NGINX-Quellen](../../../connectors/nginx/src/)
- [Source-Zuordnung](../../../connectors/nginx/SOURCE_MAP.json)

Dies ist der primäre Connectorpfad dieser Anleitung: connectors/nginx/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.

Abschnitt 7 baut diesen adaptereigenen Connector als dokumentiertes dynamisches NGINX-Modul; die offizielle Hostdokumentation stellt nur die NGINX-Hostquelle oder den Paketkontext bereit.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Building nginx from Sources](https://nginx.org/en/docs/configure.html)
  Die offiziellen Configure-Optionen einschließlich Prefix-Pfaden, Kompatibilität sowie Compiler- und Linkerflags. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (NGINX options are release-dependent; inspect `./configure --help` for the selected source archive.)
- **Quelle und Umfang:** [Official NGINX packages](https://nginx.org/en/linux_packages.html)
  Offizielle Distributionsrepositories und Paketinstallationskontext; kein ABI-Gleichwertigkeitsclaim für ein aus Source gebautes Modul. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Package layout changes by distribution and release.)

## Alternative: offizieller Upstream-Connector

Der offizielle Upstream-Connector [ModSecurity-nginx](https://github.com/owasp-modsecurity/ModSecurity-nginx) ist eine alternative Implementierung.

Diese Anleitung verwendet standardmäßig den Connector aus [`connectors/nginx/`](../../../connectors/nginx/README.de.md), weil dieser die repository-eigene Common-Integration, Konfiguration und die hier getesteten Anpassungen enthält. Ein Upstream-only-Build ist ein anderer Buildpfad und nicht automatisch gleichwertig mit dem ausgewählten Repository-Connector.

## 4. Voraussetzungen

Zuerst libmodsecurity mit der gemeinsamen Anleitung bauen. Danach die dokumentierten Entwicklungswerkzeuge des ausgewählten Hosts installieren und Host, Connector, Header sowie Libraries kompatibel halten.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```



## 5. ModSecurity vorbereiten

Installiere zuerst libmodsecurity v3:

[Einfacher libmodsecurity-v3-Build](libmodsecurity.de.md)

Danach werden NGINX und der repository-eigene NGINX-Connector gebaut.

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

Nur die ausgewählte offizielle NGINX-Hostquelle herunterladen. Die Repository-Source-of-Truth pinnt derzeit `NGINX_RELEASE_TAG=release-1.31.2`; dies entspricht dem unten verwendeten offiziellen Archiv `1.31.2`. Dabei wird kein Connector aus einem anderen Repository geladen: Der Connector liegt bereits in diesem Checkout unter `connectors/nginx/`.

```sh
WORKDIR="$HOME/nginx-modsecurity"
VERSION="1.31.2"
```

#### Hostquelle herunterladen und entpacken

Dies prüft das ausgewählte NGINX-Archiv vor dem Entpacken und erstellt nur den Host-Source-Baum. Vor der GPG-Prüfung den NGINX-Release-Signaturschlüssel von der offiziellen Release-Seite importieren. Abschnitt 7 fügt den repository-eigenen dynamischen Connector aus dem aktuellen Checkout hinzu.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz"
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz.asc"
gpg --verify "nginx-$VERSION.tar.gz.asc" "nginx-$VERSION.tar.gz"
tar -xzf "nginx-$VERSION.tar.gz"
```

### Was wurde installiert oder gebaut?

Es wurde noch kein Hostbinary oder Modul gebaut. Die NGINX-Quelle ist für Abschnitt 7 bereit, und der repository-eigene Connector bleibt in diesem Checkout unter `connectors/nginx/`.

### Erfolg prüfen

Diese Datei zeigt, dass die ausgewählte Upstream-NGINX-Source-Eingabe vorhanden ist.

```sh
test -f "$WORKDIR/nginx-$VERSION/configure"
```

### Source-Build und Integritätsprüfung

## 7. Connector bauen und einbinden

Abschnitt 6 hat nur die NGINX-Hostquelle bereitgestellt. Der adaptereigene Connector liegt bereits in diesem Checkout unter `connectors/nginx/`; ihn als ausgewähltes dynamisches NGINX-Modul bauen. Die Common- und libmodsecurity-Pfade unten sind bewusst explizit, damit das dynamische Modul aus denselben Repository- und Engine-Eingaben gebaut wird. `make install` installiert das dynamische Modul in den konfigurierten Modulpfad; es nicht ein zweites Mal kopieren.

```sh
INSTALL_DIR="$HOME/.local/nginx-modsecurity"
JOBS=2
cd "$WORKDIR/nginx-$VERSION"
MODSECURITY_INC="$MODSECURITY_INCLUDE_DIR"
MODSECURITY_LIB="$MODSECURITY_LIB_DIR"
MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include" \
MSCONNECTOR_COMMON_SRC="$CONNECTOR_ROOT/common/src" \
MODSECURITY_INC="$MODSECURITY_INC" \
MODSECURITY_LIB="$MODSECURITY_LIB" \
./configure \
  --prefix="$INSTALL_DIR" \
  --sbin-path="$INSTALL_DIR/sbin/nginx" \
  --modules-path="$INSTALL_DIR/modules" \
  --conf-path="$INSTALL_DIR/conf/nginx.conf" \
  --pid-path="$INSTALL_DIR/logs/nginx.pid" \
  --error-log-path="$INSTALL_DIR/logs/error.log" \
  --http-log-path="$INSTALL_DIR/logs/access.log" \
  --with-compat \
  --add-dynamic-module="$CONNECTOR_ROOT/connectors/nginx"
make -j"$JOBS"
make install
```

## 8. Konfiguration

Eine lokale Testregel und nginx.conf erstellen. Der primäre Connector ist ein dynamisches Modul; deshalb lädt nginx.conf es vor den Blöcken events und http. Dieser Abschnitt schreibt nur Konfiguration; Abschnitt 10 validiert und startet sie.

```sh
RULES_FILE="$WORKDIR/modsecurity-local.conf"
NGINX_CONFIG="$INSTALL_DIR/conf/nginx.conf"
NGINX_DOCROOT="$WORKDIR/htdocs"
mkdir -p "$NGINX_DOCROOT"
printf "nginx modsecurity test\n" > "$NGINX_DOCROOT/index.html"
cat > "$RULES_FILE" <<'EOF'
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$NGINX_CONFIG" <<EOF
load_module modules/ngx_http_modsecurity_module.so;

events {}
http {
    server {
        listen 127.0.0.1:8080;
        modsecurity on;
        modsecurity_rules_file "$RULES_FILE";
        location = /__modsec_ready {
            modsecurity off;
            return 204;
        }
        location / {
            root "$NGINX_DOCROOT";
            index index.html;
        }
    }
}
EOF
```

Für den vollständigen Direktivenvertrag vor der Anpassung dieses lokalen Beispiels die repository-eigene [NGINX-Konfigurationsreferenz](../../../examples/nginx/configuration-reference.de.md) lesen.

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
test -x "$INSTALL_DIR/sbin/nginx"
test -f "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so"
"$INSTALL_DIR/sbin/nginx" -V
"$INSTALL_DIR/sbin/nginx" -V 2>&1 | grep -F -- "--add-dynamic-module=$CONNECTOR_ROOT/connectors/nginx"
file "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so"
ldd "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so" | grep -F libmodsecurity | grep -Fv "not found"
test -f "$RULES_FILE"
test -f "$NGINX_CONFIG"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

Zuerst die Syntax prüfen, dann den lokalen Host starten, eine normale und eine geblockte Loopback-Anfrage senden und ihn wieder stoppen.

```sh
"$INSTALL_DIR/sbin/nginx" -t -p "$INSTALL_DIR" -c conf/nginx.conf
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf -s quit
```

## 11. Paketgestützter Weg

Status: `package-assisted source build`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.

Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.

```sh
apt-cache search nginx
dnf search nginx
nginx -V 2>&1 || true
```

Ein offizielles Paket kann einen Host bereitstellen, ist aber nicht mit diesem aus Source gebauten NGINX-/Connectorpaar austauschbar. Vor der Wahl eines anderen Host-Builds die offizielle NGINX-Paketseite und die Ausgabe `nginx -V` des Pakets prüfen.

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
git -C "$CONNECTOR_ROOT" pull --ff-only
git -C "$CONNECTOR_ROOT" submodule update --init --recursive
# Rebuild the selected host and connector with the commands above.
```

## 14. Deinstallation und Cleanup

Keine Dateien pauschal nach `/usr/lib` kopieren und keine globalen Verzeichnisse entfernen. Bei einem Benutzer-Prefix ist kein `sudo` nötig. Evidence oder Logs erst nach bewusster Prüfung entfernen.

```sh
test ! -e "$HOME/nginx-modsecurity" || find "$HOME/nginx-modsecurity" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/.local/nginx-modsecurity" || find "$HOME/.local/nginx-modsecurity" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Ein Start- oder Direktivenfehler bedeutet normalerweise, dass NGINX-Binary, Configure-Argumente für das dynamische Modul, Repository-Connector oder installierte Library voneinander abweichen. Das Paar gemeinsam neu bauen; nicht mit einer fremden Paketinstallation kombinieren.

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
| MSCONNECTOR_COMMON_INC | An die NGINX-Modulkonfiguration übergebenes Repository-Common-Headerverzeichnis. |
| MSCONNECTOR_COMMON_SRC | In das NGINX-Modul kompilierte Repository-Common-Quelldateien. |
| MODSECURITY_INC | Aus dem gemeinsamen Build ausgewähltes libmodsecurity-Headerverzeichnis. |
| MODSECURITY_LIB | Aus dem gemeinsamen Build ausgewähltes libmodsecurity-Bibliotheksverzeichnis. |
| NGINX_CONFIG | Lokale NGINX-Konfiguration für den Loopback-Test. |
| NGINX_DOCROOT | Externes lokales Document-Root des geschützten Static-Content-Tests. |
| WORKDIR | Externes NGINX-Host-Source-Arbeitsverzeichnis. |
| VERSION | Ausgewählter offizieller NGINX-Release. |
| INSTALL_DIR | Privater NGINX-Installationsprefix für den Dynamic-Module-Build. |
| JOBS | Bewusst kleine Anzahl paralleler NGINX-Buildjobs. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
