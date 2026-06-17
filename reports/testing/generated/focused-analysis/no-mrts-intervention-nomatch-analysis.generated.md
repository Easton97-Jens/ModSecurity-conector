> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:40:09Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-no-mrts-intervention-nomatch-analysis.py`
> Make target: `generate-no-mrts-intervention-nomatch-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> Input status: `complete`

# No-MRTS Intervention No-Match Analysis

- Generated at: `2026-06-17T02:40:09Z`
- no-MRTS expected `403` / actual `200` rows with loaded rule and no match: **46**
- Unique cases: **12**
- Rule not loaded: **0**
- Rule loaded, no match: **46**
- Rule matched, no intervention: **0**
- Intervention created but connector did not return 403: **0**
- Backend reached: **46**

## Cause Groups

| Cause | Count | Likely cause | Safe fixability | Risk | Examples |
|---|---|---|---|---|---|
| Transformation/request literal does not expose expected token | 24 | The request literal does not contain the expected operator token, or requires unverified transformation semantics before a match can occur. | not safe as a harness fix; changing the request token would change test semantics | high | sqli_like_keyword_spacing_probe, sqli_like_quote_encoding_runtime_difference, unicode_double_encoded_uri_runtime_difference, unicode_whitespace_normalization_gap, xss_like_encoded_angles_normalization_probe, xss_like_mixed_case_script_token_gap |
| Collection-name normalization semantics | 20 | Header, cookie, or query-name normalization differs from the rule target expectation. | requires native/libmodsecurity comparison before changing harness or connector code | medium to high | duplicate_args_encoded_separator_edge, duplicate_header_case_normalization_gap, edge_semicolon_query_args_names, v3_request_cookies_names_case_runtime_difference, v3_request_headers_names_lowercase_runtime_difference |
| Phase 1 request-body unavailable or empty | 2 | The rule reads REQUEST_BODY in phase 1 while the case request body does not contain the expected token. | not safe to fix by changing the body; that would change the test definition | low to medium | phase1_vs_phase2_request_body_gap |

## Connector / Phase / Target / Operator

### Connectors
| Value | Count |
|---|---|
| apache | 23 |
| haproxy | 23 |

### Phases
| Value | Count |
|---|---|
| 2 | 28 |
| 1 | 18 |

### Targets
| Value | Count |
|---|---|
| ARGS:q | 20 |
| ARGS_NAMES | 8 |
| REQUEST_HEADERS_NAMES | 8 |
| REQUEST_URI | 4 |
| REQUEST_COOKIES_NAMES | 4 |
| REQUEST_BODY | 2 |

### Operators
| Value | Count |
|---|---|
| @contains b | 8 |
| @contains x-demo | 4 |
| @contains select from | 4 |
| @contains a'b | 4 |
| @contains café | 4 |
| @streq a b | 4 |
| @contains user_token | 4 |
| @contains x-smoke-header | 4 |
| @contains <tag> | 4 |
| @contains script | 4 |
| @contains bodyhit | 2 |

### Source categories
| Value | Count |
|---|---|
| transformations | 24 |
| collections | 20 |
| phase-handling | 2 |

### Classifications
| Value | Count |
|---|---|
| transformation_request_literal_no_match | 24 |
| collection_name_normalization_semantics | 20 |
| phase1_request_body_unavailable | 2 |

### Work directions
| Value | Count |
|---|---|
| transformation_semantics | 24 |
| collection_semantics | 20 |
| request_body_processor | 2 |

### Priorities
| Value | Count |
|---|---|
| P3 | 46 |

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
| no-MRTS no-match | 46 | 46 |
| intervention_blocking true candidates | 46 |  |
| P0/P1 intervention_blocking rows | 46 |  |
| full-matrix pass | 3074 | 3074 |
| full-matrix fail | 782 | 782 |
| full-matrix blocked |  |  |

## Representative Records

| Case | Connector | Variant | Rule | Phase | Target | Operator | Request | Expected value | Classification | Work direction | Priority | Cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | 4511 | 1 | REQUEST_BODY | @contains bodyhit | POST /?- | bodyhit | phase1_request_body_unavailable | request_body_processor | P3 | phase1_request_body_unavailable_or_empty_body |
| sqli_like_keyword_spacing_probe | apache | no-crs/no-mrts | 4715 | 2 | ARGS:q | @contains select from | GET /?q=SAFE | select from | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| sqli_like_quote_encoding_runtime_difference | apache | no-crs/no-mrts | 4716 | 2 | ARGS:q | @contains a'b | GET /?q=SAFE | a'b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=SAFE | a b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | apache | no-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | apache | no-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| xss_like_encoded_angles_normalization_probe | apache | no-crs/no-mrts | 4713 | 2 | ARGS:q | @contains <tag> | GET /?q=SAFE | <tag> | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| xss_like_mixed_case_script_token_gap | apache | no-crs/no-mrts | 4714 | 2 | ARGS:q | @contains script | GET /?q=SAFE | script | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| duplicate_args_encoded_separator_edge | haproxy | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | haproxy | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | haproxy | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| phase1_vs_phase2_request_body_gap | haproxy | no-crs/no-mrts | 4511 | 1 | REQUEST_BODY | @contains bodyhit | POST /?- | bodyhit | phase1_request_body_unavailable | request_body_processor | P3 | phase1_request_body_unavailable_or_empty_body |
| sqli_like_keyword_spacing_probe | haproxy | no-crs/no-mrts | 4715 | 2 | ARGS:q | @contains select from | GET /?q=SAFE | select from | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| sqli_like_quote_encoding_runtime_difference | haproxy | no-crs/no-mrts | 4716 | 2 | ARGS:q | @contains a'b | GET /?q=SAFE | a'b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_double_encoded_uri_runtime_difference | haproxy | no-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | haproxy | no-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=SAFE | a b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | haproxy | no-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | haproxy | no-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| xss_like_encoded_angles_normalization_probe | haproxy | no-crs/no-mrts | 4713 | 2 | ARGS:q | @contains <tag> | GET /?q=SAFE | <tag> | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| xss_like_mixed_case_script_token_gap | haproxy | no-crs/no-mrts | 4714 | 2 | ARGS:q | @contains script | GET /?q=SAFE | script | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |

## Guardrails

- Analysis-only report: no Expected status, runtime PASS/FAIL, rule, request, or MRTS definition was changed.
- No connector/core code fix is recommended from this evidence alone.
- No row shows a generated disruptive intervention that a connector later lost.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `c1bafe3651af877ed965d9b22cdeb6175f4df1d478e28b603ebf0bdc2b68f6e9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `676cc8d9b51b9294387e0b73fe8a7ff1f78a4fe5ff268f5996cb1967b906c576` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `893fb7f44572f7c5b06974f727c4bd5b56ac2b68eeaf50bd2eb287292a85c567` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d7a581758867799859f481971e56c0e7da57ca399f5a7e016b2ce839ac83063` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `56d43bad850595932f10e7e412d8d7a2a63b60ec8a170535015b7eb12ad7f15d` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
