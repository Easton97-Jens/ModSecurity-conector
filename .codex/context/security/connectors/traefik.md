# Traefik Deep Security Delta

## Logical profiles

- `traefik-native-uds`: native Go middleware plus private UDS engine service
- `traefik-forwardauth`: forwardAuth request authorization plus mandatory response observer

Keep forwardAuth and native middleware evidence separate.

## Host-specific boundaries

Assess router selection/priority, middleware ordering, path mutation, Forwarded/X-Forwarded identity, forwardAuth request/response/body-limit semantics, native `CreateConfig`/`New`/`ServeHTTP`, `ResponseWriter` wrapping, optional writer interfaces and fast paths, context cancellation, client disconnect, streaming/flush/read-from behavior, Go concurrency/goroutines, private UDS engine service, frame protocol/session map, peer credentials, socket replacement/readiness, and local plugin staging/load integrity.

Pay special attention to:

- forwardAuth is request-oriented and cannot alone prove P3/P4;
- body truncation where auth sees less than upstream receives;
- router/path normalization before/after security middleware;
- forwarded-header spoofing and trusted-proxy semantics;
- `Flush`, `ReadFrom`, `Unwrap`, `Hijack`, streaming/SSE/WebSocket bypass classes where interfaces exist;
- post-commit P4 action versus visible response;
- UDS same-UID residual risk, peer credentials, replacement races, path length and cleanup;
- frame lengths/order/EOS/finish/destroy/transaction-ID isolation;
- plugin staging symlink/hardlink/race/dependency/cache poisoning.

## Required common checks

Load all common modules including `filesystem-ipc.md` and `protocol-framing.md`.

## Traefik-specific validation seeds

Where current harnesses support them, cover forwardAuth Allow/Deny/timeout/error/malformed response/body truncation/forwarded-header manipulation, native writer Write/WriteHeader/Flush/ReadFrom/streaming/cancellation, parallel requests, UDS path and replacement cases, frame parser/session ordering, service restart, plugin load confirmation, and a legitimate follow-up request.
