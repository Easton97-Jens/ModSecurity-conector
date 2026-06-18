> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T21:57:04Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-intervention-blocking-analysis.py`
> Make target: `generate-intervention-blocking-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `29083baa42f7cae3aff7c9f340e2fbe437dd410d`
> Framework SHA: `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67`
> Input status: `complete`

# Intervention Blocking Analysis

- Generated at: `2026-06-17T21:57:04Z`
- Expected `403` / actual `200` rows under review: **553**.
- Intervention-blocking true candidates: **6** runtime-fixable rows.
- Remaining P0/P1 intervention-blocking rows: **6**.
- DetectionOnly overlay non-disruptive rows: **502** report-only rows.
- no-MRTS semantic no-match rows: **45** metadata-only rows.
- Rule in generated loadfile: **366**
- Strict rule-load errors: **0**
- Rule matched: **185**
- Disruptive intervention evidence: **0**
- Connector lost intervention evidence: **0**
- Connector returned 403 from that evidence: **0**
- Backend/client 200 reached: **553**

## Key Split

- with-MRTS DetectionOnly overlay rows: **502**
- with-MRTS rows with logged target-rule match suppressed by that overlay: **185**
- no-MRTS rows with loaded rule but no match evidence: **51**

## A-H Groups

| group | label | count | connectors | variants | suspected cause | fixability | risk |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| A | Rule not loaded | 187 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | Rule-load evidence is missing or startup logs show a strict rule-load error. | fixable if generated loadfile path is wrong | low to medium |
| B | Rule loaded, no match | 34 | apache, haproxy | no-crs/no-mrts, with-crs/no-mrts | The rule is present and no strict load error is visible, but no target rule hit appears in logs or HAProxy decisions. | not a safe intervention fix; requires semantic/native comparison | medium to high |
| C | Rule matched, no intervention created | 0 | - | - | - | - | - |
| D | Intervention created, connector did not set 403 | 0 | - | - | - | - | - |
| E | Intervention created, runner/evidence missed it | 0 | - | - | - | - | - |
| F | Expected block, but effective runtime is non-disruptive | 332 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with-MRTS loads MRTS INIT, which sets ctl:ruleEngine=DetectionOnly; disruptive actions are intentionally non-blocking in this overlay. | classification/report-only unless the MRTS overlay policy changes | low for report-only, high if expectations are changed |
| G | CRS changed behavior | 0 | - | - | - | - | - |
| H | Connector-specific blocking gap | 0 | - | - | - | - | - |

## Representative Evidence

### A. Rule not loaded

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| duplicate_args_encoded_separator_edge | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| duplicate_header_case_normalization_gap | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| edge_semicolon_query_args_names | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| files_empty_part_future_compatibility | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| phase1_vs_phase2_request_body_gap | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| unicode_double_encoded_uri_runtime_difference | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| unicode_whitespace_normalization_gap | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| v3_request_cookies_names_case_runtime_difference | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |

### B. Rule loaded, no match

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | `ARGS_NAMES` | `@contains b` | `/?a=1%3Bb=2&a=3` | yes | no | no | yes |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | `REQUEST_HEADERS_NAMES` | `@contains x-demo` | `/` | yes | no | no | yes |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | `ARGS_NAMES` | `@contains b` | `/?a=1;b=2` | yes | no | no | yes |
| files_empty_part_future_compatibility | apache | no-crs/no-mrts | 4706 | 2 | `FILES` | `@rx ^$` | `/` | yes | no | no | yes |
| phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | 4511 | 1 | `REQUEST_BODY` | `@contains bodyhit` | `/` | yes | no | no | yes |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | `REQUEST_URI` | `@contains café` | `/?q=%25u0063%25u0061%25u0066%25u00E9` | yes | no | no | yes |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | `ARGS:q` | `@streq a b` | `/?q=SAFE` | yes | no | no | yes |
| v3_request_cookies_names_case_runtime_difference | apache | no-crs/no-mrts | 4403 | 1 | `REQUEST_COOKIES_NAMES` | `@contains user_token` | `/` | yes | no | no | yes |

### F. Expected block, but effective runtime is non-disruptive

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| action_deny_phase1 | apache | no-crs/with-mrts | 2101 | 1 | `-` | `-` | `/` | yes | yes | no | yes |
| action_deny_phase2 | apache | no-crs/with-mrts | 2102 | 2 | `-` | `-` | `/` | yes | yes | no | yes |
| audit_log_empty_sections_future_target | apache | no-crs/with-mrts | 4605 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |
| audit_log_matched_var_encoded_value | apache | no-crs/with-mrts | 4603 | 2 | `ARGS:q` | `@contains a b` | `/?q=a+b` | yes | yes | no | yes |
| audit_log_message_presence_connector_gap | apache | no-crs/with-mrts | 4602 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |
| audit_log_multiline_message_normalization | apache | no-crs/with-mrts | 4604 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |
| audit_log_phase1_block | apache | no-crs/with-mrts | 1401 | 1 | `ARGS:audit` | `@streq trigger` | `/?audit=trigger` | yes | yes | no | yes |
| audit_log_rule_id_presence_runtime_difference | apache | no-crs/with-mrts | 4601 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |

## Safe Subcluster

- Selected: **no**
- Name: `none`
- Count: **0**
- Reason: no row shows a real disruptive intervention that is later lost by connector or runner
- Recommended action: do not edit connector/core code yet; decide whether to classify with-MRTS DetectionOnly overlay separately and run native/semantic comparison for no-MRTS no-match cases

## Current Next Fix Plan

- Recommended next cluster: `multipart_files`
- Reason: remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits

## Guardrail Notes

- This report does not change Expected statuses, testcase rules, MRTS definitions, or PASS/FAIL values.
- No row currently proves a disruptive intervention that was later lost by connector or runner.
- The with-MRTS group is classification/report-only unless the MRTS overlay policy is intentionally changed.
- Treat the no-MRTS group as semantic/native-comparison work, not as an intervention-forwarding fix.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `5af2dd56db978d8414704196dececf85cd691fbbcc654f03c0844c73fb4369a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `5eb9a018436e2edd12871ccb50aea3f84e08ae00118acfd315399a8f8f7d0512` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `b237c0433ef2a2d0bf1e4d2bb778d6f7f0501feadebbd3337c99a63d0fe2dd61` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `2316fe5b7e70ff986d2616f0528e208983f6a5dd4b2671bf443f865c6ffbf26f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `bf94318ee4981b80cb2d08e43a02a93a0ff4e20ddf22c88e8b79766ac4bb71f7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
