Sprache: [English](COMPILE_NGINX.md) | Deutsch

# Compile NGINX

## Inhaltsverzeichnis

- [Zweck](#zweck)
- [Status und Grenzen](#status-und-grenzen)
- [Überblick: Drei Pfade](#überblick-drei-pfade)
- [Pfad 1: Repository-Smoke / Validierung](#pfad-1-repository-smoke--validierung)
- [Pfad 2: Externer Einsatz mit Paketen](#pfad-2-externer-einsatz-mit-paketen)
- [Pfad 3: Externer Einsatz aus Source](#pfad-3-externer-einsatz-aus-source)
- [Config Snippets](#config-snippets)
- [Beispiel-Konfigurationen](#beispiel-konfigurationen)
- [Logs](#logs)
- [Troubleshooting](#troubleshooting)
- [Nicht-Claims / Grenzen](#nicht-claims--grenzen)
- [Verwandte Dokumente](#verwandte-dokumente)


## Zweck

Dieser Guide beschreibt den Einsatz des NGINX-Connectors oder Runtime-Pfads außerhalb dieses Repositorys. Er erklärt die drei Pfade von Voraussetzungen bis zum ersten Syntax-Check oder Start und verweist auf passende Beispiel-Konfigurationen.

## Status und Grenzen

Unterstützt ist nur das, was durch Repository-Quellen, Make-Targets, Harnesses oder Beispiele belegt ist. Repository-Smokes sind Evidence für dieses Repository und keine automatische externe Installation. RESPONSE_BODY / Phase 4 ist nicht promoted. Force-all-FAIL-Zeilen sind kein Produktionssupport.

## Überblick: Drei Pfade

| Pfad | Zweck | Haupteinsatz |
| --- | --- | --- |
| Pfad 1: Repository-Smoke | Repository-Evidence validieren | Entwickler / Reviewer |
| Pfad 2: Externer Einsatz mit Paketen | Distro-Pakete nutzen, wo kompatibel | Betreiber mit Systempaketen |
| Pfad 3: Externer Einsatz aus Source | ModSecurity und/oder Connector-Teile manuell bauen | Betreiber mit genauer Versionskontrolle |

## Pfad 1: Repository-Smoke / Validierung

Diese Befehle validieren Repository-Evidence. Sie sind nicht die externe Installationsprozedur.

```sh
git submodule update --init --recursive
make setup-dev
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

## Pfad 2: Externer Einsatz mit Paketen

1. Installieren Sie Betriebssystempakete für Runtime, Build-Werkzeuge und libmodsecurity, sofern kompatibel. Paketnamen unterscheiden sich je Distribution.
2. Aus Paketen kommen typischerweise Runtime und Header/Bibliotheken. Das Artefakt `ngx_http_modsecurity_module.so` oder der Decision-Service muss weiterhin passend zu diesem Repository-Pfad gebaut, vorbereitet oder vom Betreiber bereitgestellt werden.
3. Holen Sie die Connector-Quellen:

```sh
git clone <modsecurity-conector-repo-url> ModSecurity-conector
cd ModSecurity-conector
```

4. Bauen oder bereiten Sie den Pfad mit kompatiblen Paket-Headern/Bibliotheken vor. Benötigte Komponenten: NGINX mit kompatibler ABI und `nginx -V`-Prüfung.
5. Kopieren/adaptieren Sie Konfigurationen in die Modul-, Service-Konfigurations-, ModSecurity-Regel-, Log- und Runtime-Verzeichnisse Ihrer Umgebung. Diese Kategorien sind Platzhalter, keine universellen Pfade.
6. Führen Sie den ersten Syntax-Check oder Start mit dem Zielservice aus und prüfen Sie Logs.

## Pfad 3: Externer Einsatz aus Source

1. Installieren Sie Compiler und Build-Voraussetzungen.
2. Identifizieren Sie den gewünschten libmodsecurity-Ref oder den Repository-/Framework-Pin.

Wenn Pakete nicht geeignet sind, kann libmodsecurity v3 aus Source gebaut werden. Das folgende Beispiel ist ein Upstream-Style-Beispiel und kein repository-eigener Build-Guarantee:

```sh
git clone --depth 1 -b <modsecurity-v3-ref> https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity-v3
cd ModSecurity-v3
git submodule update --init --recursive
./build.sh
./configure --prefix=<libmodsecurity-prefix>
make -j"$(nproc)"
sudo make install
```

`<modsecurity-v3-ref>` und `<libmodsecurity-prefix>` müssen vom Betreiber gewählt oder gegen den Repository-/Framework-Pin geprüft werden.

3. Holen Sie dieses Repository und bauen/vorbereiten Sie `ngx_http_modsecurity_module.so` oder die vom Betreiber bereitzustellenden Backend-Teile.
4. Führen Sie den ersten Syntax-Check oder Start aus. Beispiele und Platzhalter stehen in [examples/nginx/README.de.md](examples/nginx/README.de.md).

## Config Snippets

```text
load_module modules/ngx_http_modsecurity_module.so;
modsecurity on;
modsecurity_rules_file <modsecurity-rules-file>;
```

Siehe [examples/nginx/README.de.md](examples/nginx/README.de.md) für die Erklärung dieser Direktiven, Platzhalter, Logs und Grenzen.

## Beispiel-Konfigurationen

Nutzen Sie die Dateien in [examples/nginx/README.de.md](examples/nginx/README.de.md) als Startpunkte für externe Konfiguration. Sie werden nicht automatisch vom Repository installiert und sind keine universellen Produktionsdefaults.

## Logs

Prüfen Sie je nach Pfad Webserver-/Proxy-Access-Logs, Error-Logs, ModSecurity-Audit-Logs, Connector-Decision-Logs und Sidecar-/Agent-Logs. Beispielpfade sind Platzhalter.

## Troubleshooting

Prüfen Sie ABI-Mismatch, fehlende Header, fehlende Shared Libraries, falschen Konfigurationskontext, falschen Regelpfad, fehlende schreibbare Log-Verzeichnisse, fehlenden Sidecar/Auth-Service, falsche Backend-Adresse und RESPONSE_BODY-Annahmen über die Evidence hinaus.

## Nicht-Claims / Grenzen

- RESPONSE_BODY / Phase 4 ist nicht promoted.
- Force-all-FAIL-Zeilen sind kein Produktionssupport.
- Das Modul muss zur NGINX-ABI passen und nach NGINX-Paketwechseln neu gebaut werden.

## Verwandte Dokumente

- [English](COMPILE_NGINX.md)
- [examples/nginx/README.de.md](examples/nginx/README.de.md)
