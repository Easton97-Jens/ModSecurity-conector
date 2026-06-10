# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-10T18:10:17Z`
- Variant runs: **12**
- Total attempted: **2628**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **1000** / **304** / **1304** / **24**
- Pending metadata rows observed in runtime summaries: **1532**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 3 | /tmp/modsec-full-run-mrts/full-matrix/no-crs/no-mrts/apache/results/apache-summary.json | /tmp/modsec-full-run-mrts/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 95 | 39 | 0 | 6 | 0 | 334 | /tmp/modsec-full-run-mrts/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-mrts/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 0 | 0 | 133 | 0 | 0 | 81 | /tmp/modsec-full-run-mrts/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-mrts/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 3 | /tmp/modsec-full-run-mrts/full-matrix/no-crs/with-mrts/apache/results/apache-summary.json | /tmp/modsec-full-run-mrts/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 405 | 112 | 0 | 6 | 383 | 1288 | /tmp/modsec-full-run-mrts/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-mrts/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 0 | 0 | 516 | 0 | 383 | 316 | /tmp/modsec-full-run-mrts/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-mrts/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 3 | /tmp/modsec-full-run-mrts/full-matrix/with-crs/no-mrts/apache/results/apache-summary.json | /tmp/modsec-full-run-mrts/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 96 | 39 | 0 | 6 | 0 | 390 | /tmp/modsec-full-run-mrts/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-mrts/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 0 | 0 | 134 | 0 | 0 | 83 | /tmp/modsec-full-run-mrts/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-mrts/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | BLOCKED | 0 | 0 | 0 | 1 | 0 | 0 | 4 | /tmp/modsec-full-run-mrts/full-matrix/with-crs/with-mrts/apache/results/apache-summary.json | /tmp/modsec-full-run-mrts/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 404 | 114 | 0 | 6 | 383 | 1502 | /tmp/modsec-full-run-mrts/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-mrts/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 0 | 0 | 517 | 0 | 383 | 318 | /tmp/modsec-full-run-mrts/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-mrts/full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| nginx | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | no-crs/with-mrts | 383 | 0 | 0 | 383 | 0 | 383 |
| apache | with-crs/with-mrts | 0 | 0 | 0 | 0 | 0 | 0 |
| nginx | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | with-crs/with-mrts | 383 | 0 | 0 | 383 | 0 | 383 |

## Guardrails
- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.
- MRTS golden outputs under the submodule are golden/reference/drift input only and are not runtime case roots.
- `no-mrts` variants should have zero MRTS runtime cases.
- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.
