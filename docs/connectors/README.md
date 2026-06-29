# Connector Docs

**Language:** English | [Deutsch](README.de.md)


Status: implemented

Connector docs explain current Apache, NGINX, and HAProxy connector behavior and
the requirements future connectors must meet before claiming compatibility.

## Documents

| Document | Use |
| --- | --- |
| `directive-parity.md` | Current Apache and NGINX directive support and semantics |
| `rule-load-stats.md` | Common rule-load metadata shape and Apache/NGINX adapter semantics |
| `future-connectors.md` | Envoy, Lighttpd, Traefik, and deferred connector planning constraints |
| `../../reports/testing/real-world-connector-validation.md` | Current real-world connector proof model and smoke evidence caveats |
| `../../reports/testing/evidence/pr-evidence-summary.md` | PR #377 and PR #3564 evidence boundaries |

## Upstream References

| Connector | Upstream |
| --- | --- |
| Apache | https://github.com/owasp-modsecurity/ModSecurity-apache |
| NGINX | https://github.com/owasp-modsecurity/ModSecurity-nginx |
| HAProxy | https://github.com/haproxy/haproxy |
| Envoy | https://github.com/envoyproxy/envoy |
| Lighttpd | https://github.com/lighttpd/lighttpd1.4 |
| Traefik | https://github.com/traefik/traefik |

No future connector is implemented until it can prove a real HTTP client to
server connector to libmodsecurity path. HAProxy now has an evidence-scoped
SPOA/SPOP runtime path; Envoy, Lighttpd, and Traefik remain deferred until the
Common metadata and harness behavior are stable enough to design
connector-specific proof paths.
