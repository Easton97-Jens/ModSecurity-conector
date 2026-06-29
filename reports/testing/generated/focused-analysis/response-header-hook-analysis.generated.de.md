> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:16Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-response-header-hook-analysis.py`
> Ziel erstellen: `generate-response-header-hook-analysis`
> Besitzer: `connector`
> Schweregrad: `informational`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Antwort-Header-Hook-Analyse

**Sprache:** [English](response-header-hook-analysis.generated.md) | Deutsch

Generierte Datei – nicht manuell bearbeiten.

## Umfang
- Antwort-Header FAIL Zeilen analysiert: **60**
- Antwortheader PASS Steuerzeilen: **84**
- Konnektoren: Apache, Haproxy, Nginx
- Varianten: no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts
- Phasen: 3

## Klassifizierung
- `response_header_hook` vorher: **60**
- `response_header_hook` nach: **0**
- Backend/header Setup: **0**
- HAProxy Set-Cookie-Mehrwertlücke: **0**
- MRTS DetectionOnly-Overlay: **60**

## Grundursache
- Apache, NGINX und HAProxy verfügen jetzt über No-MRTS-PASS-Kontrollen für die deterministische Antwort-Header-Blockierung, einschließlich spezieller Content-Type-, Location- und Set-Cookie-Probes.
- HAProxy bewahrt wiederholte `Set-Cookie`-Antwortheader über den binären SPOE-Antwortheader-Argumentpfad; Der text/scalar-Fallback bleibt nur ein sekundärer Nachweis.
- `with-mrts` Zeilen, die ansonsten in No-MRTS übergeben werden, werden durch das DetectionOnly-Steuerelement auf Transaktionsebene der MRTS-Init-Regel unterdrückt. Dies ist nur eine Klassifizierung und keine Connector-PASS-Aktion.

## PASS Steuerelemente
| Connector | Variant | Case | Rule | Header | Expected | Actual |
|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | Set-Cookie | 403 | 403 |
| apache | no-crs/no-mrts | phase3_response_headers_server_presence_pending | 4901 | Server | 200 | 200 |
| apache | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | Set-Cookie | 403 | 403 |
| apache | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| apache | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| apache | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | phase3_response_headers_server_presence_pending | 4901 | Server | 200 | 200 |
| nginx | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | Set-Cookie | 403 | 403 |
| nginx | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| nginx | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| nginx | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_content_type_charset_gap | 4902 | Content-Type | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_encoded_value_future_target | 4804 | Location | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | Location | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| haproxy | no-crs/no-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | content-type | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | phase3_response_headers_server_presence_pending | 4901 | Server | 200 | 200 |
| haproxy | no-crs/no-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | Set-Cookie | 403 | 403 |
| haproxy | no-crs/no-mrts | pr70_phase3_audit_response_header | 5703 | Last-Modified | 403 | 403 |
| haproxy | no-crs/no-mrts | response_header_basic | 1301 | Last-Modified | 403 | 403 |
| haproxy | no-crs/no-mrts | response_headers_multi_value_runtime_gap | 4410 | Set-Cookie | 403 | 403 |
| apache | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| apache | no-crs/with-mrts | phase3_response_headers_server_presence_pending | 4901 | Server | 200 | 200 |
| nginx | no-crs/with-mrts | phase3_response_headers_missing_pass_through | 4801 | X-Missing | 200 | 200 |
| nginx | no-crs/with-mrts | phase3_response_headers_server_presence_pending | 4901 | Server | 200 | 200 |

## Fehlergruppen
| Count | Connector | Header | Classification | Phase | Expected | Actual | Example |
|---|---|---|---|---|---|---|---|
| 8 | apache | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 8 | haproxy | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 8 | nginx | Set-Cookie | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_duplicate_value_runtime_difference |
| 4 | apache | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | apache | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 4 | haproxy | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | haproxy | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 4 | nginx | Last-Modified | response_header_mrts_detection_only | 3 | 403 | 200 | pr70_phase3_audit_response_header |
| 4 | nginx | Location | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_encoded_value_future_target |
| 2 | apache | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | apache | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |
| 2 | haproxy | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | haproxy | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |
| 2 | nginx | Content-Type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_content_type_charset_gap |
| 2 | nginx | content-type | response_header_mrts_detection_only | 3 | 403 | 200 | phase3_response_headers_mixed_case_connector_gap |

## Fehlerzeilen
| Connector | Variant | Case | Rule | Target | Expected header | Actual evidence | Backend header set | ModSecurity sees header | Classification |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | no-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule matched | True | True | response_header_mrts_detection_only |
| apache | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| nginx | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type | RESPONSE_HEADERS:Content-Type @contains charset | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_duplicate_value_runtime_difference | 4803 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains a=b | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_encoded_value_future_target | 4804 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_location_encoded_runtime_diff | 4903 | RESPONSE_HEADERS:Location | RESPONSE_HEADERS:Location @contains %2F | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_mixed_case_connector_gap | 4802 | RESPONSE_HEADERS:content-type | RESPONSE_HEADERS:content-type @contains text/html | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | phase3_response_headers_set_cookie_multi_gap | 4904 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains token | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | pr70_phase3_audit_response_header | 5703 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified @rx . | target rule matched | True | True | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | response_header_basic | 1301 | RESPONSE_HEADERS:Last-Modified | RESPONSE_HEADERS:Last-Modified . | target rule missing from logs | True | False | response_header_mrts_detection_only |
| haproxy | with-crs/with-mrts | response_headers_multi_value_runtime_gap | 4410 | RESPONSE_HEADERS:Set-Cookie | RESPONSE_HEADERS:Set-Cookie @contains session | target rule missing from logs | True | False | response_header_mrts_detection_only |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `6c36afa87a2f63eaa9ff2df91e08759b8f657ee9a8090112afcc534174e98e70` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
