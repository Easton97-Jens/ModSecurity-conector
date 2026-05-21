Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Summary

## Kurzstatus
- Gesamtzahl aller YAML Cases: **133**
- verified/pass (`runtime_verified=true`): **0**
- xfail: **79**
- pending-runtime-verification (`runtime_verified=false`): **86**
- pending-runtime-verification (`runtime_verified=unknown`): **47**
- connector-gap: **11**
- runtime-difference: **13**
- future/experimental: **16**
- RESPONSE_BODY Cases: **19**
- default runtime-executable YAML Cases: **54**
- force-all runtime-executable YAML Cases: **133**
- Apache attempted YAML Cases in latest runtime snapshot: **126**
- NGINX attempted YAML Cases in latest runtime snapshot: **133**
- mapped-only import inventory entries: **10**

**RESPONSE_BODY ist nicht verified/promoted.** Diese Datei ist generiertes Reporting und keine Runtime-Evidenz.

## Framework Integration
- Framework root used for shared cases/tools: `FRAMEWORK_ROOT`.
- Connector root used for adapter inventory/reports: `CONNECTOR_ROOT`.
- Common YAML cases, runners, normalizers, and generators are owned by `ModSecurity-test-Framework`.
- Connector-specific cases, adapter metadata, harnesses, import status, and generated reports are owned by this connector repository.
- `FRAMEWORK_ROOT` is configurable and may point at a module/submodule or another explicit checkout; there is no absolute workspace fallback.

## Testarten
- Common YAML Cases: **126**
- Apache-specific Cases: **0**
- NGINX-specific Cases: **7**
- xfail Cases: **79**
- mapped-only import inventory entries: **10** (nicht als runnable YAML Cases gezählt)
- runtime-blocked import inventory entries: **0** (belegte Harness-/Umgebungsblocker, keine PASS- oder XFAIL-Promotion)
- pending/future compatibility Cases: **16** future/experimental; **133** nicht runtime-verified

## Statusklassen
| Status | Count |
|---|---:|
| imported | 47 |
| unknown | 7 |
| xfail | 79 |

## Scope
| Scope | Count |
|---|---:|
| common | 126 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Coverage nach Variablen/Collections
| Variable / Collection | Count |
|---|---:|
| `ARGS` | 43 |
| `ARGS_NAMES` | 7 |
| `REQUEST_HEADERS` | 4 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `REQUEST_COOKIES` | 2 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `REQUEST_URI` | 7 |
| `REQUEST_BODY` | 10 |
| `FILES` | 2 |
| `FILES_NAMES` | 2 |
| `XML` | 5 |
| `RESPONSE_HEADERS` | 10 |
| `RESPONSE_BODY` | 19 |
| `AUDIT_LOG` | 0 |

## Coverage nach Phase
| Phase | Count |
|---|---:|
| Phase 1 | 35 |
| Phase 2 | 69 |
| Phase 3 | 11 |
| Phase 4 | 19 |

## Coverage nach Themen
| Topic | Count |
|---|---:|
| Operators | 128 |
| Transformations | 28 |
| Multipart / FILES | 11 |
| JSON | 7 |
| XML | 5 |
| Unicode / Encoding | 16 |
| XSS-like compatibility probes | 2 |
| SQLi-like compatibility probes | 2 |
| Audit-log probes | 12 |
| Response header probes | 10 |
| Response body experimental probes | 2 |

## Runtime Matrix Status
| Status | Apache | NGINX |
|---|---:|---:|
| PASS | 48 | 54 |
| XFAIL_PASS | 16 | 16 |
| XFAIL_FAIL | 20 | 21 |
| PENDING_FAIL | 1 | 1 |
| FUTURE_PASS | 7 | 7 |
| FUTURE_FAIL | 9 | 9 |
| CONNECTOR_GAP_PASS | 4 | 5 |
| CONNECTOR_GAP_FAIL | 7 | 6 |
| RUNTIME_DIFFERENCE_PASS | 6 | 6 |
| RUNTIME_DIFFERENCE_FAIL | 8 | 8 |
| NOT_EXECUTABLE | 7 | 0 |
| MAPPED_ONLY | 10 | 10 |

- Apache attempted YAML cases from latest summary: **126**
- NGINX attempted YAML cases from latest summary: **133**
- Apache raw runtime XFAIL observations from latest summary: **0**
- NGINX raw runtime XFAIL observations from latest summary: **0**
- Apache NOT EXECUTED YAML rows: **0**
- NGINX NOT EXECUTED YAML rows: **0**
- Apache NOT_EXECUTABLE YAML rows: **7**
- NGINX NOT_EXECUTABLE YAML rows: **0**
- mapped-only import inventory entries: **10**
- Runtime Matrix Detail: `docs/testing/generated/runtime-matrix.generated.md`
- Apache per-case results: `docs/testing/generated/apache-runtime-results.generated.md`
- NGINX per-case results: `docs/testing/generated/nginx-runtime-results.generated.md`
- PASS/BLOCKED/FAIL counts here come only from tracked runtime snapshot evidence; xfail/pending cases are not promoted.
- RESPONSE_BODY remains non-verified even when a pass-through runtime case returns HTTP 200.

