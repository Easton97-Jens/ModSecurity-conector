# Response Header Hook Analysis

Generated file - do not edit manually.

## Scope
- Response-header FAIL rows analyzed: **94**
- Response-header PASS control rows: **38**
- Connectors: apache, haproxy, nginx
- Variants: no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts
- Phases: 3

## Classification
- `response_header_hook` before: **94**
- `response_header_hook` after: **0**
- Backend/header setup: **56**
- HAProxy Set-Cookie multi-value gap: **12**
- MRTS DetectionOnly overlay: **26**

## Root Cause
- Apache and NGINX only prove basic `Last-Modified` response-header blocking in current no-MRTS evidence; the specialized Content-Type, Location, and Set-Cookie probes do not have deterministic backend header setup there.
- HAProxy response-header processing is live-evidenced, but `Set-Cookie` multi-value probes do not expose every expected value through the current SPOE response-header argument path.
- `with-mrts` rows that otherwise pass in no-MRTS are suppressed by the MRTS init rule's transaction-level DetectionOnly control; this is classification-only and not a connector PASS promotion.

## PASS Controls
| Connector | Variant | Case | Rule | Header | Expected | Actual |
|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| apache | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| apache | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| nginx | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| nginx | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| haproxy | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| haproxy | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| apache | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | with-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | with-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| apache | with-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| apache | with-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| nginx | with-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | with-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| nginx | with-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| nginx | with-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| haproxy | with-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| haproxy | with-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| haproxy | with-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| haproxy | with-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| haproxy | with-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | with-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| haproxy | with-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| haproxy | with-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| apache | with-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | with-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | with-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |

## Failure Groups
| Count | Connector | Header | Classification | Phase | Expected | Actual | Example |
|---|---|---|---|---|---|---|---|
| 16 | apache | Set-Cookie | response_header_backend_setup | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 16 | nginx | Set-Cookie | response_header_backend_setup | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 12 | haproxy | Set-Cookie | response_header_multi_value_gap | 3 | 403 | 200 | phase3_response_headers_multi_value_connector_gap |
| 8 | apache | Location | response_header_backend_setup | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 8 | nginx | Location | response_header_backend_setup | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 4 | apache | Content-Type | response_header_backend_setup | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 4 | apache | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | haproxy | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | haproxy | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 4 | nginx | Content-Type | response_header_backend_setup | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 4 | nginx | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 2 | apache | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |
| 2 | haproxy | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | haproxy | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 2 | haproxy | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |
| 2 | nginx | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |

## Failure Rows
| Connector | Variant | Case | Rule | Target | Expected header | Actual evidence | Backend header set | ModSecurity sees header | Classification |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| haproxy | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| apache | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| apache | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| haproxy | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| apache | with-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| haproxy | with-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | with-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | with-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| apache | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| apache | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_backend_setup |
| nginx | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_backend_setup |
| haproxy | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | False | False | response_header_multi_value_gap |
| haproxy | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | False | False | response_header_multi_value_gap |
