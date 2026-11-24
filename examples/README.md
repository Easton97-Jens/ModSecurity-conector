# Connector examples

**Language:** English | [Deutsch](README.de.md)

Choose your host and topology, then adapt the matching example. For an existing
installation, check [Migration](../docs/migration.md) before reusing options.

## Choose a host

| Host family | Example guide | Logical profiles |
| --- | --- | --- |
| Apache | [Apache](apache/README.md) | `apache` |
| NGINX | [NGINX](nginx/README.md) | `nginx` |
| HAProxy | [HAProxy](haproxy/README.md) | `haproxy-htx`, `haproxy-spoe-spop` |
| Envoy | [Envoy](envoy/README.md) | `envoy-ext-proc`, `envoy-ext-authz` |
| Traefik | [Traefik](traefik/README.md) | `traefik-native-uds`, `traefik-forwardauth` |
| lighttpd | [lighttpd](lighttpd/README.md) | `lighttpd-patched`, `lighttpd-stock` |

See the [body-inspection matrix](../docs/body-inspection-review-matrix.md)
for the request-body visibility, response companion requirements and
late-action limits of each profile.

## Choose a configuration layout

| Layout | Use |
| --- | --- |
| `off` | Keep native intervention and error handling, with engine inspection governed by the configured rules. |
| `safe` | Start here to learn the profile's conservative handling of late decisions. Native Reject results and processing errors still apply. |
| `strict` | Select the profile's strict late action. Startup requires host support for that action. |
| `all` | Consult the complete configuration reference. The example selects a real Phase-4 mode, often `strict`, with the same startup requirements. |

`SecRuleEngine DetectionOnly`, `SecRuleEngine Off`, host disablement and
Phase-4 `off` act at different layers. See [rule examples](common/rule-examples.md).

## Ten logical solutions

| Logical connector solution | Off | Safe | Strict | All |
| --- | --- | --- | --- | --- |
| Apache | [off](apache/off/httpd.conf) | [safe](apache/safe/httpd.conf) | [strict](apache/strict/httpd.conf) | [all](apache/all/httpd.conf) |
| NGINX | [off](nginx/off/nginx.conf) | [safe](nginx/safe/nginx.conf) | [strict](nginx/strict/nginx.conf) | [all](nginx/all/nginx.conf) |
| HAProxy HTX | [off](haproxy/off/haproxy-htx.cfg) | [safe](haproxy/safe/haproxy-htx.cfg) | [strict](haproxy/strict/haproxy-htx.cfg) | [all](haproxy/all/haproxy-htx.cfg) |
| HAProxy SPOE/SPOP | [off](haproxy/spoe-spop/off/) | [safe](haproxy/spoe-spop/safe/) | [strict](haproxy/spoe-spop/strict/) | [all](haproxy/spoe-spop/all/) |
| Envoy ext_proc | [off](envoy/ext-proc/off/) | [safe](envoy/ext-proc/safe/) | [strict](envoy/ext-proc/strict/) | [all](envoy/ext-proc/all/) |
| Envoy ext_authz | [off](envoy/ext-authz/off/) | [safe](envoy/ext-authz/safe/) | [strict](envoy/ext-authz/strict/) | [all](envoy/ext-authz/all/) |
| Traefik Native UDS | [off](traefik/native-uds/off/) | [safe](traefik/native-uds/safe/) | [strict](traefik/native-uds/strict/) | [all](traefik/native-uds/all/) |
| Traefik forwardAuth | [off](traefik/forwardauth/off/) | [safe](traefik/forwardauth/safe/) | [strict](traefik/forwardauth/strict/) | [all](traefik/forwardauth/all/) |
| lighttpd Patched | [off](lighttpd/patched/off/) | [safe](lighttpd/patched/safe/) | [strict](lighttpd/patched/strict/) | [all](lighttpd/patched/all/) |
| lighttpd Stock | [off](lighttpd/stock/off/) | [safe](lighttpd/stock/safe/) | [strict](lighttpd/stock/strict/) | [all](lighttpd/stock/all/) |

## Compatibility and companion boundaries

The host guides identify standalone compatibility files and the companions
required for response inspection.

- [HAProxy SPOE/SPOP compatibility material](haproxy/README.md#spoespop-compatibility-material)
- [Envoy ext_authz compatibility](envoy/README.md#ext_authz-compatibility)
- [Traefik forwardAuth compatibility](traefik/README.md#forwardauth-compatibility)
- [lighttpd sidecar compatibility](lighttpd/README.md#sidecar-compatibility)

## Values to adapt

Use the selected host guide to adapt module and rules paths, listeners,
upstreams, service identities, private sockets and log destinations.
Review options that require deployment-specific credentials before enabling
them. Keep credentials, keys and sensitive traffic out of examples and logs.

Configure body access, MIME scope, limits and limit actions in the
libModSecurity rules. See [Configuration](../docs/configuration.md) for the
engine directives and the [body-limit contract](../docs/phase4-mode-budget.md)
for separate host and transport limits.

Run the selected host's documented configuration checker after adapting the
bundle. Use [Testing and evidence](../docs/testing-and-evidence.md) to verify
any runtime behavior you rely on.

## Detailed references

See the matching host guide for its generated configuration reference.
[Common examples and references](common/README.md) cover the Common Runtime,
engine directives and example rules. Update generated references through
their source and generator.
