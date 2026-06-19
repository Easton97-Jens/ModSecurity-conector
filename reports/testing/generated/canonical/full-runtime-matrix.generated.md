> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:43:20Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-runtime-matrix.py`
> Make target: `generate-full-runtime-matrix`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-19T06:43:20Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **3154** / **774** / **0** / **0**
- Pending metadata rows observed in runtime summaries: **2298**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 121 | 12 | 0 | 0 | 0 | 336 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 114 | 26 | 0 | 0 | 0 | 551 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 121 | 12 | 0 | 0 | 0 | 266 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 407 | 109 | 0 | 0 | 383 | 1296 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 407 | 116 | 0 | 0 | 383 | 3212 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 407 | 109 | 0 | 0 | 383 | 1042 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 122 | 12 | 0 | 0 | 0 | 367 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 115 | 26 | 0 | 0 | 0 | 613 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 122 | 12 | 0 | 0 | 0 | 301 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 406 | 111 | 0 | 0 | 383 | 1388 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 406 | 118 | 0 | 0 | 383 | 3437 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 406 | 111 | 0 | 0 | 383 | 1183 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log |

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
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `fada5d0fadca101488838264f9845932d6c5c1e889a73f7e728d5047efed2011` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
