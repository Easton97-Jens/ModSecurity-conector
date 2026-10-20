# Body-inspection review matrix

**Language:** English | [Deutsch](body-inspection-review-matrix.de.md)

This matrix belongs to [PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407), stacked on #382. I09/#408 and I11/#406 are integrated into the reviewed base; I10/#409 and the full I12/#410 / V08–V10 host acceptance remain separate. Source wiring, executable contracts, selected hosted probes and full protocol acceptance are different evidence layers. No row claims a completed full I12 matrix.

## Request and response routes

All streaming rows describe the available data path, not unbounded host delivery or completed HTTP/1–HTTP/3 acceptance. Every direction uses explicit native inspection directives in its inspection fixtures.

| Profile | Request path and scope | Response path and scope | Review evidence and remaining host work |
| --- | --- | --- | --- |
| Apache native | Native request ingestion offers memory/file chunks to P2, with checked counters and file access. | `connectors/apache/src/msc_filters.c` offers APR brigades; native Reject terminates at append and survives EOS. After commitment it seals output and aborts the actual connection before forwarding the rejected brigade. | Genuine libModSecurity/APR regression: 9 tests, exit 0; strict C17 exit 0. Real httpd/protocol/commit matrix remains not_run; APR caller evidence is not a hosted httpd run. |
| NGINX native | `connectors/nginx/src/ngx_http_modsecurity_access.c` processes memory/file input incrementally with descriptor/range checks. | Native body filter preserves native results and once-only P4 at EOS; native body-limit terminal handling differs from ordinary Safe late-rule handling. | Source/contract review; fresh complete hosted memory/file and late-abort matrix not_run. |
| HAProxy native HTX | Borrowed HTX blocks reach native P2; no SPOP full-sample ceiling applies. | Native HTX response blocks and EOS reach P4; shared terminal decisions govern commitment. | Selected real combined HTX/SPOP companion run passed. Full HTX request/response/protocol/Strict matrix not_run. |
| HAProxy SPOE/SPOP + response companion | One complete, frame-representable request sample. Producers send `req.body_size` and `http_version=req.ver`; typed totals, explicit framing and sample length must agree before P2. | Separate native HTX companion supplies the actual response stream; SPOP response-header notifications alone provide no response body. | Real HAProxy 3.2.25 combined harness and 28 host assertions passed, including On/DetectionOnly, large incomplete samples and small controls. Unknown/chunked framing and unframed HTTP/2 remain unsupported (category 4); native HTX is the full-stream alternative. |
| Envoy ext_proc | Streamed body messages reach Common bridge P2; message capacity is per message. | Streamed response messages and EOS reach P4; no cumulative connector budget. | Source/contracts and eight-package genuine CGo/native execution passed. Complete ext_proc host/protocol/late-commit matrix not_run. |
| Envoy ext_authz + observer | Host buffers a complete authorization sample; `max_request_bytes=4096/33` remains category 3. Partial/ambiguous metadata is rejected before native transaction/lease creation. | Independent response observer supplies MRC1 response chunks and EOS to Common. | Retained Envoy 1.39.1 HTTP/1 subset: 14 cases and 14 terminal cleanups; nine verifier cases LIFECYCLE_ONLY and p4_strict NOT_RUN. Host 413 with zero native events is distinct from native 403 for a complete sample above the engine limit. Full matrix not_run. |
| Traefik native UDS middleware | Native middleware and engine UDS protocol offer incremental request chunks to P2. | Incremental application response chunks and EOS go through the UDS engine path. | Go/vet, C selftest, protocol-runtime and seven API contracts passed; genuine Common/UDS tests cover engine delivery beyond former limits. Full Traefik host/protocol/commit matrix not_run. |
| Traefik forwardAuth + observer | Host full-buffer authorization request, `maxBodySize=4096/33` (category 3); response observer cannot make request input streaming. | Observer supplies the application response independently of the authorization reply. `maxResponseBodySize=32768` protects only the latter. | Source/contract review; current full Traefik authorization/observer host matrix not_run. Host sample rejection is not native engine-limit evidence. |
| lighttpd Stock sidecar | Incremental HTTP input/native P2; private disk spool with bounded RAM, replay only after native allow. | Incremental upstream input/native P4 with technical-error/no-replay terminal behavior. | 37 executed tests: 36 passed, one baseline RST delivery failure (FU-STOCK-RST-DELIVERY), zero skips. Full host matrix and foreign-UID/read-only-mount probes not_run/blocked. |
| lighttpd patched native | Validated native memory/file chunks offered incrementally to P2. | Native response chunks/EOS offered to P4; descriptor/range/scratch checks remain. | Source/contract review; complete freshly built patched-host/protocol/commit matrix not_run. |

## Decision, completion and safety contract

