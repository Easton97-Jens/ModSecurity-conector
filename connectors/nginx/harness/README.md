# NGINX Smoke Harness

**Language:** English | [Deutsch](README.de.md)

Status: scaffolded

This harness is a connector-specific proof-of-concept runner for the dynamic
NGINX module built from the read-only `ModSecurity-nginx` source copy. It is not
a complete regression suite.

Observed locally on 2026-05-15: source-built NGINX `1.31.0` from GitHub tag
`release-1.31.0` returned the YAML-expected HTTP status for all current shared
minimal cases.

## Boundaries

- Uses only artifacts under `BUILD_ROOT`.
- Does not build or modify any `<external-source-root>/*` repository.
- Does not import NGINX or ModSecurity-nginx source into this monorepo.
- Reports `pass` only when NGINX returns the YAML-expected HTTP status for a
  real local request.
- Reads rule, request, headers, body, multipart body, response fixture, and
  expected status from YAML through `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.

## Usage

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
make smoke-nginx

BUILD_ROOT=/src/ModSecurity-conector-build \
make smoke-nginx
```

The build helper defaults to the official GitHub release source:

```sh
NGINX_SOURCE_MODE=github-release
NGINX_GITHUB_REPO=https://github.com/nginx/nginx
NGINX_RELEASE_TAG=latest
```

When `NGINX_RELEASE_TAG=latest`, the helper queries the GitHub Releases API and
records the actual tag in `$BUILD_ROOT/logs/nginx/artifacts.txt`. To pin a
specific release, set `NGINX_RELEASE_TAG=release-1.31.0` or another exact tag.

If NGINX, the dynamic module, or `libmodsecurity.so` is missing, the script
exits `77` and marks the result as `blocked`.

## Native P3/P4 and HTTP/2 applicability evidence

The real-host harness routes cases that use `RESPONSE_HEADERS` through its
local deterministic upstream. This is the native Phase-3 path; it is not a
synthetic response header. The canonical full-lifecycle selection also adds the
connector-specific Phase-4 safe and strict cases. Their results must remain
separate: safe expects a post-commit `log_only` event, while strict expects a
post-commit `connection_aborted` event. Both events carry
`integration_mode: native-nginx-http-module`.

Every host invocation records the selected binary's `nginx -V` output in
`$LOG_DIR/nginx-version.log` and writes
`$LOG_DIR/nginx-http2-applicability.json`. The file is deliberately
conservative:

- no `--with-http_v2_module` means `NOT_APPLICABLE`, so the harness makes no
  HTTP/2 request;
- a host with that flag is still `NOT_EXECUTED` until a connector-owned HTTP/2
  case and matching listener configuration are selected.

Consequently neither a successful build nor the presence of the configure flag
is an HTTP/2 runtime claim.

## Shared Cases

By default the harness iterates every `*.yaml` file in:

```text
modules/ModSecurity-test-Framework/tests/cases/
modules/ModSecurity-test-Framework/tests/cases/
modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/
```

To run a subset:

```sh
BUILD_ROOT=/src/ModSecurity-conector-build \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-nginx
```

The harness materializes the NGINX rule file, request variables, request
headers, request body, multipart body, and response fixture from each YAML file
at runtime. It uses `/__modsec_smoke_ready` with ModSecurity disabled only for
readiness checks. Do not duplicate the rule, request path, request method,
headers, body, response fixture, or expected HTTP status in the harness.

Response-body blocking remains non-promoted until the NGINX smoke observes a
stable HTTP 403 for the same common YAML case.
