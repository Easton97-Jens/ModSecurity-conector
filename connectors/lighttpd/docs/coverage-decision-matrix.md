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
| Request body | patched source contract, unverified | borrowed HTTP/1.1 request ranges exist only in the matched 1.4.84 ABI; no capability promotion |
| Response metadata/headers | IMPLEMENTED, NOT ASSERTED | response-start hook exists; no real Phase-3 behavioral assertion yet |
| Response body | patched identity source contract, unverified | borrowed HTTP/1.1 entity ranges before transfer framing; no streaming host result or promotion |
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
- [x] Patched HTTP/1.1 request/entity callback ABI with borrowed ranges and EOS.
- [ ] Streaming request-body/Phase-2 host evidence.
- [ ] Response-body/Phase-4 runtime and late-intervention evidence.
- [ ] Redirect/drop/abort behavior evidence.
- [ ] Native CRS evidence.
- [ ] Stress, resilience, security, and production hardening evidence.

## Promotion decision

The connector may claim only `minimal_runtime_smoke` for the narrow native
header path. It must not claim response-body verification, CRS verification,
security verification, production readiness, or full-matrix readiness.

## Canonical Phase-4 decision

The stock module has no response-body hook. The patched callback selected by
the separate full-lifecycle profile receives the current HTTP/1.1 identity
entity range in `http_chunk.c` before HTTP/1 transfer framing, not socket-wire
output. It borrows the bytes synchronously, tracks the offset, and emits EOS at
most once. It retains no queue copy; socket short writes and `EAGAIN` occur
after the callback and therefore cannot structurally duplicate an append. This
is a source/build contract only: no real streaming host run validates it, and
gzip/br, HTTP/2, and unexamined file/zero-copy routes are excluded.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered`, `phase4`, and `phase4_rule_evaluation` | `not_implemented` | identity entity source path is not promoted without a real streaming host result; no per-chunk rule-evaluation claim |
| `phase4_pre_commit_deny` | `not_implemented` | no client-validated precommit disposition exists |
| `late_intervention`, `late_intervention_log_only`, and `late_intervention_abort` | `not_implemented` | safe source behavior records `log_only`; strict abort lacks client-visible evidence and remains `NOT EXECUTED` |
| `late_intervention_status_metadata` | `not_implemented` | no client artifact separates original/requested/visible status and actual action after commitment |

Phase-4 rows are `NOT_EXECUTED` (or omitted by capability selection), not
`UNSUPPORTED`. The existing header hook and Phase-1 deny are separate;
evidence remains metadata-only.
