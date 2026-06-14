# Intervention Blocking Analysis

- Generated at: `2026-06-14T11:06:36Z`
- Expected `403` / actual `200` rows under review: **559**.
- Intervention-blocking true candidates: **0** runtime-fixable rows.
- Remaining P0/P1 intervention-blocking rows: **0**.
- DetectionOnly overlay non-disruptive rows: **490** report-only rows.
- no-MRTS semantic no-match rows: **69** metadata-only rows.
- Rule in generated loadfile: **559**
- Strict rule-load errors: **0**
- Rule matched: **298**
- Disruptive intervention evidence: **0**
- Connector lost intervention evidence: **0**
- Connector returned 403 from that evidence: **0**
- Backend/client 200 reached: **559**

## Key Split

- with-MRTS DetectionOnly overlay rows: **490**
- with-MRTS rows with logged target-rule match suppressed by that overlay: **298**
- no-MRTS rows with loaded rule but no match evidence: **69**

## A-H Groups

| group | label | count | connectors | variants | suspected cause | fixability | risk |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| A | Rule not loaded | 0 | - | - | - | - | - |
| B | Rule loaded, no match | 69 | apache, haproxy, nginx | no-crs/no-mrts, with-crs/no-mrts | The rule is present and no strict load error is visible, but no target rule hit appears in logs or HAProxy decisions. | not a safe intervention fix; requires semantic/native comparison | medium to high |
| C | Rule matched, no intervention created | 0 | - | - | - | - | - |
| D | Intervention created, connector did not set 403 | 0 | - | - | - | - | - |
| E | Intervention created, runner/evidence missed it | 0 | - | - | - | - | - |
| F | Expected block, but effective runtime is non-disruptive | 490 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with-MRTS loads MRTS INIT, which sets ctl:ruleEngine=DetectionOnly; disruptive actions are intentionally non-blocking in this overlay. | classification/report-only unless the MRTS overlay policy changes | low for report-only, high if expectations are changed |
| G | CRS changed behavior | 0 | - | - | - | - | - |
| H | Connector-specific blocking gap | 0 | - | - | - | - | - |

## Representative Evidence

### B. Rule loaded, no match

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | `ARGS_NAMES` | `@contains b` | `/?a=1%3Bb=2&a=3` | yes | no | no | yes |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | `REQUEST_HEADERS_NAMES` | `@contains x-demo` | `/` | yes | no | no | yes |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | `ARGS_NAMES` | `@contains b` | `/?a=1;b=2` | yes | no | no | yes |
| phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | 4511 | 1 | `REQUEST_BODY` | `@contains bodyhit` | `/` | yes | no | no | yes |
| sqli_like_keyword_spacing_probe | apache | no-crs/no-mrts | 4715 | 2 | `ARGS:q` | `@contains select from` | `/?q=SAFE` | yes | no | no | yes |
| sqli_like_quote_encoding_runtime_difference | apache | no-crs/no-mrts | 4716 | 2 | `ARGS:q` | `@contains a'b` | `/?q=SAFE` | yes | no | no | yes |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | `REQUEST_URI` | `@contains café` | `/?q=%25u0063%25u0061%25u0066%25u00E9` | yes | no | no | yes |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | `ARGS:q` | `@streq a b` | `/?q=SAFE` | yes | no | no | yes |

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

- Recommended next cluster: `rule_chain_semantics and small single-connector leftovers`
- Reason: smaller count; useful after high-signal evidence clusters

## Guardrail Notes

- This report does not change Expected statuses, testcase rules, MRTS definitions, or PASS/FAIL values.
- No row currently proves a disruptive intervention that was later lost by connector or runner.
- The with-MRTS group is classification/report-only unless the MRTS overlay policy is intentionally changed.
- Treat the no-MRTS group as semantic/native-comparison work, not as an intervention-forwarding fix.
