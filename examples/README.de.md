# Connector-Beispiele

**Sprache:** [English](README.md) | Deutsch

Die Beispiele sind der praktische Konfigurationsbegleiter zur
Hauptdokumentation. Sie decken alle sechs Hostfamilien und alle zehn logischen
Connector-Lösungen ab. Beginnen Sie hier, wenn der gewünschte Host bereits
feststeht, aber noch unklar ist, wie die Konfigurationsebenen des Repositorys
zusammenspielen.

Beispiele sind **Lehr- und Referenzmaterial**. Sie sind keine
Produktions-Deployment-Manifeste und beweisen für sich allein kein
Runtime-Verhalten.

## Host wählen

| Hostfamilie | Beispiel-Guide | Logische Lösungen |
| --- | --- | --- |
| Apache | [Apache](apache/README.de.md) | `apache` |
| NGINX | [NGINX](nginx/README.de.md) | `nginx` |
| HAProxy | [HAProxy](haproxy/README.de.md) | `haproxy-htx`, `haproxy-spoe-spop` |
| Envoy | [Envoy](envoy/README.de.md) | `envoy-ext-proc`, `envoy-ext-authz` |
| Traefik | [Traefik](traefik/README.de.md) | `traefik-native-uds`, `traefik-forwardauth` |
| lighttpd | [lighttpd](lighttpd/README.de.md) | `lighttpd-patched`, `lighttpd-stock` |

## Konfigurationsprofil wählen

| Profil | Geeignet für | Wichtige Grenze |
| --- | --- | --- |
| `off` | Baseline ohne zusätzliches connector-eigenes kumulatives Phase-4-Budget | Konfigurierte libmodsecurity-Response-Body-Inspection und unabhängige Engine-/Host-/Transportlimits gelten weiterhin. |
| `safe` | Empfohlener Lern-/Startpunkt für die vollständige eingecheckte P1–P4-Form | Späte P4-Ergebnisse, die eine bereits gestartete Response nicht sicher ändern können, bleiben dort nicht-disruptiv, wo dies dokumentiert ist. |
| `strict` | Test der strikten Late-Action-Policy bei Profilen mit unterstützter Hostaktion | Eine eingecheckte Strict-Datei beweist keinen beobachteten client-sichtbaren Post-Commit-Abbruch. |
| `all` | Umfassende quellenbasierte Konfigurationsreferenz | `all` ist ein Layout und kein vierter Phase-4-Modus; es verwendet gültige Einstellungen wie `strict`. |

`DetectionOnly`, Engine `Off` und ein deaktivierter Connector sind
getrennte Konzepte und werden in den hostspezifischen Beispiel-Guides erklärt.

## Zehn logische Lösungen

| Logische Lösung | Off | Safe | Strict | All |
| --- | --- | --- | --- | --- |
| Apache | [off](apache/off/httpd.conf) | [safe](apache/safe/httpd.conf) | [strict](apache/strict/httpd.conf) | [all](apache/all/httpd.conf) |
| NGINX | [off](nginx/off/nginx.conf) | [safe](nginx/safe/nginx.conf) | [strict](nginx/strict/nginx.conf) | [all](nginx/all/nginx.conf) |
| HAProxy HTX | [off](haproxy/off/haproxy-htx.cfg) | [safe](haproxy/safe/haproxy-htx.cfg) | [strict](haproxy/strict/haproxy-htx.cfg) | [all](haproxy/all/haproxy-htx.cfg) |
| HAProxy SPOE/SPOP | [off](haproxy/spoe-spop/off/) | [safe](haproxy/spoe-spop/safe/) | [strict](haproxy/spoe-spop/strict/) | [all](haproxy/spoe-spop/all/) |
| Envoy ext_proc | [off](envoy/ext-proc/off/) | [safe](envoy/ext-proc/safe/) | [strict](envoy/ext-proc/strict/) | [all](envoy/ext-proc/all/) |
| Envoy ext_authz | [off](envoy/ext-authz/off/) | [safe](envoy/ext-authz/safe/) | [strict](envoy/ext-authz/strict/) | [all](envoy/ext-authz/all/) |
| Traefik Native UDS | [off](traefik/native-uds/off/) | [safe](traefik/native-uds/safe/) | [strict](traefik/native-uds/strict/) | [all](traefik/native-uds/all/) |
| Traefik forwardAuth | [off](traefik/forwardauth/off/) | [safe](traefik/forwardauth/safe/) | [strict](traefik/forwardauth/strict/) | [all](traefik/forwardauth/all/) |
| lighttpd Patched | [off](lighttpd/patched/off/) | [safe](lighttpd/patched/safe/) | [strict](lighttpd/patched/strict/) | [all](lighttpd/patched/all/) |
| lighttpd Stock | [off](lighttpd/stock/off/) | [safe](lighttpd/stock/safe/) | [strict](lighttpd/stock/strict/) | [all](lighttpd/stock/all/) |

