# Traefik native-middleware examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: repository-owned native Traefik local plugin plus a persistent
local Unix-domain-socket engine service. The
[minimal static reference](minimal/traefik-static.yaml) registers the local
plugin and a File Provider. Its adjacent minimal dynamic and engine-service
files select the same UDS shape with `phase4_mode=minimal`; the
[Safe dynamic reference](safe/traefik-dynamic.yaml) selects engineMode uds.
The matching [engine-service configuration](safe/traefik-engine-service.conf)
selects streaming bodies and phase4_mode safe.

This is the native HTTP/1.1 P1--P4 Safe reference. P1, P2, P3, and P4 mean
request headers, request body, response headers, and response body. Safe does
not claim a late status rewrite or Strict connection abort. The configuration
does not promise a full response buffer or per-chunk rule evaluation. The
Strict directory documents the optional boundary rather than claiming a
runnable host abort.

[forwardAuth compatibility files](compatibility-forwardauth/README.md) are
request authorization only and must not be treated as a P3/P4 core path.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/traefik-static.yaml](minimal/traefik-static.yaml) | Static host configuration | Local-plugin registration, web entry point, and File Provider. |
| [minimal/traefik-dynamic.yaml](minimal/traefik-dynamic.yaml) | Dynamic host configuration | Minimal UDS middleware/router/service shape. |
| [minimal/traefik-engine-service.conf](minimal/traefik-engine-service.conf) | Engine configuration | Streaming body modes with minimal late-P4 policy. |
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

## Configuration reference

The generated [configuration reference](configuration-reference.md) documents
static/dynamic YAML fields, native plugin defaults, the Common Runtime file,
and the separately labelled forwardAuth compatibility path.

| Setting | Layer | Task |
| --- | --- | --- |
| `engineMode: uds` | Host / Connector | Selects the persistent native UDS engine service. |
| `SecRuleEngine` | ModSecurity Engine | Selects enforcement, DetectionOnly, or Off in the engine rule file. |
| `request_body_mode` | Common Runtime | Selects native engine P2 body handling. |
| `response_body_mode` | Common Runtime | Selects native engine P4 body handling. |
| `phase4_mode` | Common Runtime | Records requested late-P4 policy; post-commit Go middleware remains log-only. |

`engineMode: passthrough` is a source-only allow engine, not rule enforcement.
`SecRuleEngine Off` keeps the UDS route but disables engine rules. forwardAuth
is a separate request-only compatibility route.

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
