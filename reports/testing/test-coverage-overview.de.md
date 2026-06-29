Generierte Datei – nicht manuell bearbeiten.

# Übersicht über die ModSecurity Connector-Testabdeckung

**Sprache:** [English](test-coverage-overview.md) | Deutsch

## Zusammenfassung
- Gesamtzahl der Fälle: **141**
- Verified/pass Anzahl (`runtime_verified=true`): **0**
- Aktuelle XFAIL-Anzahl: **0**
- Frühere XFAIL-Fälle verfolgt: **80**
- Anzahl der ausstehenden Laufzeitüberprüfungen: **11**
- Anzahl der Verbindungslücken: **11**
- Anzahl der Laufzeitunterschiede: **13**
- Future/experimental Anzahl: **17**
- RESPONSE_BODY Fälle: **24** (immer noch **nicht verified/promoted**)
- Nur zugeordnete Importinventareinträge: **10**

## Abdeckung nach Variable/Sammlung
| Variable | Count |
|---|---:|
| `RESPONSE_BODY` | 20 |
| `ARGS:q` | 18 |
| `REQUEST_BODY` | 10 |
| `REQUEST_URI` | 7 |
| `ARGS_NAMES` | 6 |
| `ARGS:test` | 6 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `ARGS:a` | 4 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `ARGS:param1` | 4 |
| `MULTIPART_FILENAME` | 4 |
| `ARGS` | 4 |
| `RESPONSE_HEADERS:Set-Cookie` | 4 |
| `ARGS:probe` | 4 |
| `XML` | 3 |
| `ARGS:chain_a` | 3 |
| `ARGS:chain_b` | 3 |
| `FILES_NAMES` | 2 |
| `REQUEST_HEADERS:Content-Type` | 2 |
| `XML:/*` | 2 |

## Abdeckung nach Phase
| Phase | Count |
|---|---:|
| 1 | 38 |
| 2 | 75 |
| 3 | 12 |
| 4 | 20 |

## Abdeckung nach Status
| Status | Count |
|---|---:|
| active | 8 |
| imported | 133 |

## Abdeckung nach Umfang
| Scope | Count |
|---|---:|
| common | 134 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Laufzeitmatrixstatus
- Standardmäßige zur Laufzeit ausführbare YAML-Fälle: **61**
- Alle zur Laufzeit ausführbaren YAML-Fälle erzwingen: **141**
- Apache hat YAML-Fälle aus der Standardzusammenfassung versucht: **54**
- NGINX versuchte YAML-Fälle aus der Standardzusammenfassung: **60**
- HAProxy versuchte YAML-Fälle aus der Standardzusammenfassung: **54**
- Apache versuchte YAML-Fälle aus der Force-All-Zusammenfassung: **133**
- NGINX versuchte YAML-Fälle aus der Force-All-Zusammenfassung: **140**
- HAProxy versuchte YAML-Fälle aus der Force-All-Zusammenfassung: **133**
- Apache Force-All Raw-Laufzeit PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **108** / **19** / **0** / **6**
- NGINX Alle rohen Laufzeiten erzwingen PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **74** / **60** / **0** / **6**
- HAProxy Force-All Raw Runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **104** / **23** / **0** / **6**
| Status | Apache | NGINX | HAProxy |
|---|---:|---:|---:|
| PASS | 10 | 10 | 10 |
| FAIL | 44 | 50 | 44 |
| NOT_EXECUTABLE | 87 | 81 | 87 |
| MAPPED_ONLY | 10 | 10 | 10 |
- Details: `reports/testing/generated/runtime/runtime-matrix.generated.md`
- HAProxy-Ergebnisse pro Fall: `reports/testing/generated/runtime/haproxy-runtime-results.generated.md`

## MRTS Nachweis der nativen Infrastruktur
- Apache nativ: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 nativ: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native Zusammenfassung: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Kombinierter nativer Bericht: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Diese nativen MRTS-Berichte sind vom Connector-Vollmatrixbeweis getrennt.

