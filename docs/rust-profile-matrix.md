| Logical profile | Rust implementation | Evidence status |
|---|---|---|
| Apache | Rust host module P1-P2; real 200/403 smoke passed | passed: real Apache 200/403 smoke
| NGINX | Shared C ABI exists; direct host module not replaced | not executed |
| HAProxy HTX | Not implemented | not executed |
| HAProxy SPOE/SPOP | Not implemented | not executed |
| Envoy ext_proc | Not implemented | not executed |
| Envoy ext_authz | Not implemented | not executed |
| Traefik native UDS | Rust MSE1 UDS engine; BEGIN/EOS/DESTROY smoke passed | passed: MSE1 UDS 403 smoke
| Traefik forwardAuth | Standalone proxy is not forwardAuth-compatible | not executed |
| lighttpd patched | Not implemented | not executed |
| lighttpd stock/Sidecar | Not implemented | not executed |
