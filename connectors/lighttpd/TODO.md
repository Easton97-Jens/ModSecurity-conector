# lighttpd Connector TODO

Status: native `minimal_runtime_smoke` for Phase-1 headers
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`

Canonical capability source: `connectors/lighttpd/capabilities.json`.

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

- [x] Versioned 1.4.84 source patch defines bounded HTTP/1.x request-body
      capture and has a compile-only check; no runtime capability is promoted.
- [x] Dedicated patched-host target copies, patches, configures, builds,
      installs, stages and ABI-loads a matched 1.4.84 core plus module. The
      full-lifecycle profile selects its isolated 200/403 Phase-1 host smoke;
      it remains non-promoted and does not establish body or Phase-4 evidence.
- [ ] Preserve and test request-body truncation metadata.
- [ ] Implement and test Phase-2 request-body processing.
- [x] Versioned 1.4.84 source patch defines a bounded pre-socket-write HTTP/1.x
      output/EOS hook with short-write deduplication; it is wire output, not a
      decoded entity body, and makes no response-body runtime claim.
- [ ] Implement response-body buffering only if intervention timing is honest.
- [ ] Test Phase 4 and late-intervention behavior.
- [ ] Exercise the implemented response-header hook with a real Phase-3 rule;
      until then `response_headers` and `phase3` remain
      `implemented_not_asserted`, not verified.
- [ ] Verify redirects, drops, connection aborts, and non-403 decisions.
- [ ] Add multi-worker, concurrency, keep-alive, HTTP/2, and abort-path tests.
- [ ] Run native No-CRS negative/pass-through and expanded rule cases.
- [ ] Add native CRS smoke only with explicit local CRS evidence.
- [ ] Add long-running, memory, cleanup, and fault-injection evidence.
- [ ] Complete security review and production hardening.
- [ ] Run the relevant full matrix.
- [ ] `make no-crs-baseline-lighttpd` produces current canonical evidence.
- [ ] `make evidence-check-lighttpd` validates native-module evidence and never
      substitutes the legacy bridge/sidecar self-test.

Until those items are evidenced, keep status at `minimal_runtime_smoke` /
`partial_runtime_path` and keep all body, CRS, security, production, and full
matrix claims false.

## Canonical Phase-4 implementation boundary

The current native module has no decoded response-body hook.  The following facets are
therefore `not_implemented`: `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata`.

- [ ] Implement a bounded native response-body hook with an explicit response
      commitment point before selecting Phase-4 cases for execution.
- [ ] Prove rule `1100301` separately from visible deny status.
- [ ] Prove pre-commit deny, safe `log_only`, and strict
      `abort_connection` as separate outcomes with metadata-only evidence.
- [ ] Add original host status, requested WAF status, visible client status,
      requested action, actual action, commit state, and connection-abort state
      to the relevant event proof.
- [x] Until then retain Phase-4 results as `NOT EXECUTED` (or omit them through
      capability selection), not `UNSUPPORTED`; this is not a claim that
      lighttpd cannot ever support a suitable response-body hook.
