# Connector Docs

Status: implemented

Connector docs explain the real-world Apache and NGINX PoCs and the requirements
future connectors must meet before claiming compatibility.

## Documents

| Document | Use |
| --- | --- |
| `apache-poc.md` | Apache source-build, module build, and smoke harness status |
| `nginx-poc.md` | NGINX source-build, dynamic module, and smoke harness status |
| `nginx-poc-plan.md` | NGINX lifecycle and build model notes |
| `apache-vs-nginx-poc.md` | Shared YAML evidence and connector lifecycle differences |
| `real-world-connector-validation.md` | Required proof path through real server connector modules |
| `future-connectors.md` | HAProxy, Envoy, Lighttpd, and Traefik planning constraints |

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
server connector to libmodsecurity path.
