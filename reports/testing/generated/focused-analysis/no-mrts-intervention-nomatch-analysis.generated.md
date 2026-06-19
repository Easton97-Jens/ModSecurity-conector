> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:52:48Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-no-mrts-intervention-nomatch-analysis.py`
> Make target: `generate-no-mrts-intervention-nomatch-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# No-MRTS Intervention No-Match Analysis

- Generated at: `2026-06-19T16:52:48Z`
- no-MRTS expected `403` / actual `200` rows with loaded rule and no match: **32**
- Unique cases: **8**
- Rule not loaded: **0**
- Rule loaded, no match: **32**
- Rule matched, no intervention: **0**
- Intervention created but connector did not return 403: **0**
- Backend reached: **32**

## Cause Groups

| Cause | Count | Likely cause | Safe fixability | Risk | Examples |
|---|---|---|---|---|---|
| Collection-name normalization semantics | 20 | Header, cookie, or query-name normalization differs from the rule target expectation. | requires native/libmodsecurity comparison before changing harness or connector code | medium to high | duplicate_args_encoded_separator_edge, duplicate_header_case_normalization_gap, edge_semicolon_query_args_names, v3_request_cookies_names_case_runtime_difference, v3_request_headers_names_lowercase_runtime_difference |
| Transformation/request literal does not expose expected token | 8 | The request literal does not contain the expected operator token, or requires unverified transformation semantics before a match can occur. | not safe as a harness fix; changing the request token would change test semantics | high | unicode_double_encoded_uri_runtime_difference, unicode_whitespace_normalization_gap |
| Multipart processor activation missing | 4 | The multipart bodies, Content-Type, and boundary are present, but these fixtures do not enable SecRequestBodyAccess before expecting Multipart FILES/ARGS_NAMES collections. | metadata/report-only; do not change multipart body, rules, Expected status, or connector-core behavior | low if kept report-only; high if treated as connector multipart parser evidence | files_empty_part_future_compatibility |

## Connector / Phase / Target / Operator

### Connectors
| Value | Count |
|---|---|
| apache | 16 |
| haproxy | 16 |

### Phases
| Value | Count |
|---|---|
| 2 | 16 |
| 1 | 16 |

### Targets
| Value | Count |
|---|---|
| ARGS_NAMES | 8 |
| REQUEST_HEADERS_NAMES | 8 |
| FILES | 4 |
| REQUEST_URI | 4 |
| ARGS:q | 4 |
| REQUEST_COOKIES_NAMES | 4 |

### Operators
| Value | Count |
|---|---|
| @contains b | 8 |
| @contains x-demo | 4 |
| @rx ^$ | 4 |
| @contains café | 4 |
| @streq a b | 4 |
| @contains user_token | 4 |
| @contains x-smoke-header | 4 |

### Source categories
| Value | Count |
|---|---|
| collections | 20 |
| transformations | 8 |
| multipart | 4 |

### Classifications
| Value | Count |
|---|---|
| collection_name_normalization_semantics | 20 |
| transformation_request_literal_no_match | 8 |
| runtime-difference | 4 |

### Work directions
| Value | Count |
|---|---|
| collection_semantics | 20 |
| transformation_semantics | 8 |
| intervention_blocking | 4 |

### Priorities
| Value | Count |
|---|---|
| P3 | 28 |
| P0 | 4 |

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
| no-MRTS no-match | 32 | 32 |
| intervention_blocking true candidates | 32 | 4 |
| P0/P1 intervention_blocking rows | 32 | 4 |
| full-matrix pass | 3157 | 3157 |
| full-matrix fail | 771 | 771 |
| full-matrix blocked |  |  |

## Representative Records

| Case | Connector | Variant | Rule | Phase | Target | Operator | Request | Expected value | Classification | Work direction | Priority | Cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| files_empty_part_future_compatibility | apache | no-crs/no-mrts | 4706 | 2 | FILES | @rx ^$ | POST /?- | ^$ | runtime-difference | intervention_blocking | P0 | multipart_processor_activation_missing |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=a%E2%80%83b | a b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | apache | no-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | apache | no-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_args_encoded_separator_edge | haproxy | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | haproxy | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | haproxy | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| files_empty_part_future_compatibility | haproxy | no-crs/no-mrts | 4706 | 2 | FILES | @rx ^$ | POST /?- | ^$ | runtime-difference | intervention_blocking | P0 | multipart_processor_activation_missing |
| unicode_double_encoded_uri_runtime_difference | haproxy | no-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | haproxy | no-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=a%E2%80%83b | a b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | haproxy | no-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | haproxy | no-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_args_encoded_separator_edge | apache | with-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | apache | with-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | apache | with-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| files_empty_part_future_compatibility | apache | with-crs/no-mrts | 4706 | 2 | FILES | @rx ^$ | POST /?- | ^$ | runtime-difference | intervention_blocking | P0 | multipart_processor_activation_missing |
| unicode_double_encoded_uri_runtime_difference | apache | with-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | apache | with-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=a%E2%80%83b | a b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | apache | with-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | apache | with-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |

## Guardrails

- Analysis-only report: no Expected status, runtime PASS/FAIL, rule, request, or MRTS definition was changed.
- No connector/core code fix is recommended from this evidence alone.
- No row shows a generated disruptive intervention that a connector later lost.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `01a816a7d7bf3062a4b8a236aa9d1a56cf008828c6b67a09ce939b0fe9da9d9d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `d31fb8c743fe579a70cd77d1d455f749b99e3682d1737d2751c70f3b46c520a8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `3425a08630d7eee65c73745216c902a605453363e9b26c12d62d042fabddf0a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `06d58887a5b4c5497345a54792d90cfa4c910b3ae1610b2f0efed714c60f3a54` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `67eae92c2d1fde007978f559f16c43598eb52d2c4a80fd0bd171c4748cfb62ff` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
