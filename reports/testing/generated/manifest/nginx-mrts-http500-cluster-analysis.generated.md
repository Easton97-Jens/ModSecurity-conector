> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:43:27Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-nginx-mrts-http500-cluster-analysis.py`
> Make target: `generate-nginx-mrts-http500-cluster-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# NGINX with-crs/with-mrts HTTP-500 Cluster Analysis

## Summary

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Job: `nginx:with-crs:with-mrts`
- Primary blocker: `none`
- HTTP-500 failures: `0`
- Likely cause: Historical evidence: NGINX worker could not traverse /root-owned runtime parents, generated docroot was inaccessible, and try_files /index.html looped into HTTP 500. New runs should block in the worker-docroot preflight before this becomes runtime mismatch evidence.
- Classification: `harness_environment_error`; secondary `nginx_config_error`
- Confidence: `high`

## Cluster Counts

| Group | Count | Classification | Representative Cases |
| --- | --- | --- | --- |
| Missing/Empty | - | - | - |

## Error Patterns

| Error Pattern | Count | Example | Affected Cases |
| --- | --- | --- | --- |
| Missing/Empty | - | - | - |

## Representative Cases

| Case | Expected | Actual | Access | Error Pattern | Classification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Missing/Empty | - | - | - | - | - | - |

## Root Cause Evidence

- 0 HTTP-500 rows have 'rewrite or internal redirection cycle while internally redirecting to "/index.html"'.
- 0 HTTP-500 rows have htdocs/index.html Permission denied in final-run error logs.
- Historical namei evidence shows /root is 0700 while NGINX worker user is nobody; generated files below it are otherwise readable.
- No segfault/core/module-load error pattern was observed in the final-run cluster.

## Minimal Repro

- Minimal case: `mrts_100000_mrts_002_args_a_get_100000_1`
- Existing producer reproducer: `VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=3600 make verified-full-matrix-job CONNECTOR=nginx CRS=with-crs MRTS=with-mrts`
- Target to add: `make verified-nginx-mrts-case CASE=mrts_100000_mrts_002_args_a_get_100000_1 CRS=with-crs MRTS=with-mrts`
- Notes: The connector harness supports TEST_CASE internally, but the verified full-matrix path does not yet expose a single-case target with CRS/MRTS setup and isolated job metadata.

## Fix Plan

| Fix | File/Path | Risk | Expected Effect | Needs New Verified Run |
| --- | --- | --- | --- | --- |
| Keep verified NGINX Full-Matrix harness roots under VERIFIED_RUN_ROOT/NGINX_HARNESS_PARENT outside /root. | ci/run-full-matrix-parallel.sh / Makefile NGINX_HARNESS_PARENT | medium | Eliminates docroot Permission denied or reports it as a BLOCKED preflight before the 500 cluster can form. | True |
| Add a readiness/permission preflight that blocks NGINX jobs when worker user cannot traverse DOCROOT parents. | connectors/nginx/harness/run_nginx_smoke.sh | low | Classifies future inaccessible-docroot evidence as BLOCKED instead of runtime FAIL. | True |
| Add a verified single-case Full-Matrix target for NGINX with CRS/MRTS setup and job metadata. | Makefile / ci/run-full-matrix-job.py | low | Provides minimal repro without rerunning the 524-case NGINX job. | False |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `79d08ce77343c7ae1e3443bf38fb44e5341b1fa0586ca5ed9cbd69b5de8271bd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `79114cad6b8c729beaae429b29d4caa467f5ce686a7cd78d7ba9d1dbd7a7c140` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `ebf9c0111b63f4ccb349e5c4ec1960702ec9e9c5ac53ab70153f60616341aa3d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `8d05493d1747a79de336faf3347245881ef226b7f9587038d945ff048c9b2a5a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `3f11d1fce15cdfa561cc96ef730cbd1b5604528e8f8a7fa8b2e7209629377e3b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6934388824f6a335f3ffb3e8282b0c0ec98d28b3e466b9bce7266e9db3b5fcd4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
