# lighttpd Connector TODO

Status: native `minimal_runtime_smoke` for Phase-1 headers
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`

Canonical capability source: `connectors/lighttpd/capabilities.json`.

The standard compatibility target remains the stock native module. The
full-lifecycle profile dispatches `patched-native` through
`full-lifecycle-lighttpd-patched`, which stages a matched lighttpd 1.4.84 core
and module for an isolated Phase-1 smoke. Its checked-in runtime uses both body
modes as `none`, so it cannot promote body or Phase-4 capabilities even though
the patched ABI now exposes borrowed HTTP/1.1 request ranges and identity
entity-response ranges before transfer framing.

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

- [x] Versioned 1.4.84 source patch defines bounded borrowed HTTP/1.x
      request-body capture and has a compile-only check; no runtime capability
      is promoted.
- [x] Dedicated patched-host target copies, patches, configures, builds,
      installs, stages and ABI-loads a matched 1.4.84 core plus module. The
      full-lifecycle profile selects its isolated 200/403 Phase-1 host smoke;
      it remains non-promoted and does not establish body or Phase-4 evidence.
- [ ] Preserve and test request-body truncation metadata.
- [ ] Run and retain selected Phase-2 request-body artifacts for the patched path.
- [x] Versioned 1.4.84 source patch defines a bounded HTTP/1.1 identity
      entity-body/EOS hook before transfer framing. It supplies borrowed ranges,
      monotonic offsets, and one EOS; socket short-write/EAGAIN retries occur
      later and cannot re-ingest a range.
- [ ] Run real response streaming with identity body data; gzip/br remain
      `NOT EXECUTED` pending an evidenced filter order and decompression scope.
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

The stock module has no response-body hook. The patched 1.4.84 module has an
identity entity-body source path, but no canonical streaming host result. The
following facets therefore remain `not_implemented` for the selected evidence
profile: `response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort`, and `late_intervention_status_metadata`.

- [x] Implement a bounded native identity entity-body hook with explicit EOS
      before selecting Phase-4 cases for execution.
- [ ] Prove rule `1100301` separately from visible deny status.
- [ ] Prove pre-commit deny, safe `log_only`, and strict
      `abort_connection` as separate outcomes with real-client metadata-only
      evidence; strict currently remains `NOT EXECUTED`.
- [ ] Add original host status, requested WAF status, visible client status,
      requested action, actual action, commit state, and connection-abort state
      to the relevant event proof.
- [x] Until then retain Phase-4 results as `NOT EXECUTED` (or omit them through
      capability selection), not `UNSUPPORTED`; this is not a claim that
      lighttpd cannot ever support a suitable response-body hook.
