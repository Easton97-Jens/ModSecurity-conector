> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:27Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Ziel erstellen: `generate-remaining-failure-analysis`
> Besitzer: `connector`
> Schweregrad: `important`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `stale`

# Verbleibende Full-Matrix-Fehleranalyse

**Sprache:** [English](remaining-failure-analysis.generated.md) | Deutsch

Erstellt unter: `2026-06-19T16:58:27Z`

## Umfang
- Der Connector-Vollmatrixbeweis ist vom nativen MRTS-Infrastrukturbeweis getrennt.
- Native Apache/NGINX-Nachweise werden in den `mrts-native-*`-Berichten gemeldet und ersetzen nicht die Connector-PASS/FAIL-Werte.
- Native `100003-1` bleibt als `native_modsecurity_semantics / phase4_native_limitation` klassifiziert.
- Dieser Bericht dient nur der Analyse; Laufzeit PASS/FAIL und erwartete Status werden durch Klassifizierungsmetadaten nicht geändert.

## Zusammenfassung
- Attempted/pass/fail/blocked/not ausführbare Datei: **3928 / 3157 / 771 / 0 / 0**
- Ausstehende Metadatenzeilen beobachtet: **2298**
- Eindeutige verbleibende Fehlerfälle: **118**
- MRTS importierte Connector-Fehler: **0**
- Nicht-MRTS-Framework-Fehler: **771**

## Regressionsprüfungen
| Check | Status | Count | Cases |
|---|---|---|---|
| Unexpected BLOCKED entries | clear | 0 | - |
| Apache expected 200 -> actual 404 | clear | 0 | - |
| HAProxy expected 200 -> actual 501 | clear | 0 | - |
| NGINX actual status 500 | clear | 0 | - |
| MRTS classification incomplete | clear | 0 | - |

## Kategorie-Rollup
| Category | Count | Connectors | Fixable | Risk | Next step |
|---|---|---|---|---|---|
| with_mrts_detection_only_non_disruptive | 519 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay makes disruptive request-side rules non-blocking | low; report-only and not a connector blocking bug | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 72 | apache, nginx | fixable only through real strict abort/log evidence, not status-only changes | high if promoted without transport proof | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay suppresses disruptive action | low; report-only if kept separate from PASS promotion | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| phase4_connector_gap | 42 | apache, haproxy, nginx | connector capability gap unless a real abort mechanism is implemented and evidenced | high if faked; low if reported as gap | document connector gap unless implementation can prove a real hard abort |
| collection_name_normalization_semantics | 30 | apache, haproxy, nginx | metadata-only semantic split; needs native/libmodsecurity comparison before any fix | medium to high | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| xml_processor_activation_missing | 18 | apache, haproxy, nginx | classification-only; XML body exists but the fixture does not enable the XML request body processor | low if kept report-only; high if treated as connector runtime evidence | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| transformation_semantics | 12 | apache, haproxy, nginx | not a harness quick win; needs semantic comparison against libmodsecurity expectations | high | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| multipart_files | 6 | apache, haproxy, nginx | possibly fixable; likely connector/body parser evidence work | medium | compare multipart variable population across connectors with one representative request |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | classification-only; nolog/pass rule is absent from audit evidence and CRS noise is unrelated | low; no runtime or expected-status change | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report-only unless the case is meant to exercise strict hard abort | low if reported honestly, high if promoted as hard abort | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |

## Top 10 Gesamtfehlercluster
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 60 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 42 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top 10 Apache-Cluster
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | apache / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 20 | apache / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 16 | apache / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 16 | apache / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | apache / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 14 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 14 | apache / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | apache / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | apache / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top 10 NGINX Cluster
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 30 | nginx / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 24 | nginx / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 22 | nginx / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | - | - |
| 20 | nginx / phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 20 | nginx / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 16 | nginx / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 16 | nginx / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |

## Top 10 HAProxy-Cluster
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | haproxy / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | haproxy / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 20 | haproxy / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 16 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 16 | haproxy / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 16 | haproxy / phase4_connector_gap / response-body / phase:4 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | haproxy / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top MRTS Importierte Fehler
- Keine.

## Die häufigsten Fehler im Nicht-MRTS-Framework
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 60 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 42 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Die häufigsten Phase4-/Response-Body-Fehler
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 28 | phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 22 | phase4_connector_gap / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_chunk_assumption_connector_gap | - | - |
| 20 | phase4_connector_gap / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_message_connector_gap | - | - |
| 6 | phase4_log_only_no_abort / response-body / phase:4 / 200→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_content_type_out_of_scope | - | - |

