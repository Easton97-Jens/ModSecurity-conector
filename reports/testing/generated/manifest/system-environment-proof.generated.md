> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:51:10Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-system-environment-proof.py`
> Make target: `generate-system-environment-proof`
> Owner: `system`
> Severity: `critical`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
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
| BUILD_ROOT | `/root/.local/state/ModSecurity-conector-build` |
| SOURCE_ROOT | `/root/.local/state/ModSecurity-conector-src` |
| TMP_ROOT | `/root/.local/state/ModSecurity-conector-build/tmp` |
| LOG_ROOT | `/root/.local/state/ModSecurity-conector-build/logs` |
| CONNECTOR_COMPONENT_CACHE | `/root/.local/state/ModSecurity-conector-build/component-cache` |
| NGINX_HARNESS_PARENT | `/root/.local/state/ModSecurity-conector-build/tmp/nginx-harness` |
| MATRIX_ROOT | `unset` |
| MRTS_BUILD_ROOT | `/root/.local/state/ModSecurity-conector-build/mrts` |
| MRTS_NATIVE_ROOT | `/root/.local/state/ModSecurity-conector-build/mrts-native` |
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
| HAPROXY_BIN | `/root/.local/state/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy` |
| HAPROXY_VERSION | `3.2.19` |
| HAPROXY_SOURCE_URL | `https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz` |
| HAPROXY_RUNTIME_DIR | `/root/.local/state/ModSecurity-conector-build/haproxy-runtime/haproxy` |
| HAPROXY_RUNTIME_BUILD_DIR | `/root/.local/state/ModSecurity-conector-build/haproxy-runtime-build` |
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
| haproxy | configured_missing | `/root/.local/state/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy` | `HAPROXY_BIN from framework common.sh` | `` | `file not found` | `runtime path configured by common.sh but binary has not been built/prepared locally; HAPROXY_VERSION=3.2.19; HAPROXY_SOURCE_URL=https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz; HAPROXY_RUNTIME_DIR=/root/.local/state/ModSecurity-conector-build/haproxy-runtime/haproxy; HAPROXY_RUNTIME_BUILD_DIR=/root/.local/state/ModSecurity-conector-build/haproxy-runtime-build` |
| apxs | missing | `` | `CI_APXS_BIN_CANDIDATES from framework common.sh` | `apxs apxs2` | `no candidate found: apxs apxs2` | `APXS_BIN is unset; checked framework candidates` |

## Runtime Component Readiness

| Component | Status | Expected Path | Source URL | Version / Ref | How to Prepare |
|---|---|---|---|---|---|
| HAProxy | configured_missing | `/root/.local/state/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy` | `https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz` | `3.2.19` | `make prepare-runtime-components or make runtime-matrix-haproxy` |
| NGINX | missing | `nginx` | `https://github.com/nginx/nginx` | `latest` | `install nginx or prepare runtime components` |
| Apache/APXS | missing | `apxs apxs2` | `https://archive.apache.org/dist/httpd/httpd-2.4.67.tar.bz2` | `2.4.67` | `install apache2-dev/httpd-devel or prepare Apache runtime` |
| go-ftw | missing_optional | `go-ftw` | `https://github.com/coreruleset/go-ftw` | `v2.2.0` | `install go-ftw only if MRTS/FTW checks are required` |
| albedo | missing_optional | `albedo` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `install albedo only if native MRTS checks require it` |
| expat | informational | `n/a` | `https://github.com/libexpat/libexpat` | `master` | `used only if the related runtime build path requires it` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules` |
| ModSecurity module path | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `true` |
| How to prepare | `make prepare-runtime-components` |

## Verified Producer Readiness

| Producer | Required | Status | Missing Tools | Missing Paths | How to Fix |
|---|---|---|---|---|---|
| prepare-runtime-components | True | not_run | - | `BUILD_ROOT=/root/.local/state/ModSecurity-conector-build`<br>`SOURCE_ROOT=/root/.local/state/ModSecurity-conector-src`<br>`CONNECTOR_COMPONENT_CACHE=/root/.local/state/ModSecurity-conector-build/component-cache` | `ensure BUILD_ROOT, SOURCE_ROOT, TMP_ROOT, LOG_ROOT and CONNECTOR_COMPONENT_CACHE are under $HOME/.local/state, then run make prepare-runtime-components` |
| runtime-matrix-all | True | not_run | - | `BUILD_ROOT=/root/.local/state/ModSecurity-conector-build`<br>`TMP_ROOT=/root/.local/state/ModSecurity-conector-build/tmp`<br>`LOG_ROOT=/root/.local/state/ModSecurity-conector-build/logs`<br>`NGINX_HARNESS_PARENT=/root/.local/state/ModSecurity-conector-build/tmp/nginx-harness` | `run make runtime-matrix-all after prepare-runtime-components; inspect the verified command log on BLOCKED/FAIL` |
| full-matrix-parallel | True | not_run | - | `MATRIX_ROOT=$BUILD_ROOT/full-matrix` | `run make verified-report-run with safe BUILD_ROOT/MATRIX_ROOT paths` |
| mrts-native-full-run | False | not_run | go-ftw, albedo, apachectl, apache/httpd, nginx, apxs | `MRTS_NATIVE_ROOT=/root/.local/state/ModSecurity-conector-build/mrts-native` | `install optional go-ftw/albedo/native webserver tooling or leave native MRTS as optional WARN evidence` |

## Runtime Network / Cache Readiness

| Source | Status | Path | Notes |
|---|---|---|---|
| nginx latest release | present | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx/nginx-latest-release.json` | local cache available |
| nginx archive cache | present | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx` | local cache available |
| go-ftw git cache | present | `/root/.local/state/ModSecurity-conector-build/component-cache/git/go-ftw` | local cache available |
| albedo git cache | present | `/root/.local/state/ModSecurity-conector-build/component-cache/git/albedo` | local cache available |

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
| `make refresh-connector-reports` | PASS | 0 | 138.457 | refresh-connector-reports: RUN /root/git/ModSecurity-conector/.venv/bin/python /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/genera |
| `env ALLOW_IN_PROGRESS_SYSTEM_PROOF=1 make check-generated-report-layout` | FAIL | 2 | 1.326 | - reports/testing/generated/manifest/report-refresh-manifest.generated.json: critical report input  |
| `make lint` | FAIL | 2 | 3.1 | - reports/testing/generated/manifest/report- |
| `make quick-check` | FAIL | 2 | 3.106 | - reports/testing/generated/manifest/report- |
| `git status --short` | PASS | 0 | 0.028 |  M reports/testing/generated/manifes |

## Report Layout Evidence

| Metric | Value |
|---|---|
| Generated report files | 70 |
| Flat files in generated root | 0 |
| Categories | 8 (cache, canonical, coverage, focused-analysis, manifest, mrts-native, runtime, work-queues) |
| Missing registry outputs | 0 |
| Orphan generated reports | 0 |
| Skipped reports | 3 |
| Failed reports | 0 |

## Known Skipped Inputs

| Report | Status | Missing Inputs | Reason |
|---|---|---|---|
| `intervention_blocking_analysis` | skipped_stale_input | - | local optional inputs are missing or unavailable |
| `body_processor_analysis` | skipped_stale_input | - | local optional inputs are missing or unavailable |
| `rule_chain_semantics_analysis` | skipped_stale_input | - | local optional inputs are missing or unavailable |

## Git Evidence

| Command | Status | Return Code | Output Hash |
|---|---|---:|---|
| `git_status_short` | PASS | 0 | `9920275fade259f4b5ae05069bce988b154ba229f7f3c63a9fe4c7e133014f5b` |
| `git_head` | PASS | 0 | `3defb3e2731c6bdbf606df563c53f3777621ffd237acf9387602a80d500c85f3` |
| `git_branch` | PASS | 0 | `9b3162498c21d7f960877099174ecea13410bd21d12440b2ea8868117fc08ae0` |
| `git_submodule_status` | PASS | 0 | `7e9d4ff8259566b541ffc78874c53d4c1c700c346a3e85f41cac0278ee468988` |
| `git_diff_stat` | PASS | 0 | `6f1e98715f3dd59de624b4cffdd5452c0b1fdf848c24cd32b83d60b49fe69235` |
| `framework_status_short` | PASS | 0 | `bbf2c2c9a063e43ddc9d8473907284c3e346bef1e6ce32efd0977caa4391777e` |
| `framework_head` | PASS | 0 | `dd6af8fcb53e7491364b71e664ac8e010a321cd7c6fe6cfc118afc8bf9b55cb5` |
| `framework_diff_stat` | PASS | 0 | `d188fb08e3c3de2398bfb9ecc90eb134e4731c69a8176f703318049b0f261753` |

## Proof Summary

The generated report layout was validated on the system above.
- `make refresh-connector-reports`: PASS
- `env ALLOW_IN_PROGRESS_SYSTEM_PROOF=1 make check-generated-report-layout`: FAIL
- `make lint`: FAIL
- `make quick-check`: FAIL
- `git status --short`: PASS
- Flat generated root files: 0
- Categorized generated report files: 70
- Known skipped report: runtime/cache reports due to missing optional local inputs

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `a3b1413388e5767d2ddae37b06576c5ca338a7ffc8e132d47bb3b1af5fa148a4` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `d816c3ea81eb97ce2a3c30ff8c0236234a555a34bc6730dce20f660b89ccb2db` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `424246dcf26c7ab6b190f4b91b71277395ca5d8943ee927903d819a0bc7d6489` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