## Latest Local Runtime Validation Snapshot
- Snapshot: **2026-05-21** (2026-05-21 18:02:19 CEST)
- Git: branch `master`, commit `aea6d52`
- BUILD_ROOT: `/root/.local/state/ModSecurity-conector-build`
- This is a manual local runtime snapshot rendered from tracked snapshot data and local smoke summary files.
- Runtime matrix snapshot generated from local Apache and NGINX smoke summary JSON files.
- Per-case PASS/FAIL/BLOCKED/XFAIL values are runtime evidence for this local run only.
- No xfail/pending YAML case is promoted by this snapshot.
- RESPONSE_BODY remains non-verified/non-promoted, including pass-through response-body probes.
- Mapped-only import inventory entries remain visible but are not executed runtime cases.
- make smoke-all is not implied by separate Apache/NGINX runtime matrix runs.

## Framework Check Status
| Command | Status | Details |
|---|---|---|
| make setup-dev | PASS | Development dependencies available in .venv |
| make lint | PASS | Repository lint checks passed |
| make generate-test-matrix | PASS | Generated coverage docs refreshed from current metadata |
| make check-test-matrix | PASS | Generated coverage docs matched generator output after staging generated docs |
| make quick-check | PASS | Lightweight framework checks passed |
| make cloud-quick-check | PASS | Framework/generator-only cloud check passed |
| .venv/bin/python -m py_compile modules/ModSecurity-test-Framework/tests/normalizers/*.py modules/ModSecurity-test-Framework/tests/runners/*.py modules/ModSecurity-test-Framework/ci/*.py | PASS | Framework Python files compiled through the connector module path |
| sh -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | POSIX shell syntax check passed for connector integration shell scripts |
| bash -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | Bash syntax check passed for connector integration shell scripts |
| git diff --check | PASS | No whitespace errors reported |
| diff -u /tmp/pre-connector.diff /tmp/post-connector.diff | PASS | Connector source diff snapshot is unchanged; no new connector source changes were introduced |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | BLOCKED | Non-zero because connectors/apache/src/mod_security3.c had a pre-existing unrelated local change before this fix; the pre/post connector diff snapshot is unchanged |
| git ls-files .venv | PASS | No tracked .venv files |

## Readiness / Fetch Status
| Command | Status | Details |
|---|---|---|
| make fetch-deps | NOT_RUN | Not rerun during the framework-module migration; runtime-matrix-all used the configured local source tree and build output location |
| optional installed readiness | BLOCKED | System Apache/APXS/NGINX/libmodsecurity readiness remains diagnostic only and is not required for source-build smokes |
| make runtime-matrix-all | PASS | Force-all matrix orchestration completed and recorded Apache/NGINX per-case evidence; expected runtime FAILs remain evidence and are not PASS promotions |

## Runtime Smoke Status
| Command | Status | Exit | PASS | FAIL | BLOCKED | XFAIL | Evidence |
|---|---|---|---|---|---|---|---|
| FORCE_ALL_CASES=1 REFRESH=1 make smoke-apache | FAIL | 2 | 81 | 45 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/apache-summary.json |
| FORCE_ALL_CASES=1 REFRESH=1 make smoke-nginx | FAIL | 2 | 88 | 45 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/nginx-summary.json |
| REFRESH=1 make smoke-all | NOT_RUN | not_run | unknown | unknown | unknown | unknown | not available |

## Runtime FAIL Details
| Connector | Case | Expected | Actual | Assessment |
|---|---|---|---|---|
| apache | duplicate_args_encoded_separator_edge | 403 | 200 | runtime summary reported non-pass |
| apache | duplicate_header_case_normalization_gap | 403 | 200 | runtime summary reported non-pass |
| apache | edge_semicolon_query_args_names | 403 | 200 | runtime summary reported non-pass |
| apache | files_empty_part_future_compatibility | 403 | None | runtime summary reported non-pass |
| apache | files_names_mixed_case_filename_gap | 403 | 200 | runtime summary reported non-pass |
| apache | json_empty_body_future_compatibility | 403 | None | runtime summary reported non-pass |
| apache | multipart_duplicate_field_names_gap | 403 | 200 | runtime summary reported non-pass |
| apache | multipart_empty_filename_connector_gap | 403 | None | runtime summary reported non-pass |
| apache | parser_xml_partial_body_future_target | 403 | 200 | runtime summary reported non-pass |
| apache | phase1_vs_phase2_request_body_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_content_type_charset_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_duplicate_value_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_encoded_value_future_target | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_location_encoded_runtime_diff | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_mixed_case_connector_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_multi_value_connector_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase3_response_headers_server_presence_pending | 200 | None | runtime summary reported non-pass |
| apache | phase3_response_headers_set_cookie_multi_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_auditlog_outbound_escaped_value_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_auditlog_outbound_matched_var_future | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_auditlog_outbound_message_connector_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_auditlog_outbound_multiline_section_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_auditlog_outbound_rule_id_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_response_body_buffering_order_future_target | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_response_body_chunk_assumption_connector_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_response_body_compressed_assumption_experimental | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_response_body_empty_future_target | 403 | None | runtime summary reported non-pass |
| apache | phase4_response_body_html_entity_decode_gap | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_response_body_html_text_normalization_probe | 403 | 200 | runtime summary reported non-pass |
| apache | phase4_response_body_unicode_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | response_body_basic_block | 403 | 200 | runtime summary reported non-pass |
| apache | response_headers_multi_value_runtime_gap | 403 | 200 | runtime summary reported non-pass |
| apache | sqli_like_keyword_spacing_probe | 403 | 200 | runtime summary reported non-pass |
| apache | sqli_like_quote_encoding_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | tfn_chain_lowercase_trim_pass_through | 200 | 0 | runtime summary reported non-pass |
| apache | unicode_double_encoded_uri_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | unicode_whitespace_normalization_gap | 403 | 200 | runtime summary reported non-pass |
| apache | v2_transformation_url_decode_invalid_sequence_mapped_candidate | 403 | None | runtime summary reported non-pass |
| apache | v3_request_cookies_names_case_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | v3_request_headers_names_lowercase_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| apache | xml_deep_nesting_future_target | 403 | 200 | runtime summary reported non-pass |
| apache | xml_namespace_edge_connector_gap | 403 | 200 | runtime summary reported non-pass |
| apache | xml_request_body_malformed_connector_gap | 403 | 200 | runtime summary reported non-pass |
| apache | xss_like_encoded_angles_normalization_probe | 403 | 200 | runtime summary reported non-pass |
| apache | xss_like_mixed_case_script_token_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | duplicate_args_encoded_separator_edge | 403 | 200 | runtime summary reported non-pass |
| nginx | duplicate_header_case_normalization_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | edge_semicolon_query_args_names | 403 | 200 | runtime summary reported non-pass |
| nginx | files_empty_part_future_compatibility | 403 | None | runtime summary reported non-pass |
| nginx | files_names_mixed_case_filename_gap | 403 | 405 | runtime summary reported non-pass |
| nginx | json_empty_body_future_compatibility | 403 | None | runtime summary reported non-pass |
| nginx | multipart_duplicate_field_names_gap | 403 | 405 | runtime summary reported non-pass |
| nginx | multipart_empty_filename_connector_gap | 403 | None | runtime summary reported non-pass |
| nginx | nginx_phase4_strict_connection_abort | 403 | 0 | runtime summary reported non-pass |
| nginx | parser_xml_partial_body_future_target | 403 | 405 | runtime summary reported non-pass |
| nginx | phase1_vs_phase2_request_body_gap | 403 | 405 | runtime summary reported non-pass |
| nginx | phase3_response_headers_content_type_charset_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase3_response_headers_duplicate_value_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | phase3_response_headers_encoded_value_future_target | 403 | 200 | runtime summary reported non-pass |
| nginx | phase3_response_headers_location_encoded_runtime_diff | 403 | 200 | runtime summary reported non-pass |
| nginx | phase3_response_headers_multi_value_connector_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase3_response_headers_server_presence_pending | 200 | None | runtime summary reported non-pass |
| nginx | phase3_response_headers_set_cookie_multi_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_auditlog_outbound_escaped_value_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_auditlog_outbound_matched_var_future | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_auditlog_outbound_message_connector_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_auditlog_outbound_multiline_section_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_auditlog_outbound_rule_id_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_response_body_buffering_order_future_target | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_response_body_chunk_assumption_connector_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_response_body_compressed_assumption_experimental | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_response_body_empty_future_target | 403 | None | runtime summary reported non-pass |
| nginx | phase4_response_body_html_entity_decode_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_response_body_html_text_normalization_probe | 403 | 200 | runtime summary reported non-pass |
| nginx | phase4_response_body_unicode_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | response_body_basic_block | 403 | 200 | runtime summary reported non-pass |
| nginx | response_headers_multi_value_runtime_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | sqli_like_keyword_spacing_probe | 403 | 200 | runtime summary reported non-pass |
| nginx | sqli_like_quote_encoding_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | tfn_chain_lowercase_trim_pass_through | 200 | 0 | runtime summary reported non-pass |
| nginx | unicode_double_encoded_uri_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | unicode_whitespace_normalization_gap | 403 | 200 | runtime summary reported non-pass |
| nginx | v2_transformation_url_decode_invalid_sequence_mapped_candidate | 403 | None | runtime summary reported non-pass |
| nginx | v3_request_cookies_names_case_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | v3_request_headers_names_lowercase_runtime_difference | 403 | 200 | runtime summary reported non-pass |
| nginx | xml_deep_nesting_future_target | 403 | 405 | runtime summary reported non-pass |
| nginx | xml_namespace_edge_connector_gap | 403 | 405 | runtime summary reported non-pass |
| nginx | xml_request_body_malformed_connector_gap | 403 | 405 | runtime summary reported non-pass |
| nginx | xss_like_encoded_angles_normalization_probe | 403 | 200 | runtime summary reported non-pass |
| nginx | xss_like_mixed_case_script_token_gap | 403 | 200 | runtime summary reported non-pass |

## Runtime Verified Status
- Runtime matrix records current local Apache and NGINX per-case smoke evidence.
- PASS in this snapshot means the case was executed by that connector's smoke harness and matched the case expectation in the summary JSON.
- XFAIL, pending, connector-gap, runtime-difference, future, and mapped-only inventory are not promoted by this snapshot.
- FORCE_ALL_CASES=1 attempts xfail/pending/future/gap YAML cases where they are applicable to the connector.
- RESPONSE_BODY remains non-verified/non-promoted.
- make smoke-all was not run by runtime-matrix; full-smoke PASS counts remain unknown.

## Offene Runtime-Probleme
- Mapped-only import inventory entries are not executable YAML runtime cases.
- XFAIL/pending/future/connector-gap/runtime-difference cases require separate evidence before any status change.
- RESPONSE_BODY remains experimental/non-verified.

## Offene Bereiche / Gaps
- Runtime verification pending: Cases mit `runtime_verified=false` oder `runtime_verified=unknown` sind nicht als Runtime-PASS zu lesen.
- RESPONSE_BODY non-verified: RESPONSE_BODY bleibt nicht promoted, auch wenn Reporting Cases erfasst.
- GitHub/Codex checks sind absichtlich leichtgewichtig und liefern keine Runtime-Kompatibilitaetsbeweise.
- XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.
- Runtime-blocked Import-Einträge sind belegte Harness-/Umgebungsblocker und keine Connector-Gap- oder Runtime-Difference-Promotion.
- `installed-readiness` ist Komponenten-Erkennung/Readiness, keine Runtime-Ausführung.
- Es gibt keinen separaten Artefakt-Reuse-Smoke-Pfad; Runtime-Validierung erfolgt per frischem Source-Build.
- `make smoke-all` bleibt die autoritative Quelle für echte Runtime-PASS-Zahlen.

## Kommandos
- `make quick-check`
- `make quick-all`
- `make cloud-quick-check`
- `make installed-readiness`
- `make runtime-matrix`
- `make runtime-matrix-all`
- `make smoke-apache`
- `make smoke-nginx`
- `make smoke-all`
- `make generate-test-matrix`
- `make check-test-matrix`

## Detaildokumente
- `docs/testing/test-coverage-overview.md`
- `docs/testing/generated/case-matrix.generated.md`
- `docs/testing/generated/coverage-summary.generated.md`
- `docs/testing/generated/xfail-summary.generated.md`
- `docs/testing/generated/connector-gap-summary.generated.md`
- `docs/testing/generated/phase-coverage.generated.md`
- `docs/testing/generated/runtime-matrix.generated.md`
- `docs/testing/generated/apache-runtime-results.generated.md`
- `docs/testing/generated/nginx-runtime-results.generated.md`
- `docs/testing/runtime-validation-snapshot.json`
- `docs/testing/nginx-runtime-failure-classification.md`
- `docs/testing/response-body-blocking-investigation.md`
- `docs/testing/compatibility.md`

## Wichtiger Hinweis
Generated coverage != runtime evidence.
Full runtime validation is local.
GitHub/Codex checks are intentionally lightweight.
XFAIL/pending/gap cases need local runtime validation.
Die generierte Coverage-Dokumentation ist Reporting. Sie ersetzt keine Runtime-Evidenz.
Full runtime validation ist lokal; GitHub/Codex checks sind absichtlich leichtgewichtig.
XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.
`make smoke-all` bleibt die autoritative Quelle für echte PASS-Zahlen.
Keine PASS-Zahlen werden aus dieser Datei abgeleitet, wenn `make smoke-all` nicht vollständig lief.
Keine RESPONSE_BODY-Promotion ohne stabile Full-Smoke-Runtime-Evidenz.
