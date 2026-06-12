# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-12T19:14:09Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **1956** / **1899** / **1** / **72**
- Pending metadata rows observed in runtime summaries: **2298**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 100 | 27 | 0 | 6 | 0 | 312 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 95 | 39 | 0 | 6 | 0 | 381 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 104 | 23 | 0 | 6 | 0 | 296 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 183 | 327 | 0 | 6 | 383 | 1245 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 405 | 112 | 0 | 6 | 383 | 1823 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 91 | 418 | 1 | 6 | 383 | 1076 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 101 | 27 | 0 | 6 | 0 | 341 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 96 | 39 | 0 | 6 | 0 | 437 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 105 | 23 | 0 | 6 | 0 | 328 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 182 | 329 | 0 | 6 | 383 | 1364 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 404 | 114 | 0 | 6 | 383 | 2042 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 90 | 421 | 0 | 6 | 383 | 1203 | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-full-run-after-nginx-fix/full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream Config Tests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 383 | 161 | 222 | 0 | 0 | 383 |
| nginx | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | no-crs/with-mrts | 383 | 69 | 313 | 1 | 0 | 383 |
| apache | with-crs/with-mrts | 383 | 161 | 222 | 0 | 0 | 383 |
| nginx | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | with-crs/with-mrts | 383 | 69 | 314 | 0 | 0 | 383 |

## Guardrails
- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.
- MRTS golden outputs under the submodule are golden/reference/drift input only and are not runtime case roots.
- `no-mrts` variants should have zero MRTS runtime cases.
- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.
