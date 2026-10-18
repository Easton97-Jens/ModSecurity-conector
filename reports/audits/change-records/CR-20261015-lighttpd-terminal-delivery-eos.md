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
