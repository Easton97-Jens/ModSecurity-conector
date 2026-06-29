> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:57:53Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-system-environment-proof.py`
> Make target: `generate-system-environment-proof`
> Owner: `system`
> Severity: `critical`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# System Environment Proof

**Language:** English | [Deutsch](system-environment-proof.generated.de.md)

## Proof Status

| Field | Value |
|---|---|
| Proof generation status | `PASS` |
| Embedded strict evidence gate | `PASS` |
| Overall target status | `PASS` |
| Strict gate reason | strict generated-report evidence gate passed |

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
| VERIFIED_RUN_ID | `2026-06-16T19-12-00Z-614c8049` |
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
| NGINX_BIN | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules` |
| ModSecurity module path | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `true` |
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
| nginx latest release | present | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx/nginx-latest-release.json` | local cache available |
| nginx archive cache | present | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx` | local cache available |
| go-ftw git cache | present | `/var/tmp/ModSecurity-conector-verified/component-cache/git/go-ftw` | local cache available |
| albedo git cache | present | `/var/tmp/ModSecurity-conector-verified/component-cache/git/albedo` | local cache available |

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
| `make refresh-connector-reports` | PASS | 0 | 87.639 | refresh-connector-reports: RUN /root/git/ModSecurity-conector/.v |
| `env ALLOW_IN_PROGRESS_SYSTEM_PROOF=1 make check-generated-report-layout` | PASS | 0 | 1.508 | make[1]: Leaving directory '/root/git/ModSecurity-conector' |
| `make lint` | PASS | 0 | 6.435 | make[1]: Leaving directory '/root/git/ModSecurity-conector' |
| `make quick-check` | PASS | 0 | 7.576 | PYTHONPYCACHEPREFIX="/var/tmp/ModSecurity-conector-verified/build/pycache" .venv/bin/python -P -m py_compile "/root/git/ModSecurity-conector/modules/ModSecurity-test-Fra |
| `git status --short` | PASS | 0 | 0.106 |  M reports/testing/generated/manifest/report-path-migration.generate |

## Report Layout Evidence

| Metric | Value |
|---|---|
| Generated report files | 78 |
| Flat files in generated root | 0 |
| Categories | 8 (cache, canonical, coverage, focused-analysis, manifest, mrts-native, runtime, work-queues) |
| Missing registry outputs | 0 |
| Orphan generated reports | 0 |
| Skipped reports | 0 |
| Failed reports | 0 |

## Known Skipped Inputs

| Report | Status | Missing Inputs | Reason |
|---|---|---|---|
| `-` | none | - | no skipped reports |

## Git Evidence

| Command | Status | Return Code | Output Hash |
|---|---|---:|---|
| `git_status_short` | PASS | 0 | `771c4dec95969fab14a846b9d7b4d7a4cee44491d8168ef18cf837cc40e3d16f` |
| `git_head` | PASS | 0 | `8f2a7551123e5f2bf3a31f99f2a71a3b5108fc8a49810e20e43a289f50922266` |
| `git_branch` | PASS | 0 | `9b3162498c21d7f960877099174ecea13410bd21d12440b2ea8868117fc08ae0` |
| `git_submodule_status` | PASS | 0 | `6c1d462016aed1965bcbc99385794104338b56b2f064ac148092ed368adf551f` |
| `git_diff_stat` | PASS | 0 | `e5a0ba4c61a62755075cdfb9705d8f3e71477ead02c3fa82651883e6987c8202` |
| `framework_status_short` | PASS | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `framework_head` | PASS | 0 | `678c6c2458b79e5581ea4c9b734ac74c991cebfbf74c46b70fca8f9d115de491` |
| `framework_diff_stat` | PASS | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Proof Summary

The generated report layout was validated on the system above.
- `make refresh-connector-reports`: PASS
- `env ALLOW_IN_PROGRESS_SYSTEM_PROOF=1 make check-generated-report-layout`: PASS
- `make lint`: PASS
- `make quick-check`: PASS
- `git status --short`: PASS
- Flat generated root files: 0
- Categorized generated report files: 78

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `f87925b87ebaaa3c2511956c55b7f9dbb6f6269e295a8ce214d93811512eb6e6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `9398f825fbe26f5d562ba7cc7fc0e39d4cc3a59a9c35e5727d75e385d20fe9a4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `02c5ee904439f4d351d98c3664edd67b7b1212edd9a15fa04c3615d6db92c30e` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
