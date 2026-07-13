> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:54:49Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-verified-report-run.py`
> Make target: `verified-report-run`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `complete`

# Verified Run Manifest

**Language:** English | [Deutsch](verified-run-manifest.generated.de.md)

## Summary

| Field | Value |
|---|---|
| Verified run id | `2026-06-16T19-12-00Z-614c8049` |
| Data source policy | `verified-inputs-only` |
| Profile | `full` |
| Start time UTC | `2026-06-16T19:12:00Z` |
| End time UTC | `2026-06-18T16:54:49Z` |
| Duration seconds | `164569.0` |
| Input status | `complete` |

## Runtime Environment

| Field | Value |
|---|---|
| Connector SHA | `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5` |
| Framework SHA | `2334d31b942fd79770c7381b02fcaf031cccc4d2` |
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
| `VERIFIED_RUN_ROOT` | `<verified-run-root>` | PASS | ok |
| `VERIFIED_BUILD_ROOT` | `<verified-run-root>/build` | PASS | ok |
| `VERIFIED_SOURCE_ROOT` | `<verified-run-root>/src` | PASS | ok |
| `VERIFIED_TMP_ROOT` | `<verified-run-root>/tmp` | PASS | ok |
| `VERIFIED_LOG_ROOT` | `<verified-run-root>/logs` | PASS | ok |
| `VERIFIED_COMPONENT_CACHE` | `<verified-run-root>/component-cache` | PASS | ok |
| `NGINX_HARNESS_PARENT` | `<verified-run-root>/nginx-harness` | PASS | ok |
| `BUILD_ROOT` | `<verified-run-root>/build` | PASS | ok |
| `SOURCE_ROOT` | `<verified-run-root>/src` | PASS | ok |
| `TMP_ROOT` | `<verified-run-root>/tmp` | PASS | ok |
| `LOG_ROOT` | `<verified-run-root>/logs` | PASS | ok |
| `CONNECTOR_COMPONENT_CACHE` | `<verified-run-root>/component-cache` | PASS | ok |

## Worker Accessibility / Preflight

| Check | Status | Path | Notes |
|---|---|---|---|
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | outside <local-home-root> |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | current process can traverse; per-case worker checks are recorded in nginx-worker-preflight.jsonl |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_double_encoded_uri_runtime_difference/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_double_encoded_uri_runtime_difference/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_double_encoded_uri_runtime_difference/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_double_encoded_uri_runtime_difference/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_whitespace_normalization_gap/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_whitespace_normalization_gap/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_whitespace_normalization_gap/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/unicode_whitespace_normalization_gap/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_request_body_malformed_connector_gap/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_request_body_malformed_connector_gap/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_request_body_malformed_connector_gap/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_request_body_malformed_connector_gap/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_namespace_edge_connector_gap/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_namespace_edge_connector_gap/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_namespace_edge_connector_gap/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/build/verified-nginx-case/no-crs-no-mrts-nginx/runtime/xml_namespace_edge_connector_gap/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100156_mrts_110_xml_100156_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100155_mrts_110_xml_100155_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |
| DOCROOT/index.html exists | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs/index.html` | materialized before NGINX start |
| Harness parent traversable | PASS | `<verified-run-root>/nginx-harness` | checked with runuser -u nobody |
| NGINX worker can traverse docroot | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs` | checked with runuser -u nobody |
| htdocs/index.html readable by worker | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs/index.html` | checked with runuser -u nobody |
| try_files fallback guarded | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/mrts_100154_mrts_110_xml_100154_1/htdocs/index.html` | docroot readability is checked before try_files /index.html can loop |
| Path under <local-home-root> | PASS | `<verified-run-root>/nginx-harness` | NGINX_HARNESS_PARENT is outside <local-home-root> |
| Work root under <local-home-root> | PASS | `<verified-run-root>/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000` | NGINX_HARNESS_WORK_ROOT is outside <local-home-root> |

## Runtime Producer Readiness

- Status: `PASS`
- Runtime env loaded: `True`
- Runtime env path: `<verified-run-root>/component-cache/runtime-env.sh`

| Component | Required | Status | Path | Fix |
|---|---|---|---|---|
| common.sh | True | present | `<local-home-root>/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/common.sh` | `ensure FRAMEWORK_ROOT points at modules/ModSecurity-test-Framework` |
| NGINX binary | True | present | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` | `run make prepare-runtime-components` |
| NGINX ModSecurity module | True | present | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` | `run make prepare-runtime-components` |
| NGINX libmodsecurity | True | present | `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/libmodsecurity.so.3.0.15` | `run make prepare-runtime-components` |
| Apache/httpd | True | present | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/httpd` | `run make prepare-runtime-components` |
| Apache/APXS | True | present | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apxs` | `run make prepare-runtime-components` |
| Apache ModSecurity module | True | present | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so` | `run make prepare-runtime-components` |
| HAProxy binary | True | present | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-runtime/haproxy/sbin/haproxy` | `run make prepare-runtime-components` |
| HAProxy SPOA runtime | True | present | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `run make prepare-runtime-components` |
| HAProxy binding metadata | True | present | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-modsecurity-binding/paths.env` | `run make prepare-runtime-components` |
| go-ftw | False | present | `<verified-run-root>/component-cache/bin/go-ftw` | `optional native MRTS: install or cache go-ftw` |
| albedo | False | present | `<verified-run-root>/component-cache/bin/albedo` | `optional native MRTS: install or cache albedo` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules` |
| ModSecurity module path | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `true` |
| How to prepare | `make prepare-runtime-components` |

## Runtime Network / Cache Readiness

| Source | Status | Path | Notes |
|---|---|---|---|
| nginx latest release | present | `<verified-run-root>/component-cache/archives/nginx/nginx-latest-release.json` | local cache available |
| nginx archive cache | present | `<verified-run-root>/component-cache/archives/nginx` | local cache available |
| go-ftw git cache | present | `<verified-run-root>/component-cache/git/go-ftw` | local cache available |
| albedo git cache | present | `<verified-run-root>/component-cache/git/albedo` | local cache available |

## Producer Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `git submodule update --init --recursive` | PASS | 0 | 0.116 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/01-git-submodule-update---init---recursive.log` |
| `make prepare-runtime-components` | PASS | 0 | 47.168 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/02-make-prepare-runtime-components.log` |
| `make check-runtime-producer-readiness` | PASS | 0 | 0.266 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/03-make-check-runtime-producer-readiness.log` |
| `make runtime-matrix-all-runtime` | FAIL | 2 | 34.838 | runtime_completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/04-make-runtime-matrix-all-runtime.log` |
| `make full-matrix-parallel-runtime` | BLOCKED_TIMEOUT | -15 | 7200.004 | runtime_completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/05-make-full-matrix-parallel-runtime.log` |
| `make mrts-native-full-run-runtime` | FAILED_OPTIONAL | 2 | 50.088 | runtime_completed | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/06-make-mrts-native-full-run-runtime.log` |
| `make generate-verified-runtime-mismatch-analysis` | PASS | 0 | 1.721 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/07-make-generate-verified-runtime-mismatch-analysis.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 3600.006 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/08-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 662.744 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/19-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 1593.675 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/21-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 687.44 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/23-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 1707.546 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/25-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 877.15 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/27-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 3523.191 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/29-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 934.575 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/31-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 3660.01 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/33-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 617.9 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/35-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 1412.258 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/37-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 650.082 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/39-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 1510.347 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/41-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 35.044 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/46-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 16.276 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/48-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 32.533 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/50-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 16.126 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/52-make-full-matrix-single-job-runtime-CONNECTOR-apache-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 32.131 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/54-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 16.476 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/56-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 32.177 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/58-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 15.669 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/60-make-full-matrix-single-job-runtime-CONNECTOR-nginx-CRS-with-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 31.275 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/62-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-no-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 16.226 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/64-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-no-crs-MRTS-with-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 31.428 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/66-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-with-crs-MRTS-no-mrts.log` |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 15.921 | completed_with_mismatches | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/68-make-full-matrix-single-job-runtime-CONNECTOR-haproxy-CRS-with-crs-MRTS-with-mrts.log` |

## Consumer / Refresh Commands

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `make refresh-all-reports` | FAIL | 2 | 33.131 | - | consumer_stale | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/43-make-refresh-all-reports.log` |
| `make generate-system-environment-proof` | FAIL | 2 | 55.57 | - | refresh_failed | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/44-make-generate-system-environment-proof.log` |
| `make refresh-all-reports` | FAIL | 2 | 52.236 | - | consumer_stale | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/45-make-refresh-all-reports.log` |
| `make refresh-all-reports` | FAIL | 2 | 34.639 | - | consumer_stale | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/70-make-refresh-all-reports.log` |
| `make generate-system-environment-proof` | FAIL | 2 | 56.313 | - | refresh_failed | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/71-make-generate-system-environment-proof.log` |
| `make refresh-all-reports` | FAIL | 2 | 54.449 | - | consumer_stale | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/72-make-refresh-all-reports.log` |

## Checks

| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |
|---|---:|---:|---:|---|---|---|
| `make check-generated-report-layout` | FAIL | 2 | 1.42 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/10-make-check-generated-report-layout.log` |
| `make lint` | PASS | 0 | 5.737 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/11-make-lint.log` |
| `make quick-check` | PASS | 0 | 6.99 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/12-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 1.421 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/13-make-check-generated-report-layout.log` |
| `make lint` | PASS | 0 | 5.535 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/14-make-lint.log` |
| `make quick-check` | PASS | 0 | 6.99 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/15-make-quick-check.log` |
| `make check-generated-report-layout` | FAIL | 2 | 1.319 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/16-make-check-generated-report-layout.log` |
| `make lint` | PASS | 0 | 5.835 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/17-make-lint.log` |
| `make quick-check` | PASS | 0 | 7.089 | - | - | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/logs/18-make-quick-check.log` |

## Full-Matrix Job Completeness

| Field | Value |
|---|---|
| Completeness | `12/12` |
| Overall status | `complete` |
| Missing jobs | `-` |
| Timeout jobs | `-` |

| Slowest Job | Duration Seconds | Status |
|---|---:|---|
| `nginx:with-crs:with-mrts` | 3439 | completed_with_mismatches |
| `nginx:no-crs:with-mrts` | 3208 | completed_with_mismatches |
| `apache:with-crs:with-mrts` | 1380 | completed_with_mismatches |
| `apache:no-crs:with-mrts` | 1291 | completed_with_mismatches |
| `haproxy:with-crs:with-mrts` | 1182 | completed_with_mismatches |

## Runtime Mismatch Summary

| Field | Value |
|---|---|
| Total mismatches | `787` |
| Critical mismatches | `107` |
| Top connector | `nginx` |
| Primary blocker | `completed_with_mismatches` |
| Merge readiness | `FAIL` |

## Blocked / Stale Inputs

| Item | Status | Reason | Affected Reports |
|---|---|---|---|
| `-` | zero_result_verified | No missing, skipped, blocked, stale, or failed reports were recorded. | - |

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
| connector | `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5` | `master` | `dirty` |
| framework | `2334d31b942fd79770c7381b02fcaf031cccc4d2` | `master` | `dirty` |
| MRTS | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | `dirty` |

## Proof Summary

| Claim | Status | Evidence |
|---|---|---|
| Runtime paths outside <local-home-root> by default | `PASS` | `VERIFIED_RUN_ROOT=<verified-run-root>` |
| NGINX docroot preflight evidence | `PASS` | `nginx-worker-preflight.jsonl` rows are included when NGINX smoke ran |
| Verified inputs only | `PASS` | `verified-inputs-only` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `79c41b77eaeb9504b58875610f780a24766a2518aa7880ff2f30b3edd0e4e9b8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/system-environment-proof.generated.json` | `d5da2d21e504d694c42b0f1cf4ad44b85e0b452f266c68fa20ae2109c493ad7d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `3e2797d4f1af140de1e2f073f6a1de13f2cc9a58191207a7a53a0c34d377b556` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/system-environment-proof.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
