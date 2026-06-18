> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:47:53Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-native-case-comparison.py`
> Make target: `generate-native-semantics-comparison`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Native Semantics Comparison

## Tool Inventory

| Tool/Target | Purpose | Inputs | Outputs | Usable for Single Case? |
| --- | --- | --- | --- | --- |
| tools/MRTS/mrts/generate-rules.py | Generate MRTS rules and go-ftw tests from upstream MRTS YAML definitions. | MRTS config_tests YAML | $BUILD_ROOT/mrts/*/rules and ftw | no; corpus generator |
| framework Makefile mrts-generate/mrts-import/mrts-ftw | Prepare/import MRTS corpora and optionally run go-ftw. | MRTS corpus definitions and infra config | generated framework cases, rules, go-ftw results | not for framework YAML cases |
| ci/run-mrts-native-full.sh | Stage native Apache/NGINX MRTS infra and run the MRTS suite through go-ftw. | MRTS generated corpus, native Apache/NGINX binaries, libmodsecurity | $BUILD_ROOT/mrts-native/*/job.json and logs | no; suite-oriented MRTS evidence |
| framework:ci/generate-mrts-native-report.py | Summarize native MRTS jobs into generated reports. | $MRTS_NATIVE_ROOT/apache2_ubuntu/job.json and nginx-pr24/job.json | reports/testing/generated/mrts-native/*.generated.* | no; summarizes completed native MRTS jobs |
| ci/run-native-case-comparison.py | Run one framework YAML case through connector-free libmodsecurity C API. | framework case YAML, native_modsecurity_oracle.c, libmodsecurity runtime-env | $VERIFIED_RUN_ROOT/native-case-runs/<timestamp>-<case>/ and native-semantics-comparison.generated.* | yes |

## Native Comparisons

| Case | Native Actual | Connector Actuals | Native Match | Decision | Classification Hint |
| --- | --- | --- | --- | --- | --- |
| unicode_whitespace_normalization_gap | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics |
| unicode_double_encoded_uri_runtime_difference | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics |
| xml_namespace_edge_connector_gap | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics |
| xml_request_body_malformed_connector_gap | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | 403 | apache:no-crs/no-mrts=http_status, apache:no-crs/with-mrts=http_status, apache:with-crs/no-mrts=http_status, apache:with-crs/with-mrts=http_status, haproxy:no-crs/no-mrts=http_status, haproxy:no-crs/with-mrts=http_status, haproxy:with-crs/no-mrts=http_status, haproxy:with-crs/with-mrts=http_status, nginx:no-crs/no-mrts=http_status, nginx:no-crs/with-mrts=http_status, nginx:with-crs/no-mrts=http_status, nginx:with-crs/with-mrts=http_status | yes | REFRESH | full_matrix_refresh_needed |

## Reclassified

| Case | Rows | Classification | Native Actual | Decision |
| --- | --- | --- | --- | --- |
| unicode_whitespace_normalization_gap | 12 | libmodsecurity_transformation_semantics | 200 | DOCUMENT |
| unicode_double_encoded_uri_runtime_difference | 12 | libmodsecurity_transformation_semantics | 200 | DOCUMENT |

## Fixed

_No rows available. Reason: this pass added native comparison tooling only._

## Deferred

| Case | Reason |
| --- | --- |
| _No rows available. Reason: no data._ | _No rows available. Reason: no data._ |

## Notes

- Data source policy: `verified-inputs-only`.

- Native comparison rows are refreshed from the current verified runtime mismatch analysis; no PASS/FAIL values are invented.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `ci/run-native-case-comparison.py` | `88f122170fc7625f250d12ccd8590353b4a5e08fbea8b4751c03ae61cb8134ce` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `ci/native_modsecurity_oracle.c` | `57bcb4e66611f597b623599680807795296193e156d4bd91c694422f9eb0f9db` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `06ccc48b304f836f75d06b5343edae8e966492cdc91bb13e3cfef4f62159bc49` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml` | `d712ede8bab7f74851255571299327a0e166e562798e4d5ac64d3a122b45a61d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | `9167164893422a4ebf6587db8d70a96a61f169b49766a2abca2279126459a8d3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/request/uri/unicode_double_encoded_uri_runtime_difference.yaml` | `889068df10e66f52e5f5cbce49d5640be4f55e33ac09bbd21a469826e65a74ec` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | `97a35281bbe37a2d08df5962b766ed71be05dd4dcb0673d275a0596d16650820` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_namespace_edge_connector_gap.yaml` | `37652618368231240de64e7c80bcd405056ccf79ecc3a57fdc6180e2b8f4b438` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-xml_namespace_edge_connector_gap/native-case-run.json` | `f39d89ef54667786d28c009ee065e295effb85ba8fc5314ccd28962932991d27` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_request_body_malformed_connector_gap.yaml` | `3a77f805aa8989e85f9ba512172e0cc13d8eec062874bacef1bb3ed73aeebd4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-xml_request_body_malformed_connector_gap/native-case-run.json` | `07ea67bcf7252f1ad9d1f1695be57baf415501d0e115a74a8121a937b8a8437c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/request/uri/v2_transformation_url_decode_invalid_sequence_mapped_candidate.yaml` | `66a559e2c72e40e78dfc04723dfa823f495dbad75789d1e8becc81892be426df` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T174441Z-v2_transformation_url_decode_invalid_sequence_mapped_candidate/native-case-run.json` | `a7dae3db2178486d2f0d91702be394aaaa60390a6b3df0654119aac198cdd942` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `ci/run-native-case-comparison.py` | present | input file available |
| `ci/native_modsecurity_oracle.c` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/request/uri/unicode_double_encoded_uri_runtime_difference.yaml` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_namespace_edge_connector_gap.yaml` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-xml_namespace_edge_connector_gap/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_request_body_malformed_connector_gap.yaml` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-xml_request_body_malformed_connector_gap/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/request/uri/v2_transformation_url_decode_invalid_sequence_mapped_candidate.yaml` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T174441Z-v2_transformation_url_decode_invalid_sequence_mapped_candidate/native-case-run.json` | present | input file available |
