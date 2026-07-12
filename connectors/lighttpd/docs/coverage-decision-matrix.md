# lighttpd Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: `minimal_runtime_smoke` / `partial_runtime_path`

This matrix records only the native lighttpd connector evidence. Global
promotion and response-body gates remain defined by the repository-wide
connector policy.

## Current status

| Gate | Status | Evidence or boundary |
| --- | --- | --- |
| Origin/source map | documented | `ORIGIN.md`, `SOURCE_MAP.json` |
| Common SDK adoption | implemented | Common config, mapper contracts, runtime, decisions, limits, events |
| Native module lifecycle | implemented | init/defaults/hooks/reset/cleanup in `module/mod_msconnector.c` |
| C17 compile/link | PASS | pinned lighttpd 1.4.84, PIC, shared object, `-Werror` |
| Config/module load | PASS | real `lighttpd -tt` |
| Patched core/module pair | build/load path available | copied 1.4.84 core, matching ABI-tagged module, patch/artifact manifests; no capability promotion |
| Start smoke | PASS | real process, clean stop, zero requests |
| Request metadata/headers | PASS, narrow | real baseline 200 and rule-backed 403 |
| Request body | not implemented / unverified | mapper advertises no body and passes no payload |
| Response metadata/headers | IMPLEMENTED, NOT ASSERTED | response-start hook exists; no real Phase-3 behavioral assertion yet |
| Response body | not implemented / unverified | no body hook or payload mapping |
| Decision/block status | PASS, Phase 1 | canonical rule `1100001`, HTTP 403 via `http_status_set_err()` |
| Events | PASS, narrow | JSONL connector/rule metadata; no body payload field |
| Transaction cleanup | implemented | finish/destroy and mapper storage cleanup at reset |
| No-CRS targeted smoke | NOT EXECUTED | the minimal 200/403 runtime core is separate from the 53-case baseline |
| CRS | not run / not claimed | no native CRS evidence |
| Production/security/full matrix | not claimed | broader hardening and evidence absent |

## Gate checklist

- [x] Pinned lighttpd source, binary, and generated ABI header available.
- [x] Native module and host mapper exist.
- [x] Build and bridge self-test are separate.
- [x] Config check loads the real module.
- [x] Start smoke sends no requests.
- [x] Separate runtime smoke traverses lighttpd and the module.
- [x] Baseline request is allowed with 200.
- [x] Phase-1 header rule blocks with 403.
- [x] Decision event includes connector and rule metadata.
- [ ] Request-body mapping and Phase 2 evidence.
- [ ] Response-body mapping, Phase 4, and late-intervention evidence.
- [ ] Redirect/drop/abort behavior evidence.
- [ ] Native CRS evidence.
- [ ] Stress, resilience, security, and production hardening evidence.

## Promotion decision

The connector may claim only `minimal_runtime_smoke` for the narrow native
header path. It must not claim response-body verification, CRS verification,
security verification, production readiness, or full-matrix readiness.

## Canonical Phase-4 decision

The native module deliberately has no decoded response-body hook. The patched
callback selected by the separate full-lifecycle profile sees pre-socket-write
HTTP/1.x wire output, so it is a no-op for response-body inspection. These are
current module implementation gaps, not host-model impossibility claims.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered`, `phase4`, and `phase4_rule_evaluation` | `not_implemented` | no response-body data reaches ModSecurity |
| `phase4_pre_commit_deny` | `not_implemented` | no Phase-4 timing point exists in the module |
| `late_intervention`, `late_intervention_log_only`, and `late_intervention_abort` | `not_implemented` | no post-commit response-body policy exists |
| `late_intervention_status_metadata` | `not_implemented` | no Phase-4 event can yet separate original/requested/visible status and actions |

Phase-4 rows are `NOT_EXECUTED` (or omitted by capability selection), not
`UNSUPPORTED`. The existing header hook and Phase-1 deny are separate;
evidence remains metadata-only.
