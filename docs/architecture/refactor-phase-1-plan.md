# Refactor Phase 1 Plan

Status: implemented

This phase starts a conservative common foundation without changing Apache or
NGINX runtime connector code. The goal is to make safe connector-neutral data
shapes visible while preserving the existing real-world smoke behavior.

## Inputs Reviewed

- Apache upstream connector source under `connectors/apache/upstream/src/`.
- NGINX upstream connector source under `connectors/nginx/upstream/src/` at the
  time of phase 1. Phase 9 later migrated those files to adapter-owned
  `connectors/nginx/src/`, and phase 10 removed the former NGINX `upstream/`
  reference tree after durable attribution was preserved.
- Existing common C-first headers under `common/include/msconnector/`.
- Real-world smoke harnesses for Apache and NGINX.

## Safe Common Foundation

The following common areas are safe in phase 1 because they do not include
server SDK headers, do not own libmodsecurity objects, and do not move hook or
filter logic:

| Area | Decision | Reason |
| --- | --- | --- |
| Capability descriptors | Keep existing `capabilities.h` as canonical | Already connector-neutral and C-compatible |
| Intervention representation | Split into `intervention.h` | Apache and NGINX both consume libmodsecurity interventions, but translation remains connector-specific |
| Operation status values | Add `status.h` | Needed for neutral adapter/test status vocabulary without HTTP semantics |
| Origin metadata | Add `origin.h` | Captures provenance/version strings without source ownership assumptions |
| Request/response metadata | Keep existing headers | Already neutral; no ownership rules changed |
| Logging metadata | Keep existing header | Existing logger type is callback-only and connector-neutral |

## Refactor Candidates For Later

| Candidate | Apache evidence | NGINX evidence | Phase 1 decision |
| --- | --- | --- | --- |
| Ruleset loading | `msc_rules_add_file`, remote rules in Apache config | rules file directives in NGINX config | Document only |
| Transaction lifecycle | `create_tx_context`, hook phases, filters | request context plus access/header/body/log handlers | Document only |
| Intervention handling | `process_intervention(Transaction *, request_rec *)` | `ngx_http_modsecurity_process_intervention(Transaction *, ngx_http_request_t *, ngx_int_t)` | Represent data only; do not move behavior |
| Audit/logging | Apache error/log hooks | NGINX log callback and log phase | Document only |
| Request metadata mapping | Apache request records and tables | NGINX request fields/chains | Document only |
| Response metadata mapping | Apache output filter | NGINX header/body filters | Document only |
| Error handling | Server-specific HTTP/finalize paths | Server-specific return/finalize paths | Common status vocabulary only |

## Non-Goals

- No Apache hook registration changes.
- No NGINX module registration changes.
- No Apache bucket brigade changes.
- No NGINX body/header filter changes.
- No server-specific configuration parsing changes.
- No libmodsecurity transaction ownership abstraction.
- No response-body blocking promotion; `RESPONSE_BODY` remains xfail/mapped-only.

## Acceptance For This Phase

- New common headers compile as standalone C headers.
- Apache and NGINX source imports remain runtime-equivalent to the prior smoke
  state.
- The existing smoke targets continue to pass before any future code extraction
  is attempted.
- All external reference repositories remain read-only.
