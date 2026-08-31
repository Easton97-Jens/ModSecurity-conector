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

## Logical SPOE/SPOP response companion boundary

The separate SPOE/SPOP process can own the request-side P1/P2 transaction, but
its request protocol does not carry the HTX response-body stream or response
EOS. The repository therefore models response processing as one logical
transaction across two host components: SPOP creates a bounded opaque
`response_handle` after P2, and the native HTX filter uses the private response
companion to claim that handle, process P3, pass bounded P4 chunks, and close
P4 at HTX EOS. Missing, expired, malformed, or unclaimed correlation must
fail closed and clean up the transaction; it must not silently become a
request-only result.

The repository-native combined harness builds the current MRC1-v2 SPOP agent
and HTX overlay and has locally observed ordered P1/P2 acknowledgement, P3
claim, P4 DATA/EOS, cancellation, TTL, missing-correlation, and cleanup cases.
It is qualified local runtime evidence, not a production-readiness or broad
deployment claim. Production activation remains explicit: the private companion
socket, matching uid/gid, and bounded response-body limit are mandatory. The
default `response-companion=none` compatibility path continues to reject
response-body activation because it cannot transport response EOS. The selected
native HTX route above remains independently available.

### SPOP request-ID byte boundary

The SPOP `request_id` is a correlation key, not a display string. The runtime
validates its original length-delimited bytes before copying it into a C string.
Empty, embedded-NUL, control-byte, non-ASCII, and overlong values are rejected;
for example, `A\0X` can never collapse to `A` and address the same transaction
cache slot. A nonempty printable-ASCII ID, including the normal UUID form,
remains accepted. A malformed `request_id` fails the notification extraction
and does not create, replace, or claim a transaction.

## Historical SPOE/SPOP compatibility

The files under <code>examples/haproxy/compatibility-spoe/</code> are
historical request/header compatibility examples. They are not the logical
response-companion bridge described above and are not the selected native HTX
route. In particular, their `http-response send-spoe-group` examples do not
transport response-body chunks or response EOS. They must not be used to
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
