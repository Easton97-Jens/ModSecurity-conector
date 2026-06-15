> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:36Z`
> Generator: `ci/generate-body-processor-analysis.py`
> Make target: `generate-body-processor-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# Body Processor Failure Analysis

- Generated at: `2026-06-15T10:40:36Z`
- Before selected metadata fix: request_body_processor **9**, multipart_files **0**, xml_processor **0**, combined **9**.
- After selected metadata fix: request_body_processor **0**, multipart_files **0**, xml_processor **0**, combined **0**.
- Selected subcluster rows: **9**
- URL-encoded form rows moved out of active body-processor work: **0** -> **0**.
- XML processor activation-missing rows moved out of active xml_processor work: **0** -> **0**.
- Multipart processor activation-missing rows moved out of active multipart_files work: **0** -> **0**.
- Rule loaded evidence rows: **0**
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

- Count: **0**
- Active request_body_processor rows before report sync: **0**
- Active request_body_processor rows after report sync: **0**
- Classification: `with_mrts_detection_only_non_disruptive`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **0**
- Correct Content-Type rows: **0**
- SecRequestBodyAccess On rows: **0**
- Rule loaded rows: **0**
- Rule matched rows: **0**
- Collection/target evidence rows: **0**
- Backend reached rows: **0**
- Root cause: The URL-encoded bodies and Content-Type are present; these rows are with-MRTS DetectionOnly overlay cases, so disruptive actions remain non-blocking and belong to report-only classification.
- Fix: metadata/report-only; no request body, Content-Type, rule, Expected status, or PASS/FAIL value changed
- Risk: low when kept out of active request_body_processor work; high if promoted to PASS without disruptive runtime evidence

| field | distribution |
| --- | --- |
| connectors | - |
| variants | - |
| case_ids | - |
| rule_ids | - |
| targets | - |
| operators | - |
| body_lengths | - |
| request_body_seen | - |

## XML Processor Activation-Missing Subcluster

- Count: **0**
- Active xml_processor rows before report sync: **0**
- Active xml_processor rows after report sync: **0**
- Classification: `xml_processor_activation_missing`
- Work direction: `classification_only`
- Priority: `report_only`
- Body sent rows: **0**
- Correct XML Content-Type rows: **0**
- SecRequestBodyAccess On rows: **0**
- XML processor active rows: **0**
- Rule loaded rows: **0**
- Rule matched rows: **0**
- XML collection evidence rows: **0**
- Backend reached rows: **0**
- Root cause: The XML bodies and Content-Type are present, but these fixtures do not enable SecRequestBodyAccess/ctl:requestBodyProcessor=XML, so XML collection population is not expected evidence.
- Fix: metadata/report-only; no XML body, rule, Expected status, connector-core behavior, or PASS/FAIL value changed
- Risk: low when kept report-only; high if treated as a connector XML parser failure without processor activation

| field | distribution |
| --- | --- |
| connectors | - |
| variants | - |
| case_ids | - |
| rule_ids | - |
| targets | - |
| operators | - |
| content_types | - |
| body_lengths | - |
| body_hashes | - |
| request_body_seen | - |

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

- Recommended next cluster: `none`
- Reason: No remaining runtime-fixable connector Full-Matrix cluster is recommended after report-only and not-next filters.

## Guardrail Notes

- No Expected statuses, testcase rules, request bodies, MRTS definitions, or PASS/FAIL values are changed by this analysis.
- The selected subcluster is metadata-only and remains a runtime FAIL; it is no longer counted as body-processor work.
- URL-encoded/form rows are report-only with-MRTS DetectionOnly overlay evidence; no harness or connector-core change is made for them.
- XML rows in the activation-missing subcluster are report-only because their fixtures do not enable the XML request body processor.
- Multipart rows in the activation-missing subcluster are report-only because their fixtures do not enable request body access before expecting FILES/ARGS_NAMES collection evidence.
- Remaining active body-processor rows are zero after the URL-encoded, XML, and Multipart metadata splits.

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
