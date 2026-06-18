> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:15:29Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-no-mrts-intervention-nomatch-analysis.py`
> Make target: `generate-no-mrts-intervention-nomatch-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
> Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
> Input status: `complete`

# No-MRTS Intervention No-Match Analysis

- Generated at: `2026-06-18T16:15:29Z`
- no-MRTS expected `403` / actual `200` rows with loaded rule and no match: **34**
- Unique cases: **9**
- Rule not loaded: **0**
- Rule loaded, no match: **34**
- Rule matched, no intervention: **0**
- Intervention created but connector did not return 403: **0**
- Backend reached: **34**

## Cause Groups

| Cause | Count | Likely cause | Safe fixability | Risk | Examples |
|---|---|---|---|---|---|
| Collection-name normalization semantics | 20 | Header, cookie, or query-name normalization differs from the rule target expectation. | requires native/libmodsecurity comparison before changing harness or connector code | medium to high | duplicate_args_encoded_separator_edge, duplicate_header_case_normalization_gap, edge_semicolon_query_args_names, v3_request_cookies_names_case_runtime_difference, v3_request_headers_names_lowercase_runtime_difference |
| Transformation/request literal does not expose expected token | 8 | The request literal does not contain the expected operator token, or requires unverified transformation semantics before a match can occur. | not safe as a harness fix; changing the request token would change test semantics | high | unicode_double_encoded_uri_runtime_difference, unicode_whitespace_normalization_gap |
| Multipart processor activation missing | 4 | The multipart bodies, Content-Type, and boundary are present, but these fixtures do not enable SecRequestBodyAccess before expecting Multipart FILES/ARGS_NAMES collections. | metadata/report-only; do not change multipart body, rules, Expected status, or connector-core behavior | low if kept report-only; high if treated as connector multipart parser evidence | files_empty_part_future_compatibility |
| Phase 1 request-body unavailable or empty | 2 | The rule reads REQUEST_BODY in phase 1 while the case request body does not contain the expected token. | not safe to fix by changing the body; that would change the test definition | low to medium | phase1_vs_phase2_request_body_gap |

## Connector / Phase / Target / Operator

### Connectors
| Value | Count |
|---|---|
| apache | 17 |
| haproxy | 17 |

### Phases
| Value | Count |
|---|---|
| 1 | 18 |
| 2 | 16 |

### Targets
| Value | Count |
|---|---|
| ARGS_NAMES | 8 |
| REQUEST_HEADERS_NAMES | 8 |
| FILES | 4 |
| REQUEST_URI | 4 |
| ARGS:q | 4 |
| REQUEST_COOKIES_NAMES | 4 |
| REQUEST_BODY | 2 |

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
| @contains bodyhit | 2 |

### Source categories
| Value | Count |
|---|---|
| collections | 20 |
| transformations | 8 |
| multipart | 4 |
| phase-handling | 2 |

### Classifications
| Value | Count |
|---|---|
| collection_name_normalization_semantics | 20 |
| transformation_request_literal_no_match | 8 |
| runtime-difference | 4 |
| phase1_request_body_unavailable | 2 |

### Work directions
| Value | Count |
|---|---|
| collection_semantics | 20 |
| transformation_semantics | 8 |
| intervention_blocking | 4 |
| request_body_processor | 2 |

### Priorities
| Value | Count |
|---|---|
| P3 | 30 |
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
| no-MRTS no-match | 34 | 34 |
| intervention_blocking true candidates | 34 | 4 |
| P0/P1 intervention_blocking rows | 34 | 4 |
| full-matrix pass | 3141 | 3141 |
| full-matrix fail | 775 | 775 |
| full-matrix blocked |  |  |

## Representative Records

| Case | Connector | Variant | Rule | Phase | Target | Operator | Request | Expected value | Classification | Work direction | Priority | Cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| files_empty_part_future_compatibility | apache | no-crs/no-mrts | 4706 | 2 | FILES | @rx ^$ | POST /?- | ^$ | runtime-difference | intervention_blocking | P0 | multipart_processor_activation_missing |
| phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | 4511 | 1 | REQUEST_BODY | @contains bodyhit | POST /?- | bodyhit | phase1_request_body_unavailable | request_body_processor | P3 | phase1_request_body_unavailable_or_empty_body |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | REQUEST_URI | @contains café | GET /?q=%25u0063%25u0061%25u0066%25u00E9 | café | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | ARGS:q | @streq a b | GET /?q=a%E2%80%83b | a b | transformation_request_literal_no_match | transformation_semantics | P3 | transformation_request_value_absent_or_semantic_gap |
| v3_request_cookies_names_case_runtime_difference | apache | no-crs/no-mrts | 4403 | 1 | REQUEST_COOKIES_NAMES | @contains user_token | GET /?- | user_token | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| v3_request_headers_names_lowercase_runtime_difference | apache | no-crs/no-mrts | 4401 | 1 | REQUEST_HEADERS_NAMES | @contains x-smoke-header | GET /?- | x-smoke-header | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_args_encoded_separator_edge | haproxy | no-crs/no-mrts | 4608 | 2 | ARGS_NAMES | @contains b | GET /?a=1%3Bb=2&a=3 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| duplicate_header_case_normalization_gap | haproxy | no-crs/no-mrts | 4607 | 1 | REQUEST_HEADERS_NAMES | @contains x-demo | GET /?- | x-demo | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| edge_semicolon_query_args_names | haproxy | no-crs/no-mrts | 4513 | 2 | ARGS_NAMES | @contains b | GET /?a=1;b=2 | b | collection_name_normalization_semantics | collection_semantics | P3 | collection_name_normalization_semantics |
| files_empty_part_future_compatibility | haproxy | no-crs/no-mrts | 4706 | 2 | FILES | @rx ^$ | POST /?- | ^$ | runtime-difference | intervention_blocking | P0 | multipart_processor_activation_missing |
| phase1_vs_phase2_request_body_gap | haproxy | no-crs/no-mrts | 4511 | 1 | REQUEST_BODY | @contains bodyhit | POST /?- | bodyhit | phase1_request_body_unavailable | request_body_processor | P3 | phase1_request_body_unavailable_or_empty_body |
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

## Guardrails

- Analysis-only report: no Expected status, runtime PASS/FAIL, rule, request, or MRTS definition was changed.
- No connector/core code fix is recommended from this evidence alone.
- No row shows a generated disruptive intervention that a connector later lost.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `cfb36ec0b68c9177b1e4072ec8e7fe9342f023e4e6727caac86c5224df2d6aa0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `94ef7376661e451a7c3a25bd98cb9b769096cd64fe85684fa62e6cef951a017e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `88479f6014f3ca276541b5219356b48ce820401b9146bb365b9839fe9589c1d2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `cc04a8bfd49ce1f7daa7859b93446aae935aa69b452e69ba2db8eda757857660` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `05bc958c83d0fba9f7991380580343ddbe984c2e25b5cd856adc79de70f55828` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
