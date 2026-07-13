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

## 6. Host oder Proxy vorbereiten beziehungsweise bauen

Der einfache NGINX-Weg verwendet nur ein Arbeitsverzeichnis, ein Installationsverzeichnis und eine bewusst kleine Anzahl Buildjobs. Er baut den Connector statisch mit dem NGINX-Binary; libmodsecurity wird dabei nicht erneut gebaut.

1. NGINX herunterladen.
2. ModSecurity-nginx klonen.
3. configure ausführen.
4. make ausführen.
5. make install ausführen.
6. nginx.conf erstellen.
7. nginx -t ausführen.
8. Curl-Test ausführen.

```sh
WORKDIR="$HOME/nginx-modsecurity"
INSTALL_DIR="$HOME/.local/nginx-modsecurity"
JOBS=2
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO https://nginx.org/download/nginx-1.31.2.tar.gz
tar -xzf nginx-1.31.2.tar.gz
git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git
cd nginx-1.31.2
./auto/configure --prefix="$INSTALL_DIR" --with-http_ssl_module --add-module="$WORKDIR/ModSecurity-nginx" --with-cc-opt="-I/usr/local/include" --with-ld-opt="-L/usr/local/lib"
make -j"$JOBS"
make install
cat > "$WORKDIR/modsecurity-local.conf" <<'EOF'
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$INSTALL_DIR/conf/nginx.conf" <<EOF
events {}
http {
    server {
        listen 127.0.0.1:8080;
        location / {
            modsecurity on;
            modsecurity_rules_file "$WORKDIR/modsecurity-local.conf";
            return 200 "nginx modsecurity test\n";
        }
    }
}
EOF
"$INSTALL_DIR/sbin/nginx" -t -p "$INSTALL_DIR" -c conf/nginx.conf
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf -s quit
```

## 7. Connector bauen und einbinden

NGINX und ModSecurity-nginx wurden im vorhergehenden einfachen Build gemeinsam geklont, konfiguriert, kompiliert und installiert.

## 8. Konfiguration

Der einfache Build oben schreibt die lokale Regeldatei und nginx.conf und führt anschließend den erforderlichen NGINX-Konfigurationstest aus.

Für den vollständigen Direktivenvertrag vor der Anpassung dieses lokalen Beispiels die repository-eigene [NGINX-Konfigurationsreferenz](../../../examples/nginx/configuration-reference.de.md) lesen.

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$INSTALL_DIR/sbin/nginx" -V
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

Der einfache Build startet NGINX auf Loopback und verwendet curl für eine normale und eine geblockte Anfrage, bevor er ihn beendet.

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

| Variable | Bedeutung |
| --- | --- |
| WORKDIR | Arbeitsverzeichnis für NGINX-Quelle, Connector und lokale Regeldatei. |
| INSTALL_DIR | Privates NGINX-Installationsverzeichnis. |
| JOBS | Bewusst kleine Anzahl paralleler NGINX-Buildjobs. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