## Die häufigsten Interventions-/Blockierungsfehler
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 60 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 42 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Die häufigsten Cross-Connector-Fehler
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 12 | duplicate_args_encoded_separator_edge | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4608 | ARGS_NAMES |
| 12 | duplicate_header_case_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4607 | REQUEST_HEADERS_NAMES |
| 12 | edge_semicolon_query_args_names | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4513 | ARGS_NAMES |
| 12 | files_empty_part_future_compatibility | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_files | {'403→200': 12} | 4706 | FILES |
| 12 | parser_xml_partial_body_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor_activation_missing | {'403→200': 12} | 4610 | XML |
| 12 | unicode_double_encoded_uri_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4707 | REQUEST_URI |
| 12 | unicode_whitespace_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4708 | ARGS:q |
| 12 | v3_request_cookies_names_case_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4403 | REQUEST_COOKIES_NAMES |
| 12 | v3_request_headers_names_lowercase_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4401 | REQUEST_HEADERS_NAMES |
| 12 | xml_deep_nesting_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor_activation_missing | {'403→200': 12} | 4712 | XML |

## Die häufigsten Nur-Connector-Fehler
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 2 | nginx_phase4_content_type_out_of_scope | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | - | - |
| 2 | nginx_phase4_minimal_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | - | - |
| 2 | nginx_phase4_safe_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | - | - |
| 2 | nginx_phase4_strict_connection_abort | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→200': 2} | - | - |
| 2 | nginx_redirect_phase1_302 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | {'302→200': 2} | - | - |
| 2 | nginx_tx_scoring_absolute_block | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | {'403→200': 2} | - | - |
| 2 | nginx_tx_scoring_iterative_block | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | {'403→200': 2} | - | - |

## Empfehlung
- Empfohlener nächster Fix-Cluster: `multipart_files`
- Begründung: Die verbleibende aktive Body-Prozessor-Arbeit ist jetzt nur noch mehrteilig, nachdem URL-codiert und XML Metadaten aufgeteilt wurden
- Nicht als nächstes bearbeiten: `phase4_hard_abort_capability`, weil Transportabbruchnachweis plus Phase-4-Interventionsprotokolle erforderlich sind; Nicht mit Expected/PASS Änderungen lösen.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil große Anzahl, aber wahrscheinlich semantisch; erfordert native/libmodsecurity Vergleich vor Korrekturen.
- Nicht als nächstes bearbeiten: `nolog_expected_no_audit`, weil nur Klassifizierung: explizites Nolog bedeutet, dass die Übereinstimmungsregel keine Prüfnachweise ausgeben sollte.
- Nicht als nächstes bearbeiten: `response_header_mrts_detection_only`, weil Classification-only: with-MRTS DetectionOnly Overlay unterdrückt störende Phase-3-Aktion.
- Nicht als nächstes bearbeiten: `with_mrts_detection_only_non_disruptive`, weil Classification-only: with-MRTS DetectionOnly Overlay unterdrückt störende anforderungsseitige Aktionen.
- Nicht als nächstes bearbeiten: `secaction_detection_only_overlay`, weil Classification-only: with-MRTS DetectionOnly Overlay unterdrückt störende SecAction-Eingriffe.
- Nicht als nächstes bearbeiten: `xml_processor_activation_missing`, da nur Klassifizierung: XML Body und Content-Type existieren, aber diese Fixtures aktivieren ctl:requestBodyProcessor=XML nicht.
- Nicht als nächstes bearbeiten: `multipart_processor_activation_missing`, da nur Klassifizierung: mehrteiliger Körper, Inhaltstyp und Grenze vorhanden sind, diese Vorrichtungen jedoch keinen Zugriff auf den Anforderungskörper ermöglichen, bevor FILES/ARGS_NAMES-Sammlungen erwartet werden.
- Nicht als nächstes bearbeiten: `collection_name_normalization_semantics`, weil metadata-only: geladene Regeln haben keine Übereinstimmungsnachweise; benötigt native/libmodsecurity Vergleich vor Laufzeitkorrekturen.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `6d5df1521cb6cfe501824c42c2268704efba9b4f8650b1a3b7f5e118a95fdeda` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `aa606baae6319f5ab44951ed86fd5e3f7990feb4937b026e5b45258486319def` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `8b8298f135b70c6487dcfbae620801fc09fabe03e73c91fe8657a27505216bce` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `a628c7910973dfe3ea2379d1de447632bb7a68bc93945814d7e5922711b01933` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `dcb7aea74fa53c58425123bf580dbe52ae9898bbc0af29bd38ee98925848c833` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: connector_sha differs |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | stale | generated report input is stale: connector_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
