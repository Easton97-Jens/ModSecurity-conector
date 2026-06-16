> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:38Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-system-environment-proof.py`
> Make target: `generate-system-environment-proof`
> Owner: `system`
> Severity: `critical`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `complete`

# System Environment Proof

## OS / System

| Field | Value |
|---|---|
| OS Name | Ubuntu |
| OS Version | 26.04 LTS (Resolute Raccoon) |
| Kernel | 7.0.0-22-generic |
| Architecture | x86_64 |
| Hostname | jens |
| User | root |
| Working Directory | `/root/git/ModSecurity-conector` |

## Framework Environment Resolution

| Field | Value |
|---|---|
| Framework root | `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework` |
| common.sh path | `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/common.sh` |
| common.sh status | `loaded` |
| common.sh return code | `0` |
| VERIFIED_RUN_ROOT | `/var/tmp/ModSecurity-conector-verified` |
| VERIFIED_STATE_ROOT | `/var/tmp/ModSecurity-conector-verified/state` |
| VERIFIED_BUILD_ROOT | `/var/tmp/ModSecurity-conector-verified/build` |
| VERIFIED_SOURCE_ROOT | `/var/tmp/ModSecurity-conector-verified/src` |
| VERIFIED_TMP_ROOT | `/var/tmp/ModSecurity-conector-verified/tmp` |
| VERIFIED_LOG_ROOT | `/var/tmp/ModSecurity-conector-verified/logs` |
| VERIFIED_COMPONENT_CACHE | `/var/tmp/ModSecurity-conector-verified/component-cache` |
| BUILD_ROOT | `/var/tmp/ModSecurity-conector-verified/build` |
| SOURCE_ROOT | `/var/tmp/ModSecurity-conector-verified/src` |
| TMP_ROOT | `/var/tmp/ModSecurity-conector-verified/tmp` |
| LOG_ROOT | `/var/tmp/ModSecurity-conector-verified/logs` |
| CONNECTOR_COMPONENT_CACHE | `/var/tmp/ModSecurity-conector-verified/component-cache` |
| NGINX_HARNESS_PARENT | `/var/tmp/ModSecurity-conector-verified/nginx-harness` |
| MATRIX_ROOT | `/var/tmp/ModSecurity-conector-verified/build/full-matrix` |
| MRTS_BUILD_ROOT | `/var/tmp/ModSecurity-conector-verified/build/mrts` |
| MRTS_NATIVE_ROOT | `/var/tmp/ModSecurity-conector-verified/build/mrts-native` |
| VERIFIED_RUN_ID | `2026-06-15T21-01-39Z-9391a8d0` |
| VERIFIED_RUN_PROFILE | `unset` |
| VERIFIED_RUN_FULL_MATRIX_TIMEOUT_SECONDS | `unset` |
| GO_FTW_BIN | `go-ftw` |
| GO_FTW_SOURCE_URL | `https://github.com/coreruleset/go-ftw` |
| GO_FTW_PROMPT_EXPECTED_LATEST | `v2.2.0` |
| GO_FTW_GIT_REF | `v2.2.0` |
| ALBEDO_BIN | `albedo` |
| ALBEDO_SOURCE_URL | `https://github.com/coreruleset/albedo` |
| ALBEDO_PROMPT_EXPECTED_LATEST | `v0.3.0` |
| ALBEDO_GIT_REF | `v0.3.0` |
| APACHECTL_BIN | `unset` |
| APACHE_BIN | `unset` |
| HTTPD_BIN | `unset` |
| HTTPD_VERSION | `2.4.67` |
| HTTPD_SOURCE_URL | `https://archive.apache.org/dist/httpd/httpd-2.4.67.tar.bz2` |
| APXS | `unset` |
| APXS_BIN | `unset` |
| NGINX_BIN | `unset` |
| NGINX_SOURCE_REPO_URL | `https://github.com/nginx/nginx` |
| NGINX_GITHUB_REPO | `https://github.com/nginx/nginx` |
| NGINX_RELEASE_TAG | `latest` |
| NGINX_SOURCE_GIT_REF | `latest` |
| CI_APACHE_BIN_CANDIDATES | `apache2 httpd apachectl` |
| CI_APXS_BIN_CANDIDATES | `apxs apxs2` |
| CI_NGINX_BIN_CANDIDATES | `nginx` |
| HAPROXY_BIN | `/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime/haproxy/sbin/haproxy` |
| HAPROXY_VERSION | `3.2.19` |
| HAPROXY_SOURCE_URL | `https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz` |
| HAPROXY_RUNTIME_DIR | `/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime/haproxy` |
| HAPROXY_RUNTIME_BUILD_DIR | `/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime-build` |
| EXPAT_SOURCE_URL | `https://github.com/libexpat/libexpat` |
| EXPAT_GIT_REF | `master` |
| EXPAT_GIT_URL | `https://github.com/libexpat/libexpat` |
| EXPAT_PROMPT_EXPECTED_LATEST | `master` |
| CC | `unset` |
| CLANG | `unset` |
| MAKE | `unset` |
| PYTHON | `.venv/bin/python` |

