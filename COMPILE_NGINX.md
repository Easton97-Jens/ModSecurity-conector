# Nginx kompilieren

Diese Anleitung beschreibt den Build des ModSecurity-Connectors für Nginx im
Kontext dieses Repositories. Sie deckt den belegten lokalen Build-/Smoke-Pfad
über die vorhandenen Skripte ab und ergänzt ihn um manuelle Build-Schritte für
Umgebungen, in denen Nginx und libmodsecurity bereits separat bereitgestellt
werden.

## Überblick

Der Nginx-Connector liegt unter `connectors/nginx/`. Er ist ein
Nginx-HTTP-Modul, das Nginx-Requests und -Responses an libmodsecurity v3
weitergibt. Die WAF-Entscheidung selbst liegt in libmodsecurity und den
geladenen Regeln; der Connector übernimmt die Einbindung in Nginx, die
Konfigurationsdirektiven, die Anlage von Transaktionen und die Übergabe der
HTTP-Daten an die ModSecurity-Phasen.

Beim Build passiert grundsätzlich:

1. libmodsecurity-v3-Header und `libmodsecurity.so` werden bereitgestellt.
2. Der Nginx-Quellcode wird mit dem Third-Party-Modul aus `connectors/nginx/`
   konfiguriert.
3. Nginx kompiliert die Connector-Quellen aus `connectors/nginx/src/`.
4. Das Ergebnis ist entweder ein dynamisches Modul
   `ngx_http_modsecurity_module.so` oder ein Nginx-Binary mit statisch
   einkompiliertem Modul.

Der Unterschied zwischen dynamischem und statischem Modul:

- Dynamisch: `./configure --add-dynamic-module=...` erzeugt eine `.so`-Datei.
  Diese wird später mit `load_module` geladen. Dieser Pfad ist im Repository
  durch den Smoke-Build belegt.
- Statisch: `./configure --add-module=...` baut den Connector direkt in den
  Nginx-Binary. Dafür gibt es keine separate `load_module`-Zeile. Die
  Projektdokumentation behandelt diesen Pfad als grundsätzlich möglichen, aber
  separat zu validierenden Build-Pfad.

In `connectors/nginx/docs/build.md` ist festgehalten, dass die lokale
Proof-of-Concept-Automation den dynamischen Modul-Build nutzt und unterstützte
Nginx-Versionen noch explizit verifiziert werden müssen.

## Voraussetzungen

Für Debian/Ubuntu sind diese Pakete ein sinnvoller Startpunkt:

```sh
sudo apt-get update
sudo apt-get install -y \
  git make gcc g++ clang \
  autoconf automake libtool pkg-config \
  curl ca-certificates tar perl python3 \
  libpcre3-dev zlib1g-dev libssl-dev \
  libxml2-dev libyajl-dev liblmdb-dev libgeoip-dev \
  libcurl4-openssl-dev
```

Wenn die Distribution ein passendes Paket anbietet, kann eine installierte
libmodsecurity-Entwicklungsumgebung verwendet werden:

```sh
sudo apt-get install -y libmodsecurity-dev
```

Paketnamen unterscheiden sich je nach Distribution. Auf RHEL/Fedora heißen
vergleichbare Pakete häufig `pcre-devel`, `zlib-devel`, `openssl-devel`,
`pkgconf-pkg-config` oder `mod_security`. Entscheidend ist, dass Compiler,
Make, Nginx-Build-Abhängigkeiten, ModSecurity-Header und `libmodsecurity.so`
vorhanden sind.

Für libmodsecurity benötigt der Connector insbesondere:

- `modsecurity/modsecurity.h`,
- `modsecurity/transaction.h`,
- je nach Version `modsecurity/rules_set.h` oder `modsecurity/rules.h`,
- `libmodsecurity.so`.

Wenn libmodsecurity nicht an Standardpfaden liegt, werden beim Nginx-Build
diese Variablen verwendet:

```sh
export MODSECURITY_INC=/opt/modsecurity/include
export MODSECURITY_LIB=/opt/modsecurity/lib
```

Der Nginx-Quellcode muss zur Ziel-Nginx-Version passen. Für dynamische Module
ist ABI-Kompatibilität zentral. Prüfe bei einem vorhandenen Ziel-Nginx:

```sh
nginx -V 2>&1
```

Diese Ausgabe zeigt Version, Compiler und Configure-Argumente. Nach Nginx-
Updates sollte das Modul neu gebaut und getestet werden.

## Repository vorbereiten

Nach einem frischen Clone:

```sh
git clone <repository-url> ModSecurity-conector
cd ModSecurity-conector
git submodule update --init --recursive
```

Das Submodul `modules/ModSecurity-test-Framework` ist notwendig für die
Makefile-Ziele und die Smoke-Helfer. Ohne Submodul blockieren Ziele wie
`make smoke-nginx`.

Wichtige Pfade:

| Pfad | Bedeutung |
| --- | --- |
| `connectors/nginx/config` | Nginx-Third-Party-Module-Konfiguration und libmodsecurity-Erkennung |
| `connectors/nginx/src/` | Produktive Nginx-Connector-Quellen |
| `common/include/msconnector/` | Gemeinsame Direktiven-, Options- und Metadaten-Header |
| `connectors/nginx/harness/` | Runtime-Smoke-Konfiguration und Runner |
| `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh` | Build-Helper für den lokalen dynamischen Nginx-Modul-Build |

Der vorhandene Build-Pfad:

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

Dieser Befehl baut nicht nur das Modul. Er baut oder staged libmodsecurity v3,
materialisiert die Nginx-Connector-Quelle nach
`$BUILD_ROOT/nginx-build/connector-src`, lädt Nginx-Quellen, konfiguriert Nginx
mit `--with-compat --add-dynamic-module=...`, installiert einen lokalen Nginx
unter `$BUILD_ROOT/nginx-runtime/nginx` und führt anschließend echte HTTP-
Smoke-Tests aus.

## Nginx-Quellcode vorbereiten

Für manuelle Builds muss ein Nginx-Quellbaum vorliegen:

```sh
mkdir -p "$HOME/src"
cd "$HOME/src"
curl -LO https://nginx.org/download/nginx-1.26.3.tar.gz
tar -xzf nginx-1.26.3.tar.gz
cd nginx-1.26.3
```

Wenn das Modul für einen Distributions-Nginx gebaut wird, sollten Version und
Configure-Optionen aus `nginx -V` übernommen werden. Mindestens sollte
`--with-compat` gesetzt werden, wenn ein dynamisches Modul für einen kompatiblen
Ziel-Nginx entstehen soll.

Der Repository-Helper verwendet standardmäßig einen GitHub-Release-Download.
Die relevanten Variablen kommen aus `modules/ModSecurity-test-Framework/ci/common.sh`:

```sh
NGINX_SOURCE_MODE=github-release
NGINX_SOURCE_REPO_URL=https://github.com/nginx/nginx
NGINX_RELEASE_TAG=latest
```

Für reproduzierbare Builds sollte `latest` durch einen konkreten Tag ersetzt
werden:

```sh
NGINX_RELEASE_TAG=release-1.31.0 \
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

## Connector als dynamisches Modul kompilieren

Der dynamische Build ist der im Projekt belegte Hauptpfad.

### Build über das Repository

```sh
git submodule update --init --recursive

REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

Erwartete Artefakte:

```text
$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx
$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
$BUILD_ROOT/nginx-build/output/modsecurity/include/modsecurity/modsecurity.h
$BUILD_ROOT/nginx-build/output/modsecurity/lib/libmodsecurity.so
$BUILD_ROOT/logs/nginx/artifacts.txt
$BUILD_ROOT/logs/nginx/commands.txt
```

`commands.txt` dokumentiert die ausgeführten Befehle. `artifacts.txt`
dokumentiert die erzeugten Artefakte, die aufgelöste Nginx-Version und die
verwendeten Pfade.

### Manueller dynamischer Build

```sh
export CONNECTOR_ROOT=/pfad/zu/ModSecurity-conector
export MODSECURITY_INC=/usr/local/modsecurity/include
export MODSECURITY_LIB=/usr/local/modsecurity/lib
export MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include"

cd /pfad/zu/nginx-source

./configure \
  --prefix=/opt/nginx-modsec \
  --modules-path=/opt/nginx-modsec/modules \
  --with-compat \
  --add-dynamic-module="$CONNECTOR_ROOT/connectors/nginx"

make modules
```

