# Change Record: CR-20261015-lighttpd-terminal-delivery-eos

**Language:** English | [Deutsch](CR-20261015-lighttpd-terminal-delivery-eos.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-lighttpd-terminal-delivery-eos |
| Date (UTC) | 2026-10-15 |
| Base revision | `9980eb049dde0643da6a4f04e3b6712801b670b3` |

## Motivation and problem statement

Independent I12 host captures exposed four lighttpd lifecycle defects: reset resumed a body phase after an applied terminal P3 action; a real zero-length upstream response omitted native EOS; the response hook discarded an already selected technical 500; and stock/body-mode=none reset omitted the actual output commitment before logging.

## Acceptance criteria

Preserve terminal decisions and first cause; deliver an acknowledged technical response without engine reentry; report actual host header/body commitment; deliver CL0 EOS once at real header completion. Incomplete positive Content-Length must retain missing EOS. Cleanup remains once and native limits remain engine-owned.

## Implementation decision and rationale

Three reset guards use the existing host_response_attempted terminal marker. The new failure_response_selected flag is set only after successful host failure selection and acknowledgement, including paths already marked api_failed. Reset synchronizes real write_queue.bytes_out/resp_header_len through the checked Common API only after ordinary P3 processing. The patched core closes the entity bridge at its actual CL0 completion; reset never fabricates EOS.

## Changed files

connectors/lighttpd/module/mod_msconnector.c; the lighttpd stream-hook patch; new compiled test_terminal_response_reset.py, test_empty_response_eos.py and test_tech_delivery_commit.py; existing I09/I10 fixtures and two stale source-contract assertions. The P2 assertion now checks existing native-limit ownership instead of an obsolete connector byte-limit literal. This record is the paired behavior documentation.

## Commands executed

All commands use RTK. Compiled terminal reset controls: 2 PASS, with guard-removal mutations failing for stock and patched ABI. CL0 core regression: baseline fails with EOS0; fixed test PASS, including callback failure and incomplete positive length. Technical delivery/commit controls: 4 PASS, four targeted mutations fail. Final I10 adapter error suite: 8 PASS. Selected patched/P2 source contracts: 51 tests, 49 PASS, 2 namespace skips. The initial broader 206-test run retained two stale assertion failures, subsequently corrected; the final broad run passes 212 tests (199 PASS, 12 namespace skips, 1 SDK-loopback class skip without the selected SDK environment). The explicit SDK3.0.14 Stock-sidecar suite passes45 tests (44 PASS, 1 distinct-UID sandbox skip).

## Security impact

No namespace, UID, source trust, permissions, warnings or gate is relaxed. An error response bypasses engine reentry only after explicit successful failure selection. Failed acknowledgement still returns HANDLER_ERROR. A failed checked commit update stops completion, retains first cause and destroys once.

## Runtime evidence

Run i12-lighttpd-412-completion-20261015 preserves original failure captures and separate fixes. Preliminary real Nonroot patched CL0 retake1792078514962046469 observes EOS1, append0, P4/logging/finish/free once and healthy neighbors; short Content-Length retains EOS0 and abnormal client exit. This preliminary run predates final integrated product identity and adds no final qualification. The pinned lighttpd1.4.85 core build passes; the new hunk applies without fuzz. Three pre-existing patch fuzz requirements remain unchanged.

## Known limitations

Compiled callback tests use bounded host seams; they are regression evidence, not complete hosted lifecycle PASS. Current-head host retakes and required CI/Sonar are pending integration through #410 into #412. Stock-native remains a diagnostic route without native entity hooks; patched Strict client abort remains unsupported.

## Remaining risks

Actual output counters must remain valid at the host reset boundary. The new tests cover header-only commitment, body commitment, failed checked synchronization, API-failed delivery and failed failure-action acknowledgement. Final host retakes must confirm the integrated binaries.

## Checks not run and rationale

No master integration, release, deployment, Framework/MRTS or other-connector matrix. Unprivileged namespace tests are skipped in the restricted shell; separately authorized guarded true Nonroot host runs retain the original isolation contract. #382 historical Gitleaks remains an independent release blocker.

## Final diff and review status

Root reviewed the minimal production diff and targeted regressions. Normal commits on existing #382 and normal #382→#410→#412 integration are authorized; no history rewrite or master merge. Reader-facing final qualification and downloadable raw evidence belong to the existing #412 follow-up.

## 2026-10-18: precommit P3 response replacement

A controlled real Nonroot host reproducer separates backend headers from the body by250ms, or writes both in one physical send. Both an ordinary P3 deny and the existing redirect-to-deny capability fallback deliver403 in the coalesced case but time out without client response in the separated case (attempt1792317367022881887). This is a host delivery defect independent of redirect support. The unchanged original redirect oracle is reviewed separately.

`http_response_write_prepare()` prepares error documents before dispatching response-start filters. Merely selecting403 in that later hook leaves the upstream response framing active and cannot request an error-document pass that has already occurred. The connector now rejects replacement once any output byte has committed; for an already processed, uncommitted response it resets the upstream framing/queue/headers, restores the optional host-generated identity header, and uses Lighttpd's existing finished-error API. An empty completed403 is valid on this path. Earlier P1/P2 error-document behavior is preserved. No native EOS is synthesized.

The compiled actual decision function regression fails before this change, passes afterward, and rejects four mutations removing reset, redirect reset, the commit guard or explicit finished response. Preliminary isolated-source host retake1792317601336591360 delivers complete403 for both actions with either backend scheduling; separated responses have actual Content-Length0 and coalesced responses complete with the host error document. Every neighbor remains a separate real request. This retake precedes the final identity-header preservation addition; the final source-bound retake is recorded separately. Required integrated CI and final-head host qualification remain independent gates.

Final isolated-source retake1792317807850563840 includes identity-header preservation and observes complete403 plus healthy200 neighbors in all four cases. Source and physical hashes are retained in patched/p3-product-regression/final-host.json.

Root verification of the additional P3 change: 214 lighttpd tests with the explicitly selected SDK3.0.14 pass (201 PASS, 13 namespace/UID skips), including the new compiled reset/finish/committed-output mutations. I09 has6 PASS; I10 has8 PASS; technical delivery/commit has4 PASS; patched host contracts have40 PASS and2 namespace skips. The first broad run retained an I10 fixture compilation failure because its host API model lacked the newly used reset/finished-error helpers. Updating that model exposed a stale assertion: after reset and an injected failed status setter, the retired upstream200 is now correctly unset (0), with no acknowledged replacement. The test still requires terminal failure, preserved first cause, zero reentry and once cleanup. The original failed runs remain in the run directory. No warning or assertion was disabled.

## 2026-10-18: complete response observation across the splice path

A fresh integrated-head capture of the original1050657-byte response delivered every byte to the client, but the native engine received only10105 bytes. The missing1040552 bytes passed through `http_response_append_splice()`, which moves backend data directly into a tempfile without the entity callback. The original capture and its worker assertions remain preserved; their large-response lifecycle PASS is invalidated. Client hash equality alone does not prove inspection completeness.

The core now queries the existing registered response-body callback slot and returns to its ordinary bounded userspace read path when a consumer exists. Without a consumer, the existing socket/pipe splice optimization remains enabled. This adds no body accumulator, native limit, replay, or synthetic EOS. The compiled regression extracts the actual patched splice guard and entity bridge; it covers a registered consumer, no consumer, callback failure and exactly-once EOS. The pre-fix consumer test fails, the fixed test passes, and removing the guard fails again. The first fresh build exposed a missing declaration include; that failed build is retained. The corrected pinned1.4.85 core and newly compiled module both build successfully.

The real private Nonroot retake uses the unchanged1050657 original bytes, a separate equal-length body with a harmless pass/log marker in its middle, and the CL0 control, each with a healthy neighbor. Physical byte/EOS/hash results are recorded after the run; no lifecycle qualification is assigned by these component regressions.

The isolated-source Nonroot retake1792321992503537309 completes all three cases with HTTP200, actual backend/client hash equality, exact native append and contiguous hosthook totals1050657/1050657/0, EOS1, native P4/logging/cleanup once, zero invalid observer rows and200 neighbors. The middle marker appears in the engine-written audit. Raw `common_finish` invocation count is2 and remains visible, rather than being relabeled once. `patched/splice-product-regression/final-host.json` binds every physical path/hash and build source; final integrated qualification and CI remain Root-owned.
