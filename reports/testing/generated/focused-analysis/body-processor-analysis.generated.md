> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:40:18Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-body-processor-analysis.py`
> Make target: `generate-body-processor-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> Input status: `complete`

# Body Processor Failure Analysis

- Generated at: `2026-06-17T02:40:18Z`
- Before selected metadata fix: request_body_processor **9**, multipart_files **8**, xml_processor **16**, combined **33**.
- After selected metadata fix: request_body_processor **0**, multipart_files **0**, xml_processor **0**, combined **0**.
- Selected subcluster rows: **9**
- URL-encoded form rows moved out of active body-processor work: **12** -> **0**.
- XML processor activation-missing rows moved out of active xml_processor work: **16** -> **0**.
- Multipart processor activation-missing rows moved out of active multipart_files work: **8** -> **0**.
- Rule loaded evidence rows: **6**
- Target rule matched rows: **0**
- Backend reached rows: **9**
- Request body access explicitly on: **0**
- Collection/target evidence rows: **0**

## Selected Subcluster

- Case: `phase1_vs_phase2_request_body_gap`
- Count: **9**
- Action: metadata-only classification: request_body_processor -> connector_gap
- Why safe: the case has an empty request body and existing source metadata says connector-gap; no request, rule, expected status, or PASS/FAIL value changed
- Root cause: phase:1 REQUEST_BODY cannot match the expected bodyhit because the YAML request body is empty
- Body arrived: empty by fixture
- Processor active: not relevant for the selected metadata-only classification
- Collections created: no target rule match evidence

## URL-encoded Form Subcluster

- Count: **12**
- Active request_body_processor rows before report sync: **12**
- Active request_body_processor rows after report sync: **0**
- Classification: `with_mrts_detection_only_non_disruptive`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **12**
- Correct Content-Type rows: **12**
- SecRequestBodyAccess On rows: **12**
- Rule loaded rows: **12**
- Rule matched rows: **8**
- Collection/target evidence rows: **8**
- Backend reached rows: **12**
- Root cause: The URL-encoded bodies and Content-Type are present; these rows are with-MRTS DetectionOnly overlay cases, so disruptive actions remain non-blocking and belong to report-only classification.
- Fix: metadata/report-only; no request body, Content-Type, rule, Expected status, or PASS/FAIL value changed
- Risk: low when kept out of active request_body_processor work; high if promoted to PASS without disruptive runtime evidence

| field | distribution |
| --- | --- |
| connectors | `apache`: 6, `haproxy`: 6 |
| variants | `no-crs/with-mrts`: 6, `with-crs/with-mrts`: 6 |
| case_ids | `pr70_phase2_audit_urlencoded_body`: 4, `request_body_args_post_names_block`: 4, `request_body_urlencoded_block`: 4 |
| rule_ids | `5702`: 4, `2204`: 4, `1200`: 4 |
| targets | `ARGS_POST:arg1`: 4, `ARGS_POST_NAMES`: 4, `ARGS_POST:test`: 4 |
| operators | `@streq pr70phase2`: 4, `@streq arg1`: 4, `@streq attack`: 4 |
| body_lengths | `26`: 4, `19`: 4, `11`: 4 |
| request_body_seen | `unknown`: 6, `yes`: 6 |

## XML Processor Activation-Missing Subcluster

- Count: **16**
- Active xml_processor rows before report sync: **16**
- Active xml_processor rows after report sync: **0**
- Classification: `xml_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **16**
- Correct XML Content-Type rows: **16**
- SecRequestBodyAccess On rows: **0**
- XML processor active rows: **0**
- Rule loaded rows: **16**
- Rule matched rows: **0**
- XML collection evidence rows: **0**
- Backend reached rows: **16**
- Root cause: The XML bodies and Content-Type are present, but these fixtures do not enable SecRequestBodyAccess/ctl:requestBodyProcessor=XML, so XML collection population is not expected evidence.
- Fix: metadata/report-only; no XML body, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector XML parser failure without processor activation

| field | distribution |
| --- | --- |
| connectors | `apache`: 8, `haproxy`: 8 |
| variants | `no-crs/no-mrts`: 8, `with-crs/no-mrts`: 8 |
| case_ids | `parser_xml_partial_body_future_target`: 4, `xml_deep_nesting_future_target`: 4, `xml_namespace_edge_connector_gap`: 4, `xml_request_body_malformed_connector_gap`: 4 |
| rule_ids | `4610`: 4, `4712`: 4, `4711`: 4, `4408`: 4 |
| targets | `XML`: 16 |
| operators | `@contains root`: 4, `@contains deepnode`: 4, `@contains ns:root`: 4, `@contains broken`: 4 |
| content_types | `application/xml`: 16 |
| body_lengths | `9`: 4, `50`: 4, `53`: 4, `21`: 4 |
| body_hashes | `a1cbdf58569b7f77dd47ef83641e48fe830098618b019034b88563050b12eb06`: 4, `9aab1567b5d32b5a5a60ad9f5f6f8f8cf485dbf9aa938905e71a0e88b009f011`: 4, `7eebe35c1d4703c2ed4df34cea9d4149c8aa61bbc104d7c2db81978128ae96e4`: 4, `0c13b76b5721981c5ae77b5629399200d777a7e3b54e6c6d1dbbd43b0d5b75d6`: 4 |
| request_body_seen | `unknown`: 8, `yes`: 8 |

## Multipart Processor Activation-Missing Subcluster

- Count: **8**
- Active multipart_files rows before report sync: **8**
- Active multipart_files rows after report sync: **0**
- Classification: `multipart_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **8**
- Correct Multipart Content-Type rows: **8**
- Boundary valid rows: **8**
- SecRequestBodyAccess On rows: **0**
- Multipart parser active rows: **0**
- Rule loaded rows: **8**
- Rule matched rows: **0**
- FILES/FILES_NAMES evidence rows: **0**
- ARGS/ARGS_NAMES evidence rows: **0**
- Collection/target evidence rows: **0**
- Backend reached rows: **8**
- Root cause: The multipart bodies, Content-Type, boundaries, field names, and filenames are present, but these fixtures do not enable SecRequestBodyAccess before expecting FILES/ARGS_NAMES collection evidence.
- Fix: metadata/report-only; no multipart body, Content-Type, boundary, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector multipart parser failure without request body activation

