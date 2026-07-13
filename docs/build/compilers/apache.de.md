<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manueller Source-Build: Apache HTTP Server

**Sprache:** [English](apache.md) | Deutsch

## 1. Zweck und ausgewählter Integrationspfad

Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `native-httpd-module` bei Apache HTTP Server. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.

## 2. Komponenten des Builds

libmodsecurity v3, Apache HTTP Server 2.4, APR/APR-util, PCRE2, der Repository-Apache-Adapter, APXS, eine lokale Regeldatei und eine httpd-Instanz auf Loopback.

## Connector in diesem Repository

- [Apache-Connector](../../../connectors/apache/README.de.md)
- [Produktive Apache-Quellen](../../../connectors/apache/src/)
- [Autotools-Konfiguration](../../../connectors/apache/configure.ac)
- [Source-Zuordnung](../../../connectors/apache/SOURCE_MAP.json)

Dies ist der primäre Connectorpfad dieser Anleitung: connectors/apache/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.

Abschnitt 7 materialisiert diese adaptereigene Quelle in einen externen Autotools-Worktree und baut sie mit dem ausgewählten APXS-/httpd-Paar.

## 3. Offizielle Upstream-Dokumentation

- **Quelle und Umfang:** [Compiling and Installing](https://httpd.apache.org/docs/2.4/install.html)
  Offizieller Apache-Quellrelease sowie Voraussetzungen für APR/APR-util und PCRE2, Configure, Make, Installation, Start und Stop. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (HTTP Server 2.4; choose and verify the release again before building.)
- **Quelle und Umfang:** [APXS](https://httpd.apache.org/docs/2.4/programs/apxs.html)
  Die DSO-Build-/Installationsschnittstelle und die Abfragen, die ein Modul an genau einen httpd-Build binden. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (HTTP Server 2.4 APXS reference.)
- **Quelle und Umfang:** [Apache HTTP Server Download](https://httpd.apache.org/download.cgi)
  Offizielle Releasearchive, PGP-Signaturen, Prüfsummen und Apache KEYS. Versionsbezug: Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. (The page changes when Apache publishes a release.)

## Alternative: offizieller Upstream-Connector

Der offizielle Upstream-Connector [ModSecurity-apache](https://github.com/owasp-modsecurity/ModSecurity-apache) ist eine alternative Implementierung.

Der Hauptweg dieser Anleitung verwendet den repository-eigenen Adapter unter [`connectors/apache/`](../../../connectors/apache/README.de.md). Ein separater Upstream-Build enthält nicht automatisch die repository-eigene Common-Integration und ist nicht automatisch mit dem hier geprüften Pfad gleichwertig.

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

Die folgenden Connector-Befehle setzen die Standardinstallation unter `/usr/local` voraus. Für einen benutzerlokalen Prefix den fortgeschrittenen Abschnitt der gemeinsamen Anleitung verwenden und Include- sowie Library-Pfade bewusst übergeben.

## 6. Host oder Proxy bereitstellen

### Einfacher Weg

Für den einfachsten lokalen Adapterbuild ein Apache-Paket zusammen mit seinem Entwicklungspaket installieren. Das Entwicklungspaket liefert APXS und die passenden Header.

#### Debian / Ubuntu

Host und zugehöriges APXS-/Header-Paket aus der Distribution installieren.

```sh
sudo apt update
sudo apt install apache2 apache2-dev
```

#### Fedora / RHEL

Die entsprechenden httpd- und Entwicklungspakete installieren.

```sh
sudo dnf install httpd httpd-devel
```

### Was wurde installiert oder gebaut?

Der Paketweg stellt Apache httpd, APXS, das Modulverzeichnis und die Header für ein Modul dieses konkreten Hosts bereit.

### Erfolg prüfen

Diese Abfragen zeigen Host-Prefix, Headerverzeichnis, Modulverzeichnis und Apache-Version. Sie müssen dieselbe Apache-Installation beschreiben.

```sh
apxs -q PREFIX
apxs -q INCLUDEDIR
apxs -q LIBEXECDIR
apachectl -v
```

### Source-Build und Integritätsprüfung

#### Optional: Apache vollständig aus Source bauen

APR und APR-util sind Apache-Portable-Bibliotheken. Passende System-Entwicklungspakete verwenden oder verifizierte APR- und APR-util-Source-Bäume vor dem Configure unter srclib ablegen.

```sh
WORKDIR="$HOME/connector-build/apache"
VERSION="2.4.68"
INSTALL_DIR="$HOME/.local/apache-modsecurity"
```

#### Herunterladen und entpacken

Dies erstellt einen isolierten Source-Baum; der Adapter wird dadurch noch nicht gebaut.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2"
tar -xjf "httpd-$VERSION.tar.bz2"
```

#### Host bauen

Apache in den privaten Prefix konfigurieren und installieren. Der Connector bleibt Arbeit für Abschnitt 7.

```sh
cd "httpd-$VERSION"
./configure --prefix="$INSTALL_DIR" --enable-mods-shared=most --with-pcre="$(command -v pcre2-config)"
make -j2
make install
```

#### Source-Host-Ausgaben prüfen

Diese Prüfungen bestätigen, dass der private Source-Host genau das APXS-/Executable-Paar bereitstellt, das Abschnitt 7 verwenden muss.

```sh
test -x "$INSTALL_DIR/bin/httpd"
test -x "$INSTALL_DIR/bin/apachectl"
test -x "$INSTALL_DIR/bin/apxs"
"$INSTALL_DIR/bin/apxs" -q PREFIX
```

#### Optional: Download und Version verifizieren

Vor der Signaturprüfung den Apache-Release-Schlüssel von der offiziellen Downloadseite importieren.

```sh
cd "$WORKDIR"
curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2.sha256"
curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2.asc"
sha256sum -c "httpd-$VERSION.tar.bz2.sha256"
gpg --verify "httpd-$VERSION.tar.bz2.asc" "httpd-$VERSION.tar.bz2"
```

## 7. Connector bauen und einbinden

Der in dieser Anleitung verwendete Adapter befindet sich unter [connectors/apache](../../../connectors/apache/README.de.md). Der produktive Modulcode liegt unter [connectors/apache/src](../../../connectors/apache/src/). Das in Abschnitt 6 geprüfte APXS verwenden; der Paketweg stellt normalerweise apxs bereit, während die optionale Source-Host-Zuweisung unten das passende private APXS ausdrücklich auswählt. Der unterstützte Materialisierungsschritt hält erzeugte Autotools-Templates in einem externen Worktree, während connectors/apache/ die maßgebliche Adapterquelle bleibt.

#### Optional: Source-Host-APXS auswählen

Wenn der optionale Apache-Source-Host aus Abschnitt 6 gebaut wurde, diese Zuweisung vor den Adapterbefehlen in derselben Shell ausführen. Nutzer des Pakethosts überspringen sie.

```sh
APXS="$HOME/.local/apache-modsecurity/bin/apxs"
```

#### Adapter materialisieren, bauen und installieren

configure.ac akzeptiert --with-apache als optionales Lookup-Override, aber diese Anleitung übergibt das aus dem ausgewählten APXS abgeleitete httpd ausdrücklich. Der Repository-Buildhelper verwendet dieselbe Paarung und verhindert so, dass der Adapter gegen ein anderes Hostbinary konfiguriert wird.

```sh
APXS="${APXS:-apxs}"
HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"
cd "$CONNECTOR_ROOT/connectors/apache"
test -f "$CONNECTOR_ROOT/connectors/apache/configure.ac"
mkdir -p "$HOME/connector-build/apache"
CONNECTOR_BUILD_DIR="$(mktemp -d "$HOME/connector-build/apache/connector-src.XXXXXX")"
```

```sh
CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$CONNECTOR_ROOT/modules/ModSecurity-test-Framework/ci/provisioning/materialize-connector-source.sh" --connector apache --adapter-dir "$CONNECTOR_ROOT/connectors/apache" --dest-dir "$CONNECTOR_BUILD_DIR"
cd "$CONNECTOR_BUILD_DIR"
./autogen.sh
./configure --with-libmodsecurity="/usr/local" --with-apxs="$APXS" --with-apache="$HTTPD_BIN"
make -j2
make install
```

```sh
MODULE_PATH="$("$APXS" -q LIBEXECDIR)/mod_security3.so"
test -f "$MODULE_PATH"
```

## 8. Konfiguration

Die lokale Testregel und eigenständige Apache-Konfiguration erstellen. Dieser Abschnitt startet Apache nicht; Abschnitt 10 führt Syntaxprüfung und Loopback-Anfragen aus.

```sh
APXS="${APXS:-apxs}"
HTTPD_PREFIX="$("$APXS" -q PREFIX)"
HTTPD_BIN="$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)"
RULES_FILE="$HOME/connector-build/apache/modsecurity-local.conf"
HTTPD_CONFIG="$HOME/connector-build/apache/httpd-local.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
```

```sh
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
```

## 9. Build- und ABI-Validierung

Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.

```sh
"$HTTPD_BIN" -v
"$HTTPD_BIN" -M | grep -E "(^|[[:space:]])so_module"
"$APXS" -q PREFIX
"$APXS" -q INCLUDEDIR
"$APXS" -q LIBEXECDIR
file "$MODULE_PATH"
```

```sh
ldd "$MODULE_PATH" | grep -F libmodsecurity
```

## 10. Lokaler HTTP/1.1-Funktionstest

Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.

```sh
"$HTTPD_BIN" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -t
"$HTTPD_BIN" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -k start
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$HTTPD_BIN" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -k stop
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

Wenn `apxs -q` auf andere Header oder ein anderes Modulverzeichnis als das laufende httpd zeigt, stoppen und den Adapter neu bauen. Ein gegen eine Apache-ABI gebautes Modul darf nicht von einer anderen geladen werden.

## 16. Variablen und Platzhalter

| Variable/Platzhalter | Bedeutung |
| --- | --- |
| CONNECTOR_ROOT | Git-Top-Level dieses Repository-Checkouts; die Connector-Skripte werden von dort aus aufgerufen. |
| RULES_FILE | Lokale Testregeldatei; keine CRS-Regeldatei. |
| VERIFIED_RUN_PARENT | Externer Elternordner eines frischen Repository-Testcheckouts und seiner Testartefakte. |
| run_id | Eindeutige Kennung eines repository-gesteuerten Full-Lifecycle-Laufs. |
| NO_CRS_RUN_ID | Exportierte Full-Lifecycle-Kennung für den nachfolgenden Make-Aufruf; sie hält Evidence und Laufzeitdaten getrennt. |
| HTTPD_PREFIX | Privater httpd-Installationsprefix. |
| APXS | APXS desselben Hosts, der das Modul lädt. |
| CONNECTOR_BUILD_DIR | Externer materialisierter Autotools-Worktree für den Repository-Apache-Adapter. |
| HTTPD_BIN | httpd-Executable, das beim Configure ausdrücklich mit APXS gepaart wird. |
| MODULE_PATH | Durch APXS aufgelöstes installiertes Repository-DSO. |
| HTTPD_CONFIG | Lokale eigenständige httpd-Konfiguration. |
| WORKDIR | Externes Apache-Source-Arbeitsverzeichnis. |
| VERSION | Ausgewählter Apache-Source-Release im optionalen Source-Weg. |
| INSTALL_DIR | Privater Apache-Installationsprefix im optionalen Source-Weg. |

## 17. Grenzen und nicht erhobene Claims

Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.
