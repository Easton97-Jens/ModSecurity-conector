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
| Delivery disposition | Historical entries below retain the former Draft-only authorization. For the pre-documentation-successor head `2a5aeb91b20ef6ec100206a9afef09cae416dbe9`, Draft PR #341 is `OPEN`/`MERGEABLE`/`CLEAN` against `master`; local and PR heads agree, all required checks and review threads are resolved, and its matching `2026-08-26T12:09:25Z` SonarQube Cloud analysis has Quality Gate `OK` with zero open/accepted issues, security hotspots, new duplication, and new-coverage counters. The current user explicitly accepts the remaining P4 Strict, duplicate/cancel, same-process Traefik follow-up, H2/H3, and cross-connector-parity evidence gaps only for PR #341 and authorizes a protected squash merge. This paired correction must be normally committed/pushed and receive a new exact-head verification round before the Draft transition or merge; no merge or `master` change has occurred. |

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
| P3 redirect follow-up | 302 | `LIFECYCLE_ONLY` P1/P2/P3, exact `Location` attestation |
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

On 2026-08-28, a fresh isolated Traefik H1 follow-up for `p3_redirect`
returned HTTP 302. Its trusted client boundary observed exactly one canonical,
bounded `Location`; the receipt keeps only
`redirect_location_verified: true`, never the target value. A fresh Envoy
`1.39.0` full H1 matrix exercised the same case, projected it through the
shared verifier as `LIFECYCLE_ONLY`, and retained the same boolean-only
attestation. Envoy's top-level matrix remains `structural_input_only`, and
neither result is catalog acceptance or production promotion.

The follow-up changes the shared verifier/docs, Envoy helper/matrix/projection,
Traefik driver/matrix, and focused Python/Go tests. The verifier now requires
the canonical P3 rule `1103002`, exactly HTTP 302, and the boolean attestation;
it also normalizes absolute projection paths before containment checks. The
latter closes the independent `FND-PARENT-0987` CWE-22 path-containment defect,
which is fixed pending exact-PR-head verification.

## Checks not run and rationale

- P4 Strict was not promoted: Envoy intentionally does not run it, and Traefik
  has no independently observed client-visible reset/abort.
- P3 redirect now has the isolated Traefik and Envoy HTTP 302 evidence above,
  but the full Traefik host matrix was not repeated after the follow-up. Those
  receipts retain their stated `LIFECYCLE_ONLY` scope.
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

`FND-PARENT-0221` remains a P0/high release blocker and is neither closed nor
downgraded. The current user explicitly accepts, only for the protected squash
merge of PR #341, the P4 Strict, duplicate/cancel, same-process Traefik
follow-up, H2/H3, and cross-connector-parity evidence gaps. That limited
delivery decision does not claim that any gap is verified, does not weaken a
control, and does not replace the remaining evidence work.

## Final diff and review status

The final local review covers the scoped source diff, paired documentation,
focused tests, current CGo build, real H1 receipts, and independent post-fix
security review. The pre-documentation-successor PR #341 head has passed its
hosted checks, branch-protection requirements, resolved-thread review, and
matching SonarQube Cloud zero-new-code analysis. The current user has
authorized a protected squash merge after the limited residual-risk acceptance,
but no merge has been attempted. This paired correction creates a new exact PR
head, so the complete GitHub, review, branch-protection, and SonarQube Cloud
cycle must be repeated before the Draft transition or merge. No Framework/MRTS
change or Gitlink update is asserted.

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

## Scanner-compatible native TLS-server successor

Exact PR head `00b767aec09ccab0a6cceba37c8dc4ae763395d5` preserved the
certificate-verifying Traefik-to-upstream TLS transport, but its hosted
SonarCloud check `97786524327` still failed: New-Code Security Rating was B
with one new LOW `python:S5332` vulnerability at the controlled upstream's
`server.serve_forever` call. The local TLS control was real, but this rule
models a call resolved to `socketserver.BaseServer.serve_forever` as a
clear-text server-start sink without propagating the wrapped socket/context
state. It is neither suppressed nor reclassified.

