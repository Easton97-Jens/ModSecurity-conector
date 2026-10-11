# Request/response body-limit stack checklist

**Language:** English | [Deutsch](response-limit-stack-checklist.de.md)

## Stack identity

Existing [Draft PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
remains stacked on [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).
Branch: `fix/engine-owned-response-limits-stack-20261011`.
Base branch: `fix/unified-native-results-events-20260921`.
Exact base: `498653c2a193d34b7b25b2903b1e4db1c45e7f73`.
Expanded-task starting head: `6576661724841e26802a93b19d8bbfbdb5c8235a`.
No new PR or merge; expanded changes have not yet been pushed at this snapshot.

## Implementation

- [x] Trace Common and all ten logical direct/companion/middleware/sidecar profiles.
- [x] Remove Common request/response body policy fields, defaults, merge/parser logic and connector `body_limit_action`; remove adapter/service policy consumers.
- [x] Use native request and response directives; no connector-injected limits, rule-text inference, chosen Reject/ProcessPartial or cumulative truncation.
- [x] Retain native append interventions/results through EOS and phase completion, including actual DetectionOnly semantics.
- [x] Replace socket full-body allocation and stock-sidecar fallback with incremental processing/private spooling; retain technical safeguards.
- [x] Reject removed options and update examples, generator and EN/DE references.
- [ ] Eliminate all active profile total-body constraints: the concrete authorization limitations below remain.

## Current executable evidence

- [x] Genuine request/response below/equal/above, actions, chunks/files, varied limits, DetectionOnly and markers beyond former connector ceilings.
- [x] Real 2 MiB authorization-socket lifecycle and no duplicate prefix.
- [x] Selected component builds, contracts, safety/configuration and documentation checks.
- [x] Terminal full `quick-check` and final native test reconciliation.
- [ ] Current changed-head CI/Sonar: zero new issues, hotspots and duplication.

Current Common real-library validation passed nine methods: 112 native request
and 81 response scenarios (193 total). A later combined run passed 30 tests.
Four real authorization-socket cases use a 2 MiB body: a tail marker produces
native 451 under a high limit, the same payload under a low ProcessPartial limit
produces 200, low Reject produces native 403, and a marker-free body is allowed.
The callback completes P2 before handoff without offering a prefix twice.

Common helper/SDK/security/memory/flow/adapter/directive checks passed. Six
configuration-reference tests passed; all 21 generated files are current.
EN/DE, path/link checks and 22 compiler-guide tests passed. Apache C17 passed;
HAProxy binding/self-test/SPOP C builds and 104 tests with 119 subtests passed,
with the final genuine request/response suite passing 13 methods in 13.62 seconds. Envoy passed eight Go
packages and its real CGo build. Traefik Go/C builds and socket-protocol self-tests
passed. lighttpd C build, 15 gate tests and two isolated Envoy tests passed.
Stock-sidecar validation passed 35/36; its unchanged RST empty-event base defect
remains open. The Common legacy lossy-event assertion and two old SPOP source
assertions also remain unchanged base failures; assertions are preserved.

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
MRC1 retains individual 64 KiB frames and 32 KiB body chunks. Pointer/integer
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

## Historical evidence boundary

Earlier response-only checks and completed Sonar results, including the starting
head, establish only those revisions. They do not verify the expanded current
diff. See the [ownership contract](phase4-mode-budget.md) and
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.md).
