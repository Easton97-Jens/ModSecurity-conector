# Change Record: CR-20261018-haproxy-strict-h1-transport-abort

**Language:** English | [Deutsch](CR-20261018-haproxy-strict-h1-transport-abort.de.md)

Product transport follow-up on existing #382; independent host acceptance on #415.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-strict-h1-transport-abort |
| Date (UTC) | 2026-10-18 |
| Base revision | `ebbb35e19694b6446ecf653934f1b542b94f4cc8` |

## Motivation and problem statement

A fresh isolated HAProxy3.2.25 Strict 33-byte host run suppressed the queued body, but the H1 mux still sent TLS close_notify. The predeclared transport-abort observation remained false despite Content-Length underflow.

## Acceptance criteria

Use the supported hard transport shutdown before H1 can perform clean TLS shutdown; retain stream-local H2 shutdown, queued-byte suppression, Safe behavior, earlier delivered bytes and independent neighbor state. Verify actual transport in a fresh integrated host retest.

## Implementation decision and rationale

After channel_htx_erase, obtain only the frontend connection through guarded public sc_conn. For a ready connection whose actual mux name is H1, call conn_xprt_shutw_hard before stream_abort/sc_abort/sc_shutdown/stream_shutdown. The public hard helper invokes transport clean=0, allowing TLS to suppress close_notify. H2 and unknown/nonconnection endpoints retain their existing stream shutdown. No descriptor close/free or backend transport access is added.

## Changed files

HAProxy HTX filter and existing native I10 host-caller regression fixtures. Documentation: connectors/haproxy/README.md and README.de.md, plus this Change Record pair. Common, SPOP, MRC1 and frozen physical-sink behavior are unchanged.

## Commands executed

RTK-wrapped actual upstream-inline-API callback matrix: three tests and 25 mutations passed; final ASan/UBSan control passed. C17 and overlay checks and a fresh complete HAProxy3.2.25 build passed. Exact compiler argv, exits, raw C fixtures and hashes are indexed by external run i12-haproxy-415-acceptance-20261015/product-spop/strict-tls/review.json; 56 raw C/JSON files cover 28 probes. The old ebbb35 filter fails the real-API hard/clean ordering assertion before the fix.

## Security impact

Only the affected ready H1 frontend transport receives hard shutdown. H2 retains the existing per-stream mux path so this repair does not explicitly close its shared transport. Null stream/frontend/sedesc/connection, unready transport and nonconnection endpoints are guarded. No loader, isolation, validation, compiler-warning, gate or dependency weakening.

## Runtime evidence

Historical and fresh pre-fix raw evidence are retained: initial-ea62 Strict client received 200 headers declaring 33 bytes, zero body bytes and clean TLS close_notify; Safe received the complete independently expected 33 bytes. The separate probes each had a healthy 12-byte neighbor. These runs confirm suppression and the remaining clean-close gap; they do not qualify the new transport repair.

## Known limitations

A hard shutdown cannot recall delivered bytes. Actual H1 wire behavior and H2 parallel-stream effects require independent host measurement. A component H2 neighbor control is not an H2 hosted runtime proof. TCP reset is not inferred from truncation or TLS errors.

## Remaining risks

Fresh integrated capture builds and Safe/Strict empty, buffered, large, multichunk, streaming, cancellation and parallel cases remain required. Original abort expectations remain unchanged and no HTTP-only result becomes a full lifecycle PASS.

## Checks not run and rationale

Fresh host execution and final-head CI/Sonar follow normal #382→#410→#415 integration and rebuilding. No automatic merge. The independent historical #382 Gitleaks release blocker remains.

## Final diff and review status

The separate product delta, three-file frozen identity and EN/DE handoff are retained under product-spop/strict-tls. Root reviewed the H1-only public-API guard and shutdown order; independent review and integrated host qualification are tracked separately.
