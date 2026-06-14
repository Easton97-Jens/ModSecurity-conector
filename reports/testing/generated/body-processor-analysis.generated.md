# Body Processor Failure Analysis

- Generated at: `2026-06-14T10:52:34Z`
- Before selected metadata fix: request_body_processor **9**, multipart_files **12**, xml_processor **24**, combined **45**.
- After selected metadata fix: request_body_processor **0**, multipart_files **0**, xml_processor **0**, combined **0**.
- Selected subcluster rows: **9**
- URL-encoded form rows moved out of active body-processor work: **18** -> **0**.
- XML processor activation-missing rows moved out of active xml_processor work: **24** -> **0**.
- Multipart processor activation-missing rows moved out of active multipart_files work: **12** -> **0**.
- Rule loaded evidence rows: **9**
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

- Count: **18**
- Active request_body_processor rows before report sync: **18**
- Active request_body_processor rows after report sync: **0**
- Classification: `with_mrts_detection_only_non_disruptive`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **18**
- Correct Content-Type rows: **18**
- SecRequestBodyAccess On rows: **18**
- Rule loaded rows: **18**
- Rule matched rows: **14**
- Collection/target evidence rows: **14**
- Backend reached rows: **18**
- Root cause: The URL-encoded bodies and Content-Type are present; these rows are with-MRTS DetectionOnly overlay cases, so disruptive actions remain non-blocking and belong to report-only classification.
- Fix: metadata/report-only; no request body, Content-Type, rule, Expected status, or PASS/FAIL value changed
- Risk: low when kept out of active request_body_processor work; high if promoted to PASS without disruptive runtime evidence

| field | distribution |
| --- | --- |
| connectors | `apache`: 6, `nginx`: 6, `haproxy`: 6 |
| variants | `no-crs/with-mrts`: 9, `with-crs/with-mrts`: 9 |
| case_ids | `pr70_phase2_audit_urlencoded_body`: 6, `request_body_args_post_names_block`: 6, `request_body_urlencoded_block`: 6 |
| rule_ids | `5702`: 6, `2204`: 6, `1200`: 6 |
| targets | `ARGS_POST:arg1`: 6, `ARGS_POST_NAMES`: 6, `ARGS_POST:test`: 6 |
| operators | `@streq pr70phase2`: 6, `@streq arg1`: 6, `@streq attack`: 6 |
| body_lengths | `26`: 6, `19`: 6, `11`: 6 |
| request_body_seen | `unknown`: 12, `yes`: 6 |

## XML Processor Activation-Missing Subcluster

- Count: **24**
- Active xml_processor rows before report sync: **24**
- Active xml_processor rows after report sync: **0**
- Classification: `xml_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **24**
- Correct XML Content-Type rows: **24**
- SecRequestBodyAccess On rows: **0**
- XML processor active rows: **0**
- Rule loaded rows: **24**
- Rule matched rows: **0**
- XML collection evidence rows: **0**
- Backend reached rows: **24**
- Root cause: The XML bodies and Content-Type are present, but these fixtures do not enable SecRequestBodyAccess/ctl:requestBodyProcessor=XML, so XML collection population is not expected evidence.
- Fix: metadata/report-only; no XML body, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector XML parser failure without processor activation

| field | distribution |
| --- | --- |
| connectors | `apache`: 8, `nginx`: 8, `haproxy`: 8 |
| variants | `no-crs/no-mrts`: 12, `with-crs/no-mrts`: 12 |
| case_ids | `parser_xml_partial_body_future_target`: 6, `xml_deep_nesting_future_target`: 6, `xml_namespace_edge_connector_gap`: 6, `xml_request_body_malformed_connector_gap`: 6 |
| rule_ids | `4610`: 6, `4712`: 6, `4711`: 6, `4408`: 6 |
| targets | `XML`: 24 |
| operators | `@contains root`: 6, `@contains deepnode`: 6, `@contains ns:root`: 6, `@contains broken`: 6 |
| content_types | `application/xml`: 24 |
| body_lengths | `9`: 6, `50`: 6, `53`: 6, `21`: 6 |
| body_hashes | `a1cbdf58569b7f77dd47ef83641e48fe830098618b019034b88563050b12eb06`: 6, `9aab1567b5d32b5a5a60ad9f5f6f8f8cf485dbf9aa938905e71a0e88b009f011`: 6, `7eebe35c1d4703c2ed4df34cea9d4149c8aa61bbc104d7c2db81978128ae96e4`: 6, `0c13b76b5721981c5ae77b5629399200d777a7e3b54e6c6d1dbbd43b0d5b75d6`: 6 |
| request_body_seen | `unknown`: 16, `yes`: 8 |

## Multipart Processor Activation-Missing Subcluster

- Count: **12**
- Active multipart_files rows before report sync: **12**
- Active multipart_files rows after report sync: **0**
- Classification: `multipart_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **12**
- Correct Multipart Content-Type rows: **12**
- Boundary valid rows: **12**
- SecRequestBodyAccess On rows: **0**
- Multipart parser active rows: **0**
- Rule loaded rows: **12**
- Rule matched rows: **0**
- FILES/FILES_NAMES evidence rows: **0**
- ARGS/ARGS_NAMES evidence rows: **0**
- Collection/target evidence rows: **0**
- Backend reached rows: **12**
- Root cause: The multipart bodies, Content-Type, boundaries, field names, and filenames are present, but these fixtures do not enable SecRequestBodyAccess before expecting FILES/ARGS_NAMES collection evidence.
- Fix: metadata/report-only; no multipart body, Content-Type, boundary, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector multipart parser failure without request body activation

