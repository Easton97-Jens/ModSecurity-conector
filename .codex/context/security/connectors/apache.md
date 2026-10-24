# Apache Deep Security Delta

## Current logical profile

- `apache`
- selected host route: native HTTPD module
- product source: `connectors/apache/`

Current route identity, build targets, directives, and evidence claims must be read from the current checkout. Do not freeze historical runtime counts in this policy.

## Host-specific boundaries

Assess Apache hooks and filters, APR/request pools, primary request ownership, subrequest reuse, internal redirects, ErrorDocument transitions, input/output bucket brigades, request/response body EOS, configuration create/merge, APXS/Autotools module build/loading, transaction cleanup, and Apache-visible intervention mapping.

Pay special attention to:

- request-pool and transaction lifetime;
- subrequest versus primary-request state;
- internal redirect / ErrorDocument rebinding limits;
- bucket normalization, split/coalesced buckets, flush/EOS ordering;
- output filter forwarding versus response commit;
- P3/P4 before and after commitment;
- response-body limits and current `SecResponseBodyMimeType` engine boundary;
- current compatibility status of connector-owned Phase-4 content-type configuration;
- error paths that must not fall back to uninspected traffic;
- APXS/HTTPD/libmodsecurity header/library compatibility.

## Required common checks

Load:

- `../checks/http-normalization.md`
- `../checks/request-desync.md`
- `../checks/modsecurity-bypass.md`
- `../checks/memory-lifecycle.md`
- `../checks/concurrency-races.md`
- `../checks/resource-exhaustion.md`
- `../checks/logging-disclosure.md`
- `../checks/config-injection.md`
- `../checks/supply-chain.md`
- `../checks/advisory-research.md`
- `../checks/finding-validation.md`
- `../checks/response-commit-phase4.md`
- `../checks/evidence-integrity.md`
- `../checks/runtime-failure-recovery.md`

## Apache-specific validation seeds

Where repository-native harnesses support them, cover normal Allow/Deny, request-body EOS, response-header and response-body boundaries, split/fragmented bucket sequences, empty response, limit handling, subrequest/internal-redirect/ErrorDocument behavior, keepalive follow-up requests, client abort, and cleanup.

Do not present source-level P4 wiring, parser acceptance, or a module build as canonical client-visible P4 evidence.