Common records actual append results and native interventions, completes P2/P4 once, preserves the first technical error and rejects re-entry after terminal failure. For requests, `bytes_seen` counts offered bytes and `bytes_retained` records the SDK-owned prefix. Request `bytes_inspected` remains zero, meaning unknown/unproven, because retention and successful P2/EOS do not prove body inspection: even `SecRequestBodyAccess Off` can retain the body. Inspection claims need independent source/runtime evidence. Native append `0` establishes ProcessPartial telemetry; a retained-length mismatch alone does not. For responses, `bytes_inspected` still counts bytes offered, not the engine's ProcessPartial prefix. Reject/ProcessPartial and DetectionOnly follow libModSecurity; the connector neither infers limits from rules nor injects directives or chooses a prefix. Off/Safe/Strict are host response-handling modes. Apache native body-limit Reject must not be downgraded to ordinary Safe late-rule log_only.

DetectionOnly is not an assertion that response Reject becomes ProcessPartial:
the native engine can discard an overrunning append without a disruptive result.
Tests must distinguish offered bytes, actual inspected content and intervention
outcome. Native terminal phase finalization before HTTP EOS must record EOS only
when the host actually supplied it.

Pointer/overflow/file-range/descriptor checks, individual frames/messages, metadata/event/header bounds, timeouts and correlation cleanup remain technical safeguards. Reused 16/32-KiB work buffers and MRC1 32-KiB chunks/64-KiB frames are category 2, not total-body budgets. Stock spool files are exclusive, effective-UID-owned 0600 regular files immediately unlinked inside a canonical private 0700 directory. Pinned descriptors, ancestor checks, bounded read/write loops and error cleanup remain; no public/TMPDIR fallback or unlimited full-body RAM allocation is introduced. Root-only UID maps, foreign-UID chown EINVAL and namespace EPERM block the adversarial deployment probes here.

## Classification of the four remaining limits

| Limit | Category | Actual effect and disposition |
| --- | --- | --- |
| SecRequestBodyLimit / SecRequestBodyNoFilesLimit / SecRequestBodyLimitAction; SecResponseBodyLimit / SecResponseBodyLimitAction | 1 | Native engine inspection policy; omitted values retain native behavior. |
| Envoy ext_authz max_request_bytes | 3; full-stream use case remains 4 | Host complete-sample ceiling; use ext_proc for full request streaming. |
| Traefik forwardAuth maxBodySize | 3; full-stream use case remains 4 | Host full-request buffer ceiling; use native UDS middleware for streaming. |
| Traefik maxResponseBodySize=32768 | 2, configured by host (3) | Retained authorization-response memory protection; application response inspection remains native. |
| HAProxy SPOE/SPOP individual frame/message | 2; unsupported framing/full streaming remains 4 | Bounded complete sample only; fail before engine on incomplete or contradictory metadata. Never label category 4 fully implemented. |

