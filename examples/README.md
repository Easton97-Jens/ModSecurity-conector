# Connector examples

**Language:** English | [Deutsch](README.de.md)

The examples are the practical configuration companion to the main
documentation. They cover all six host families and all ten logical connector
solutions. Start here when you know which host you want to use but need to see
how the repository's configuration layers fit together.

Examples are **teaching/reference material**. They are not production
deployment manifests and they do not prove runtime behavior by themselves.

## Choose a host

| Host family | Example guide | Logical solutions |
| --- | --- | --- |
| Apache | [Apache](apache/README.md) | `apache` |
| NGINX | [NGINX](nginx/README.md) | `nginx` |
| HAProxy | [HAProxy](haproxy/README.md) | `haproxy-htx`, `haproxy-spoe-spop` |
| Envoy | [Envoy](envoy/README.md) | `envoy-ext-proc`, `envoy-ext-authz` |
| Traefik | [Traefik](traefik/README.md) | `traefik-native-uds`, `traefik-forwardauth` |
| lighttpd | [lighttpd](lighttpd/README.md) | `lighttpd-patched`, `lighttpd-stock` |

## Choose a configuration profile

| Profile | Use it for | Important boundary |
| --- | --- | --- |
| `off` | Baseline with the extra connector-owned cumulative Phase-4 budget disabled | Configured libmodsecurity response-body inspection and independent engine/host/transport limits still apply. |
| `safe` | Recommended learning/start profile for the full checked-in P1–P4 shape | Late P4 outcomes that cannot safely change a committed response remain non-disruptive where documented. |
| `strict` | Testing the strict late-action policy on profiles that support the required host action | A checked-in strict file is not proof that a client-visible post-commit abort has been observed. |
| `all` | Comprehensive source-backed configuration reference | `all` is a layout, not a fourth Phase-4 mode; it uses valid settings such as `strict`. |

`DetectionOnly`, engine `Off`, and a disabled connector are separate
concepts and are documented in the host-specific example guides.

## Ten logical solutions

| Logical solution | Off | Safe | Strict | All |
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

## What you normally need to change

| Value | Why | Typical example |
| --- | --- | --- |
| installed host/module path | Distribution and build layouts differ | `/etc/nginx/nginx.conf` or an installed module path |
| rules-file path | The host must read the intended reviewed rules | `/etc/modsecurity/no-crs-baseline.conf` |
| listener/upstream ports | Local applications and test environments differ | `127.0.0.1:8080` / `127.0.0.1:8081` |
| runtime/socket paths | Services need writable, private runtime locations | private UDS or runtime directory outside the checkout |
| log/event paths | The service account must be able to write safely | protected and rotated JSONL/error-log destination |

Never copy example credentials, private keys, cookies, authorization values, or
sensitive request/response bodies into version control or review evidence.

## Typical workflow

1. Choose the host family and logical solution.
2. Start with the matching `safe` example unless you specifically need
   another policy.
3. Read the host example guide and replace installation/runtime placeholders.
4. Validate the host configuration with its native checker.
5. Build/start through repository root targets where available.
6. If you need a runtime claim, run the matching lifecycle/evidence target and
   evaluate the run-scoped artifacts.

A syntax/configuration check confirms parsing/loading only. It does not prove
P1–P4 outcomes, production readiness, CRS coverage, or strict late behavior.

## Rules and phase IDs

The repository No-CRS baseline uses these test-profile rule IDs:

| Rule ID | Phase | Meaning |
| ---: | ---: | --- |
| 1100001 | P1 | request-header deny |
| 1100101 | P2 | request-body deny |
| 1100201 | P3 | response-header deny |
| 1100301 | P4 | response-body decision used by the selected policy boundary |

These are repository test-profile IDs, not OWASP Core Rule Set IDs.

## Detailed configuration references

The host guides link source-backed configuration references for Common Runtime,
ModSecurity engine directives, and each host's parser surface. Generated
configuration references are maintained through their generators; do not edit
them manually in isolation.

For concepts before syntax, read [Configuration](../docs/configuration.md).
For runtime-result semantics, read
[Testing and evidence](../docs/testing-and-evidence.md).