## Tool Versions

| Tool | Status | Resolved Command | Source | Candidates | Version / Output | Notes |
|---|---|---|---|---|---|---|
| git | present | `/usr/bin/git` | `PATH fallback` | `git` | `git version 2.53.0` | `` |
| python3 | present | `/usr/bin/python3` | `PATH fallback` | `python3` | `Python 3.14.4` | `` |
| python | present | `/root/git/ModSecurity-conector/.venv/bin/python` | `PYTHON from process/make environment` | `.venv/bin/python python3 python` | `Python 3.14.4` | `resolved by Make PYTHON, ci_python, then python3/python fallback` |
| make | present | `/usr/bin/make` | `PATH fallback` | `make` | `GNU Make 4.4.1` | `` |
| bash | present | `/usr/bin/bash` | `PATH fallback` | `bash` | `GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)` | `` |
| sh | present | `/usr/bin/dash` | `/bin/sh executable check` | `/bin/sh` | `POSIX shell available (/usr/bin/dash)` | `checked shell availability with /bin/sh -c instead of sh --version` |
| gcc | present | `/usr/bin/gcc` | `PATH fallback` | `gcc` | `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0` | `` |
| clang | present | `/usr/bin/clang` | `PATH fallback` | `clang` | `Ubuntu clang version 21.1.8 (6ubuntu1)` | `` |
| go | present | `/usr/bin/go` | `PATH fallback` | `go` | `go version go1.26.0 linux/amd64` | `` |
| go-ftw | missing | `go-ftw` | `GO_FTW_BIN from process/make environment` | `go-ftw` | `command not found` | `optional MRTS/FTW tool not installed or not in PATH` |
| albedo | missing | `albedo` | `ALBEDO_BIN from process/make environment` | `albedo` | `command not found` | `optional native MRTS tool not installed or not in PATH` |
| actionlint | missing | `` | `PATH fallback` | `actionlint` | `command not found` | `` |
| jq | present | `/usr/bin/jq` | `PATH fallback` | `jq` | `jq-1.8.1` | `` |
| curl | present | `/usr/bin/curl` | `PATH fallback` | `curl` | `curl 8.18.0 (x86_64-pc-linux-gnu) libcurl/8.18.0 OpenSSL/3.5.5 zlib/1.3.1 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.68.0 librtmp/2.3 mit-krb5/1.22.1 OpenLDAP/2.6.10` | `` |
| docker | missing | `` | `PATH fallback` | `docker` | `command not found` | `` |
| apachectl | missing | `` | `CI_APACHE_BIN_CANDIDATES from framework common.sh` | `apachectl` | `no candidate found: apachectl` | `APACHECTL_BIN is unset; checked apachectl candidate` |
| apache/httpd | missing | `` | `CI_APACHE_BIN_CANDIDATES from framework common.sh` | `apache2 httpd apachectl` | `no candidate found: apache2 httpd apachectl` | `APACHECTL_BIN/APACHE_BIN are unset; checked APXS helper and framework candidates` |
| nginx | missing | `` | `CI_NGINX_BIN_CANDIDATES from framework common.sh` | `nginx` | `no candidate found: nginx` | `NGINX_BIN is unset; checked framework candidates` |
| haproxy | configured_missing | `/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime/haproxy/sbin/haproxy` | `HAPROXY_BIN from framework common.sh` | `` | `file not found` | `runtime path configured by common.sh but binary has not been built/prepared locally; HAPROXY_VERSION=3.2.19; HAPROXY_SOURCE_URL=https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz; HAPROXY_RUNTIME_DIR=/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime/haproxy; HAPROXY_RUNTIME_BUILD_DIR=/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime-build` |
| apxs | missing | `` | `CI_APXS_BIN_CANDIDATES from framework common.sh` | `apxs apxs2` | `no candidate found: apxs apxs2` | `APXS_BIN is unset; checked framework candidates` |

