> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:56:27Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-runtime-matrix.py`
> Make target: `generate-full-runtime-matrix`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-16T05:56:27Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **2206** / **1650** / **0** / **72**
- Pending metadata rows observed in runtime summaries: **2298**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 108 | 19 | 0 | 6 | 0 | 344 | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 74 | 60 | 0 | 6 | 0 | 524 | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 108 | 19 | 0 | 6 | 0 | 329 | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 406 | 104 | 0 | 6 | 383 | 1372 | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 0 | 517 | 0 | 6 | 383 | 3141 | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 406 | 104 | 0 | 6 | 383 | 1209 | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 109 | 19 | 0 | 6 | 0 | 398 | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 76 | 59 | 0 | 6 | 0 | 597 | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 109 | 19 | 0 | 6 | 0 | 383 | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 405 | 106 | 0 | 6 | 383 | 1521 | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 0 | 518 | 0 | 6 | 383 | 3273 | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 405 | 106 | 0 | 6 | 383 | 1347 | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| nginx | no-crs/with-mrts | 383 | 0 | 383 | 0 | 0 | 383 |
| haproxy | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| apache | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| nginx | with-crs/with-mrts | 383 | 0 | 383 | 0 | 0 | 383 |
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
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | `f9634d21e3486bd05843bab0d423dd871d48edcfe6a2ec7a46cd5c694f3b54bb` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
