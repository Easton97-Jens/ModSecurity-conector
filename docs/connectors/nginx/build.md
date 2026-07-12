<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# NGINX build

**Language:** English | [Deutsch](build.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Build path and host version

`make build-nginx` prepares the selected host path; `make check-config-nginx` validates generated configuration.

The authoritative host version is the version of the current prepared runtime or its pinned provisioning input. A documented version is not support for every distribution, ABI, or operating environment.

## Toolchain and dependencies

Use the host-appropriate C/C++ or Go toolchain, libmodsecurity dependencies, and a writable build/cache root outside the checkout. Compiler, flags, and host revision are recorded as build provenance; this guide makes no universal compiler or Go-version claim.

## Cache-v2 and provenance

Cache-v2 reuse is identity-bound. Source URL, revision or digest, patchset, architecture, compiler, and configuration decide whether an entry is reusable. A cache hit is not a runtime PASS.

## Build, configuration, and runtime

Run `make build-nginx` and then `make check-config-nginx`. Start and runtime smokes exist only for the target families that provide them; the selected core run is `make full-lifecycle-nginx`. A successful build or config check is not a rule-engine PASS.

## Optional profiles and troubleshooting

Compatibility, CRS, extended-matrix, H2/H3, and Strict profiles remain separate from the selected core. Before changing configuration, check executable paths, ABI, module/service load, writable runtime roots, and pinned source/patch inputs.

## Configuration variables and placeholders

The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference.

| Name | Required | Format | Set by | Example value |
| --- | --- | --- | --- | --- |
| `NGINX_PREFIX` | Optional | absolute generated prefix | Provisioning or caller | `/srv/modsecurity-work/nginx-runtime/nginx` |
| `NGINX_BINARY` | Optional | executable NGINX path | Derived from `NGINX_PREFIX` | `<nginx-prefix>/sbin/nginx` |
| `NGINX_MODULE` | Optional | dynamic module path | Derived from `NGINX_PREFIX` | `<nginx-prefix>/modules/ngx_http_modsecurity_module.so` |
| `NGINX_PHASE4_MODE` | Optional | `minimal`, `safe`, or `strict` where host supports it | Caller/harness | `safe` |

See the [central variables reference](../../configuration/variables.md).
