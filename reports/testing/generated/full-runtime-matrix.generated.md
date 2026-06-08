# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-08T14:37:02Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **1320** / **2536** / **0** / **72**
- Pending metadata rows observed in runtime summaries: **2298**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 100 | 27 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/full-matrix/no-crs/no-mrts/apache/apache-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/no-crs/no-mrts/apache.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 95 | 39 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/full-matrix/no-crs/no-mrts/nginx/nginx-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/no-crs/no-mrts/nginx.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 104 | 23 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/full-matrix/no-crs/no-mrts/haproxy/haproxy-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/no-crs/no-mrts/haproxy.log |
| apache | no-crs | with-mrts | FAIL | 516 | 183 | 327 | 0 | 6 | 383 | /src/ModSecurity-conector-build/results/full-matrix/no-crs/with-mrts/apache/apache-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/no-crs/with-mrts/apache.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 87 | 430 | 0 | 6 | 383 | /src/ModSecurity-conector-build/results/full-matrix/no-crs/with-mrts/nginx/nginx-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/no-crs/with-mrts/nginx.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 91 | 419 | 0 | 6 | 383 | /src/ModSecurity-conector-build/results/full-matrix/no-crs/with-mrts/haproxy/haproxy-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/no-crs/with-mrts/haproxy.log |
| apache | with-crs | no-mrts | FAIL | 134 | 101 | 27 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/full-matrix/with-crs/no-mrts/apache/apache-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/with-crs/no-mrts/apache.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 96 | 39 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/full-matrix/with-crs/no-mrts/nginx/nginx-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/with-crs/no-mrts/nginx.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 105 | 23 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/full-matrix/with-crs/no-mrts/haproxy/haproxy-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/with-crs/no-mrts/haproxy.log |
| apache | with-crs | with-mrts | FAIL | 517 | 182 | 329 | 0 | 6 | 383 | /src/ModSecurity-conector-build/results/full-matrix/with-crs/with-mrts/apache/apache-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/with-crs/with-mrts/apache.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 86 | 432 | 0 | 6 | 383 | /src/ModSecurity-conector-build/results/full-matrix/with-crs/with-mrts/nginx/nginx-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/with-crs/with-mrts/nginx.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 90 | 421 | 0 | 6 | 383 | /src/ModSecurity-conector-build/results/full-matrix/with-crs/with-mrts/haproxy/haproxy-summary.json | /src/ModSecurity-conector-build/logs/full-matrix/with-crs/with-mrts/haproxy.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 383 | 161 | 222 | 0 | 0 | 383 |
| nginx | no-crs/with-mrts | 383 | 65 | 318 | 0 | 0 | 383 |
| haproxy | no-crs/with-mrts | 383 | 69 | 314 | 0 | 0 | 383 |
| apache | with-crs/with-mrts | 383 | 161 | 222 | 0 | 0 | 383 |
| nginx | with-crs/with-mrts | 383 | 65 | 318 | 0 | 0 | 383 |
| haproxy | with-crs/with-mrts | 383 | 69 | 314 | 0 | 0 | 383 |

## Guardrails
- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.
- `tests/mrts/imported/**` is golden/reference/drift input only and is not a runtime case root.
- `no-mrts` variants should have zero MRTS runtime cases.
- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.
