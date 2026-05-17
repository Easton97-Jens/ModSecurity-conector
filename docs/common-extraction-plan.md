# Common Extraction Plan

Status: planned

The Apache and NGINX connector sources are imported as separate upstream code
trees first. No common code is extracted in this step.

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
| Ruleset loading | Both connectors load ModSecurity rules and files | Document only |
| Transaction lifecycle | Both create and drive libmodsecurity transactions | Document only |
| Intervention handling | Both translate libmodsecurity intervention into HTTP responses | Document only |
| Audit/logging | Both connect libmodsecurity logging to server artifacts | Document only |
| Request metadata mapping | Both map method, URI, headers, body, and connection data | Document only |
| Response metadata mapping | Both map response headers/body through server filters | Document only |
| Config model | Both have enable/rules-file style connector config | Keep connector-specific |
| Error handling | Both need consistent blocked/fail reporting in tests | Candidate for test harness common code only |

## Non-Candidates For Now

- Apache hook registration and filters.
- NGINX phase handlers and filter ordering.
- APXS/Autotools integration.
- NGINX `config` dynamic module integration.
- Any `RESPONSE_BODY` blocking logic until it is proven stable for both
  connectors.

## Next Step

After the imported code builds from the monorepo source paths, inspect duplicate
libmodsecurity API usage and design a small connector-neutral adapter proposal.
That proposal must include before/after smoke results.
