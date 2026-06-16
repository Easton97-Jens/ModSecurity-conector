> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:55:36Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-verified-report-run.py`
> Make target: `verified-report-run`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `blocked`

# Verified Run Manifest

## Summary

| Field | Value |
|---|---|
| Verified run id | `2026-06-16T16-57-44Z-b53340a8` |
| Data source policy | `verified-inputs-only` |
| Profile | `full` |
| Start time UTC | `2026-06-16T16:57:44Z` |
| End time UTC | `2026-06-16T18:55:36Z` |
| Duration seconds | `7072.0` |
| Input status | `blocked` |

## Runtime Environment

| Field | Value |
|---|---|
| Connector SHA | `b53340a84f9acd5fbc3aff3de136c92ac122c3fa` |
| Framework SHA | `2b2e402708fca5ff40664926ff01c2c5e520a48a` |
| MRTS SHA | `13aa91291adea12d5c607fdd165d010fcfb1da78` |
| Connector branch | `master` |
| Framework branch | `master` |
| Dirty status | `dirty` / `dirty` |
| Runtime matrix timeout seconds | `1800` |
| Full matrix runtime timeout seconds | `7200` |
| Report refresh timeout seconds | `1800` |
| Native MRTS timeout seconds | `1800` |

## Runtime Paths

| Variable | Value | Status | Notes |
|---|---|---|---|
| `VERIFIED_RUN_ROOT` | `/var/tmp/ModSecurity-conector-verified` | PASS | ok |
| `VERIFIED_BUILD_ROOT` | `/var/tmp/ModSecurity-conector-verified/build` | PASS | ok |
| `VERIFIED_SOURCE_ROOT` | `/var/tmp/ModSecurity-conector-verified/src` | PASS | ok |
| `VERIFIED_TMP_ROOT` | `/var/tmp/ModSecurity-conector-verified/tmp` | PASS | ok |
| `VERIFIED_LOG_ROOT` | `/var/tmp/ModSecurity-conector-verified/logs` | PASS | ok |
| `VERIFIED_COMPONENT_CACHE` | `/var/tmp/ModSecurity-conector-verified/component-cache` | PASS | ok |
| `NGINX_HARNESS_PARENT` | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | PASS | ok |
| `BUILD_ROOT` | `/var/tmp/ModSecurity-conector-verified/build` | PASS | ok |
| `SOURCE_ROOT` | `/var/tmp/ModSecurity-conector-verified/src` | PASS | ok |
| `TMP_ROOT` | `/var/tmp/ModSecurity-conector-verified/tmp` | PASS | ok |
| `LOG_ROOT` | `/var/tmp/ModSecurity-conector-verified/logs` | PASS | ok |
| `CONNECTOR_COMPONENT_CACHE` | `/var/tmp/ModSecurity-conector-verified/component-cache` | PASS | ok |

## Worker Accessibility / Preflight

| Check | Status | Path | Notes |
|---|---|---|---|
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | outside /root |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | current process can traverse; per-case worker checks are recorded in nginx-worker-preflight.jsonl |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_4/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_4/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_4/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_4/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_3/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_3/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_3/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_3/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_2/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_2/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_2/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_2/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100153_mrts_069_response_body_100153_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |
| DOCROOT/index.html exists | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100152_mrts_069_response_body_100152_4/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100152_mrts_069_response_body_100152_4/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100152_mrts_069_response_body_100152_4/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100152_mrts_069_response_body_100152_4/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness` | NGINX_HARNESS_PARENT is outside /root |
| Work root under /root | PASS | `/var/tmp/ModSecurity-conector-verified/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside /root |

## Runtime Producer Readiness

- Status: `PASS`
- Runtime env loaded: `True`
- Runtime env path: `/var/tmp/ModSecurity-conector-verified/component-cache/runtime-env.sh`

| Component | Required | Status | Path | Fix |
|---|---|---|---|---|
| common.sh | True | present | `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/common.sh` | `ensure FRAMEWORK_ROOT points at modules/ModSecurity-test-Framework` |
| NGINX binary | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/c50bf9f846cc261b1ccf6bda433c9469632d6ab12f66d2b8a67e6f16644a6fa3/nginx/sbin/nginx` | `run make prepare-runtime-components` |
| NGINX ModSecurity module | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/c50bf9f846cc261b1ccf6bda433c9469632d6ab12f66d2b8a67e6f16644a6fa3/nginx/modules/ngx_http_modsecurity_module.so` | `run make prepare-runtime-components` |
| NGINX libmodsecurity | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/f6a9f464f349d369e27dc9fa8f17ef6f9ba2f1189ed6a9c33020e93c412e8b03/lib/libmodsecurity.so.3.0.15` | `run make prepare-runtime-components` |
| Apache/httpd | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/httpd` | `run make prepare-runtime-components` |
| Apache/APXS | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/apxs` | `run make prepare-runtime-components` |
| Apache ModSecurity module | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/build/output/apache/mod_security3.so` | `run make prepare-runtime-components` |
| HAProxy binary | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/a9829d8bd25aef3c282e8d666f98666dfaab4e91dfed7a193302e72a4818f095/haproxy-runtime/haproxy/sbin/haproxy` | `run make prepare-runtime-components` |
| HAProxy SPOA runtime | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/a9829d8bd25aef3c282e8d666f98666dfaab4e91dfed7a193302e72a4818f095/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `run make prepare-runtime-components` |
| HAProxy binding metadata | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/a9829d8bd25aef3c282e8d666f98666dfaab4e91dfed7a193302e72a4818f095/haproxy-modsecurity-binding/paths.env` | `run make prepare-runtime-components` |
| go-ftw | False | present | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/go-ftw` | `optional native MRTS: install or cache go-ftw` |
| albedo | False | present | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/albedo` | `optional native MRTS: install or cache albedo` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/c50bf9f846cc261b1ccf6bda433c9469632d6ab12f66d2b8a67e6f16644a6fa3/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/c50bf9f846cc261b1ccf6bda433c9469632d6ab12f66d2b8a67e6f16644a6fa3/nginx/modules` |
| ModSecurity module path | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/c50bf9f846cc261b1ccf6bda433c9469632d6ab12f66d2b8a67e6f16644a6fa3/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `true` |
| How to prepare | `make prepare-runtime-components` |

