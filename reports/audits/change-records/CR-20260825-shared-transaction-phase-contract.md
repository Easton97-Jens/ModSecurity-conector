# Change Record CR-20260825: shared transaction-phase contract

**Language:** English | [Deutsch](CR-20260825-shared-transaction-phase-contract.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260825-shared-transaction-phase-contract` |
| Date (UTC) | `2026-08-25` |
| Base revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Reconciled delivery base | `5d71be74369123257851eb5ec612d7523a6b061d` (`origin/master` before the first task-branch push) |
| PR #344 remediation base | `c1653fb84201bc6a29c47723fa74e12270deb164` (`origin/master` normally merged locally as `b1b6e72294a654c96dc44c9db69d25a704084c8f`; delivery remains pending) |
| Scope | Parent repository only: the shared P1--P4 transaction contract, ten connector mappings, bounded response companions, Stock-lighttpd sidecar, tests, English/German documentation, and this paired Change Record. The original 2026-08-25 contract slice made no Framework, MRTS, Gitlink, workflow, ruleset, branch-protection, or required-check change. Later separately authorized PR #344 HAProxy evidence remediation changed limited workflow and CI-helper material; it did not change Framework, MRTS, Gitlinks, rulesets, branch protection, or required checks. |

## Motivation and problem statement

The connector implementations previously exposed different lifecycle and
decision shapes. This change makes their business meaning common: P1 is
request headers before request commitment, P2 is the bounded request body with
one end-of-stream, P3 is response headers before response commitment, and P4
is the bounded response body with one end-of-stream. The meanings are derived
from the existing Common, adapter, test, and documentation boundaries; no new
phase meaning is introduced.

## Acceptance criteria

- Bind Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy
  ext_proc, Traefik forwardAuth, Traefik Native UDS, lighttpd Stock, and
  lighttpd Patched to the same bounded transaction/decision contract or a
  documented minimal host translation.
- Reject duplicate, skipped, late, post-terminal, cancel, timeout, and
  premature-cleanup phase transitions deterministically.
- Preserve bounded headers, request/response bodies, events, opaque
  correlation, private defaults, metadata-only JSONL, and no silent
  version/capability fallback.
- Keep response-capable companions for Envoy ext_authz and Traefik forwardAuth
  rather than treating P3/P4 as not applicable.
- Add focused valid/invalid order, limit, timeout, cancel, cleanup, concurrent
  transaction, and connection/stream-reuse coverage.
- Create only a truthful Draft PR; no merge or `verified_pr` claim is made.

## Implementation decision and rationale

- `transaction_contract.h` and the Common Runtime own canonical transaction
  identity, connector/host metadata, phase state, bounded request/response
  metadata, decisions, rule correlation, mode, error class, timestamps, and
  cleanup state. They also own the explicit finite-state transition checks and
  normalized host-action records.
- Direct adapters use that contract at their native P1--P4 hooks. HAProxy
  SPOE/SPOP uses an owner-queue/MRC1 response path; Envoy ext_authz and Traefik
  forwardAuth hand the same transaction to a single-claim opaque-handle,
  private-UDS response observer. The handle has fixed capacity and an absolute
  TTL; it is not a client transaction identifier.
- The canonical Stock-lighttpd solution is a literal-`127.0.0.1` HTTP/1.1
  traffic-owning sidecar with direct P1--P4. The native `stock-lighttpd` path
  remains an exact noncanonical P1/P3 compatibility translation and never
  silently falls back to the sidecar.
- Failure decisions remain typed and preserve the original rule correlation.
  Body limits emit a bounded terminal event without body payload. No connector
  negotiates an older MRC1 version or invents capability fallback.

## Compatibility impact

Connector protocol and host mechanics remain adapter-specific, but decision
meaning, failure classification, cleanup, and limits are shared. Deployments
using the Stock solution must use the documented private literal-loopback
sidecar and explicit external build root. Envoy ext_authz and Traefik
forwardAuth require their paired private response observer for P3/P4.

## Security impact

The change touches untrusted HTTP framing, bounded body processing, UDS
correlation, state ownership, and failure handling. It preserves fail-closed
Strict pre-commit behavior, bounded event serialization with no body payload,
opaque single-claim correlation, private listener binding, explicit phase
validation, and deterministic destruction.

`FND-PARENT-0949` is fixed locally and its direct component regressions pass,
but requires exact-delivered-revision and real Stock-backend evidence before it
can be verified. `FND-PARENT-0221` remains P0/high,
`in_progress`/`blocked_missing_evidence`; P4 Strict real-host proof and other
named host evidence are not promoted. `FND-PARENT-0947` records the
out-of-scope CI capability conflict: its collector expects Traefik forwardAuth
P2 to be `not_implemented`, while the product manifest truthfully says
`configured_not_exercised`. The original contract slice changed no CI file and
claims no risk acceptance; later separately authorized HAProxy evidence work is
recorded in its own addenda.

## Changed files

- Common contract and runtime: `common/include/msconnector/transaction_contract.h`,
  `common/src/transaction_state.c`, `common/runtime/msconnector_runtime.*`,
  `common/runtime/response_companion_{transport,client}.*`, decision/error/event
  interfaces, and the English/German contract and design documentation.
- Adapters: Apache, NGINX, HAProxy HTX/SPOE-SPOP, Envoy ext_authz/ext_proc,
  Traefik forwardAuth/Native UDS, lighttpd Stock/Patched sources, manifests,
  harnesses, and English/German connector documents.
- New focused tests: Common C contract/runtime/transport/client tests; HAProxy
  binding/overlay/harness tests; Envoy and Traefik observer tests; Stock
  sidecar and lighttpd gate tests; Apache/NGINX/Traefik contract tests.
- Traceability: this English/German record and the paired archive-index entries.

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| Focused Apache/NGINX/lighttpd/Traefik `python3 -m unittest` suite | Passed: 92 tests, 4 expected skips. |
| Stock-sidecar strict C17 build plus direct loopback `python3 connectors/lighttpd/tests/test_stock_sidecar_contract.py` | Passed: 11 tests in 20.514 seconds for the final prebuilt sidecar artifact. |
| `transaction_phase_contract_test` with `-std=c17 -Wall -Wextra -Werror` | Passed. |
| `transaction_phase_runtime_companion_test`, `response_companion_transport_test`, and `response_companion_client_test` with the same strict C17 mode | Passed. |
| `make -C connectors/haproxy check-htx-overlay` | Passed: 28 source checks. |
| HAProxy binding/overlay/combined-harness `python3 -m unittest` suite | Passed: 12 tests. |
| `go test -buildvcs=false -count=1 ./...` in Envoy ext_proc, Traefik response observer, and Traefik Native UDS middleware | Passed. |
| `python3 -m unittest tests.test_bilingual_docs` | Passed: 22 tests. |
| `git diff --check` and the scoped `.github`/`ci` diff check | Passed for the original contract slice; no CI/governance file was in that slice. Later separately authorized PR #344 HAProxy evidence work changed limited workflow/CI-helper material without changing governance controls. |
| `make check-bilingual-docs` and `make check-doc-links` | Failed only because unrelated documents refer to unavailable `modules/ModSecurity-test-Framework` paths in this task worktree. The task-owned English/German pair-and-switch check passed; no link or CI workaround was added. |
| Combined capability/documentation/adapter `python3 -m unittest` suite | Failed as expected at 95 tests/one error: unchanged CI collector contradicts the truthful Traefik forwardAuth P2 manifest; retained as `FND-PARENT-0947`, not suppressed. |

## Runtime evidence

The Stock sidecar test is a real private-loopback component exchange through
the Common Runtime. It covers P1--P4 Allow/Block, limits, unsafe framing,
no-body responses, timeout, cancel, cleanup, capacity, connection reuse,
non-reading workers, and terminal delivery/reset correlation. It is not a run
through an unmodified Stock-lighttpd backend topology.

The Envoy and Traefik tests are source/component evidence for the observers
and their private transport. This record does not promote unrun host, H2, H3,
or client-visible late-action claims.

## Checks not run and rationale

- No unmodified real Stock-lighttpd backend topology, full native host matrix,
  H2, or H3 run was available in this task; component evidence is recorded at
  its actual scope.
- The original contract slice made no CI workflow, ruleset, required-check, or
  CI collector modification because the user explicitly excluded CI from that
  implementation scope. Later separately authorized HAProxy evidence work is
  recorded in its own addenda and did not change governance controls.
- The repository-wide documentation make targets were executed and failed only
  for unavailable Framework/MRTS link targets outside this task's changed
  files. The focused bilingual document test passed, and the task did not
  alter external links merely to force a green result.
- Hosted PR checks, SonarCloud, review, and merge evidence do not exist at the
  time this record is committed. They must be tied to the exact Draft-PR head.

## Known limitations

The task commit was reconciled to `origin/master`
(`5d71be74369123257851eb5ec612d7523a6b061d`) before its first push. An
existing Draft PR #341 covers related Envoy/Traefik composite response work; it
is not modified here and its relationship must remain visible during review.

## Remaining risks

Real-host coverage gaps and the listed findings prevent a `verified_pr` claim.
Host-specific late-action behavior remains reported as a bounded adapter
translation, not silently promoted to an enforceable action.

## Final diff and review status

The current user explicitly requested a PR. This paired record is therefore
authorized as the required traceability for one Parent Draft PR. It does not
authorize a merge, direct `master` push, CI-scope expansion, Framework/MRTS
change, Gitlink update, check bypass, or risk acceptance.

## Delivery status

Reconciled task-owned commit prepared for one Draft PR against `master`. At the
time of writing, no remote branch SHA, PR number, hosted check result, or merge
result is claimed.

## 2026-08-26 PR #344 remediation addendum

The user requested that the existing Draft PR #344 be brought onto the current
`master` and that task-owned SonarQube Cloud/Codex causes be repaired without
weakening workflows or quality controls. The isolated follow-up branch normally
merged the fetched `origin/master` revision
`c1653fb84201bc6a29c47723fa74e12270deb164` as
`b1b6e72294a654c96dc44c9db69d25a704084c8f`; it has not been rebased,
force-pushed, or merged to `master`.

The remediation keeps the shared profile registry connector-owned, removes
broad compatibility macros, closes Apache's profile-registry C17/APXS build
path, and keeps the existing contract checks semantic after helper extraction:
the Apache cleanup harness links the real transaction-state implementation and
the HAProxy HTX check follows payload callbacks through the borrowed-slice
append helpers. No `.github/workflows` file, ruleset, branch rule, required
check, Sonar suppression, or quality threshold changed.

| Continuation check | Actual local result |
| --- | --- |
| `make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-http-authorization-service-timeout` | Passed. |
| Focused connector adoption/wiring checks for HAProxy, Envoy, Traefik, lighttpd, NGINX, and Apache; plus `make check-haproxy-htx-overlay` | Passed. |
| Apache request-transaction cleanup Python/real-APR harness and Apache C17 compile with a task-owned output root | Passed. |
| Direct C17 binaries for `transaction_phase_contract_test`, `transaction_phase_runtime_companion_test`, `response_companion_client_test`, and `response_companion_transport_test` with their real Common source closures | Passed. |
| Focused HAProxy/Sonar/workflow Python suite | Passed: 54 tests. |
| `go test ./...` in Envoy ext_proc and Traefik response observer, using a registered task-owned Go build cache | Passed. |
| `git diff --check` | Passed. |
| HAProxy C17 native-header target | Blocked before compilation by the Framework-owned `nginx_pinned_provenance_ref_mismatch`; no bypass or Framework change was made. |

Exact delivered-head SonarQube Cloud and hosted workflow evidence remains
pending. This addendum therefore does not claim a zero issue count, a passing
Quality Gate, a ready-for-review state, or a merge until those exact-head
results are observed.

## 2026-08-26 progressive P4 completion addendum

The follow-up corrects a streaming lifecycle defect discovered while validating
the response path: repeated bounded request- or response-body chunks must
resume their already-active P2/P4 phase; only the explicit final EOS may
complete it. The Common Runtime now enforces that rule. Apache's output filter
forwards each normalized pre-EOS brigade fragment immediately, preserves FLUSH
and metadata buckets, retains no full response brigade, and commits the
canonical response state at the first forwarded body or FLUSH boundary, or on
terminal empty EOS. The Stock-lighttpd sidecar now sends fixed 2-KiB response chunks through
the Common Runtime and to the client immediately, with one final P4 EOS.

The English/German common contract, Apache and Stock-lighttpd guides,
capabilities, and matrix now describe the same semantics. The matrix retains
all ten logical connector solutions: raw response-blind protocol paths are
explicitly unsupported, while their documented bounded companions provide the
required P3/P4 mapping. No workflow, ruleset, required check, scanner
configuration, suppression, allow-list, or quality threshold changed.

| Follow-up check | Actual local result |
| --- | --- |
| `make check-common-helpers-c17` | Passed. |
| `python3 -B -m unittest -v tests.test_apache_phase4_response_regression_wiring tests.test_nginx_phase4_runner_wiring tests.test_bilingual_docs` | Passed: 39 tests, 3 expected Framework-gitlink skips. |
| Stock-sidecar contract test with GCC and then with `CC=clang` | Passed: 11 tests in each run. |
| `CC=clang MSCONNECTOR_C_STD=c17 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror' make check-common-helpers` | Passed. |
| `make check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity` with a task-owned build root | Passed. |
| Apache strict-C17 check with Clang and a task-owned output root | Passed. |
| Focused Codex Security diff scan of the local P4 patch | Completed with zero reportable findings; retained report: `/var/tmp/codex/ModSecurity-conector/pr344-quality-gate-remediation-20260826/security-diff-p4-final-20260826/report.md`. |

The Apache result is source, wiring, and strict-C17 compilation evidence; an
actual Apache traffic run remains unavailable in this environment. NGINX and
Patched-lighttpd retain their documented host-specific runtime-evidence gaps.
At this point no claim is made about SonarQube Cloud or GitHub Actions for a
new delivered head: those results must be observed after the normal
current-`origin/master` reconciliation and push.

### Follow-up validation boundaries

`make check-apache-request-transaction-cleanup` passed its 11 Python tests and
real APR lifecycle harness, and `make check-adapter-contracts` passed. The
repository documentation make targets again stopped only at unchanged missing
Framework/MRTS link targets. `make check-apache-common-adoption` failed one
static assertion that still requires the superseded `ap_save_brigade()`
full-response-through-EOS design. Satisfying it by restoring that buffering
would violate this record's progressive P4 contract; no CI check, workflow, or
suppression was changed. The conflict is retained as
`FND-PARENT-0958` and blocks a clean Apache structure-workflow claim pending a
separately authorized, non-weakening control update.

### Partial response-header ownership correction

The final source review identified a separate Stock-lighttpd sidecar protocol
integrity defect: a downstream nonblocking response-header write could emit
some bytes, fail, and still let generic error handling attempt a second
fallback response. The writer now cumulatively observes status-line, field,
and terminator bytes. Any nonzero observed result claims client-response
ownership, suppressing a second HTTP response; the Common Runtime response
commit remains intentionally after a complete header block.

`FND-PARENT-0959` is fixed locally, pending verification on the exact delivered
PR head. The Stock-sidecar component suite, including a constrained 64-KiB
partial-header socketpair regression, passed 12 tests with GCC and again with
Clang. An independent bypass review found no remaining direct second-response
path. This is component and source-path evidence: no external Stock-lighttpd
host capture of the close-after-partial-header path was available. No workflow,
quality-gate, scanner, or suppression setting changed.

## 2026-08-26 Codex finding-remediation addendum

Four current product findings were remediated without changing any workflow,
quality gate, scanner configuration, suppression, ruleset, branch rule, or
required check.

- Apache records the Common-bounded rule ID and terminal canonical decision for a
  disruptive P3 response-header intervention before the native Apache sink.
  Redirect, rate-limit, and block outcomes map to their shared decision kinds;
  an uncorrelatable intervention fails closed before response commitment.
- The Stock-lighttpd sidecar applies its response-body limit only when a body
  is semantically present, recognizes only the exact `HEAD` method as
  bodyless, and returns 417 for every unsupported `Expect` field before body
  reads or upstream release.
- Patched lighttpd marks both declared-length and streaming body-limit P2
  rejections as host-rejected, which selects the intended incomplete-body
  cleanup instead of synthesizing an invalid P3 transition.

| Local check | Actual result |
| --- | --- |
| Direct C17 `transaction_phase_contract_test` binary, including the maximum Common rule-ID length | Passed. |
| Focused Apache/Patched-lighttpd Python suite | Passed: 28 tests. |
| `make check-apache-intervention-cleanup` and Apache C17 compile | Passed: 7 tests and strict C17 compilation. |
| Stock-sidecar loopback contract with GCC and Clang | Passed: 13 tests in each run. |
| Common helper C17, Common security/flow integrity, adapter contracts, and lighttpd Common adoption | Passed. |
| `git diff --check` | Passed. |

These are local source, component, and compilation results only. Exact-head
SonarQube Cloud and hosted-workflow results must be observed after the normal
current-`origin/master` merge and normal PR-branch push.

Two independent read-only post-patch reviews found no concrete reachable
security bypass. One review identified that initial Apache local rule-ID
buffers were smaller than the Common maximum; both were aligned to
`MSCONNECTOR_MAX_RULE_ID_LENGTH`, and the strict C17 and maximum-length
contract checks were repeated successfully.

## 2026-08-27 Codex thread-remediation addendum

Five open Codex review threads at PR #344 head
`053ed5c827d28cd06fcb82709496b45baebf0a6e` were revalidated as
task-owned bounded-protocol or lifecycle defects and remediated without any
workflow, scanner, Quality-Gate, ruleset, branch-rule, required-check, or
suppression change. The current fetched `origin/master` remains
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`; the branch is `0 behind / 14
ahead`, so no rebase or history rewrite is required.

- Canonical request/response `Content-Type` metadata now has the accepted
  Common header-value bound plus its required terminator.
- One absolute deadline now covers the complete MRC1 request frame and result
  exchange, rather than granting one timeout to each half.
- The Stock-lighttpd sidecar permits valid 304 representation-length metadata,
  preserves a request target up to the canonical URI bound, and rejects a
  truncated upstream request line before I/O.
- NGINX records the correlated canonical BLOCK, REDIRECT, or RATE_LIMIT
  decision before its native redirect/status sink; an invalid decision fails
  closed.

| Follow-up check | Actual local result |
| --- | --- |
| Direct C17 `transaction_phase_contract_test` and `response_companion_client_test` | Passed, including maximum content-type metadata and combined MRC1 deadline regressions. |
| `python3 -B -m unittest -v tests.test_nginx_upstream_security_contract` | Passed: 12 tests. |
| `python3 -B -m unittest -v connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest` | Passed: 4 source-contract tests. |
| Stock-sidecar strict C17 syntax, Common security/flow/adapter/memory/header-fuzz checks, and NGINX adoption/wiring checks | Passed. |
| Native NGINX C17 and dynamic Stock-sidecar/HAProxy component runs | Blocked by unavailable NGINX headers/source and the available libModSecurity artifact's unresolved `libxml2.so.2` dependency; neither is reported as a pass. |

An independent postpatch security review found no validated reportable finding
in the five corrections. Delivery remains pending: the follow-up commit must
be pushed normally, then PR-head equality, Codex threads, SonarQube Cloud, and
hosted workflows must be evaluated for that exact new head.

## 2026-08-27 P4 limit and Sonar remediation addendum

The working-tree follow-up refactors the two existing SonarQube Cloud
new-code locations without a suppression, exclusion, Quality-Gate change, or
workflow change. The Envoy response observer separates terminal and streamed
response-body handling while retaining complete-callback aggregate validation
before bounded MRC1 chunk emission. The NGINX P4 filter separates preparation,
per-buffer inspection, prefix forwarding, and terminal handling; its local
body-limit path now calls the Common `REJECT` planner before any native
forwarding. Thus a current over-limit memory, file, or mixed buffer fails
closed instead of forwarding an uninspected suffix.

Apache examples, source comments, the generated configuration reference, and
the shared English/German contract consistently describe progressive pre-EOS
P4 forwarding. No `.github/workflows` file, branch rule, ruleset, required
check, scanner configuration, or quality threshold changed.

| Follow-up check | Actual local result |
| --- | --- |
| `go test ./... -count=1` in `connectors/envoy/ext_proc` | Passed. |
| `go test -race ./internal/responseobserver -count=1` | Passed. |
| Focused NGINX phase/runtime Python suite | Passed: 29 tests, 3 explicit Framework-gitlink skips. |
| Focused Apache/example Python suite | Passed: 25 tests. |
| `make check-connector-config-reference` and `make check-common-helpers` | Passed. |
| `git diff --check` | Passed. |
| `make check-nginx-c17-lint` | Blocked/skipped before compilation because compatible NGINX headers/source are unavailable. |

The sealed scoped security artifact
`security-scan-20260827T043109Z-nginx-file-buffer` records zero reportable
findings for this working-tree review and explicitly defers native NGINX
filter-chain execution for file, mixed-buffer, downstream-forwarding, and
connection-reuse cases. It is not a native-host pass.

The fetched `origin/master` is
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`; before the follow-up commit the
task branch is zero commits behind it. Normal PR push and exact-head hosted
workflow/SonarQube Cloud observation remain pending. The local Sonar client
is absent and its integration workflow requires explicit approval before any
tool installation or configuration, so this addendum does not claim a hosted
zero issue count or a passing Quality Gate.

## 2026-08-28 Stock/Common validation and delivery-status addendum

The Stock-lighttpd sidecar and Common transaction-integrity changes were
revalidated as one bounded logical slice. The real Stock-lighttpd backend run
covered seven H1 cases: allow with body, allow without body, P1 deny, P2 deny,
P2 body-limit rejection, P3 deny, and P4 Safe rate-limit. Every case produced
the canonical P1--P4 evidence where applicable, bounded events without body
payloads or opaque handles, and deterministic cleanup. P4 Strict remains
unclaimed because no valid client-abort proof is available.

The Common integrity-event chain now authenticates decision metadata,
requested and actual actions, HTTP reason/default values, and
redaction/truncation flags. The Stock verifier rejects malformed, duplicated,
reordered, or uncorrelatable engine/host decisions and validates the exact
bounded event schema. Resolver artifacts are rehashed immediately before
process start and published atomically with restrictive permissions.

| Follow-up check | Actual result |
| --- | --- |
| Stock-sidecar contract suite with task-owned `MODSECURITY_INCLUDE_DIR` and `MODSECURITY_LIB_DIR` | Passed: 31 tests. |
| Real Stock-lighttpd backend H1 run | Passed: 7 cases. |

No workflow, scanner configuration, suppression, Quality Gate, ruleset,
required check, or branch rule was changed.

At the previously delivered PR head
`7223b13650a5e999c062adb5993766b33b060eea`, `origin/master` was
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`; the branch was 18 commits ahead
and 0 behind. SonarCloud reported success with zero new issues, zero accepted
issues, zero security hotspots, and zero Sonar annotations. The Apache and
HAProxy hosted runtime jobs still failed, and the pull-request-range Gitleaks
check still reported one historical finding. These hosted results must be
re-evaluated after the next pushed head.

NGINX remains blocked by the required worker-isolation `chown` operation in
this environment. Patched lighttpd remains unpromoted because its exact
Framework gitlink and non-root runtime prerequisites are unavailable. Strict
P4 evidence remains unclaimed for connectors without a verified client-abort
capture.

## 2026-08-28 Apache/HAProxy hosted-build remediation addendum

The Parent-owned build closure separates a missing connector profile-registry
header from an actual missing libModSecurity linker dependency. The generated
Apache APXS build now receives the explicit Parent-root include path needed by
`connectors/profile_registry.h`; the strict Apache source check uses that same
repository-root include path. Apache source-archive extraction uses
`--no-same-owner`, so a task-owned id-mapped or user-namespace build root does
not fail while restoring irrelevant archive ownership metadata.

The disposable HAProxy HTX overlay now stages the connector-owned profile
registry C source and header, adds only its generated-worktree include path,
links its object explicitly, records its hashes, and keeps Framework build
logs under the task-owned HAProxy runtime root. The exact overlay patch and
Parent caller retain the existing source-tree/output-root checks. This is a
build/provenance repair only; it does not promote HAProxy runtime evidence.

| Follow-up check | Actual result |
| --- | --- |
| Focused runtime-component and HAProxy-overlay suite | Passed: 55 tests, with 5 expected Framework-HEAD skips. |
| `make check-haproxy-htx-overlay` | Passed. |
| `APACHE_C_STANDARDS_OUT=<task-owned> make check-apache-c17` | Passed. |
| Default `make check-apache-c17` output root | Blocked by a read-only default output root; the task-owned output-root rerun above passed. |

No workflow, scanner configuration, suppression, Quality Gate, ruleset,
required check, or branch rule was changed. The exact-head Apache and HAProxy
hosted runtime checks remain pending after the next normal PR-head delivery;
their historical failures and the historical Gitleaks finding are not claimed
as repaired by this local evidence alone.

## 2026-08-28 clean-history and exact-head validation addendum

The PR product tree was rebuilt from `origin/master`
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` as local replacement commit
`47eefcd3432608361d093919ae117049034b86ea`. Before this evidence addendum,
that replacement tree was byte-for-byte equal to the previous PR product tree
at `66155ac03681214c59bc9fc661145227980be130`. The previous head is retained
locally under a dedicated backup reference. The historical redacted Gitleaks
match is not in the replacement ancestry; the scan is not bypassed or
suppressed.

The project-pinned Gitleaks binary completed a redacted scan of
`origin/master..47eefcd3432608361d093919ae117049034b86ea` with no findings.
The scanner workflow and all workflow, scanner, Quality Gate, ruleset,
required-check, and branch-rule files remain byte-identical to the prior PR
tree. A final redacted scan and an exact `--force-with-lease` delivery are
still required after this documentation commit; hosted checks and SonarCloud
must then be observed for the new remote head.

| Local validation | Actual result |
| --- | --- |
| Common SDK/security/flow and adapter-contract checks; Common C17 helper; HAProxy HTX overlay | Passed. |
| C transaction FSM, runtime companion, response-companion client, HAProxy SPOE response-companion backend, and UDS transport tests | Passed. |
| Focused Common/Apache/NGINX/Envoy/Traefik/lighttpd Python contract tests | Passed: 115 tests; 3 Framework-gitlink-mismatch skips. |
| Sonar wrapper authentication | Connected through `/usr/local/bin/sonar-with-env`; no credential values were read or persisted. |

The UDS transport test uses a private short task path because Unix-domain
socket path length is bounded. The sandbox default `/tmp` is read-only and a
long evidence root exceeds `sun_path`; the short-path rerun passed and leaves
no product defect claim. The Framework checkout is uninitialized and required
host binaries are unavailable, so real host/client H1 evidence—including the
aggregate-only hosted HAProxy runtime failure—and Patched-lighttpd evidence
remain unverified. These gaps are non-passing entries, not compatibility or
Safe-mode fallbacks. The PR remains Draft until exact-head hosted and host
runtime evidence meets the stated acceptance criteria.

## 2026-08-28 final review-thread remediation addendum

### Motivation and acceptance criteria

At the then-current Draft PR #344 head
`efcaa86d5afd225aa7402cec424b3c7e785b212d`, six unresolved final-head review
threads identified boundedness, lifecycle, and protocol defects in the Envoy,
Stock-lighttpd, and HAProxy response-companion paths. The local acceptance
criteria are that a valid one-MiB Envoy response callback remains within a
finite receive bound, projection rollback cannot remove a same-UID pathname
replacement, Stock lighttpd forwards bounded non-upgrade informational
responses while only the final response reaches P3, and queued HAProxy owner
work never retains callback-owned decision text after the callback returns.
Common/MRC1 header bounds must remain exact, including C-string terminators.

### Technical decisions and changed components

- Envoy ext_proc now admits a one-MiB response body plus 64-KiB bounded gRPC
  framing headroom (`1114112` bytes) and retains the 64-KiB send limit. A
  bufconn regression sends the complete bounded body through the actual gRPC
  server.
- The Envoy composite verifier uses anonymous `O_TMPFILE` staging and retains
  any already-published owner-private fixed-name projection artifact after a
  later failure. It no longer attempts a non-atomic stat-then-unlink rollback
  of a pathname that a same-UID actor could replace.
- The Stock-lighttpd sidecar recognizes the HTTP header terminator
  incrementally in bounded chunks, avoiding repeated full-buffer scans. It
  forwards bounded non-upgrade `1xx` responses, invokes P3 once for the final
  response only, and continues to reject `101` upgrades. The Stock-lighttpd
  English/German README pair now states that visible protocol rule.
- HAProxy response-companion callbacks receive bounded session storage for
  decision text. A delayed owner task and its copied result each use separate
  bounded storage; callback storage is populated only after successful owner
  completion. The bridge accepts the existing Common/MRC1 header-name and
  header-value maxima together with their C-string terminators while retaining
  aggregate and count limits.

The affected files are the Common response-companion transport declaration and
test, the Envoy observer/projection and tests, the Stock-lighttpd sidecar and
test, and the HAProxy diagnostic bridge, backend, backend tests, and delayed
owner lifetime regression. No workflow, scanner configuration, suppression,
Quality Gate, ruleset, required check, or branch rule changed.

### Security impact and verification

The affected security boundaries are the private response-companion owner/
worker handoff, bounded upstream response parsing, and private projection
output. A concrete pre-fix AddressSanitizer/UndefinedBehaviorSanitizer harness
reproduced a heap use-after-free when an owner task delayed past a callback
timeout wrote decision text through freed callback storage. The repair makes
that storage task- and result-owned until a synchronous post-completion copy;
the same response-header and response-EOS harness is clean under both
sanitizers. The projection change removes the same-UID replacement/deletion
race instead of weakening output validation or deleting a replacement.

| Local validation | Actual result |
| --- | --- |
| `pytest -q tests/test_haproxy_transaction_contract_binding.py` | Passed: 23 tests, including the delayed owner ASan/UBSan harness. |
| HAProxy MRC1 overlay, combined SPOE/HTX, and binding contract suite | Passed: 36 tests. |
| Envoy projection and Stock-lighttpd sidecar suite | Passed: 31 tests; 16 external-runtime tests skipped because their native runtime is unavailable. |
| `go test -race -count=1 ./...` in `connectors/envoy/ext_proc` | Passed: all eight packages. |
| Direct C17 syntax closure, direct HAProxy backend ASan/UBSan test, and `make -C connectors/haproxy check-htx-overlay` | Passed. |
| `pytest -q -p no:cacheprovider tests/test_bilingual_docs.py` and `make check-bilingual-docs` | Passed: 22 tests; repository checker reported `bilingual docs ok`. |
| `git diff --check` | Passed. |

### Runtime evidence, checks not run, and residual risk

These are focused source/component and sanitizer controls, not new full native
host evidence. The successor PR head has not yet been pushed when this
addendum is written; exact-successor GitHub checks, SonarQube Cloud analysis,
and hosted connector runtime cells must be rerun. The wrapper query for the
pre-successor head reported zero open/confirmed SonarQube Cloud issues and an
`OK` Quality Gate, but that result becomes stale after a successor push. The
aggregate-only HAProxy hosted-runtime failure, the unavailable full ten-host
matrix, and the missing fresh external Codex review remain non-passing
evidence gaps. The PR remains Draft; no merge or `master` push is claimed.

## 2026-08-28 Sonar remediation addendum

### Motivation and bounded change

The required managed Sonar wrapper, `/usr/local/bin/sonar-with-env`, is now
authenticated through its managed environment. Its query of PR #344 at
`8a35aa6a752a28ce2062945c2d36e8ee7c41574c` returned an `OK` Quality Gate but
ten open task-owned code-smell issues. The explicit acceptance criterion is
zero open issues, so the green gate alone was not treated as completion.

The remediation makes only P3/P4 response-companion callbacks const-correct.
Their bounded decision scratch storage now belongs to the transport's
per-worker session state and is rebound on initialization, CLAIM, CANCEL, and
RELEASE. A P3/P4 callback can write only through that bounded pointer while
it is synchronous; it cannot change the session capability or retain the
pointer. HAProxy rejects a missing scratch pointer before owner dispatch. The
existing task/result deep-copy boundary remains responsible for delayed owner
work and still prevents callback-storage use after a timeout.

The same focused patch also merges one nested HAProxy result-copy condition,
turns two Stock-lighttpd header-terminator nested expressions into explicit
state transitions, and splits the backend test owner's independent assertion,
blocking, error, and operation-contract checks into helpers. No behavior,
limit, phase order, fail-open/fail-closed choice, workflow, scanner,
suppression, Quality Gate, rule, or branch protection was weakened or changed.

### Validation and compatibility

| Local validation | Actual result |
| --- | --- |
| `pytest -q -p no:cacheprovider tests/test_haproxy_transaction_contract_binding.py` | Passed: 23 tests, including the delayed-owner ASan/UBSan regression. |
| Direct HAProxy response-companion backend C17 ASan/UBSan binary | Passed, including the missing-decision-storage fail-closed control. |
| `pytest -q -p no:cacheprovider connectors/lighttpd/tests/test_stock_sidecar_contract.py` | Passed: 16 tests; 16 native-runtime tests skipped because that runtime is unavailable. |
| C17 `-Wall -Wextra -Werror` syntax checks for the Common transport, HAProxy backend/diagnostic runtime, Stock-lighttpd sidecar, and transport mock test | Passed. |
| `make check-haproxy-c17`, `make check-remaining-connectors-c17`, `make check-common-helpers-c17`, and `make -C connectors/haproxy check-htx-overlay` | Passed. |

Changing the P3/P4 callback qualifiers and replacing the inline session member
with an explicit scratch pointer is source/ABI-incompatible for independently
compiled external implementations of this experimental backend vtable.
Internal implementations and mocks are updated in this PR. External adapters
must recompile and provide bounded scratch storage before invoking P3/P4; they
must not cast away `const` or retain the pointer. The successor commit has not
yet been pushed at this addendum's time, so the wrapper query must be repeated
for that exact remote head before claiming zero open Sonar issues.

## 2026-08-28 successor-analysis follow-up

SonarQube Cloud analyzed successor `f67395bf89f0ceb39b1629ed637b77bf07629bcd`
with an `OK` Quality Gate and removed eight of the ten earlier task-owned
issues. Its exact analysis nevertheless found two new `c:S995` findings in
the HAProxy response-companion backend test. The follow-up changes only a
compare-only native-transaction parameter to pointer-to-const and a read-only
fake-owner parameter to pointer-to-const. It does not change a production API,
test scenario, assertion, phase, limit, host action, scanner, or Quality Gate.

`pytest -q -p no:cacheprovider tests/test_haproxy_transaction_contract_binding.py`
passed all 23 tests after the correction; the direct C17
`-Wall -Wextra -Werror` syntax check and `git diff --check` also passed. The
next normal successor delivery and its exact-head wrapper query remain
required before this record claims zero open SonarQube Cloud issues.

## 2026-08-29 Sonar-zero and traceability addendum

### Scope and implementation decision

This bounded follow-up removes only real duplication and test-helper
complexity discovered by SonarQube Cloud. Commit
`d91a0df57daf5800fe3520c1f63e9f383c25d240` table-drives identical Envoy
response-header cases, centralizes the shared NGINX intervention
classification while retaining each host action, and reuses equivalent
Traefik, lighttpd, and C transport-test setup. Commit
`b2da4449672975f14d2c0953f7b779942af3122f` then groups the five coherent C
transport setup values into `mock_transport_setup`, reducing the helper from
ten to six parameters. It does not alter a connector protocol, P1--P4,
limits, Strict/Safe behavior, callbacks, cancellation, cleanup, or production
source behavior.

No workflow, ruleset, required check, branch rule, SonarQube setting,
exclusion, suppression, Quality Gate threshold, test case, or `paths.env`
file changed. The changes stay within the Parent repository; Framework and
MRTS source and Gitlinks remain untouched.

### Observed exact-head SonarQube Cloud result

SonarQube Cloud analyzed PR #344 at
`b2da4449672975f14d2c0953f7b779942af3122f` on
`2026-08-29T10:05:19+0000`. The managed read-only wrapper
`/usr/local/bin/sonar-with-env` observed all required zero values:

| Metric | Observed result |
| --- | --- |
| Quality Gate | `OK` |
| Open or confirmed issues | `0` |
| Accepted issues | `0` |
| New Code bugs | `0` |
| New Code vulnerabilities | `0` |
| New Code code smells | `0` |
| New Code security hotspots | `0` |
| New Code duplicated lines | `0` |
| Duplication on New Code | `0.0%` |

`new_coverage` was not returned by the PR measure query; no coverage file was
removed, hidden, or altered. The Quality Gate has no failed coverage condition.

### Local validation and security boundary

| Validation | Actual result |
| --- | --- |
| Direct `response_companion_transport_test` C17 build with `-Wall -Wextra -Werror` and execution | Passed. |
| Common helper, SDK, security-contract, memory-safety, and flow-integrity checks | Passed. |
| `make check-no-crs-source-normalization` | Passed: 124 tests. |
| Envoy processor unit and race checks; Traefik observer unit and race checks | Passed. |
| Scoped NGINX/lighttpd contracts | Passed: 32 tests, one expected Stock-sidecar loopback skip because local ModSecurity include/library paths are unavailable. |
| `git diff --check`, Go formatting, and source-tree bytecode inspection | Passed. |

An independent focused review of the C setup-value refactor found no security
regression: callback binding, private `0700` socket directories, timeout
values, cancellation/race assertions, body-payload exclusion, and deterministic
cleanup remain intact. NGINX C17 remains `blocked_environment` because NGINX
headers/source are absent locally; its common-adoption check still has the two
unchanged documented body-mapper assertions. Those limitations are not treated
as passing evidence.

### Delivery boundary

This paired documentation addendum itself advances the PR head. The final
remote/PR head SHA, exact-head hosted checks, fresh SonarQube Cloud result,
and final regular and security Codex reviews are therefore revalidated after
this documentation commit. To avoid a self-referential commit loop, the final
SHA is bound in the mutable PR description and task-completion evidence, as
per the repository traceability policy. PR #344 remains Draft and `UNSTABLE`;
this record makes no merge or `verified_pr` claim.

## 2026-08-29 HAProxy hosted-evidence projection addendum

### Motivation and acceptance criteria

The existing HAProxy `with-crs/no-mrts` hosted runtime deliberately skipped its
evidence upload: its runtime root can be modified by processes running as the
same runtime identity, so copying it or changing its mode would not establish
a trustworthy upload boundary. This limited follow-up accepts only a fixed,
successful HAProxy P2 source receipt and produces a new, canonical, bounded,
payload-free, secret-free metadata package after runtime cleanup.

The local acceptance criteria are strict source schema/path/type/size/digest
validation, exactly the two allowlisted files `haproxy-runtime-evidence.json`
and `manifest.json`, a separately owned sealed staging package, and no checkout
code running with retained root privilege. Final acceptance additionally
requires the exact pushed PR head to complete all five hosted runtime cells,
show `Upload real runtime evidence` as `success`, expose an artifact accepted
by the shared verifier, and receive the required fresh external checks and
reviews.

### Technical decisions and security impact

`ci/runtime/lifecycle/project-haproxy-runtime-evidence.py` uses only the
standard library and descriptor-relative `O_NOFOLLOW` reads to reject paths,
symlinks, special files, unexpected JSON, forbidden metadata categories, and
non-canonical output. It never recursively discovers or copies a runtime tree.
The harness writes the fixed receipt after its existing cleanup instead of
providing runtime output for upload. The workflow starts runtime, source export,
projection, verification, and final summary code only in a private PID/mount
namespace after `setpriv` drops to the intended unprivileged identity with
`no_new_privs` and cleared capabilities/groups. Fixed privileged operations
only create, own, and seal the staging parent; they do not execute checkout
Python or accept runtime-controlled paths.

The untrusted receipt first crosses a fixed unprivileged
`head --bytes=16385` stream cap and then reaches the projector only through
standard input after the identity drop. The projector accepts at most 16 KiB
and rejects the 16,385th byte, so the workflow does not collect untrusted
receipt output in a shell variable. It is not an argument to `sudo`,
`unshare`, or `setpriv`.

The exact Git-object checks bind each post-runtime invocation to the requested
blob rather than a workspace pathname that the preceding runtime could change.
They are not a claim that PR-selected code is authenticated: the security
property is that such code has already lost privilege and runs in the bounded
namespace. The final upload path is limited to the two revalidated package
files and retains `if-no-files-found: error`.

This resolves local findings `FND-PARENT-0987` (checkout Python previously
reachable through a privileged helper path) and `FND-PARENT-0988` (a detached
runtime descendant could escape process-group-only cleanup) at the source and
workflow-contract level. Their exact-head hosted validation remains open;
neither finding is recorded as verified or closed.

### Changed files and actual local results

The implementation changes the one named workflow, its final summary runner,
the HAProxy smoke harness, the projector/verifier, and focused projector,
harness, workflow, CI-security, and runtime tests. This English/German testing
guide pair and this Change Record pair document the new bounded evidence
contract. No scanner configuration, SonarQube setting, exclusion, suppression,
Quality Gate, ruleset, required check, branch rule, `paths.env`, Framework,
MRTS, `master`, or merge state changed.

| Local validation | Actual result |
| --- | --- |
| Focused projector unittest suite | Passed: 17 tests; 9 cross-identity cases skipped because this sandbox cannot provide the required host capability. |
| Focused harness, workflow, and CI-security unittest suite (retained Python environment) | Passed: 40 tests. |
| `make check-ci-security-contract` | Passed: 125 tests; 5 host-capability cases skipped. |
| `actionlint` for `.github/workflows/test-connectors-with-crs-no-mrts.yml` | Passed with no output. |
| `zizmor --offline .github/workflows/test-connectors-with-crs-no-mrts.yml` | Passed: `No findings to report. Good job!` |
| Independent post-patch security review | No concrete remaining local root-bypass path found; it retained hosted namespace/cross-identity execution as required evidence. |

### Runtime evidence, checks not run, and residual risk

These results are local source, contract, and static-workflow evidence only.
No final-head hosted runtime matrix has yet been started for this addendum; no
HAProxy artifact, secret-scan result, CodeQL result, final SonarQube Cloud
query, or fresh exact-head regular/security review is claimed. The prior
SonarQube Cloud zero result is stale as soon as this change advances the PR
head and must be queried through `/usr/local/bin/sonar-with-env` after push.

The local sandbox cannot dynamically prove the distinct hosted identities or
the required `unshare`/`sudo` namespace behavior. The workflow preflights them
and fails closed instead of falling back. PR #344 remains Draft and `UNSTABLE`;
there is no `master` push, merge, `verified_pr`, or production-runtime claim.

## 2026-08-29 HAProxy upload-reader and Sonar follow-up

### Root cause and bounded correction

Exact-head hosted run `33260079101` established that the HAProxy runtime step
aborted under `set -u` before it started the runtime target because
`SETUP_PYTHON_PATH` was step-local. The runtime step now receives the direct,
action-owned `setup-python` output explicitly; it does not trust the mutable
job-level `PYTHON` value exported through `GITHUB_ENV`.

The same exact head had a SonarQube Cloud permission finding for the evidence
directory's `0555` seal. The package directory is now owned by the evidence
UID, grouped to the upload reader's runtime GID, and sealed at `0550`. The two
fixed, payload-free files retain the evidence identity and `0444`; no unrelated
identity can traverse the sealed directory, while the upload reader can read
but cannot create, replace, rename, unlink, chmod, or otherwise mutate the
package. This avoids a recursive copy, ACL, suppression, or privileged
checkout-code path.

The focused source correction also removes the reproduced Sonar rule patterns
for redundant exception types, unsafe type narrowing, cognitive complexity,
an unused summary parameter, and an ambiguous exception-test expression. No
Sonar configuration, exclusion, suppression, Quality Gate, CI requirement,
ruleset, branch rule, or `paths.env` changed.

### Actual local validation

| Local validation | Actual result |
| --- | --- |
| Focused projector, evidence-workflow, harness, and CI-security unittests | Passed: 59 tests; 10 expected cross-identity skips because this sandbox cannot map the required identities. |
| Runtime workflow-summary contract tests | Passed: 61 tests. |
| `make check-ci-security-contract` | Passed: 125 tests; 5 documented host-capability skips. |
| `actionlint`, `zizmor --offline`, `make check-bilingual-docs`, `make check-doc-links`, `sh -n`, and `git diff --check` | Passed; zizmor reported no findings. |
| Local Sonar agentic analysis | Not available: the authenticated CLI reports that Vortex analysis is unavailable for this organization; this does not replace the required PR analysis. |

### Remaining exact-head evidence

The new local candidate has not been committed or pushed when this addendum is
written. Therefore no hosted runtime/upload result, artifact inspection,
secret-scan or CodeQL result, SonarQube Cloud zero result, or fresh regular and
security Codex review is claimed. Those checks must be rerun on the exact
successor PR head, and PR #344 remains Draft until then.

## 2026-08-29 immutable Git-blob and bounded-cleanup follow-up

### Evidence-bound correction

Exact-head hosted run `33263212757` reached the final summary step in the
four non-HAProxy cells but exited with status `2`; the HAProxy projector and
verifier use the same launcher pattern. The four embedded Python launchers
formed their Git SHA-1 preimage with printable `b"\\0"` bytes instead of
Git's required NUL delimiter `b"\0"`. A direct current-blob calculation
reproduced that the correct NUL preimage equals the Git object ID while the
printable form does not, so each launcher failed before `exec(compile(...))`.
The correction changes only those four delimiter literals. It leaves the
object-ID check, 128-KiB source bound, sanitized Git environment, namespace,
identity drop, capability clearing, and fail-closed shell behavior unchanged.

The HAProxy cleanup regression uses a `setsid` leader with a TERM-ignoring
descendant. The prior group-only TERM path left that group observable and
returned a failed cleanup. The harness now gives the recorded leader a bounded
grace window, waits for it once it has exited or become a reapable zombie, then
terminates residual group members and escalates to `KILL` only after another
bounded window. It still rejects an unkillable leader or nonempty group and
withholds the receipt, projection, and upload on any failure. The added `ps`
preflight is required only for the existing evidence-receipt `setsid` mode;
it distinguishes an exited-but-unreaped leader from a still-running leader so
ordinary successful cleanup does not consume every bounded window.

### Actual local validation

| Local validation | Actual result |
| --- | --- |
| Immutable Git-blob workflow regression before correction | Failed as intended: the workflow contained zero of four correct NUL delimiters. |
| Immutable Git-blob workflow regression after correction | Passed. |
| TERM-ignoring descendant cleanup regression before correction | Failed as intended: `stubborn process group remains alive after cleanup`. |
| Focused HAProxy cleanup harness suite after correction | Passed: 6 tests. |
| Focused projector, workflow, harness, CI-security, and runtime-summary suite | Passed: 122 tests; 10 expected cross-identity skips. |

### Remaining exact-head evidence

This successor is still local at the time of this addendum. No successful
five-cell hosted runtime, HAProxy artifact upload/inspection, Secret Scanning,
CodeQL, successor SonarQube Cloud zero result, or fresh regular and Security
Codex review is claimed. Those checks must bind to the eventual exact pushed
head; PR #344 remains Draft, and no scanner, Quality Gate, ruleset,
required-check, `paths.env`, `master`, or merge change is part of this work.

## 2026-08-29 bounded HAProxy build-target diagnostic follow-up

### Current hosted state

The exact-head five-cell workflow
[`33266984528`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33266984528)
ran at `8757a8d1689d6cccd70327b681b9bb90f7e44433`. Apache, Envoy, Traefik,
and lighttpd completed successfully. HAProxy job `99138670479` failed while
preparing the runtime components, before projection, verification, upload, or
artifact creation. Its existing sanitized output established the real nonzero
exit but did not contain an allowlisted compiler/linker classification. This
record therefore does not attribute the current failure to an earlier,
historical header diagnosis.

### Bounded correction and security boundary

The provisioning helper now reads only GNU Make failure footers from the
captured `stderr` stream. It accepts exactly two existing logical target names
— `build-modsecurity-binding` and `build-spoa-runtime` — or maps a footer's
output-target spelling only when it is byte-for-byte equal to the
internally-derived expected output path. It emits, at most, one fixed
`target_failure=<allowlisted-target>` label. It discards Makefile paths, line
numbers, commands, raw compiler output, arbitrary targets, secrets, and all
`stdout` target-like text.

A controlled standalone GNU Make run confirms that a failing prerequisite can
produce only the file-target footer, not a phony-goal footer. The exact
expected-path comparison therefore keeps the combined invocation intact while
covering both Make footer forms without publishing the path.

The Make invocation remains one combined invocation; it is not split merely
for diagnostics. A failure still preserves its original status and exit code,
keeps raw build output private, and blocks the receipt, projector, verifier,
and upload exactly as before. The label is diagnostic metadata only; it is not
trusted evidence and cannot influence cleanup, authorization, or artifact
publication. A syntactically valid footer could be forged by a failing build
recipe on `stderr`, so it can only guide the next root-cause investigation; it
does not prove source attribution.

The independent review also revisited numeric-PID cleanup. The historical
detached-session condition remains tracked as `FND-PARENT-0988`. The hosted
runtime executes in a mandatory private PID/mount namespace with
`--kill-child=SIGKILL` before the separate-owner staging step starts. A
PID/PGID reuse scenario is not reproduced and is contained to that namespace;
it remains an availability-risk consideration rather than a newly validated
cross-stage integrity bypass.

### Actual local validation and remaining evidence

| Local validation | Actual result |
| --- | --- |
| Projector, evidence-workflow, evidence-harness, and provisioning unit suites | Passed: 93 tests; 10 cross-identity tests skipped because this sandbox cannot provide the required hosted identity mapping. |
| Five-cell runtime workflow security contract | Passed: 1 test. |
| Whitespace review | `git diff --check` passed. |
| Independent post-patch diagnostic/security review | No injection, path disclosure, fail-open, cleanup, or upload-boundary regression found. |

The next normal PR-branch successor must identify the target on an exact
hosted run before any HAProxy build-source correction is considered. A
successful exact final head still requires all five runtime cells, HAProxy
projection/verification/upload and artifact inspection, Secret Scanning,
CodeQL, the complete SonarQube Cloud zero target, and fresh regular plus
Security Codex review. PR #344 remains Draft.

## 2026-08-29 bounded HAProxy diagnostic parser and decoder follow-up

### SonarQube Cloud remediation and diagnostic boundary

At exact PR #344 head `1a6d711752d86033e8c0b959a73683e1125ff3bc`, SonarQube
Cloud reported one open `python:S8786` issue in the HAProxy Make-footer parser.
The Quality Gate was `OK`, but the open code smell meant the user's required
zero target was not met. The regex is replaced with a deterministic ASCII
parser for the existing Make prefix, optional numeric job level, footer
delimiter, numeric exit code, and optional location prefix. It retains the
closed allowlist of the two logical targets and the exact trusted output-path
control. It never emits captured target or path text.

Diagnostic scanning is explicitly per stream: `stderr` is examined before
`stdout`, at most 512 lines and 4096 characters per line are examined for each
stream, and an overlong untrusted line stops that stream. Recognized resolver,
compiler, and linker indicators map only to fixed constants. The failed build
status, exit code, receipt, cleanup, projection, verifier, upload eligibility,
and event privacy controls remain unchanged.

A separate controlled child exposed a decoding boundary: invalid tool-output
bytes previously raised `UnicodeDecodeError` before the HAProxy helper could
return its failed result. `run_env` now accepts an optional decoding policy,
but only `run_haproxy_binding_build` supplies `errors="replace"`. Other
callers retain strict decoding. The exact fixed Make argv and private-log path
are unchanged; the original nonzero result reaches the existing structured
failure and cleanup path. This local correction is tracked as
`FND-PARENT-0990` pending exact delivered-head hosted verification.

### Root-cause discipline

The prior hosted target label `target_failure=build-modsecurity-binding` is
not a source-cause diagnosis. Independent source review confirmed that the
binding common-object loop does not compile the response-runtime source that
includes ModSecurity headers; the response-runtime loop already passes the
resolved include directory. No speculative Makefile include-path change is
made. The next exact-head hosted result must provide a fixed allowlisted cause
before any HAProxy build-source, resolver, Makefile, harness, or workflow
repair is considered.

### Actual local validation and remaining evidence

| Local validation | Actual result |
| --- | --- |
| `tests.test_prepare_runtime_components` | Passed: 67 tests, including deterministic footer grammar/bounds and invalid-text decoder regression/control. |
| HAProxy projector/workflow/harness/provisioning plus selected five-cell contract | Passed: 99 tests; 10 expected cross-identity skips. |
| `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract` | Passed: 125 tests; 5 host-capability skips. |
| HAProxy resolver and libModSecurity compatibility contracts | Passed: 18 tests. |
| Python compile check | `python -m compileall -q ci/provisioning/components/prepare-runtime-components.py` passed. |
| Workflow/documentation/shell static checks | `actionlint`, `zizmor --offline`, harness `sh -n`, `make check-bilingual-docs`, and 22 bilingual-doc tests passed. |
| Whitespace review | `git diff --check` passed. |
| Independent post-fix security review | No concrete decoding bypass, command injection, raw-output disclosure, fail-open, cleanup, projection, or upload regression found. |

The existing `stdout=PIPE`/`stderr=PIPE` capture and private-build-log volume
are not bounded by this narrow decoder remediation and remain a hardening
observation. No workflow, scanner, Quality Gate, suppression, ruleset,
required check, `paths.env`, Framework, MRTS, `master`, or merge state changed.
The next normal successor must receive exact-head hosted HAProxy evidence,
SonarQube Cloud zero results, and fresh regular plus Security Codex review;
PR #344 remains Draft.

## 2026-08-29 exact resolver-cause correlation follow-up

### Exact-head boundary and narrow diagnostic

At exact PR #344 head `888482e81348850c6281f446c8cadbae48d6f6da`, workflow
[`33274434129`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33274434129)
completed Apache, Envoy, Traefik, and lighttpd successfully. HAProxy job
`99158566221` failed in the real with-CRS/no-MRTS step before evidence
projection, verification, or upload. An authorized bounded inspection retained
only `target_failure=build-modsecurity-binding`,
`classification=resolver_error`, and `build_step=modsecurity_resolver` in an
external payload-free summary. Its raw 76,712-byte job-log download was
checksum-recorded and deleted from the task root; it is neither repository
content nor evidence of a source cause.

The provisioning helper now adds the fixed
`resolver_cause=unresolved_runtime_dependencies` value only when one bounded
`stderr` line equals the resolver's existing static failure line after the
normal single terminal CRLF carriage return is removed. It does not parse a
path, header, tool output, credential, or suffix. A line with any additional
content retains at most the existing generic resolver labels, and the same
text on `stdout` cannot select the new cause enum. The
diagnostic stays advisory: a build recipe can still emit a static-looking
line, so an emitted enum narrows follow-up investigation but does not prove
the underlying resolver input, dependency, or source owner.

The original nonzero build result, transactional cleanup, private raw-log
handling, receipt eligibility, projection, verifier, upload gate, workflow
permissions, and all scanner and Quality-Gate settings are unchanged. No
resolver, Makefile, connector, harness, or workflow repair is claimed by this
follow-up.

### Actual local validation and remaining evidence

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
tests.test_prepare_runtime_components` passed 68 tests. The new regression
covers the exact `stderr` line, a credential-bearing suffix, the same line on
`stdout`, and an unknown resolver failure, while existing integration tests
retain failed status, original exit code, and staging cleanup controls.

The current hosted summary did not contain the exact static resolver line, so
the actual sub-cause remains unestablished. A normal successor must obtain its
own exact-head hosted result before any resolver or build repair can be
considered. PR #344 remains Draft and still requires successful hosted
HAProxy evidence publication, final scanner/Sonar evidence, and fresh regular
and Security Codex review.

## 2026-08-30 candidate validation and remaining decision boundary

### Current candidate and security boundary

At the local-validation point of this Change Record, the broader successor
candidate had not yet been staged, committed, or pushed. Its HAProxy component
adds a descriptor-open regression for a symlinked intermediate
source-directory component; receipt-mode cleanup uses fixed trusted process
tools and `/bin/rm`, propagates result-writer and startup-cleanup failures,
and rejects any unexpected process-inspection result. These changes preserve
the existing receipt, projection, verifier, and upload gates: a failed cleanup
cannot create an eligible receipt.

The candidate also contains the narrow `python:S3776` helper extraction in
the HAProxy diagnostic path and previously reviewed Envoy and Traefik
hardening. The Envoy work resolves the directly observed unlink-on-error,
unexpected-`Serve`, shutdown-deadline, and late-accept cases. It does not
claim to solve the separate pathname-UDS same-effective-UID substitution and
final-unlink race. That residual is retained locally as `FND-PARENT-0991`,
`P1`, `blocked`, and `requires_user_decision`: the required restart-compatible
UDS topology cannot safely be selected implicitly. `FND-PARENT-0992`, the
HAProxy receipt cleanup command-resolution finding, is locally fixed and
awaits exact delivered-head hosted verification.

At exact remote PR head `c1a9a80aa33959e418ac9467278a7685cc51399a`, hosted
workflow [`33276652544`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33276652544)
failed in HAProxy job `99164435759` during the libModSecurity resolver before
projection, verification, or `Upload real runtime evidence`. The known result
is `target_failure=build-modsecurity-binding`,
`classification=resolver_error`, and `build_step=modsecurity_resolver`; it is
not upload evidence and does not justify a speculative Makefile repair. The
current SonarQube Cloud readback for that same remote head has one open
critical `python:S3776` issue (`AaBPeSvj3f23caWmipnJ`) in
`ci/provisioning/components/prepare-runtime-components.py`; no zero-issue
claim is made for the uncommitted extraction.

The candidate now makes the unavoidable two-file digest boundary explicit
without fabricating a self-digest: after the common verifier has reopened and
validated both fixed package files, it emits a canonical, newline-terminated,
at-most-1-KiB detached record with both SHA-256 values. The workflow captures
that record outside the two-file package in a fixed root-owned `0640` file,
reopens it with `O_NOFOLLOW`, rejects noncanonical JSON, duplicate keys,
non-integer schema versions, unexpected fields, unsafe ownership/mode/size,
or anything other than the two fixed lowercase digests, and writes only those
two validated values to `GITHUB_OUTPUT`. It removes the detached record before
upload; neither it nor a runtime root is an artifact input. An independent
post-patch review found no concrete bypass or regression in this additional
evidence path.

### Actual local validation

| Local validation | Actual result |
| --- | --- |
| Focused HAProxy projector suite | Passed: 26 tests; 11 expected cross-identity skips. The block-device source test is present but needs a mapped Cross-Identity fixture. |
| Projector, workflow-contract, HAProxy-harness, provisioning, CI-security, and Traefik runtime-security Python suite | Passed: 162 tests; 11 expected cross-identity skips. |
| HAProxy receipt harness syntax and direct contract suite | Passed: `sh -n` and 14 tests, including PATH-shadowed `rm`, stale startup cleanup, result-writer failure, and process-group controls. |
| Envoy ext_proc observer | Passed with a short isolated Unix-socket temporary root: `go test -race -count=1 ./...` across eight packages and `go vet ./...`. |
| Traefik response observer | Passed with a short isolated Unix-socket temporary root: `go test -race -count=1 ./...` and `go vet ./...`. |
| Hosted workflow static controls | Workflow-YAML validation, `actionlint`, and `zizmor --offline` passed. |
| Formatting and whitespace | `gofmt -d` for changed Envoy files and `git diff --check` passed. |

An earlier Go test attempt with an excessively deep temporary directory failed
before the relevant Unix-socket tests started (`bind: invalid argument`); it
is not counted as a successful test. The short-root reruns above are the
recorded evidence.

### Delivery state and remaining blockers

The HAProxy runtime-evidence workflow is the one explicitly authorized
workflow edit in this candidate. No scanner, Quality-Gate, ruleset,
required-check, `paths.env`, `master`, or merge change was made. PR #344
remains Draft.
The remaining delivery blockers are: an explicit Envoy UDS ownership/restart
topology decision for `FND-PARENT-0991`; a source-specific diagnosis or a new
successful hosted result for the HAProxy resolver failure; a pushed exact-head
SonarQube Cloud zero result; then the required exact-head artifact, scanner,
and regular plus Security Codex review evidence. No final-hosted success is
asserted before those conditions exist on one last unchanged head.

## 2026-08-30 post-delivery observation and successor correction

The authorized HAProxy evidence-publication correction was committed and
normally pushed as `74aab90978107e0f104b4441a476dfa2d6a53279`. Exact-head
workflow
[`33285597376`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33285597376)
passed Apache, Envoy, Traefik, and lighttpd. HAProxy failed in its real runtime
step before projection, verification, or upload, so its evidence upload was
skipped fail-closed and no artifact/upload success is claimed.

Exact-head SonarQube Cloud reported two open issues: `python:S5778` at
`tests/test_haproxy_evidence_projection.py:323` and `python:S3776` at
`ci/provisioning/components/prepare-runtime-components.py:9195`. The local
S5778 test-only adjustment preserves the projector call; the local S3776
helper extraction preserves the bounded, stderr-first, fixed-label diagnostic
behavior. Neither is yet a remote Sonar result.

`FND-PARENT-0993` records and corrects a local Traefik forwardAuth P3
compatibility defect. The C adapter now passes Common's total-header limit
unchanged, while the Go observer enforces the actual MRC1 frame size. Its
observer header ceiling is aligned from 128 to Common's 256; controls cover
256 accepted, 257 rejected, exact 65,536-byte payload accepted, one byte over
rejected, and a sparse Common-valid 65,204-byte frame. The focused Python
suite passed 16 tests, `go test -race -count=1 ./...` and `go vet ./...`
passed, and the combined affected Python suite passed 162 tests with 11
explicit cross-identity skips. A native C build remains not run because this
checkout lacks a local libModSecurity include/library pair; the exact hosted
runtime is the relevant build evidence.

`FND-PARENT-0991` remains intentionally unstaged pending the explicit Envoy
pathname-UDS topology decision. PR #344 remains Draft; no `paths.env`,
scanner, Quality Gate, ruleset, required-check, `master`, or merge change is
made by this addendum.

## 2026-08-30 bounded HAProxy resolver-sentinel follow-up

At exact head `eabf2b07ed4e5f317e2435d5f40e5b48d84f92a1`, workflow
[`33288804917`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33288804917)
is terminal. Apache, lighttpd, and Traefik succeeded; Envoy and HAProxy
failed. HAProxy again reached the real runtime step after its evidence-boundary
preparation, but exposed only `target_failure=build-modsecurity-binding`,
`classification=resolver_error`, and `build_step=modsecurity_resolver` before
failing. Projection, verification, upload, and a HAProxy artifact did not run.
That is a release blocker, not a source-cause result.

The successor candidate gives the resolver one closed machine-readable
channel. Every controlled `blocked` branch first emits one literal
`BLOCKED: HAProxy libModSecurity resolver: sentinel=<cause>` line from the
fixed 22-value allowlist, then retains its existing human-detail line and exit
status `77`. Seven additive causes identify every nonempty missing-header mask
of the fixed public trio (`modsecurity.h`, `rules_set.h`, and
`transaction.h`); the defensive `headers_missing` cause remains as the
fallback for a non-exact state. An unknown internal code is rejected with the
same nonzero exit. The legacy detail is not parsed as a cause.

The Python recognizer maps only one complete, bounded `stderr` sentinel line
to fixed `classification=resolver_error`, `build_step=modsecurity_resolver`,
and `resolver_cause=<allowlisted-value>` diagnostics. It accepts the existing
single-terminal-CRLF normalization but rejects a suffix, second carriage
return, unknown value, overlong line, and the same text on `stdout` for cause
correlation. Those cases retain at most generic resolver labels. When
`GITHUB_ACTIONS=true`, exactly one recognized cause additionally emits only
the fixed `::error title=HAProxy resolver diagnostic::resolver_cause=…`
annotation; no raw path, header, body, token, command, or tool output reaches
it. The annotation cannot change build status, cleanup, receipt eligibility,
projection, verification, upload, scanner, or Quality-Gate behavior.

Actual local validation of this uncommitted candidate passed: resolver shell
syntax; an in-memory Python syntax check; 14 focused resolver tests; and 71
focused provisioning tests. The latter cover all sentinels, CRLF, suffix,
stdout, unknown, and overlong rejection, a rejected unknown internal cause,
private-output non-leakage, and exact annotation behavior. The candidate has
not yet produced a hosted run, so it does not establish the HAProxy root cause
or successful evidence publication.

## 2026-08-30 HAProxy cache completeness and MRC1 P3 framing

The hosted HAProxy resolver reported the bounded generic
`resolver_cause=headers_missing`. The resolver requires the v3 public trio
`modsecurity.h`, `rules_set.h`, and `transaction.h`, while the shared-cache
readiness predicate had accepted a prefix containing only `modsecurity.h` and
the library. The Parent cache publisher now uses the same three-header
predicate both before publishing source build output and before reusing a
published prefix. A marker-valid but incomplete prefix is therefore discarded
and rebuilt rather than silently reaching the HAProxy resolver.

MRC1 keeps its 65,536-byte generic frame and logical name/value aggregate
limits. It makes only P3 `RESPONSE_HEADERS` opcode-aware: a C peer may receive
or send a payload of at most 66,630 bytes, enough for the existing 64-byte HTTP
version maximum, 256 four-byte field prefixes, and the unchanged 65,536-byte
logical aggregate. Other opcodes remain at 65,536 bytes. The Envoy and
Traefik HTTP/1.1 observers emit at most 66,574 P3 payload bytes and still reject
more than 256 fields or one byte beyond the logical aggregate; this is a
framing-capacity correction, not a phase or header-policy expansion.

The shared C transport treats those Common count and aggregate ceilings as
non-negotiable: initialization and start reject counts outside `1..256` and
aggregate-byte limits outside `1..65,536`, and the decoder repeats both hard
limits before any backend header callback. This remains true if public
configuration is modified after initialization. Raw P3 controls reject a
257-field frame and a 65,537-byte aggregate before backend processing; the
ordinary exact-limit P3/cancel control remains accepted and cleans up
deterministically.

| Local validation | Actual result |
| --- | --- |
| ModSecurity cache contract | Passed: 45 tests, including complete-prefix reuse and deterministic rebuild after each required public header is removed while cache markers remain valid. |
| Provisioning and HAProxy resolver contracts | Passed: 70 provisioning tests and 14 resolver tests. |
| Direct C17 MRC1 transport integration | Passed with `-std=c17 -Wall -Wextra -Werror`: 256 P3 fields with exactly 65,536 logical bytes are accepted, then cancel performs deterministic cleanup. |
| Envoy and Traefik response observers | Passed: focused `go test -race -count=1` plus `go vet` with a short task-owned Unix-socket temporary root. |

At the time of this local validation, the candidate had not yet produced a
successor hosted run. This addendum does not claim that the cache correction
alone proves the hosted HAProxy root cause or that HAProxy evidence publication
has succeeded. No workflow, scanner, Quality-Gate, ruleset, required-check,
`paths.env`, `master`, or merge change is part of this addendum.

## 2026-08-30 response-companion listener recovery

### Motivation and acceptance criteria

`FND-PARENT-0997` records a reproduced shared lifecycle defect: a terminal
Common listener `poll` or `accept4` exit cleared `listener.running`, but a
caller-owned ready flag could still make a later Envoy ext_authz or Traefik
forwardAuth startup call succeed. The direct HAProxy SPOE/SPOP native-HTX route
had no equivalent live-listener check before it moved transaction ownership to
the bounded response backend.

The acceptance criteria are that every opaque P2-to-P3/P4 handoff has a live
private listener and expiry owner, a dead listener is fully cleaned before a
fresh start, incomplete cleanup fails closed before ownership moves, normal
live-listener startup remains accepted, and the direct HAProxy order is covered
by a regression. Exact delivered-head hosted, SonarQube Cloud, and review
evidence remain required after the normal successor.

### Technical decision and security impact

The shared
`msconnector_response_companion_transport_ensure_running` helper is the single
lifecycle seam. It rejects a transport whose stopping state denotes incomplete
cleanup, joins and cleans a dead prior listener, and starts a fresh private UDS
listener. `ensure_started` delegates to it for Envoy and Traefik. HAProxy calls
it before both `haproxy_modsecurity_transaction_handoff_response_companion` and
`haproxy_spop_response_companion_handoff`. A nonzero `pthread_join` result is
now a cleanup failure, so the transport remains stopped and cannot be reused.

The change preserves the private UDS, peer-identity, bounded worker, opaque
handle, TTL, and no-payload-event invariants. It adds no network endpoint,
fallback, or privilege. An incomplete cleanup or listener restart failure
returns the existing fail-closed connector path before a handle/lease can be
created. The deterministic descriptor-close test proves the lifecycle
transition, not a remote method for causing a terminal kernel error; no
authorization bypass or fail-open behavior was observed.

### Changed files and documentation

- `common/runtime/response_companion_transport.h`
- `common/runtime/response_companion_transport.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/response_companion_transport_test.c`
- `tests/test_haproxy_transaction_contract_binding.py`
- `common/docs/transaction-phase-contract.md` and
  `common/docs/transaction-phase-contract.de.md`
- this English/German Change Record pair

### Tests and actual results

| Validation | Actual result |
| --- | --- |
| Strict C17 listener-recovery regression | Passed with `-std=c17 -Wall -Wextra -Werror`; after forced terminal listener exit it joins, restarts, accepts a fresh private client, and removes the owned socket. |
| Pre-fix regression | Reproduced as expected: exit `134` at the assertion that a stale-ready call must not leave `listener.running` false. |
| HAProxy handoff contract | `python3 tests/test_haproxy_transaction_contract_binding.py` passed; it proves `ensure_running` precedes both transaction ownership transfer and backend handoff. |
| Envoy/Traefik companion contracts | `python3 -m unittest -v tests.test_envoy_transport_hardening_contract tests.test_traefik_transport_hardening_contract tests.test_traefik_forwardauth_p2_contract` passed `39` tests. |
| Common and adapter controls | `make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity` and `make check-adapter-contracts check-http-authorization-service-timeout` passed. |
| Documentation and whitespace | `git diff --check`, `make check-bilingual-docs`, and `make check-doc-links` passed against the final local candidate. |

### Runtime evidence, checks not run, and limitations

The C regression is a local private-UDS runtime control. It does not claim a
deployed Envoy, Traefik, or HAProxy host runtime, and no fresh hosted check,
SonarQube Cloud result, or remote listener-error trigger exists for this
uncommitted successor. The direct module invocation of `unittest` found no
function-style HAProxy tests, so the file's repository-native direct entrypoint
was used; `pytest` is unavailable locally. Neither result is treated as a
product failure or as the regression evidence.

### Final review and delivery status

The one permitted independent post-patch bypass/regression review found the
direct HAProxy sibling route. It was confirmed from source, incorporated in
the same remediation, and all focused checks above were rerun; no second review
cycle was opened. At this local-validation point, PR #344 remains Draft and
this Change Record has no successor-delivery fact yet. No workflow, scanner, Quality-Gate, ruleset,
required-check, `paths.env`, `master`, or merge change is included.

## 2026-08-30 HAProxy non-ready ModSecurity preflight

Exact head `7f4f7a8a5060b4cc2d32a08116c66c95363146dc` reached the five-cell
hosted runtime matrix. Apache, Envoy, Traefik, and lighttpd succeeded; HAProxy
failed after the shared ModSecurity component reported
`modsecurity_build_failed` and the resolver observed all three public headers
absent. That outcome is a release blocker, not evidence of successful HAProxy
runtime evidence publication.

The source trace found a status-integrity gap in HAProxy's preflight: it
rejected only the literal `blocked` state, while the canonical ready set is
exactly `present`, `built`, and `reused`. A `failed`, `unknown`, missing, or
otherwise non-ready shared record could therefore reach host preparation and
the binding resolver. The resolver still failed closed, but too late and with
an avoidable opportunity for host-level resolution behaviour.

HAProxy now rejects every state outside `READY_COMPONENT_STATUSES` before
cache reuse, preparation, binding compilation, linking, or environment-based
resolver fallback. It records `blocked` and preserves the source blocker
reason, with the existing fixed `modsecurity_build_failed` fallback. The
shared producer/cache predicates, resolver, diagnostics, and other connector
preflights are unchanged by this narrow repair.

The direct local regression covers `blocked`, `failed`, `unknown`, `corrupt`,
optional/not-selected, and absent status values, plus all three allowed
statuses. A separate sink test proves a failed shared record invokes neither
HAProxy preparation nor the binding build. These two focused tests passed
locally; broader validation and fresh exact-head hosted evidence remain
required before PR #344 can be considered verified. No workflow, scanner,
Quality-Gate, ruleset, required-check, `paths.env`, `master`, or merge change
is included.

## 2026-08-30 Apache and NGINX non-ready ModSecurity preflight parity

The subsequent exact-head review established the same status-integrity gap in
the two remaining direct shared-ModSecurity consumers. Apache and NGINX had
rejected only the literal `blocked` state, so a record with `failed`,
`unknown`, `corrupt`, an optional/not-selected value, or no status could reach
their cache-reuse and host-build continuations. The pre-fix direct control
returned `False` for both Apache and NGINX with `status=failed`, while the
legitimate `status=built` control also returned `False`.

Both preflights now use the same canonical allowlist as HAProxy:
`READY_COMPONENT_STATUSES = {present, built, reused}`. Every state outside
that set records `blocked`, preserves the source blocker reason, and uses the
existing fixed `modsecurity_build_failed` fallback. The gate runs before
Apache artifact/cache checks and `build_apache_source`, and before NGINX cache
reuse or `nginx_prepare_or_reuse_runtime`; it therefore cannot publish a
ready-looking host record from a non-ready shared component. The shared
producer/cache schema, host-specific later preflights, resolver behavior,
transaction phases, and the other eight connector solutions are unchanged.

Four focused controls passed locally: Apache and NGINX each exercise all seven
sampled non-ready representations and the three accepted states; separate
Apache/NGINX sink controls prove a failed shared record calls neither host
build continuation. The direct post-fix control returns `True` for
`status=failed` and `False` for `status=built` in both functions. Broader
provisioning/cache, documentation, and exact-successor hosted validation remain
required before PR #344 is considered verified. No workflow, scanner,
Quality-Gate, ruleset, required-check, `paths.env`, `master`, or merge change
is included.

## 2026-08-30 temporary HAProxy component failure classification

### Motivation

The isolated HAProxy hosted-runtime failure stopped at a generic private Expat
or ModSecurity component result. That is insufficient evidence for a build
environment or source repair. This temporary diagnostic can expose one fixed
classification during a deliberately enabled manual run without publishing a
raw build log.

### Acceptance criteria

The diagnostic was off by default, usable only for the HAProxy target with its
evidence receipt, and emitted at most a fixed component, build-step, bounded
exit-code, and classification tuple. It did not alter build outcomes, records,
cleanup, receipt eligibility, projection, verification, upload, or the runtime
sandbox. The switch, emitter, and dedicated tests are now removed after one
enabled dispatch.

### Technical decisions

The temporary `workflow_dispatch` Boolean input,
`haproxy_component_failure_diagnostics`, defaulted to `false`. It evaluated to
`RUNTIME_COMPONENT_FAILURE_DIAGNOSTICS=1` only for an explicit `true` dispatch
and was passed only inside the existing HAProxy isolated `env -i` environment.
The provisioner additionally required `RUNTIME_COMPONENT_TARGET=haproxy` and
`HAPROXY_EVIDENCE_RECEIPT=1`. All of these temporary surfaces are removed in
the cleanup candidate.

Private Expat/ModSecurity output is examined only in memory to select a static
allowlist value. The sole output has the fixed form
`component=<enum> build_step=<enum> exit_code=<0..255|unavailable> classification=<enum>`.
Unknown classifications become `unclassified`; unknown components or steps
produce no diagnostic. Existing component records retain their previous
failure classification and exit-code behavior.

### Security impact

No private command output, argument, path, URL, environment value, header,
body, credential, token, cookie, or raw log was emitted or added to evidence.
The existing `env -i`, `unshare`, `setpriv --no-new-privs`, capability-drop,
UID/GID isolation, cleanup, strict projector, verifier, and fail-closed upload
boundary remained unchanged. An independent post-patch security review found
no diagnostic leak or sandbox regression.

### Changed files

- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_ci_security_workflows.py`
- this English/German Change Record pair

### Tests and actual results

| Validation | Actual result |
| --- | --- |
| Focused diagnostic and HAProxy workflow tests | Passed: 5 tests. |
| `tests.test_prepare_runtime_components` | Passed: 81 tests. |
| Cleanup `tests.test_prepare_runtime_components` | Passed: 77 tests. |
| HAProxy workflow-contract suites | Passed: 38 tests. |
| Runtime, projection, and HAProxy harness contract suites | Passed: 101 tests; 11 environment-supported skips. |
| Cleanup combined workflow, runtime, projection, and harness contracts | Passed: 139 tests; 11 environment-supported skips. |
| `actionlint` | Passed for `.github/workflows/test-connectors-with-crs-no-mrts.yml` before and after cleanup. |
| `zizmor` | Passed for that workflow before and after cleanup; it reported only its offline capability note. |
| Documentation and whitespace cleanup checks | `make check-bilingual-docs`, `make check-doc-links`, and `git diff --check` passed. |

### Runtime evidence

One enabled manual dispatch ran as
[`33333351395`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33333351395)
at exact head `092276eb6395d8caaddbe1a167f5ad065029430c`. Apache, Envoy,
Traefik, and lighttpd succeeded; HAProxy failed in its selected real runtime
step before projection, verification, upload, or HAProxy artifact publication.
The only retained diagnostics were
`component=expat build_step=expat-configure exit_code=1 classification=expat_build_failed`
and
`component=modsecurity build_step=modsecurity-configure exit_code=1 classification=modsecurity_build_failed`.
They establish no source-backed missing dependency, tool, path, or environment
value. No raw job log was stored, reported, or published. The temporary
workflow switch, emitter, and dedicated tests are removed in the cleanup
candidate; this remains a diagnosis, not a production repair.

### Checks not run

`ruff` was not run because no local executable is available. Delivery
preflight and successor hosted checks remain pending at this point.

### Known limitations

The tuple deliberately cannot disclose a compiler, configure, linker, or
network message beyond its fixed classification. A result of `unclassified` is
valid evidence that no source-backed repair is justified yet.

### Residual risks

PR #344 remains Draft and blocked on a source-backed runtime repair and
subsequent exact-head verification. `FND-PARENT-0975` remains `in_progress` /
`blocked_missing_evidence`; the preflight status-integrity behavior is already
covered there and needs no duplicate finding.

### Final review status

The initial local implementation and independent security review completed;
the one enabled bounded manual dispatch completed; the temporary path is
removed; and cleanup validation is complete. Normal delivery to the existing
Draft PR branch and all successor hosted verification are still pending. No
workflow security control, scanner, Quality Gate, ruleset, required check,
`paths.env`, `master`, or merge change is included.

## 2026-08-31 workflow-reset disposition

### Motivation

The user requested that the workflow be reset for now and that decision be
recorded. The temporary HAProxy component-diagnostic workflow path was already
removed at `90cd00384efbbce4e2a26a760ee9e532eb8e953e`; this addendum records
that state and the result of reviewing a broader reset.

### Acceptance criteria

The temporary diagnostic remains absent. The record distinguishes that
completed cleanup from a full HAProxy workflow rollback, describes the
security consequence of the latter, and makes no unverified claim that the
hosted failure is fixed.

### Technical decisions

No workflow behavior is changed by this addendum. Relative to master
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`, the current HAProxy workflow
delta is 657 additions and 8 deletions. A full reset would replace the
isolated `env -i` / `unshare` / `setpriv --no-new-privs` execution and its
receipt projection, verification, and HAProxy-specific upload path with the
master-style direct `make verified-haproxy-case` invocation. That full reset
was not made.

### Security impact

The current invariant is that PR-controlled Make/runtime code cannot retain
the runner identity or capabilities and cannot directly control uploaded
evidence. The master-style direct invocation would remove the privilege drop,
capability clearing, namespace boundary, and verified evidence path. Therefore
the broader reset is not a safe automatic change, even though it is
Git-reversible.

### Changed files

- this English/German Change Record pair

### Tests and actual results

| Validation | Actual result |
| --- | --- |
| HAProxy evidence, harness, and workflow contracts | Passed: 23 tests. |
| `actionlint` | Passed for `.github/workflows/test-connectors-with-crs-no-mrts.yml`. |
| `zizmor` | Passed for that workflow; it reported only its offline capability note. |
| `make check-bilingual-docs` | Passed: bilingual docs ok. |
| `make check-doc-links` | Passed: repository path references and documentation links ok. |
| `git diff --check` | Passed: no whitespace errors. |
| Delivery preflight | Passed: expected writable `origin`, `master` default branch, and Draft PR #344 were confirmed. |

### Runtime evidence

At exact head `90cd00384efbbce4e2a26a760ee9e532eb8e953e`, pull-request run
[`33334626289`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33334626289)
completed with Apache, Envoy, Traefik, and lighttpd successful and HAProxy
failed. It is evidence that the temporary diagnostic removal did not make a
hosted repair; it does not justify removing the hardened workflow boundary.

### Checks not run

`ruff` was not run because no local executable is available. Successor hosted
checks remain pending for this documentation-only addendum.

### Known limitations

"Reset the workflow" has two materially different meanings: the temporary
diagnostic reset is already complete; a full reset to master would remove
security controls. No security-preserving broad rollback has been specified.

### Residual risks

PR #344 remains Draft and blocked on a source-backed HAProxy runtime repair.
Removing its isolation or evidence-verification controls merely to make the
job resemble the master path would reintroduce a privilege/evidence boundary
risk.

### Final review status

The requested reset was reviewed and recorded. The temporary path remains
removed; the current hardened workflow remains unchanged. No workflow,
master, merge, scanner, Quality Gate, ruleset, or required-check change is
performed by this addendum.

## 2026-08-31 HAProxy private TMPDIR preparation repair

### Motivation

The selected HAProxy runtime failed before evidence projection with an Expat
`configure` failure, followed by the expected fail-closed ModSecurity and
HAProxy blocking records. The generic hosted summary did not contain private
configure output. A bounded local configure-only differential established that
the isolated run passed a `TMPDIR` below the verified run root without first
creating that directory.

### Technical decision

The HAProxy branch now binds the canonical runner temporary directory and run
ID to GitHub context values, then derives every runtime root from those values
and the validated parent SHA. It rejects a changed inherited root, run ID, or
cell identity; verifies every existing root ancestor is a directory rather
than a symlink and resolves canonically; and passes only the re-derived build,
source, cache, log, temporary, and component-cache paths into the isolated
environment. The CRS preparation owns the pre-existing verified root; the
runtime creates only its previously absent private `tmp` child with mode
`0700`, re-applies strict modes, and verifies the expected runtime UID/GID
ownership before the existing `sudo` → `env -i` → `unshare` →
`setpriv --no-new-privs` → capability-drop boundary.

All privileged HAProxy workflow operations now invoke `/usr/bin/sudo` rather
than resolving `sudo` through an inherited `PATH`. This prevents a prior
checkout-controlled `GITHUB_ENV` write from intercepting namespace, privilege,
or evidence commands.

The fix creates no fallback, does not inherit host build-library variables,
and does not change receipt projection, verification, upload eligibility, or
failure behavior. A missing or unsafe root still fails closed.

### Evidence and validation

The local configure-only control used a fresh external Expat source copy and
the same bounded environment shape. `configure` failed when `TMPDIR` named a
missing directory and succeeded when that directory existed and was private;
no raw configure output was retained. The exact workflow source is covered by
a regression contract that requires the path validation, `0700` creation and
ownership check to occur before the privilege drop.

| Validation | Actual result |
| --- | --- |
| Expat configure-only missing-TMPDIR control | Failed, as expected. |
| Expat configure-only valid-private-TMPDIR control | Passed. |
| HAProxy workflow, evidence, harness, and CI-security contracts | Passed: 26 tests. |
| `actionlint` | Passed for `.github/workflows/test-connectors-with-crs-no-mrts.yml`. |
| `zizmor` | Passed for that workflow; it reported only its offline capability note. |
| `git diff --check` | Passed: no whitespace errors. |

### Changed files

- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `tests/test_haproxy_evidence_workflow_contract.py`
- this English/German Change Record pair

### Checks not run

`ruff` was not run because no local executable is available. An exact-head
hosted HAProxy runtime and evidence publication have not run for this repair
yet; therefore this record does not claim a hosted fix.

### Residual risk and status

The hardened execution and evidence boundary remains intact. Two independent
post-patch reviews found no concrete bypass or regression: one reviewed the
trusted-root, identity, namespace, and fail-closed boundary; the other verified
that all privileged calls use the absolute `/usr/bin/sudo` path. The patch is
ready for normal delivery to PR #344. `FND-PARENT-0975` remains open until an
exact-head hosted HAProxy runtime succeeds and its expected evidence is
verified.

## 2026-08-31 HAProxy evidence-projector staged-source repair

### Motivation and updated diagnosis

Hosted successor run `33372492366` proved the private-TMPDIR correction: its
HAProxy real-runtime step passed. The following scoped Git experiment was a
useful local ownership control, but hosted run `33376138121` at head
`6d7ed04c51169aec6d2785b5363d7a68ca566ffb` again passed the real runtime and
then failed only in `Project HAProxy runtime evidence`. The bounded evidence
shows no projector `FAIL:` classification before the secondary `head`
broken-pipe message. Therefore the evidence-UID Git loader still exited before
the pinned projector executed; a scoped `safe.directory` setting was not a
sufficient hosted repair.

### Technical decision

The evidence identity no longer reads the checkout or invokes Git. During the
trusted preparation step, the workflow resolves the projector blob from the
pinned Parent SHA with global and system Git configuration disabled, bounds it
to 128 KiB, and verifies its Git blob SHA-1. It writes the verified bytes to a
random exact `RUNNER_TEMP` staging parent, then seals the fixed
`verified-projector.py` capsule as a regular `root:root` `0444` file. The
parent is private until projection.

Both unprivileged projector invocations receive only the capsule path and the
expected blob ID. They use `O_NOFOLLOW`, verify canonical ancestor paths, a
regular single-link `root:root` `0444` source, the bounded size, stable
pre/post-descriptor identity, and the Git blob SHA-1 before `compile`/`exec`.
No `safe.directory` fallback, global Git configuration, or evidence-UID Git
read remains. The exact stage parent is cleaned on preparation failure by a
local trap and after upload by an HAProxy-only `always()` step; both paths
validate the literal random parent before deletion. A hard runner cancellation
can still prevent a later workflow step, which remains a hosted lifecycle
limitation rather than a fail-open path.

### Evidence and validation

The source-capsule contract failed before implementation and now requires the
sealed source, descriptor checks, absence of `safe.directory`, and explicit
cleanup. The focused projector, workflow-contract, harness, and CI-security
command passed 53 tests with 11 expected cross-identity skips. `actionlint`,
offline `zizmor`, and `git diff --check` also passed. A fresh independent
security review found no validated control regression in the new trust
boundary.

### Status

This successor is not yet an exact-head hosted success claim. Hosted run
`33381788663` at `4221526d91506adc246b422219a2537cf39702ff` passed both the
new preparation boundary and the HAProxy real-runtime step, but projection
still exited fail closed without an allowlisted source-loader classification;
the exact cleanup then passed. The next narrow successor adds only fixed,
payload-free source-capsule failure labels. `FND-PARENT-0998` remains in
progress until hosted runtime, projection, verification, upload, and artifact
inspection all succeed.

## 2026-08-31 HAProxy evidence-stage-root availability repair

### Motivation and root cause

Exact-head hosted run `33383672335` at
`e2f8c70f4800ac84bf9ffeb3d1c8b11ab8a8022a` passed the HAProxy preparation
boundary and real runtime, then failed only `Project HAProxy runtime evidence`.
The bounded payload-free classification was `evidence-source-capsule-open`.
Verification and upload skipped fail closed; exact cleanup passed. The
120,825-byte raw response had SHA-256
`3f878fc503d5b22bffe51c9e7fce461095e4437123ad12de832d959db0dd1a5d` and was
deleted from its exact task-owned directory after the local finding update.

The capsule itself was correctly root-owned, regular, single-linked, mode
`0444`, bounded, and SHA-verified. The failure was instead its ancestry:
`runner.temp` is not guaranteed to be traversable by the distinct
`EVIDENCE_UID`. The projector additionally requires the random stage parent to
be a direct child of its `--runner-temp` argument and root-owned mode `0755`.

### Technical decision

Only the random source-capsule parent moves to the literal
`TRUSTED_EVIDENCE_STAGE_ROOT` `/tmp`. Prepare, Project, Verify, and Cleanup
each require that exact value and reject a missing, linked, non-canonical, or
non-`root:root`-sticky-mode-`1777` root. Root creates the random child with
mode `0700`, seals `verified-projector.py` as `root:root` `0444`, then changes
the parent only to the pre-existing projector-required `0755` immediately
before unprivileged projection. The package remains
`EVIDENCE_UID:RUNTIME_GID:0700` and the existing projector still seals it to
`0550`.

Both projector operations now pass `/tmp` as `--runner-temp`, retaining the
helper's direct-child, descriptor-relative, `O_NOFOLLOW`, ownership, mode,
link-count, size, and SHA validation. Runtime, build, cache, source, and
receipt roots remain below the separately validated `runner.temp`; neither the
runtime command nor the upload allowlist changes. `/tmp` is acceptable here
because its sticky semantics protect the random root-owned child from
replacement, and the capsule contains only already public pinned projector
source, never a runtime receipt, payload, log, or secret.

### Evidence and validation

| Validation | Actual result |
| --- | --- |
| Focused HAProxy projector, workflow-contract, harness, and CI-security tests | Passed: 53 tests in 5.249 seconds; 11 expected cross-identity skips. |
| `actionlint .github/workflows/test-connectors-with-crs-no-mrts.yml` | Passed. |
| `zizmor --offline .github/workflows/test-connectors-with-crs-no-mrts.yml` | Passed: no findings. |
| `git diff --check` | Passed. |
| Fresh independent bypass/regression review | Passed: no concrete surviving bypass or regression found. |

### Status and residual risk

This change preserves the namespace, identity drop, source-capsule, fail-
closed verification/upload gate, and exact cleanup; it does not reset the
workflow to the less isolated master path. Exact code head
`6cac8ab83163d9728f03564a1444d38c8514a150` completed hosted workflow run
`33386995419` successfully at `2026-08-31T11:43:04Z`. HAProxy job
`99471747111` passed preparation, real runtime, projection, verification,
upload, and exact cleanup.

The published artifact
`with-crs-no-mrts-haproxy-33386995419-1` (GitHub artifact ID `9756326224`)
was inspected only through the bounded contract: its 807-byte receipt passed
the expected schema/result checks and the manifest matched receipt SHA-256
`79bf09bda36757f5625cec448553249a54e50bd7b6a688e8dd97f03029e24522` and
size. Apache, Envoy, Traefik, and lighttpd also passed in the same terminal
connector-runtime workflow. At the final observed PR state, all displayed
non-skipped PR checks, including SonarCloud Code Analysis, passed.

`FND-PARENT-0998` is therefore fixed on the PR head. A hard runner
cancellation can still prevent a later `always()` cleanup step; this remains
a hosted lifecycle limitation rather than a fail-open path. The finding policy
requires an authorized post-merge current-master reproduction before that
finding can become verified or closed. This record changes no master state,
CI protection, ruleset, required check, scanner, Quality Gate, or evidence
boundary.

## 2026-08-31 Logical-profile documentation reconciliation

### Motivation and root cause

The shared transaction contract, the source-backed example matrix, and the
capability manifests identify ten logical connector profiles. Connector
navigation documentation nevertheless described six host-family routes as six
selected routes, which could be read as a complete logical-profile inventory.
The lighttpd manifest likewise named its current patched lifecycle target
without restating that the canonical Stock profile is the traffic-owning
sidecar.

### Technical decision

The six host-family rows are now explicitly navigation only, and their
English/German connector guides contain a ten-profile inventory. Direct host
routes and their separate HAProxy SPOE/SPOP, Envoy ext_authz, and Traefik
forwardAuth composite profiles remain evidence-distinct. The lighttpd text and
capability constraint now distinguish canonical `lighttpd-stock` /
`stock-lighttpd-sidecar`, separate `lighttpd-patched`, and the noncanonical
native Stock P1/P3 translation.

No host code, workflow, source-phase contract, runtime result, protection
configuration, event schema, or safety limit changed. This is a claim
reconciliation only; it does not promote host-runtime evidence for a composite
or sidecar profile.

### Evidence and validation

| Validation | Actual result |
| --- | --- |
| Focused logical-connector examples | `python3 -m unittest -v tests.test_logical_connector_all_examples` passed 11 tests in 0.653 seconds. |
| Logical examples, matrix, capabilities, and bilingual documentation | `python3 -m unittest -v tests.test_logical_connector_all_examples tests.test_logical_connector_example_matrix tests.test_connector_capabilities tests.test_bilingual_docs` passed 52 tests in 2.730 seconds. |
| Source-backed logical-profile matrix | `python3 ci/checks/documentation/check-logical-connector-example-matrix.py` passed with 10 profiles and 30 variants. |
| Documentation and capability checks | `make check-bilingual-docs`, `make check-doc-links`, and `python3 ci/evidence/collectors/connector_capabilities.py check` passed. |
| Whitespace/error scan | `git diff --check` passed. |

### Status and residual risk

The new regression test prevents the connector navigation guides from again
presenting six host integrations as the complete set of logical profiles and
checks the canonical lighttpd Stock-sidecar identity. The six host-family
runtime targets remain navigation and bounded-evidence targets; this record is
not a claim that all ten profiles have equivalent native-host runtime evidence.
Final exact-head PR validation, hosted checks, SonarCloud metrics, and fresh
reviews are still required before merge.

## 2026-08-31 Native intervention normalization and SPOP correlation repair

### Motivation and scope

A fresh source-to-sink security review identified two independently remediable
boundaries. Apache and NGINX could record a Common terminal rule action while
handing a raw native intervention status to the host. Separately, HAProxy SPOP
copied a length-delimited `request_id` into a C string before validation, so
byte-distinct values such as `A\0X` and `A` could address one cache key.

This addendum changes only the Common/native-intervention boundary, direct
Apache/NGINX/HAProxy adapter wiring, focused tests, paired documentation, and
this record. The C-standard source-list updates make the newly linked Common
source visible to existing local checks; no workflow, scanner, quality gate,
ruleset, required check, `paths.env`, Framework, MRTS, or Gitlink changed.

### Technical decision

`msconnector_intervention_normalize_status()` now centralizes the existing
Common Runtime rule-decision mapping: a nonempty URL preserves a valid 3xx
status or becomes `302`; without a URL, only an allowed block status is kept
and every other value uses an allowed `default_block_status`, otherwise `403`.
Common Runtime, Apache, and NGINX call it before retaining status, recording a
contract decision, writing event metadata, or using a host sink. This remains
distinct from the Common `invalid_engine_response` error policy.

HAProxy SPOP validates exact-length `request_id` bytes with the canonical
transaction-ID validator before any C-string copy. Empty, embedded-NUL,
control-byte, non-ASCII, and overlong values fail notification extraction and
cannot create, replace, or claim a transaction-cache entry; printable-ASCII
UUIDs remain accepted.

### Evidence and validation

| Validation | Actual result |
| --- | --- |
| Focused diagnostics, Apache/NGINX source-contract, HAProxy combined-harness, and bilingual-doc tests | Passed: 63 tests with `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v`. |
| HAProxy transaction-ID binding regression | `PYTHONDONTWRITEBYTECODE=1 python3 -B tests/test_haproxy_transaction_contract_binding.py` passed. |
| Direct Common normalizer unit | C17 `-Wall -Wextra -Werror` compile and execution of `tests/intervention_normalization_test.c` passed. |
| Common helper and connector source wiring | `make check-common-helpers-c17`, all Apache/NGINX/HAProxy C-standard wiring checks, and shell syntax checks passed. |
| Connector C17 compilation | Apache and HAProxy passed. NGINX was correctly blocked/skipped because this environment lacks NGINX headers/source. |
| Independent bypass/regression review | Found no remaining host-visible-success or arbitrary-3xx bypass and confirmed that `A\0X` cannot collapse to `A`. |

### Limits and residual risk

`make check-apache-common-adoption` remains failed on four pre-existing
`msc_filters.c`/`msc_utils.c` structural expectations. Those files are
byte-identical to pre-repair candidate
`297330cf91ab65af4958dd75d12e1b9e1862d235`; this repair neither weakens nor
changes that unrelated control.

The bypass review also confirmed a pre-existing fail-closed NGINX edge: a
redirect URL containing CR/LF returns HTTP `400` without installing `Location`,
but the earlier contract/event classification remains `redirect`. It is not a
header-injection or success bypass. A separately scoped rule-generated URL
test and host-policy decision are required before changing that error mapping;
it is retained in `FND-PARENT-0999` rather than silently recast here.

The two new local findings are `fixed`, not `verified`, until an exact
successor PR head completes native/hosted validation. The repository finding
catalog remains intentionally unsynchronized under `FND-PARENT-0996`; no
broad catalog repair is claimed. Prior hosted, SonarCloud, and review evidence
becomes stale after normal successor delivery.

## 2026-09-01 Redirect preservation and native P2 body-limit parity repair

### Motivation and scope

A fresh PR #344 review found that the shared HTTP authorization service could
return a redirect status after discarding the rule-owned target, so it emitted
no `Location` header. The same review cycle found that the direct Apache,
NGINX, and HAProxy native adapters did not share Common Runtime's exact
`SecRequestBodyLimitAction Reject` P2 translation. They could treat the valid,
rule-ID-free native result as an invalid generic intervention; HAProxy's
legacy SPOP sink also recognized only disruptive HTTP 403 decisions.

This focused Parent-only repair changes the Common intervention/auth-service
boundary, direct Apache/NGINX/HAProxy translation, focused regression tests,
the HAProxy source README pair, Envoy/Traefik capability claims, and this
paired Change Record. It changes no `.github/` workflow, ruleset, required
check, scanner, Quality Gate, `paths.env`, Framework, MRTS, Gitlink, or
HTTP/2/HTTP/3 host-model claim.

### Technical decision

The authorization service copies a redirect target into response-owned,
1024-byte bounded storage before native transaction cleanup. It accepts only
nonempty, NUL-terminated targets without C0/DEL bytes or leading/trailing
space and emits exactly one generated `location` header for a 3xx response.
An empty, control-bearing, overlong, inconsistent, or native-truncated target
becomes the configured runtime-error response without `Location`; it is never
silently truncated or retained after transaction destruction.

`msconnector_intervention_is_request_body_limit_rejection()` is the shared,
exact P2 classifier: disruptive, HTTP 403, no redirect URL, and
`Request body limit is marked to reject the request`. Common Runtime and each
direct native adapter classify it before ordinary status normalization or
rule-ID correlation. Only that signature records the canonical rule-ID-free
`BODY_LIMIT` terminal outcome and a 413 deny; every other missing-rule-ID
intervention remains fail closed. HAProxy keeps the marker through its decision
structure so the legacy SPOP ACK sets `txn.blocked=true` for this exact
body-limit result without broadly accepting arbitrary HTTP 413 decisions.

### Evidence and validation

| Validation | Actual result |
| --- | --- |
| Shared authorization-service redirect regression | The new P1/P2 valid-redirect, cleanup-lifetime, deny/allow, empty, overlong, and CR/LF cases first exposed the missing `Location`; `BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/verified/pr344-final-closure-20260828/build make check-http-authorization-service-timeout` then passed. |
| Common and focused adapter contracts | `make check-common-helpers` passed; `python3 -m unittest -v tests.test_modsecurity_request_body_limit_status_contract tests.test_native_request_body_limit_adapter_contract tests.test_apache_intervention_cleanup tests.test_nginx_upstream_security_contract` passed 30 tests. |
| Native HAProxy P2 proof | `make -C connectors/haproxy self-test-modsecurity-binding` passed. Its new `SecRequestBodyLimit 8` / `SecRequestBodyLimitAction Reject` request obtains a disruptive, rule-ID-free P2 413 deny through the real libmodsecurity binding. The optional rule-ID API probe is unavailable with the selected libmodsecurity 3.0.14 headers, but the supported baseline self-test passed. |
| C17 connector checks | `make check-apache-c17` and `make check-haproxy-c17` passed. `make check-nginx-c17` is environment-blocked because NGINX headers/source are unavailable. |
| Composite adoption and manifests | `make check-envoy-common-adoption check-traefik-common-adoption` and `jq empty connectors/envoy/capabilities.json connectors/traefik/capabilities.json` passed. |
| Diff and independent security review | `git diff --check` passed. A fresh read-only bypass/regression review found no concrete bypass or legitimate regression. |

### Limits, risk, and delivery status

The NGINX native C17 compile remains blocked by the local host prerequisite,
not by a source diagnostic. The new local evidence does not replace the
required exact-successor PR hosted matrix, SonarQube Cloud analysis, Secret
Scanning, CodeQL, or fresh regular and Security Codex reviews. No merge,
direct `master` push, admin bypass, or scanner/Quality-Gate weakening is
claimed by this addendum. The known H2/H3 and host-model limitations remain
unchanged.
