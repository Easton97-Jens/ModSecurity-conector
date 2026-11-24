# Connector-Beispiele

**Sprache:** [English](README.md) | Deutsch

Host und Topologie wählen und das passende Beispiel anpassen. Vor der Übernahme
älterer Optionen die [Migration](../docs/migration.de.md) prüfen.

## Host wählen

| Hostfamilie | Beispiel-Guide | Logische Profile |
| --- | --- | --- |
| Apache | [Apache](apache/README.de.md) | `apache` |
| NGINX | [NGINX](nginx/README.de.md) | `nginx` |
| HAProxy | [HAProxy](haproxy/README.de.md) | `haproxy-htx`, `haproxy-spoe-spop` |
| Envoy | [Envoy](envoy/README.de.md) | `envoy-ext-proc`, `envoy-ext-authz` |
| Traefik | [Traefik](traefik/README.de.md) | `traefik-native-uds`, `traefik-forwardauth` |
| lighttpd | [lighttpd](lighttpd/README.de.md) | `lighttpd-patched`, `lighttpd-stock` |

Die [Body-Inspection-Matrix](../docs/body-inspection-review-matrix.de.md)
beschreibt je Profil die Request-Body-Sichtbarkeit, Anforderungen an
Response-Companions und Grenzen später Aktionen.

## Konfigurationslayout wählen

| Layout | Verwendung |
| --- | --- |
| `off` | Native Interventions- und Fehlerbehandlung nutzen. Die konfigurierten Engine-Regeln bestimmen die Inspection. |
| `safe` | Einstieg in die vorsichtige Behandlung später Entscheidungen des Profils. Native Reject-Ergebnisse und Verarbeitungsfehler behalten ihre Wirkung. |
| `strict` | Die strikte späte Aktion des Profils wählen. Der Start setzt passende Hostunterstützung voraus. |
| `all` | Die vollständige Konfigurationsreferenz nachschlagen. Das Beispiel wählt einen gültigen Phase-4-Modus, oft `strict`, mit denselben Startvoraussetzungen. |

`SecRuleEngine DetectionOnly`, `SecRuleEngine Off`, der deaktivierte Hostconnector
und Phase-4-`off` wirken auf unterschiedlichen Ebenen. Siehe [Regelbeispiele](common/rule-examples.de.md).

## Zehn logische Lösungen

| Logische Connectorlösung | Off | Safe | Strict | All |
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

## Kompatibilitäts- und Companion-Grenzen

Die Host-Guides kennzeichnen eigenständige Kompatibilitätsdateien und nennen
die für Response-Inspection erforderlichen Companions.

- [HAProxy-SPOE/SPOP-Kompatibilitätsmaterial](haproxy/README.de.md#spoespop-kompatibilitätsmaterial)
- [Envoy-ext_authz-Kompatibilität](envoy/README.de.md#ext_authz-kompatibilität)
- [Traefik-forwardAuth-Kompatibilität](traefik/README.de.md#forwardauth-kompatibilität)
- [lighttpd-Sidecar-Kompatibilität](lighttpd/README.de.md#sidecar-kompatibilität)

## Anzupassende Werte

Modul- und Regelpfade, Listener, Upstreams, Service-Identitäten, private
Sockets und Logziele nach dem gewählten Host-Guide anpassen. Optionen, die
betreiberspezifische Zugangsdaten benötigen, vor dem Aktivieren prüfen.
Zugangsdaten, Schlüssel und sensible Traffic-Daten aus Beispielen und Logs heraushalten.

Body-Zugriff, MIME-Auswahl, Limits und Limitaktionen in den
libModSecurity-Regeln einstellen. Die Engine-Direktiven stehen unter
[Konfiguration](../docs/configuration.de.md). Separate Host- und Transportlimits
erklärt der [Body-Limit-Vertrag](../docs/phase4-mode-budget.de.md).

Nach dem Anpassen den dokumentierten Konfigurationscheck des Hosts ausführen.
Das benötigte Laufzeitverhalten anhand von [Tests und Nachweisen](../docs/testing-and-evidence.de.md)
prüfen.

## Detaillierte Referenzen

Der passende Host-Guide verweist auf seine generierte Konfigurationsreferenz.
[Common-Beispiele und Referenzen](common/README.de.md) behandeln Common Runtime,
Engine-Direktiven und Beispielregeln. Generierte Referenzen über ihre Quellen
und Generatoren aktualisieren.
