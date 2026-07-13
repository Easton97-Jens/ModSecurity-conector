> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:11Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/run-native-case-comparison.py`
> Ziel erstellen: `generate-native-semantics-comparison`
> Besitzer: `manifest`
> Schweregrad: `important`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

<!-- retained-historical-generated-output -->
> Aktueller Refresh-Status: `skipped_stale_input`. Dieser Report bewahrt einen früheren evidenztragenden Snapshot, weil keine neuen verifizierten Eingaben vorliegen. Grund: required generated input is stale.

# Vergleich der nativen Semantik

**Sprache:** [English](native-semantics-comparison.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

## Werkzeuginventar

| Tool/Target | Purpose | Inputs | Outputs | Usable for Single Case? |
| --- | --- | --- | --- | --- |
| tools/MRTS/mrts/generate-rules.py | Generate MRTS rules and go-ftw tests from upstream MRTS YAML definitions. | MRTS config_tests YAML | $BUILD_ROOT/mrts/*/rules and ftw | no; corpus generator |
| framework Makefile mrts-generate/mrts-import/mrts-ftw | Prepare/import MRTS corpora and optionally run go-ftw. | MRTS corpus definitions and infra config | generated framework cases, rules, go-ftw results | not for framework YAML cases |
| ci/run-mrts-native-full.sh | Stage native Apache/NGINX MRTS infra and run the MRTS suite through go-ftw. | MRTS generated corpus, native Apache/NGINX binaries, libmodsecurity | $BUILD_ROOT/mrts-native/*/job.json and logs | no; suite-oriented MRTS evidence |
| framework:ci/generate-mrts-native-report.py | Summarize native MRTS jobs into generated reports. | $MRTS_NATIVE_ROOT/apache2_ubuntu/job.json and nginx-pr24/job.json | reports/testing/generated/mrts-native/*.generated.* | no; summarizes completed native MRTS jobs |
| ci/run-native-case-comparison.py | Run one framework YAML case through connector-free libmodsecurity C API. | framework case YAML, native_modsecurity_oracle.c, libmodsecurity runtime-env | $VERIFIED_RUN_ROOT/native-case-runs/<timestamp>-<case>/ and native-semantics-comparison.generated.* | yes |

## Native Vergleiche

| Case | Native Actual | Connector Actuals | Native Match | Decision | Classification Hint | Full-Matrix Refresh Needed |
| --- | --- | --- | --- | --- | --- | --- |
| unicode_whitespace_normalization_gap | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics | no |
| unicode_double_encoded_uri_runtime_difference | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics | no |
| xml_namespace_edge_connector_gap | 403 | apache:no-crs/with-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/with-mrts=200 | yes | DEFER | common_harness_or_input_issue_possible | no |
| xml_request_body_malformed_connector_gap | 200 | apache:no-crs/no-mrts=200, apache:no-crs/with-mrts=200, apache:with-crs/no-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/no-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/no-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/no-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/no-mrts=200, nginx:with-crs/with-mrts=200 | no | DOCUMENT | likely_framework_expected_behavior_gap_or_libmodsecurity_semantics | no |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | 403 | apache:no-crs/with-mrts=200, apache:with-crs/with-mrts=200, haproxy:no-crs/with-mrts=200, haproxy:with-crs/with-mrts=200, nginx:no-crs/with-mrts=200, nginx:with-crs/with-mrts=200 | yes | DEFER | common_harness_or_input_issue_possible | no |

## Umklassifiziert

| Case | Rows | Classification | Native Actual | Decision |
| --- | --- | --- | --- | --- |
| unicode_whitespace_normalization_gap | 12 | libmodsecurity_transformation_semantics | 200 | DOCUMENT |
| unicode_double_encoded_uri_runtime_difference | 12 | libmodsecurity_transformation_semantics | 200 | DOCUMENT |

## Behoben

_Keine Zeilen verfügbar. Grund: Bei diesem Durchgang wurden nur native Vergleichstools hinzugefügt._

## Aufgeschoben

| Case | Reason |
| --- | --- |
| xml_namespace_edge_connector_gap | common_harness_or_input_issue_possible |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | common_harness_or_input_issue_possible |

## Notizen

- Datenquellenrichtlinie: `verified-inputs-only`.

- Native Vergleichszeilen werden anhand der aktuellen verifizierten Laufzeitinkongruenzanalyse aktualisiert. Es werden keine PASS/FAIL-Werte erfunden.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `ci/run-native-case-comparison.py` | `c62686d446b5b50102d78a03509fb6883b7a084d975684fb5e1b809473c726de` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `ci/native_modsecurity_oracle.c` | `57bcb4e66611f597b623599680807795296193e156d4bd91c694422f9eb0f9db` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `340546dbab42432eef255f99fda65c0d4301db589d6ac5c9f2a201a94326420e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml` | `d712ede8bab7f74851255571299327a0e166e562798e4d5ac64d3a122b45a61d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | `9167164893422a4ebf6587db8d70a96a61f169b49766a2abca2279126459a8d3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/request/uri/unicode_double_encoded_uri_runtime_difference.yaml` | `889068df10e66f52e5f5cbce49d5640be4f55e33ac09bbd21a469826e65a74ec` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | `97a35281bbe37a2d08df5962b766ed71be05dd4dcb0673d275a0596d16650820` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_namespace_edge_connector_gap.yaml` | `b0f83be8f28c6c12030822e625605bac6c53c99e685eb191350159ad852494cf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/native-case-runs/20260618T175942Z-xml_namespace_edge_connector_gap/native-case-run.json` | `9f2741cfa08f9cf813e123da398c973ec1dae1e76a83a8da755aee5ae08fdb92` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_request_body_malformed_connector_gap.yaml` | `7bf2dacc4c5b4de76ccbd33b01fecf0dc598930dd4289497500e40be5816ce88` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/native-case-runs/20260619T063228Z-xml_request_body_malformed_connector_gap/native-case-run.json` | `38964013ce0ab0541e763b0472694e0123e70d8c55e609fb961c290064cee1a5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `modules/ModSecurity-test-Framework/tests/cases/request/uri/v2_transformation_url_decode_invalid_sequence_mapped_candidate.yaml` | `66a559e2c72e40e78dfc04723dfa823f495dbad75789d1e8becc81892be426df` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/native-case-runs/20260618T174441Z-v2_transformation_url_decode_invalid_sequence_mapped_candidate/native-case-run.json` | `a7dae3db2178486d2f0d91702be394aaaa60390a6b3df0654119aac198cdd942` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `ci/run-native-case-comparison.py` | present | input file available |
| `ci/native_modsecurity_oracle.c` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml` | present | input file available |
| `<verified-run-root>/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/request/uri/unicode_double_encoded_uri_runtime_difference.yaml` | present | input file available |
| `<verified-run-root>/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_namespace_edge_connector_gap.yaml` | present | input file available |
| `<verified-run-root>/native-case-runs/20260618T175942Z-xml_namespace_edge_connector_gap/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/body/xml/xml_request_body_malformed_connector_gap.yaml` | present | input file available |
| `<verified-run-root>/native-case-runs/20260619T063228Z-xml_request_body_malformed_connector_gap/native-case-run.json` | present | input file available |
| `modules/ModSecurity-test-Framework/tests/cases/request/uri/v2_transformation_url_decode_invalid_sequence_mapped_candidate.yaml` | present | input file available |
| `<verified-run-root>/native-case-runs/20260618T174441Z-v2_transformation_url_decode_invalid_sequence_mapped_candidate/native-case-run.json` | present | input file available |
