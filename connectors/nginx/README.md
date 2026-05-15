# NGINX Connector

Status: scaffolded

This directory contains the NGINX proof-of-concept harness for the external
ModSecurity-nginx connector source. It does not vendor or reimplement that
connector.

Implemented now:

- Documentation of observed local NGINX connector concepts.
- Directory layout for future source and connector-specific tests.
- A connector-specific runtime harness under `harness/`.
- Shared YAML case consumption through `tests/runners/case_cli.py`.
- Source-derived shared imported cases for raw JSON body matching, simple
  multipart text-field matching, and response-body pass-through.

Not implemented:

- No NGINX module source is imported into this monorepo.
- No full NGINX regression suite.
- No runtime pass is claimed beyond environments where the NGINX smoke runner
  observes the YAML-expected real HTTP behavior for the shared YAML cases.
- No response-body blocking pass is claimed; the upstream NGINX test marks that
  behavior TODO and this repository maps it as xfail until stable HTTP 403 is
  observed.

Primary local reference: `/root/conecter/ModSecurity-nginx`.

The build helper is `ci/prepare-nginx-build.sh`. It copies the external
ModSecurity-nginx source and libmodsecurity v3 source into `BUILD_ROOT`, then
builds the connector as a dynamic NGINX module against an official
`nginx/nginx` GitHub release archive.

Observed locally on 2026-05-15: `NGINX_RELEASE_TAG=latest` resolved to
`release-1.31.0`, built `nginx/1.31.0`, built
`ngx_http_modsecurity_module.so`, and the harness observed the YAML-expected
HTTP status for all current shared minimal cases.