| field | distribution |
| --- | --- |
| connectors | `apache`: 4, `nginx`: 4, `haproxy`: 4 |
| variants | `no-crs/no-mrts`: 6, `with-crs/no-mrts`: 6 |
| case_ids | `files_names_mixed_case_filename_gap`: 6, `multipart_duplicate_field_names_gap`: 6 |
| rule_ids | `4705`: 6, `4703`: 6 |
| targets | `FILES_NAMES`: 6, `ARGS_NAMES`: 6 |
| operators | `@contains MiXeD.TXT`: 6, `@contains upload`: 6 |
| content_types | `multipart/form-data; boundary=----AaB03x`: 12 |
| boundaries | `----AaB03x`: 12 |
| boundary_status | `valid`: 12 |
| part_counts | `1`: 6, `2`: 6 |
| field_names | `upload`: 18 |
| filenames | `MiXeD.TXT`: 6, `a.txt`: 6, `b.txt`: 6 |
| body_lengths | `130`: 6, `175`: 6 |
| body_hashes | `c798e7b5072cb99121f130d470c4a6fcb5acfae67931b80fe50d1b0d0399f6de`: 6, `fb81f7beb32771bd956270117b1a5040371a2697700d3ffcf43d55f01bd8d46a`: 6 |
| request_body_seen | `unknown`: 8, `yes`: 4 |

## Active Body Processor Distributions

### Connectors

| value | count |
| --- | ---: |

### Variants

| value | count |
| --- | ---: |

### Body Kinds

| value | count |
| --- | ---: |

### Content Types

| value | count |
| --- | ---: |

### Targets

| value | count |
| --- | ---: |

### Failure Categories

| value | count |
| --- | ---: |

## Grouped Rows

| count | connector | body kind | content-type | phase | target | status | category | variants | matched | cause | fixability |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |

## Current Next Fix Plan

- Recommended next cluster: `phase4_hard_abort_capability`
- Reason: Phase 4/RESPONSE_BODY now requires hard-abort evidence, not status-only denial

## Guardrail Notes

- No Expected statuses, testcase rules, request bodies, MRTS definitions, or PASS/FAIL values are changed by this analysis.
- The selected subcluster is metadata-only and remains a runtime FAIL; it is no longer counted as body-processor work.
- URL-encoded/form rows are report-only with-MRTS DetectionOnly overlay evidence; no harness or connector-core change is made for them.
- XML rows in the activation-missing subcluster are report-only because their fixtures do not enable the XML request body processor.
- Multipart rows in the activation-missing subcluster are report-only because their fixtures do not enable request body access before expecting FILES/ARGS_NAMES collection evidence.
- Remaining active body-processor rows are zero after the URL-encoded, XML, and Multipart metadata splits.
