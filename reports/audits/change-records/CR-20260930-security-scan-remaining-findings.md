# Security scan remaining findings remediation

**Language:** English | [Deutsch](CR-20260930-security-scan-remaining-findings.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-security-scan-remaining-findings |
| Date (UTC) | 2026-09-30 |
| Base revision | 9bc87cbdb600b09c6edd02667a75b117a1f09eea |
| Delivery target | Pull request against `master`; no merge |

## Motivation and problem statement

The supplied ModSecurity-conector scan identified three validated findings. The NGINX `error_page` intervention finding is already remediated in the base revision by merged PR #391, so this change does not duplicate that code. The remaining work removes an HAProxy error-continuation escape from four closed-default SPOE/SPOP profiles and hardens response-companion UDS peer and path identity before a response observer sends `CLAIM`.

## Acceptance criteria

Positive NGINX intervention behavior remains supplied by the base revision. Every listed HAProxy profile must keep `fail-mode=closed` and omit `option continue-on-error`. A response companion must start only under a private directory whose complete ancestor chain resists cross-UID replacement. Envoy and Traefik response observers must authenticate the connected UDS server with Linux `SO_PEERCRED` before `CLAIM`, reject missing or mismatched UID/GID credentials, and fail closed when no Linux credential mechanism is available.

## Implementation decision and rationale

The HAProxy change deletes only the error-continuation option from the four affected profile files and adds a focused regression contract that asserts the profiles stay closed by default. The Common Runtime exposes one canonical directory-chain check shared by the response transport and Traefik engine: every ancestor must be owned by the effective service UID or UID 0 (the trusted superuser), and writable ancestors must also be sticky and protect the owned child from cross-UID replacement.

The Envoy and Traefik observers use explicit expected UID/GID pairs. Absent configuration defaults to the observer process's effective UID/GID; an explicit identity requires both fields and permits an intentional value of zero. The only production Envoy connection path is `dialWithExpectedPeer`; it authenticates immediately after connecting and before any `CLAIM` bytes can be written. Protocol-framing tests construct their test client separately and do not provide a production unauthenticated route.

## Changed files

- common/runtime/{msconnector_runtime.c,msconnector_runtime.h,response_companion_transport.c}
- tests/response_companion_transport_test.c
- examples/haproxy/spoe-spop/{strict,safe,off,all}/spoe.cfg
- tests/test_haproxy_spop_peer_isolation_contract.py
- connectors/envoy/ext_proc/internal/responseobserver/{protocol.go,service.go,peercred_linux.go,peercred_other.go,peercred_linux_test.go}
- connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main.go
- connectors/traefik/src/traefik_engine_service.c
- connectors/traefik/response_observer/{observer.go,observer_test.go,peercred_linux.go,peercred_other.go}
- connector source maps, response-observer documentation, focused CI workflows, and this paired record

## Commands executed

GitHub connector inspection compared the prepared scope with base revision 9bc87cbdb600b09c6edd02667a75b117a1f09eea and confirmed that the NGINX `error_page` remediation is already in the base. The proposed focused CI commands are:

```sh
python3 -m unittest -v tests.test_haproxy_spop_peer_isolation_contract
go test -mod=readonly -count=1 ./internal/responseobserver
go test -mod=readonly -count=1 -run 'a^' ./cmd/msconnector-envoy-response-observer
go test -mod=readonly -count=1 ./...
```

They are configured in the PR workflows. They have not been claimed as locally passed from this Windows workspace.

## Security impact

The HAProxy profiles no longer turn an unavailable or errored SPOE agent into a continuation path in configurations designated closed-default. The shared Common Runtime policy rejects a socket parent below an ancestor owned by an untrusted UID, and rejects a writable ancestor unless it is sticky and protects the service-owned child. Traefik reuses that exact policy. The Go observers bind their response-companion trust decision to kernel-supplied peer credentials before protocol state is claimed; credential failure becomes the existing pre-commit 503 fail-closed behavior.

## Runtime evidence

The new regression tests demonstrate the expected source and protocol boundaries. Linux tests use a real local Unix listener and assert that a mismatched peer identity receives zero request bytes before rejection. The C transport test creates a private child under a writable, non-sticky ancestor and requires startup failure; the companion source contract additionally locks the shared trusted-owner check ahead of the writable-mode allowance and its Traefik reuse. These are bounded component tests, not a live Envoy, Traefik, HAProxy, or NGINX deployment acceptance claim.

## Known limitations

Linux `SO_PEERCRED` authenticates the kernel-reported UID/GID for the UDS peer. It does not attest the executable, file integrity, MAC label, or user-namespace mapping. Matching Unix IDs form one trust domain. The directory-chain check evaluates ownership, mode bits, and sticky protection. UID 0 is deliberately trusted for standard root-owned sticky ancestors such as `/tmp` and `/var/tmp`; production sockets should remain below a service-owned mode-0700 leaf. Deployments must also avoid POSIX ACLs or mount policies that grant another identity replacement authority.

## Remaining risks

The change intentionally has no non-Linux credential fallback, so unsupported deployments fail closed rather than silently continuing. Operators who run a companion under a different Unix identity must configure both expected IDs. The focused tests do not establish all response-phase host behavior, arbitrary filesystem namespaces, or a live SPOE-agent failure injection. The base NGINX remediation's host-level evidence remains separate from this PR.

## Checks not run and rationale

The local Sonar CLI and a direct SonarQube connector tool were unavailable, and the local container daemon was inaccessible; no credentials, packages, or service configuration were altered to work around that limitation. The exact-head SonarQube Cloud GitHub check is therefore the PR quality gate. Local C/Go execution was also unavailable from the read-only Windows workspace; the focused commands are delegated to exact-head GitHub Actions.

## Final diff and review status

The diff is limited to the two remaining findings, their regression coverage, and deployment documentation. NGINX source is intentionally untouched because #391 is already the current base. A review specifically checks that UDS authentication precedes `CLAIM`, that unsupported platforms fail closed, and that all four HAProxy profiles omit the continuation option. PR CI and reviewer approval remain pending at record creation.
