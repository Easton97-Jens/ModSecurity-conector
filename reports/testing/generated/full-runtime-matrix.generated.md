# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-09T15:47:40Z`
- Variant runs: **12**
- Total attempted: **2628**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **1072** / **1508** / **4** / **48**
- Pending metadata rows observed in runtime summaries: **1532**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | /src/ModSecurity-conector-full-matrix/no-crs/no-mrts/apache/results/apache-summary.json | /src/ModSecurity-conector-full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 95 | 39 | 0 | 6 | 0 | 351 | /src/ModSecurity-conector-full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /src/ModSecurity-conector-full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 104 | 23 | 0 | 6 | 0 | 303 | /src/ModSecurity-conector-full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /src/ModSecurity-conector-full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 1 | /src/ModSecurity-conector-full-matrix/no-crs/with-mrts/apache/results/apache-summary.json | /src/ModSecurity-conector-full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 405 | 112 | 0 | 6 | 383 | 1308 | /src/ModSecurity-conector-full-matrix-nginx-routing/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /src/ModSecurity-conector-full-matrix-nginx-routing/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 91 | 419 | 0 | 6 | 383 | 1081 | /src/ModSecurity-conector-full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /src/ModSecurity-conector-full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 1 | /src/ModSecurity-conector-full-matrix/with-crs/no-mrts/apache/results/apache-summary.json | /src/ModSecurity-conector-full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 96 | 39 | 0 | 6 | 0 | 403 | /src/ModSecurity-conector-full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /src/ModSecurity-conector-full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 105 | 23 | 0 | 6 | 0 | 330 | /src/ModSecurity-conector-full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /src/ModSecurity-conector-full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 1 | /src/ModSecurity-conector-full-matrix/with-crs/with-mrts/apache/results/apache-summary.json | /src/ModSecurity-conector-full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 86 | 432 | 0 | 6 | 383 | 1544 | /src/ModSecurity-conector-full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /src/ModSecurity-conector-full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 90 | 421 | 0 | 6 | 383 | 1205 | /src/ModSecurity-conector-full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /src/ModSecurity-conector-full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| nginx | no-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| haproxy | no-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| apache | with-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| nginx | with-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| haproxy | with-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |

## Guardrails
- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.
- MRTS golden outputs under the submodule are golden/reference/drift input only and are not runtime case roots.
- `no-mrts` variants should have zero MRTS runtime cases.
- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.
