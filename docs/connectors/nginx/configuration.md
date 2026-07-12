<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# NGINX configuration

**Language:** English | [Deutsch](configuration.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Configuration model

The adapter uses existing NGINX directives such as `modsecurity on` and `modsecurity_rules_file`. The dynamic module, prefix, and phase-4 mode are selected by existing harness variables.

## Minimal, Safe, and Strict

The [annotated NGINX examples](../../../examples/nginx/README.md) are the complete local source. Replace every path, port, and endpoint for the target host. Minimal and Safe belong to the documented core; Strict is described only where the host and current evidence support it. Do not copy a compatibility configuration as the selected core path.

## Defaults, body scope, and logging

Only existing host directives and harness options are listed in the examples. Body and content-type behavior remain host- and profile-bound; no configuration permits a connector-owned full response buffer. Use payload-free connector/evidence logs and keep secrets out of rules, paths, and command lines.

## Validation

Run `make check-config-nginx` before starting a host. The core run `make full-lifecycle-nginx` needs writable runtime and evidence roots; always inspect its artifacts for the result.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `NGINX_PREFIX` | Optional | absolute generated prefix | Provisioning or caller | `/srv/modsecurity-work/nginx-runtime/nginx` |
| `NGINX_BINARY` | Optional | executable NGINX path | Derived from `NGINX_PREFIX` | `<nginx-prefix>/sbin/nginx` |
| `NGINX_MODULE` | Optional | dynamic module path | Derived from `NGINX_PREFIX` | `<nginx-prefix>/modules/ngx_http_modsecurity_module.so` |
| `NGINX_PHASE4_MODE` | Optional | `minimal`, `safe`, or `strict` where host supports it | Caller/harness | `safe` |

See the [central variables reference](../../configuration/variables.md).
