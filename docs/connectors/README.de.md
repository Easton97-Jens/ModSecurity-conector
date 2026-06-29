# Connector-Dokumente

**Sprache:** [English](README.md) | Deutsch

Status: umgesetzt

Connector-Dokumente erläutern das aktuelle Verhalten der Apache-, NGINX- und
HAProxy-Connectoren sowie die Anforderungen, die zukünftige Connectoren erfüllen
müssen, bevor sie Kompatibilität beanspruchen können.

## Dokumente

| Dokument | Zweck |
| --- | --- |
| `directive-parity.md` | Aktuelle Unterstützung und Semantik von Apache- und NGINX-Direktiven |
| `rule-load-stats.md` | Gemeinsame Regellade-Metadatenform und Apache/NGINX-Adaptersemantik |
| `future-connectors.md` | Einschränkungen bei der Planung von Envoy-, Lighttpd-, Traefik- und verzögerten Connectors |
| `../../reports/testing/real-world-connector-validation.md` | Aktuelles Real-World-Connector-Proof-Modell und Caveats zur Smoke-Evidence |
| `../../reports/testing/evidence/pr-evidence-summary.md` | PR #377 und PR #3564 Evidenzgrenzen |

## Upstream-Referenzen

| Connector | Upstream |
| --- | --- |
| Apache | https://github.com/owasp-modsecurity/ModSecurity-apache |
| NGINX | https://github.com/owasp-modsecurity/ModSecurity-nginx |
| HAProxy | https://github.com/haproxy/haproxy |
| Envoy | https://github.com/envoyproxy/envoy |
| Lighttpd | https://github.com/lighttpd/lighttpd1.4 |
| Traefik | https://github.com/traefik/traefik |

Kein zukünftiger Connector gilt als implementiert, bis er einen echten
HTTP-Client-zu-Server-Connector-zu-libmodsecurity-Pfad nachweisen kann. HAProxy
hat inzwischen einen evidence-begrenzten SPOA/SPOP-Runtime-Pfad; Envoy,
Lighttpd und Traefik bleiben zurückgestellt, bis Common-Metadaten und
Harness-Verhalten stabil genug sind, um connector-spezifische Proof-Pfade zu
entwerfen.
