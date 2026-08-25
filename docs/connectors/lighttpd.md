# lighttpd Connector

**Language:** English | [Deutsch](lighttpd.de.md)

## Overview

lighttpd uses the selected <code>patched-native-lighttpd</code> route with
<code>mod_msconnector.so</code>. The selected profile is HTTP/1.1-focused and
uses a versioned patched-host boundary for borrowed body ranges. It does not
claim production readiness, security verification, CRS verification, complete
matrix coverage, HTTP/2/HTTP/3 coverage, or canonical P4 runtime evidence.

The separately supported stock native ABI emits
<code>native-lighttpd-plugin</code> in raw event evidence. It must never be
represented as <code>patched-native-lighttpd</code>; this is an ABI provenance
property, not a promotion of Stock body or lifecycle capabilities.

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

### Stock lifecycle evidence (bounded)

The run-scoped evidence under
`lighttpd-stock-lifecycle-v6-v10-20260825T100000Z` is a bounded HTTP/1.1
host exercise, not full 17-vector acceptance. Its fail-safe boundary is
explicit:

| Case | Observed behavior | Evidence boundary |
|---|---|---|
| V6 client close | Direct client-cancel propagation and a typed Stock connector event were not observed or claimed. A 2-second gateway/proxy backend read-timeout contained the request, emitted host `read timeout on socket`, and a same-host follow-up returned `200`. | Host timeout fallback; no direct Stock abort-event claim |
| V7/V11 truncated upstream response | The raw upstream truncation fixture closed and the bounded harness completed cleanup. | Host/transport closure only; no typed connector event claim |
| Bounded parallelism | Eight parallel HTTP/1.1 requests returned `200`. | Subset observation; V14 and full matrix remain `NOT_EXECUTED` |
| Host termination | The active client received EOF, then restart controls returned `200 -> 403 -> 200`. | Bounded host lifecycle observation; V12--V15 remain `NOT_EXECUTED` |
| Cleanup | pidfd/session/port/UDS receipts passed for the first and replacement host. | Run-scoped cleanup receipt; no full leak audit claim |

The run does not claim a Stock-specific event for V6, direct cancel
propagation, a complete HTTP/protocol status mapping for the client-close
fallback, or full V12--V15/17-vector coverage. The historical five-second
frontend-timeout receipts remain separate FND-PARENT-0311 evidence.

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

## No-CRS fixture isolation

The patched lifecycle's No-CRS baseline uses the trusted private-namespace
runner documented in the [harness guide](../../connectors/lighttpd/harness/README.md).
Root-owned `/usr/bin/unshare`, fixed `/usr/bin/dash` and `/usr/bin/mount`, and
then `/usr/bin/bwrap` establish the user, mount, and PID boundary. The shell
setup makes propagation private and mounts a private `nosuid,nodev,noexec`
tmpfs at `/tmp`. Bwrap exposes only the minimal read-only system and runtime
binds needed by the harness plus the exact task-owned smoke root as the sole
writable bind. The fixture root is mode-0700.

Namespace setup is capability-gated. After setup the runner verifies that all
capability sets, including the bounding and ambient sets, are empty and that
`no_new_privs` is enabled before the test harness runs. Any missing kernel
capability or failed attestation aborts closed; the former pathname
check-then-`rmdir` cleanup is not a fallback.

Fixture cleanup is tied to child and namespace lifetime. Normal completion,
test error, timeout, signal, helper failure, and partial initialization all
terminate the child group and release the private namespace. The final
namespace-state verifier checks only capability sets, `no_new_privs`, mount
state, and the fixed fixture-root device/inode (`dev:ino`) identity. The
descriptor-I/O cleanup command separately verifies the allowlisted fixture-leaf
inventory, retains every leaf, and neither unlinks nor re-resolves the fixture
pathname. All leaves and the directory disappear when the private tmpfs
namespace is torn down.

Threat model: a same-UID process can race the old fixture pathname by renaming,
replacing, or recreating it. The private namespace and controlled writable root
ensure that releasing the namespace removes the fixture mounts without
deleting a replacement selected through the host pathname.

The current nested local container exposes only a one-entry UID/GID mapping,
so the complete non-root production entry path cannot be exercised locally.
This is a validation limitation, not permission to weaken the fail-closed
prerequisite checks.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [lighttpd configuration reference](../../examples/lighttpd/configuration-reference.md)
