> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:47:46Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-nginx-mrts-http500-cluster-analysis.py`
> Make target: `generate-nginx-mrts-http500-cluster-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
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
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `c75a893fd02c2e641831bfc8439251e77c63090b9f02d8d64072f6847bab29a9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `c72148b63be5e429c0f15840fad2f3f97aa3a633672acf9a6e8d28e2fcb8b031` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `b879807daa3ac77b4e2dd6254233ffeaa4f46bd0ec76163d98ff2cd2590b3412` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `7de51af87cf4175d9dba4efcb43ff5187319593fdcb7e4d25e49b97a1cb10adf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `bd7f3ba3382d7800e5de9bcf7eb1d28a26b0317b1a5aae2089b5f5812acddc78` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6bc04b7e3157faa5f7d32e333051db6fe568b604eef038f0706c32d1f2028cac` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `4a82546f163707fb800b44dcf86ecd7f1722f0e84428c1b41020d15f1d228dd2` | `2026-06-16T19-12-00Z-614c8049` | present |

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
