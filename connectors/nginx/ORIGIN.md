# NGINX Connector Origin Map

**Language:** English | [Deutsch](ORIGIN.de.md)

Status: adapter-owned source migration complete

Local reference: `<external-source-root>/ModSecurity-nginx`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source branch: `master`
Source commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source describe: `v1.0.4-14-g9eb44fd`
License: Apache-2.0, retained in `licenses/nginx/LICENSE`
Default imported path: `connectors/nginx`

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `<external-source-root>/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Central attribution: `licenses/nginx/`

## Adapter-Owned Source

NGINX now builds from a materialized source tree generated under
`$BUILD_ROOT/nginx-build/connector-src`. The module `config` is adapter-owned
at `connectors/nginx/config`, and productive module source is adapter-owned in
`connectors/nginx/src/`. The former
`connectors/nginx/upstream/` reference tree was removed in phase 10 after the
source migration, materialized-source build, and real NGINX smokes passed.

| Adapter-owned path | Original upstream path | Repo | Base commit | Extra provenance | License | Import reason |
| --- | --- | --- | --- | --- | --- | --- |
| `connectors/nginx/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX dynamic module build metadata |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX access phase integration |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | NGINX response/body filter integration plus phase-4 late-intervention changes |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | Shared NGINX connector declarations plus phase-4 mode/config fields |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX header filter integration |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX log phase integration |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | NGINX module entrypoint/config plus phase-4 directives |
| `connectors/nginx/src/ddebug.h` | `src/ddebug.h` | repo-owned compatibility header | n/a | replaces imported upstream debug helper | Apache-2.0-compatible project code | Keeps the NGINX module build dependency satisfied without retaining the imported debug helper in `upstream/` |
| `connectors/nginx/metadata.c` | n/a | repo-owned adapter metadata | n/a | none | Apache-2.0-compatible project code | Report/build-summary origin metadata |
| `connectors/nginx/metadata.h` | n/a | repo-owned adapter metadata | n/a | none | Apache-2.0-compatible project code | Report/build-summary origin metadata |
| `connectors/nginx/SOURCE_MAP.json` | n/a | repo-owned provenance manifest | n/a | records base and PR #377 provenance | Apache-2.0-compatible project metadata | Source migration and PR provenance map |

## Phase 13 Layout Moves

| Former path | Current path | Materialized path |
| --- | --- | --- |
| `connectors/nginx/src/config` | `connectors/nginx/config` | `config` |
| `connectors/nginx/src/metadata.*` | `connectors/nginx/metadata.*` | not materialized |
| `connectors/nginx/src/SOURCE_MAP.json` | `connectors/nginx/SOURCE_MAP.json` | not materialized |
| `connectors/nginx/src/README.md` | `connectors/nginx/README.md` and docs | not materialized |

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

## Durable Attribution Files

| Attribution path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `licenses/nginx/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | License text for NGINX-derived adapter source |
| `licenses/nginx/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream attribution |
| `licenses/nginx/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream change context |

## Excluded Upstream Files

The NGINX test harness, `.git`, `.github`, CI files, release scripts, Windows
build files, raw upstream tests, and build/runtime artifacts are not imported.
The previous upstream `config` and `src/*` files were migrated to
`connectors/nginx/src/`; the former `connectors/nginx/upstream/` directory was
removed after passing materialized-source NGINX smokes.

## Central Attribution Copies

The NGINX upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are mirrored under
`licenses/nginx/` for repository-level license review. The central license
directory is the durable attribution source; this origin map records how those
files relate to the adapter-owned source tree.

## Pruning Review

The Framework's current [connector integration guide](../../modules/ModSecurity-test-Framework/docs/connector-integration.md)
records the applicable source/catalog boundary.

`connectors/nginx/upstream/` was removed in phase 10. Future NGINX source
reductions should update `connectors/nginx/SOURCE_MAP.json`,
`licenses/nginx/`, and this origin map, then prove `smoke-nginx` and
`smoke-all` still pass.
