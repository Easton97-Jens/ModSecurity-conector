# Compile Apache


**Sprache:** [English](COMPILE_APACHE.md) | Deutsch

## Inhaltsverzeichnis

- [Zweck](#zweck)
- [Status und Grenzen](#status-und-grenzen)
- [Überblick: Drei Pfade](#überblick-drei-pfade)
- [Pfad 1: Repository-Smoke / Validierung](#pfad-1-repository-smoke--validierung)
- [Pfad 2: Externer Einsatz mit Distribution-Paketen](#pfad-2-externer-einsatz-mit-distribution-paketen)
- [Pfad 3: Externer Einsatz aus Source](#pfad-3-externer-einsatz-aus-source)
- [Config Snippets](#config-snippets)
- [Beispiel-Konfigurationen](#beispiel-konfigurationen)
- [Logs](#logs)
- [Troubleshooting](#troubleshooting)
- [Nicht-Claims](#nicht-claims)
- [Verwandte Dokumente](#verwandte-dokumente)

## Zweck

Dieser Guide beschreibt den Einsatz des Apache-Connectors außerhalb dieses
Repositorys: libmodsecurity bauen oder installieren, `mod_security3.so` gegen
das Ziel-Apache/APXS bauen, das Artefakt in ein externes Apache/httpd-Setup
kopieren, Konfiguration verdrahten und den ersten Syntax-Check oder Reload
ausführen.

## Status und Grenzen

Der Apache-Connector-Quellcode liegt unter `connectors/apache/`.
Repository-Smoke-Evidence validiert nur bestimmte Repository-Pfade. Sie belegt
nicht jedes Apache-Distribution-Paket, jedes MPM, jedes Modul-Layout oder jedes
RESPONSE_BODY- / Phase-4-Deployment.

## Überblick: Drei Pfade

| Pfad | Zweck | Haupteinsatz |
| --- | --- | --- |
| Pfad 1: Repository-Smoke | Repository-Evidence validieren | Entwickler / Reviewer |
| Pfad 2: Externer Einsatz mit Paketen | Distro-Pakete nutzen, wo kompatibel | Betreiber mit Systempaketen |
| Pfad 3: Externer Einsatz aus Source | ModSecurity und/oder Connector-Teile manuell bauen | Betreiber mit genauer Versionskontrolle |

## Pfad 1: Repository-Smoke / Validierung

Diese Befehle validieren Repository-Evidence. Sie sind nicht die externe
Installationsprozedur.

```sh
git submodule update --init --recursive
make setup-dev
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

Optionale breitere Repository-Evidence:

```sh
FORCE_ALL_CASES=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

## Pfad 2: Externer Einsatz mit Distribution-Paketen

1. Installieren Sie Apache/httpd, passende APXS-/Development-Header,
   Build-Werkzeuge und libmodsecurity-Development-Dateien. Paketnamen
   unterscheiden sich je Distribution; dieser Debian-/Ubuntu-artige Befehl ist
   nur ein Beispiel:

   ```sh
   sudo apt-get update
   sudo apt-get install -y apache2 apache2-dev build-essential libmodsecurity-dev
   ```

2. Paketbereitgestellte Komponenten können Apache/httpd, APXS, Header und
   libmodsecurity enthalten. `mod_security3.so` muss trotzdem aus diesem
   Repository gegen das Ziel-APXS gebaut werden.
3. Holen Sie den Connector-Quellcode dieses Repositorys:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

4. Bauen Sie den Connector gegen paketbereitgestelltes APXS/libmodsecurity.
   Wenn Sie den direkten Autotools-Pfad verwenden, prüfen Sie ihn für Ihr
   Zielsystem gegen `connectors/apache`-Dokumentation und -Quellen:

   ```sh
   cd connectors/apache
   ./autogen.sh
   ./configure --with-apxs=<target-apxs> --with-libmodsecurity=<libmodsecurity-prefix>
   make
   ```

5. Kopieren Sie das gebaute Modul und angepasste Konfiguration in das
   Zielsystem. Verwenden Sie Ihr Apache-Modulverzeichnis,
   Service-Konfigurationsverzeichnis, ModSecurity-Regelverzeichnis und
   Log-Verzeichnis; die Platzhalter unten sind nicht universell:

   > Hinweis: `install` ist hier kein Paketmanager-Befehl. Er kopiert Dateien
   > und kann Berechtigungen setzen. Zum Beispiel ist
   > `sudo install -m 0755 file.so /target/file.so` ähnlich zu
   > `sudo cp file.so /target/file.so` gefolgt von
   > `sudo chmod 0755 /target/file.so`.

   ```sh
   sudo install -d -m 0755 <modsecurity-config-dir> <modsecurity-log-dir>
   sudo install -m 0755 <built-mod_security3.so> <apache-module-dir>/mod_security3.so
   sudo install -m 0644 examples/apache/modsecurity-request-only.conf <modsecurity-config-dir>/modsecurity-request-only.conf
   sudo install -m 0644 examples/apache/apache-modsecurity-request-only.conf <apache-service-config-dir>/security3.conf
   sudo apachectl configtest
   sudo systemctl reload <apache-service-name>
   ```

APXS und Apache/httpd müssen zusammenpassen. Andernfalls kann das Modul zwar
gebaut werden, aber beim Laden oder zur Laufzeit fehlschlagen.

## Pfad 3: Externer Einsatz aus Source

1. Installieren Sie Compiler-/Build-Voraussetzungen und Apache/httpd APXS für
   die Zielinstallation.
2. Bauen Sie libmodsecurity v3 aus Source, falls Pakete nicht geeignet sind:

Installieren Sie zuerst die Build-Voraussetzungen für Ihr Betriebssystem.
Verwenden Sie dann entweder den von Ihrem Deployment ausgewählten
libmodsecurity-Ref oder ermitteln Sie vor dem Build den Repository-/Framework-
Pin. Das folgende Beispiel ist ein Upstream-Style-Beispiel, keine
repository-eigene Build-Garantie:

```sh
git clone --depth 1 -b <modsecurity-v3-ref> https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity-v3
cd ModSecurity-v3
git submodule update --init --recursive
./build.sh
./configure --prefix=<libmodsecurity-prefix>
make -j"$(nproc)"
sudo make install
```

Ersetzen Sie `<modsecurity-v3-ref>` und `<libmodsecurity-prefix>` durch vom
Betreiber gewählte Werte. Prüfen Sie Upstream-Voraussetzungen und Flags für Ihr
Betriebssystem.

3. Holen Sie den Connector-Quellcode dieses Repositorys von GitHub oder aus
   Ihrem Fork:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector/connectors/apache
   ```

4. Bauen Sie `mod_security3.so` mit dem Ziel-APXS und dem aus Source gebauten
   libmodsecurity-Prefix. Wenn der genaue Befehl für Ihre Plattform angepasst
   werden muss, prüfen Sie ihn gegen `connectors/apache/docs/build.md` und die
   Autotools-Dateien:

   ```sh
   ./autogen.sh
   ./configure --with-apxs=<target-apxs> --with-libmodsecurity=<libmodsecurity-prefix>
   make
   ```

5. Installieren/kopieren Sie das gebaute Modul mit dem Platzhalter-
   Installationsmuster aus Pfad 2, führen Sie `apachectl configtest` aus und
   reloaden oder restarten Sie danach den Ziel-Apache-Service.

## Config Snippets

```apache
LoadModule security3_module <module-path>/mod_security3.so

modsecurity on
modsecurity_rules_file <modsecurity-rules-file>
```

Siehe [examples/apache/README.de.md](examples/apache/README.de.md) für die
Erklärung dieser Direktiven, Platzhalter, Logs und Grenzen.

## Beispiel-Konfigurationen

Verwenden Sie die Dateien in [examples/apache/](examples/apache/README.de.md)
als Startpunkte für externe Konfiguration. Sie werden vom Repository nicht
automatisch installiert und sind keine universellen Produktionsdefaults.

## Logs

Prüfen Sie die relevanten Deployment-Logs; behandeln Sie die Pfade in den
Beispielen nicht als universelle Anforderungen.

- Webserver-/Proxy-Access-Logs.
- Webserver-/Proxy-Error-Logs.
- ModSecurity-Audit-Log, wenn aktiviert.
- Connector-Decision-Log, falls dieser Connector/Pfad eines hat.
- Sidecar-/Agent-Log, falls dieser Connector/Pfad eines hat.

## Troubleshooting

Prüfen Sie APXS-/Apache-ABI-Mismatch, fehlende Header, fehlende Shared
Libraries, falschen Apache-Konfigurationskontext, falschen Regelpfad, fehlendes
schreibbares Log-Verzeichnis und RESPONSE_BODY-Annahmen außerhalb belegter
Evidence.

## Nicht-Claims

- RESPONSE_BODY / Phase 4 ist nicht promoted.
- Force-all-FAIL-Zeilen sind kein Produktionssupport.
- Dieser Guide belegt nicht jedes Apache-Distro-Paket, jedes MPM oder jedes
  Modul-Layout.

## Verwandte Dokumente

- [examples/apache/README.de.md](examples/apache/README.de.md)
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`

## Apache-Common-Adoption-C-Standard-Smoke

Die Apache-Common-Adoption-Schicht hat einen reinen Compile-Standards-Smoke:

- `make check-apache-c17` ist verpflichtend und kompiliert die Apache-
  Adoption-Dateien sowie die genutzten Common-Quellen mit
  `-std=c17 -Wall -Wextra -Werror`.
- `make check-apache-c23` und `make check-apache-future-c` sind optional; sie
  nutzen `ci/detect-c-standard.py` und werden übersprungen, wenn der Compiler
  den angeforderten C-Modus nicht unterstützt.
- `make check-apache-c-standards` führt C17 sowie die optionalen C23-/future-C-
  Profile aus.

Der Check benötigt APXS (`apxs` oder `apxs2`) und Apache-/APR-/libmodsecurity-
Header. Wenn diese Build-Header fehlen, meldet der Check `BLOCKED` und beendet
sich mit Exit-Code `77`. Das ist nur Compile-/Structure-Evidence für die
Apache/Common-Adoption-Grenze; es ist keine Produktions-, CRS-, Full-Matrix-
oder Runtime-Verifikation.