Traefik 3.7.10 `readResponseBodyBytes` allocates `maxResponseBodySize+1` and uses `io.ReadFull`; an omitted/negative limit uses `io.ReadAll`. The retained 32768 bounds this authorization buffer to 32769 bytes. Request authorization also buffers. Oversized authorization input/reply yields host 401 in this pin, not a native inspection outcome. [Pinned Traefik source](https://raw.githubusercontent.com/traefik/traefik/v3.7.10/pkg/middlewares/auth/forward.go).

Independent host controls, including lighttpd `server.max-request-size`, remain category 3. No route claims that all HTTP bodies automatically reach the engine in full.

## Executed evidence and independent follow-ups

Current acceptance evidence is retained under run `pr407-review-ready-20261012`. Genuine Common native tests passed 13 methods/207 scenarios, exit 0. Restoring the former 1-MiB response threshold only in an external test build caused the existing real marker fixture to fail at assertion 407, exit 1; compilation passed and the unmutated suite passed. This negative control detects a resurrected connector policy.

The genuine suite covers request/response below, at and above explicit engine
limits, Reject/ProcessPartial, DetectionOnly, multiple chunks, files, bodies and
markers beyond former limits, and the same payload under different engine limits.
Request adapters preserve the raw native status, including actual 403; obsolete
test expectations of connector-remapped 413 are corrected without a product remap.

Apache early native Reject versus actual HTTP EOS was independently reproduced: three pre-fix cases failed, then the nine genuine libModSecurity/APR tests passed, exit 0, with strict C17 exit 0. Native terminal finalization does not invent received HTTP EOS. Every limit/action helper argument is explicit. Independent review reported no new unresolved blocker; broad host/deployment acceptance remains separate.

Fresh SPOP evidence: 64 tests, zero skips, exit 0; strict C17/runtime selftest, five pinned HAProxy 3.2.25 configuration checks and both shell syntax checks exit 0. The integrated real host harness passed, exit 0, with 28 assertions against the unchanged runtime source. The superseded fixture extraction failure was repaired without weakening assertions.

Envoy passed all eight distinct Go packages twice, including genuine CGo/native tests, exit 0; four focused tests plus four subcases cover the marker beyond 1 MiB/native 451, first technical cause and physical sink. Traefik Go tests/vet and C selftest passed, exit 0; seven API source contracts passed, exit 0. Corrected protocol runtime tests passed on both current and base production, exit 0, including oversized-frame terminal STATE2/EOF/no-reentry, invalid OUTCOME, Safe/EOS/P3/P4 controls, independent peers, 64 slow peers and socket cleanup.

Stock ran 37 tests: 36 passed, one unchanged baseline RST failure, zero skips. Private-spool, large-replay and safety cases passed; this is not a passing aggregate suite. Three foreign-UID setup probes remain environment-blocked by chown EINVAL/root-only UID maps; they are not waived or renamed passing. All 21 generated outputs are current. The final local quick-check used the pinned Parent CPython 3.14.7 with existing PyYAML 6.0.3 and passed 304 reported tests, exit 0. The combined Common/native/adapter suite passed 69 methods, exit 0. Broad Apache discovery ran 237 tests: 234 passed and three foreign-UID setup errors remained blocked, aggregate exit 1. These results establish their layers, not future final-head CI/Sonar/secret-scan success or full I12 coverage.

| Follow-up / owner | Exact baseline comparison | Required work |
| --- | --- | --- |
| FU-COMMON-LOSSY-CONTRACT / Common tests | Current legacy test exits 134 at lossy assertion 209. Exact base legacy test exits 134 earlier at config assertion 366 because it still uses removed options. The unchanged valid current fixture against immutable base production also fails at 209. UTF8 serializer smoke passes both. | Reconcile lossless invalid-byte escaping with actual lossy/truncated classification; update obsolete fixture configuration. Keep overflow/chaining assertions. |
| FU-STOCK-RST-DELIVERY / Stock + Common runtime | Exact RST test exits 1 on both current and immutable base with an empty event log. Staged header/body delivery still exits 1 on both: P2 rule block appears but technical delivery-error event is absent. | Add deterministic admission barrier and truthful technical delivery-failure event; do not invent an abort or weaken assertions. |

These IDs are durable follow-up references, not claims that GitHub issues were created. Baseline production was compared with base `2619b20b9d2e70fa07cbe71f664b48ff3c105380`. The possible request-only SPOP logging/phase-completion baseline issue has source evidence only; the accepted completeness host probe uses the actual response companion.

## Review versus merge evidence

An exact-head Sonar readback exposed one `c:S3776` issue in SPOP
`parse_headers_text` (complexity 26, threshold 25), despite Quality Gate OK.
The stricter zero-new-issue acceptance therefore required a repair. Extracting
`parse_header_text_line` preserves statement behavior, framing/length checks and
complete header terminators; independent review found no new security finding.
After extraction, the broad 64-test SPOP suite, genuine combined HAProxy/HTX
harness and 28 integrated host assertions passed again, exit 0. Fresh final-head
CI/Sonar readback remains mandatory; the earlier Quality Gate is not that proof.

The focused reliability-boundary test compiles the productive parser translation
unit with actual `error.c` and the checked event producer. Stale I09/I11 mocks were
aligned with those contracts, retaining assertions and adding malformed BOOL,
incomplete-sample and mismatched-header controls; the focused test passed, exit 0.
Its lower JSON writer remains stubbed, so this proves parser/checked-producer
behavior, not physical event-sink delivery. After correcting the Traefik fixture
to the actual `begin_request_stream` API, the complete reliability module passed
15 tests, exit 0, in 7.936 seconds. Assertions remain intact, with stronger
`lock < stream_begin < unlock` ordering. Independent final diff review found no
scoped blocker. The runtime helper remained unchanged during the fixture repair;
fresh final-head CI/Sonar readback remains separate.

Final-head quick checks, affected regressions/builds/generators/docs, a sensitive former-limit mutation control, an independent redacted secret scan and exact-head CI/Sonar readback are mandatory before Ready. Zero new open/accepted issues, hotspots and duplication must be observed without exemptions. Sonar without measured coverage proves no executable test coverage. The complete I12/V08–V10 matrix and blocked deployment probes remain separate from review readiness. Read actual delivery state from [PR checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407/checks), not an old source-document SHA. See the [stack checklist](response-limit-stack-checklist.md).

The independent redacted whole-worktree Gitleaks scan returned exit 1 for 47 candidates. Read-only classification established 44 cache hashes, one public Action commit SHA, one report identifier and one audit prose match, all unchanged against the immutable base and prior head. No scanner exclusion, suppression or risk acceptance was added. This does not convert the tree scan into a pass; final commit-range scanning has its own proof.
