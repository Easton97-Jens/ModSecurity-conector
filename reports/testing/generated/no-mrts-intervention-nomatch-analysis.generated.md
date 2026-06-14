# No-MRTS Intervention No-Match Analysis

- Generated at: `2026-06-14T09:07:51Z`
- no-MRTS expected `403` / actual `200` rows with loaded rule and no match: **105**
- Unique cases: **18**
- Rule not loaded: **0**
- Rule loaded, no match: **105**
- Rule matched, no intervention: **0**
- Intervention created but connector did not return 403: **0**
- Backend reached: **105**

## Cause Groups

| Cause | Count | Likely cause | Safe fixability | Risk | Examples |
|---|---|---|---|---|---|
| Transformation/request literal does not expose expected token | 36 | The request literal does not contain the expected operator token, or requires unverified transformation semantics before a match can occur. | not safe as a harness fix; changing the request token would change test semantics | high | sqli_like_keyword_spacing_probe, sqli_like_quote_encoding_runtime_difference, unicode_double_encoded_uri_runtime_difference, unicode_whitespace_normalization_gap, xss_like_encoded_angles_normalization_probe, xss_like_mixed_case_script_token_gap |
| Collection-name normalization semantics | 30 | Header, cookie, or query-name normalization differs from the rule target expectation. | requires native/libmodsecurity comparison before changing harness or connector code | medium to high | duplicate_args_encoded_separator_edge, duplicate_header_case_normalization_gap, edge_semicolon_query_args_names, v3_request_cookies_names_case_runtime_difference, v3_request_headers_names_lowercase_runtime_difference |
| XML/body processor collection semantics | 24 | XML collection population or malformed/deep/namespaced XML behavior is not proven to expose the expected value. | not a small safe fix; belongs with body processor evidence work | medium to high | parser_xml_partial_body_future_target, xml_deep_nesting_future_target, xml_namespace_edge_connector_gap, xml_request_body_malformed_connector_gap |
| Multipart collection semantics | 12 | Multipart FILES/ARGS_NAMES population does not expose the expected field or filename token. | not a small safe fix; belongs with multipart/body processor evidence work | medium | files_names_mixed_case_filename_gap, multipart_duplicate_field_names_gap |
| Phase 1 request-body unavailable or empty | 3 | The rule reads REQUEST_BODY in phase 1 while the case request body does not contain the expected token. | not safe to fix by changing the body; that would change the test definition | low to medium | phase1_vs_phase2_request_body_gap |

## Connector / Phase / Target / Operator

### Connectors
| Value | Count |
|---|---|
| apache | 35 |
| nginx | 35 |
| haproxy | 35 |

### Phases
| Value | Count |
|---|---|
| 2 | 78 |
| 1 | 27 |

### Targets
| Value | Count |
|---|---|
| ARGS:q | 30 |
| XML | 24 |
| ARGS_NAMES | 18 |
| REQUEST_HEADERS_NAMES | 12 |
| FILES_NAMES | 6 |
| REQUEST_URI | 6 |
| REQUEST_COOKIES_NAMES | 6 |
| REQUEST_BODY | 3 |

### Operators
| Value | Count |
|---|---|
| @contains b | 12 |
| @contains x-demo | 6 |
| @contains MiXeD.TXT | 6 |
| @contains upload | 6 |
| @contains root | 6 |
| @contains select from | 6 |
| @contains a'b | 6 |
| @contains café | 6 |
| @streq a b | 6 |
| @contains user_token | 6 |
| @contains x-smoke-header | 6 |
| @contains deepnode | 6 |
| @contains ns:root | 6 |
| @contains broken | 6 |
| @contains <tag> | 6 |
| @contains script | 6 |
| @contains bodyhit | 3 |

### Source categories
| Value | Count |
|---|---|
| transformations | 36 |
| collections | 30 |
| body-processors | 24 |
| multipart | 12 |
| phase-handling | 3 |

## Native Comparator

- Status: `no native comparator`
- Matching native case IDs: `-`
- Reason: Native MRTS reports cover upstream MRTS target cases; these 105 rows are framework-owned no-MRTS connector cases.
- Native Apache status: `FAIL`
- Native NGINX status: `FAIL`