## Runtime Network / Cache Readiness

| Source | Status | Path | Notes |
|---|---|---|---|
| nginx latest release | present | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx/nginx-latest-release.json` | local cache available |
| nginx archive cache | present | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx` | local cache available |
| go-ftw git cache | present | `/var/tmp/ModSecurity-conector-verified/component-cache/git/go-ftw` | local cache available |
| albedo git cache | present | `/var/tmp/ModSecurity-conector-verified/component-cache/git/albedo` | local cache available |

## Producer Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `git submodule update --init --recursive` | PASS | 0 | 0.116 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/01-git-submodule-update---init---recursive.log` |
| `make prepare-runtime-components` | PASS | 0 | 532.147 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/02-make-prepare-runtime-components.log` |
| `make check-runtime-producer-readiness` | PASS | 0 | 0.266 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/03-make-check-runtime-producer-readiness.log` |
| `make runtime-matrix-all-runtime` | FAIL | 2 | 34.84 | runtime_completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/04-make-runtime-matrix-all-runtime.log` |
| `make full-matrix-parallel-runtime` | FAIL | 2 | 6445.7 | runtime_completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/05-make-full-matrix-parallel-runtime.log` |
| `make mrts-native-full-run-runtime` | FAILED_OPTIONAL | 2 | 50.75 | runtime_completed | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/06-make-mrts-native-full-run-runtime.log` |
| `make generate-verified-runtime-mismatch-analysis` | PASS | 0 | 1.922 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/logs/07-make-generate-verified-runtime-mismatch-analysis.log` |

## Consumer / Refresh Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `-` | not_run | - | - | - | - | `-` |

## Checks

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `-` | not_run | - | - | - | - | `-` |

## Full-Matrix Job Completeness

| Field | Value |
|---|---|
| Completeness | `0/0` |
| Overall status | `unknown` |
| Missing jobs | `-` |
| Timeout jobs | `-` |

| Slowest Job | Duration Seconds | Status |
|---|---:|---|
| `-` | - | unknown |

## Runtime Mismatch Summary

| Field | Value |
|---|---|
| Total mismatches | `586` |
| Critical mismatches | `524` |
| Top connector | `nginx` |
| Primary blocker | `command_failed` |
| Merge readiness | `FAIL` |

## Blocked / Stale Inputs

