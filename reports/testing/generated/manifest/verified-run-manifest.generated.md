> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:48:19Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-verified-report-run.py`
> Make target: `verified-report-run`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `blocked`

# Verified Run Manifest

## Summary

| Field | Value |
|---|---|
| Verified run id | `2026-06-16T19-12-00Z-614c8049` |
| Data source policy | `verified-inputs-only` |
| Profile | `full` |
| Start time UTC | `2026-06-16T19:12:00Z` |
| End time UTC | `2026-06-17T15:48:19Z` |
| Duration seconds | `74179.0` |
| Input status | `blocked` |

## Runtime Environment

| Field | Value |
|---|---|
| Connector SHA | `dd6e0455c4838949ce86cff81ce89dccd4e524f8` |
| Framework SHA | `ee23a10d5224401d9e63f28ad374969ac129e5f0` |
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
| NGINX binary | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` | `run make prepare-runtime-components` |
| NGINX ModSecurity module | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` | `run make prepare-runtime-components` |
| NGINX libmodsecurity | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/libmodsecurity.so.3.0.15` | `run make prepare-runtime-components` |
| Apache/httpd | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/httpd` | `run make prepare-runtime-components` |
| Apache/APXS | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apxs` | `run make prepare-runtime-components` |
| Apache ModSecurity module | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so` | `run make prepare-runtime-components` |
| HAProxy binary | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-runtime/haproxy/sbin/haproxy` | `run make prepare-runtime-components` |
| HAProxy SPOA runtime | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `run make prepare-runtime-components` |
| HAProxy binding metadata | True | present | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-modsecurity-binding/paths.env` | `run make prepare-runtime-components` |
| go-ftw | False | present | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/go-ftw` | `optional native MRTS: install or cache go-ftw` |
| albedo | False | present | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/albedo` | `optional native MRTS: install or cache albedo` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules` |
| ModSecurity module path | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` |
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
| `git submodule update --init --recursive` | PASS | 0 | 0.116 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/01-git-submodule-update---init---recursive.log` |
| `make prepare-runtime-components` | PASS | 0 | 47.168 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/02-make-prepare-runtime-components.log` |
| `make check-runtime-producer-readiness` | PASS | 0 | 0.266 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/03-make-check-runtime-producer-readiness.log` |
| `make runtime-matrix-all-runtime` | FAIL | 2 | 34.838 | runtime_completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/04-make-runtime-matrix-all-runtime.log` |
| `make full-matrix-parallel-runtime` | BLOCKED_TIMEOUT | -15 | 7200.004 | runtime_completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/05-make-full-matrix-parallel-runtime.log` |
| `make mrts-native-full-run-runtime` | FAILED_OPTIONAL | 2 | 50.088 | runtime_completed | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/06-make-mrts-native-full-run-runtime.log` |
| `make generate-verified-runtime-mismatch-analysis` | PASS | 0 | 1.721 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/07-make-generate-verified-runtime-mismatch-analysis.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 3600.006 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/08-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 662.744 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/19-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 1593.675 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/21-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 687.44 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/23-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 1707.546 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/25-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 877.15 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/27-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 3523.191 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/29-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 934.575 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/31-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 3660.01 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/33-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 617.9 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/35-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 1412.258 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/37-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 650.082 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/39-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 1510.347 | completed_with_mismatches | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/41-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-with-crs-MRTS-with-mrts.log` |

## Consumer / Refresh Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `make refresh-all-reports` | FAIL | 2 | 33.131 | - | consumer_stale | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/43-make-refresh-all-reports.log` |
| `make generate-system-environment-proof` | FAIL | 2 | 55.57 | - | refresh_failed | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/44-make-generate-system-environment-proof.log` |
| `make refresh-all-reports` | FAIL | 2 | 52.236 | - | consumer_stale | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/45-make-refresh-all-reports.log` |

## Checks

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `make check-generated-report-layout` | FAIL | 2 | 1.42 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/10-make-check-generated-report-layout.log` |
| `make lint` | PASS | 0 | 5.737 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/11-make-lint.log` |
| `make quick-check` | PASS | 0 | 6.99 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/12-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 1.421 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/13-make-check-generated-report-layout.log` |
| `make lint` | PASS | 0 | 5.535 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/14-make-lint.log` |
| `make quick-check` | PASS | 0 | 6.99 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/15-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 1.319 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/16-make-check-generated-report-layout.log` |
| `make lint` | PASS | 0 | 5.835 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/17-make-lint.log` |
| `make quick-check` | PASS | 0 | 7.089 | - | - | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/18-make-quick-check.log` |

## Full-Matrix Job Completeness

| Field | Value |
|---|---|
| Completeness | `12/12` |
| Overall status | `complete` |
| Missing jobs | `-` |
| Timeout jobs | `-` |

| Slowest Job | Duration Seconds | Status |
|---|---:|---|
| `nginx:with-crs:with-mrts` | 3419 | completed_with_mismatches |
| `nginx:no-crs:with-mrts` | 3200 | completed_with_mismatches |
| `apache:with-crs:with-mrts` | 1383 | completed_with_mismatches |
| `apache:no-crs:with-mrts` | 1270 | completed_with_mismatches |
| `haproxy:with-crs:with-mrts` | 1185 | completed_with_mismatches |

## Runtime Mismatch Summary

| Field | Value |
|---|---|
| Total mismatches | `836` |
| Critical mismatches | `264` |
| Top connector | `nginx` |
| Primary blocker | `completed_with_mismatches` |
| Merge readiness | `FAIL` |

## Blocked / Stale Inputs

| Item | Status | Reason | Affected Reports |
|---|---|---|---|
| `native_mrts_reports` | skipped_stale_input | required generated input is stale | reports/testing/generated/mrts-native/mrts-native-full.generated.json, reports/testing/generated/mrts-native/mrts-native-full.generated.md, reports/testing/generated/mrts-native/mrts-native-apache.generated.json, reports/testing/generated/mrts-native/mrts-native-apache.generated.md, reports/testing/generated/mrts-native/mrts-native-nginx.generated.json, reports/testing/generated/mrts-native/mrts-native-nginx.generated.md, reports/testing/generated/mrts-native/mrts-native-summary.generated.json, reports/testing/generated/mrts-native/mrts-native-summary.generated.md |
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
| connector | `dd6e0455c4838949ce86cff81ce89dccd4e524f8` | `master` | `dirty` |
| framework | `ee23a10d5224401d9e63f28ad374969ac129e5f0` | `master` | `dirty` |
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
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `7be7707b48f88a7b2a19c0b5c1209d40aec5396ed773e4b79d4ceec00fc3b23e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `0bb9214483188e3b133bf05175593346bc03e690b5a1b9c3b2bf0a2b0cff9999` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/system-environment-proof.generated.json` | `e0b0211225f5cb7aad9cb724a7819810b0c43de8fa0c5ca436f407267d8d1b24` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `4bcd8974231779d1a792c923d74e43a534a689110fda69bf619eede9a5098508` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/system-environment-proof.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
