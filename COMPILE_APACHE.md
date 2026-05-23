# Apache kompilieren

Diese Anleitung beschreibt, wie der ModSecurity-Connector aus diesem
Repository als Apache/httpd-Modul gebaut und aktiviert wird. Der lokale
Connector liegt unter `connectors/apache/`, verwendet Autotools und wird über
`apxs` gegen eine konkrete Apache-Installation gebaut.

## Überblick

Der Apache-Connector ist ein Dynamic Shared Object für Apache/httpd. Er wird
über `LoadModule` geladen, registriert Apache-Hooks und Filter und übergibt
Request-/Response-Daten an libmodsecurity v3. Im Unterschied zum Nginx-
Connector wird kein Nginx-Quellbaum erweitert; stattdessen nutzt der Build
`apxs`, um Compiler-Flags, Include-Pfade und Modulpfade der Ziel-Apache-
Installation zu erhalten.

`apxs` ist deshalb wichtig:

- Es gehört zur Apache-Development-Umgebung.
- Es kennt das Modulverzeichnis über `apxs -q LIBEXECDIR`.
- Es kennt Compiler und Include-Pfade über `apxs -q CC` und
  `apxs -q INCLUDEDIR`.
- Es installiert Module bei Bedarf passend zur Apache-Installation.

Der lokale Build verwendet:

| Datei oder Verzeichnis | Bedeutung |
| --- | --- |
| `connectors/apache/autogen.sh` | Erzeugt `configure` über `autoreconf --install` |
| `connectors/apache/configure.ac` | Sucht APXS, Apache und libmodsecurity |
| `connectors/apache/Makefile.am` | Ruft den APXS-Wrapper und das Install-Ziel auf |
| `connectors/apache/build/` | Autoconf-Makros und APXS-Wrapper-Vorlage |
| `connectors/apache/src/` | Produktive Apache-Connector-Quellen |

Das erwartete Build-Artefakt ist:

```text
mod_security3.so
```

Im Repository-Helfer wird es nach
`$BUILD_ROOT/apache-build/output/apache/mod_security3.so` kopiert.

## Voraussetzungen

Für Debian/Ubuntu:

```sh
sudo apt-get update
sudo apt-get install -y \
  git make gcc g++ clang \
  autoconf automake libtool pkg-config \
  curl ca-certificates tar perl python3 \
  apache2 apache2-dev \
  libpcre2-dev libxml2-dev libyajl-dev liblmdb-dev libgeoip-dev \
  libcurl4-openssl-dev
```

Falls verfügbar:

```sh
sudo apt-get install -y libmodsecurity-dev
```

Auf Debian/Ubuntu heißt APXS häufig `apxs2`. Auf RHEL/Fedora kommt APXS meist
aus `httpd-devel` und heißt `apxs`. Andere Distributionen verwenden andere
Paketnamen. Entscheidend ist, dass Apache, Apache-Development-Dateien, APXS,
Compiler, Autotools und libmodsecurity-v3-Header vorhanden sind.

Für libmodsecurity benötigt der Connector:

- `modsecurity/modsecurity.h`,
- `modsecurity/intervention.h`,
- `modsecurity/transaction.h`,
- je nach Version `modsecurity/rules_set.h` oder `modsecurity/rules.h`,
- `libmodsecurity.so`.

Der Repository-Helper baut und staged libmodsecurity unter:

```text
$BUILD_ROOT/apache-build/output/modsecurity/include
$BUILD_ROOT/apache-build/output/modsecurity/lib
```

Bei manuellen Builds kann ein vorhandener Prefix angegeben werden:

```sh
./configure --with-libmodsecurity=/usr/local/modsecurity
```

## Repository vorbereiten

Nach einem frischen Clone:

```sh
git clone <repository-url> ModSecurity-conector
cd ModSecurity-conector
git submodule update --init --recursive
```

Das Submodul `modules/ModSecurity-test-Framework` wird für Makefile-Ziele,
Materialisierung und Smoke-Tests benötigt.

Wichtige Pfade:

| Pfad | Bedeutung |
| --- | --- |
| `connectors/apache/` | Apache-Connector-Root |
| `connectors/apache/src/` | Apache-Modulquellen |
| `connectors/apache/build/` | M4-Makros und APXS-Wrapper |
| `common/include/msconnector/` | Gemeinsame Direktiven-, Options- und Rule-Load-Stats-Header |
| `connectors/apache/harness/` | Runtime-Smoke-Harness |
| `modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` | Build-Helper |