The scoped successor retains the TLS 1.2-or-later certificate/key pair and
uses Python 3.14's native `http.server.ThreadingHTTPSServer`, passing that
pair to the constructor and setting its socket context minimum version. Its
bounded process-owned loop sets `server.timeout = 0.2` and repeatedly invokes
`server.handle_request()`. This retains threaded TLS request handling while
removing the scanner-modelled generic `serve_forever` sink; it changes neither
Traefik's certificate verification nor the unchanged public HTTP listener.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_runtime_artifact_utils connectors.composite_harness.test_verify_matrix_evidence connectors.traefik.harness.test_composite_config connectors.traefik.harness.test_composite_harness_paths` passed 55 focused stdlib tests. The added control asserts the native TLS server and request loop, alongside verified TLS, untrusted-certificate rejection, and trusted wrong-hostname rejection against the actual controlled upstream. Source-only Python compilation, runner shell syntax, `git diff --check`, and a source scan for the generic server-start, plaintext-template, and insecure-verification patterns also passed.

No local `traefik` executable is available, so actual Traefik dynamic-config
parsing and a TLS-enabled matrix run remain `blocked_environment`. The next
steps are the authorized scoped commit/push and exact-successor hosted Sonar
verification. The Draft PR remains `DIRTY`; no rebase, conflict-resolution
commit, or merge is authorized.

## Sonar zero-new-code remediation (hosted confirmation recorded)

A separate, bounded follow-up refactors the 92 current New-Code Code Smells
and six duplicated blocks reported for this Draft PR. It changes no Sonar
configuration, quality gate, exclusion, accepted-issue state, coverage input,
or suppression. The source changes are limited to behavior-preserving helper
extraction, literal reuse, dispatcher decomposition, and focused test-fixture
reuse.

The current local source review identifies a structural remediation for every
reported issue and duplicate block. Uncached validation passed for the full
Envoy and Traefik Go suites, the relevant Envoy race suites, both Go vet
suites, 53 Python runtime/evidence/harness tests, Go formatting, shell syntax,
and diff whitespace. An independent security review also confirmed that the
temporary descriptor-cleanup and UDS outcome-routing regressions found during
this follow-up are fixed and that fail-closed controls remain intact.

SonarCloud analysis at `2026-08-25T16:32:43Z` for source head
`6af90bc98f90452faae1e7179ade38a2a41561b0` recorded Quality Gate OK, 0 open
New Issues, 0 Accepted Issues, 0 Hotspots, 0 duplicated new blocks/lines/
density, and `new_lines_to_cover=0` / `new_uncovered_lines=0`. The coverage UI
still displays 0.0%; this is reported as observed UI state, not as a coverage
claim beyond those zero new-line counters. Five GitHub workflows passed. The
PR remains Draft/Open and no merge was attempted or authorized. Final
verification of this documentation follow-up against its future documentation
head is still pending.

## PR #341 Codex-feedback remediation — 2026-08-26

The registered task worktree for `agent/fnd-parent-0221-composite-connectors`
was advanced normally to include `origin/master` at
`c1653fb84201bc6a29c47723fa74e12270deb164`; `master` was not changed. Seven
current Codex review threads were repaired without changing a quality gate,
suppression, CI configuration, or security control:

- root-owned non-writable path ancestors are accepted while writable ancestors
  remain rejected except for root-owned sticky `/tmp` and `/var/tmp`;
- a pre-activation claim leaves the owning UDS cleanup to retain `disconnect`
  rather than race an `out_of_order` terminal;
- ForwardAuth accepts one bounded comma-containing URI and rejects control or
  over-limit data;
- empty ordinary header values are consistently serialized and parsed while
  method, URI, header name, and Host remain non-empty;
- downstream errors and short writes stop false P3/P4 EOS/outcome evidence;
- a coordinator fault is queried after close and takes shutdown-result
  precedence; and
