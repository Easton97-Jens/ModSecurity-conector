> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:29Z`
> Generator: `ci/generate-intervention-blocking-analysis.py`
> Make target: `generate-intervention-blocking-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# Intervention Blocking Analysis

- Generated at: `2026-06-15T10:40:29Z`
- Expected `403` / actual `200` rows under review: **559**.
- Intervention-blocking true candidates: **0** runtime-fixable rows.
- Remaining P0/P1 intervention-blocking rows: **0**.
- DetectionOnly overlay non-disruptive rows: **490** report-only rows.
- no-MRTS semantic no-match rows: **69** metadata-only rows.
- Rule in generated loadfile: **0**
- Strict rule-load errors: **0**
- Rule matched: **0**
- Disruptive intervention evidence: **0**
- Connector lost intervention evidence: **0**
- Connector returned 403 from that evidence: **0**
- Backend/client 200 reached: **559**

## Key Split

- with-MRTS DetectionOnly overlay rows: **490**
- with-MRTS rows with logged target-rule match suppressed by that overlay: **0**
- no-MRTS rows with loaded rule but no match evidence: **69**

## A-H Groups

| group | label | count | connectors | variants | suspected cause | fixability | risk |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| A | Rule not loaded | 559 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | Rule-load evidence is missing or startup logs show a strict rule-load error. | fixable if generated loadfile path is wrong | low to medium |
| B | Rule loaded, no match | 0 | - | - | - | - | - |
| C | Rule matched, no intervention created | 0 | - | - | - | - | - |
| D | Intervention created, connector did not set 403 | 0 | - | - | - | - | - |
| E | Intervention created, runner/evidence missed it | 0 | - | - | - | - | - |
| F | Expected block, but effective runtime is non-disruptive | 0 | - | - | - | - | - |
| G | CRS changed behavior | 0 | - | - | - | - | - |
| H | Connector-specific blocking gap | 0 | - | - | - | - | - |

## Representative Evidence

### A. Rule not loaded

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| sqli_like_keyword_spacing_probe | apache | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| sqli_like_quote_encoding_runtime_difference | apache | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |

## Safe Subcluster

- Selected: **no**
- Name: `none`
- Count: **0**
- Reason: no row shows a real disruptive intervention that is later lost by connector or runner
- Recommended action: do not edit connector/core code yet; decide whether to classify with-MRTS DetectionOnly overlay separately and run native/semantic comparison for no-MRTS no-match cases

## Current Next Fix Plan

- Recommended next cluster: `none`
- Reason: No remaining runtime-fixable connector Full-Matrix cluster is recommended after report-only and not-next filters.

## Guardrail Notes

- This report does not change Expected statuses, testcase rules, MRTS definitions, or PASS/FAIL values.
- No row currently proves a disruptive intervention that was later lost by connector or runner.
- The with-MRTS group is classification/report-only unless the MRTS overlay policy is intentionally changed.
- Treat the no-MRTS group as semantic/native-comparison work, not as an intervention-forwarding fix.

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