## Runtime Component Readiness

| Component | Status | Expected Path | Source URL | Version / Ref | How to Prepare |
|---|---|---|---|---|---|
| HAProxy | configured_missing | `/var/tmp/ModSecurity-conector-verified/build/haproxy-runtime/haproxy/sbin/haproxy` | `https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz` | `3.2.19` | `make prepare-runtime-components or make runtime-matrix-haproxy` |
| NGINX | missing | `nginx` | `https://github.com/nginx/nginx` | `latest` | `install nginx or prepare runtime components` |
| Apache/APXS | missing | `apxs apxs2` | `https://archive.apache.org/dist/httpd/httpd-2.4.67.tar.bz2` | `2.4.67` | `install apache2-dev/httpd-devel or prepare Apache runtime` |
| go-ftw | missing_optional | `go-ftw` | `https://github.com/coreruleset/go-ftw` | `v2.2.0` | `install go-ftw only if MRTS/FTW checks are required` |
| albedo | missing_optional | `albedo` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `install albedo only if native MRTS checks require it` |
| expat | informational | `n/a` | `https://github.com/libexpat/libexpat` | `master` | `used only if the related runtime build path requires it` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/modules` |
| ModSecurity module path | `/var/tmp/ModSecurity-conector-verified/build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `false` |
| How to prepare | `make prepare-runtime-components` |

## Verified Producer Readiness

| Producer | Required | Status | Missing Tools | Missing Paths | How to Fix |
|---|---|---|---|---|---|
| prepare-runtime-components | True | not_run | - | `BUILD_ROOT=/var/tmp/ModSecurity-conector-verified/build`<br>`SOURCE_ROOT=/var/tmp/ModSecurity-conector-verified/src`<br>`CONNECTOR_COMPONENT_CACHE=/var/tmp/ModSecurity-conector-verified/component-cache` | `ensure VERIFIED_RUN_ROOT points outside /root and rerun make prepare-runtime-components` |
| runtime-matrix-all | True | not_run | - | `BUILD_ROOT=/var/tmp/ModSecurity-conector-verified/build`<br>`TMP_ROOT=/var/tmp/ModSecurity-conector-verified/tmp`<br>`LOG_ROOT=/var/tmp/ModSecurity-conector-verified/logs`<br>`NGINX_HARNESS_PARENT=/var/tmp/ModSecurity-conector-verified/nginx-harness` | `run make runtime-matrix-all after prepare-runtime-components; inspect the verified command log on BLOCKED/FAIL` |
| full-matrix-parallel | True | not_run | - | `MATRIX_ROOT=/var/tmp/ModSecurity-conector-verified/build/full-matrix` | `run make verified-report-run with safe BUILD_ROOT/MATRIX_ROOT paths` |
| mrts-native-full-run | False | not_run | go-ftw, albedo, apachectl, apache/httpd, nginx, apxs | `MRTS_NATIVE_ROOT=/var/tmp/ModSecurity-conector-verified/build/mrts-native` | `install optional go-ftw/albedo/native webserver tooling or leave native MRTS as optional WARN evidence` |

## Runtime Network / Cache Readiness

