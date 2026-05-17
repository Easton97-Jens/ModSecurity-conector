# NGINX Connector Origin Map

Status: adapter-owned source migration implemented

Local reference: `/root/conecter/ModSecurity-nginx`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source branch: `master`
Source commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source describe: `v1.0.4-14-g9eb44fd`
License: Apache-2.0, retained as `connectors/nginx/upstream/LICENSE`
Default imported path: `connectors/nginx/src`

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `/root/conecter/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Central attribution: `licenses/nginx/`

## Adapter-Owned Source

NGINX now builds from a materialized source tree generated under
`$BUILD_ROOT/nginx-build/connector-src`. The productive module source is
adapter-owned in `connectors/nginx/src/`; `connectors/nginx/upstream/` is kept
only for upstream attribution and reference files.

| Adapter-owned path | Original upstream path | Repo | Base commit | Extra provenance | License | Import reason |
| --- | --- | --- | --- | --- | --- | --- |
| `connectors/nginx/src/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX dynamic module build metadata |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX access phase integration |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | NGINX response/body filter integration plus phase-4 late-intervention changes |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | Shared NGINX connector declarations plus phase-4 mode/config fields |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX header filter integration |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX log phase integration |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | NGINX module entrypoint/config plus phase-4 directives |
| `connectors/nginx/src/ddebug.h` | `src/ddebug.h` | repo-owned compatibility header | n/a | replaces imported upstream debug helper | Apache-2.0-compatible project code | Keeps the NGINX module build dependency satisfied without retaining the imported debug helper in `upstream/` |
| `connectors/nginx/src/metadata.c` | n/a | repo-owned adapter metadata | n/a | none | Apache-2.0-compatible project code | Report/build-summary origin metadata |
| `connectors/nginx/src/metadata.h` | n/a | repo-owned adapter metadata | n/a | none | Apache-2.0-compatible project code | Report/build-summary origin metadata |
| `connectors/nginx/src/SOURCE_MAP.json` | n/a | repo-owned provenance manifest | n/a | records base and PR #377 provenance | Apache-2.0-compatible project metadata | Source migration and PR provenance map |
| `connectors/nginx/src/README.md` | n/a | repo-owned documentation | n/a | none | Apache-2.0-compatible project documentation | Adapter-owned source boundary documentation |

## PR #377 Intake

PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377

Observed PR head commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`

The PR source changes were applied only to adapter-owned NGINX source files:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`

The imported PR tests/docs were not copied into the active smoke suite.
Phase-4 / `RESPONSE_BODY` behavior remains evidence-only; `RESPONSE_BODY` is
not added to `verified_variables` until a separate Apache+NGINX real-world
promotion proves stable HTTP behavior.

## Retained Upstream Reference Files

| Imported path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `connectors/nginx/upstream/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | License text for NGINX-derived adapter source |
| `connectors/nginx/upstream/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream attribution |
| `connectors/nginx/upstream/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream change context |
| `connectors/nginx/upstream/README.md` | `README.md` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream build and usage context |

## Excluded Upstream Files

The NGINX test harness, `.git`, `.github`, CI files, release scripts, Windows
build files, raw upstream tests, and build/runtime artifacts are not imported.
The previous upstream `config` and `src/*` files were migrated to
`connectors/nginx/src/` and removed from `connectors/nginx/upstream/` after a
passing materialized-source NGINX smoke.

## Central Attribution Copies

The NGINX upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are also mirrored
under `licenses/nginx/` for repository-level license review. The central
license directory is an attribution index; it does not replace this origin map.

## Pruning Review

Last reviewed in `docs/imports/upstream-pruning-analysis.md`.

`connectors/nginx/upstream/` is now a reference/attribution basis. Future
removal is allowed only after origin/license documentation remains complete and
real-world smoke evidence continues to pass.
