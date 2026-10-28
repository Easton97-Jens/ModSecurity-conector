# Connector examples

**Language:** English | [Deutsch](README.de.md)

These examples show how to configure the repository's six host families and
ten logical connector solutions. Choose the host and topology first, then
adapt its configuration. Examples are teaching/reference material, not
production deployment manifests or runtime evidence.

Updating an older configuration? Read [Migration](../docs/migration.md).
Connector-owned cumulative request/response limits have been removed. A value
found in an older example is not automatically accepted by current source.

## Choose a host

| Host family | Example guide | Logical profiles |
| --- | --- | --- |
| Apache | [Apache](apache/README.md) | `apache` |
| NGINX | [NGINX](nginx/README.md) | `nginx` |
| HAProxy | [HAProxy](haproxy/README.md) | `haproxy-htx`, `haproxy-spoe-spop` |
| Envoy | [Envoy](envoy/README.md) | `envoy-ext-proc`, `envoy-ext-authz` |
| Traefik | [Traefik](traefik/README.md) | `traefik-native-uds`, `traefik-forwardauth` |
| lighttpd | [lighttpd](lighttpd/README.md) | `lighttpd-patched`, `lighttpd-stock` |

A native streaming route, an authorization route with a response companion,
and a traffic-owning sidecar are different topologies. Their request-body
visibility, host prerequisites, and late-action capabilities differ. The
[ten-profile body-inspection matrix](../docs/body-inspection-review-matrix.md)
explains those limitations. A response observer does not make its host's
buffered request authorization incremental.

## Choose a configuration layout

| Layout | Use | Boundary |
| --- | --- | --- |
| `off` | Native intervention/error handling without the additional Safe/Strict late-action policy | Does not disable configured engine inspection |
| `safe` | A useful starting reference for the selected P1–P4 configuration | Conservative late handling does not ignore native Reject results or genuine errors |
| `strict` | The selected profile's supported strict late action | May be rejected at startup if the required host action is unavailable |
| `all` | Comprehensive source-backed configuration reference | Not a fourth Phase-4 mode or a guarantee of runtime admission |

The `all` layout uses a real Phase-4 value such as `strict` and never introduces an unsupported `all` phase mode.
A checked-in strict file does not prove a client-visible post-commit abort.
Values that cannot coexist or require operator-specific credentials remain
inactive with their selection boundary. Do not enable every commented option.

`SecRuleEngine DetectionOnly`, `SecRuleEngine Off`, a disabled connector, and
Phase-4 `off` affect different layers. See the host guide and
[rule examples](common/rule-examples.md) before choosing one.

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

Links are relative to this `examples/` directory. Paths written inside a host
configuration, such as `/etc/modsecurity/no-crs-baseline.conf`, are installation
examples and usually need changing for the target machine.

## Compatibility and companion boundaries

The complete bundles above and the retained standalone compatibility material
are not the same thing. Read the relevant host section:

- [HAProxy SPOE/SPOP compatibility material](haproxy/README.md#spoespop-compatibility-material)
- [Envoy ext_authz compatibility](envoy/README.md#ext_authz-compatibility)
- [Traefik forwardAuth compatibility](traefik/README.md#forwardauth-compatibility)
- [lighttpd sidecar compatibility](lighttpd/README.md#sidecar-compatibility)

A request-only service does not establish P3/P4 inspection without its required
companion. The old host-only sidecar illustration is not the traffic-owning
Stock lighttpd solution. Evidence for one route does not qualify another.

## Body inspection and safety

P1/P2 mean request headers/body; P3/P4 mean response headers/body.
libModSecurity owns inspection limits and actions for both request and response
bodies. Configure the intended native engine directives in the rules file,
including `SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit`,
`SecRequestBodyLimitAction`, `SecResponseBodyLimit`, and
`SecResponseBodyLimitAction`, where required by your policy. Access and MIME
scope remain engine settings too.

Do not add removed Common/native body-size options as an extra safety layer.
They fail configuration; the connector must not inject defaults or silently
inspect a connector-chosen prefix. See the full
[removed-options list](../docs/migration.md) and
[body-limit ownership contract](../docs/phase4-mode-budget.md).

Individual frames/messages, working buffers, header/event metadata, timeouts,
file validation, and the documented host authorization ceilings remain
independent controls. Do not confuse their removal with the removal of
connector inspection-size policy. Safe intent, first-byte-before-EOS, and
no-full-buffer properties require matching host evidence; static files alone
do not establish them.

## Values to adapt

| Value | Why it varies | Example and precaution |
| --- | --- | --- |
| Host/module path | Installation and module ABI differ | Use the selected host's matching module; do not overwrite an installed configuration blindly |
| Rules-file path | The service must read the reviewed engine rules | `/etc/modsecurity/no-crs-baseline.conf` is an installation example, not a universal default |
| Listener/upstream | Local applications and routes differ | `127.0.0.1:8080` / `127.0.0.1:8081`; public exposure is a separate decision |
| Runtime/socket path | Services need private writable locations | Use a protected runtime directory outside the checkout |
| Log/event destination | Permissions and retention are deployment-specific | Protect and rotate metadata logs; never add secrets or traffic bodies for review |

Supply credentials, private keys, cookies, and authorization values through the
host's secure configuration mechanism. Do not commit them or include them in
run IDs or review evidence.

## Typical workflow

1. Choose the host family and logical profile, then read its prerequisites.
2. Start with the matching `safe` reference for learning, or explicitly choose
   another policy. Check strict admission before using a `strict` or `all` file.
3. Adapt paths, addresses, rules, permissions, and private endpoints.
4. Run the documented native host checker or root configuration target.
5. Use root build/start targets only with their prerequisites. Select normal
   tests through the active inventory, not by assuming every old test is a default.
6. For a runtime claim, use separately authorized profile/run evidence and
   validate its artifacts. Broad campaigns are not an automatic example step.

A successful syntax/configuration check establishes parsing/loading only. It
does not prove production readiness, CRS completeness, full protocol coverage,
all P1–P4 outcomes, or strict late behavior.

## Rules and phase IDs

The No-CRS baseline uses the following repository test-profile IDs. They are
not OWASP Core Rule Set IDs; host-local illustration rules can have other IDs.

| Rule ID | Phase | Meaning |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision within the selected host/policy boundary |

Each host guide names the rules source and its example's scope. Do not copy a
mutable Framework rules file into an example and treat it as a fixed baseline.

## Detailed references

| Reference | Scope |
| --- | --- |
| [Common Runtime](common/common-connector-configuration.md) | Current source-backed `key=value` parser surface |
| [ModSecurity directives](common/modsecurity-directives.md) | Engine directives used by the checked-in examples |
| [Rule examples](common/rule-examples.md) | Enforcement, DetectionOnly, and engine Off |
| [Apache](apache/configuration-reference.md) | Registered host directives and example fields |
| [NGINX](nginx/configuration-reference.md) | Registered host directives, contexts, and example fields |
| [HAProxy](haproxy/configuration-reference.md) | Native HTX and separately labelled SPOE/SPOP configuration |
| [Envoy](envoy/configuration-reference.md) | Processor, service, and host configuration |
| [Traefik](traefik/configuration-reference.md) | Native UDS and separately labelled forwardAuth configuration |
| [lighttpd](lighttpd/configuration-reference.md) | Patched native and Stock sidecar configuration |

These detailed references are generated. Update them through their generator
rather than editing output in isolation. For concepts read
[Configuration](../docs/configuration.md); for commands read
[Getting started](../docs/getting-started.md); for results read
[Testing and evidence](../docs/testing-and-evidence.md).
