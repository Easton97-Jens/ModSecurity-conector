#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
nginx = ROOT/'connectors/nginx/src'
common_h = (nginx/'ngx_http_modsecurity_common.h').read_text()
module_c = (nginx/'ngx_http_modsecurity_module.c').read_text()
mapper_h = (nginx/'ngx_http_modsecurity_mapper.h').read_text() if (nginx/'ngx_http_modsecurity_mapper.h').exists() else ''
mapper_c = (nginx/'ngx_http_modsecurity_mapper.c').read_text() if (nginx/'ngx_http_modsecurity_mapper.c').exists() else ''
body_c = (nginx/'ngx_http_modsecurity_body_filter.c').read_text()
access_c = (nginx/'ngx_http_modsecurity_access.c').read_text()
header_c = (nginx/'ngx_http_modsecurity_header_filter.c').read_text()
nginx_config = (ROOT/'connectors/nginx/config').read_text()
all_nginx = '\n'.join(p.read_text(errors='ignore') for p in nginx.glob('*.c')) + common_h + mapper_h
checks = [
('msconnector_config common_config' in common_h or 'msconnector_config        common_config' in common_h, 'NGINX config embeds msconnector_config common_config'),
('#if (NGX_PCRE) && !(NGX_PCRE2)' in module_c and '#if !(NGX_PCRE) || (NGX_PCRE2)' in common_h, 'NGINX PCRE allocation shim is disabled for PCRE2 and no-PCRE builds'),
('msconnector_config_init' in module_c and 'msconnector_config_merge' in module_c and 'msconnector_config_validate' in module_c, 'NGINX config init/merge/validate uses Common'),
('msconnector_parse_bool' in module_c, 'NGINX bool parsing uses Common parser'),
('msconnector_parse_phase4_mode' in module_c, 'NGINX phase4 parsing uses Common parser'),
('msconnector_parse_size' in module_c or 'config_parser.h' in module_c, 'NGINX size parser is available through Common config surface'),
('MSCONNECTOR_DIRECTIVE_' in module_c and ('directive_adapter.h' in module_c or 'directive_spec.h' in module_c), 'NGINX directive registration is tied to Common macros/specs/adapters'),
('ngx_http_request_t' in mapper_h and 'msconnector_request' in mapper_h and 'msconnector_request_mapper_contract' in mapper_h and 'msconnector_request_mapper_validate_output' in mapper_c, 'NGINX request mapper contract is present'),
('ngx_http_modsecurity_map_request' in access_c and 'msconnector_request_mapper_contract_init' in access_c, 'NGINX request mapper is exercised in access path'),
('common request mapper validation skipped' in access_c and 'NGX_LOG_WARN' in access_c and 'return NGX_HTTP_INTERNAL_SERVER_ERROR;' not in access_c.split('ngx_http_modsecurity_map_request', 1)[1].split('}', 1)[0], 'NGINX request mapper validation is non-fatal in access path'),
('msconnector_response' in mapper_h and 'msconnector_response_mapper_contract' in mapper_h and 'msconnector_response_mapper_validate_output' in mapper_c, 'NGINX response mapper contract is present'),
(('ngx_http_modsecurity_map_response_from_ctx' in header_c or 'ngx_http_modsecurity_map_response' in header_c) and 'msconnector_response_mapper_contract_init' in header_c and 'ngx_http_modsecurity_map_response_from_ctx' in body_c, 'NGINX response mapper is exercised in header/body paths'),
('common response mapper validation skipped' in header_c and 'NGX_LOG_WARN' in header_c and 'NGX_HTTP_INTERNAL_SERVER_ERROR' not in header_c.split('ngx_http_modsecurity_map_response_from_ctx', 1)[1].split('ctx->common_response_validated = 1', 1)[0], 'NGINX response mapper validation is non-fatal in header path'),
('msconnector_headers_find_first' in mapper_c, 'NGINX mapper uses Common header helpers'),
('msconnector_validate_content_type_token' in module_c and 'ngx_http_modsecurity_validate_strict_mime_token' in module_c and "c == '*'" in module_c and "c == '@'" not in module_c, 'NGINX content-type validation uses Common parser/helper and strict local MIME validation'),
(not re.search(r'ngx_http_modsecurity_[a-z0-9_]*json_escape\s*\(', all_nginx), 'Duplicate NGINX JSON escape helper is absent'),
(not re.search(r'ngx_http_modsecurity_[a-z0-9_]*rule_id\s*\(', all_nginx), 'Duplicate NGINX rule-id helper is absent'),
('ngx_http_modsecurity_pool_strndup' in mapper_c and 'out->method = ngx_http_modsecurity_pool_strndup' in mapper_c and 'out->uri = ngx_http_modsecurity_pool_strndup' in mapper_c, 'NGINX request mapper NUL-terminates request string fields'),
('Content-Type' in mapper_c and 'Content-Length' in mapper_c and 'msconnector_headers_find_first' in mapper_c, 'NGINX response mapper preserves synthetic special headers'),
(mapper_c.find('r->err_status != 0') != -1 and mapper_c.find('headers_out.status != 0') != -1 and mapper_c.find('r->err_status != 0') < mapper_c.find('headers_out.status != 0') and 'out->status = (int) r->err_status' in mapper_c, 'NGINX response mapper preserves err_status before headers_out fallback status'),
('msconnector_event_init' in body_c and 'msconnector_event_write_jsonl_line' in body_c and '"intervention_log"' not in body_c, 'NGINX Phase4 log uses Common metadata-only event serialization without intervention text'),
('msconnector_late_intervention_policy_init' in body_c and 'msconnector_late_intervention_resolve' in body_c and 'msconnector_late_intervention_action_name' in body_c, 'NGINX Phase4 handling uses the Common late-intervention policy'),
('extracted[0]' in body_c and 'rule_id_result =' in body_c and 'rule_id_result > 0' in body_c and 'if (!msconnector_rule_id_extract_from_message' not in body_c, 'NGINX rule-id extraction handles negative failures safely'),
('MSCONNECTOR_COMMON_SRC' in nginx_config and '$MSCONNECTOR_COMMON_SRC/event.c' in nginx_config and '$MSCONNECTOR_COMMON_SRC/transaction_state.c' in nginx_config and '$MSCONNECTOR_COMMON_SRC/late_intervention.c' in nginx_config, 'NGINX build uses stable Common source root and links event and late-intervention support'),
('common_response_validated' in common_h and ('if (!ctx->common_response_validated)' in body_c or 'if (ctx->common_response_validated)' in body_c) and 'ctx->common_response_validated = 1' in body_c, 'NGINX response mapper validation is gated once per response in body path'),
('response_body_bytes_inspected' in common_h and 'ngx_http_modsecurity_append_limited_response_body' in body_c and 'common_config.phase4_body_limit' in body_c and 'ctx->response_body_truncated = 1' in body_c and not re.search(r'msc_append_response_body\s*\([^;]*,\s*len\s*\)', body_c), 'NGINX enforces phase4 body limit before appending response bytes to ModSecurity'),
('chain->buf->last_buf ||' in body_c and 'chain->buf->last_in_chain' in body_c and 'ctx->phase4_processed' in body_c, 'NGINX finalizes Phase4 once at the actual main or subrequest end-of-stream'),
('ngx_int_t in_scope' in body_c and 'if (in_scope == 0)' in body_c and 'ctx->response_body_bytes_seen += len' in body_c, 'NGINX records seen bytes while only ingesting in-scope response chunks'),
('ngx_http_modsecurity_phase4_actual_action(action, wanted)' in body_c and '"redirect" : "deny"' in body_c, 'NGINX preserves redirect as the requested pre-commit action'),
('event.body.content_type' in body_c and 'event.body.bytes_seen' in body_c and 'event.body.bytes_inspected' in body_c, 'NGINX Phase4 events include payload-free content-type and body-byte metadata'),
('ngx_str_t event_transaction_id' in common_h and 'ctx->event_transaction_id' in module_c and 'ctx->event_transaction_id' in body_c and 'event.meta.transaction_id = ctx != NULL' in body_c, 'NGINX Phase4 events retain a request-level transaction ID instead of a connection-only identifier'),
('MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR' not in module_c, 'NGINX does not register Apache-style transaction_id_expr'),
]
claims = ['production verified','runtime verified','full-matrix verified','crs verified']
text = '\n'.join((ROOT/p).read_text(errors='ignore') for p in ['connectors/nginx/README.md','connectors/nginx/docs/architecture.md'] if (ROOT/p).exists()).lower()
checks.append((not any(c in text for c in claims), 'NGINX docs avoid production/runtime/CRS/full-matrix claims'))
ok=True
for passed,msg in checks:
    print(('PASS' if passed else 'FAIL')+': '+msg)
    ok = ok and passed
sys.exit(0 if ok else 1)
