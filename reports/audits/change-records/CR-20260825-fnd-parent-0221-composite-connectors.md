# CR-20260825 — Bounded Envoy and Traefik composite response correlation

**Language:** English | [Deutsch](CR-20260825-fnd-parent-0221-composite-connectors.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260825-fnd-parent-0221-composite-connectors` |
| Date (UTC) | 2026-08-25 |
| Base revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Finding | `FND-PARENT-0221` |
| Scope | Parent-only Envoy `ext_authz` + `ext_proc` and Traefik `forwardAuth` + private-UDS response composite, tests, configuration, and paired documentation |
| Framework/MRTS boundary | No Framework or MRTS source, branch, `HEAD`, Gitlink, or delivery change |
| Delivery disposition | The user authorized a task-owned worktree, scoped commit/push, and exactly one Parent Draft PR against `master`; no merge. Commits `931d6eb81207997169719bb475d50274ae281eed` and `9aeb0b551b34a0e44b9409130c2ecafeac641530` are on Draft PR #341. Sonar analysis `af6a96df-297f-47dd-af26-83b5315327e6` closed/fixed nine of ten vulnerability records, but left LOW `python:S5332` open at the controlled upstream. The scoped TLS follow-up is locally validated; commit/push and exact-successor hosted validation remain pending. FND-SONAR-0061 remains P0/high, `in_progress`, release- and candidate-integration-blocking; no green Sonar result is claimed. `FND-PARENT-0221` remains `in_progress`/`blocked_missing_evidence`, so this change is not eligible for `verified_pr` or merge. |

## Motivation and problem statement

Request-only authorization hooks do not by themselves preserve the Common
transaction needed to assess P3/P4 after upstream response processing. The
change implements bounded server-owned correlation for Envoy and Traefik
without allowing a caller to choose a transaction or inject a reusable lease.

## Acceptance criteria

- P1--P4 observations act only on the same retained Common transaction for the
  supported Envoy or Traefik composite path.
- The lease is server-generated, integrity-bound, bounded, single-use, and
  absent from client, upstream, and event boundaries.
- Traefik sends raw P1 headers only in a bounded versioned private-UDS
  snapshot; ForwardAuth HTTP receives only the opaque lease and
  Traefik-generated forwarded metadata.
- Reservation, timeout, disconnect, request termination, and finish paths have
  one bounded terminal cleanup and fail closed.
- P4 Safe remains log-only after commitment. P4 Strict is not promoted without
  an actual client-visible reset/abort.
- Focused source checks and real H1 host evidence run against the current
  binary and retain their stated evidence scope.

## Implementation decision and rationale

`composite.Coordinator` retains a bounded immutable reservation snapshot and
issues an HMAC-authenticated opaque lease only after a payload-free
`reservation` lifecycle opener is accepted. `Activate` consumes only that
snapshot for P1 and binds trusted forwarded method, URI, and Host metadata to
the reservation; it does not accept a raw request-context capsule over the
ForwardAuth HTTP hop. Snapshot and lease material are wiped on terminalization.

The Traefik outer middleware strips caller-supplied internal headers and
trailers, reserves over its owner-only UDS session, forwards the lease only to
the immediate inner ForwardAuth call, and strips it before the real upstream
and client response. UDS read and result-write deadline failures retain a
`timeout` reason. When a UDS failure occurs before HTTP commitment, the outer
writer clears pending upstream headers/body and emits a sanitized 503.
Request-terminal ForwardAuth decisions now write the same normalized final
status recorded as their host action, so an invalid deny/redirect status cannot
become an informational or success response. The private P1 snapshot also
preserves a known zero transport `Content-Length` rather than silently omitting
the explicit empty-body field.

The Envoy composite keeps its protected `ext_authz` dynamic-metadata handoff
and uses `ext_proc` for response observation. The shared evidence verifier
recognizes the payload-free reservation opener and requires it for a
missing-metadata pre-admission receipt. Before the Envoy composite records or
emits a disruptive P1/P2/P3 outcome, one action-specific normalizer now keeps
the recorded host action equal to the wire result: denies are `4xx`--`5xx`,
redirects require a non-blank target and use `3xx` plus `Location`, and every
other malformed decision fails closed as `403`.

The protected terminal marker allows an `ext_authz` local reply through
`ext_proc` only as a validated `3xx` with exactly one safe `Location`, or as a
`4xx`--`5xx` without one. Every other marker fails closed as a sanitized `503`
without opening a second Common transaction.

## Security impact

The affected boundary is authorization-to-response correlation. The controls
prevent client-selected correlation, raw P1 header propagation through the
ForwardAuth HTTP trust boundary, replay across UDS sessions, and lease egress
to clients/upstreams/events. Bounds apply before snapshot copies or protocol
allocations. A focused independent post-fix review found no supported-path
high/critical issue or authorization bypass.

Request-terminal host-action metadata and the emitted ForwardAuth HTTP status
now remain identical after fail-closed normalization; malformed `100`--`399`
deny/redirect statuses cannot yield an interim or successful client response.
Known zero transport content length is retained in the bounded P1 snapshot.
The same invariant now covers Envoy composite P1/P2 and pre-commit P3
immediate replies, including action-preserving valid redirects and protected
`ext_authz`--`ext_proc` terminal continuation.

`Hijack` and `Unwrap` remain unsupported downstream response-path escape
hatches; they are excluded from no-egress and P3/P4 guarantees. After an HTTP
response is committed, a replacement 503 is intentionally impossible and the
response path remains log-only where applicable.

## Changed files

- `common/rules/modsecurity_p1_p4_vectors.conf` and
  `common/rules/p1_p4_traffic_vectors.json`
- `connectors/composite_harness/verify_matrix_evidence.py` and its tests
- Envoy composite coordinator, adapter, command, configuration, build, and
  host-runner paths under `connectors/envoy/`
- Traefik `composite_middleware/`, composite configuration, driver, upstream,
  host runner, and `README.md` / `README.de.md` under `connectors/traefik/`
- Sonar remediation paths in `ci/lib/runtime_path_utils.py`,
  `connectors/composite_harness/verify_matrix_evidence.py`, and the Traefik
  composite harness helpers and focused tests
- this English/German Change Record pair and the paired archive indexes

## Commands executed

### Tests and actual results

The four explicit pre-fix reproductions below exited `1` as expected; all
post-fix validation commands below exited `0`.

- `CGO_ENABLED=1 go test -race -count=1 ./internal/composite ./internal/compositeenvoy ./internal/compositetraefik ./cmd/msconnector-composite` in `connectors/envoy/ext_proc` — focused coordinator, Envoy, UDS, ForwardAuth, and command race tests passed.
- `go test -race -count=1 ./...` in `connectors/traefik/composite_middleware` — middleware race tests passed.
- `go vet ./internal/composite ./internal/compositeenvoy ./internal/compositetraefik ./cmd/msconnector-composite` in `connectors/envoy/ext_proc` and `go vet ./...` in `connectors/traefik/composite_middleware` — passed.
- `go test -count=1 -run TestForwardAuthNormalizesInvalidRequestDenyStatus ./internal/compositetraefik` — first reproduced a malformed P1 deny reaching the client as `103`; after normalization it passed for both an informational and a success-status input.
- `go test -count=1 -run 'TestCheckNormalizesMalformedRequestDenyStatus|TestCheckPreservesValidatedRedirect|TestNormalizePolicyDecisionRejectsInvalidRedirect|TestNormalizePolicyDecisionRejectsUnsafeRedirectTarget|TestProcessNormalizesMalformedP3DenyStatus|TestSendImmediatePreservesValidatedRedirect|TestProcessMarkedTerminalRedirectPassesThrough|TestProcessMarkedTerminalServerErrorPassesThrough|TestProcessMarkedTerminalInvalidRedirectFailsClosed' ./internal/compositeenvoy` — first reproduced Envoy P1/P2/P3 status/evidence divergence, dropped redirect location, and a marked terminal redirect/5xx replaced by `503`; after action-specific normalization and terminal-marker validation it passed for malformed `103`, `200`, and `600` deny statuses, safe redirects, invalid redirect fallback, and terminal continuation without a second transaction.
- `go test -count=1 -run TestReservationPayloadPreservesZeroTransportContentLength ./...` — first reproduced the omitted zero-length P1 field; after the fix it passed.
- `PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v connectors.composite_harness.test_verify_matrix_evidence connectors.traefik.harness.test_composite_config` — 22 verifier/configuration tests passed.
- `gofmt -d` for changed Go files and `sh -n connectors/envoy/build/build_composite.sh connectors/envoy/harness/run_envoy_composite_matrix.sh connectors/traefik/harness/run_traefik_composite_matrix.sh` — no formatter or shell-syntax diagnostic.
- `BUILD_ROOT=<task-build-root> ... sh connectors/envoy/build/build_composite.sh` — the rebuilt Common/libmodsecurity Composite passed for Envoy release `1.39.0`.
- Focused paired-record/document language-switch, required-heading, and local-link-target inspection — exit `0`; the affected English/German pairs and local targets are present.
- `make check-bilingual-docs` — exit `2`; the new records and affected composite documents passed their own structural checks, while pre-existing repository links to the uninitialized Framework submodule are missing.
- `make check-doc-links` — exit `2` for the same pre-existing missing Framework-submodule link targets; no affected composite or Change-Record target was reported missing.

## Runtime evidence

Fresh Traefik `3.7.10` H1 host runs against the then-current Composite binary
returned:

| Case | Client status | Evidence scope |
| --- | ---: | --- |
| P1 allow | 200 | `LIFECYCLE_ONLY` P1/P2/P3/P4 |
| P1 deny | 403 | `LIFECYCLE_ONLY` P1 |
| P2 allow | 200 | `LIFECYCLE_ONLY` P1/P2/P3/P4 |
| P2 deny | 403 | `LIFECYCLE_ONLY` P1/P2 |
| P2 oversize | 413 | `LIFECYCLE_ONLY` P1/P2 |
| P3 deny | 403 | `LIFECYCLE_ONLY` P1/P2/P3 |
| P4 Safe | 200 | `LIFECYCLE_ONLY` P1/P2/P3/P4, log-only |
| metadata omitted | 503 | `LIFECYCLE_ONLY` pre-admission reservation plus terminal disconnect |
| P2-to-P3 timeout | 503 | `LIFECYCLE_ONLY` P1/P2 plus terminal timeout |

Every listed Traefik receipt has `lifecycle_verified: true`,
`catalog_acceptance: false`, and no lease reported at the client or upstream
boundary. The P2 allow run specifically exercised explicit empty-body
`Content-Length: 0` handling.

The final-source Envoy `1.39.0` H1 matrix recorded P1/P2/P3/P4
Safe, spoofed lease header, metadata omission, lease expiry, companion
unavailability, and same-service follow-up controls. Its evidence is
`structural_input_only`, not catalog acceptance. The final-current-source
runtime summary is payload-safe and retained locally with `FND-PARENT-0221`;
no raw payload, credential, lease, or decision token is included in this
record.

## Checks not run and rationale

- P4 Strict was not promoted: Envoy intentionally does not run it, and Traefik
  has no independently observed client-visible reset/abort.
- The shared Traefik `p3_redirect` vector is configured as a 403 deny, so it
  is non-passing as redirect evidence.
- The full Traefik host matrix was not repeated after the final Envoy-only
  status/terminal-normalizer patch. Its direct middleware/UDS race suite
  passed, and the earlier Traefik receipts retain their stated
  `LIFECYCLE_ONLY` scope.
- Real-host duplicate response callback, raw client cancellation, same-process
  Traefik follow-up, H2/H3, and broader cross-connector parity are not run.
- One initial timeout invocation used a runtime-root suffix that intentionally
  did not select the controlled six-second delay and therefore returned `200`;
  it is not accepted as evidence. The retained rerun with the exact controlled
  suffix returned the required `503` and terminal `timeout`.
- Hosted check `97747662107` was observed and failed with New-Code Security
  Rating C instead of required A. Exact successor-head checks, review, and
  branch protection remain pending.

## Known limitations

The Traefik case driver is an operator-trusted boundary, so its receipts are
`LIFECYCLE_ONLY`. The Envoy matrix is `structural_input_only`. Neither scope
promotes full catalog acceptance or production readiness. P4 Safe does not
provide strict client disruption.

## Remaining risks

`FND-PARENT-0221` remains a P0/high release blocker. P4 Strict, duplicate
callback, raw client cancellation, same-process Traefik follow-up, H2/H3, and
cross-connector parity require further evidence or an explicit current-user
risk decision. No such risk acceptance exists.

## Initial native-remediation diff and review status

The final local review covers the scoped source diff, paired documentation,
focused tests, current CGo build, real H1 receipts, and independent post-fix
security review. Draft PR #341 and its initial scoped commit/push are
observed; no merge was attempted. Native remediation is locally validated, but
the post-push exact-head check, hosted check, review decision, branch
protection, and green Sonar result remain pending. No Framework/MRTS change or
Gitlink update is asserted.

## Initial Post-Draft PR Sonar status

Draft PR #341 against `master` is present at commit/head
`931d6eb81207997169719bb475d50274ae281eed`; no merge was attempted. Hosted
check `97747662107` failed with New-Code Security Rating C instead of the
required A and reported ten vulnerabilities. FND-SONAR-0061 is P0/high,
`in_progress`, and release- and candidate-integration-blocking. Native local
remediation is in progress using descriptor-backed exact `0700` roots, direct
`0600` single-link leaves, a runtime-root case-input copy, and a fixed
loopback/origin-form client. No suppression, configuration change, or
quality-gate change was made. Focused native tests validate the remediation
locally; the post-push exact-head and successor hosted checks remain pending,
and no green Sonar result is claimed.

## Successor Sonar and upstream TLS follow-up

At the start of this scoped follow-up, Draft PR #341 was at
`9aeb0b551b34a0e44b9409130c2ecafeac641530`. Its exact successor Sonar
analysis `af6a96df-297f-47dd-af26-83b5315327e6` closed/fixed nine of the
original ten vulnerability records but left LOW `python:S5332` open at the
controlled upstream. This is a real clear-text hop; it is not suppressed or
reclassified.

The remediation changes only Traefik's internal controlled-upstream hop. The
runner creates a per-run `0600` certificate/key in the `0700` runtime root.
The dynamic configuration uses `https` with a certificate-verifying
`serversTransport` (`serverName` and `rootCAs`), and the controlled upstream
requires TLS 1.2 or later. There is no `insecureSkipVerify` or plaintext
fallback. The case driver remains the HTTP client of Traefik's unchanged
public listener.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_runtime_artifact_utils connectors.composite_harness.test_verify_matrix_evidence connectors.traefik.harness.test_composite_config connectors.traefik.harness.test_composite_harness_paths` passed 54 focused stdlib tests. They include verified TLS, untrusted-certificate rejection, and trusted wrong-hostname rejection against the actual controlled upstream. Source-only Python compilation, runner shell syntax, and `git diff --check` also passed. An independent scoped security review found no validated bypass. The residual same-UID path-replacement assumption is documented; cross-user access is constrained by the private runtime root.

No local `traefik` executable is available, so actual Traefik dynamic-config
parsing and a real TLS-enabled matrix run are blocked in this environment.
The next steps are the authorized scoped commit/push and exact-successor
hosted Sonar verification. The Draft PR remains `DIRTY`; no rebase,
conflict-resolution commit, or merge is authorized.