Der vorhandene Build-/Smoke-Pfad:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-apache
```

Dieser Pfad baut oder staged libmodsecurity v3, materialisiert den Apache-
Connector nach `$BUILD_ROOT/apache-build/connector-src`, baut bei Bedarf Apache
httpd aus Quellcode, führt `./autogen.sh`, `./configure` und `make` im
materialisierten Connector-Quellbaum aus und startet anschließend echte HTTP-
Smoke-Tests.

## Apache-Entwicklungsumgebung prüfen

Vor einem manuellen Build sollte klar sein, welches Apache und welches APXS
verwendet werden.

Debian/Ubuntu:

```sh
command -v apxs2
command -v apache2
apache2 -v
apache2 -V
```

Andere Distributionen:

```sh
command -v apxs
command -v httpd
httpd -v
httpd -V
```

Nützliche APXS-Abfragen:

```sh
apxs2 -q CC
apxs2 -q INCLUDEDIR
apxs2 -q LIBEXECDIR
apxs2 -q SBINDIR
apxs2 -q PROGNAME
```

Wenn `apxs2` nicht vorhanden ist, verwende `apxs`. `LIBEXECDIR` ist der
übliche Modulpfad. `SBINDIR` und `PROGNAME` helfen, das zugehörige Apache-
Binary zu finden.

Geladene Module prüfen:

```sh
apache2ctl -M 2>/dev/null | head
```

oder:

```sh
httpd -M 2>/dev/null | head
```

Wenn die Systeminstallation schwer zu verwenden ist, kann der isolierte
Repository-Pfad mit `BUILD_HTTPD_FROM_SOURCE=1` einfacher sein.

## Connector kompilieren

### Build über das Repository

```sh
git submodule update --init --recursive

REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-apache
```

Erwartete Artefakte:

```text
$BUILD_ROOT/apache-build/output/apache/mod_security3.so
$BUILD_ROOT/apache-build/output/modsecurity/include/modsecurity/modsecurity.h
$BUILD_ROOT/apache-build/output/modsecurity/lib/libmodsecurity.so
$BUILD_ROOT/apache-runtime/httpd/bin/httpd
$BUILD_ROOT/apache-runtime/httpd/bin/apxs
$BUILD_ROOT/logs/apache/artifacts.txt
$BUILD_ROOT/logs/apache/commands.txt
```

`commands.txt` dokumentiert die ausgeführten Build-Befehle. Das ist hilfreich,
um Fehler auf einer anderen Maschine nachzustellen.

### Manueller Build

```sh
cd /pfad/zu/ModSecurity-conector/connectors/apache

./autogen.sh

./configure \
  --with-libmodsecurity=/usr/local/modsecurity \
  --with-apxs="$(command -v apxs2 || command -v apxs)" \
  --with-apache="$(command -v apache2 || command -v httpd)"

make
```

Wichtige Optionen:

| Option | Bedeutung |
| --- | --- |
| `--with-libmodsecurity=...` | Prefix mit libmodsecurity-Headern und Bibliothek |
| `--with-apxs=...` | APXS der Ziel-Apache-Installation |
| `--with-apache=...` | Apache/httpd-Binary der Zielinstallation |

Das lokale Build-Artefakt liegt typischerweise hier:

```text
connectors/apache/src/.libs/mod_security3.so
```

Installation über APXS:

```sh
sudo make install
```

Das Install-Ziel ruft APXS mit `-i -n mod_security3` auf. In Paket- oder
Container-Builds ist es oft besser, die `.so` in ein Staging-Verzeichnis zu
kopieren und die Apache-Konfiguration separat zu verwalten.

## Apache-Modul aktivieren

### Debian/Ubuntu mit `a2enmod`

Beispiel für eine Load-Datei:

```apache
LoadModule security3_module /usr/lib/apache2/modules/mod_security3.so
```

Aktivieren:

```sh
sudo sh -c 'printf "%s\n" "LoadModule security3_module /usr/lib/apache2/modules/mod_security3.so" > /etc/apache2/mods-available/security3.load'
sudo a2enmod security3
```

Beispielkonfiguration:

```apache
<IfModule security3_module>
    modsecurity on
    modsecurity_rules_file /etc/apache2/modsecurity/main.conf
</IfModule>
```

### Manuelle `LoadModule`-Direktive

```apache
LoadModule security3_module "/opt/httpd/modules/mod_security3.so"

modsecurity on
modsecurity_rules_file "/opt/httpd/conf/modsecurity/main.conf"
```

Minimale Rules-Datei:

```apache
SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On

SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog "/var/log/apache2/modsec_audit.log"

SecRule ARGS:test "@streq block" \
  "id:200000,phase:2,deny,status:403,msg:'Apache connector test rule'"
