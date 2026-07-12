# Traefik native-middleware examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: repository-owned native Traefik local plugin plus a persistent
local Unix-domain-socket engine service. The
[minimal static reference](minimal/traefik-static.yaml) registers the local
plugin and a File Provider; the
[Safe dynamic reference](safe/traefik-dynamic.yaml) selects engineMode uds.
The matching [engine-service configuration](safe/traefik-engine-service.conf)
selects streaming bodies and phase4_mode safe.

This is the native HTTP/1.1 P1--P4 Safe reference. P1, P2, P3, and P4 mean
request headers, request body, response headers, and response body. Safe does
not claim a late status rewrite or Strict connection abort. The configuration
does not promise a full response buffer or per-chunk rule evaluation. No Strict
file is supplied.

[forwardAuth compatibility files](compatibility-forwardauth/README.md) are
request authorization only and must not be treated as a P3/P4 core path.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/traefik-static.yaml](minimal/traefik-static.yaml) | Static host configuration | Local-plugin registration, web entry point, and File Provider. |
| [safe/traefik-dynamic.yaml](safe/traefik-dynamic.yaml) | Dynamic host configuration | Router, middleware, UDS engine selection, and local upstream. |
| [safe/traefik-engine-service.conf](safe/traefik-engine-service.conf) | Engine configuration | Rules, limits, streaming body modes, and Safe policy. |
| [rules/README.md](rules/README.md) | Documentation | No-CRS source and phase IDs. |
| [expected/p1-p4-safe.md](expected/p1-p4-safe.md) | Documentation | Configuration intent, not evidence. |
| [compatibility-forwardauth/](compatibility-forwardauth/README.md) | Compatibility | Former request-only route. |

All paths above are repository-relative from examples/traefik. Paths inside the
files are either host-installation paths or local test values and must be
adapted.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| moduleName | Go module identifier for the local plugin | Required; explicit static value; Traefik local-plugin scope | github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware. Stage matching source in the installed Traefik local-plugin workspace. |
| entryPoints.web.address | Listener address string | Required; explicit static value; Traefik static scope | :8080. A public bind changes exposure. |
| providers.file.filename | Dynamic configuration file path relative to Traefik working directory | Required; explicit static value; File Provider scope | ./traefik-dynamic.yaml. Copy the Safe dynamic file to this resolved location. |
| router rule and service URL | Request matcher and upstream URL | Required; dynamic configuration; router/service scope | PathPrefix for all paths and http://127.0.0.1:8081. Restrict routes and replace endpoint for deployment. |
| maxHeaderCount, maxHeaderBytes, maxRequestChunkBytes, maxResponseChunkBytes | Positive plugin limits | Required; dynamic configuration; middleware scope | 128, 65536, 32768, 32768. Lower values reject more input; do not remove bounds. |
| transactionIDHeader | HTTP correlation header name | Required; dynamic configuration; middleware scope | X-Request-Id. It is metadata, not a secret. |
| engineMode | Native engine mode: passthrough or uds | Required for Safe reference; dynamic configuration; middleware scope | uds. It requires a valid private engineSocketPath. |
| engineSocketPath | Absolute private Unix socket path | Required when engineMode is uds; dynamic configuration; middleware scope | /run/traefik-msconnector/engine.sock. The parent directory must be access-controlled and owned by the trusted service. |
| rules_file | Installed reviewed rules-file path | Required; engine configuration; engine scope | /etc/modsecurity/no-crs-baseline.conf. Rules can block traffic. |
| request_body_mode and response_body_mode | Engine body modes | Required for Safe reference; engine configuration; engine scope | streaming. This does not itself prove a complete buffer or a late client action. |
| phase4_mode | Late P4 policy name | Required for Safe reference; engine configuration; engine scope | safe. It does not authorize a fabricated status or Strict abort. |

## Validation

Copy the static and dynamic files to the host locations selected by the File
Provider, adapt all paths and endpoints, and validate the installed static
configuration. /etc/traefik/traefik.yaml is an installation example:

~~~sh
traefik check --configFile=/etc/traefik/traefik.yaml
~~~

Also verify that the engine socket is private, the engine service can read the
rules file, and Traefik can load the local plugin. A configuration check does
not prove P1--P4 behavior, Safe host actions, Strict behavior, production
readiness, or CRS coverage.

## Related material

- [Traefik connector source and native service boundary](../../connectors/traefik/README.md)
- [Repository examples overview](../README.md)
