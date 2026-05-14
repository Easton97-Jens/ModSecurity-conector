# Apache vs NGINX PoC

Status: scaffolded

## Shared Behavior

Both connector PoCs use the same portable case:

```text
tests/common/cases/minimal/phase2_args_block.yaml
```

Shared pieces:

- `tests/runners/case_cli.py materialize` writes connector runtime rule files
  and request variables from the YAML case.
- `tests/runners/case_cli.py assert-status` compares the observed HTTP status
  with `expect.status`.
- The expected proof is HTTP `403` for `GET /?test=attack`.

The shared case is a rule/request/expectation model. It is not proof of a
connector until that connector's runtime harness observes HTTP `403`.

## Connector-Specific Pieces

Apache:

- Build integration uses APXS/Autotools from the local `ModSecurity-apache`
  source copy.
- Runtime loads `mod_security3.so` with `LoadModule security3_module`.
- Configuration enables `modsecurity on` and points `modsecurity_rules_file` at
  the materialized rules file.
- A local source-built Apache httpd smoke has observed HTTP `403`.

NGINX:

- Build integration uses the ModSecurity-nginx third-party dynamic module path
  with `--with-compat --add-dynamic-module=...`.
- Runtime loads `ngx_http_modsecurity_module.so` with `load_module`.
- Configuration enables `modsecurity on` and points `modsecurity_rules_file` at
  the materialized rules file.
- A local source-built NGINX smoke has observed HTTP `403`.

## Lifecycle Differences

Apache and NGINX expose different hook models. The shared runner intentionally
does not model hooks; it only provides the portable test data.

Observed NGINX local source facts:

- Access handling is registered in `NGX_HTTP_ACCESS_PHASE`.
- Logging is registered in `NGX_HTTP_LOG_PHASE`.
- Header and body filters are installed separately.
- Response body processing depends on NGINX filter ordering.

Apache hook details remain connector-specific and are documented in
`docs/import-analysis-apache.md` and `docs/apache-poc.md`.

## Build Differences

Apache source-build mode downloads and builds httpd, APR, and APR-util under
`BUILD_ROOT`. NGINX source-build mode downloads the official GitHub release
archive from `nginx/nginx`, builds NGINX under `BUILD_ROOT`, and writes the
dynamic module under:

```text
$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
```

Neither PoC writes to `/usr`, `/usr/local`, `/etc/apache2`, `/etc/nginx`, or
`/root/conecter/*`.

## Current Local Comparison

Observed on 2026-05-14 with `BUILD_ROOT=/src/ModSecurity-conector-build`:

| Connector | Source-built server | Shared case | Observed status |
| --- | --- | --- | --- |
| Apache | httpd 2.4.67 | `phase2_args_block.yaml` | HTTP 403 |
| NGINX | nginx 1.31.0 from `release-1.31.0` | `phase2_args_block.yaml` | HTTP 403 |

This proves the minimal shared case for this workspace only. Broader
compatibility still requires connector-specific regression coverage.
