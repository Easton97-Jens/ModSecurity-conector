#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
nginx = ROOT/'connectors/nginx/src'
common_h = (nginx/'ngx_http_modsecurity_common.h').read_text()
module_c = (nginx/'ngx_http_modsecurity_module.c').read_text()
mapper_h = (nginx/'ngx_http_modsecurity_mapper.h').read_text() if (nginx/'ngx_http_modsecurity_mapper.h').exists() else ''
mapper_c = (nginx/'ngx_http_modsecurity_mapper.c').read_text() if (nginx/'ngx_http_modsecurity_mapper.c').exists() else ''
body_c = (nginx/'ngx_http_modsecurity_body_filter.c').read_text()
access_c = (nginx/'ngx_http_modsecurity_access.c').read_text()
header_c = (nginx/'ngx_http_modsecurity_header_filter.c').read_text()
log_c = (nginx/'ngx_http_modsecurity_log.c').read_text()
nginx_config = (ROOT/'connectors/nginx/config').read_text()
EVENT_BODY_BYTES_SEEN = 'event.body.bytes_seen'
EVENT_BODY_BYTES_INSPECTED = 'event.body.bytes_inspected'
REQUEST_BODY_ACCESS = 'r->request_body'
EVENT_JSONL_HEADER = '"msconnector/event_jsonl.h"'
EVENT_JSONL_LINE_BUFFER = 'char line[4096];'
RETURN_NGX_OK = 'return NGX_OK;'
CTX_NULL_GUARD = 'if (ctx == NULL)'
CTX_INTERVENTION_GUARD = 'if (ctx->intervention_triggered)'
CTX_RESPONSE_VALIDATED_GUARD = 'if (ctx->common_response_validated)'
CTX_RESPONSE_VALIDATED_ASSIGNMENT = 'ctx->common_response_validated = 1;'
ERR_STATUS_PRESENT = 'r->err_status != 0'
all_nginx = '\n'.join(p.read_text(errors='ignore') for p in nginx.glob('*.c')) + common_h + mapper_h
access_event_start = access_c.index('static void\nngx_http_modsecurity_request_intervention_log_event')
access_event_end = access_c.index('\n\nngx_int_t\nngx_http_modsecurity_access_handler', access_event_start)
access_event = access_c[access_event_start:access_event_end]
log_event_start = log_c.index('void\nngx_http_modsecurity_log_rule_match_event')
log_event_end = log_c.index('\n\nvoid\nngx_http_modsecurity_log(', log_event_start)
log_event = log_c[log_event_start:log_event_end]
event_metadata_helper_start = common_h.index('static ngx_inline ngx_http_modsecurity_event_request_metadata_t\nngx_http_modsecurity_event_request_metadata')
event_jsonl_helper_start = common_h.index('static ngx_inline int\nngx_http_modsecurity_write_event_jsonl')
event_metadata_helper_end = event_jsonl_helper_start
event_metadata_helper = common_h[event_metadata_helper_start:event_metadata_helper_end]
event_jsonl_helper_end = common_h.index('\n\n/* Phase 3/4 evidence writes', event_jsonl_helper_start)
event_jsonl_helper = common_h[event_jsonl_helper_start:event_jsonl_helper_end]
event_jsonl_serialization_start = event_jsonl_helper.index('if (!msconnector_event_write_jsonl_line')
event_jsonl_serialization_end = event_jsonl_helper.index('\n\n    line_length', event_jsonl_serialization_start)
event_jsonl_serialization = event_jsonl_helper[event_jsonl_serialization_start:event_jsonl_serialization_end]
event_jsonl_write = event_jsonl_helper[event_jsonl_serialization_end:]
phase_event_jsonl_helper_start = common_h.index('static ngx_inline ngx_int_t\nngx_http_modsecurity_write_phase_event_jsonl')
phase_event_jsonl_helper_end = common_h.index('\n\n#if !(NGX_PCRE)', phase_event_jsonl_helper_start)
phase_event_jsonl_helper = common_h[phase_event_jsonl_helper_start:phase_event_jsonl_helper_end]
server_header_resolver_marker = 'static ngx_int_t\nngx_http_modsecurity_resolv_header_server'
server_header_resolver_start = header_c.index(server_header_resolver_marker)
server_header_resolver_end = header_c.find('\nstatic ngx_int_t\n', server_header_resolver_start + len(server_header_resolver_marker))
server_header_resolver = header_c[server_header_resolver_start:server_header_resolver_end] if server_header_resolver_end != -1 else ''
custom_server_header_marker = 'ngx_table_elt_t *h = r->headers_out.server;'
custom_server_header_start = server_header_resolver.find(custom_server_header_marker)
custom_server_header_end = server_header_resolver.find('\n#if', custom_server_header_start)
custom_server_header_branch = server_header_resolver[custom_server_header_start:custom_server_header_end] if custom_server_header_start != -1 and custom_server_header_end != -1 else ''

