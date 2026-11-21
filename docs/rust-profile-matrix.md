| Logical profile | Rust implementation | Evidence status |
|---|---|---|
| Apache | Rust host module P1-P2; real 200/403 smoke passed | passed: real Apache 200/403 smoke
| NGINX | Rust dynamic module P1-P2; real 200/403 smoke passed | passed: real NGINX 200/403 smoke
| HAProxy HTX | Not implemented | not executed |
| HAProxy SPOE/SPOP | Not implemented | not executed |
| Envoy ext_proc | Not implemented | not executed |
| Envoy ext_authz | Rust HTTP auth service behind real Envoy ext_authz; real 200/403 smoke passed | passed: real Envoy 200/403 smoke
| Traefik native UDS | Rust MSE1 UDS engine; BEGIN/EOS/DESTROY smoke passed | passed: MSE1 UDS 403 smoke
| Traefik forwardAuth | Rust HTTP auth service behind real Traefik forwardAuth; real 200/403 smoke passed | passed: real Traefik 200/403 smoke
| lighttpd patched | Not implemented | not executed |
| lighttpd stock/Sidecar | Rust auth-only proxy may serve stock-sidecar route | implementation complete; real host smoke not executed