Wichtige Optionen und Variablen:

| Option oder Variable | Bedeutung |
| --- | --- |
| `--add-dynamic-module=...` | Baut den Connector als dynamisches Nginx-Modul |
| `--with-compat` | Erhöht die Chance, dass das Modul mit einem kompatiblen Ziel-Nginx geladen werden kann |
| `MODSECURITY_INC` | Include-Pfad zu den ModSecurity-Headern |
| `MODSECURITY_LIB` | Library-Pfad zu `libmodsecurity.so` |
| `MSCONNECTOR_COMMON_INC` | Include-Pfad zu `common/include`; in der Monorepo-Struktur wird er auch automatisch erkannt |
| `YAJL_LIB` | Optionaler Library-Pfad, falls `libyajl` nicht an Standardpfaden liegt |
| `NGX_IGNORE_RPATH=YES` | Optional, wenn keine RPATH-Information in das Ergebnis geschrieben werden soll |

Nach `make modules` liegt das Modul normalerweise hier:

```text
objs/ngx_http_modsecurity_module.so
```

Ein typischer Zielpfad:

```sh
sudo mkdir -p /etc/nginx/modules
sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/
```

## Connector statisch in Nginx einkompilieren

Für einen statischen Build wird `--add-module` verwendet:

```sh
export CONNECTOR_ROOT=/pfad/zu/ModSecurity-conector
export MODSECURITY_INC=/usr/local/modsecurity/include
export MODSECURITY_LIB=/usr/local/modsecurity/lib
export MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include"

cd /pfad/zu/nginx-source

./configure \
  --prefix=/opt/nginx-modsec-static \
  --with-http_ssl_module \
  --add-module="$CONNECTOR_ROOT/connectors/nginx"

make
sudo make install
```

Statisches Kompilieren kann sinnvoll sein, wenn dynamische Module in einer
Umgebung nicht erlaubt sind oder ein Image einen einzigen Nginx-Binary
ausliefern soll. Der Nachteil ist, dass Nginx und Modul immer gemeinsam neu
gebaut werden müssen. Da der lokale Projektpfad statische Builds nicht als
validierten Standard ausweist, sollte dieser Weg mit `nginx -t`, echten
Requests und Logprüfung separat abgesichert werden.

## Nginx-Konfiguration

Bei einem dynamischen Modul steht `load_module` im Hauptkontext:

```nginx
load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;

events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name example.local;

        modsecurity on;
        modsecurity_rules_file /etc/nginx/modsecurity/main.conf;

        location / {
            proxy_pass http://127.0.0.1:8080;
        }
    }
}
```

Eine minimale Rules-Datei:

```apache
SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On

SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog /var/log/nginx/modsec_audit.log

SecRule ARGS:test "@streq block" \
  "id:100000,phase:2,deny,status:403,msg:'Nginx connector test rule'"
```

Hinweise:

- `modsecurity on;` aktiviert den Connector im jeweiligen Scope.
- `modsecurity_rules_file` muss für den Nginx-Worker lesbar sein.
- Audit-Log-Pfade müssen für den Worker schreibbar sein.
- `modsecurity_use_error_log off;` betrifft nur den Error-Log-Callback, nicht
  Audit-Logs oder Interventions.
- `modsecurity_transaction_id` kann im Nginx-Connector eine Nginx Complex
  Value verwenden.

Der lokale Harness nutzt `connectors/nginx/harness/nginx_smoke.conf` als
Vorlage. Dort werden `load_module`, `modsecurity on;` und
`modsecurity_rules_file` in einem generierten Runtime-Verzeichnis gesetzt.

## Funktionstest

Konfiguration prüfen:

```sh
nginx -t
```

Bei einem Helper-Build:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build"
"$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx" \
  -t \
  -p "$BUILD_ROOT/nginx-runtime/nginx" \
  -c "$BUILD_ROOT/nginx-runtime/nginx/conf/nginx.conf"
