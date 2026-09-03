# lighttpd Connector

**Language:** English | [Deutsch](lighttpd.de.md)

## Overview

The canonical Stock solution uses the selected traffic-owning
<code>stock-lighttpd-sidecar</code>; the separately documented
<code>patched-native-lighttpd</code> route remains a distinct solution with
<code>mod_msconnector.so</code>. The selected profile is HTTP/1.1-focused and
uses a versioned patched-host boundary for borrowed body ranges. It does not
claim production readiness, security verification, CRS verification, complete
matrix coverage, HTTP/2/HTTP/3 coverage, or canonical P4 runtime evidence.

The <code>lighttpd-stock</code> logical solution is the traffic-owning
<code>stock-lighttpd-sidecar</code>: it binds only to literal private loopback,
speaks bounded HTTP/1.1, and owns one complete client/backend exchange in one
worker. It executes P1--P4 directly without a cross-process correlation handle
or TTL registry. Its event JSONL is metadata-only and never carries body
payloads. The unmodified native Stock module is an explicit noncanonical P1/P3
compatibility translation, never a silent fallback. The patched route remains a
separate direct P1--P4 solution.

## Architecture and ownership

The plugin lifecycle layer is host-owned and the mapper is the only lighttpd
API translation layer. Common Runtime and Common SDK types remain free of
lighttpd callback types. A runtime is initialized from server-scoped
configuration; each request receives its own transaction and mapper storage
until request reset.

| Lifecycle area | Selected lighttpd responsibility | Boundary |
| --- | --- | --- |
| P1 | Map URI/request headers and apply an eligible request decision | The narrow smoke is not a broad host guarantee |
| P2 | Inspect patched borrowed request-body ranges while the selected HTTP/1.1 `mod_proxy` gate buffers until EOS | Only a Phase-2 allow may reach the upstream; this is not general upstream streaming |
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

## HTTP/1.1 pre-upstream Phase-2 gate

For `request_body_mode=streaming`, the selected patched HTTP/1.1 `mod_proxy`
profile suppresses active host request streaming before each body read. The
host therefore buffers request bytes until terminal EOS and the Phase-2 allow
decision; only then may the proxy connect and forward the request. The
validated delayed allow control was reframed as `Content-Length` upstream.

The profile requires `mod_proxy` before `mod_msconnector`, a positive Common
request-body limit, `body_limit_action=reject`, and the matching
patched host/module pair. It rejects preconfigured `server.stream-request-body`,
`Incremental`, and explicitly enabled body-bearing `Upgrade` plus
`gw.upgrade-with-request-body` requests with `501` before upstream connection.
A streaming configuration with `body_limit_action=process_partial` is rejected
at configuration load before a listener or upstream connection exists. This is
not a claim for HTTP/2, HTTP/3, other stream handlers, response-body P4,
unrestricted upstream streaming, or production readiness.

The retained-body bound relies on the positive Common `request_body_limit`
(default 1 MiB) and a rejecting read cycle. The module does not configure
`server.max-request-size`; that remains an independent host defense-in-depth
limit.

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
`connectors/lighttpd/harness/run_phase2_pre_upstream_gate.py` additionally
provides a repository-owned, payload-safe loopback proof: a delayed Phase-2
marker returned `403` with zero preterminal upstream connections, and a
delayed benign chunked request reached the upstream only after EOS/allow.
The same runner proves the profile-local `process_partial` configuration
rejection without retaining a request payload.
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
