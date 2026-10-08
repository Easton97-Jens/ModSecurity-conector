# Change Record: CR-20261008-nginx-response-limit-signature

**Language:** English | [Deutsch](CR-20261008-nginx-response-limit-signature.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-response-limit-signature |
| Date (UTC) | 2026-10-08 |
| Base revision | `91625ef984dcff914ea3a631dc738645d78abf45` |

## Motivation and problem statement

The pinned Engine returns a legitimate rule-ID-free SecResponseBodyLimitAction Reject intervention. The NGINX adapter currently classifies this as an invalid Engine result. A general exemption for missing rule identity would weaken validation.

## Acceptance criteria

Accept only response-body phase, disruptive 1, status 403, no URL, no rule identity and the exact native diagnostic. Reject wrong phases, statuses, boolean values, log prefixes/suffixes, redirects and rule-bearing interventions.

## Implementation decision and rationale

The new NGX-only static inline predicate takes the existing common intervention representation and a bounded extracted rule identity. It compares no more than 52 diagnostic bytes, including the terminator. This restores recognition of an existing Engine policy; it neither introduces connector limit policy nor changes Common or off/safe/strict semantics.

## Changed files

connectors/nginx/src/ngx_http_modsecurity_response_body_limit.h; tests/fixtures/nginx_response_body_limit.c; tests/test_nginx_response_body_limit.py; this EN/DE pair. Module timing and source-map wiring remain coordinator-owned.

## Commands executed

RTK-wrapped explicit Parent Python unittest compiled C17 with -Wall -Wextra -Werror -pedantic-errors under MODSECURITY_SANITY_CHECKS=0 and 1. Initial RED failed because the header was absent; GREEN compiled and executed all positive and negative controls with exit 0.

## Security impact

No global missing-rule exception, relaxed validator or new privileges. NULL intervention/log, nonexact disruptive values and non-NULL URLs are rejected. Inputs are valid Engine-owned NUL-terminated strings, not arbitrary unterminated buffers.

## Runtime evidence

The retained external Engine-only CAPI probe observed append 1, retained length 0 and immediate intervention 1/status403/disruptive1/noURL/noRule with exact native diagnostic: Response body limit is marked to reject the request. This is not fabricated NGINX runtime evidence. The earlier actual NGX Reject request returned client18 with invalid-Engine abort; the helper alone does not claim its repair is integrated.

## Known limitations

The helper is not yet called by the adapter. Coordinator integration must collect the intervention at its actual immediate boundary, preserve ordinary rule-ID validation and rebuild the module.

## Remaining risks

A matching signature alone cannot establish enforcement timing or a canonical response-limit PASS.

## Checks not run and rationale

Fresh integrated native Reject and full suite are pending coordinator module/timing/SOURCE_MAP integration and rebuild. No final Exact-Head, protected acceptance or canonical PASS is claimed.

## Final diff and review status

Only exclusive new helper, compiled fixture/test and documentation; MRTS, Gitlinks, shared adapter and Common files unchanged.
