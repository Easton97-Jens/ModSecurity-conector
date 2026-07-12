# lighttpd native-module examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native lighttpd module named mod_msconnector. The
[minimal reference](minimal/lighttpd.conf) is for the stock host/module shape
and keeps both body modes none. The [Safe reference](safe/lighttpd-http1-identity.conf)
and matching [runtime file](safe/msconnector-runtime.conf) require the matching
patched lighttpd 1.4.84 host and module. They limit scope to proxied HTTP/1.1
identity entity data.

The Safe reference configures the P1--P4 shape with phase4_mode safe. P1 is
request headers, P2 request body, P3 response headers, and P4 response body.
It is not a claim of client-observed P4 behavior, full response buffering,
HTTP/2, HTTP/3, compression, file/zero-copy handling, or Strict abort. No
Strict file is supplied.

The retained [sidecar proxy](compatibility-sidecar/README.md) is not native
module configuration and has no native lifecycle claim.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/lighttpd.conf](minimal/lighttpd.conf) | Host configuration | Stock native module with bodies disabled. |
| [minimal/msconnector-runtime.conf](minimal/msconnector-runtime.conf) | Runtime configuration | Rules and bounded header metadata for minimal mode. |
| [safe/lighttpd-http1-identity.conf](safe/lighttpd-http1-identity.conf) | Host configuration | Patched native HTTP/1.1 identity-entity reference. |
| [safe/msconnector-runtime.conf](safe/msconnector-runtime.conf) | Runtime configuration | Streaming body modes and Safe P4 policy. |
| [rules/README.md](rules/README.md) | Documentation | No-CRS source and phase IDs. |
| [expected/p1-p4-safe.md](expected/p1-p4-safe.md) | Documentation | Configuration intent, not run evidence. |
| [compatibility-sidecar/](compatibility-sidecar/README.md) | Compatibility | Illustrative non-native proxy setup. |

All listed paths are repository-relative from examples/lighttpd. Paths inside
the configurations are host-installation or host-runtime examples.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| server.modules | Ordered installed lighttpd module names | Required; host configuration; server scope | mod_msconnector for minimal and mod_proxy plus mod_msconnector for Safe. Use the matching module ABI. |
| server.document-root, errorlog, pid-file, upload-dirs | Absolute host paths | Required in these references; host configuration; server scope | /srv/lighttpd/htdocs, /srv/lighttpd/log/error.log, /srv/lighttpd/run/lighttpd.pid, /srv/lighttpd/runtime/uploads. Create them with suitable service permissions. |
| server.bind and server.port | Listener host and decimal port | Required; host configuration; server scope | 127.0.0.1 and 8080. A public bind changes exposure. |
| msconnector.config-file | Absolute runtime key=value file path | Required; host configuration; module scope | /etc/lighttpd/msconnector-runtime.conf. The file must be readable by the host process. |
| rules_file | Installed reviewed rules file | Required; runtime configuration; engine scope | /etc/modsecurity/no-crs-baseline.conf. Rules can block traffic. |
| transaction_id_header | HTTP correlation-header name | Required; runtime configuration; transaction scope | x-modsec-transaction-id. Metadata only; do not use it for secrets. |
| request_body_mode and response_body_mode | none, buffered, or streaming according to host capability | Required; runtime configuration; engine scope | none for stock minimal; streaming for matching patched Safe. Do not enable streaming on a stock host. |
| request_body_limit, response_body_limit, body_limit_action | Positive byte limits and reject or process_partial policy | Required where bodies are enabled; runtime configuration; engine scope | 1048576 and reject. Bounds do not imply full connector buffering. |
| phase4_mode | P4 policy: minimal, safe, or strict | Required in these runtime files; runtime configuration; engine scope | safe for patched Safe. It does not prove a status rewrite or abort. |
| server.stream-response-body and proxy.server | Patched delivery setting and local upstream route | Required only for Safe host file; host configuration; server scope | 1 and 127.0.0.1:8081. Identity HTTP/1.1 only; do not infer gzip/br or HTTP/2 behavior. |
| event_path | Writable JSONL metadata destination | Required in these references; runtime configuration; engine scope | /var/log/lighttpd/msconnector-events.jsonl. Protect and rotate it; do not write bodies or secrets. |

## Validation

Install the matching lighttpd module and configuration files, adapt all paths,
then check the installed host configuration. The path below is an installation
example:

~~~sh
lighttpd -tt -f /etc/lighttpd/lighttpd.conf
~~~

For the Safe reference, also verify the exact patched host/module pair and a
private local upstream before starting it. A configuration check proves syntax
and readable inputs only; it does not prove P1--P4 outcomes, Safe host actions,
Strict behavior, production readiness, or CRS coverage.

## Related material

- [lighttpd connector source and patched-host boundary](../../connectors/lighttpd/README.md)
- [Repository examples overview](../README.md)