- the composite response writer no longer exposes `Hijack` or `Unwrap`, so
  unsupported HTTP upgrade takeover fails closed rather than bypassing P3/P4.

The final local checks passed: Envoy coordinator/ForwardAuth/UDS/command race
tests, Traefik middleware race tests, both affected Go-vet suites, 39 focused
Python verifier/configuration/harness tests, Traefik runner shell syntax, and
`git diff --check`. The independent 33-file security-diff review found no new
open security candidate; it records the pre-fix raw-writer escape as a
remediated instance of `FND-PARENT-0221` and retains the separate P4 Strict
harness observation as a suppressed, non-promoting evidence-integrity note.

These are local final-worktree results only. The corrective commit, push, and
new exact-head GitHub/SonarCloud checks remain to be performed; no future
Sonar result is claimed here, and no merge is authorized.

## PR #341 Sonar cognitive-complexity successor — 2026-08-26

At exact Draft PR #341 head `19c441c28ffb431167b62b1a75df9ac0ec929180`, the
raw SonarQube Cloud pull-request API reported one task-owned New-Code issue:
`AaA9jhYnEWWk2M7bnB7N` (`go:S3776`) in `Coordinator.Claim`, cognitive
complexity `17` where `15` is allowed. This is remediated structurally, not by
changing Sonar configuration, Quality Gate, coverage input, exclusions,
accepted-issue state, false-positive state, or a suppression.

The nested non-reserved out-of-order cleanup was extracted into
`finishOutOfOrderClaim`. The helper preserves the existing asynchronous
`out_of_order` terminal path. Reserved pre-activation claims still leave their
terminal reason to the owning UDS session, so a disconnect remains truthful.
`TestPreActivationClaimLeavesTerminalReasonToOwner` and the new
`TestFinishOutOfOrderClaimClosesUnreservedEntry` cover those respective
controls.

`go test -race -count=1 ./internal/composite ./internal/compositetraefik
./cmd/msconnector-composite`, `go vet ./internal/composite
./internal/compositetraefik ./cmd/msconnector-composite`, `gofmt -d`, and
`git diff --check` passed in the corrective worktree. A focused independent
security review found no new candidate and confirmed that locking,
single-close cleanup, capacity release, and terminal-event behavior are
unchanged. Commit, normal push, and exact-successor Sonar evidence remain
pending; no merge is authorized.

## Current Codex-thread successor (local validation)

After a fresh fetch, `origin/master` remains
`c1653fb84201bc6a29c47723fa74e12270deb164` and is already an ancestor of the
registered task branch. The worktree is therefore current without a merge,
rebase, or any change to `master`.

This scoped successor repairs the remaining current Codex feedback without
altering a Quality Gate, suppression, coverage input, CI configuration, or
security control:

- response-header end-of-stream now emits P4 evidence, response processing
  errors after P3 are terminal transport errors rather than a second Immediate
  Response, and request/response body chunk budgets are independent;
- the version-2 private Traefik reservation snapshot binds the protected
  request's HTTP protocol, listener IP address, and listener port. The outer
  middleware obtains these only from the protected request, the UDS parser and
  coordinator validate them fail-closed, and activation restores them instead
  of using the ForwardAuth loopback listener. No request-context header or
  HTTP capsule was added; and
- the private result protocol now distinguishes a successful post-commit P4
  Safe decision from an inspection processing/limit failure. The former carries
  a bounded opcode-specific log-only flag, preserves already committed bytes,
  and requires a truthful log-only outcome. The latter remains a terminal
  reject and is stopped before the downstream response writer.

The local regression set passed: Envoy `go test -race -count=1
./internal/composite ./internal/compositeenvoy ./internal/compositetraefik
./cmd/msconnector-composite`; Traefik `go test -race -count=1 .`; both scoped
Go-vet suites; `gofmt -d`; and `git diff --check`. The Traefik tests use a
short task-owned temporary root because Unix-domain socket paths are bounded;
the initially longer cache path produced only a local `bind: invalid argument`
test-environment failure and was not a product result.

