> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:44:32Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-body-processor-analysis.py`
> Make target: `generate-body-processor-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# Body Processor Failure Analysis

- Generated at: `2026-06-19T06:44:32Z`
- Before selected metadata fix: request_body_processor **9**, multipart_files **6**, xml_processor **12**, combined **27**.
- After selected metadata fix: request_body_processor **0**, multipart_files **6**, xml_processor **0**, combined **6**.
- Selected subcluster rows: **9**
- URL-encoded form rows moved out of active body-processor work: **12** -> **0**.
- XML processor activation-missing rows moved out of active xml_processor work: **12** -> **0**.
- Multipart processor activation-missing rows moved out of active multipart_files work: **0** -> **0**.
- Rule loaded evidence rows: **10**
- Target rule matched rows: **0**
- Backend reached rows: **15**
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

- Count: **12**
- Active xml_processor rows before report sync: **12**
- Active xml_processor rows after report sync: **0**
- Classification: `xml_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **12**
- Correct XML Content-Type rows: **12**
- SecRequestBodyAccess On rows: **4**
- XML processor active rows: **4**
- Rule loaded rows: **12**
- Rule matched rows: **0**
- XML collection evidence rows: **0**
- Backend reached rows: **12**
- Root cause: The XML bodies and Content-Type are present, but these fixtures do not enable SecRequestBodyAccess/ctl:requestBodyProcessor=XML, so XML collection population is not expected evidence.
- Fix: metadata/report-only; no XML body, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector XML parser failure without processor activation

| field | distribution |
| --- | --- |
| connectors | `apache`: 6, `haproxy`: 6 |
| variants | `no-crs/no-mrts`: 6, `with-crs/no-mrts`: 6 |
| case_ids | `parser_xml_partial_body_future_target`: 4, `xml_deep_nesting_future_target`: 4, `xml_request_body_malformed_connector_gap`: 4 |
| rule_ids | `4610`: 4, `4712`: 4, `4408`: 4 |
| targets | `XML`: 12 |
| operators | `@contains root`: 4, `@contains deepnode`: 4, `@contains broken`: 4 |
| content_types | `application/xml`: 12 |
| body_lengths | `9`: 4, `50`: 4, `21`: 4 |
| body_hashes | `a1cbdf58569b7f77dd47ef83641e48fe830098618b019034b88563050b12eb06`: 4, `9aab1567b5d32b5a5a60ad9f5f6f8f8cf485dbf9aa938905e71a0e88b009f011`: 4, `0c13b76b5721981c5ae77b5629399200d777a7e3b54e6c6d1dbbd43b0d5b75d6`: 4 |
| request_body_seen | `unknown`: 6, `yes`: 6 |

## Multipart Processor Activation-Missing Subcluster

- Count: **0**
- Active multipart_files rows before report sync: **0**
- Active multipart_files rows after report sync: **0**
- Classification: `multipart_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **0**
- Correct Multipart Content-Type rows: **0**
- Boundary valid rows: **0**
- SecRequestBodyAccess On rows: **0**
- Multipart parser active rows: **0**
- Rule loaded rows: **0**
- Rule matched rows: **0**
- FILES/FILES_NAMES evidence rows: **0**
- ARGS/ARGS_NAMES evidence rows: **0**
- Collection/target evidence rows: **0**
- Backend reached rows: **0**
- Root cause: The multipart bodies, Content-Type, boundaries, field names, and filenames are present, but these fixtures do not enable SecRequestBodyAccess before expecting FILES/ARGS_NAMES collection evidence.
- Fix: metadata/report-only; no multipart body, Content-Type, boundary, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector multipart parser failure without request body activation

| field | distribution |
| --- | --- |
| connectors | - |
| variants | - |
| case_ids | - |
| rule_ids | - |
| targets | - |
| operators | - |
| content_types | - |
| boundaries | - |
| boundary_status | - |
| part_counts | - |
| field_names | - |
| filenames | - |
| body_lengths | - |
| body_hashes | - |
| request_body_seen | - |

## Active Body Processor Distributions

### Connectors

| value | count |
| --- | ---: |
| `apache` | 2 |
| `nginx` | 2 |
| `haproxy` | 2 |

### Variants

| value | count |
| --- | ---: |
| `no-crs/no-mrts` | 3 |
| `with-crs/no-mrts` | 3 |

### Body Kinds

| value | count |
| --- | ---: |
| `multipart` | 4 |
| `empty` | 2 |

### Content Types

| value | count |
| --- | ---: |
| `multipart/form-data; boundary=----AaB03x` | 4 |
| `-` | 2 |

### Targets

| value | count |
| --- | ---: |
| `FILES` | 4 |
| `-` | 2 |

### Failure Categories

| value | count |
| --- | ---: |
| `multipart_files` | 6 |

## Grouped Rows

| count | connector | body kind | content-type | phase | target | status | category | variants | matched | cause | fixability |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 2 | apache | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES` | 403->200 | multipart_files | no-crs/no-mrts, with-crs/no-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES` | 403->200 | multipart_files | no-crs/no-mrts, with-crs/no-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | nginx | empty | `-` | 2 | `-` | 403->200 | multipart_files | no-crs/no-mrts, with-crs/no-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |

## Current Next Fix Plan

- Recommended next cluster: `multipart_files`
- Reason: remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits

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
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `e270fa2d3f5496b6f5013accb531e9f467fb00871beb7a6c42ac32b45e757676` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `40bf2a3a4325fe9e0dba795d48c4153b1b633d936212a809adce08387261ed80` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `d0ee4bf5ca82cf279209d179703f7b15f244056edd31451b42c708b9e3083c13` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f264523d6bb83b4a3382d4871099d221aac496d36dc8697548b4bba10fd2e52a` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