```

Hinweise:

- `modsecurity on` aktiviert den Connector.
- `modsecurity_rules_file` lädt lokale Regeln über libmodsecurity.
- `modsecurity_rules` lädt Inline-Regeln.
- `modsecurity_rules_remote` lädt Remote-Regeln.
- `modsecurity_transaction_id` akzeptiert im Apache-Connector eine statische
  Zeichenkette. Es werden keine Apache-Ausdrücke ausgewertet.
- Ohne gesetzte Transaktions-ID versucht der Connector `UNIQUE_ID` zu nutzen
  und erzeugt sonst eine Transaktion ohne explizite ID.
- `modsecurity_use_error_log off` betrifft nur den Error-Log-Callback, nicht
  Audit-Logs, Interventions oder Request-/Response-Verarbeitung.

Rules-Dateien müssen lesbar sein. Audit-Log-Dateien oder -Verzeichnisse müssen
für den Apache-Prozess schreibbar sein.

## Funktionstest

Konfiguration prüfen:

```sh
sudo apachectl configtest
```

oder:

```sh
sudo apache2ctl -t
```

Bei eigenständigem httpd:

```sh
/opt/httpd/bin/httpd -t -f /opt/httpd/conf/httpd.conf
```

Apache neu laden:

```sh
sudo systemctl reload apache2
```

oder:

```sh
sudo systemctl reload httpd
```

Geladenes Modul prüfen:

```sh
apache2ctl -M 2>/dev/null | grep -i security
```

oder:

```sh
httpd -M 2>/dev/null | grep -i security
```

Request-Test:

```sh
curl -i "http://127.0.0.1/?test=block"
```

Bei der Beispielregel und `SecRuleEngine On` wird `403` erwartet. Ein Request,
der nicht matcht, sollte normal passieren:

```sh
curl -i "http://127.0.0.1/?test=ok"
```

Repository-Smoke:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-apache
```

Teilmenge:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-apache
```

Prüfe Apache Error Log, Access Log, ModSecurity Audit Log und bei Helper-
Builds die Logs unter `$BUILD_ROOT/logs/apache/` sowie
`$BUILD_ROOT/logs/apache-runtime/`.

## Troubleshooting

### `apxs` nicht gefunden

Installiere das Apache-Development-Paket:

```sh
sudo apt-get install -y apache2-dev
```

oder auf RHEL/Fedora sinngemäß:

```sh
sudo dnf install -y httpd-devel
```

Prüfen:

```sh
command -v apxs2 || command -v apxs
```

Beim Configure kann der Pfad explizit gesetzt werden:

```sh
./configure --with-apxs=/usr/bin/apxs2 --with-apache=/usr/sbin/apache2
```

### Apache-Development-Paket fehlt

Fehlende Header wie `httpd.h`, `http_config.h` oder APR-Header deuten auf ein
fehlendes Development-Paket hin.

```sh
apxs2 -q INCLUDEDIR
ls "$(apxs2 -q INCLUDEDIR)/httpd.h"
```

### Compiler- oder Linkerfehler

Prüfe bei Repository-Builds:

```text
$BUILD_ROOT/logs/apache/commands.txt
```

Bei manuellen Builds:

```sh
make V=1
```

Typische Ursachen sind falsches APXS, fehlende APR/APR-util-Header, fehlende
libmodsecurity-Header, inkompatible Compiler-Flags oder alte Artefakte in einem
wiederverwendeten Build-Verzeichnis.

### Fehlende libmodsecurity-Abhängigkeiten

Prüfen:

```sh
test -f /usr/local/modsecurity/include/modsecurity/modsecurity.h
test -f /usr/local/modsecurity/lib/libmodsecurity.so
ldd /pfad/zu/mod_security3.so
```

Wenn `libmodsecurity.so` nicht gefunden wird:

```sh
sudo sh -c 'echo /usr/local/modsecurity/lib > /etc/ld.so.conf.d/modsecurity.conf'
sudo ldconfig
```

Für lokale Tests kann `LD_LIBRARY_PATH` gesetzt werden.

### Modul kann nicht geladen werden

Prüfe, ob der Pfad in `LoadModule` stimmt, ob die Datei existiert, ob `ldd`
fehlende Libraries zeigt und ob das Modul mit dem passenden APXS gebaut wurde.

### Fehlerhafte Rules-Datei

Wenn `apachectl configtest` eine ModSecurity-Regelmeldung ausgibt, prüfe
Syntax, eindeutige `id`-Werte, Pfade, Leserechte und Kompatibilität der Regeln
mit der verwendeten libmodsecurity-Version.

### Rechteprobleme

Apache läuft je nach Distribution als `www-data`, `apache` oder ein anderer
Benutzer. Prüfe:

```sh
namei -l /etc/apache2/modsecurity/main.conf
namei -l /var/log/apache2/modsec_audit.log
```

Bei SELinux:

```sh
getenforce
ausearch -m avc -ts recent
```

### Unterschiede zwischen Distributionen

Binary-Namen, APXS-Namen, Modulverzeichnisse, Default-MPMs, systemd-Units und
Sicherheitsprofile unterscheiden sich. Verlasse dich auf `apxs -q ...`,
`apachectl -V` und `apachectl -M` statt auf angenommene Pfade.

## Best Practices

- Dokumentiere Apache-Version, APXS-Pfad, libmodsecurity-Version,
  Connector-Commit und Build-Befehl.
- Berücksichtige Apache-, APR-, APR-util- und APXS-Updates.
- Teste Builds in einer sauberen Umgebung.
- Führe vor jedem Reload `apachectl configtest` oder `apache2ctl -t` aus.
- Starte mit kleinen Regeln, bevor ein großes Regelwerk aktiviert wird.
- Trenne `SecRuleEngine DetectionOnly` und `SecRuleEngine On` bewusst.
- Prüfe Error-Logs und Audit-Logs regelmäßig.
- Nutze `make smoke-apache`, um den Projektpfad mit echten HTTP-Requests zu
  validieren.
