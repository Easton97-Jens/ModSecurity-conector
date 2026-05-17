# NGINX Connector Origin Map

Status: implemented

Local reference: `/root/conecter/ModSecurity-nginx`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source branch: `master`
Source commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source describe: `v1.0.4-14-g9eb44fd`
License: Apache-2.0, imported as `connectors/nginx/upstream/LICENSE`

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Central attribution: `licenses/nginx/`

| Imported path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `connectors/nginx/upstream/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | License text for imported NGINX connector files |
| `connectors/nginx/upstream/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream attribution |
| `connectors/nginx/upstream/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream change context |
| `connectors/nginx/upstream/README.md` | `README.md` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream build and usage context |
| `connectors/nginx/upstream/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX module build metadata |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX access phase integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX response/body filter integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Shared NGINX connector declarations |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX header filter integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX log phase integration |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | NGINX module entrypoint and config |

## Repo-Owned Replacement Files

| Path | Replaces | Origin | Reason |
| --- | --- | --- | --- |
| `connectors/nginx/src/ddebug.h` | `connectors/nginx/upstream/src/ddebug.h` | Repo-owned compatibility header | Keeps the NGINX module build dependency satisfied without retaining the imported debug helper in `upstream/`; copied only into `$BUILD_ROOT` build copies when the selected connector source lacks `src/ddebug.h` |

## Excluded Upstream Files

The NGINX test harness, `.git`, `.github`, CI files, release scripts, Windows
build files, imported debug helper `src/ddebug.h`, and build/runtime artifacts
are not imported.

## Central Attribution Copies

The NGINX upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are also mirrored
under `licenses/nginx/` for repository-level license review. The copies in this
`upstream/` tree remain authoritative for the imported source layout and are not
removed.

## Pruning Review

Last reviewed in `docs/imports/upstream-pruning-analysis.md`.

The phase-4 replace-and-reduce pass removed only the imported NGINX debug helper
`src/ddebug.h`. The NGINX module `config` still lists `src/ddebug.h` as a build
dependency, so `ci/prepare-nginx-build.sh` overlays the repo-owned
`connectors/nginx/src/ddebug.h` into the generated `$BUILD_ROOT` build copy when
needed. No request, response, filter, hook, transaction, or `RESPONSE_BODY`
logic was replaced.

`connectors/nginx/upstream/` is a temporary reference/import basis. Future
removal is allowed only after functional replacement, retained origin/license
documentation, and passing real-world smoke evidence.
