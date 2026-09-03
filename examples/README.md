# Connector examples

**Language:** English | [Deutsch](README.de.md)

This directory contains small, repository-relative configuration references for
six host roots and the ten logical connector solutions. They are configuration
teaching material, not deployment manifests and not evidence by themselves.

## Layout and scope

| Directory | Integration mode | Logical connector solutions | Legacy-only material |
| --- | --- | --- | --- |
| [apache/](apache/README.md) | native httpd module | Apache | none |
| [nginx/](nginx/README.md) | native NGINX HTTP module | NGINX | none |
| [haproxy/](haproxy/README.md) | native HTX filter and SPOE/SPOP bridge | HAProxy HTX; HAProxy SPOE/SPOP with native HTX response companion | [SPOE/SPOP compatibility material](haproxy/README.md#spoespop-compatibility-material) |
| [envoy/](envoy/README.md) | external processors | Envoy ext_proc; Envoy ext_authz with private response observer | [ext_authz compatibility material](envoy/README.md#ext_authz-compatibility) |
| [traefik/](traefik/README.md) | middleware and UDS engine | Traefik Native UDS; Traefik forwardAuth with private response observer | [forwardAuth compatibility material](traefik/README.md#forwardauth-compatibility) |
| [lighttpd/](lighttpd/README.md) | native module and traffic-owning sidecar | lighttpd Patched; lighttpd Stock sidecar | [sidecar compatibility material](lighttpd/README.md#sidecar-compatibility) |

All paths in the table are repository-relative: resolve them from the root of
this repository. A host path such as /etc/modsecurity/no-crs-baseline.conf is
an installation example, not a repository path and not a value that can be
copied unchanged to every host.

## Four configuration variants

Every logical connector solution has `minimal`, `safe`, `strict`, and `all`
artifacts. `all` is a comprehensive, source-backed configuration layout: it
uses a real `strict` P4 policy and never introduces an unsupported `all` phase
mode. Values that cannot coexist or require credentials remain commented with
their selection boundary. A strict artifact does not claim a client-visible
post-commit abort where its host transport has no proven safe abort hook.

| Logical connector solution | Minimal | Safe | Strict | All |
| --- | --- | --- | --- | --- |
| Apache | [minimal](apache/minimal/httpd.conf) | [safe](apache/safe/httpd.conf) | [strict](apache/strict/httpd.conf) | [all](apache/all/httpd.conf) |
| NGINX | [minimal](nginx/minimal/nginx.conf) | [safe](nginx/safe/nginx.conf) | [strict](nginx/strict/nginx.conf) | [all](nginx/all/nginx.conf) |
| HAProxy HTX | [minimal](haproxy/minimal/haproxy-htx.cfg) | [safe](haproxy/safe/haproxy-htx.cfg) | [strict](haproxy/strict/haproxy-htx.cfg) | [all](haproxy/all/haproxy-htx.cfg) |
| HAProxy SPOE/SPOP | [minimal](haproxy/spoe-spop/minimal/) | [safe](haproxy/spoe-spop/safe/) | [strict](haproxy/spoe-spop/strict/) | [all](haproxy/spoe-spop/all/) |
| Envoy ext_authz | [minimal](envoy/ext-authz/minimal/) | [safe](envoy/ext-authz/safe/) | [strict](envoy/ext-authz/strict/) | [all](envoy/ext-authz/all/) |
| Envoy ext_proc | [minimal](envoy/ext-proc/minimal/) | [safe](envoy/ext-proc/safe/) | [strict](envoy/ext-proc/strict/) | [all](envoy/ext-proc/all/) |
| Traefik forwardAuth | [minimal](traefik/forwardauth/minimal/) | [safe](traefik/forwardauth/safe/) | [strict](traefik/forwardauth/strict/) | [all](traefik/forwardauth/all/) |
| Traefik Native UDS | [minimal](traefik/native-uds/minimal/) | [safe](traefik/native-uds/safe/) | [strict](traefik/native-uds/strict/) | [all](traefik/native-uds/all/) |
| lighttpd Stock | [minimal](lighttpd/stock/minimal/) | [safe](lighttpd/stock/safe/) | [strict](lighttpd/stock/strict/) | [all](lighttpd/stock/all/) |
| lighttpd Patched | [minimal](lighttpd/patched/minimal/) | [safe](lighttpd/patched/safe/) | [strict](lighttpd/patched/strict/) | [all](lighttpd/patched/all/) |

## P1--P4 Safe core

P1 means request headers, P2 request body, P3 response headers, and P4
response body. The Safe examples select the documented post-commit Safe policy:
when a P4 decision is too late to change a response cleanly, it is recorded as
a non-disruptive outcome rather than represented as a fabricated HTTP status.

The current core references are HTTP/1.1-oriented. They do not imply full
connector response buffering. First-byte-before-EOS and no-full-buffer
properties, where exercised, remain properties of the corresponding host
runner and evidence, not promises made by a static configuration file.

Strict is intentionally narrow. A strict directory exists only where there is
an actual checked-in configuration shape. It is never a claim that a
post-commit status rewrite, reset, or connection abort was observed. Read the
connector-specific limitation before enabling it.

## Configuration references

| Reference | Scope |
| --- | --- |
| [Common Runtime](common/common-connector-configuration.md) | Complete source-backed `key=value` parser surface. |
| [ModSecurity Engine](common/modsecurity-directives.md) | Engine directives actually used by checked-in examples. |
| [Rule examples](common/rule-examples.md) | On, DetectionOnly, and Off engine behavior. |
| [Apache](apache/configuration-reference.md) | Apache `command_rec` directives and example host fields. |
| [NGINX](nginx/configuration-reference.md) | NGINX `ngx_command_t` directives and example host fields. |
| [HAProxy](haproxy/configuration-reference.md) | Native HTX options separated from SPOE/SPOP compatibility. |
| [Envoy](envoy/configuration-reference.md) | ext_proc YAML/service/CLI contract separated from ext_authz. |
| [Traefik](traefik/configuration-reference.md) | Native middleware/UDS configuration separated from forwardAuth. |
| [lighttpd](lighttpd/configuration-reference.md) | Native plugin keys and Common Runtime separated from sidecar proxy. |

## Rules and expected outcomes

Each connector parent README embeds its No-CRS rule source and P1--P4 Safe
intent. The rules directories retain the checked-in profile files without
copying a mutable framework file into these examples. Safe intent remains
configuration guidance, not a test result.

The No-CRS rule IDs 1100001, 1100101, 1100201, and 1100301 correspond to P1,
P2, P3, and P4 respectively. They are repository test-profile IDs, not
OWASP Core Rule Set IDs.

## Values that must be adapted

| Value form | Meaning | Example | Safety note |
| --- | --- | --- | --- |
| host configuration path | File owned by the installed host | /etc/nginx/nginx.conf | Distribution-specific; do not overwrite an existing host file blindly. |
| rules-file path | Readable ModSecurity rules file | /etc/modsecurity/no-crs-baseline.conf | Use a reviewed ruleset. Rules can block traffic. |
| listener or upstream address | Host and TCP port for a local test route | 127.0.0.1:8080 | Bind loopback for a local exercise unless network exposure is intentional. |
| log or event path | Writable host/runtime destination | /var/log/modsecurity/connector.jsonl | Logs can contain request metadata; protect and rotate them. |
| private UDS path | Absolute Unix-domain-socket pathname | /run/traefik-msconnector/engine.sock | Put it in a directory inaccessible to untrusted users. |

No example contains credentials, API keys, cookies, authorization headers, TLS
private keys, or other secrets. Supply such values through the host's secure
configuration mechanism; do not commit them or place them in evidence.

## Validation

Before loading any reference, replace the documented host paths, rules-file
path, addresses, and log locations for the target machine. Then use that
host's native configuration checker and inspect its error log. The connector
README names the exact reference and the boundary to validate. A successful
syntax check proves only that the host accepted configuration; it does not
prove P1--P4 behavior, production readiness, CRS coverage, or strict
late-intervention behavior.
