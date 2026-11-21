| Logical profile | Rust implementation | Evidence status |
|---|---|---|
| Apache | Rust host module P1-P2; real 200/403 smoke passed | passed: real Apache 200/403 smoke
| NGINX | Rust dynamic module P1-P2; real 200/403 smoke passed | passed: real NGINX 200/403 smoke
| HAProxy HTX | Rust reverse-proxy sidecar behind real HAProxy; real 200/403 smoke passed | passed: real HAProxy 200/403 smoke
| HAProxy SPOE/SPOP | Rust SPOP agent implemented; real /deny 403 enforcement not proven | blocked: 404 reached upstream
| Envoy ext_proc | Rust tonic gRPC ExternalProcessor; real 200/403 smoke passed | passed: real Envoy ext_proc 200/403 smoke
| Envoy ext_authz | Rust HTTP auth service behind real Envoy ext_authz; real 200/403 smoke passed | passed: real Envoy 200/403 smoke
| Traefik native UDS | Rust MSE1 UDS engine; BEGIN/EOS/DESTROY smoke passed | passed: MSE1 UDS 403 smoke
| Traefik forwardAuth | Rust HTTP auth service behind real Traefik forwardAuth; real 200/403 smoke passed | passed: real Traefik 200/403 smoke
| lighttpd patched | Existing patched module retained as thin host integration; Rust host API not fully wired to stream hooks | blocked: Rust stream-hook wiring and host smoke
| lighttpd stock/Sidecar | Rust reverse-proxy sidecar; real 200/403 smoke passed | passed: real Rust sidecar 200/403 smoke
