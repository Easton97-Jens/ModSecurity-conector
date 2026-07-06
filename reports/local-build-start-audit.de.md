# Lokaler Build- und Start-Audit

**Sprache:** [English](local-build-start-audit.md) | Deutsch

Erstellt: 2026-07-06
Aktualisiert: 2026-07-06

Dieser Audit dokumentiert nur Compile-Nachweise, Link-Nachweise,
Config-Load-Nachweise und minimale Prozess-Start-Nachweise. Es wurden keine
HTTP-Requests gesendet, keine CRS-Cases ausgefuehrt, keine Full-Matrix
ausgefuehrt, keine Response-Bodies geprueft und kein Live-Traffic- oder
Security-Verhalten behauptet.

Nachweis-Root: `/var/tmp/ModSecurity-conector-verified/build/local-build-start`

## Framework-Provisioning

| Abhaengigkeit | Lokale Quelle | Pfad | Ergebnis |
|---|---|---|---|
| Apache/APXS | Framework-`ci/common.sh`-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/apxs` | PASS |
| Apache httpd | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/httpd` | PASS |
| Apache-Modul | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/build/output/apache/mod_security3.so` | PASS |
| NGINX-Headers/Source | Framework-`ci/common.sh`-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/build/nginx-src` | PASS |
| NGINX-Binary/-Modul | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/nginx` | PASS |
| HAProxy-Headers/Source | Framework-`ci/common.sh`-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/sources/haproxy/haproxy-3.2.19` | PASS |
| HAProxy-Binary | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/de600fcd33bfda9614b0753e2e10a318b9719ba03c3acbe0838e25b9fb862658/haproxy-runtime/haproxy/sbin/haproxy` | PASS |
| libmodsecurity-Headers | Framework-`ci/common.sh`-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include` | PASS |
| libmodsecurity-Library | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib` | PASS |

## Build- und Start-Matrix

| Komponente | Build/Link | Config-Load | Start-Smoke | Nachweis | Hinweise |
|---|---|---|---|---|---|
| Common SDK | PASS | n/a | n/a | `logs/common-checks.log` | Nur `check-common-helpers`, SDK-Contract, Adapter-Contract und Directive-Parity |
| Apache | PASS | PASS | PASS | `logs/apache-compile-checks.log`; `apache/configtest.log`; `apache/start-summary.txt` | `mod_security3.so` mit `modsecurity off` geladen; keine Requests gesendet |
| NGINX | PASS | PASS | PASS | `logs/nginx-compile-checks.log`; `nginx/configtest.log`; `nginx/start-summary.txt` | `ngx_http_modsecurity_module.so` mit `modsecurity off` geladen; keine Requests gesendet |
| HAProxy | PASS | PASS | PASS | `logs/haproxy-compile-checks.log`; `logs/haproxy-build-link.log`; `haproxy-start/start-summary.txt` | Nur minimaler HAProxy-Prozessstart; kein Traffic gesendet |
| HAProxy-SPOA-Runtime-Binary | PASS | n/a | PASS | `logs/haproxy-build-link.log`; `haproxy-spoa-start/start-summary.txt`; `haproxy-spoa-start/spoa.log` | Binary startete im `--serve`-Listenmodus, schrieb Ready-/PID-Dateien und wurde gestoppt; kein SPOP-Client verbunden |
| Envoy-Starter | PASS | NOT PRESENT | NOT PRESENT | `logs/envoy-build-starter.log` | Starter-Binary erstellt; kein Nicht-Test-Server-/Config-Startmodus vorhanden; Status bleibt `not_verified` / `connector-gap` |
| Traefik-Starter | PASS | NOT PRESENT | NOT PRESENT | `logs/traefik-build-starter.log` | Starter- und Decision-Service-Binaries erstellt; kein Nicht-Test-Server-/Config-Startmodus vorhanden; Status bleibt `not_verified` / `connector-gap` |
| lighttpd-Starter | PASS | NOT PRESENT | NOT PRESENT | `logs/lighttpd-build-starter.log`; `logs/lighttpd-bridge-compile-only.log` | Build-Starter erstellt; Bridge-Starter wurde compile-only neu gebaut, weil das Make-Target einen eingebetteten Self-Test aufruft |
| Remaining-Connector-Helper | PASS | n/a | n/a | `logs/remaining-connectors-compile-checks.log` | Nur C17/C23/future-C und Common-Adoption-Checks |

## Start-Nachweise

| Komponente | Config-Ergebnis | Prozess-Nachweis | Stop-Ergebnis |
|---|---|---|---|
| Apache | `Syntax OK` in `apache/configtest.log` | `background_pid=529328`, `pid_file=529328` in `apache/start-summary.txt` | `stopped=yes` |
| NGINX | `syntax is ok` und `test is successful` in `nginx/configtest.log` | `background_pid=530458`, `pid_file=530458` in `nginx/start-summary.txt` | `stopped=yes` |
| HAProxy | `haproxy -c -f` gab 0 zurueck; Logdatei ist leer | `pid_file=531716` in `haproxy-start/start-summary.txt` | `stopped=yes` |
| HAProxy-SPOA-Runtime-Binary | n/a | `background_pid=531815`, `pid_file=531815`, Ready-Datei erstellt | `stopped=yes` |

## Target-Verfuegbarkeit

| Angefragte Target-Familie | Lokaler Status | Aktion |
|---|---|---|
| `common-build`, `build-common` | Nicht vorhanden | Als nicht vorhanden dokumentiert |
| `apache-build`, `build-apache`, `apache-structure` | Nicht vorhanden | Apache-Common-/C-Standard-Compile-Checks plus gecachten Modul-Load-/Start-Nachweis genutzt |
| `nginx-build`, `build-nginx`, `nginx-structure` | Nicht vorhanden | NGINX-Common-/C-Standard-Compile-Checks plus gecachten Modul-Load-/Start-Nachweis genutzt |
| `haproxy-build`, `build-haproxy`, `haproxy-structure` | Nicht vorhanden | HAProxy-Common-/C-Standard-Compile-Checks plus connector-lokale Build-/Link-Targets genutzt |
| `envoy-build`, `build-envoy`, `envoy-structure` | Nicht vorhanden | `make -C connectors/envoy build-starter` genutzt |
| `traefik-build`, `build-traefik`, `traefik-structure` | Nicht vorhanden | `make -C connectors/traefik build-starter build-decision-service build-forwardauth-starter` genutzt |
| `lighttpd-build`, `build-lighttpd`, `lighttpd-structure` | Nicht vorhanden | `make -C connectors/lighttpd build-starter` und manueller compile-only Bridge-Build genutzt |
| `smoke-*`, Runtime-, CRS-, Matrix- und Harness-Targets | Vorhanden, aber ausserhalb des Umfangs | Nicht als akzeptierter Audit-Nachweis genutzt |

## Disqualifizierte Evidence

`make -C connectors/lighttpd build-bridge-starter` ruft innerhalb von
`connectors/lighttpd/build/bridge_starter.sh` `--self-test` auf. Dieses Ergebnis
wird fuer diesen Audit nicht als akzeptierter Nachweis gezaehlt. Der
Bridge-Starter wurde danach mit einem compile-only-Befehl erneut gebaut; der
Nachweis liegt in `logs/lighttpd-bridge-compile-only.log`.

## Bewusst Nicht Ausgefuehrt

| Kategorie | Status | Grund |
|---|---|---|
| HTTP-Requests | Nicht ausgefuehrt | Start-Smokes prueften nur Config, PID-/Ready-Dateien und Stop-Verhalten |
| CRS-Runtime-Cases | Nicht ausgefuehrt | Ausserhalb des Compile-/Link-/Start-Audit-Umfangs |
| Full-Matrix-Runtime-Jobs | Nicht ausgefuehrt | Ausserhalb des Compile-/Link-/Start-Audit-Umfangs |
| Response-Body-Checks | Nicht ausgefuehrt | Wuerden Runtime-Traffic benoetigen |
| Live-Connector-Transaktionschecks | Nicht ausgefuehrt | Wuerden Request-/Response-Traffic benoetigen |
| Runtime-/Security-Claims | Nicht gemacht | Dieser Report dokumentiert nur Build-, Link-, Config-Load- und Prozess-Start-Faehigkeit |
