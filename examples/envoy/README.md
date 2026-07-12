# Envoy ext_proc examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: Envoy ext_proc with a repository-owned gRPC processor. The
[Safe template](safe/envoy-ext-proc-streaming.yaml.in) uses STREAMED request and
response body modes. Together with
[safe/envoy-ext-proc-service.json](safe/envoy-ext-proc-service.json), it is the
native HTTP/1.1 P1--P4 Safe reference.

P1 is request headers, P2 request body, P3 response headers, and P4 response
body. Safe means a late P4 result is recorded as log-only rather than claimed as
a late HTTP status change or deterministic stream reset. The template does not
promise a full connector response buffer, a client-observed first byte, or a
Strict post-commit abort. No Strict file is supplied.

The old [ext_authz compatibility example](compatibility-ext-authz/README.md)
is explicitly request-phase only. It must not be used to describe P3/P4
coverage.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/README.md](minimal/README.md) | Documentation | Why there is no separate native request-only template. |
| [safe/envoy-ext-proc-streaming.yaml.in](safe/envoy-ext-proc-streaming.yaml.in) | Template | Envoy listener, ext_proc filter, and gRPC/upstream clusters. |
| [safe/envoy-ext-proc-service.json](safe/envoy-ext-proc-service.json) | Service configuration | Bounds and Safe late-action policy for the processor. |
| [rules/README.md](rules/README.md) | Documentation | No-CRS rule source and phase IDs. |
| [expected/p1-p4-safe.md](expected/p1-p4-safe.md) | Documentation | Configuration intent, not run evidence. |
| [compatibility-ext-authz/](compatibility-ext-authz/README.md) | Compatibility | Former request authorization route. |

All paths above are repository-relative from examples/envoy. The generated
runtime configuration must be written outside the checkout.

## Template values and service fields

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| @ENVOY_RELEASE@ | Pinned Envoy release string | Required in the template comment; connector version lock sets it; materialization scope | 1.38.2. It records the intended API release; it is not runtime evidence. |
| @LISTEN_PORT@ | Decimal TCP listener port from 1 through 65535 | Required; connector preparation script sets it; listener scope | 18080. Binding a public address/port changes exposure. |
| @UPSTREAM_PORT@ | Decimal application-backend port | Required; connector preparation script sets it; upstream cluster | 18081. Replace only through the materialization input. |
| @EXT_PROC_PORT@ | Decimal local gRPC processor port | Required; connector preparation script sets it; gRPC cluster | 18083. Keep it private to the trusted Envoy/service boundary. |
| @ADMIN_PORT@ | Decimal Envoy administration port | Required; connector preparation script sets it; admin listener | 19001. Do not expose administration endpoints without an explicit security design. |
| listen_address | Processor host:port string | Required; explicit in JSON; processor scope | 127.0.0.1:18083. It must agree with the ext_proc cluster endpoint. |
| transaction_id_header | HTTP header name | Required; explicit in JSON; transaction scope | x-request-id. It is correlation metadata, not a credential. |
| max_header_count, max_header_name_bytes, max_header_value_bytes, max_total_header_bytes | Positive metadata limits | Required; explicit in JSON; processor scope | 128, 256, 8192, 32768. Lower values reject more traffic; do not remove limits. |
| max_body_chunk_bytes, max_request_body_bytes, max_response_body_bytes, max_grpc_message_bytes | Positive byte limits | Required; explicit in JSON; processor scope | 1048576, 10485760, 10485760, 1114112. These bounds do not imply full response buffering. |
| late_action_policy | Late P4 policy name | Required; explicit in JSON; processor scope | safe. It does not authorize a synthetic late response status or reset. |

The literal @NAME@ values are template markers, not Envoy fields. The
repository materializer replaces them and rejects unresolved markers.

## Validation

From this directory, materialize a private generated configuration outside the
checkout with the repository-owned preparation script:

~~~sh
sh ../../connectors/envoy/config/prepare_envoy_ext_proc_config.sh
~~~

The script prints the generated configuration path. Validate that generated
file with the installed Envoy binary; `/srv/modsecurity-work/envoy-ext-proc.yaml` is only an
example generated path:

~~~sh
envoy --mode validate -c /srv/modsecurity-work/envoy-ext-proc.yaml
~~~

Successful materialization and syntax validation do not prove P1--P4 behavior,
Safe host outcomes, Strict behavior, production readiness, or CRS coverage.

## Related material

- [Envoy connector source and ext_proc boundary](../../connectors/envoy/README.md)
- [Repository examples overview](../README.md)
