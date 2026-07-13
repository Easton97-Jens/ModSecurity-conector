<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: NGINX

**Sprache:** [English](nginx.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-nginx-http-module` bei NGINX. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, ein offizieller NGINX-Source-Release, ModSecurity-nginx, ein statisch eingebundenes NGINX-Modul, eine lokale Regeldatei und eine NGINX-Instanz auf Loopback.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Building nginx from Sources](https://nginx.org/en/docs/configure.html)
  Die offiziellen Configure-Optionen einschließlich Prefix-Pfaden, Kompatibilität sowie Compiler- und Linkerflags. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (NGINX options are release-dependent; inspect `./auto/configure --help` for the selected source.)
- **Quelle und Umfang:** [Official NGINX packages](https://nginx.org/en/linux_packages.html)
  Offizielle Distributionsrepositories und Paketinstallationskontext; kein ABI-Gleichwertigkeitsclaim für ein aus Source gebautes Modul. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Package layout changes by distribution and release.)
- **Quelle und Umfang:** [ModSecurity-nginx](https://github.com/owasp-modsecurity/ModSecurity-nginx)
  Die offizielle NGINX-Connectorquelle, die vom NGINX-Configure-Schritt eingebunden wird. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (Pin it to a release tag or commit matching the selected NGINX source.)

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

Danach werden NGINX und ModSecurity-nginx gebaut.

Die folgenden Connector-Befehle setzen die Standardinstallation unter `/usr/local` voraus. Für einen benutzerlokalen Prefix den fortgeschrittenen Abschnitt der gemeinsamen Anleitung verwenden und Include- sowie Library-Pfade bewusst übergeben.

## 6. Host oder Proxy bereitstellen

### Einfacher Weg

Die ausgewählte NGINX-Quelle und die ModSecurity-nginx-Connectorquelle herunterladen. Das bereitet nur die Eingaben vor; Abschnitt 7 baut den statischen Connector.

```sh
WORKDIR="$HOME/nginx-modsecurity"
VERSION="1.31.2"
```

#### Host- und Connectorquellen herunterladen

Die beiden Source-Bäume sind alles, was Abschnitt 7 benötigt, um NGINX mit dem Connector zu konfigurieren.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz"
tar -xzf "nginx-$VERSION.tar.gz"
git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git
```

### Was wurde installiert oder gebaut?

Es wurde noch kein Hostbinary oder Modul gebaut. NGINX-Quelle und ModSecurity-nginx-Checkout sind für die Connector-Integration in Abschnitt 7 bereit.

### Erfolg prüfen

Beide Dateien zeigen, dass die erwarteten Upstream-Source-Eingaben vorhanden sind.

```sh
test -f "$WORKDIR/nginx-$VERSION/auto/configure"
test -f "$WORKDIR/ModSecurity-nginx/config"
```

### Source-Build und Integritätsprüfung

#### Optional: Download und Version verifizieren

Vor der Prüfung der abgetrennten Signatur den NGINX-Release-Schlüssel von der offiziellen Release-Seite importieren. Connector-Tag und aufgelöster Commit werden getrennt vom Einsteigerweg dokumentiert.

```sh
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz.asc"
gpg --verify "nginx-$VERSION.tar.gz.asc" "nginx-$VERSION.tar.gz"
git -C "$WORKDIR/ModSecurity-nginx" checkout --detach v1.0.4
test "$(git -C "$WORKDIR/ModSecurity-nginx" rev-parse HEAD)" = "3f4b57df10ce43b1f1c722141f7621dc64838be8"
```

## 7. Connector bauen und einbinden

Abschnitt 6 hat NGINX- und ModSecurity-nginx-Source-Bäume bereitgestellt. Sie werden nun gemeinsam gebaut, wobei der Connector statisch in das ausgewählte NGINX-Binary eingebunden wird.

```sh
INSTALL_DIR="$HOME/.local/nginx-modsecurity"
JOBS=2
cd "$WORKDIR/nginx-$VERSION"
./auto/configure --prefix="$INSTALL_DIR" --with-http_ssl_module --add-module="$WORKDIR/ModSecurity-nginx" --with-cc-opt="-I/usr/local/include" --with-ld-opt="-L/usr/local/lib"
make -j"$JOBS"
make install
```

```sh
test -x "$INSTALL_DIR/sbin/nginx"
```

## 8. Konfiguration

Eine lokale Testregel und nginx.conf erstellen. Dieser Abschnitt schreibt nur Konfiguration; Abschnitt 10 validiert und startet sie.

```sh
RULES_FILE="$WORKDIR/modsecurity-local.conf"
NGINX_CONFIG="$INSTALL_DIR/conf/nginx.conf"
cat > "$RULES_FILE" <<'EOF'
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$NGINX_CONFIG" <<EOF
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
```

Für den vollständigen Direktivenvertrag vor der Anpassung dieses lokalen Beispiels die repository-eigene [NGINX-Konfigurationsreferenz](../../../examples/nginx/configuration-reference.de.md) lesen.

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$INSTALL_DIR/sbin/nginx" -V
test -x "$INSTALL_DIR/sbin/nginx"
"$INSTALL_DIR/sbin/nginx" -V 2>&1 | grep -F -- "--add-module=$WORKDIR/ModSecurity-nginx"
test -f "$RULES_FILE"
test -f "$NGINX_CONFIG"
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

Zuerst die Syntax prüfen, dann den lokalen Host starten, eine normale und eine geblockte Loopback-Anfrage senden und ihn wieder stoppen.

```sh
"$INSTALL_DIR/sbin/nginx" -t -p "$INSTALL_DIR" -c conf/nginx.conf
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
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
find "$HOME/src/modsecurity-connectors" -maxdepth 2 -mindepth 1 -print
# Review the listed paths first; remove only a chosen external host-build directory.
```

## 15. Troubleshooting

Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.

Ein Start- oder Direktivenfehler bedeutet normalerweise, dass NGINX-Binary, Configure-Argumente, Connector-Checkout oder installierte Library voneinander abweichen. Das Paar gemeinsam neu bauen; nicht mit einer fremden Paketinstallation kombinieren.

## 16. Variablen und Platzhalter

| Variable/Platzhalter | Bedeutung |
| --- | --- |
| CONNECTOR_ROOT | Git-Top-Level dieses Repository-Checkouts; die Connector-Skripte werden von dort aus aufgerufen. |
| HOST_BUILD_BASE | Connector-spezifisches externes Verzeichnis für Quellen, Builds, Konfiguration und lokale Logs. |
| BUILD_ROOT | Externer Build- und Laufzeitstamm der repository-eigenen Connector-Komponenten. |
| RULES_FILE | Lokale Testregeldatei; keine CRS-Regeldatei. |
| VERIFIED_RUN_PARENT | Externer Elternordner eines frischen Repository-Testcheckouts und seiner Testartefakte. |
| run_id | Eindeutige Kennung eines repository-gesteuerten Full-Lifecycle-Laufs. |
| NO_CRS_RUN_ID | Exportierte Full-Lifecycle-Kennung für den nachfolgenden Make-Aufruf; sie hält Evidence und Laufzeitdaten getrennt. |
| upstream_pid | Lokale Prozess-ID des Test-Upstreams aus `$!`; nur im selben Shell-Lauf verwenden. |
| haproxy_pid | Lokale Prozess-ID des gestarteten HAProxy aus `$!`; nur im selben Shell-Lauf verwenden. |
| engine_pid | Lokale Prozess-ID des gestarteten Traefik-Engine-Service aus `$!`; nur im selben Shell-Lauf verwenden. |
| traefik_pid | Lokale Prozess-ID des gestarteten Traefik aus `$!`; nur im selben Shell-Lauf verwenden. |
| lighttpd_pid | Lokale Prozess-ID des gestarteten lighttpd aus `$!`; nur im selben Shell-Lauf verwenden. |
| NGINX_CONFIG | Lokale NGINX-Konfiguration für den Loopback-Test. |
| WORKDIR | NGINX-Source- und Connector-Arbeitsverzeichnis. |
| VERSION | Ausgewählter offizieller NGINX-Release. |
| INSTALL_DIR | Privater Installationsprefix des statischen NGINX. |
| JOBS | Bewusst kleine Anzahl paralleler NGINX-Buildjobs. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
