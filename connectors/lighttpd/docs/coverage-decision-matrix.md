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
| Start smoke | PASS | real process, clean stop, zero requests |
| Request metadata/headers | PASS, narrow | real baseline 200 and rule-backed 403 |
| Request body | unsupported / unverified | mapper advertises no body and passes no payload |
| Response metadata/headers | executed in smoke | response-start hook and Common response processing |
| Response body | unsupported / unverified | no body hook or payload mapping |
| Decision/block status | PASS, Phase 1 | rule `1000001`, HTTP 403 via `http_status_set_err()` |
| Events | PASS, narrow | JSONL connector/rule metadata; no body payload field |
| Transaction cleanup | implemented | finish/destroy and mapper storage cleanup at reset |
| No-CRS targeted smoke | PASS | only the repository targeted rule, not CRS |
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