An independent post-patch security review found no new validated exploitable
or functional finding in these boundaries. It confirmed that no header/capsule
bypass was introduced and that only successful Safe decisions use the
post-commit flag. Its residual evidence gap is the separately required runtime
host matrix; IPv6 link-local listener addresses with a zone are deliberately
fail-closed by the literal-IP validation and merit explicit future runtime
coverage.

These are local results for the uncommitted successor only. The remaining
steps are a normal scoped commit and push, exact-head GitHub/SonarCloud checks,
and then factual review-thread reconciliation. The PR remains Draft and no
merge is authorized.

## PR #341 Sonar-zero remediation (local validation) — 2026-08-26

At published Draft PR #341 head `7a1473c17ac3343e4b4ac4944d8a7cea5da816dc`,
the raw SonarQube Cloud pull-request API reported five task-owned New-Code code
smells: parser complexity in `parseReservationSnapshot`, P4 Safe test
complexity, eight `reservationPayloadWithMetadata` parameters, response-writer
finish complexity, and reservation-payload test parser complexity. This local
successor addresses each structurally without changing Sonar configuration,
Quality Gate, exclusions, accepted-issue state, suppression, coverage input,
CI configuration, or a security control.

`parseReservationMetadata` now preserves the exact bounded private-frame
validation order before existing header-group parsing. The P4 Safe test splits
lifecycle exercise from event assertions. `reservationTransportMetadata`
groups the protected listener facts, while `finishTransport` and
`finishResponse` retain the previous fail-closed terminal ordering. The
test-only reservation parser now uses a bounded cursor. These decompositions
do not alter the version-2 snapshot wire layout, HMAC-bound protocol/IP/port
metadata, result-flag restriction, or post-commit reject behavior.

The integrated local regression set passed: Envoy `go test -race -count=1
./internal/composite ./internal/compositeenvoy ./internal/compositetraefik
./cmd/msconnector-composite`; Traefik `go test -race -count=1 .`; both
corresponding Go-vet suites; `gofmt -d`; and `git diff --check`. A fresh
read-only security review found no new validated security or functional
finding and confirmed that malformed private input remains fail-closed and
that response EOS/error paths retain their original safeguards.

This section records local pre-delivery evidence. The following delivery
operation must perform the authorized scoped commit and normal push; matching-
head GitHub CI, matching-head Sonar zero evidence, and review-thread
reconciliation remain required afterward. The PR remains Draft and no merge
is authorized.

## PR #341 Sonar duplication successor (local validation) — 2026-08-26

The exact `cdc4d9c7c60a25a9f38e02089f2a7f16d7b433c1` SonarQube Cloud analysis
cleared all five New-Code code smells and all open issues, but still reported
`new_duplicated_lines=22` and `new_duplicated_lines_density=0.1653140967838894`.
The exact duplication API evidence locates both 11-line blocks only in
`uds_test.go`; no production file has a new duplicated line. This remains a
strict zero-acceptance blocker even though the Quality Gate is OK.

`startP4Test` now owns the common test-only coordinator/UDS reservation and
ForwardAuth setup. The P4 Safe test still asserts the explicit log-only flag
and allow result, while the P4 processing-error test still asserts terminal
reject without that flag. No production code, Sonar configuration, Quality
Gate, exclusion, suppression, accepted-issue state, coverage input, or
security control changed.

The full focused regression set passed after the test-only refactoring: Envoy
`go test -race -count=1 ./internal/composite ./internal/compositeenvoy
./internal/compositetraefik ./cmd/msconnector-composite`; Traefik `go test
-race -count=1 .`; both corresponding Go-vet suites; `gofmt -d`; and `git
diff --check`. The following delivery operation must push the scoped successor
and rebind GitHub/Sonar evidence to its exact head before review-thread
reconciliation. The PR remains Draft and no merge is authorized.