def c_function(source, signature):
    start = source.find(signature)
    if start == -1:
        return ''
    opening_brace = source.find('{', start)
    if opening_brace == -1:
        return ''
    depth = 0
    for position in range(opening_brace, len(source)):
        if source[position] == '{':
            depth += 1
        elif source[position] == '}':
            depth -= 1
            if depth == 0:
                return source[start:position + 1]
    return ''

response_mapper_helper = c_function(mapper_c,
    'void\nngx_http_modsecurity_validate_response_mapper')
response_mapper_from_ctx = c_function(mapper_c,
    'int ngx_http_modsecurity_map_response_from_ctx')
body_response_mapper_once = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_validate_response_mapper_once')
body_filter = c_function(body_c,
    'ngx_int_t\nngx_http_modsecurity_body_filter(ngx_http_request_t *r, ngx_chain_t *in)')
header_filter = c_function(header_c,
    'ngx_int_t\nngx_http_modsecurity_header_filter(ngx_http_request_t *r)')
phase3_log_event = c_function(header_c,
    'static ngx_int_t\nngx_http_modsecurity_phase3_log_event')
phase4_log_event = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_phase4_log_event')
mapper_validation_call = 'ngx_http_modsecurity_validate_response_mapper(ctx, r,'
body_mapper_validation_call = (mapper_validation_call + '\n'
    '        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY);')
header_mapper_validation_call = (mapper_validation_call + '\n'
    '        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER);')
