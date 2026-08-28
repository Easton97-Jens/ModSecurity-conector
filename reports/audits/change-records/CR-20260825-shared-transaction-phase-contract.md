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
| Scope | Parent repository only: the shared P1--P4 transaction contract, ten connector mappings, bounded response companions, Stock-lighttpd sidecar, tests, English/German documentation, and this paired Change Record. No Framework, MRTS, Gitlink, workflow, ruleset, branch-protection, or required-check change. |

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
`configured_not_exercised`. No CI file was changed and no risk acceptance is
claimed.

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
| `git diff --check` and the scoped `.github`/`ci` diff check | Passed; no CI/governance file is in this task diff. |
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
- No CI workflow, ruleset, required-check, or CI collector modification was
  made because the user explicitly excluded CI from the implementation scope.
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
