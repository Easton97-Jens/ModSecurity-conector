# Body Processor Failure Analysis

- Generated at: `2026-06-14T08:49:22Z`
- Before selected metadata fix: request_body_processor **69**, multipart_files **66**, xml_processor **54**, combined **189**.
- After selected metadata fix: request_body_processor **60**, multipart_files **66**, xml_processor **54**, combined **180**.
- Selected subcluster rows: **9**
- Rule loaded evidence rows: **189**
- Target rule matched rows: **76**
- Backend reached rows: **189**
- Request body access explicitly on: **72**
- Collection/target evidence rows: **76**

## Selected Subcluster

- Case: `phase1_vs_phase2_request_body_gap`
- Count: **9**
- Action: metadata-only classification: request_body_processor -> connector_gap
- Why safe: the case has an empty request body and existing source metadata says connector-gap; no request, rule, expected status, or PASS/FAIL value changed
- Root cause: phase:1 REQUEST_BODY cannot match the expected bodyhit because the YAML request body is empty
- Body arrived: empty by fixture
- Processor active: not relevant for the selected metadata-only classification
- Collections created: no target rule match evidence

## Distributions

### Connectors

| value | count |
| --- | ---: |
| `apache` | 60 |
| `nginx` | 60 |
| `haproxy` | 60 |

### Variants

| value | count |
| --- | ---: |
| `no-crs/with-mrts` | 72 |
| `with-crs/with-mrts` | 72 |
| `no-crs/no-mrts` | 18 |
| `with-crs/no-mrts` | 18 |

### Body Kinds

| value | count |
| --- | ---: |
| `multipart` | 66 |
| `xml` | 54 |
| `json` | 36 |
| `form` | 18 |
| `raw` | 6 |

### Content Types

| value | count |
| --- | ---: |
| `application/xml` | 48 |
| `application/json` | 36 |
| `multipart/form-data; boundary=----AaB03x` | 30 |
| `-` | 30 |
| `application/x-www-form-urlencoded` | 18 |
| `multipart/form-data; boundary=----BROKEN` | 6 |
| `text/plain` | 6 |
| `text/xml` | 6 |

### Targets

| value | count |
| --- | ---: |
| `XML` | 48 |
| `REQUEST_BODY` | 48 |
| `FILES_NAMES` | 18 |
| `ARGS_NAMES` | 12 |
| `MULTIPART_FILENAME` | 12 |
| `ARGS:name` | 6 |
| `FILES_COMBINED_SIZE` | 6 |
| `FILES:filedata1` | 6 |
| `ARGS_POST:arg1` | 6 |
| `ARGS_POST_NAMES` | 6 |
| `ARGS_POST:test` | 6 |
| `XML:/*` | 6 |

### Failure Categories

| value | count |
| --- | ---: |
| `multipart_files` | 66 |
| `request_body_processor` | 60 |
| `xml_processor` | 54 |

## Grouped Rows

