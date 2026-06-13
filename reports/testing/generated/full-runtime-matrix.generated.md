# Full MRTS Runtime Matrix

Generated file - do not edit manually.

- Generated at: `2026-06-13T17:29:47Z`
- Variant runs: **12**
- Total attempted: **3928**
- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **3068** / **788** / **0** / **72**
- Pending metadata rows observed in runtime summaries: **2298**

## Variant Results
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 108 | 19 | 0 | 6 | 0 | 330 | /tmp/modsec-response-header-backend/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-response-header-backend/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 103 | 31 | 0 | 6 | 0 | 417 | /tmp/modsec-response-header-backend/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-response-header-backend/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 105 | 22 | 0 | 6 | 0 | 302 | /tmp/modsec-response-header-backend/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-response-header-backend/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 406 | 104 | 0 | 6 | 383 | 1283 | /tmp/modsec-response-header-backend/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-response-header-backend/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 406 | 111 | 0 | 6 | 383 | 2121 | /tmp/modsec-response-header-backend/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-response-header-backend/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 406 | 104 | 0 | 6 | 383 | 1092 | /tmp/modsec-response-header-backend/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-response-header-backend/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 109 | 19 | 0 | 6 | 0 | 363 | /tmp/modsec-response-header-backend/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-response-header-backend/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 104 | 31 | 0 | 6 | 0 | 475 | /tmp/modsec-response-header-backend/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-response-header-backend/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 106 | 22 | 0 | 6 | 0 | 335 | /tmp/modsec-response-header-backend/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-response-header-backend/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 405 | 106 | 0 | 6 | 383 | 1402 | /tmp/modsec-response-header-backend/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /tmp/modsec-response-header-backend/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 405 | 113 | 0 | 6 | 383 | 2357 | /tmp/modsec-response-header-backend/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /tmp/modsec-response-header-backend/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 405 | 106 | 0 | 6 | 383 | 1232 | /tmp/modsec-response-header-backend/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /tmp/modsec-response-header-backend/full-matrix/with-crs/with-mrts/haproxy/run.log |

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
- Apache native: `reports/testing/generated/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.
