# NGINX Connector Origin Map

Status: implemented

Source repository: `/root/conecter/ModSecurity-nginx`  
Source branch: `master`  
Source commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`  
Source describe: `v1.0.4-14-g9eb44fd`  
License: Apache-2.0, imported as `connectors/nginx/upstream/LICENSE`

Central attribution: `licenses/nginx/`

| Imported path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `connectors/nginx/upstream/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | License text for imported NGINX connector files |
| `connectors/nginx/upstream/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream attribution |
| `connectors/nginx/upstream/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream change context |
| `connectors/nginx/upstream/README.md` | `README.md` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream build and usage context |
| `connectors/nginx/upstream/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX module build metadata |
| `connectors/nginx/upstream/src/ddebug.h` | `src/ddebug.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Connector debug helper |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX access phase integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX response/body filter integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Shared NGINX connector declarations |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX header filter integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX log phase integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX module entrypoint and config |

## Excluded Upstream Files

The NGINX test harness, `.git`, `.github`, CI files, release scripts, Windows
build files, and build/runtime artifacts are not imported.

## Central Attribution Copies

The NGINX upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are also mirrored
under `licenses/nginx/` for repository-level license review. The copies in this
`upstream/` tree remain authoritative for the imported source layout and are not
removed.

## Pruning Review

Last reviewed in `docs/upstream-pruning-analysis.md`.

No imported NGINX files were removed in the pruning pass. The imported tree is
already limited to license/provenance files, the NGINX module `config`, and the
source/dependency files explicitly listed by that `config`. Files with unclear
build relevance are retained until an isolated `$BUILD_ROOT` probe proves they
can be removed without breaking `make smoke-apache`, `make smoke-nginx`, and
`make smoke-all`.