## Status der Framework-Prüfung
| Command | Status | Details |
|---|---|---|
| make setup-dev | PASS | Development dependencies available in .venv |
| make lint | PASS | Repository lint checks passed |
| make generate-test-matrix | PASS | Generated coverage docs refreshed from current metadata |
| make check-test-matrix | FAIL | Exited 2 in this uncommitted working tree because generated reports differ from HEAD after the HAProxy matrix updates |
| make quick-check | PASS | Lightweight framework checks passed |
| make cloud-quick-check | PASS | Framework/generator-only cloud check passed |
| .venv/bin/python -m py_compile modules/ModSecurity-test-Framework/tests/normalizers/*.py modules/ModSecurity-test-Framework/tests/runners/*.py modules/ModSecurity-test-Framework/ci/*.py | PASS | Framework Python files compiled through the connector module path |
| sh -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | POSIX shell syntax check passed for connector integration shell scripts |
| bash -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | Bash syntax check passed for connector integration shell scripts |
| git diff --check | PASS | No whitespace errors reported |
| diff -u /tmp/pre-connector.diff /tmp/post-connector.diff | PASS | Connector source diff snapshot is unchanged; no new connector source changes were introduced |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | BLOCKED | Non-zero because connectors/apache/src/mod_security3.c had a pre-existing unrelated local change before this fix; the pre/post connector diff snapshot is unchanged |
| git ls-files .venv | PASS | No tracked .venv files |

## Bereitschafts-/Abrufstatus
| Command | Status | Details |
|---|---|---|
| make fetch-deps | NOT_RUN | Not rerun during the framework-module migration; runtime-matrix-all used the configured local source tree and build output location |
| optional installed readiness | BLOCKED | System Apache/APXS/NGINX/libmodsecurity readiness remains diagnostic only and is not required for source-build smokes |
| make runtime-matrix-all | PASS | Force-all matrix orchestration completed and recorded Apache/NGINX per-case evidence; expected runtime FAILs remain evidence and are not PASS promotions |

## Runtime-Smoke-Status
- Snapshot: **16.06.2026** (16.06.2026 21:13:26 CEST)
- Git: branch `master`, commit `614c804`
- BUILD_ROOT: `/var/tmp/ModSecurity-conector-verified/build`
- Snapshot-Datei: `reports/testing/runtime-validation-snapshot.json`

### Standardmäßiger Runtime-Smoke-Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| apache | make smoke-apache | FAIL | 2 | 54 | 10 | 44 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json |
| nginx | make smoke-nginx | FAIL | 2 | 60 | 10 | 50 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json |
| haproxy | MODSECURITY_MRTS_VARIANT=with-mrts make smoke-haproxy | FAIL | 2 | 54 | 10 | 44 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| all | REFRESH=1 make smoke-all | NOT_RUN | not_run | 0 | unknown | unknown | unknown | unknown | not available |

### Runtime-Smoke-Status erzwingen
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| apache | FORCE_ALL_CASES=1 make smoke-apache | FAIL | 2 | 133 | 108 | 19 | 0 | 6 | /root/.local/state/ModSecurity-conector-build/results/force-all/apache-summary.json |
| nginx | FORCE_ALL_CASES=1 make smoke-nginx | FAIL | 2 | 140 | 74 | 60 | 0 | 6 | /root/.local/state/ModSecurity-conector-build/results/force-all/nginx-summary.json |
| haproxy | FORCE_ALL_CASES=1 make smoke-haproxy | FAIL | 1 | 133 | 104 | 23 | 0 | 6 | /src/ModSecurity-conector-build/results/force-all/haproxy-summary.json |

## Laufzeitverfügbarkeit des Connectors
| Connector | Status | Build | Per-case results | Attempted cases | Summary evidence | Note |
|---|---|---|---|---:|---|---|
| Apache | FAIL | unknown | available | 54 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only. |
| NGINX | FAIL | unknown | available | 60 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only. |
| HAProxy | FAIL | unknown | available | 54 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json | Default HAProxy evidence is the supported non-former-XFAIL subset of live HAProxy matrix evidence; force-all rows remain separate runtime evidence. |

## Laufzeit FAIL Details

### Apache FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| action_deny_phase1 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_deny_phase2 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | 401 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| audit_log_phase1_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| json_request_body_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=json_request_body_block; status=fail; expected=403; actual=200 |
| multipart_basic_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=200 |
| multipart_filename_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=200 |
| multipart_files_combined_size | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=200 |
| multipart_files_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=200 |
| multipart_files_value_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=200 |
| phase1_header_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| phase2_args_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| pr70_phase1_audit_request_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=200 |
| pr70_phase3_audit_response_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| request_body_args_post_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=200 |
| request_body_json_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_json_block; status=fail; expected=403; actual=200 |
| request_body_raw_text_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=200 |
| request_body_urlencoded_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=200 |
| response_header_basic | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| rule_chain_both_match_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| v2_operator_begins_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=404 |
| v3_args_names_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_auditlog_serial_fields_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=404 |
| v3_operator_pm_digit_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=404 |
| v3_operator_rx_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |
| xml_request_body_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=200 |

### NGINX FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| action_deny_phase1 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_deny_phase2 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | 401 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| audit_log_phase1_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| json_request_body_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=json_request_body_block; status=fail; expected=403; actual=405 |
| multipart_basic_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=405 |
| multipart_filename_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=405 |
| multipart_files_combined_size | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=405 |
| multipart_files_names_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=405 |
| multipart_files_value_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=405 |
| nginx_phase4_content_type_out_of_scope | 200 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_content_type_out_of_scope; status=fail; expected=200; actual=200 |
| nginx_phase4_minimal_log_only | 200 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_minimal_log_only; status=fail; expected=200; actual=200 |
| nginx_phase4_safe_log_only | 200 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_safe_log_only; status=fail; expected=200; actual=200 |
| nginx_redirect_phase1_302 | 302 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_redirect_phase1_302; status=fail; expected=302; actual=200 |
| nginx_tx_scoring_absolute_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_tx_scoring_absolute_block; status=fail; expected=403; actual=200 |
| nginx_tx_scoring_iterative_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_tx_scoring_iterative_block; status=fail; expected=403; actual=200 |
| phase1_header_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| phase2_args_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| pr70_phase1_audit_request_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=405 |
| pr70_phase3_audit_response_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| request_body_args_post_names_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=405 |
| request_body_json_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_json_block; status=fail; expected=403; actual=405 |
| request_body_raw_text_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=405 |
| request_body_urlencoded_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=405 |
| response_header_basic | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| rule_chain_both_match_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| v2_operator_begins_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=404 |
| v3_args_names_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_auditlog_serial_fields_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=404 |
| v3_operator_pm_digit_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=404 |
| v3_operator_rx_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |
| xml_request_body_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=405 |

### HAProxy FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| action_deny_phase1 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_deny_phase2 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | 401 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| audit_log_phase1_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| json_request_body_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=json_request_body_block; status=fail; expected=403; actual=501 |
| multipart_basic_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=501 |
| multipart_filename_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=501 |
| multipart_files_combined_size | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=501 |
| multipart_files_names_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=501 |
| multipart_files_value_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=501 |
| phase1_header_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| phase2_args_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| pr70_phase1_audit_request_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=501 |
| pr70_phase3_audit_response_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| request_body_args_post_names_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=501 |
| request_body_json_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_json_block; status=fail; expected=403; actual=501 |
| request_body_raw_text_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=501 |
| request_body_urlencoded_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=501 |
| response_header_basic | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| rule_chain_both_match_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| v2_operator_begins_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=200 |
| v3_args_names_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_auditlog_serial_fields_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=200 |
| v3_operator_pm_digit_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=200 |
| v3_operator_rx_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |
| xml_request_body_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=501 |

## Laufzeitüberprüfter Status
- Die Laufzeitmatrix zeichnet aktuelle lokale Apache-, NGINX- und HAProxy-Smoke-Nachweise pro Fall auf, sofern verfügbar.
- PASS in diesem Snapshot bedeutet, dass der Fall vom Smoke-Harness dieses Connectors ausgeführt wurde und der Fallerwartung im Summary-JSON entsprach.
- Ausstehender, Connector-Lücke-, Laufzeitdifferenz-, zukünftiger und nur zugeordneter Bestand werden von diesem Snapshot nicht hochgestuft.
- FORCE_ALL_CASES=1 versucht alle materialisierbaren YAML-Fälle, in denen sie auf den Connector anwendbar sind.
- HAProxy PASS ist nur auf Live-HAProxy-Nachweise ausgelegt; Die aktuelle HAProxy-Abdeckung ist eine teilweise anforderungsseitige YAML-Ausführung.
- RESPONSE_BODY bleibt non-verified/non-promoted.
- Laufzeit verstrichen, aber die RESPONSE_BODY-Unterstützung wird dadurch nicht überprüft.
- make Smoke-all wurde nicht von runtime-matrix ausgeführt; Die Anzahl der Full-Smoke-PASS bleibt unbekannt.

## Öffnen Sie Laufzeitprobleme
- Nur zugeordnete Importinventareinträge sind nicht ausführbare YAML Laufzeitfälle.
- Pending/future/connector-gap/runtime-difference-Themen erfordern einen Live-Nachweis vor einem Supportanspruch.
- RESPONSE_BODY bleibt experimental/non-verified.

## Offene Bereiche / Lücken
- Laufzeitverifiziert bedeutet nur Fälle, die explizit als `runtime_verified=true` klassifiziert sind.
- Fälle mit `runtime_verified=false` oder `runtime_verified=unknown` sind kein Laufzeit-PASS-Nachweis.
- Detaillierte Connector-Gap-Einträge finden Sie unter `reports/testing/generated/coverage/connector-gap-summary.generated.md`.
- Phasen-3/4-Fälle sind in `reports/testing/generated/coverage/phase-coverage.generated.md` und in der Laufzeitmatrix sichtbar.
- RESPONSE_BODY bleibt nicht verifiziert und nicht promoted.
- GitHub/Codex-Prüfungen sind absichtlich leichtgewichtig.
- Ausstehende und Lückenthemen erfordern eine lokale Laufzeitvalidierung.
- `make smoke-all` ist nur dann maßgebend, wenn es tatsächlich erfolgreich ausgeführt wurde.

## Befehle
- `make quick-check`
- `make quick-all`
- `make cloud-quick-check`
- `make installed-readiness`
- `make runtime-matrix`
- `make runtime-matrix-all`
- `make runtime-matrix-haproxy`
- `make smoke-apache`
- `make smoke-nginx`
- `make smoke-haproxy`
- `make smoke-all`
- `make generate-test-matrix`
- `make check-test-matrix`

## Detailberichte
- `reports/testing/generated/coverage/case-matrix.generated.md`
- `reports/testing/generated/coverage/coverage-summary.generated.md`
- `reports/testing/generated/coverage/xfail-summary.generated.md`
- `reports/testing/generated/coverage/connector-gap-summary.generated.md`
- `reports/testing/generated/coverage/phase-coverage.generated.md`
- `reports/testing/generated/runtime/runtime-matrix.generated.md`
- `reports/testing/generated/runtime/apache-runtime-results.generated.md`
- `reports/testing/generated/runtime/nginx-runtime-results.generated.md`
- `reports/testing/generated/runtime/haproxy-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`

## Wichtiger Hinweis
Die generierte Abdeckung dient nur der Berichterstattung. Es ist kein Laufzeitbeweis für sich.
Die vollständige Laufzeitvalidierung erfolgt lokal und evidenzbasiert.
GitHub/Codex-Prüfungen sind absichtlich leichtgewichtig.
Ausstehende, zukünftige und Lückenthemen erfordern vor der Heraufstufung eine lokale Laufzeitvalidierung.
`make smoke-all` ist nur dann maßgebend, wenn es tatsächlich erfolgreich ausgeführt wurde.
Aus dieser Datei werden keine PASS-Nummern abgeleitet, wenn `make smoke-all` nicht erfolgreich ausgeführt wurde.
Phase 4 / RESPONSE_BODY bleibt nicht promoted; Begrenzte strikte Abbruchbeweise werden nur als Runtime-Nachweise gemeldet.