| Item | Status | Reason | Affected Reports |
|---|---|---|---|
| `BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl` | missing | input file missing | - |
| `BUILD_ROOT:mrts-native/apache2_ubuntu/job.json` | missing | input file missing | - |
| `BUILD_ROOT:mrts-native/nginx-pr24/job.json` | missing | input file missing | - |
| `full_runtime_matrix` | skipped_missing_input | required input missing or empty | reports/testing/generated/canonical/full-runtime-matrix.generated.json, reports/testing/generated/canonical/full-runtime-matrix.generated.md |
| `full_matrix_job_completeness` | skipped_missing_input | required input missing or empty | reports/testing/generated/manifest/full-matrix-job-completeness.generated.json, reports/testing/generated/manifest/full-matrix-job-completeness.generated.md |
| `verified_runtime_mismatch_analysis` | skipped_missing_input | required input missing or empty | reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json, reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md |
| `native_mrts_reports` | skipped_missing_input | required input missing or empty | reports/testing/generated/mrts-native/mrts-native-full.generated.json, reports/testing/generated/mrts-native/mrts-native-full.generated.md, reports/testing/generated/mrts-native/mrts-native-apache.generated.json, reports/testing/generated/mrts-native/mrts-native-apache.generated.md, reports/testing/generated/mrts-native/mrts-native-nginx.generated.json, reports/testing/generated/mrts-native/mrts-native-nginx.generated.md, reports/testing/generated/mrts-native/mrts-native-summary.generated.json, reports/testing/generated/mrts-native/mrts-native-summary.generated.md |
| `nginx_mrts_http500_cluster_analysis` | blocked | required generated input is blocked | reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json, reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md |
| `connector_work_queue` | blocked | required generated input is blocked | reports/testing/generated/work-queues/connector-work-queue.generated.json, reports/testing/generated/work-queues/connector-work-queue.generated.md |
| `phase_work_queue` | blocked | required generated input is blocked | reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `nolog_audit_evidence` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json, reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `response_header_hook_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json, reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `phase4_hard_abort_capability` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json, reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `remaining_failure_analysis` | blocked | required generated input is blocked | reports/testing/generated/canonical/remaining-failure-analysis.generated.json, reports/testing/generated/canonical/remaining-failure-analysis.generated.md, reports/testing/generated/canonical/next-fix-plan.generated.json, reports/testing/generated/canonical/next-fix-plan.generated.md, reports/testing/generated/canonical/full-run-evidence.generated.json, reports/testing/generated/canonical/full-run-evidence.generated.md |
| `intervention_blocking_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json, reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md |
| `no_mrts_intervention_nomatch_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json, reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md |
| `body_processor_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/body-processor-analysis.generated.json, reports/testing/generated/focused-analysis/body-processor-analysis.generated.md |
| `rule_chain_semantics_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json, reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md |
| `final_consistency_audit` | blocked | required generated input is blocked | reports/testing/generated/canonical/final-consistency-audit.generated.json, reports/testing/generated/canonical/final-consistency-audit.generated.md |

## Tool Versions

| Tool | Status | Version / Output |
|---|---|---|
| git | present | `git version 2.53.0` |
| python3 | present | `Python 3.14.4` |
| python | present | `Python 3.14.4` |
| make | present | `GNU Make 4.4.1` |
| bash | present | `GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)` |
| sh | present | `POSIX shell available (/usr/bin/dash)` |
| gcc | present | `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0` |
| clang | present | `Ubuntu clang version 21.1.8 (6ubuntu1)` |
| go | present | `go version go1.26.0 linux/amd64` |
| go-ftw | missing | `command not found` |
| albedo | missing | `command not found` |
| actionlint | missing | `command not found` |
| jq | present | `jq-1.8.1` |
| curl | present | `curl 8.18.0 (x86_64-pc-linux-gnu) libcurl/8.18.0 OpenSSL/3.5.5 zlib/1.3.1 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.68.0 librtmp/2.3 mit-krb5/1.22.1 OpenLDAP/2.6.10` |
| docker | missing | `command not found` |
| apachectl | missing | `no candidate found: apachectl` |
| apache/httpd | missing | `no candidate found: apache2 httpd apachectl` |
| nginx | missing | `no candidate found: nginx` |
| haproxy | configured_missing | `file not found` |
| apxs | missing | `no candidate found: apxs apxs2` |

## Git Evidence

| Repository | SHA | Branch | Dirty Status |
|---|---|---|---|
| connector | `b53340a84f9acd5fbc3aff3de136c92ac122c3fa` | `master` | `dirty` |
| framework | `2b2e402708fca5ff40664926ff01c2c5e520a48a` | `master` | `dirty` |
| MRTS | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | `dirty` |

## Proof Summary

| Claim | Status | Evidence |
|---|---|---|
| Runtime paths outside /root by default | `PASS` | `VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified` |
| NGINX docroot preflight evidence | `PASS` | `nginx-worker-preflight.jsonl` rows are included when NGINX smoke ran |
| Verified inputs only | `PASS` | `verified-inputs-only` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | `f7092c24374de4f6bf26ea230ed84429b8dfc9cded204a709c9619599d6dd73f` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `3653b0789501f9a2e9acecdf0b74f79e0c972db7912ab56a50ff79518ecdfd72` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/manifest/system-environment-proof.generated.json` | `65a50da14797d7d7bbedf2c59f91cc102f8632791047b225bcaf65d13a26937a` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `634a8e566d3ab11543130482bcc4df7f451771ec0cfec68736a4d8a12ae1065a` | `2026-06-15T21-01-39Z-9391a8d0` | stale |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | stale | generated report input is stale: verified_run_id differs |
| `reports/testing/generated/manifest/system-environment-proof.generated.json` | stale | generated report input is stale: verified_run_id differs |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | stale | generated report input is stale: verified_run_id differs |
