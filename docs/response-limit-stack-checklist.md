# Request/response body-limit stack checklist

**Language:** English | [Deutsch](response-limit-stack-checklist.de.md)

## Stack identity

Existing [Draft PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
remains stacked on [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).
Branch: `fix/engine-owned-response-limits-stack-20261011`.
Base branch: `fix/unified-native-results-events-20260921`.
Exact base: `2619b20b9d2e70fa07cbe71f664b48ff3c105380`.
Expanded-task starting head: `6576661724841e26802a93b19d8bbfbdb5c8235a`.
No new PR or PR/master merge. The user authorized regular base merges from #382
into the existing #407 branch; published history is retained. Delivery is pending
at this documentation snapshot.

## Implementation

- [x] Trace Common and all ten logical direct/companion/middleware/sidecar profiles.
- [x] Remove Common request/response body policy fields, defaults, merge/parser logic and connector `body_limit_action`; remove adapter/service policy consumers.
- [x] Use native request and response directives; no connector-injected limits, rule-text inference, chosen Reject/ProcessPartial or cumulative truncation.
- [x] Retain native append interventions/results through EOS and phase completion, including actual DetectionOnly semantics.
- [x] Replace socket full-body allocation and stock-sidecar fallback with incremental processing/private spooling; retain technical safeguards.
- [x] Reject removed options and update examples, generator and EN/DE references.
- [ ] Eliminate all active profile total-body constraints: the concrete authorization limitations below remain.

## Current executable evidence

Earlier component passes below retain their revision scope. The base
reconciliation section separately records the passing current I11 aggregate.

- [x] Genuine request/response below/equal/above, actions, chunks/files, varied limits, DetectionOnly and markers beyond former connector ceilings.
- [x] Real 2 MiB authorization-socket lifecycle and no duplicate prefix.
- [x] Selected component builds, contracts, safety/configuration and documentation checks.
- [x] Terminal full `quick-check` and native I09 reconciliation on the recorded I09 base.
- [x] Affected/full validation on the final merged I11 base.
- [ ] Current changed-head CI/Sonar: zero new issues, hotspots and duplication.

Earlier expanded-task Common real-library validation passed nine methods: 112 native request
and 81 response scenarios (193 total). A later combined run passed 30 tests.
Four real authorization-socket cases use a 2 MiB body: a tail marker produces
native 451 under a high limit, the same payload under a low ProcessPartial limit
produces 200, low Reject produces native 403, and a marker-free body is allowed.
The callback completes P2 before handoff without offering a prefix twice.

Common helper/SDK/security/memory/flow/adapter/directive checks passed. Seven
configuration-reference tests passed; all 21 generated files are current.
EN/DE, path/link checks and 22 compiler-guide tests passed. Apache C17 passed;
HAProxy binding/self-test/SPOP C builds and 104 tests with 119 subtests passed,
with the final genuine request/response suite passing 13 methods in 13.62 seconds. Envoy passed eight Go
packages and its real CGo build. Traefik Go/C builds and socket-protocol self-tests
passed. lighttpd C build, 15 gate tests and two isolated Envoy tests passed.
Stock-sidecar validation passed 35/36; its unchanged RST empty-event base defect
remains open. The Common legacy lossy-event assertion remains a baseline failure. The two old
SPOP source assertions pass after integrating the upstream I09 fixes. Assertions
are preserved.

The terminal native `make quick-check` passed (exit 0): ten unittest groups
with 302 tests plus lint, contracts, security, memory, documentation, generated
references, helpers, actionlint and diff checks.

Final Common native validation passed 13 methods and 168 subtests in 14.34
seconds (`root-checks/final-common-native.log`), including the four HTTP cases.
HAProxy's genuine suite passed 13 methods in 13.62 seconds; Response DetectionOnly
preserved the actual native 65536-byte prefix for a 120000-byte body in four
chunks: Reject append results `[1,1,1,1]`, ProcessPartial `[1,1,0,0]`, EOS `1`.
Seven configuration-reference tests passed, including strict removed-key tombstone
mutations. All NGINX adoption/mutation checks passed. A combined four-file sweep
passed 145 tests and 163 subtests with two stale Apache planner expectations;
after correcting those expectations, all six Apache checks passed and preserve
native append `0`/`1` continuation and exact EOS `1` guards. Independent review
identified case-alias/JSON-null removed-key acceptance; EqualFold matching and
24 negative cases now pass with the entire Traefik Go suite. Seven additional
Traefik forwardAuth tests passed. No review finding remains open.

Current changed-head CI/Sonar and zero-new-code
issues/hotspots/duplication verification are pending; live results are linked in
[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407).

## Active cumulative/sample limitations

Full removal across all active profiles is not claimed.

| Active route | Remaining limit and actual scope |
| --- | --- |
| Envoy ext_authz | Host `max_request_bytes=4096/33` bounds the complete request sample sent to authorization; its response observer does not make request ingestion incremental. |
| Traefik forwardAuth | Host `maxBodySize=4096/33` bounds the buffered authorization request. |
| Composite Traefik authorization response | Host `maxResponseBodySize=32768` bounds the authorization response, not the upstream application response. |
| HAProxy SPOE/SPOP | One request sample per bounded protocol message/frame; incomplete-sample admission fails with 503 before the engine, not native `BODY_LIMIT`. Native HTX is separate. |

## Technical safety

Incremental HTTP work buffers are 16 KiB; file-read scratch is 32 KiB.
MRC1 retains individual 64 KiB frames and 32 KiB body chunks. Counters retain
their integer representation (`SIZE_MAX`, or `INT64_MAX` for signed counters/file
offsets); overflow ends as a technical failure without engine append/truncation. Pointer/integer
checks, descriptors/file ranges, message controls, header/event metadata and
timeouts remain. Stock lighttpd uses private unlinked spooling with bounded RAM
and withholds upstream replay until native P2 allows it; disk failures remain
technical failures. The legacy full-body fallback is removed. These controls
are scoped operations/storage safeguards, not replacement inspection limits.

## Missing current host evidence

No complete current ten-profile request/response hosted matrix exists. Engine,
socket and component evidence does not prove host buffer ownership, HTTP/1/2/3
lifecycles, commit timing or late-abort behavior.

- [ ] Apache native.
- [ ] NGINX native, including memory/file buffers.
- [ ] HAProxy native HTX.
- [ ] HAProxy SPOE/SPOP with native-HTX response companion.
- [ ] Envoy ext_proc.
- [ ] Envoy ext_authz with response observer.
- [ ] Traefik native UDS middleware.
- [ ] Traefik forwardAuth with response observer.
- [ ] lighttpd Stock sidecar.
- [ ] lighttpd patched native.

## Current base reconciliation

The selected current #382 base is `2619b20b9d2e70fa07cbe71f664b48ff3c105380` (I11).
The ordinary I09 integration is committed as `2bb1a1e0`; authorized ordinary
I11 base integration is locally complete and source is frozen. Published history
is retained; no PR/master merge or force-push is performed.

On integrated I09 base `492663334d89428dce084792145ef94e91579788`, `check-i09-native-routes`
passed 33 tests and native `make quick-check` passed with exit 0, including ten
unittest groups totaling 302 tests (`root-checks/resume-base492-check.log`).
The old SPOP source assertions pass with upstream I09 fixes. Earlier Common
reconciliation passed 30 focused tests including 13 genuine engine tests;
Traefik Go packages, I09 lighttpd/Traefik tests and both C builds passed.
Stock-sidecar remains 35/36 due to unchanged RST empty-event behavior; rebuilt
Common legacy lossy-event validation exits 134 at assertion 209. Assertions are
retained.

On selected I11 base `2619b20b9d2e70fa07cbe71f664b48ff3c105380`,
final native selection passed 20 modules with 212 tests and 201 subtests in
58.51 seconds, including 13 genuine engine methods. Apache C17, APR/LTO cleanup
and adoption checks passed, as did genuine HAProxy binding/build/self-test/SPOP
protocol checks. Additional real APR-bucket and production-append regressions
for P2/P4 passed 20 methods and ten subtests: native pending 403 through EOS,
and sticky `/dev/full` IO failure with 500 and no replay. Independent review
found no finding. All eight Envoy packages passed pure Go and real
CGo/libModSecurity validation, and its binary built. Evidence:
`native/base261/validation-status.json` and `remaining/base261/validation.md`.

The final aggregate native Make run on I11 passed with exit 0:
`check-i09-native-routes` with 33 tests, `check-apache-event-sink` with 20 tests,
`check-haproxy-spop-event-sink` with 19 tests and `quick-check` with ten unittest
groups and 304 tests. Security/memory/flow/helper/documentation checks,
21 generated files and diff checks passed. Actual Apache, NGINX and HAProxy
C17 compilation passed; earlier local compilation evidence gaps are closed,
while hosted matrix evidence remains missing. Evidence:
`root-checks/base261-final-make.log`. The additional combined NGINX adoption/
bounded-URI/Envoy-bridge run passed 130 tests in 694.670 seconds
(`root-checks/base261-root-targeted.log`). Final targeted inventory, including
hidden files in Common, all connectors and examples, found no additional active
own cumulative body cap, directive injection or fallback beyond the disclosed
authorization/sample constraints; no hidden plugin manifest contains a retired
key. Independent P2/P4 EOS and sticky-IO review found no finding. Push/readback and current-head CI/Sonar remain pending; the remote
#407 head is still `6576661724841e26802a93b19d8bbfbdb5c8235a`.

## Historical evidence boundary

Earlier response-only checks and completed Sonar results, including the starting
head, establish only those revisions. They do not verify the expanded current
diff. See the [ownership contract](phase4-mode-budget.md) and
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.md).
