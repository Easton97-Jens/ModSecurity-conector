# Change Record: CR-20261008-nginx-lifecycle-sequence-driver

**Language:** English | [Deutsch](CR-20261008-nginx-lifecycle-sequence-driver.de.md)

Implementation handoff; final integrated Exact-Head coverage remains outstanding.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-lifecycle-sequence-driver |
| Date (UTC) | 2026-10-08 |
| Base revision | `b7403e30111688da00d8e7ce376ea91ced1c6145` |

## Motivation and problem statement

Required lifecycle/transport records need real operations, not inferred HTTP success or driver-created events.

## Acceptance criteria

Prove same-connection sequences, distinct transactions, native deny/late rules, bounded faults, Root/nobody identities and owned process/listener cleanup. Retain actual framing, native access and syscall observations.

## Implementation decision and rationale

Reuse safe artifact, projection and pidfd startup helpers. A bounded H1 client never silently reconnects. An owned upstream releases the marker after observed client headers. Attempt-only interposers bind Root launcher, nobody worker, exact transaction or own client socket. Short-write delegates a genuinely partial write; Would-Block uses small own socket buffers and delayed client reading to observe actual EAGAIN and resume. Receipts are not fabricated native events or Canonical PASS.

## Changed files

`ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`, `ci/runtime/lifecycle/nginx_sequence_client.py`, `ci/runtime/lifecycle/nginx_sequence_upstream.py`, `tests/fixtures/nginx_transaction_fault.c`, `tests/fixtures/nginx_write_fault.c`, `tests/test_nginx_sequence_client.py`, `tests/test_nginx_sequence_driver.py`, and this EN/DE pair. Central catalog/dispatch/collection is coordinator-owned.

## Commands executed

RTK-wrapped Parent Python ran four real-loopback client tests and two driver controls, exit 0, after the unsafe-path regression failed and was corrected. Native fixtures compiled with `cc -std=c17 -Wall -Wextra -Werror -fPIC -shared`, exit 0. Framework tests are separate repository evidence. Negative-control flags cannot affect unrelated cases; the begin-control ID is guaranteed to differ from the armed native transaction. Disabled writer controls cannot satisfy the required native write observation.

## Security impact

Only task-owned isolated attempts, loopback sockets and private bounded captures. Fresh direct projections, Root/nobody and pidfd cleanup remain mandatory. No Common/product/MRTS change, global fault, secret dump or protected verifier.

## Runtime evidence

Task `nginx-all-required-20261008T124555Z` retains 13 genuine sequence/mapping/allocation/late operations with exit 0 under `stream-d-r2`. `stream-d-write-r1` records a partial write and complete resumed framing. `stream-d-write-r2` records native EAGAIN, positive resumed writes and a complete 213228-byte response. Root/nobody and verified cleanup were observed. Earlier non-triggering fixtures and artificial-EAGAIN timeout remain failed attempts.

## Known limitations

Native transport provenance needs central integration. Phase-5 finish failure cannot honestly be reported as pre-commit HTTP500. The approved engine contract is a default-disabled post-return soft budget; product wiring and fresh native execution remain integration dependencies. Required selection is unchanged.

## Remaining risks

Approved soft-budget arithmetic follow-up: a pure bounded-time header measures completed synchronous calls using caller-supplied monotonic timestamps. Default zero disables it; exactly-at-budget remains allowed and strictly greater elapsed time exceeds it. Backward/invalid timestamps and overflow fail validation. C17 warnings-as-errors regression compilation first failed on the absent header, then compilation and boundary/control execution passed. This helper is not a hard deadline, cannot interrupt a hung native engine, and proves no host timeout until coordinator wiring and real diagnostic evidence exist.

Diagnostics use verified b7403e artifacts and separately hashed development helpers, not final integrated artifacts. Operation validity is not Canonical PASS; C17 compilation is not runtime promotion.

## Checks not run and rationale