caller_mapper_validation = body_response_mapper_once + header_filter
checks = [
('msconnector_config common_config' in common_h or 'msconnector_config        common_config' in common_h, 'NGINX config embeds msconnector_config common_config'),
('"msconnector/phase.h"' in common_h and 'enum msconnector_phase native_event_phase;' in common_h, 'NGINX native event phase has its complete Common enum declaration'),
('#if (NGX_PCRE) && !(NGX_PCRE2)' in module_c and '#if !(NGX_PCRE) || (NGX_PCRE2)' in common_h, 'NGINX PCRE allocation shim is disabled for PCRE2 and no-PCRE builds'),
('msconnector_config_init' in module_c and 'msconnector_config_merge' in module_c and 'msconnector_config_validate' in module_c, 'NGINX config init/merge/validate uses Common'),
('conf->phase4_log_file = NGX_CONF_UNSET_PTR;' in module_c and 'conf->phase4_content_types = NGX_CONF_UNSET_PTR;' in module_c and 'ngx_conf_merge_ptr_value(c->phase4_log_file, p->phase4_log_file, NULL);' in module_c, 'NGINX inherits server-level Phase4 log and content-type settings into locations'),
('msconnector_parse_bool' in module_c, 'NGINX bool parsing uses Common parser'),
('msconnector_parse_phase4_mode' in module_c, 'NGINX phase4 parsing uses Common parser'),
('msconnector_parse_size' in module_c or 'config_parser.h' in module_c, 'NGINX size parser is available through Common config surface'),
('MSCONNECTOR_DIRECTIVE_' in module_c and ('directive_adapter.h' in module_c or 'directive_spec.h' in module_c), 'NGINX directive registration is tied to Common macros/specs/adapters'),
('ngx_http_request_t' in mapper_h and 'msconnector_request' in mapper_h and 'msconnector_request_mapper_contract' in mapper_h and 'msconnector_request_mapper_validate_output' in mapper_c, 'NGINX request mapper contract is present'),
('ngx_http_modsecurity_map_request' in access_c and 'msconnector_request_mapper_contract_init' in access_c, 'NGINX request mapper is exercised in access path'),
('common request mapper validation skipped' in access_c and 'NGX_LOG_WARN' in access_c and 'return NGX_HTTP_INTERNAL_SERVER_ERROR;' not in access_c.split('ngx_http_modsecurity_map_request', 1)[1].split('}', 1)[0], 'NGINX request mapper validation is non-fatal in access path'),
('msconnector_response' in mapper_h and 'msconnector_response_mapper_contract' in mapper_h and 'msconnector_response_mapper_validate_output' in mapper_c, 'NGINX response mapper contract is present'),
('typedef enum {' in mapper_h and 'NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER' in mapper_h and 'NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY' in mapper_h and 'void ngx_http_modsecurity_validate_response_mapper(' in mapper_h, 'NGINX mapper owns an internal compile-time response diagnostic discriminator'),
('msconnector_response_mapper_contract contract;' in response_mapper_helper and 'msconnector_response mapped_response;' in response_mapper_helper and 'char mapper_error[128];' in response_mapper_helper and 'msconnector_response_mapper_contract_init(&contract);' in response_mapper_helper and response_mapper_helper.count('ngx_http_modsecurity_map_response_from_ctx') == 1, 'NGINX mapper helper exclusively owns the common response mapper contract/map tail'),
('void\nngx_http_modsecurity_validate_response_mapper' in response_mapper_helper and 'NGX_LOG_WARN' in response_mapper_helper and 'NGX_ERROR' not in response_mapper_helper and 'NGX_HTTP_INTERNAL_SERVER_ERROR' not in response_mapper_helper, 'NGINX response mapper helper is void and warning-only'),
(not any(marker in response_mapper_helper for marker in ('common_response_validated', 'ctx->processed', 'ctx->intervention_triggered', 'ctx->phase4_', 'ctx->response_body_', 'ctx->response_committed', 'msc_process_response_headers', 'msc_process_response_body', 'msc_add_n_response_header', 'ngx_http_next_', 'ngx_http_filter_finalize_request', 'ngx_palloc', 'ngx_pnalloc', 'ngx_pcalloc')), 'NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control'),
(mapper_validation_call in body_response_mapper_once and mapper_validation_call in header_filter and not any(marker in caller_mapper_validation for marker in ('msconnector_response_mapper_contract contract;', 'msconnector_response mapped_response;', 'char mapper_error[128];', 'msconnector_response_mapper_contract_init(&contract);', 'ngx_http_modsecurity_map_response_from_ctx(ctx, r, &contract,')), 'NGINX filter callers delegate instead of retaining a direct mapper-tail duplicate'),
(CTX_RESPONSE_VALIDATED_GUARD + ' {\n        return NGX_OK;\n    }' in body_response_mapper_once and body_mapper_validation_call in body_response_mapper_once and 'NGX_ERROR' not in body_response_mapper_once and body_response_mapper_once.count(RETURN_NGX_OK) == 2 and body_response_mapper_once.find(CTX_RESPONSE_VALIDATED_GUARD) < body_response_mapper_once.find(mapper_validation_call) < body_response_mapper_once.find(CTX_RESPONSE_VALIDATED_ASSIGNMENT) < body_response_mapper_once.rfind(RETURN_NGX_OK) and all(marker in body_filter for marker in (CTX_NULL_GUARD, CTX_INTERVENTION_GUARD, 'ngx_http_modsecurity_validate_response_mapper_once(r, ctx)')) and body_filter.find(CTX_NULL_GUARD) < body_filter.find(CTX_INTERVENTION_GUARD) < body_filter.find('ngx_http_modsecurity_validate_response_mapper_once(r, ctx)'), 'NGINX body mapper validation remains once-only, post-guard, and non-fatal'),
(header_mapper_validation_call in header_filter and header_filter.count(mapper_validation_call) == 1 and CTX_RESPONSE_VALIDATED_GUARD not in header_filter and all(marker in header_filter for marker in (CTX_NULL_GUARD, CTX_INTERVENTION_GUARD, header_mapper_validation_call, CTX_RESPONSE_VALIDATED_ASSIGNMENT, 'if (ctx && ctx->processed)')) and header_filter.find(CTX_NULL_GUARD) < header_filter.find(CTX_INTERVENTION_GUARD) < header_filter.find(header_mapper_validation_call) < header_filter.find(CTX_RESPONSE_VALIDATED_ASSIGNMENT) < header_filter.find('if (ctx && ctx->processed)'), 'NGINX header mapper validation retains its existing eligibility and ordering without a once gate'),
('if (diagnostic == NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY)' in response_mapper_helper and '"modsecurity common response-body mapper validation skipped: %s"' in response_mapper_helper and '"modsecurity common response mapper validation skipped: %s"' in response_mapper_helper and 'const char *' not in response_mapper_helper and body_mapper_validation_call in body_response_mapper_once and header_mapper_validation_call in header_filter, 'NGINX response mapper helper retains fixed caller-specific warning diagnostics'),
('ngx_http_modsecurity_add_synthetic_response_headers(r, headers, &header_count)' in response_mapper_from_ctx and response_mapper_from_ctx.find(ERR_STATUS_PRESENT) < response_mapper_from_ctx.find('r->headers_out.status != 0') and 'out->status = (int) r->err_status' in response_mapper_from_ctx, 'NGINX response mapper retains synthetic-header and err_status contracts'),
('msconnector_headers_find_first' in mapper_c, 'NGINX mapper uses Common header helpers'),
('msconnector_validate_content_type_token' in module_c and 'ngx_http_modsecurity_validate_strict_mime_token' in module_c and "c == '*'" in module_c and "c == '@'" not in module_c, 'NGINX content-type validation uses Common parser/helper and strict local MIME validation'),
(not re.search(r'ngx_http_modsecurity_[a-z0-9_]*json_escape\s*\(', all_nginx), 'Duplicate NGINX JSON escape helper is absent'),
(not re.search(r'ngx_http_modsecurity_[a-z0-9_]*rule_id\s*\(', all_nginx), 'Duplicate NGINX rule-id helper is absent'),
('ngx_http_modsecurity_pool_strndup' in mapper_c and 'out->method = ngx_http_modsecurity_pool_strndup' in mapper_c and 'out->uri = ngx_http_modsecurity_pool_strndup' in mapper_c, 'NGINX request mapper NUL-terminates request string fields'),
('Content-Type' in mapper_c and 'Content-Length' in mapper_c and 'msconnector_headers_find_first' in mapper_c, 'NGINX response mapper preserves synthetic special headers'),
(mapper_c.find(ERR_STATUS_PRESENT) != -1 and mapper_c.find('headers_out.status != 0') != -1 and mapper_c.find(ERR_STATUS_PRESENT) < mapper_c.find('headers_out.status != 0') and 'out->status = (int) r->err_status' in mapper_c, 'NGINX response mapper preserves err_status before headers_out fallback status'),
('msconnector_event_init' in body_c and 'msconnector_event_write_jsonl_line' not in body_c and 'msconnector_event_write_jsonl_line' in phase_event_jsonl_helper and '"intervention_log"' not in body_c, 'NGINX Phase4 log uses the strict Common metadata-only event serialization without intervention text'),
('typedef struct {\n    const char *method;\n    const char *uri;\n    const char *content_type;\n} ngx_http_modsecurity_event_request_metadata_t;' in common_h and 'ngx_http_modsecurity_event_request_metadata_t metadata = {\n        "", "", ""\n    };' in event_metadata_helper and 'if (r == NULL)' in event_metadata_helper and 'r->method_name.len > 0U' in event_metadata_helper and 'r->unparsed_uri.len > 0U' in event_metadata_helper and 'r->headers_in.content_type != NULL' in event_metadata_helper and 'value != (char *)-1 && value != NULL' in event_metadata_helper and 'metadata.method = value;' in event_metadata_helper and 'metadata.uri = value;' in event_metadata_helper and 'metadata.content_type = value;' in event_metadata_helper, 'NGINX event request-metadata helper preserves empty fallbacks for absent, empty, NULL, and allocation-failure values'),
(EVENT_JSONL_HEADER in common_h and EVENT_JSONL_HEADER not in access_c and EVENT_JSONL_HEADER not in log_c, 'NGINX common header owns the event JSONL serialization dependency'),
(EVENT_JSONL_LINE_BUFFER in event_jsonl_helper and 'int json_truncated = 0;' in event_jsonl_helper and event_jsonl_helper.count('msconnector_event_write_jsonl_line') == 1 and 'line_length = ngx_strlen(line);' in event_jsonl_helper and event_jsonl_helper.count('ngx_write_fd') == 1 and 'written < 0 || (size_t)written != line_length' in event_jsonl_helper and 'written < 0 ? ngx_errno : 0' in event_jsonl_helper and '"%s", write_failure_message' in event_jsonl_write and EVENT_BODY_BYTES_SEEN not in event_jsonl_helper and EVENT_BODY_BYTES_INSPECTED not in event_jsonl_helper and REQUEST_BODY_ACCESS not in event_jsonl_helper, 'NGINX common JSONL helper retains one bounded serialization and one warning-only write without body data'),
('"%s%s", serialization_failure_message' in event_jsonl_serialization and 'json_truncated ? " (truncated)" : ""' in event_jsonl_serialization and 'return 0;' in event_jsonl_serialization and 'return 1;' in event_jsonl_write, 'NGINX common JSONL helper returns failure only for serialization and preserves warning-only write behavior'),
('ngx_http_modsecurity_write_event_jsonl' not in body_c and 'ngx_http_modsecurity_write_event_jsonl' not in header_c, 'NGINX common JSONL helper is not extended to body or header event paths'),
(EVENT_JSONL_LINE_BUFFER in phase_event_jsonl_helper and 'int json_truncated = 0;' in phase_event_jsonl_helper and phase_event_jsonl_helper.count('msconnector_event_write_jsonl_line') == 1 and phase_event_jsonl_helper.count('ngx_write_fd') == 1 and 'return NGX_ERROR;' in phase_event_jsonl_helper and RETURN_NGX_OK in phase_event_jsonl_helper and 'written < 0' in phase_event_jsonl_helper and '(size_t)written != line_length' in phase_event_jsonl_helper and 'modsecurity %s common event serialization failed%s' in phase_event_jsonl_helper and 'modsecurity %s log write failed' in phase_event_jsonl_helper and 'modsecurity %s log short write: %z of %uz bytes' in phase_event_jsonl_helper and EVENT_BODY_BYTES_SEEN not in phase_event_jsonl_helper and EVENT_BODY_BYTES_INSPECTED not in phase_event_jsonl_helper and REQUEST_BODY_ACCESS not in phase_event_jsonl_helper, 'NGINX strict Phase3/4 JSONL helper has one bounded write tail and propagates serialization, write, and short-write failures without body data'),
('ngx_http_modsecurity_write_phase_event_jsonl(r, mcf, &event,\n        "phase3");' in phase3_log_event and 'msconnector_event_write_jsonl_line' not in phase3_log_event and 'ngx_write_fd' not in phase3_log_event and EVENT_JSONL_LINE_BUFFER not in phase3_log_event, 'NGINX Phase3 event construction delegates only the strict JSONL tail and retains its phase-specific diagnostics'),
('ngx_http_modsecurity_write_phase_event_jsonl(r, mcf, &event,\n        "phase4");' in phase4_log_event and 'msconnector_event_write_jsonl_line' not in phase4_log_event and 'ngx_write_fd' not in phase4_log_event and EVENT_JSONL_LINE_BUFFER not in phase4_log_event, 'NGINX Phase4 event construction delegates only the strict JSONL tail and retains its phase-specific diagnostics'),
('ngx_http_modsecurity_event_request_metadata(r)' in access_event and 'ngx_http_modsecurity_event_request_metadata(r)' in log_event and 'ngx_str_to_char(' not in access_event and 'ngx_str_to_char(' not in log_event and 'event.request.method = request_metadata.method;' in access_event and 'event.request.method = request_metadata.method;' in log_event and 'event.request.uri = request_metadata.uri;' in access_event and 'event.request.uri = request_metadata.uri;' in log_event and 'event.body.content_type = request_metadata.content_type;' in access_event and 'event.body.content_type = request_metadata.content_type;' in log_event, 'NGINX access and native rule-match loggers share only request-metadata conversion'),
((EVENT_BODY_BYTES_SEEN not in access_event and EVENT_BODY_BYTES_SEEN not in log_event and EVENT_BODY_BYTES_INSPECTED not in access_event and EVENT_BODY_BYTES_INSPECTED not in log_event and REQUEST_BODY_ACCESS not in access_event and REQUEST_BODY_ACCESS not in log_event), 'NGINX request event loggers keep helper output metadata-only and exclude request-body data'),
('MSCONN_EVENT_REQUEST_BLOCKED' in access_event and 'MSCONNECTOR_STATUS_BLOCKED' in access_event and 'event.decision.action = wanted;' in access_event and 'MSCONN_EVENT_RULE_MATCHED' in log_event and 'MSCONNECTOR_STATUS_OK' in log_event and 'event.decision.action = "pass";' in log_event and 'event.decision.rule_id = rule_id;' in log_event, 'NGINX event construction and decision semantics remain source-specific'),
('"modsecurity request intervention event serialization failed"' in access_event and '"modsecurity request intervention log write failed"' in access_event and '"modsecurity native rule-match event serialization failed"' in log_event and '"modsecurity native rule-match log write failed"' in log_event, 'NGINX request event callers retain exact source-specific serialization and write diagnostics'),
('if (r == NULL || mcf == NULL || mcf->phase4_log_file == NULL ||' in access_event and 'if (r == NULL || !msconnector_rule_id_validate(rule_id))' in log_event and 'ctx == NULL || mcf == NULL || mcf->phase4_log_file == NULL ||' in log_event and 'if (!ngx_http_modsecurity_write_event_jsonl(' in access_event and 'if (!ngx_http_modsecurity_write_event_jsonl(' in log_event and 'msconnector_event_write_jsonl_line' not in access_event and 'msconnector_event_write_jsonl_line' not in log_event and 'ngx_write_fd' not in access_event and 'ngx_write_fd' not in log_event and EVENT_JSONL_LINE_BUFFER not in access_event and EVENT_JSONL_LINE_BUFFER not in log_event and 'json_truncated' not in access_event and 'json_truncated' not in log_event and 'line_length' not in access_event and 'line_length' not in log_event and 'ssize_t written' not in access_event and 'ssize_t written' not in log_event, 'NGINX request event loggers retain source-specific guards and rule-ID validation while delegating the direct JSONL tail'),
('msconnector_late_intervention_policy_init' in body_c and 'msconnector_late_intervention_resolve' in body_c and 'msconnector_late_intervention_action_name' in body_c, 'NGINX Phase4 handling uses the Common late-intervention policy'),
('last_intervention_rule_id' in common_h and 'msconnector_rule_id_extract_from_message' in module_c and 'last_intervention_log' not in common_h + module_c + body_c and 'last_intervention_rule_id' in body_c, 'NGINX retains only a bounded extracted rule ID instead of copying the full intervention log'),
('log_result = ngx_http_modsecurity_phase4_log_event' in body_c and 'if (log_result != NGX_OK)' in body_c and 'return ngx_http_modsecurity_phase4_log_event' in body_c and 'return NGX_ERROR;' in phase_event_jsonl_helper and '"phase4"' in phase4_log_event, 'NGINX Phase4 event write and short-write failures are observable and propagated'),
('MSCONNECTOR_COMMON_SRC' in nginx_config and '$MSCONNECTOR_COMMON_SRC/event.c' in nginx_config and '$MSCONNECTOR_COMMON_SRC/transaction_state.c' in nginx_config and '$MSCONNECTOR_COMMON_SRC/late_intervention.c' in nginx_config, 'NGINX build uses stable Common source root and links event and late-intervention support'),
('common_response_validated' in common_h and ('if (!ctx->common_response_validated)' in body_c or CTX_RESPONSE_VALIDATED_GUARD in body_c) and 'ctx->common_response_validated = 1' in body_c, 'NGINX response mapper validation is gated once per response in body path'),
('response_body_bytes_inspected' in common_h and 'ngx_http_modsecurity_append_limited_response_body' in body_c and 'common_config.phase4_body_limit' in body_c and 'ctx->response_body_truncated = 1' in body_c and not re.search(r'msc_append_response_body\s*\([^;]*,\s*len\s*\)', body_c), 'NGINX enforces phase4 body limit before appending response bytes to ModSecurity'),
('chain->buf->last_buf ||' in body_c and 'chain->buf->last_in_chain' in body_c and 'ctx->phase4_processed' in body_c, 'NGINX finalizes Phase4 once at the actual main or subrequest end-of-stream'),
('ngx_int_t in_scope' in body_c and 'if (in_scope == 0)' in body_c and 'ctx->response_body_bytes_seen += len' in body_c, 'NGINX records seen bytes while only ingesting in-scope response chunks'),
('ngx_http_modsecurity_phase4_actual_action(action, wanted)' in body_c and '"redirect" : "deny"' in body_c, 'NGINX preserves redirect as the requested pre-commit action'),
('event.body.content_type' in body_c and EVENT_BODY_BYTES_SEEN in body_c and EVENT_BODY_BYTES_INSPECTED in body_c, 'NGINX Phase4 events include payload-free content-type and body-byte metadata'),
('ngx_str_t event_transaction_id' in common_h and 'ctx->event_transaction_id' in module_c and 'ctx->event_transaction_id' in body_c and 'event.meta.transaction_id = ctx != NULL' in body_c, 'NGINX Phase4 events retain a request-level transaction ID instead of a connection-only identifier'),
('MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR' not in module_c, 'NGINX does not register Apache-style transaction_id_expr'),
(
    'value.data = (u_char *)ngx_http_server_full_string;' in server_header_resolver
    and 'value.len = sizeof(ngx_http_server_full_string) - 1U;' in server_header_resolver
    and 'value.len = sizeof(ngx_http_server_full_string);' not in server_header_resolver,
    'NGINX server_tokens default excludes the terminating NUL from the explicit Server header length',
),
(
    'value.data = (u_char *)ngx_http_server_string;' in server_header_resolver
    and 'value.len = sizeof(ngx_http_server_string) - 1U;' in server_header_resolver
    and 'value.len = sizeof(ngx_http_server_string);' not in server_header_resolver,
    'NGINX non-tokenized default excludes the terminating NUL from the explicit Server header length',
),
(
    'ngx_table_elt_t *h = r->headers_out.server;' in custom_server_header_branch
    and 'value.data = h->value.data;' in custom_server_header_branch
    and re.search(r'value\.len\s*=\s*h->value\.len;', custom_server_header_branch) is not None
    and '- 1U' not in custom_server_header_branch
    and 'strlen(' not in custom_server_header_branch
    and 'ngx_strlen(' not in custom_server_header_branch,
    'NGINX custom Server headers retain the host-provided explicit length',
),
(
    'return msc_add_n_response_header(ctx->modsec_transaction,' in server_header_resolver
    and '(const unsigned char *) value.data,' in server_header_resolver
    and 'value.len);' in server_header_resolver,
    'NGINX Server resolver preserves the explicit-length response-header sink',
),
]
claims = ['production verified','runtime verified','full-matrix verified','crs verified']
text = '\n'.join((ROOT/p).read_text(errors='ignore') for p in ['connectors/nginx/README.md','docs/connectors/nginx.md'] if (ROOT/p).exists()).lower()
checks.append((not any(c in text for c in claims), 'NGINX docs avoid production/runtime/CRS/full-matrix claims'))
ok=True
for passed,msg in checks:
    print(('PASS' if passed else 'FAIL')+': '+msg)
    ok = ok and passed
sys.exit(0 if ok else 1)
