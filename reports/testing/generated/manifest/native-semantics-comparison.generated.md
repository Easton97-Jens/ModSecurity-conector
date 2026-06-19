> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:45:44Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-native-case-comparison.py`
> Make target: `generate-native-semantics-comparison`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
> Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
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

| Case | Native Actual | Connector Actuals | Native Match | Decision | Classification Hint | Full-Matrix Refresh Needed |
| --- | --- | --- | --- | --- | --- | --- |
| phase4_auditlog_outbound_message_connector_gap | 200 | apache:no-crs/with-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics | no |

## Reclassified

_No rows available. Reason: no current official rows are classified from native semantics evidence._

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
| Declared input | `ci/run-native-case-comparison.py` | `c62686d446b5b50102d78a03509fb6883b7a084d975684fb5e1b809473c726de` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `ci/native_modsecurity_oracle.c` | `57bcb4e66611f597b623599680807795296193e156d4bd91c694422f9eb0f9db` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `682daa5f4a31c9630b61a6bb5cc29090283acfdbfe6c37a3da83ce0008e437e1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/response/body/phase4_auditlog_outbound_message_connector_gap.yaml` | `8a7afb18ab9f7913b8bb10fe4f3b55c912e9e42e7da9ed2d1065841caf2f434a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260619T164544Z-phase4_auditlog_outbound_message_connector_gap/native-case-run.json` | `47b29058ed2f33405045eeb42a941d54242fa599247763b49de11e8a516926a6` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `ci/run-native-case-comparison.py` | present | input file available |
| `ci/native_modsecurity_oracle.c` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/response/body/phase4_auditlog_outbound_message_connector_gap.yaml` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260619T164544Z-phase4_auditlog_outbound_message_connector_gap/native-case-run.json` | present | input file available |
