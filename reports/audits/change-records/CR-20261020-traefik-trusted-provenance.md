# Change Record: CR-20261020-traefik-trusted-provenance

**Language:** English | [Deutsch](CR-20261020-traefik-trusted-provenance.de.md)

Product change for #382; host acceptance remains owned by #413.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261020-traefik-trusted-provenance |
| Date (UTC) | 2026-10-20 |
| Base revision | `c5012b70c78ae2629eeede6603f591dfb002dd9a` |

## Motivation and problem statement

Traefik's C authorization route could not attach trusted downstream run/case/connection provenance before P1. HTTP forwarding fields and the authorization loopback socket cannot establish physical client reuse.

## Acceptance criteria

Copy bounded trusted identifiers before P1; preserve old callers; reject forged, duplicate, stale and ambiguous bindings; bind authorization replies privately; derive EOS and cleanup from runtime state; validate the native, private-socket, Go/race/vet and security boundaries.

## Implementation decision and rationale

Additive Common begin and authorization entry APIs preserve existing signatures and profile layout. The opt-in Traefik MTP1 listener uses a separate private sibling socket, same UID/GID authentication, 128 fixed slots, five-second leases and random one-use capabilities. Metadata is copied before native P1 and the service reply status/companion handle is attested over that same session. The outer observer consumes this attestation before commitment. The MRC1 wire protocol and ordinary/default call paths, shared Envoy connector code, generators and matrices remain unchanged; the Common registry gains an additive trusted-confirmation API. Trusted Allow phase records do not invent rule interventions. Cleanup reserves its sequence before flow immutability and writes only after native Free and contract cleanup; sink failure cannot become successful checked cleanup.

## Changed files

`common/runtime/msconnector_runtime.{c,h}`, `common/runtime/http_authorization_service.{c,h}`; Traefik `src/traefik_provenance.{c,h}`, `src/traefik_forwardauth_service_main.c`, `build/build-connector.sh`, `response_observer/observer.go`, `response_observer/provenance{,_test}.go`, `response_observer/README{,.de}.md`; `ci/checks/common/check-http-authorization-service-timeout.sh`, `ci/checks/common/http_authorization_service_timeout_smoke.c`; `tests/http_authorization_service_{detached_worker,peer_close,trusted_binding}_smoke.c`, `tests/test_http_authorization_service_worker_contract.py`, `tests/test_i10_service_callers.py`, `tests/test_runtime_event_sink_failures.py`, `tests/test_runtime_trusted_provenance.py`, `tests/test_traefik_trusted_provenance.py`, `tests/test_engine_response_limits.py`, `tests/transaction_phase_runtime_companion_test.c`, and this Change Record pair.

## Commands executed

All shell commands used RTK. Initial verification before the preclaim correction: the repository Traefik build passed with `MODSECURITY_INCLUDE_DIR=/usr/include`, `MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu` and an external task build directory. Observer `go test -count=1 -v ./...` and `go test -race -count=1 -v ./...` each passed 42 tests; `go vet ./...` passed. Go checks explicitly used the isolated Go 1.27.2 GOROOT and saved `go env GOROOT GOVERSION`. The initial combined Common/Auth/native/private-socket suite passed 100 tests with four skips (three existing skips and the foreign-UID test blocked by the restricted test-root traversal). The same foreign UID/GID control separately passed outside the sandbox with a searchable external test root. Common SDK/security contracts and Change Record structure passed. Repository bilingual pairs plus links in all four changed documentation files passed; the full bilingual/link check encountered 22 pre-existing missing Framework-submodule link targets.

After the preclaim correction, 28 focused Python/native tests passed with one sandbox UID skip; that UID/GID control separately passed outside the sandbox. Real MTP1/Common delayed-claim positive and compiled missing-refresh negative controls passed. Isolated Go 1.27.2 test/race/vet, strict C17 syntax checks, Common security contract and `git diff --check` passed. The whole-repository bilingual check still reports only the same 22 missing Framework-submodule targets. A final narrow replay-test correction accepts reset/broken-pipe at either send or receive on the already-closed peer; the focused replay control passed after that correction.

## Security impact

Only the private authenticated lease supplies provenance. Client capabilities are discarded before reservation and the service excludes the internal token from native P1 headers after successful claim. Deployment requires outer observer → built-in ForwardAuth → inner observer with `confirmProvenance: true` → backend. The explicit `authRequestHeaders` list includes the private token. The inner instance requires the package-private outer request context, confirms once before the backend and removes both private headers/trailers. Matching Unix IDs are one trust domain, not binary attestation. Existing authentication and validation remain enforced.

## Runtime evidence

Tests exercise physical Unix sockets, real libModSecurity P1 Deny, Allow with companion P3/P4, cancellation before Request-EOS, actual Common serialization/cleanup and sink failures. A compiled missing-copy negative control reproduces the provenance gap. Controls cover capacity saturation without neighbor eviction, real foreign UID/GID rejection, fake-Go-transport ordering through a backend wait over five seconds, missing/duplicate inner confirmation, typed cancellation for Panic/Cancel/Return before headers, and a physical payload-free cleanup-failure log. Separately, genuine Common/native handles and physical MTP1 query prove initial five-second expiry and one confirmed handle surviving 5.1 seconds. A compiled control omitting only the expiry update reproduces that late-claim failure. Shutdown confirmation denial uses a real unclaimed handle with an explicitly synthetic metadata-only blocking lease. These layers do not qualify a Traefik host keepalive ID or prove downstream client delivery.

## Known limitations

The observer lacks a reliable live-connection close hook. Its instance-local HMAC tuple token is correlation and `connection_reused` remains false. Physical same-live-socket evidence remains mandatory. Runtime body-finish state, never TCP EOF, supplies `eos_seen`. `maxResponseBodySize=32768` remains authorization-response capacity. Inner confirmation caches the attestation before backend waiting. MRC1 claim occurs normally at the first response header; an earlier exit claims only for immediate typed cancellation with a detached bounded context. Failed cleanup is retained/logged and existing bounded companion expiry remains fallback.

## Remaining risks

The opt-in mode depends on the documented middleware order and inner confirmation. Authorization/confirmation exceeding the fixed five-second reservation lease fails closed. Ordinary MRC1 preclaim expiry remains five seconds. The peer-authenticated inner MTP1 query performs exactly one locked confirmation of its unused, still-valid handle before returning it: expiry becomes the original handoff plus configured TTL (Traefik 30 seconds), granting only the remaining lifetime. Deny/empty, expired, replayed, claimed, in-use, foreign and shutdown entries cannot extend; callback failure blocks backend entry. The Go slow-backend test establishes fake-transport ordering only; a physical MTP1/Common registry test verifies ordinary failure and confirmed success after 5.1 seconds. Completion runs only after a successful private claim, including a subsequent runtime-begin failure. Independent final review and Traefik host retakes remain required.

## Checks not run and rationale

No full Traefik host acceptance, CI or Sonar result is asserted for this uncommitted diff. #413 owns host retakes and ID qualification after product review. Full repository bilingual/link success is blocked by the uninitialized Framework submodule; no Framework content or shared generator was changed to conceal it. Changed-file links and repository language pairs were checked independently.

## Final diff and review status

Uncommitted diff on base `c5012b70c78ae2629eeede6603f591dfb002dd9a`; independent security and lifecycle reviews found no blocker. `git diff --check` passed. This worker has not committed, pushed or merged. Host retakes and repository-wide documentation prerequisites remain explicit.
