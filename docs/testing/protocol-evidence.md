# HTTP/2 and HTTP/3 protocol evidence

**Language:** English | [Deutsch](protocol-evidence.de.md)

This contract is for a real `client → native host → connector` run. It does
not turn a build flag, an ALPN configuration, a proxy in front of the host, or
an internal stream failure into protocol evidence.

## Canonical values

| Field | Values |
|---|---|
| `requested_protocol`, `downstream_protocol`, `upstream_protocol`, `negotiated_protocol` | `http1`, `h2`, `h2c`, `h3` |
| `transport` | `tcp`, `tls_tcp`, `quic_udp` |
| H2 TLS | `alpn=h2`, `transport=tls_tcp` |
| H2C | `transport=tcp`, no TLS ALPN claim |
| H3 | `alpn=h3`, `transport=quic_udp`, `fallback_used=false`, `quic_connection_id_present=true`, bounded `quic_version` |

Downstream and upstream protocol are independent. For example, an Envoy H3
downstream with an HTTP/1 upstream is represented as `h3` / `http1`; it does
not imply upstream H3 support.

## Managed client

Run the framework-owned helper rather than a hand-written curl command:

```sh
cd modules/ModSecurity-test-Framework
python3 ci/protocol_client.py \
  --url https://127.0.0.1:8443/no-crs/deny \
  --protocol h2 \
  --artifact-dir /absolute/evidence/client-h2 \
  --connector nginx \
  --integration-mode native-nginx-http-module \
  --run-id example-run \
  --transaction-id tx-1 \
  --transport-case-id nginx-h2-p1-001 \
  --rule-id 1100001 \
  --phase 1 \
  --stream-id 1 \
  --observation-sidecar /absolute/evidence/h2-sidecar.json
```

The helper forces `--http2`, `--http2-prior-knowledge`, or `--http3-only` as
appropriate. It never uses fallback-capable `--http3` for an H3 claim. H3 is
`BLOCKED` before a network request when the selected curl lacks the `HTTP3`
feature; that is an environment blocker, not a connector `UNSUPPORTED` claim.

Each invocation atomically writes only:

- `client-version.txt`
- `client-features.txt`
- `client-command.txt`
- `client-protocol-observation.json`

Response bodies go to the null device. The command artifact redacts request
headers, body paths, CA paths, and query strings. The observation rejects raw
QUIC connection IDs; it accepts only `quic_connection_id_present`.

For H2/H2C/H3, `--transport-case-id` is required. The helper sends it only as
the bounded `X-MSConnector-Transport-Case` request header, redacts that header
in `client-command.txt`, and retains the token as metadata. The matching
native connector event and canonical case result must carry exactly the same
token; a copied bundle cannot be relabelled to another transaction or stream.
Caller-supplied headers with that name are rejected case-insensitively: the
helper is the sole writer of the causal correlation header.
One managed bundle represents one request, so independently promotable modern
protocol cases use separate canonical runs until a multiplexing client exists.

For H2/H3, curl alone cannot supply every stream fact. The optional JSON
sidecar has a deliberately small vocabulary: stream ID, ALPN,
`quic_udp_observed`, QUIC CID presence/version, connection reuse, and
stream-reset facts. It cannot contain request/response payloads, headers,
stderr, URLs, or a raw CID.

## Strict post-commit resets

An H2/H3 Strict result is valid only when all of the following are true:

- the canonical connector event and case result bind connector, integration
  mode, run ID, transaction ID, rule ID, phase, requested/actual action, and
  stream ID;
- the response was committed and at least one body byte was visible to the
  client;
- the response is incomplete, with no invented later HTTP 403;
- `actual_action=stream_reset`, `stream_reset=true`, a reset code, and
  `transport_result=stream_reset` are recorded;
- H3 additionally proves negotiated `h3`, `quic_udp`, `alpn=h3`, and no
  fallback; and
- an independent forced-profile health request succeeds.

