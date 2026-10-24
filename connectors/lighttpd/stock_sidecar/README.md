# Stock lighttpd traffic-owning sidecar

**Language:** English | [Deutsch](README.de.md)

This is the canonical full-lifecycle route for the named Stock lighttpd
solution. Its topology is deliberately small and closed:

```text
client -> Common Runtime sidecar -> private, unchanged Stock lighttpd backend
```

The sidecar creates the Common Runtime with connector ID `lighttpd` and exact
integration mode `stock-lighttpd-sidecar`. It owns P1–P4 directly: P1 after
request headers, P2 at request-body EOS, P3 before response commitment, and
P4 at response-body EOS. The direct Stock `mod_msconnector` module remains a
separate, exact P1/P3 compatibility translation (`stock-lighttpd`); do not
load it in this backend topology, or P1/P3 would be evaluated twice.

## Boundary and framing

The sidecar has no TLS, authentication, or public-listener layer. Both
`--listen` and `--upstream` must therefore be literal IPv4 loopback endpoints
of the form `127.0.0.1:<port>`; wildcard addresses, hostnames, IPv6, and
non-loopback upstreams are rejected at startup. A deployment that needs a
network, TLS, or shared trust boundary must terminate it outside this
component and retain an equivalent private traffic owner.

Only one HTTP/1.1 exchange is accepted per client connection. The sidecar
closes that connection after the exchange, so it has no cross-request state or
reuse correlation. It supports identity framing with an optional request
`Content-Length` and a response `Content-Length` (except HEAD, 204, and 304).
Ordinary HTTP/1.1 response reason phrases and `Connection: close`/
`keep-alive` are accepted; connection fields are stripped before forwarding.
Non-upgrade informational `1xx` responses are forwarded within the configured
bounds and never enter P3; only the following final response enters P3. A
`101` upgrade remains rejected.
Chunked transfer encoding, upgrades, TE, Trailer, Proxy-Connection, unknown
Connection tokens, conflicting lengths, malformed start lines, and oversized
headers or bodies fail closed.

The configured Common header/body/event limits remain authoritative. Request
parsing is bounded by its declared limit. Response handling uses one fixed
bounded chunk at a time rather than a complete response copy; those bytes never
enter event JSONL. A declared request or response body above the configured
bound returns the configured body-limit response (normally 413), records the
typed `body_limit` terminal state, and does not silently release the request or
response.

## Failure and cleanup semantics

One absolute exchange deadline covers client reads, upstream connect/read/
write, and client output. All worker sockets remain nonblocking; `poll()` and
deadline-aware I/O handle EAGAIN/EWOULDBLOCK/EINTR, so a non-reading peer
cannot keep a worker in `send()` beyond that deadline. Engine timeout,
connector error, protocol error, client cancel, and upstream disconnect use
their distinct shared terminal error classes. When a failure response reaches
the client, the Common Runtime records that actual HTTP host action; when it
cannot reach the client, it records a connection abort instead.

The sidecar maps and writes response headers before the body. It then reads one
bounded response chunk, appends that chunk once to Common/libModSecurity, and
writes it to the client before reading another chunk. It calls the P4 finish
operation exactly once at response EOS. A disruptive P4 result can therefore
be late: after a committed prefix Safe records `log_only` and continues;
Strict shuts down the client connection rather than attempting a retroactive
HTTP deny or redirect. The Runtime marks response commitment only after
response headers were actually written, and records body start only after bytes
were sent.

There are at most 16 detached exchange workers. A seventeenth simultaneous
client receives 503 without creating transaction state. Every worker owns one
transaction, terminalizes it, destroys it, and decrements the active count
before process shutdown can destroy the shared Runtime.

## Build and local component test

Use the normal external build root and the same libModSecurity installation as
the other C connectors:

```sh
export MODSECURITY_INCLUDE_DIR=/absolute/path/to/include
export MODSECURITY_LIB_DIR=/absolute/path/to/lib
export BUILD_ROOT=/var/tmp/ModSecurity-conector-build
make -C connectors/lighttpd build-lighttpd-stock-sidecar
make -C connectors/lighttpd self-test-lighttpd-stock-sidecar
```

The self-test compiles/runs the real C sidecar on loopback with a fake private
upstream. It covers P1–P4 allow/block paths, multi-chunk P2/P4, response EOS,
body/header limits, unsafe framing, timeout, client cancel, bounded
parallelism, connection reuse, and non-reading-client deadline cleanup. It is
sidecar component evidence, not a claim that an unmodified Stock lighttpd
process has native body hooks.

`runtime-begin-smoke` is installed beside the sidecar. It verifies the exact
Common profile and streaming P2/P4 configuration against a real runtime
configuration before deployment.

## Real Stock-host evidence attestation

`build-lighttpd-stock-sidecar` writes
`stock-sidecar-artifact.manifest` beside the two Sidecar binaries. It records
the Parent revision, C17 mode, exact binary hashes, and the bounded Common/
runtime build-input hash. That hash includes stable repository-relative names
and content digests for every direct Sidecar/Common compile input, including
the private runtime, registry, and header-validation headers. The manifest is
build metadata only: because it is written with the selected artifact, it is
not an independent authenticity claim.

The real backend target therefore additionally requires
`STOCK_SIDECAR_ARTIFACT_ATTESTATION` to name an operator-supplied, regular,
non-symlink, non-group/world-writable file outside the selected Stock build,
Sidecar, and runtime roots. It has this exact key/value tuple (all digests are
lowercase SHA-256):

```text
schema_version=1
attestation_kind=operator_expected_artifact_tuple
connector_id=lighttpd
integration_mode=stock-lighttpd-sidecar
parent_commit_sha=<40-or-64-hex-parent-revision>
parent_source_tree_state=<clean-or-dirty>
lighttpd_version=<selected-version>
lighttpd_source_sha256=<selected-source-digest>
stock_lighttpd_binary_sha256=<host-binary-digest>
stock_lighttpd_mod_accesslog_sha256=<loaded-module-digest>
stock_lighttpd_staticfile_linkage=builtin
sidecar_binary_sha256=<sidecar-digest>
sidecar_source_inputs_sha256=<bounded-build-input-digest>
sidecar_modsecurity_library_sha256=<linked-library-digest>
sidecar_c_standard=c17
```

The selected contract build has `mod_staticfile` linked into the exact host
executable, while `mod_accesslog.so` is the dynamically loaded module. The
harness verifies the exported `mod_staticfile_plugin_init` symbol in the
attested executable and verifies the exact regular, non-writable dynamic
module digest. It rejects aliases and writable non-sticky ancestry for every
selected artifact path, then rechecks the launch binary/module and attestation
digests immediately before it starts either process. It verifies every tuple
value before it runs `lighttpd -v` and copies only bounded identity metadata
and hashes into the payload-free verified receipt. A missing, malformed,
writable, aliased, in-tree, or mismatched tuple fails closed. The
operator-supplied tuple makes the local trust boundary explicit; it is not a
cryptographic defense against a same-UID actor that controls both artifacts
and the operator input.
