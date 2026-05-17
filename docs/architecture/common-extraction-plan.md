# Common Extraction Plan

Status: implemented

The Apache and NGINX connector sources are imported as separate upstream code
trees first. Phase 1 creates only a small connector-neutral common foundation;
it does not move Apache or NGINX hook/filter behavior.

## Repository Roles

| Area | Role | Long-term direction |
| --- | --- | --- |
| `connectors/apache/upstream/` | Temporary Apache reference/import basis from https://github.com/owasp-modsecurity/ModSecurity-apache | Shrink only after functional replacement, retained attribution, and passing smokes |
| `connectors/nginx/src/` | Adapter-owned NGINX module source derived from https://github.com/owasp-modsecurity/ModSecurity-nginx | Keep connector-specific; reduce only with dedicated NGINX adapter proof |
| `connectors/nginx/upstream/` | NGINX attribution/reference basis from https://github.com/owasp-modsecurity/ModSecurity-nginx | Retain license/reference files while NGINX-derived source remains |
| `licenses/` | Durable license and origin attribution | Keep while imported code or source-derived evidence remains |
| `common/` | Connector-neutral C-first types and future shared helpers | Grow only after evidence-backed extraction |
| `connectors/<name>/` | Server-specific build, lifecycle, harness, and integration code | Keep hooks, filters, and config parsing connector-specific |

## Extraction Rule

A candidate may move to `common/` only after all of the following are true:

- the behavior is connector-neutral;
- Apache and NGINX real-world smoke tests still pass after the extraction;
- the extracted interface does not include Apache or NGINX headers, types, or
  lifecycle assumptions;
- origin and compatibility notes are updated.

## Candidate Areas

| Area | Candidate rationale | Current decision |
| --- | --- | --- |
| Capability descriptors | Connectors advertise supported lifecycle artifacts | Existing `capabilities.h` remains canonical |
| Operation status vocabulary | Build/test adapters need connector-neutral outcomes | Add common status values only |
| Origin metadata | Imported connectors need stable provenance metadata | Add common origin data shape only |
| Intervention data shape | Both connectors translate libmodsecurity interventions into HTTP responses | Add neutral representation only; keep translation connector-specific |
| Ruleset loading | Both connectors load ModSecurity rules and files | Document only |
| Transaction lifecycle | Both create and drive libmodsecurity transactions | Document only |
| Audit/logging | Both connect libmodsecurity logging to server artifacts | Document only |
| Request metadata mapping | Both map method, URI, headers, body, and connection data | Keep existing neutral request shape; no adapter extraction |
| Response metadata mapping | Both map response headers/body through server filters | Keep existing neutral response shape; no adapter extraction |
| Config model | Both have enable/rules-file style connector config | Keep connector-specific |
| Error handling | Both need consistent blocked/fail reporting in tests | Candidate for test harness common code only |

## Non-Candidates For Now

- Apache hook registration and filters.
- NGINX phase handlers and filter ordering.
- APXS/Autotools integration.
- NGINX `config` dynamic module integration.
- Server-specific configuration parsing.
- libmodsecurity transaction lifetime or ownership.
- Any `RESPONSE_BODY` blocking logic until it is proven stable for both
  connectors.

## Phase 1 Common Basis

Phase 1 may add or update only connector-neutral C-first headers under
`common/include/msconnector/`:

- status values for common adapter/test outcomes;
- intervention data representation without server-specific response handling;
- origin/provenance metadata;
- thin C++ alias wrappers matching the existing common header pattern.

These files must not include Apache, NGINX, or other server/proxy headers. They
also must not hide ownership of `ModSecurity`, `RulesSet`, `Transaction`, or
`ModSecurityIntervention` objects from libmodsecurity.

## Phase 3 Common Runtime Boundary

Phase 3 adds small C implementation files under `common/src/` for status,
origin, intervention, and capability metadata only. The Apache and NGINX
runtime harnesses continue to use Python/Shell and mirror the schema without
FFI.

## Phase 4 Replace-And-Reduce Boundary

Phase 4 replaces one NGINX adapter-near debug compatibility header. This is not
a Common extraction: the replacement lives under `connectors/nginx/src/` and is
copied only into generated build trees that need `src/ddebug.h`.

No Apache or NGINX hook, filter, body handling, transaction ownership,
configuration parsing, or `RESPONSE_BODY` behavior moves to `common/`.

After this boundary is stable, inspect duplicate libmodsecurity API usage and
design a separate connector-neutral adapter proposal. That proposal must include
before/after smoke results and must not start from response-body blocking
behavior while it remains xfail/mapped-only.

## Phase 9 NGINX Source Ownership Boundary

Phase 9 migrates NGINX `config` and module source files to
`connectors/nginx/src/` and builds the monorepo-default NGINX smoke from the
materialized adapter-owned source tree. This is not a Common extraction.
NGINX phase handlers, filters, config parsing, transaction ownership, and
phase-4 behavior remain NGINX-specific.
