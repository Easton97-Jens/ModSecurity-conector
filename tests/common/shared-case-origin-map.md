# Shared Case Origin Map

Status: implemented

Only connector-neutral rule/request/expectation fragments are mapped here. The
original Apache::Test and Test::Nginx harness mechanics remain
connector-specific and are not copied.

## Shared Minimal Cases

| Shared case | original_path | source_repo | category | purpose | portable | status | required_capabilities | known_limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `minimal/audit_log_phase1_block.yaml` | `tests/regression/action/10-logging.t`; `tests/modsecurity-config-auditlog.t` | apache/nginx | audit-log | Serial audit log with stable rule/URI/message fields | yes | imported | query args, phase1, audit log | Does not assert volatile audit fields or concurrent audit storage |
| `minimal/phase1_header_block.yaml` | `tests/regression/rule/15-json.t`; `tests/modsecurity.t` | apache/nginx | request-headers | Phase:1 header intervention | yes | imported | request headers, phase1, intervention | Header target adapted to `User-Agent` to avoid JSON parser assumptions |
| `minimal/phase2_args_block.yaml` | `tests/regression/rule/00-basics.t`; `tests/modsecurity.t` | apache/nginx | phase-processing | Phase:2 ARGS intervention | yes | imported | query args, phase2, intervention | Does not assert debug/error log text |
| `minimal/phase2_args_pass.yaml` | `tests/regression/rule/00-basics.t`; `tests/modsecurity.t` | apache/nginx | phase-processing | Non-matching ARGS rule passes through | yes | imported | query args, pass-through | Does not prove allow-listing |
| `minimal/request_body_json_block.yaml` | `tests/regression/rule/15-json.t`; `tests/modsecurity-request-body.t` | apache/nginx | request-body | Raw JSON request-body block | yes | imported | request body, phase2 | Does not require parsed JSON collections |
| `minimal/request_body_urlencoded_block.yaml` | `tests/regression/target/00-targets.t`; `tests/modsecurity-request-body.t` | apache/nginx | request-body | Form body `ARGS_POST` intervention | yes | imported | request body, form urlencoded, phase2 | Does not cover request-body limits or chunking |
| `minimal/response_header_basic.yaml` | `tests/regression/misc/00-phases.t`; `src/ngx_http_modsecurity_header_filter.c` | apache/nginx | response-headers | Basic phase:3 response header intervention | yes | imported | response headers, phase3 | Depends on static response exposing `Last-Modified` |

## Shared Imported Cases

| Shared case | original_path | source_repo | category | purpose | portable | status | required_capabilities | known_limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `imported/action_deny_phase1.yaml` | `tests/regression/action/00-disruptive-actions.t`; `tests/modsecurity.t` | apache/nginx | actions | Unconditional phase:1 deny returns HTTP 403 | yes | imported | phase1, intervention | Does not assert connector log text |
| `imported/action_deny_phase2.yaml` | `tests/regression/action/00-disruptive-actions.t`; `tests/modsecurity.t` | apache/nginx | actions | Unconditional phase:2 deny returns HTTP 403 | yes | imported | phase2, intervention | Does not assert connector log text |
| `imported/action_allow_phase1_pass.yaml` | `tests/regression/action/00-disruptive-actions.t` | apache | actions | Phase:1 allow bypasses later phase:1 deny and reaches origin | yes | imported | phase1, pass-through | Does not assert debug/error log text |
| `imported/collection_args_names_block.yaml` | `tests/regression/target/00-targets.t` | apache | collections | `ARGS_NAMES` query argument name match | yes | imported | query args, collections, phase2 | Converted from log/pass assertion to HTTP intervention assertion |
| `imported/collection_args_get_block.yaml` | `tests/regression/target/00-targets.t`; `tests/modsecurity.t` | apache/nginx | collections | `ARGS_GET` query argument value match | yes | imported | query args, collections, phase2 | Converted from log/pass assertion to HTTP intervention assertion |
| `imported/collection_args_combined_size_block.yaml` | `tests/regression/target/00-targets.t` | apache | collections | `ARGS_COMBINED_SIZE` for two query args | yes | imported | query args, collections, phase2 | Size expectation mirrors the upstream Apache regression value |
| `imported/request_body_args_post_names_block.yaml` | `tests/regression/target/00-targets.t`; `tests/modsecurity-request-body.t` | apache/nginx | request-body | Form body `ARGS_POST_NAMES` match | yes | imported | request body, form urlencoded, collections | Does not cover method matrix or limits |
| `imported/request_body_raw_text_block.yaml` | `tests/modsecurity-request-body.t`; `tests/regression/rule/15-json.t` | nginx/apache | request-body | Raw `REQUEST_BODY` text match | yes | imported | request body, phase2 | Does not cover streaming or chunked body delivery |

## Connector-Specific Imported Cases

| Case | original_path | source_repo | category | purpose | portable | status | target_location | required_capabilities | known_limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `nginx_redirect_phase1_302.yaml` | `tests/modsecurity.t` | nginx | actions | NGINX-observed phase:1 redirect action | no | imported | `tests/nginx/cases/imported/` | query args, phase1, redirect | NGINX-only until Apache equivalence is explicitly tested |
| `nginx_tx_scoring_absolute_block.yaml` | `tests/modsecurity-scoring.t` | nginx | actions | Absolute `tx.score` assignment blocks on threshold | no | imported | `tests/nginx/cases/imported/` | query args, TX collection, phase2 | NGINX-only until promoted after cross-connector proof |
| `nginx_tx_scoring_iterative_block.yaml` | `tests/modsecurity-scoring.t` | nginx | actions | Iterative `tx.score` increments block on threshold | no | imported | `tests/nginx/cases/imported/` | query args, TX collection, phase2 | NGINX-only until promoted after cross-connector proof |
