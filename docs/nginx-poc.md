# NGINX Connector PoC

Status: scaffolded

## Implemented

- `ci/prepare-nginx-build.sh` prepares a connector-specific NGINX PoC build
  under `BUILD_ROOT`.
- The helper copies the read-only libmodsecurity v3 and ModSecurity-nginx
  sources into `$BUILD_ROOT/nginx-build/` and builds only inside those copies.
- NGINX source is downloaded from the official `nginx/nginx` GitHub release
  archive flow.
- `connectors/nginx/harness/run_nginx_smoke.sh` prepares a local NGINX runtime
  under `BUILD_ROOT` and checks for a real HTTP `403`.
- The shared minimal YAML cases under `tests/common/cases/minimal/` are the
  rule/request/expectation source used by both Apache and NGINX harnesses.

Implemented here means build orchestration, runtime harness, shared-case
integration, and documentation. It does not mean every environment can build or
run the NGINX module.

## Build Flow

Defaults are local conveniences only:

```sh
MODSECURITY_V3_SOURCE_DIR=/root/conecter/ModSecurity_V3
MODSECURITY_NGINX_SOURCE_DIR=/root/conecter/ModSecurity-nginx
BUILD_ROOT=/src/ModSecurity-conector-build
LOG_DIR=$BUILD_ROOT/logs/nginx
```

All paths are environment-overridable. Generated files must stay outside the
Git checkout and outside `/root/conecter/*`.

Run the build helper with:

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
sh ci/prepare-nginx-build.sh
```

The helper builds libmodsecurity v3 in:

```text
$BUILD_ROOT/nginx-build/ModSecurity_V3
```

It stages libmodsecurity headers and shared libraries under:

```text
$BUILD_ROOT/nginx-build/output/modsecurity/include/
$BUILD_ROOT/nginx-build/output/modsecurity/lib/
```

The NGINX connector build uses the observed ModSecurity-nginx dynamic module
path:

```text
MODSECURITY_INC=$BUILD_ROOT/nginx-build/output/modsecurity/include
MODSECURITY_LIB=$BUILD_ROOT/nginx-build/output/modsecurity/lib
auto/configure --with-compat --add-dynamic-module=$BUILD_ROOT/nginx-build/ModSecurity-nginx
```

The helper uses `auto/configure` when that script is present in the GitHub
archive, or `./configure` if an archive provides it.

## NGINX Source Mode

Default source mode:

```sh
NGINX_SOURCE_MODE=github-release
NGINX_GITHUB_REPO=https://github.com/nginx/nginx
NGINX_RELEASE_TAG=latest
```

When `NGINX_RELEASE_TAG=latest`, the helper queries:

```text
https://api.github.com/repos/nginx/nginx/releases/latest
```

and extracts `tag_name` with `python3`. The actual tag is written to:

```text
$BUILD_ROOT/logs/nginx/artifacts.txt
```

Observed during planning on 2026-05-15: GitHub reported `release-1.31.0` as the
latest release. The helper does not hardcode this value.

For a pinned release:

```sh
NGINX_RELEASE_TAG=release-1.31.0 sh ci/prepare-nginx-build.sh
```

The archive URL is:

```text
https://github.com/nginx/nginx/archive/refs/tags/<TAG>.tar.gz
```

The helper always computes a local SHA256 and records it. If `NGINX_SHA256` is
set, the helper verifies the archive against that value. If `NGINX_SHA256` is
unset, the local hash is documentation only and is not claimed as upstream
verification.

## Runtime Smoke

The NGINX harness renders `connectors/nginx/harness/nginx_smoke.conf` into a
per-case runtime directory, for example:

```text
$BUILD_ROOT/nginx-runtime/phase2_args_block/conf/nginx.conf
```

Rules, request details, and expected statuses are read from:

```text
tests/common/cases/minimal/*.yaml
```

The harness does not hardcode the rule, request path, request method, or
expected HTTP status. Status `pass` is only valid when the common runner checks
the observed NGINX response against each YAML expectation.

Run the smoke after a successful build:

```sh
BUILD_ROOT=/src/ModSecurity-conector-build \
make smoke-nginx
```

## Current Local Status

Observed in this workspace on 2026-05-15:

- `REFRESH=1 BUILD_NGINX_FROM_SOURCE=1
  BUILD_ROOT=/src/ModSecurity-conector-build sh ci/prepare-nginx-build.sh`
  built libmodsecurity v3 in a writable copy, resolved the NGINX release
  through GitHub, built NGINX, and produced the ModSecurity dynamic module.
- `BUILD_ROOT=/src/ModSecurity-conector-build make smoke-nginx` returned pass
  for all current shared minimal cases.
- `BUILD_ROOT=/src/ModSecurity-conector-build make smoke-apache` also returned
  pass for the same shared YAML cases.

Observed NGINX source and artifact details:

```text
nginx_source_mode=github-release
nginx_release_tag_requested=latest
nginx_release_tag_resolved=release-1.31.0
nginx_archive_url=https://github.com/nginx/nginx/archive/refs/tags/release-1.31.0.tar.gz
nginx_archive_sha256_local=a450299c82f24aebae00203f09995d02b3d3611622bfe2461e62cc858f963122
nginx_archive_sha256_verified=0
nginx_version=nginx/1.31.0
nginx_binary=/src/ModSecurity-conector-build/nginx-runtime/nginx/sbin/nginx
nginx_module=/src/ModSecurity-conector-build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
nginx_smoke_cases=phase1_header_block, phase2_args_block, request_body_json_block, request_body_urlencoded_block, response_header_basic
nginx_smoke_status=all pass, HTTP 403
```

The SHA256 value above is the local hash of the GitHub archive downloaded in
this workspace. It is not an upstream checksum because `NGINX_SHA256` was not
set.

## Status Meanings

- `implemented`: helper scripts, harness template, shared case integration, and
  docs exist.
- `blocked`: required source, download, build dependency, module, or library
  prerequisite is missing; no functionality is claimed.
- `fail`: prerequisites exist but a build, configtest, startup, or HTTP
  expectation fails.
- `pass`: NGINX returns the YAML-expected HTTP status for every selected shared
  smoke case.

## Open TODOs

- Run the NGINX build and runtime smoke in every target environment before
  claiming pass there.
- Investigate any NGINX latest-release compatibility failure as a connector
  build issue, not a guessed dependency issue.
- Promote only proven NGINX behavior into connector-specific regression tests.

## Public Sources

- Official NGINX Open Source repository: https://github.com/nginx/nginx
- GitHub latest release API:
  https://api.github.com/repos/nginx/nginx/releases/latest
- NGINX configure documentation: https://nginx.org/en/docs/configure.html
- ModSecurity-nginx local source: `/root/conecter/ModSecurity-nginx`