| Source | Status | Path | Notes |
|---|---|---|---|
| nginx latest release | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx/nginx-latest-release.json` | network may be required unless this cache is prefilled |
| nginx archive cache | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx` | network may be required unless this cache is prefilled |
| go-ftw git cache | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/git/go-ftw` | network may be required unless this cache is prefilled |
| albedo git cache | missing | `/var/tmp/ModSecurity-conector-verified/component-cache/git/albedo` | network may be required unless this cache is prefilled |

## HTTPS Repository URL Policy

| Check | Status | Notes |
|---|---|---|
| HTTPS-only repo URLs | PASS | no active http, ssh, git protocol repo URLs found |
| GitHub repo URL policy | PASS | only https://github.com/owner/repo accepted |

## Python Environment

| Field | Value |
|---|---|
| sys.version | `3.14.4 (main, Apr  8 2026, 04:02:31) [GCC 15.2.0]` |
| sys.executable | `/root/git/ModSecurity-conector/.venv/bin/python` |
| sys.platform | `linux` |
| platform.platform() | `Linux-7.0.0-22-generic-x86_64-with-glibc2.43` |
| PYTHONPATH | `` |
| PYTHONDONTWRITEBYTECODE | `1` |
| .venv exists | `True` |
| pip --version | `pip 26.1.2 from /root/git/ModSecurity-conector/.venv/lib/python3.14/site-packages/pip (python 3.14)` |
| pip freeze packages in excerpt | `1` |
| pip freeze output hash | `0969da99a0bc2a1b71ed50584560f4588a37567ac63af3ddbaf3c4617ca5621a` |

## Executed Checks

| Command | Status | Return Code | Duration | Notes |
|---|---|---:|---:|---|
| `make refresh-connector-reports` | PASS | 0 | 12.935 | make[1]: Leaving directory '/root/git/ModSecurity-conector' |
| `env ALLOW_IN_PROGRESS_SYSTEM_PROOF=1 make check-generated-report-layout` | FAIL | 2 | 0.733 | - reports/tes |
| `make lint` | FAIL | 2 | 2.337 | - reports/tes |
| `make quick-check` | FAIL | 2 | 2.407 | - reports/tes |
| `git status --short` | PASS | 0 | 0.036 |  M reports/testing/generated/manifest/generator-runtime-summary.g |

## Report Layout Evidence

| Metric | Value |
|---|---|
| Generated report files | 72 |
| Flat files in generated root | 0 |
| Categories | 8 (cache, canonical, coverage, focused-analysis, manifest, mrts-native, runtime, work-queues) |
| Missing registry outputs | 0 |
| Orphan generated reports | 0 |
| Skipped reports | 4 |
| Failed reports | 0 |

## Known Skipped Inputs

| Report | Status | Missing Inputs | Reason |
|---|---|---|---|
| `full_runtime_matrix` | skipped_missing_input | `BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl` | local optional inputs are missing or unavailable |
| `full_matrix_job_completeness` | skipped_missing_input | `BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl` | local optional inputs are missing or unavailable |
| `verified_runtime_mismatch_analysis` | skipped_missing_input | `BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl` | local optional inputs are missing or unavailable |
| `native_mrts_reports` | skipped_missing_input | `BUILD_ROOT:mrts-native/apache2_ubuntu/job.json`, `BUILD_ROOT:mrts-native/nginx-pr24/job.json` | local optional inputs are missing or unavailable |

## Git Evidence

| Command | Status | Return Code | Output Hash |
|---|---|---:|---|
| `git_status_short` | PASS | 0 | `af82b46abd9242cf26d19b27c2181d2f3b8099b3388e1f6be8054cb3713bac98` |
| `git_head` | PASS | 0 | `558e224e7252db7e45e0a166d73c204972439861f23fc6103cabb67f1a083097` |
| `git_branch` | PASS | 0 | `9b3162498c21d7f960877099174ecea13410bd21d12440b2ea8868117fc08ae0` |
| `git_submodule_status` | PASS | 0 | `ba754e980921ceb1383dff6098c68e024eb0a9685c7cb46e2b4d5b1e7c4a09d9` |
| `git_diff_stat` | PASS | 0 | `0763bc8c44779eb5527d00f6542370fb2d660372042669d34d657698f7c506c2` |
| `framework_status_short` | PASS | 0 | `71bdd1bb7c1d2a8e9a2a00ed8ab6fd6c9b52f3e1bd6bb5b9fae08871e729d216` |
| `framework_head` | PASS | 0 | `581c4df039742c77cdf43b701e86c8df464a18be0f6228affa6782e64a237cb9` |
| `framework_diff_stat` | PASS | 0 | `70c566428775b54af10b200083b582a3d5ec2ddd8d37e8b0e7e1e45366451836` |

## Proof Summary

The generated report layout was validated on the system above.
- `make refresh-connector-reports`: PASS
- `env ALLOW_IN_PROGRESS_SYSTEM_PROOF=1 make check-generated-report-layout`: FAIL
- `make lint`: FAIL
- `make quick-check`: FAIL
- `git status --short`: PASS
- Flat generated root files: 0
- Categorized generated report files: 72
- Known skipped report: runtime/cache reports due to missing optional local inputs

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `ae5644b7e45dc2fedaa289b57881489257e53a99bc341d1ad853fb3a84eda33a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `7d4f982b8cc29d3c1b36b372ceaedf66a18ed73e9d0ac3dadae9ba7bd93d3d0f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `63c224e072428210f66b357e0b6bcdaffaf8435ba571277d625452943e31eed9` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
