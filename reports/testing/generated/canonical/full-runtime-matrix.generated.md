> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:47:40Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-runtime-matrix.py`
> Make target: `generate-full-runtime-matrix`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-18T17:47:40Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **3141** / **775** / **0** / **12**
- Pending metadata rows observed in runtime summaries: **2298**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 119 | 13 | 0 | 1 | 0 | 338 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 112 | 27 | 0 | 1 | 0 | 552 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 119 | 13 | 0 | 1 | 0 | 271 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 407 | 108 | 0 | 1 | 383 | 1291 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 407 | 115 | 0 | 1 | 383 | 3208 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 407 | 108 | 0 | 1 | 383 | 1049 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 120 | 13 | 0 | 1 | 0 | 365 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 113 | 27 | 0 | 1 | 0 | 609 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 119 | 14 | 0 | 1 | 0 | 309 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 406 | 110 | 0 | 1 | 383 | 1380 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 406 | 117 | 0 | 1 | 383 | 3439 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 406 | 110 | 0 | 1 | 383 | 1182 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| nginx | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| apache | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| nginx | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |

## Guardrails
- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.
- MRTS golden outputs under the submodule are golden/reference/drift input only and are not runtime case roots.
- `no-mrts` variants should have zero MRTS runtime cases.
- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.

## MRTS Native Infrastructure Evidence
- Apache native: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `05187cad277e3352bbc54ba68260c25e3cad2001d726f43e765e00965ca324c4` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
