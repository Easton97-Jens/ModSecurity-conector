> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:39:34Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-response-header-hook-analysis.py`
> Make target: `generate-response-header-hook-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> Input status: `complete`

# Response Header Hook Analysis

Generated file - do not edit manually.

## Scope
- Response-header FAIL rows analyzed: **60**
- Response-header PASS control rows: **72**
- Connectors: apache, haproxy, nginx
- Variants: no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts
- Phases: 3

## Classification
- `response_header_hook` before: **60**
- `response_header_hook` after: **0**
- Backend/header setup: **0**
- HAProxy Set-Cookie multi-value gap: **0**
- MRTS DetectionOnly overlay: **60**

## Root Cause
- Apache, NGINX, and HAProxy now have no-MRTS PASS controls for deterministic response-header blocking, including specialized Content-Type, Location, and Set-Cookie probes.
- HAProxy preserves repeated `Set-Cookie` response headers through the binary SPOE response-header argument path; the text/scalar fallback remains secondary evidence only.
- `with-mrts` rows that otherwise pass in no-MRTS are suppressed by the MRTS init rule's transaction-level DetectionOnly control; this is classification-only and not a connector PASS promotion.

## PASS Controls
| Connector | Variant | Case | Rule | Header | Expected | Actual |
|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | Set-Cookie | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | Set-Cookie | 403 | 403 |
| apache | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| apache | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| apache | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| nginx | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| nginx | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| haproxy | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| haproxy | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | Set-Cookie | 403 | 403 |
| apache | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | with-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| apache | with-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| apache | with-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| apache | with-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |

## Failure Groups
| Count | Connector | Header | Classification | Phase | Expected | Actual | Example |
|---|---|---|---|---|---|---|---|
| 8 | apache | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 8 | haproxy | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 8 | nginx | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 4 | apache | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | apache | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 4 | haproxy | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | haproxy | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 4 | nginx | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | nginx | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 2 | apache | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | apache | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |
| 2 | haproxy | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | haproxy | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |
| 2 | nginx | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | nginx | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |

## Failure Rows
| Connector | Variant | Case | Rule | Target | Expected header | Actual evidence | Backend header set | ModSecurity sees header | Classification |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d7a581758867799859f481971e56c0e7da57ca399f5a7e016b2ce839ac83063` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `676cc8d9b51b9294387e0b73fe8a7ff1f78a4fe5ff268f5996cb1967b906c576` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `8e4db3774f091e7031c19862d57a29ef6291cb2e82469d9626d637869726c1e4` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
