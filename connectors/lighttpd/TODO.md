# lighttpd Connector TODO

Status: native `minimal_runtime_smoke` for Phase-1 headers

## Completed

- [x] Repository-owned origin and source map documented.
- [x] Pinned lighttpd 1.4.84 source/binary provisioning available.
- [x] Native plugin init, config registration, defaults, cleanup implemented.
- [x] Request metadata and length-delimited header mapping implemented.
- [x] Response metadata and length-delimited header mapping implemented.
- [x] Common runtime, rule loading, transaction ID, decisions, limits, flow
  guard, DoS guard, events, and JSONL wired into live host callbacks.
- [x] Phase-1 deny mapped to `http_status_set_err()`.
- [x] Transaction finish/destroy and mapper storage cleanup implemented.
- [x] C17 PIC shared-module build with `-Wall -Wextra -Werror` implemented.
- [x] Build and bridge self-test separated.
- [x] Real module/config load check implemented.
- [x] Request-free real-process start smoke implemented.
- [x] Separate real-host 200/403 runtime smoke implemented.
- [x] Narrow JSONL event metadata check implemented.

## Required before broader runtime claims

- [ ] Define and implement bounded lighttpd request-body capture.
- [ ] Preserve and test request-body truncation metadata.
- [ ] Implement and test Phase-2 request-body processing.
- [ ] Evaluate safe response-body hooks and output timing.
- [ ] Implement response-body buffering only if intervention timing is honest.
- [ ] Test Phase 4 and late-intervention behavior.
- [ ] Verify redirects, drops, connection aborts, and non-403 decisions.
- [ ] Add multi-worker, concurrency, keep-alive, HTTP/2, and abort-path tests.
- [ ] Run native No-CRS negative/pass-through and expanded rule cases.
- [ ] Add native CRS smoke only with explicit local CRS evidence.
- [ ] Add long-running, memory, cleanup, and fault-injection evidence.
- [ ] Complete security review and production hardening.
- [ ] Run the relevant full matrix.

Until those items are evidenced, keep status at `minimal_runtime_smoke` /
`partial_runtime_path` and keep all body, CRS, security, production, and full
matrix claims false.