```

Version und Build-Optionen prüfen:

```sh
nginx -V 2>&1
```

Runtime-Abhängigkeiten prüfen:

```sh
ldd /etc/nginx/modules/ngx_http_modsecurity_module.so
```

Ein einfacher Request-Test:

```sh
curl -i "http://127.0.0.1/?test=block"
```

Bei der Beispielregel wird `403` erwartet. Ein nicht passender Request sollte
normal passieren:

```sh
curl -i "http://127.0.0.1/?test=ok"
```

Repository-Smoke:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

Teilmenge:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-nginx
```

Prüfe danach Nginx-Error-Log, Access-Log, ModSecurity-Audit-Log und bei
Helper-Builds die Logs unter `$BUILD_ROOT/logs/nginx/`.

## Troubleshooting

### Fehlende Header oder Libraries

Wenn `connectors/nginx/config` meldet, dass die ModSecurity-Bibliothek fehlt,
prüfe:

```sh
test -f "$MODSECURITY_INC/modsecurity/modsecurity.h"
test -f "$MODSECURITY_LIB/libmodsecurity.so"
```

Setze die Pfade korrekt:

```sh
export MODSECURITY_INC=/richtiger/include/pfad
export MODSECURITY_LIB=/richtiger/lib/pfad
```

### `libmodsecurity.so` wird zur Laufzeit nicht gefunden

Prüfen:

```sh
ldd /etc/nginx/modules/ngx_http_modsecurity_module.so
```

Beheben:

```sh
sudo sh -c 'echo /usr/local/modsecurity/lib > /etc/ld.so.conf.d/modsecurity.conf'
sudo ldconfig
```

Für lokale Tests kann auch `LD_LIBRARY_PATH` gesetzt werden.

### Inkompatible Nginx-Version

Fehler wie `module is not binary compatible` bedeuten, dass Modul und Nginx-
Binary nicht zusammenpassen. Baue mit derselben Nginx-Version und möglichst
denselben Configure-Optionen wie der Ziel-Nginx. Verwende für dynamische Module
`--with-compat`.

### Falscher Modulpfad

`load_module` muss auf die tatsächliche `.so`-Datei zeigen. Absolute Pfade sind
robuster als relative Pfade:

```sh
ls -l /etc/nginx/modules/ngx_http_modsecurity_module.so
nginx -t
```

### `unknown directive "modsecurity"`

Das Modul wurde nicht geladen oder der statische Nginx enthält den Connector
nicht. Bei dynamischen Modulen muss `load_module` vor dem `http`-Block stehen.
Bei statischen Modulen darf keine `load_module`-Zeile verwendet werden.

### Fehlerhafte ModSecurity-Konfiguration

Wenn `nginx -t` wegen einer Regel scheitert, prüfe Syntax, eindeutige `id`-
Werte, Dateipfade, Leserechte und die Kompatibilität mit der verwendeten
libmodsecurity-Version.

### Permission-Probleme

Rules-Dateien müssen lesbar und Audit-Logs schreibbar sein. Prüfe:

```sh
namei -l /etc/nginx/modsecurity/main.conf
namei -l /var/log/nginx/modsec_audit.log
```

Bei SELinux oder AppArmor können zusätzlich Profile oder Labels relevant sein.

### Unterschiede zwischen Distributionen

Distributionen unterscheiden sich bei Prefix, Modulpfad, Compiler-Flags,
Nginx-Patches und Sicherheitsprofilen. `nginx -V` und `nginx -T` sind die
wichtigsten Diagnosebefehle.

## Best Practices

- Dokumentiere Nginx-Version, Configure-Argumente, libmodsecurity-Version,
  Connector-Commit und Build-Befehl.
- Pinne `NGINX_RELEASE_TAG` und `MODSECURITY_GIT_REF` für reproduzierbare
  Builds.
- Baue das Modul nach Nginx-Updates neu.
- Prüfe jede Konfigurationsänderung mit `nginx -t`.
- Teste zuerst in einer isolierten Umgebung mit kleinen Regeln.
- Prüfe Error-Logs und Audit-Logs nach dem ersten Start.
- Verwende absolute Pfade für Module, Rules-Dateien und Audit-Logs.
- Trenne `SecRuleEngine DetectionOnly` und `SecRuleEngine On` bewusst.
- Nutze `make smoke-nginx`, um den Projektpfad mit echten HTTP-Requests zu
  validieren.
