# Change Record: CR-20261101-sec-traefik-native-001

**Language:** English | [Deutsch](CR-20261101-sec-traefik-native-001.de.md)

Focused product correction; Framework owns every regression and test adapter.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261101-sec-traefik-native-001 |
| Date (UTC) | 2026-11-01 |
| Base revision | `a6001a09210bc9516256d28af5da45d73f0fe2f2` |

## Motivation and problem statement

SEC-TRAEFIK-NATIVE-001: a nonterminal informational WriteHeader consumed request
EOS, final P3 and Common commit. A later final-only protection header escaped
P3; a real HTTP regression observed final 200 and protected upstream bytes
instead of the expected denial.

## Acceptance criteria

Nonterminal 1xx leaves final P2/P3/commit state available. Final headers and status
reach P3 exactly once; allow, deny, redirect, bounded streaming, P4/EOS,
101/Hijack and cleanup remain valid. Verify real informational responses and
the selected Ubuntu Traefik/plugin/UDS/Common/libmodsecurity boundary.

## Implementation decision and rationale

Handle 100--199 except 101 before final response preparation. Retain bounded
header validation and forward the informational head directly without clearing
the host header map or changing engine state. Existing final and upgrade paths
remain responsible for P3 and commitment. No response-body buffer was added.

## Changed files

`connectors/traefik/native_middleware/middleware.go`, `docs/connectors/traefik.md`,
`docs/connectors/traefik.de.md`, and this EN/DE Change Record pair. The independent
Framework branch owns tests, fixtures, adapters, inventory and test documentation.

## Commands executed

RTK-wrapped Framework public overlay/inventory invocation with explicit
CONNECTOR_ROOT, exact base CONNECTOR_REVISION, TEST_ROOT and external output:
31 new expanded Go cases passed after the fix. The real HTTP reproducer failed
before it; three no-1xx controls passed. Fresh full native-module
`go test -race -mod=readonly -count=1 -overlay <framework-overlay> ./...` and
`go vet -mod=readonly -overlay <framework-overlay> ./...` passed. `gofmt` was
applied. Parent bilingual/link/Change Record checks and Framework documentation
checks passed. Gitleaks 8.30.1 found no leaks in the changed-file snapshot.
Committed-pair run results are recorded with the PR verification evidence
after execution.

## Security impact

Restores prospective final-response-header enforcement after informational
responses. Final P3 denial/redirect withholds upstream bytes while permitting
the middleware's own rejection body. Informational headers retain configured
limits. No isolation, identity, engine or validation control was weakened.

## Runtime evidence

Ubuntu 26.04.1; Go 1.27.3; pinned Traefik 3.7.13. Framework trial `host-run-5`
passed all four probes: 103/deny 403, no-103/deny 403, 103/allow 201 and legitimate
followup 201 on the same TCP connection. Each had one correlated final P3;
denials matched rule 1199001 and exposed only the own rejection body. No recovery
panic remained; processes, private sockets and transient workspaces were cleaned.
Evidence is external under
`/var/tmp/codex/ModSecurity-conector/sec-traefik-native-001/host-run-5`.
This trial used base HEAD plus middleware SHA-256
`03944b42c9d64391eda579aa0cdd5a6cc239b02baf5907ca1c6357a61385c337`;
it is distinct from the three committed-pair acceptance repetitions reported
separately in the PR.

## Known limitations

Earlier host trials failed a portable private-UDS pathname cap, route-readiness
timing, or premature test-client cancellation during P4/cleanup. These failures
remain retained. The Framework adapter now observes physical EOF on its final
Connection: close probe; panic detection remains enabled. No claim covers other
connectors, forwardAuth, HTTP/2/3, MRTS or a general protocol matrix.

## Remaining risks

The raw Hijack ownership contract is preserved, not redesigned. Source tests do
not establish every upgrade or deployment scenario. Existing CI and Quality Gates
must be evaluated at the delivered PR head before any separately authorized merge.

## Checks not run and rationale

No full connector/protocol/MRTS matrix: expressly outside this correction.
No production deployment or merge. Hosted CI/Sonar status belongs to the PR's
actual current head, not this local execution record.

## Final diff and review status

An independent read-only candidate review found no concrete surviving bypass or
regression in the changed seam. Product and Framework remain separate commits
and Draft PRs. Integrate Framework tests first; a later explicitly authorized
Parent pin update can select that merged Framework revision. No gitlink change,
direct master push or merge is part of this task.
