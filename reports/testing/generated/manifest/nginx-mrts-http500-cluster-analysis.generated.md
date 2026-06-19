> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:51:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-nginx-mrts-http500-cluster-analysis.py`
> Make target: `generate-nginx-mrts-http500-cluster-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
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
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `31606405e016d20afb67ce650aaf098b8194133d87869846344929e74c70b8f9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `d1425a9d5db6ec05270dd7292078437ab1ffd4981efdaadc8b1bf9da902e621f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `efc447466ad8121a9316477b087e74a7155148082320a9cd57805aa3327f675e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `59dd481e19225c369952c566eca3981cb002c7050b699ee45be6dfdbef2d2603` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `9a7d2f6a8c313d7fb88071c69847f3cbb2aaf8eb90466cc56056c2199d8c44b7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `a8909f651e4e60be0c10c6cb24a1c11f98b9e99845a47a31c42aa64a727c0e65` | `2026-06-16T19-12-00Z-614c8049` | present |
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
