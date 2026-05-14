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

Not implemented:

- No NGINX module source is imported into this monorepo.
- No full NGINX regression suite.
- No runtime pass is claimed beyond environments where `run_nginx_smoke.sh`
  observes real HTTP `403` for the shared `phase2_args_block` case.

Primary local reference: `/root/conecter/ModSecurity-nginx`.

The build helper is `ci/prepare-nginx-build.sh`. It copies the external
ModSecurity-nginx source and libmodsecurity v3 source into `BUILD_ROOT`, then
builds the connector as a dynamic NGINX module against an official
`nginx/nginx` GitHub release archive.

Observed locally on 2026-05-14: `NGINX_RELEASE_TAG=latest` resolved to
`release-1.31.0`, built `nginx/1.31.0`, built
`ngx_http_modsecurity_module.so`, and the harness observed HTTP `403`.
