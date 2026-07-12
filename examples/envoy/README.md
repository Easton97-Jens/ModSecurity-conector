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
Strict post-commit abort. The [Strict profile boundary](#strict-profile-boundary) documents
the optional boundary without claiming a strict transport result.

The [ext_authz compatibility example](#ext_authz-compatibility) is explicitly
request-phase only. It must not be used to describe P3/P4 coverage.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in) | Template | Minimal streamed ext_proc transport shape. |
| [minimal/envoy-ext-proc-service.json](minimal/envoy-ext-proc-service.json) | Service configuration | Validated processor limits for the minimal profile. |
| [minimal/msconnector-runtime.conf](minimal/msconnector-runtime.conf) | Runtime configuration | Common Runtime profile with `phase4_mode=minimal`. |
| [safe/envoy-ext-proc-streaming.yaml.in](safe/envoy-ext-proc-streaming.yaml.in) | Template | Envoy listener, ext_proc filter, and gRPC/upstream clusters. |
| [safe/envoy-ext-proc-service.json](safe/envoy-ext-proc-service.json) | Service configuration | Bounds and Safe late-action policy for the processor. |
| [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Runtime configuration | DetectionOnly rules with the selected ext_proc transport; see [DetectionOnly profile](#detectiononly-profile). |
| [disabled/msconnector-runtime.conf](disabled/msconnector-runtime.conf) | Runtime configuration | Runtime disabled while host YAML stays transport-only; see [Disabled profile](#disabled-profile). |
| [rules/detection-only.conf](rules/detection-only.conf) | Rules | DetectionOnly engine settings. |
| [rules/engine-off.conf](rules/engine-off.conf) | Rules | Engine-Off settings, distinct from disabling the connector. |
| [No-CRS rules](#no-crs-rules) | Documentation | No-CRS rule source and phase IDs. |
| [P1--P4 Safe intent](#p1-p4-safe-intent) | Documentation | Configuration intent, not run evidence. |
| [Minimal ext_proc reference](#minimal-ext_proc-reference) | Documentation | Complete minimal streamed transport shape. |
| [ext_authz compatibility](#ext_authz-compatibility) | Compatibility | Former request authorization route. |

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

## Configuration reference

The generated [configuration reference](configuration-reference.md) documents
the ext_proc YAML paths, service JSON contract, CLI flags, materializer
placeholders, and the separate ext_authz compatibility entry.

| Setting | Layer | Task |
| --- | --- | --- |
| `envoy.filters.http.ext_proc` | Host / Connector | Sends the selected request/response lifecycle to the processor. |
| `SecRuleEngine` | ModSecurity Engine | Selects engine enforcement, DetectionOnly, or Off in the runtime rule file. |
| `request_body_mode` | Common Runtime | Selects required streamed request-body input for the native bridge. |
| `response_body_mode` | Common Runtime | Selects required streamed response-body input for the native bridge. |
| `late_action_policy` | Connector service | Records minimal, safe, or strict post-commit policy without fabricating a status. |

Removing `ext_proc` disables the connector path. `SecRuleEngine Off` leaves
the processor route present but disables engine rule evaluation. ext_authz is
compatibility-only and is not a P3/P4 substitute.

## Profiles

### DetectionOnly profile

`detection-only/msconnector-runtime.conf` is used with the selected ext_proc
YAML and selects DetectionOnly rules. DetectionOnly loads and evaluates engine
rules and records matches, but it does not apply disruptive engine actions.

After adapting the host paths, use the connector validation command below.
This profile is configuration guidance, not runtime evidence.

### Disabled profile

`disabled/msconnector-runtime.conf` sets `enabled=off`; the host YAML remains
a separate ext_proc transport configuration. This is distinct from
`SecRuleEngine Off`, which leaves an active host connector but disables rule
evaluation inside the engine.

After adapting the host paths, use the connector validation command below. Do
not infer P1--P4 behavior from a disabled profile.

## P1--P4 Safe intent

The ext_proc reference sets both body modes to STREAMED and the service policy
to safe. It is the native full-lifecycle reference. A P4 result after the
response begins is represented as Safe log-only behavior, not as a claimed
late HTTP status change or deterministic stream reset.

The separate ext_authz configuration cannot observe upstream response headers
or bodies and therefore is intentionally not described as a P3/P4 core path.
No Strict example is supplied.

## No-CRS rules

The ext_proc service loads the reviewed, installed rules file selected by its
runtime configuration. The repository source for the No-CRS profile is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

## Minimal ext_proc reference

The selected Envoy core needs streamed ext_proc input in both directions. The
minimal files supply a complete transport shape in
[envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in),
its validated service contract, and a paired Common Runtime file with
`phase4_mode=minimal`. It is not a request-only native path: the bridge still
requires STREAMED request and response body modes. The separate
[ext_authz request-only material](#ext_authz-compatibility) remains
compatibility-only.

## ext_authz compatibility

The retained file is the former request-phase Envoy example. It configures an
HTTP ext_authz call before routing to the upstream and remains separate from
the streamed ext_proc core in [safe/](safe/).

### Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- |
| listener socket address and port_value | TCP listener address and decimal port | Required; YAML static resources; listener scope | 0.0.0.0:8080. Bind loopback for a local exercise unless exposure is intentional. |
| modsecurity_authz | ext_authz cluster name | Required; YAML cluster and filter; filter scope | Endpoint 127.0.0.1:9000. It must be a trusted authorization service. |
| server_uri and timeout | Authorization HTTP URI and positive duration | Required; ext_authz filter; request scope | http://127.0.0.1:9000 and 0.2s. A timeout is not response-phase evidence. |
| authorization and content-type | Allowed request-header names | Optional filter allow-list; request scope | Header names only, not secret values. Do not put credentials in this file. |
| app_backend | Upstream cluster name and endpoint | Required; route and cluster; route scope | 127.0.0.1:8081. Replace with the intended application endpoint. |

[ext_authz configuration](compatibility-ext-authz/envoy-ext-authz.yaml) does
not make the later upstream response available to this service. It is not
P3/P4, Safe late-intervention, Strict, first-byte, or no-buffer evidence.

## Validation

From this directory, materialize a private generated configuration outside the
checkout with the repository-owned preparation script:

~~~sh
sh ../../connectors/envoy/config/prepare_envoy_ext_proc_config.sh
~~~

The script prints the generated configuration path. Validate that generated
file with the installed Envoy binary; the default is under the documented
`$BUILD_ROOT` outside the checkout:

~~~sh
envoy --mode validate -c "$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml"
~~~

Successful materialization and syntax validation do not prove P1--P4 behavior,
Safe host outcomes, Strict behavior, production readiness, or CRS coverage.

## Strict profile boundary <a id="strict-profile-boundary"></a>

The ext_proc service accepts `late_action_policy: strict`, but currently
records `strict_abort_not_attempted` after the commit boundary. Strict is
optional and no late-reset configuration is claimed.

Use the Safe ext_proc template and service contract, validate the generated
YAML and service JSON, and add host evidence before relying on a strict
transport outcome.

## Related material

- [Envoy connector source and ext_proc boundary](../../connectors/envoy/README.md)
- [Repository examples overview](../README.md)