| count | connector | body kind | content-type | phase | target | status | category | variants | matched | cause | fixability |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 16 | apache | xml | `application/xml` | 2 | `XML` | 403->200 | xml_processor | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review. | requires targeted native/connector comparison before code changes |
| 16 | haproxy | xml | `application/xml` | 2 | `XML` | 403->200 | xml_processor | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review. | requires targeted native/connector comparison before code changes |
| 16 | nginx | xml | `application/xml` | 2 | `XML` | 403->200 | xml_processor | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review. | requires targeted native/connector comparison before code changes |
| 12 | apache | json | `application/json` | 2 | `REQUEST_BODY` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 12 | JSON/raw REQUEST_BODY rows need processor-specific semantics review; with-MRTS rows may be non-blocking due DetectionOnly overlay. | classification/report-only unless MRTS DetectionOnly policy changes |
| 12 | haproxy | json | `application/json` | 2 | `REQUEST_BODY` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | JSON/raw REQUEST_BODY rows need processor-specific semantics review; with-MRTS rows may be non-blocking due DetectionOnly overlay. | requires targeted native/connector comparison before code changes |
| 12 | nginx | json | `application/json` | 2 | `REQUEST_BODY` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 12 | JSON/raw REQUEST_BODY rows need processor-specific semantics review; with-MRTS rows may be non-blocking due DetectionOnly overlay. | classification/report-only unless MRTS DetectionOnly policy changes |
| 4 | apache | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `ARGS_NAMES` | 403->200 | multipart_files | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 4 | apache | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES_NAMES` | 403->200 | multipart_files | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 4 | haproxy | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `ARGS_NAMES` | 403->200 | multipart_files | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 4 | haproxy | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES_NAMES` | 403->200 | multipart_files | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 4 | nginx | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `ARGS_NAMES` | 403->200 | multipart_files | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 4 | nginx | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES_NAMES` | 403->200 | multipart_files | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | apache | multipart | `-` | 2 | `ARGS:name` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | multipart | `-` | 2 | `FILES:filedata1` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | multipart | `-` | 2 | `FILES_COMBINED_SIZE` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | multipart | `-` | 2 | `FILES_NAMES` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `MULTIPART_FILENAME` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | multipart | `-` | 2 | `MULTIPART_FILENAME` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | multipart | `multipart/form-data; boundary=----BROKEN` | 2 | `REQUEST_BODY` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | haproxy | multipart | `-` | 2 | `ARGS:name` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `-` | 2 | `FILES:filedata1` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `-` | 2 | `FILES_COMBINED_SIZE` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `-` | 2 | `FILES_NAMES` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `MULTIPART_FILENAME` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `-` | 2 | `MULTIPART_FILENAME` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `multipart/form-data; boundary=----BROKEN` | 2 | `REQUEST_BODY` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | nginx | multipart | `-` | 2 | `ARGS:name` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | multipart | `-` | 2 | `FILES:filedata1` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | multipart | `-` | 2 | `FILES_COMBINED_SIZE` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | multipart | `-` | 2 | `FILES_NAMES` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `MULTIPART_FILENAME` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | multipart | `-` | 2 | `MULTIPART_FILENAME` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | multipart | `multipart/form-data; boundary=----BROKEN` | 2 | `REQUEST_BODY` | 403->200 | multipart_files | no-crs/with-mrts, with-crs/with-mrts | 2 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST:arg1` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST:test` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST_NAMES` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | raw | `text/plain` | 2 | `REQUEST_BODY` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | manual review | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | haproxy | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST:arg1` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | haproxy | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST:test` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 0 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST_NAMES` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 0 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | raw | `text/plain` | 2 | `REQUEST_BODY` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 0 | manual review | requires targeted native/connector comparison before code changes |
| 2 | nginx | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST:arg1` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST:test` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | form | `application/x-www-form-urlencoded` | 2 | `ARGS_POST_NAMES` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | nginx | raw | `text/plain` | 2 | `REQUEST_BODY` | 403->200 | request_body_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | manual review | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | apache | xml | `text/xml` | 2 | `XML:/*` | 403->200 | xml_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review. | classification/report-only unless MRTS DetectionOnly policy changes |
| 2 | haproxy | xml | `text/xml` | 2 | `XML:/*` | 403->200 | xml_processor | no-crs/with-mrts, with-crs/with-mrts | 0 | XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review. | requires targeted native/connector comparison before code changes |
| 2 | nginx | xml | `text/xml` | 2 | `XML:/*` | 403->200 | xml_processor | no-crs/with-mrts, with-crs/with-mrts | 2 | XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review. | classification/report-only unless MRTS DetectionOnly policy changes |

## Current Next Fix Plan

- Recommended next cluster: `request_body_processor / multipart_files / xml_processor`
- Reason: high combined volume, but likely multiple true processor gaps

## Guardrail Notes

- No Expected statuses, testcase rules, request bodies, MRTS definitions, or PASS/FAIL values are changed by this analysis.
- The selected subcluster is metadata-only and remains a runtime FAIL; it is no longer counted as body-processor work.
- Remaining Body/XML/Multipart rows need narrower connector/native comparisons before connector-core changes.
