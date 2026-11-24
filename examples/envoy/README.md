# Envoy examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Choose `ext_proc` for the repository-owned gRPC processor or `ext_authz`
with its mandatory private-UDS response observer. Both logical solutions have
complete bundles for the four example layouts.

## Complete logical profile matrix

| Logical solution | Off | Safe | Strict | All | P1/P2 | P3/P4 |
| --- | --- | --- | --- | --- | --- | --- |
| ext_proc | [bundle](ext-proc/off/) | [bundle](ext-proc/safe/) | [bundle](ext-proc/strict/) | [bundle](ext-proc/all/) | ext_proc | ext_proc |
| ext_authz | [bundle](ext-authz/off/) | [bundle](ext-authz/safe/) | [bundle](ext-authz/strict/) | [bundle](ext-authz/all/) | ext_authz | Private-UDS ext_proc observer |

The ext_authz observer claims a one-time opaque handle for response processing.
Missing, expired, or mismatched handles fail closed. The harness places its
socket in a private owner-only runtime directory. The source default is
`/run/modsecurity/envoy-ext-authz-companion.sock`. The observer removes
`x-msconnector-response-handle` before upstream routing.

## Files

The standalone [Safe template](safe/envoy-ext-proc-streaming.yaml.in) and
[service JSON](safe/envoy-ext-proc-service.json) provide the ext_proc reference
used by the validation commands below. The [Off template](off/envoy-ext-proc-streaming.yaml.in),
[service JSON](off/envoy-ext-proc-service.json), and
[runtime file](off/msconnector-runtime.conf) provide its Off counterpart.

### DetectionOnly profile

Use [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf)
with the selected ext_proc YAML. Its [rules](rules/detection-only.conf) evaluate
and record matches with disruptive engine actions disabled.

### Disabled profile

[disabled/msconnector-runtime.conf](disabled/msconnector-runtime.conf) sets
`enabled=off`. The YAML still describes the transport. In contrast,
[Engine-Off rules](rules/engine-off.conf) keep the connector active with engine
rule evaluation disabled.

## Template values and service fields

Adapt listener, upstream, processor, and administration endpoints, installed
rules paths, and private runtime/log paths. Keep the processor and admin
endpoints within their trusted service boundary. The processor `listen_address`
must match the ext_proc cluster. Template markers are replaced by the repository
materializer, which rejects unresolved markers.

## Configuration reference

Use the generated [configuration reference](configuration-reference.md) for
YAML fields, service JSON, CLI flags, template markers, and individual
header/chunk/gRPC-message limits. Configure cumulative body inspection limits
and actions in engine rules as described in [Configuration](../../docs/configuration.md).

## P1--P4 Safe intent

The HTTP/1.1 ext_proc reference uses STREAMED request and response body modes.
Safe records a P4 decision after response output starts as log-only. A
configuration file establishes configuration intent. Client-visible behavior
requires a matching host run.

## Off ext_proc reference

`phase4_mode=off` preserves native intervention and error handling with the
additional late policy disabled. Both body directions still require STREAMED
input. `all` selects a real policy value such as `strict`.

## No-CRS rules

Install a reviewed rules file and select it in the runtime configuration. The
[No-CRS baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
is the repository test-profile source. Phase IDs and engine modes are explained
in the [examples overview](../README.md) and [rule examples](../common/rule-examples.md).

## ext_authz compatibility

The older [HTTP ext_authz example](compatibility-ext-authz/envoy-ext-authz.yaml)
only authorizes requests. Adapt its listener, trusted authorization service,
timeout, header allow-list, and application upstream. Use the complete
`ext-authz/` bundles above when response inspection is required.

## Validation

From `examples/envoy`, use an absolute writable external `BUILD_ROOT` and the
repository preparation script. OpenSSL creates private one-day loopback test
credentials for this example.

~~~sh
export TLS_CERTIFICATE="$BUILD_ROOT/envoy-ext-proc/runtime-smoke/envoy-loopback.crt"
export TLS_PRIVATE_KEY="$BUILD_ROOT/envoy-ext-proc/runtime-smoke/envoy-loopback.key"
umask 077
mkdir -p "$(dirname "$TLS_CERTIFICATE")"
openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 1 \
  -subj /CN=127.0.0.1 -addext subjectAltName=IP:127.0.0.1 \
  -keyout "$TLS_PRIVATE_KEY" -out "$TLS_CERTIFICATE"
TEMPLATE="$PWD/safe/envoy-ext-proc-streaming.yaml.in" \
  TLS_CERTIFICATE="$TLS_CERTIFICATE" TLS_PRIVATE_KEY="$TLS_PRIVATE_KEY" \
  sh ../../connectors/envoy/config/prepare_envoy_ext_proc_config.sh
~~~

The script prints the generated configuration path. Validate it with the
installed Envoy binary using the default output path below, or the actual path
printed by the script if overridden.

~~~sh
envoy --mode validate -c "$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml"
~~~

Materialization and syntax checks establish file preparation and host loading.
Use the [testing guide](../../docs/testing-and-evidence.md) for runtime validation.

## Strict profile boundary <a id="strict-profile-boundary"></a>

The ext_proc service accepts `late_action_policy: strict` with matching
`phase4_mode=strict`. Late ImmediateResponse uses the pinned Envoy host's
local-reply path, which resets the affected downstream stream after headers
are encoded. The Framework H2 adapter checks the reset alongside a healthy
peer and follow-up request. Verify that host outcome for the selected run.

## Related material

- [Envoy connector guide](../../connectors/envoy/README.md)
- [Repository examples overview](../README.md)
