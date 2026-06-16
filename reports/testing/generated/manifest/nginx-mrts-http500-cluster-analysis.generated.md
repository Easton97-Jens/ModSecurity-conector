> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:20Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-nginx-mrts-http500-cluster-analysis.py`
> Make target: `generate-nginx-mrts-http500-cluster-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> Input status: `complete`

# NGINX with-crs/with-mrts HTTP-500 Cluster Analysis

## Summary

- Verified run id: `2026-06-16T16-57-44Z-b53340a8`
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
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `9206a9635a2c539ee6be6364bd72e0f7f5c1cd59f44944053805207de483bacd` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `cc3624e2c87d64ddbae32d7b431ba38ef7632a43f9d3e18ded5992da510e761e` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `ebb0b75de09d92c6e4f6dabb733867c64bbc7054422a7392ceb9bbcc0697f3da` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `40299cbd2d9894d945ba652a65729e2233a20ef72b4ed71cf6f532cbec705df8` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `b3ac7d2737b2859e60b8a624cd1e5500fffda8052a874d3c47dafdd35d47d07a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `5a46b78e9b0b07805bfa70305a7f2fb7f907511087e8952d7ee18b91f6e9f5bb` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | `f7092c24374de4f6bf26ea230ed84429b8dfc9cded204a709c9619599d6dd73f` | `2026-06-16T16-57-44Z-b53340a8` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | present | input file available |
