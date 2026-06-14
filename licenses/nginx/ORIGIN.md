# NGINX Connector License Origin

Status: implemented

This directory mirrors the upstream license and attribution files for the
controlled NGINX connector source import. The default NGINX build source is now
adapter-owned under `connectors/nginx/src`; the former
`connectors/nginx/upstream/` reference tree was removed in phase 10. This
directory is the durable attribution location.

Repo-local reference: `connectors/nginx/`, `licenses/nginx/`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source branch: `master`
Source commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source describe: `v1.0.4-14-g9eb44fd`
License: Apache-2.0
Default imported path: `connectors/nginx/src`

| Repository | Repo-local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `connectors/nginx/`, `licenses/nginx/` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

## Files

| Central path | Source path | Purpose |
| --- | --- | --- |
| `licenses/nginx/LICENSE` | Upstream `LICENSE` | Apache-2.0 license text for imported NGINX connector source |
| `licenses/nginx/AUTHORS` | Upstream `AUTHORS` | Upstream attribution |
| `licenses/nginx/CHANGES` | Upstream `CHANGES` | Upstream change context |

## Imported Source Map

The full file-by-file source map remains in
`connectors/nginx/ORIGIN.md`. The adapter-owned source map also records the
ModSecurity-nginx PR #377 source provenance:

- PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377
- PR head commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`
- Affected adapter-owned files:
  `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`,
  `connectors/nginx/src/ngx_http_modsecurity_common.h`, and
  `connectors/nginx/src/ngx_http_modsecurity_module.c`

This central license directory is the durable attribution index for NGINX and
is paired with the adapter-owned `SOURCE_MAP.json`.
