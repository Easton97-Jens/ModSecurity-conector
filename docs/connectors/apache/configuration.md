<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Apache configuration

**Language:** English | [Deutsch](configuration.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Configuration model

Apache directives are registered by the adapter. The documented examples use `modsecurity on`, `modsecurity_rules_file`, and existing bounded Phase-4 controls.

## Minimal, Safe, and Strict

The [annotated Apache examples](../../../examples/apache/README.md) are the complete local source. Replace every path, port, and endpoint for the target host. Minimal and Safe belong to the documented core; Strict is described only where the host and current evidence support it. Do not copy a compatibility configuration as the selected core path.

## Defaults, body scope, and logging

Only existing host directives and harness options are listed in the examples. Body and content-type behavior remain host- and profile-bound; no configuration permits a connector-owned full response buffer. Use payload-free connector/evidence logs and keep secrets out of rules, paths, and command lines.

## Validation

Run `make check-config-apache` before starting a host. The core run `make full-lifecycle-apache` needs writable runtime and evidence roots; always inspect its artifacts for the result.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `APXS / APXS_BIN` | Optional | path to an executable APXS | Set by the operator or provisioning | `/usr/bin/apxs` |
| `APACHE_BIN / APACHECTL_BIN` | Optional | path to httpd/apachectl | Set by provisioning or operator | `/usr/sbin/apachectl` |
| `BUILD_HTTPD_FROM_SOURCE` | Optional | `0` or `1` | Make caller | `1` |
| `NO_CRS_RULES_FILE` | Required for canonical rule runs | absolute rules-file path | Make default or caller | `/etc/modsecurity/no-crs-baseline.conf` |

See the [central variables reference](../../configuration/variables.md).