## Safe Subcluster Decision

- Selected: **no**
- Cluster: `none`
- Count: **0**
- Reason: No small safe harness/evidence fix was identified. The smallest clear group is phase1_request_body_unavailable_or_empty_body, but changing its body would change the test definition.
- Action: analysis only; no runtime, rule, expected-status, or PASS/FAIL change

## Before / After

| Metric | Before | After |
|---|---|---|
| no-MRTS no-match | 105 | 105 |
| intervention_blocking true candidates | 105 | 105 |
| full-matrix pass | 3074 | 3074 |
| full-matrix fail | 782 | 782 |
| full-matrix blocked |  |  |

## Representative Records

| Case | Connector | Variant | Rule | Phase | Target | Operator | Request | Expected value | Cause |
|---|---|---|---|---|---|---|---|---|---|
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics |
| files_names_mixed_case_filename_gap | apache | no-crs/no-mrts | 4705 | 2 | FILES_NAMES | @contains MiXeD.TXT | POST /?- | MiXeD.TXT | multipart_collection_semantics |
| multipart_duplicate_field_names_gap | apache | no-crs/no-mrts | 4703 | 2 | ARGS_NAMES | @contains upload | POST /?- | upload | multipart_collection_semantics |
| parser_xml_partial_body_future_target | apache | no-crs/no-mrts | 4610 | 2 | XML | @contains root | POST /?- | root | xml_body_processor_collection_semantics |
| phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | 4511 | 1 | REQUEST_BODY | @contains bodyhit | POST /?- | bodyhit | phase1_request_body_unavailable_or_empty_body |
| sqli_like_keyword_spacing_probe | apache | no-crs/no-mrts | 4715 | 2 | ARGS:q | @contains select from | GET /?q=SAFE | select from | transformation_request_value_absent_or_semantic_gap |
| sqli_like_quote_encoding_runtime_difference | apache | no-crs/no-mrts | 4716 | 2 | ARGS:q | @contains a'b | GET /?q=SAFE | a'b | transformation_request_value_absent_or_semantic_gap |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=SAFE | a b | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | apache | no-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | apache | no-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics |
| xml_deep_nesting_future_target | apache | no-crs/no-mrts | 4712 | 2 | XML | @contains deepnode | POST /?- | deepnode | xml_body_processor_collection_semantics |
| xml_namespace_edge_connector_gap | apache | no-crs/no-mrts | 4711 | 2 | XML | @contains ns:root | POST /?- | ns:root | xml_body_processor_collection_semantics |
| xml_request_body_malformed_connector_gap | apache | no-crs/no-mrts | 4408 | 2 | XML | @contains broken | POST /?- | broken | xml_body_processor_collection_semantics |
| xss_like_encoded_angles_normalization_probe | apache | no-crs/no-mrts | 4713 | 2 | ARGS:q | @contains <tag> | GET /?q=SAFE | <tag> | transformation_request_value_absent_or_semantic_gap |
| xss_like_mixed_case_script_token_gap | apache | no-crs/no-mrts | 4714 | 2 | ARGS:q | @contains script | GET /?q=SAFE | script | transformation_request_value_absent_or_semantic_gap |
| duplicate_args_encoded_separator_edge | nginx | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | nginx | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | nginx | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics |
| files_names_mixed_case_filename_gap | nginx | no-crs/no-mrts | 4705 | 2 | FILES_NAMES | @contains MiXeD.TXT | POST /?- | MiXeD.TXT | multipart_collection_semantics |
| multipart_duplicate_field_names_gap | nginx | no-crs/no-mrts | 4703 | 2 | ARGS_NAMES | @contains upload | POST /?- | upload | multipart_collection_semantics |
| parser_xml_partial_body_future_target | nginx | no-crs/no-mrts | 4610 | 2 | XML | @contains root | POST /?- | root | xml_body_processor_collection_semantics |

## Guardrails

- Analysis-only report: no Expected status, runtime PASS/FAIL, rule, request, or MRTS definition was changed.
- No connector/core code fix is recommended from this evidence alone.
- No row shows a generated disruptive intervention that a connector later lost.
