# HAProxy Connector

**Language:** English | [Deutsch](haproxy.de.md)

## Overview

HAProxy uses the selected <code>native-htx-filter</code> route with the
repository overlay. It is the selected HTTP/1.1 P1--P4 Safe reference. This
guide does not claim production readiness, CRS verification, complete protocol
coverage, a complete matrix, first-byte proof, no-full-buffer proof, or strict
late behavior for every case.

## Architecture and ownership

The native route owns HTX filter registration, HAProxy process/build glue, HTX
message translation, pre-commit reply mapping, and host lifecycle. Common
provides neutral config/default/merge/validation semantics, parser contracts,
mapping contracts, limits, metadata-only events, rule identifiers, and
redaction helpers. It does not own HAProxy frame handling or process state.

| Lifecycle area | Selected native HTX responsibility | Boundary |
| --- | --- | --- |
| P1 | Process request metadata before an eligible local reply | A reply is only evidence for its selected case |
| P2 | Process the selected request-body probe at request EOS | It does not prove general incremental request forwarding |
| P3 | Process response headers before forwarding the selected upstream header response | Preserve the actual host-visible response |
| P4 | Borrow bounded response chunks and finish at HTX EOS | Safe result is explicitly <code>log_only</code> |
| Events | Write payload-free metadata | Do not turn metadata into a transport claim |

## Build

Use [the HAProxy compiler guide](../build/compilers/haproxy.md) for the
selected HTX overlay, source inputs, build roots, and configuration checks.
The [HAProxy source guide](../../connectors/haproxy/README.md) remains the
code-adjacent entry point. Compile/link checks are not runtime evidence.

## libModSecurity binding compatibility

The shared binding supports `libModSecurity >= 3.0.14`, with `3.0.14` as the
minimum public C API baseline. It compiles and links the required baseline API
against one explicitly selected matching header/library pair. A declaration or
library mismatch fails with a baseline-API diagnostic; the optional
`msc_get_rules_messages_rule_ids` API is never the reason a valid `3.0.14`
baseline is rejected.

The optional API is enabled only after its exact declaration compiles and its
symbol links against the same pair. The resulting compile-time capability is
used consistently by the independent SPOP and native HTX builds. Without it,
a bounded Rule ID may be recovered from an intervention log for diagnostics;
otherwise `rule_id=0` is an explicit unavailable-metadata value. Disruptive
state, status, redirect/deny action, cleanup, and all host enforcement continue
to derive from `msc_intervention`, never from Rule-ID metadata. The code-adjacent
[compatibility contract and commands](../../connectors/haproxy/README.md#libmodsecurity-compatibility-contract)
describe the exact probes, `paths.env` feature state, and separate validation
targets.

## Configuration

The complete native HTX syntax and separated SPOE/SPOP compatibility entries
are in the [HAProxy configuration reference](../../examples/haproxy/configuration-reference.md).
Host filter configuration, Common Runtime key/value settings, and ModSecurity
Engine rules remain separate layers.

## HTX payload-append failure policy

The HTX binding treats a native body-append result as successful only when its
adapter returns `0` (which requires the underlying C API to report exact
success). Any other result means that the current borrowed HTX slice is no
longer certified as inspected. The filter aborts only the affected transaction
and returns `-1` to HAProxy; it must not return the positive slice length and
thereby authorize an uninspected pass-through.

| Failure class | Fail mode and host action | Event evidence | Cleanup and subsequent request |
| --- | --- | --- | --- |
| Request body append failure (V10, pre-commit) | Fail closed. HAProxy receives `-1`; the retained HTTP/1.1 HAProxy `3.2.22` control observed `400` and zero backend dispatches. | No dedicated structured connector-error event is emitted for this native callback failure. The payload-free evidence is the client status, zero upstream count, and retained host receipt. | The transaction is aborted once. The same HAProxy process accepted a one-byte POST Allow control with `200`; both task-owned listeners were absent after cleanup. |
| Response body append failure (V11, response path) | Fail closed at the transport boundary. HAProxy receives `-1` and terminates only the affected response stream. Where response handling has begun, no synthetic replacement HTTP status is promised. The retained control observed no HTTP response (`000`) and `curl_exit=52`. | No dedicated structured connector-error event is emitted for this native callback failure. The payload-free evidence is the client transport result, one upstream fault request, and retained host receipt. | The transaction is aborted once. The same HAProxy process accepted a HEAD Allow control with `200`; both task-owned listeners were absent after cleanup. |

This is a documented HTX-specific safety decision: a `ProcessPartial`-derived
native append failure is terminal for the borrowed slice because this binding
cannot certify inspection of it. It does not silently select the different
semantics of another connector. The retained bounded run is
`haproxy-htx-append-failure-20260825T131500Z`, SHA-256
`12e4d30c68ff46f45f2f8481d810eb53099f6512f384520e3942fadb0434da9c`; it proves
these V10/V11 HTTP/1.1 cases only, not HTTP/2, HTTP/3, reload, a full FD audit,
or the complete failure matrix.

## P1--P4 lifecycle and Safe boundary

The selected native host smoke can observe P1, P2, P3, and P4 through the HTX
route. P1/P3 may issue an eligible pre-commit local reply. P2's selected
one-block probe records its own observed upstream count but does not establish
a general forwarding or buffering property. P4 Safe preserves the original
response and records <code>host_action=log_only</code>; P4 Strict remains
<code>host_action=not_attempted</code> unless a selected run supplies separate
host/client evidence.

| P4 question | Required observation |
| --- | --- |
| Rule observed | Native HTX P4 rule metadata and selected run/profile |
| Safe late result | Original visible response plus recorded <code>log_only</code> action |
| Strict late result | Explicit host action and client/transport evidence, not a legacy sample |
| Streaming/first-byte property | Dedicated source and transport artifacts for that property |

## Historical SPOE/SPOP compatibility

The former SPOE/SPOP material is **documentation-only**:
<code>implementation_status: not_started</code> and
<code>runtime_verified: false</code>. It is not the selected native HTX route.
Its historical example files remain separated under
<code>examples/haproxy/compatibility-spoe/</code>; they must not be used to
claim native HTX behavior, P4 response-body handling, Safe/Strict late
behavior, first-byte behavior, or no-full-response-buffer behavior.

## Testing and evidence

Use <code>make check-config-haproxy</code> for the selected configuration and
the relevant full-lifecycle target for a real host run. Inspect run-scoped
result records, HTX/host observations, effective configuration, and
metadata-only events. The status vocabulary and promotion boundary are in
[Testing and evidence](../testing-and-evidence.md).

## Operations and troubleshooting

Use explicit externally writable build/runtime/evidence roots. For a native
configuration issue, verify the selected HTX overlay and host configuration
first. For an intervention question, distinguish requested WAF action from the
actual HAProxy host action and visible client outcome.

## Limitations and compatibility

Native HTX and historical SPOE/SPOP are distinct integrations. Do not combine
their directives, evidence, or limitations. No path here establishes broad
streaming, full response-body, strict abort, CRS, or production claims without
the matching selected host artifacts.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [HAProxy configuration reference](../../examples/haproxy/configuration-reference.md)