| field | distribution |
| --- | --- |
| connectors | `apache`: 4, `haproxy`: 4 |
| variants | `no-crs/no-mrts`: 4, `with-crs/no-mrts`: 4 |
| case_ids | `files_names_mixed_case_filename_gap`: 4, `multipart_duplicate_field_names_gap`: 4 |
| rule_ids | `4705`: 4, `4703`: 4 |
| targets | `FILES_NAMES`: 4, `ARGS_NAMES`: 4 |
| operators | `@contains MiXeD.TXT`: 4, `@contains upload`: 4 |
| content_types | `multipart/form-data; boundary=----AaB03x`: 8 |
| boundaries | `----AaB03x`: 8 |
| boundary_status | `valid`: 8 |
| part_counts | `1`: 4, `2`: 4 |
| field_names | `upload`: 12 |
| filenames | `MiXeD.TXT`: 4, `a.txt`: 4, `b.txt`: 4 |
| body_lengths | `130`: 4, `175`: 4 |
| body_hashes | `c798e7b5072cb99121f130d470c4a6fcb5acfae67931b80fe50d1b0d0399f6de`: 4, `fb81f7beb32771bd956270117b1a5040371a2697700d3ffcf43d55f01bd8d46a`: 4 |
| request_body_seen | `unknown`: 4, `yes`: 4 |

## Active Body Processor Distributions

### Connectors

| value | count |
| --- | ---: |
_No rows available. Reason: no active body-processor rows remain after report-only classification._

### Variants

| value | count |
| --- | ---: |
_No rows available. Reason: no active body-processor rows remain after report-only classification._

### Body Kinds

| value | count |
| --- | ---: |
_No rows available. Reason: no active body-processor rows remain after report-only classification._

### Content Types

| value | count |
| --- | ---: |
_No rows available. Reason: no active body-processor rows remain after report-only classification._

### Targets

| value | count |
| --- | ---: |
_No rows available. Reason: no active body-processor rows remain after report-only classification._

### Failure Categories

| value | count |
| --- | ---: |
_No rows available. Reason: no active body-processor rows remain after report-only classification._

## Grouped Rows

| count | connector | body kind | content-type | phase | target | status | category | variants | matched | cause | fixability |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
_No rows available. Reason: no active body-processor grouped rows remain after report-only classification._

## Current Next Fix Plan

- Recommended next cluster: `none`
- Reason: No remaining runtime-fixable connector Full-Matrix cluster is recommended after report-only and not-next filters.

## Guardrail Notes

- No Expected statuses, testcase rules, request bodies, MRTS definitions, or PASS/FAIL values are changed by this analysis.
- The selected subcluster is metadata-only and remains a runtime FAIL; it is no longer counted as body-processor work.
- URL-encoded/form rows are report-only with-MRTS DetectionOnly overlay evidence; no harness or connector-core change is made for them.
- XML rows in the activation-missing subcluster are report-only because their fixtures do not enable the XML request body processor.
- Multipart rows in the activation-missing subcluster are report-only because their fixtures do not enable request body access before expecting FILES/ARGS_NAMES collection evidence.
- Remaining active body-processor rows are zero after the URL-encoded, XML, and Multipart metadata splits.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d7a581758867799859f481971e56c0e7da57ca399f5a7e016b2ce839ac83063` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `893fb7f44572f7c5b06974f727c4bd5b56ac2b68eeaf50bd2eb287292a85c567` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `56d43bad850595932f10e7e412d8d7a2a63b60ec8a170535015b7eb12ad7f15d` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
