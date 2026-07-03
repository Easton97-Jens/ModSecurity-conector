# Compile NGINX


**Sprache:** [English](COMPILE_NGINX.md) | Deutsch

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

Dieser Guide beschreibt den Einsatz des NGINX-Connectors außerhalb dieses
Repositorys: libmodsecurity bereitstellen, `ngx_http_modsecurity_module.so`
gegen eine kompatible NGINX-Version/ABI bauen, das Modul in ein externes
NGINX-Setup kopieren, Konfiguration verdrahten und den ersten Syntax-Check oder
Reload ausführen.

## Status und Grenzen

Der NGINX-Connector-Quellcode liegt unter `connectors/nginx/`.
Repository-Smoke-Evidence validiert nur bestimmte Repository-Pfade. Externer
Einsatz hängt von NGINX-ABI-Kompatibilität ab und belegt nicht jedes Paket,
jeden Modulsatz oder jedes RESPONSE_BODY- / Phase-4-Deployment.

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
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

Optionale breitere Repository-Evidence:

```sh
FORCE_ALL_CASES=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

## Pfad 2: Externer Einsatz mit Distribution-Paketen

1. Installieren Sie NGINX, ein kompatibles NGINX-Development-/Source-Paket,
   Build-Werkzeuge und libmodsecurity-Development-Dateien. Paketnamen
   unterscheiden sich je Distribution; dieser Debian-/Ubuntu-artige Befehl ist
   nur ein Beispiel:

   ```sh
   sudo apt-get update
   sudo apt-get install -y nginx nginx-dev build-essential libmodsecurity-dev
   ```

2. Pakete können NGINX, NGINX-Development-Dateien und libmodsecurity
   bereitstellen. Der Paketpfad bedeutet **nicht**, dass das Connector-Modul
   fertig mitgeliefert wird. `ngx_http_modsecurity_module.so` muss weiterhin
   aus `connectors/nginx` gegen eine kompatible NGINX-Version/ABI gebaut
   werden.
3. Inspizieren Sie das installierte NGINX-Binary:

   ```sh
   nginx -V 2>&1
   ```

4. Holen Sie den Connector-Quellcode dieses Repositorys:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

5. Bauen Sie das dynamische Modul mit passender NGINX-Source und kompatiblen
   Configure-Argumenten:

   ```sh
   NGINX_VERSION=<version-from-nginx-V>
   curl -LO "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz"
   tar xf "nginx-${NGINX_VERSION}.tar.gz"
   cd "nginx-${NGINX_VERSION}"
   ./configure --with-compat \
     --add-dynamic-module=/path/to/ModSecurity-conector/connectors/nginx \
     <other-compatible-nginx-configure-args>
   make modules
   ```

6. Kopieren Sie das gebaute Modul und angepasste Konfigurationen in das
   Zielsystem. Verwenden Sie Ihr Modulverzeichnis, Service-
   Konfigurationsverzeichnis, ModSecurity-Regelverzeichnis und Log-Verzeichnis:

   > Hinweis: `install` ist hier kein Paketmanager-Befehl. Er kopiert Dateien
   > und kann Berechtigungen setzen. Zum Beispiel ist
   > `sudo install -m 0755 file.so /target/file.so` ähnlich zu
   > `sudo cp file.so /target/file.so` gefolgt von
   > `sudo chmod 0755 /target/file.so`.

   ```sh
   sudo install -d -m 0755 <nginx-module-dir> <modsecurity-config-dir> <modsecurity-log-dir>
   sudo install -m 0755 objs/ngx_http_modsecurity_module.so <nginx-module-dir>/ngx_http_modsecurity_module.so
   sudo install -m 0644 /path/to/ModSecurity-conector/examples/nginx/modsecurity-request-only.conf <modsecurity-config-dir>/modsecurity-request-only.conf
   sudo install -m 0644 /path/to/ModSecurity-conector/examples/nginx/nginx-modsecurity-request-only.conf <nginx-service-config-dir>/modsecurity.conf
   sudo nginx -t
   sudo systemctl reload <nginx-service-name>
   ```

Das Modul muss neu gebaut werden, wann immer sich das NGINX-Binary/-Paket
ändert. Wenn die Modul-ABI nicht zu NGINX passt, lädt NGINX das Modul nicht.

## Pfad 3: Externer Einsatz aus Source

1. Installieren Sie Compiler-/Build-Voraussetzungen.
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

3. Bauen oder beschaffen Sie die exakte NGINX-Source, die zum installierten
   NGINX-Binary passt. Inspizieren Sie immer zuerst `nginx -V`.
4. Konfigurieren Sie die NGINX-Source mit
   `--add-dynamic-module=/path/to/ModSecurity-conector/connectors/nginx`,
   kompatiblen Argumenten und bei Bedarf `--with-compat`; führen Sie danach
   `make modules` aus.
5. Installieren/kopieren Sie `objs/ngx_http_modsecurity_module.so`, platzieren
   Sie `load_module` im Top-Level-NGINX-Konfigurationskontext, führen Sie
   `nginx -t` aus und reloaden oder restarten Sie NGINX.

## Config Snippets

```nginx
load_module modules/ngx_http_modsecurity_module.so;

modsecurity on;
modsecurity_rules_file <modsecurity-rules-file>;

proxy_pass <backend-upstream>;
```

`load_module` gehört in den Top-Level-NGINX-Konfigurationskontext, nicht in
`http`, `server` oder `location`. Siehe
[examples/nginx/README.de.md](examples/nginx/README.de.md) für die Erklärung
dieser Direktiven, Platzhalter, Logs und Grenzen.

## Beispiel-Konfigurationen

Verwenden Sie die Dateien in [examples/nginx/](examples/nginx/README.de.md) als
Startpunkte für externe Konfiguration. Sie werden vom Repository nicht
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

Prüfen Sie NGINX-Modul-ABI-Mismatch, fehlende Header, fehlende Shared
Libraries, falsche Top-Level-`load_module`-Platzierung, falschen Regelpfad,
fehlendes schreibbares Log-Verzeichnis und RESPONSE_BODY-Annahmen außerhalb
belegter Evidence.

## Nicht-Claims

- RESPONSE_BODY / Phase 4 ist nicht promoted.
- Force-all-FAIL-Zeilen sind kein Produktionssupport.
- Dieser Guide belegt nicht jedes NGINX-Distro-Paket, jede Version oder jede
  Modul-ABI.

## Verwandte Dokumente

- [examples/nginx/README.de.md](examples/nginx/README.de.md)
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`

## Common-SDK-Adoption-Compile-Checks

Der NGINX-Connector besitzt jetzt reine Compile-/Strukturprüfungen für die
Common-SDK-Adoptionsschicht. `make check-nginx-c17` kompiliert relevante NGINX-
und Common-Objekte mit C17 (`-Wall -Wextra -Werror`), sofern lokale NGINX- und
libmodsecurity-Header vorhanden sind. `make check-nginx-c23` und
`make check-nginx-future-c` sind optionale Compiler-Fähigkeitsprüfungen. Fehlende
Header werden als `BLOCKED` mit Exit 77 gemeldet. Das ist keine Production-,
CRS-, Full-Matrix- oder Runtime-Verifikation.
