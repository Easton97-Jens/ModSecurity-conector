# Phase-4 mode and cumulative inspection budgets

**Language:** English | [Deutsch](phase4-mode-budget.de.md)

## Scope

This contract covers Apache, NGINX, HAProxy, Envoy, Traefik and lighttpd in this
repository. It concerns the extra connector-owned cumulative inspection budget,
not libModSecurity's own response-body policy or unrelated resource limits.

| Mode | Extra cumulative Phase-4 budget | Inspection and errors |
| --- | --- | --- |
| `off` (default) | Not enforced | Continue configured engine inspection and native intervention/error handling. |
| `safe` | Enforced | Preserve existing early enforcement and late-rule `log_only` behavior where supported. |
| `strict` | Enforced | Preserve existing early enforcement and supported late abort behavior. |

`UNSET` and invalid modes are not synonyms for `off`. Configuration validation
and the positive configured-limit requirements remain in place in every mode.
No change is made to engine `SecResponseBodyAccess`, `SecResponseBodyMimeType`,
`SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit` or its limit action.

## Implementation boundaries

Apache and NGINX use `modsecurity_phase4_body_limit`. HAProxy's native binding
and Common Runtime-based integrations use their configured response-inspection
budget. The cumulative planner and the secondary transaction-contract counter
must agree. HAProxy HTX also sets its per-stream budget consistently. The
lighttpd streaming sidecar's Content-Length precheck follows the same mode. Envoy's
Go processor obtains an explicit budget-disable capability from the loaded
Common engine, not from its separately configured late-action policy. Its
message/chunk cap and signed counter overflow checks remain enabled.

Common Runtime changes cover direct and response-companion append paths used
by Envoy, Traefik and lighttpd. Request-only compatibility routes still need
their supported observer/companion. HAProxy SPOE/SPOP's protocol/companion
transport limits remain independent and are not disabled. No unsupported
profile is promoted to a working Phase-4 route by this change.

The internal effective limit is `SIZE_MAX` in `off` only to represent the
absence of a configured cumulative cap. It is never an allocation size.
Byte-counter overflow, invalid pointers, bad file reads, lifecycle violations
and engine failures still fail. `process_partial` cannot turn an accounting
overflow into a successful unlimited append in `off`.

## Independent resource limits

Header/event limits, maximum chunks and messages, correlation capacities,
timeouts and bounded response storage remain active. The existing public
Common Runtime response-limit getter continues to describe the bounded
host/transport allocation capacity. It must not return `SIZE_MAX`.
A buffered compatibility sidecar may therefore still reject an oversized
response in `off`; that is its independent storage capacity, not the disabled
extra cumulative Phase-4 budget.

## Native errors and NULL guards

In NGINX `off`, a negative native intervention result uses the pre-PR #377
`ngx_http_filter_finalize_request(..., NGX_HTTP_INTERNAL_SERVER_ERROR)` path.
Positive statuses are returned unchanged; zero continues normally. This does
not change the Safe/Strict intervention policy.

Other integrations retain their own return conventions, including APR statuses,
zero/nonzero Common Runtime success and host-specific transport failures.
NGINX's integer convention must not be copied into those APIs.

NGINX's P4 planner, handler and logger guard missing configuration. Apache's
P4 bucket and intervention paths guard missing state, configuration and request
objects. The Common event writer checks runtime/event/file before dereference.
Traefik checks the session's service before reading its response-body policy.
Existing Envoy bridge checks remain in place.

## Verification boundary

Focused compiled helper/branch tests and source-wiring checks are not live
NGINX, httpd, HAProxy, Envoy, Traefik or lighttpd HTTP integration tests.
Run native host regressions, allocation/transport checks and current-head CI
before merging. See the [Change Record](../reports/audits/change-records/CR-20260920-phase4-all-connector-budget.md) for actual execution results.
