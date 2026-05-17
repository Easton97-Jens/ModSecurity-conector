# NGINX Connector

Status: scaffolded

This directory contains the NGINX proof-of-concept harness and controlled
upstream import for the ModSecurity-nginx connector source. It does not claim a
maintained rewrite of that connector.

Implemented now:

- Documentation of observed local NGINX connector concepts.
- Directory layout for future source and connector-specific tests.
- A connector-specific runtime harness under `harness/`.
- Shared YAML case consumption through `tests/runners/case_cli.py`.
- Source-derived shared imported cases for raw JSON body matching, simple
  multipart text-field matching, and response-body pass-through.

Not implemented:

- No maintained NGINX module rewrite beyond the controlled upstream import.
- No full NGINX regression suite.
- No runtime pass is claimed beyond environments where the NGINX smoke runner
  observes the YAML-expected real HTTP behavior for the shared YAML cases.
- No response-body blocking pass is claimed; the upstream NGINX test marks that
  behavior TODO and this repository maps it as xfail until stable HTTP 403 is
  observed.

Primary local reference: `/root/conecter/ModSecurity-nginx`.
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx.

The controlled imported source lives under `connectors/nginx/upstream/` as a
temporary reference/import basis. It may shrink only after equivalent project
code exists, origin is still documented, and smokes keep passing.

The build helper is `ci/prepare-nginx-build.sh`. It copies the external
ModSecurity-nginx source and libmodsecurity v3 source into `BUILD_ROOT`, then
builds the connector as a dynamic NGINX module against an official
`nginx/nginx` GitHub release archive.

Observed locally on 2026-05-15: `NGINX_RELEASE_TAG=latest` resolved to
`release-1.31.0`, built `nginx/1.31.0`, built
`ngx_http_modsecurity_module.so`, and the harness observed the YAML-expected
HTTP status for all current shared minimal cases.
