# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-13T10:10:25Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **3028** / **828** / **0** / **72**
- Pending metadata rows observed in runtime summaries: **552**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 100 | 27 | 0 | 6 | 0 | 340 | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 95 | 39 | 0 | 6 | 0 | 445 | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 104 | 23 | 0 | 6 | 0 | 322 | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 405 | 105 | 0 | 6 | 92 | 1323 | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 405 | 112 | 0 | 6 | 92 | 2430 | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 405 | 105 | 0 | 6 | 92 | 1168 | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 101 | 27 | 0 | 6 | 0 | 361 | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 96 | 39 | 0 | 6 | 0 | 503 | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 105 | 23 | 0 | 6 | 0 | 355 | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 404 | 107 | 0 | 6 | 92 | 1434 | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 404 | 114 | 0 | 6 | 92 | 2653 | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 404 | 107 | 0 | 6 | 92 | 1303 | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /root/.local/state/ModSecurity-conector-full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 92 |
| nginx | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 92 |
| haproxy | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 92 |
| apache | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 92 |
| nginx | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 92 |
| haproxy | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 92 |

## Guardrails
- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.
- MRTS golden outputs under the submodule are golden/reference/drift input only and are not runtime case roots.
- `no-mrts` variants should have zero MRTS runtime cases.
- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.
