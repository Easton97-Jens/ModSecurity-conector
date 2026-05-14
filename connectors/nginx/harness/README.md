# NGINX Smoke Harness

Status: scaffolded

This harness is a connector-specific proof-of-concept runner for the dynamic
NGINX module built from the read-only `ModSecurity-nginx` source copy. It is not
a complete regression suite.

Observed locally on 2026-05-14: source-built NGINX `1.31.0` from GitHub tag
`release-1.31.0` returned HTTP `403` for the shared minimal `ARGS:test` case.

## Boundaries

- Uses only artifacts under `BUILD_ROOT`.
- Does not build or modify any `/root/conecter/*` repository.
- Does not import NGINX or ModSecurity-nginx source into this monorepo.
- Reports `pass` only when NGINX returns HTTP `403` for the shared minimal
  `ARGS:test` case.
- Reads rule, request, and expected status from
  `tests/common/cases/minimal/phase2_args_block.yaml` through
  `tests/runners/case_cli.py`.

## Usage

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
sh ci/prepare-nginx-build.sh

BUILD_ROOT=/src/ModSecurity-conector-build \
sh connectors/nginx/harness/run_nginx_smoke.sh
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

## Shared Case

The harness implements the same rule and request described by:

```text
tests/common/cases/minimal/phase2_args_block.yaml
```

The harness materializes the NGINX rule file and request variables from this
YAML file at runtime. Do not duplicate the rule, request path, or expected HTTP
status in the harness.
