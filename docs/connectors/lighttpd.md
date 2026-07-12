# lighttpd Connector

**Language:** English | [Deutsch](lighttpd.de.md)

## Overview

lighttpd uses the selected <code>patched-native-lighttpd</code> route with
<code>mod_msconnector.so</code>. The selected profile is HTTP/1.1-focused and
uses a versioned patched-host boundary for borrowed body ranges. It does not
claim production readiness, security verification, CRS verification, complete
matrix coverage, HTTP/2/HTTP/3 coverage, or canonical P4 runtime evidence.

## Architecture and ownership

The plugin lifecycle layer is host-owned and the mapper is the only lighttpd
API translation layer. Common Runtime and Common SDK types remain free of
lighttpd callback types. A runtime is initialized from server-scoped
configuration; each request receives its own transaction and mapper storage
until request reset.

| Lifecycle area | Selected lighttpd responsibility | Boundary |
| --- | --- | --- |
| P1 | Map URI/request headers and apply an eligible request decision | The narrow smoke is not a broad host guarantee |
| P2 | Use the patched borrowed request-body range only in the selected mode | Buffered request mode remains outside the selected path |
| P3 | Map response metadata at response start | Response status/action semantics remain host-specific |
| P4 | Receive identity entity ranges before HTTP/1 transfer framing and finish once at EOS | No socket-queue callback or connector-owned body queue |
| Cleanup | Release mapper storage and transaction at request reset | Static lifetime checks are not long-running resilience evidence |

## Build

Use [the lighttpd compiler guide](../build/compilers/lighttpd.md) for the
native module, patched host, ABI checks, source inputs, and configuration
loading. The [lighttpd source guide](../../connectors/lighttpd/README.md)
remains the code-adjacent entry point. Build/load/start stages are separate
from request traffic and evidence promotion.

## Configuration

The complete server/plugin/Common Runtime syntax, defaults, scopes,
compatibility fields, profiles, and validation details are in the
[lighttpd configuration reference](../../examples/lighttpd/configuration-reference.md).
The selected native profile is separate from the retained sidecar-proxy
compatibility example.

## P1--P4 lifecycle and entity-body boundary

The patched host calls the selected response callback on synchronous borrowed
identity entity ranges before transfer framing. It advances a monotonic entity
offset and signals EOS once. Later socket short writes or retry handling must
not duplicate an already ingested entity range; this is a source/static
contract, not a fault-injection runtime claim.

| P4 question | Current boundary |
| --- | --- |
| Response-body hook | Patched identity entity-body source path exists |
| Safe/minimal result | Preserve visible response and record conservative <code>log_only</code> behavior |
| Strict result | Explicitly not executed without a client-validated host abort primitive |
| Streaming/limits | Requires a real selected host/client artifact for promotion |

gzip/br, HTTP/2, unexamined file/zero-copy output, short-write fault injection,
and unselected buffering modes are outside the selected contract.

## Testing and evidence

Use <code>make check-lighttpd-config</code> for real module/configuration
loading and the selected lifecycle target for a run-scoped host exercise.
The narrow native smoke can establish only its stated request-path observation.
P4 and late-intervention facets remain not executed or capability-selected
until real host/client artifacts establish their timing and visible outcome.
See [Testing and evidence](../testing-and-evidence.md).

## Operations and troubleshooting

Stage the matching patched core and module together in an external build root.
For loader/config failures inspect ABI markers, module directory selection,
Common Runtime configuration, rule load, and the real <code>lighttpd -tt</code>
output. Keep module, runtime, log, and evidence paths outside the checkout.

## Limitations and compatibility

The legacy sidecar proxy is compatibility-only and does not become native
lighttpd behavior. The selected evidence profile does not establish P4 rule
evaluation, visible late action, abort, response truncation, full CRS behavior,
or production hardening without dedicated artifacts.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [lighttpd configuration reference](../../examples/lighttpd/configuration-reference.md)
