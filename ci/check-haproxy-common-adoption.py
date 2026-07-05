#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
paths = [p for p in (ROOT/'connectors/haproxy').rglob('*') if p.is_file() and p.suffix in {'.c','.h','.md',''}]
text = '\n'.join(p.read_text(errors='ignore') for p in paths)
binding = (ROOT/'connectors/haproxy/src/haproxy_modsecurity_binding.c').read_text()
mapper = (ROOT/'connectors/haproxy/src/haproxy_modsecurity_mapper.c').read_text()
ok = True
def check(cond,msg):
    global ok
    print(('PASS' if cond else 'FAIL')+': '+msg)
    ok = ok and cond
check('msconnector_config common_config' in text, 'HAProxy config/runtime embeds msconnector_config common_config')
check('msconnector_config_init' in text and 'msconnector_config_merge' in text and 'msconnector_config_validate' in text, 'HAProxy uses Common config init/merge/validate')
for sym in ['msconnector_parse_bool','msconnector_parse_phase4_mode','msconnector_parse_size']:
    check(sym in text or 'BLOCKED' in text, f'HAProxy uses or documents {sym}')
check('msconnector_parse_bool("on", &bool_value) != 1' in binding, 'Common parser success is treated as return value 1')
check('msconnector_parse_size("1048576", &size_value) != 1' in binding and 'msconnector_parse_size("1m"' not in binding, 'size parser probe uses decimal bytes, not 1m')
check('msconnector_config_merge(&created->common_config, &created->common_config,' in binding and ') != 1 ||' in binding, 'config merge treats 1 as success')
check('msconnector_config_validate(&created->common_config, config_error,' in binding and ') != 1) {' in binding, 'config validate treats 1 as success')
check('config_error[0] = \'\\0\';' in binding, 'config error buffer is initialized before use')
check('MSCONNECTOR_DIRECTIVE_' in text or 'msconnector_directive_spec' in text or 'msconnector_directive_adapter' in text, 'HAProxy references Common directive macros/specs/adapters')
check('haproxy_modsecurity_map_request' in text and 'msconnector_request_mapper_contract' in text and 'msconnector_request_mapper_validate_output' in text, 'HAProxy request mapper uses Common request contract')
check('haproxy_modsecurity_map_response' in text and 'msconnector_response_mapper_contract' in text and 'msconnector_response_mapper_validate_output' in text, 'HAProxy response mapper uses Common response contract')
check('msconnector_request_mapper_validate_output(contract, out, error, error_len)' in mapper and 'if (rc != 1)' in mapper, 'request mapper validation success is not inverted')
check('msconnector_response_mapper_validate_output(contract, out, error, error_len)' in mapper and mapper.count('if (rc != 1)') >= 2, 'response mapper validation success is not inverted')
check('return 1;' in mapper, 'request/response mappers return 1 on success')
check('msconnector_headers_host' in text or 'msconnector_headers_find' in text, 'HAProxy uses Common header helpers')
check('msconnector_event_write_jsonl_line' in text or 'msconnector_rule_id_extract_from_message' in text or 'msconnector_json_escape' in text or 'msconnector_sanitize_log_message' in text, 'HAProxy uses Common event/rule/json/log primitives or documents gap')
check("common_rule_id[0] = '\\0';" in binding, 'rule-id buffer is initialized before extraction')
check('rule_id_result > 0' in binding and 'strtol(common_rule_id' in binding, 'rule-id extraction only uses positive results')
for bad in ['haproxy_parse_bool(', 'haproxy_parse_phase4(', 'haproxy_parse_size(', 'haproxy_json_escape(', 'haproxy_rule_id_extract(']:
    check(bad not in text, f'no duplicate helper {bad}')
for forbidden in ['production verified claim', 'runtime verified claim', 'full-matrix verified claim', 'crs verified claim']:
    check(forbidden not in text.lower(), f'no unsupported {forbidden}')
sys.exit(0 if ok else 1)