## Was normalerweise angepasst werden muss

| Wert | Warum | Typisches Beispiel |
| --- | --- | --- |
| installierter Host-/Modulpfad | Distributionen und Build-Layouts unterscheiden sich | `/etc/nginx/nginx.conf` oder ein installierter Modulpfad |
| Rules-Dateipfad | Der Host muss die gewünschte geprüfte Rules-Datei lesen können | `/etc/modsecurity/no-crs-baseline.conf` |
| Listener-/Upstream-Ports | Lokale Anwendungen und Testumgebungen unterscheiden sich | `127.0.0.1:8080` / `127.0.0.1:8081` |
| Runtime-/Socket-Pfade | Services benötigen beschreibbare, private Runtime-Orte | private UDS oder Runtime-Verzeichnis außerhalb des Checkouts |
| Log-/Eventpfade | Der Service-Account muss sicher schreiben können | geschütztes und rotiertes JSONL-/Error-Log-Ziel |

Beispiel-Credentials, Private Keys, Cookies, Authorization-Werte oder sensible
Request-/Response-Bodies dürfen niemals in Versionskontrolle oder
Review-Evidence kopiert werden.

## Typischer Ablauf

1. Hostfamilie und logische Lösung wählen.
2. Mit dem passenden `safe`-Beispiel beginnen, sofern nicht gezielt eine
   andere Policy benötigt wird.
3. Hostspezifischen Beispiel-Guide lesen und Installations-/Runtime-Platzhalter
   ersetzen.
4. Hostkonfiguration mit dem nativen Checker validieren.
5. Build/Start soweit vorhanden über Root-Targets des Repositorys ausführen.
6. Wenn eine Runtime-Aussage benötigt wird, das passende Lifecycle-/Evidence-
   Target ausführen und die laufbezogenen Artefakte bewerten.

Ein Syntax-/Konfigurationscheck bestätigt nur Parsing/Laden. Er beweist keine
P1–P4-Ergebnisse, Production Readiness, CRS-Abdeckung oder Strict-Late-Verhalten.

## Regeln und Phasen-IDs

Die Repository-No-CRS-Baseline verwendet diese Testprofil-Regel-IDs:

| Regel-ID | Phase | Bedeutung |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die ausgewählte Policy-Grenze |

Dies sind IDs des Repository-Testprofils und keine OWASP-Core-Rule-Set-IDs.

## Detaillierte Konfigurationsreferenzen

Die Host-Guides verlinken quellenbasierte Konfigurationsreferenzen für Common
Runtime, ModSecurity-Engine-Direktiven und die Parseroberfläche des jeweiligen
Hosts. Generierte Konfigurationsreferenzen werden über ihre Generatoren
gepflegt und nicht isoliert manuell editiert.

Für Konzepte vor Syntax lesen Sie [Konfiguration](../docs/configuration.de.md).
Für die Semantik von Runtime-Ergebnissen lesen Sie
[Tests und Nachweise](../docs/testing-and-evidence.de.md).