The resumed Parent bilingual check failed on 22 pre-existing missing Framework link targets in the uninitialized isolated worktree. The changed EN/DE record is checked directly as the strongest available local alternative; integrated documentation validation remains required. Ruff could not run because the selected Parent environment has no Ruff module; no dependency or environment was changed.

Final integrated suites, standard lifecycle, current-head CI/Sonar and protected administration remain coordinator responsibilities. No overall acceptance.

## Final diff and review status

Two HTTP/1.1 framing follow-ups are closed operations: `transport_http11_content_length` uses an actual static 22-byte `transport fixture body` file with `text/plain`; `transport_http11_chunked` uses an owned real chunked HTTP/1.1 origin and unbuffered proxying. Safe Phase4 remains enabled. The client captures actual bounded request/response socket bytes through EOF, without relying on `HTTPResponse`'s inferred framing. The origin separately retains received upstream request bytes and successfully written response bytes. Private `.bin` artifacts and separate downstream/upstream SHA256 receipt fields retain these evidence layers.

Four bounded loopback raw-client/origin tests passed after initial missing-client regressions failed; the affected Parent focus now passes 19 tests. Dedicated additions are `tests/test_nginx_http11_wire_client.py` and the framing configuration regression in `tests/test_nginx_sequence_driver.py`. Source inspection shows no connector Content-Length rewriting on the normal P4 path, but cannot prove actual NGINX downstream chunking. Product-native P4 completion and transaction cleanup must be emitted by the coordinator's new module; no NGINX build/runtime was performed for this slice. Central registration/schema/collector and final canonical evidence remain coordinator-owned.

Approved soft-budget probe follow-up: `tests/fixtures/nginx_engine_budget_fault.c` delegates the actual phase-1/phase-4 API, then delays only the exact owned worker/transaction by 25ms and records actual monotonic start/end/elapsed and native return. It delegates Common cleanup and records actual cleanup return/completion/error-class code and name; it does not replace cleanup. The driver configures a 10ms budget, expects actual precommit504 or committed200 with aborted framing, removes rule1100301 only for these technical probes and hashes the effective rules afterward. Wrong-transaction control and explicit disabled0/under-budget100 controls must fail timeout validation. The client now accepts defined504 operations. Receipt includes the native ledger hash.

RTK-wrapped Parent Python passed 14 focused driver/client/transport tests. C17 `-Wall -Wextra -Werror -fPIC -shared -Icommon/include` fixture compilation and C17 arithmetic compilation/execution passed. These checks prove fixture compilation, clock boundary arithmetic and driver configuration/receipt behavior; no rebuilt NGINX timeout runtime has executed. Exact native event pairing and flat Common serialization are validated separately by Framework. Product hooks, full suites, clean artifact binding and canonical runtime remain coordinator-owned.

The `transport_sequential_requests` selection now sends allow/deny/allow on one actual socket, matching its catalog contract. Its red dynamic test observed three connections before correction; two transport tests now pass, including the existing keep-alive allow/allow control. Independent-connection lifecycle cases remain separately selected. Native transport event production and final canonical coverage remain coordinator-owned.

Approved post-response finish follow-up:

The attempt-only finish interposer binds exact worker and case transaction, rejects native logging once and delegates real Common cleanup. The client retains actual body SHA256. An exact-URI transaction map and non-redirecting static fixture prevent unrelated listener probes/internal redirects from sharing the armed identity. Seven Parent focused tests pass after a red identity-scope regression. `stream-d-finish-r3` proves unchanged HTTP 200/body, exact logging error, actual cleanup and wrong-transaction control rejection (direct exits 0/1). Earlier attempts remain retained failures. No product cleanup mutation or validator relaxation was required. Final Canonical coverage remains outstanding.

Exclusive source and negative controls reviewed. No unrelated edits, payload copies, Gitlink update, merge or history rewrite. Separate commits await controlled integration.
