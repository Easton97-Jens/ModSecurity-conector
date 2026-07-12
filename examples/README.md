# Connector examples

**Language:** English | [Deutsch](README.de.md)

This directory contains small, repository-relative configuration references for
the six selected connector paths. They are configuration teaching material, not
deployment manifests and not evidence by themselves.

## Layout and scope

| Directory | Integration mode | Core reference | Compatibility reference |
| --- | --- | --- | --- |
| [apache/](apache/README.md) | native httpd module | Native HTTP/1.1 P1--P4 Safe configuration | none |
| [nginx/](nginx/README.md) | native NGINX HTTP module | Native HTTP/1.1 P1--P4 Safe configuration | none |
| [haproxy/](haproxy/README.md) | native HTX filter | Native HTTP/1.1 P1--P4 Safe configuration | [SPOE/SPOP](haproxy/compatibility-spoe/README.md) |
| [envoy/](envoy/README.md) | Envoy ext_proc | Streamed HTTP/1.1 P1--P4 Safe configuration | [ext_authz](envoy/compatibility-ext-authz/README.md) |
| [traefik/](traefik/README.md) | native Traefik middleware | Local-plugin/UDS HTTP/1.1 P1--P4 Safe configuration | [forwardAuth](traefik/compatibility-forwardauth/README.md) |
| [lighttpd/](lighttpd/README.md) | patched native lighttpd module | HTTP/1.1 identity-entity P1--P4 Safe reference | [sidecar proxy](lighttpd/compatibility-sidecar/README.md) |

All paths in the table are repository-relative: resolve them from the root of
this repository. A host path such as /etc/modsecurity/no-crs-baseline.conf is
an installation example, not a repository path and not a value that can be
copied unchanged to every host.

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

Each connector has a rules directory and an expected directory. The rules
directory identifies the repository-owned No-CRS baseline rule source without
copying a mutable framework file into these examples. The expected directory
describes configuration intent only; it is not a test result.

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
