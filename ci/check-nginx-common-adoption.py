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
('msconnector_config_init' in module_c and 'msconnector_config_merge' in module_c and 'msconnector_config_validate' in module_c, 'NGINX config init/merge/validate uses Common'),
('msconnector_parse_bool' in module_c, 'NGINX bool parsing uses Common parser'),
('msconnector_parse_phase4_mode' in module_c, 'NGINX phase4 parsing uses Common parser'),
('msconnector_parse_size' in module_c or 'config_parser.h' in module_c, 'NGINX size parser is available through Common config surface'),
('MSCONNECTOR_DIRECTIVE_' in module_c and ('directive_adapter.h' in module_c or 'directive_spec.h' in module_c), 'NGINX directive registration is tied to Common macros/specs/adapters'),
('ngx_http_request_t' in mapper_h and 'msconnector_request' in mapper_h and 'msconnector_request_mapper_contract' in mapper_h and 'msconnector_request_mapper_validate_output' in mapper_c, 'NGINX request mapper contract is present'),
('ngx_http_modsecurity_map_request' in access_c and 'msconnector_request_mapper_contract_init' in access_c, 'NGINX request mapper is exercised in access path'),
('msconnector_response' in mapper_h and 'msconnector_response_mapper_contract' in mapper_h and 'msconnector_response_mapper_validate_output' in mapper_c, 'NGINX response mapper contract is present'),
(('ngx_http_modsecurity_map_response_from_ctx' in header_c or 'ngx_http_modsecurity_map_response' in header_c) and 'msconnector_response_mapper_contract_init' in header_c and 'ngx_http_modsecurity_map_response_from_ctx' in body_c, 'NGINX response mapper is exercised in header/body paths'),
('msconnector_headers_find_first' in mapper_c, 'NGINX mapper uses Common header helpers'),
('msconnector_validate_content_type_token' in module_c and 'ngx_http_modsecurity_validate_strict_mime_token' in module_c and "c == '*'" in module_c and "c == '@'" not in module_c, 'NGINX content-type validation uses Common parser/helper and strict local MIME validation'),
(not re.search(r'ngx_http_modsecurity_[a-z0-9_]*json_escape\s*\(', all_nginx), 'Duplicate NGINX JSON escape helper is absent'),
(not re.search(r'ngx_http_modsecurity_[a-z0-9_]*rule_id\s*\(', all_nginx), 'Duplicate NGINX rule-id helper is absent'),
('ngx_http_modsecurity_pool_strndup' in mapper_c and 'out->method = ngx_http_modsecurity_pool_strndup' in mapper_c and 'out->uri = ngx_http_modsecurity_pool_strndup' in mapper_c, 'NGINX request mapper NUL-terminates request string fields'),
('Content-Type' in mapper_c and 'Content-Length' in mapper_c and 'msconnector_headers_find_first' in mapper_c, 'NGINX response mapper preserves synthetic special headers'),
('ngx_http_modsecurity_redact_intervention' in body_c and 'id:%s msg:%s operator:%s truncated:%s' in body_c, 'NGINX phase4 intervention log uses metadata-only redaction summary'),
('MSCONNECTOR_COMMON_SRC' in nginx_config and '$MSCONNECTOR_COMMON_SRC/event.c' in nginx_config and '$MSCONNECTOR_COMMON_SRC/transaction_state.c' in nginx_config, 'NGINX build uses stable Common source root and links transaction_state.c with event.c'),
('common_response_validated' in common_h and 'if (!ctx->common_response_validated)' in body_c and 'ctx->common_response_validated = 1' in body_c, 'NGINX response mapper validation is gated once per response in body path'),
]
claims = ['production verified','runtime verified','full-matrix verified','crs verified']
text = '\n'.join((ROOT/p).read_text(errors='ignore') for p in ['connectors/nginx/README.md','connectors/nginx/docs/architecture.md'] if (ROOT/p).exists()).lower()
checks.append((not any(c in text for c in claims), 'NGINX docs avoid production/runtime/CRS/full-matrix claims'))
ok=True
for passed,msg in checks:
    print(('PASS' if passed else 'FAIL')+': '+msg)
    ok = ok and passed
sys.exit(0 if ok else 1)