The present managed curl helper is deliberately negotiation-only: it cannot
issue or independently decode a stream-level reset/cancel or multiplexed
peers. It therefore cannot promote Strict, reset/cancel, or multiplexing
cases; those remain `NOT EXECUTED` until a dedicated stream-control client is
provisioned. The checker retains the Strict contract so that such a client has
an exact non-promoting acceptance gate.

Pass `--followup-url` for the independent health request. It produces the
additional payload-free `client-followup-observation.json` needed by strict
validation. The helper derives a distinct bounded follow-up
`transport_case_id` and persists it together with a non-reversible
`target_authority_sha256`; strict validation requires that different token and
the same target-authority hash, while retaining neither raw URL nor request
payload. Then validate the client side explicitly:

```sh
python3 ci/check_protocol_evidence.py \
  --artifact-dir /absolute/evidence/client-h3-strict \
  --protocol h3 \
  --strict \
  --connector nginx \
  --integration-mode native-nginx-http-module \
  --run-id example-run \
  --transaction-id tx-4 \
  --rule-id 1100301 \
  --phase 4
```

The No-CRS finalizer independently rejects a H2/H3 `PASS` without matching
canonical event provenance. For a canonical full-lifecycle run, pass the
client bundle through `no_crs_baseline.py finalize` with
`--protocol-client-artifact-dir`; it is copied under
`inventory/protocol-client/` with manifest checksums before a modern-protocol
PASS is retained. The root full-lifecycle runner forwards an explicit,
regular, non-symlinked `NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR` only when it is
inside that invocation's raw run. Alternatively,
`NO_CRS_PROTOCOL_CLIENT=1` makes the runner reserve its own
`raw-run/protocol-client` directory; an absent optional bundle is explicitly
non-promoting when the selected host cannot start its protocol path. Run both
gates; neither replaces the other.

## NGINX profiles

The managed NGINX profiles are `h1` (default), `h1-h2`, and
`h1-h2-h3-quic`. H2/H3 profiles use profile-specific build paths and cache
identities. The H3 profile requires pinned TLS/QUIC source inputs and checks
`nginx -V` for `--with-http_ssl_module`, `--with-http_v2_module`, and
`--with-http_v3_module`. A successful build remains build provenance until a
forced client and matching events pass the gates above.

For H2/H3 local listeners, the harness creates an ephemeral test CA and a
separately issued one-day `localhost`/`127.0.0.1` leaf certificate. It records
TCP and UDP listener facts separately even when they use the same port. It
does not test 0-RTT; `http3_0rtt` remains `NOT EXECUTED`.

An opt-in NGINX H2/H3 invocation runs the managed forced client through a
ModSecurity-enabled Allow route while that listener is alive and keeps its
payload-free bundle in the fresh raw run:

```sh
NO_CRS_RUN_ID="protocol-nginx-$(date -u +%Y%m%dT%H%M%SZ)" \
NO_CRS_PROTOCOL_CLIENT=1 \
NGINX_PROTOCOL_PROFILE=h1-h2 \
NGINX_DOWNSTREAM_PROTOCOL=h2 \
make full-lifecycle-nginx
```

The bounded harness supplies its own fixed probe token so the managed client
can make the forced request, but no native event or catalog case adopts that
token. It intentionally supplies neither a synthetic stream ID nor an ALPN
sidecar. Thus a successful forced negotiation is recorded as `NOT_EXECUTED`
until a native event and a protocol case establish the required stream/case
correlation; it cannot promote an H2/H3 capability by itself.

## CI split

The `protocol-contract` workflow runs the payload/privacy/client and NGINX
profile-contract checks on pull requests. Its scheduled/manual matrix builds
the `h1-h2` and `h1-h2-h3-quic` NGINX profiles, emits a forced client
preflight artifact for each, and uploads only the payload-free bundle. A
no-listener preflight is explicitly not connector runtime evidence; an H3
`BLOCKED` observation is reported as a client-environment condition.

See [the transport-hardening audit](../../reports/transport-hardening-audit.md)
for current connector-specific boundaries and deliberately unmade claims.
