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
CTX_BODY_MAPPER_SKIP_GUARD = 'if (ctx->intervention_triggered || ctx->phase4_processed)'
CTX_RESPONSE_VALIDATED_GUARD = 'if (ctx->common_response_validated)'
CTX_RESPONSE_VALIDATED_ASSIGNMENT = 'ctx->common_response_validated = 1;'
ERR_STATUS_PRESENT = 'r->err_status != 0'
nginx_source_paths = (
    tuple(sorted(nginx.glob('*.c')))
    + tuple(sorted(nginx.glob('*.h')))
    + tuple(sorted(nginx.glob('*.hpp')))
)
common_include = ROOT/'common/include'
common_header_paths = (
    tuple(sorted(common_include.rglob('*.h')))
    + tuple(sorted(common_include.rglob('*.hpp')))
) if common_include.is_dir() else ()
profile_registry_header = ROOT/'connectors/profile_registry.h'
profile_registry_header_paths = (
    (profile_registry_header,) if profile_registry_header.is_file() else ()
)
critical_macro_source_paths = (
    nginx_source_paths + common_header_paths + profile_registry_header_paths
)
critical_macro_source_resolved_paths = frozenset(
    path.resolve() for path in critical_macro_source_paths
)
critical_macro_source_inputs = tuple(
    (path, path.read_text(errors='ignore')) for path in critical_macro_source_paths
)
all_nginx = '\n'.join(p.read_text(errors='ignore') for p in nginx.glob('*.c')) + common_h + mapper_h
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
C_TRIGRAPHS = {
    '??=': '#',
    '??/': '\\',
    "??'": '^',
    '??(': '[',
    '??)': ']',
    '??!': '|',
    '??<': '{',
    '??>': '}',
    '??-': '~',
}

def c_function_bounds(source, signature):
    start = source.find(signature)
    if start == -1:
        return None
    opening_brace = source.find('{', start)
    if opening_brace == -1:
        return None
    depth = 0
    for position in range(opening_brace, len(source)):
        if source[position] == '{':
            depth += 1
        elif source[position] == '}':
            depth -= 1
            if depth == 0:
                return start, position + 1
    return None

def c_function(source, signature):
    bounds = c_function_bounds(source, signature)
    if bounds is None:
        return ''
    start, end = bounds
    return source[start:end]

def c_mask_non_newline(characters, start, end):
    for position in range(start, end):
        if characters[position] != '\n':
            characters[position] = ' '

def c_mask_all(source):
    return ''.join('\n' if character == '\n' else ' ' for character in source)

def c_translation_phase_view(source):
    """Apply the C translation phases that affect lexical source selection."""
    translated = []
    position = 0
    while position < len(source):
        replacement = C_TRIGRAPHS.get(source[position:position + 3])
        if replacement is not None:
            translated.append(replacement)
            position += 3
        else:
            translated.append(source[position])
            position += 1
    spliced = re.sub(r'\\\r?\n', '', ''.join(translated))
    return spliced.replace('%:', '#')

def c_outer_include_guard_lines(source):
    lines = source.splitlines(keepends=True)
    nonempty = [(index, line) for index, line in enumerate(lines) if line.strip()]
    if len(nonempty) < 3:
        return None
    first_index, first_line = nonempty[0]
    match = re.match(r'^[ \t\f\v]*#\s*ifndef\s+([A-Za-z_]\w*)\s*$',
        first_line.rstrip('\r\n'))
    if match is None:
        return None
    _, second_line = nonempty[1]
    if not re.match(r'^[ \t\f\v]*#\s*define\s+' + re.escape(match.group(1))
            + r'\s*$', second_line.rstrip('\r\n')):
        return None
    last_index, last_line = nonempty[-1]
    if not re.match(r'^[ \t\f\v]*#\s*endif\b', last_line):
        return None
    return first_index, last_index

def c_mask_conditional_branches(source, allow_outer_include_guard=False):
    characters = list(source)
    lines = source.splitlines(keepends=True)
    outer_guard = c_outer_include_guard_lines(source) if allow_outer_include_guard else None
    conditional_stack = []
    offset = 0

    for line_index, line in enumerate(lines):
        line_end = offset + len(line)
        directive = re.match(r'^[ \t\f\v]*#\s*([A-Za-z_]\w*)\b', line)
        if directive is not None:
            name = directive.group(1)
            c_mask_non_newline(characters, offset, line_end)
            if name in ('if', 'ifdef', 'ifndef'):
                is_outer_guard = outer_guard is not None and line_index == outer_guard[0]
                conditional_stack.append((not is_outer_guard, is_outer_guard))
            elif name in ('elif', 'else'):
                if not conditional_stack:
                    return c_mask_all(source)
                masks_contents, is_outer_guard = conditional_stack[-1]
                if is_outer_guard:
                    conditional_stack[-1] = (True, True)
            elif name == 'endif':
                if not conditional_stack:
                    return c_mask_all(source)
                conditional_stack.pop()
        elif any(masks_contents for masks_contents, _ in conditional_stack):
            c_mask_non_newline(characters, offset, line_end)
        offset = line_end

    if conditional_stack:
        return c_mask_all(source)
    return ''.join(characters)

def c_noncode_views(source):
    """Return C translation-phase-normalized lexical views without non-code text."""
    source = c_translation_phase_view(source)
    active = list(source)
    visible = list(source)
    position = 0

    while position < len(source):
        if source.startswith('/*', position):
            start = position
            end = source.find('*/', position + 2)
            position = len(source) if end == -1 else end + 2
            c_mask_non_newline(active, start, position)
            c_mask_non_newline(visible, start, position)
            continue

        if source.startswith('//', position):
            start = position
            position += 2
            while position < len(source):
                if source[position] == '\\' and source.startswith('\r\n', position + 1):
                    position += 3
                    continue
                if source[position] == '\\' and source.startswith('\n', position + 1):
                    position += 2
                    continue
                if source[position] == '\n':
                    break
                position += 1
            c_mask_non_newline(active, start, position)
            c_mask_non_newline(visible, start, position)
            continue

        if source[position] in "'\"":
            start = position
            quote = source[position]
            position += 1
            while position < len(source):
                if source[position] == '\\':
                    if source.startswith('\r\n', position + 1):
                        position += 3
                    elif position + 1 < len(source):
                        position += 2
                    else:
                        position += 1
                    continue
                if source[position] == quote:
                    position += 1
                    break
                position += 1
            c_mask_non_newline(active, start, position)
            continue

        position += 1

    return ''.join(active), ''.join(visible)

def c_lexical_views(source, allow_outer_include_guard=False):
    active, visible = c_noncode_views(source)
    return (
        c_mask_conditional_branches(active, allow_outer_include_guard),
        c_mask_conditional_branches(visible, allow_outer_include_guard),
    )

def c_checked_function(source, signature, allow_outer_include_guard=False):
    active, visible = c_lexical_views(source, allow_outer_include_guard)
    bounds = c_function_bounds(active, signature)
    if bounds is None:
        return '', ''
    start, end = bounds
    return active[start:end], visible[start:end]

def c_unmasked_function(source, signature):
    """Return one function after translation/non-code masking, before branch masking."""
    active, visible = c_noncode_views(source)
    bounds = c_function_bounds(active, signature)
    if bounds is None:
        return '', ''
    start, end = bounds
    return active[start:end], visible[start:end]

def c_brace_depth_at(source, position):
    depth = 0
    for character in source[:position]:
        if character == '{':
            depth += 1
        elif character == '}':
            depth -= 1
    return depth

def c_direct_matches(source, pattern):
    return [match for match in pattern.finditer(source)
            if c_brace_depth_at(source, match.start()) == 1]

def c_direct_visible_matches(active, visible, pattern):
    if len(active) != len(visible):
        return []
    return [match for match in pattern.finditer(visible)
            if c_brace_depth_at(active, match.start()) == 1]

C_UNIVERSAL_CHARACTER_NAME = re.compile(
    r'\\(?:u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})'
)
C_PREPROCESSOR_DIRECTIVE = re.compile(r'^[ \t\f\v]*#', re.MULTILINE)
C_RETURN_STATEMENT = re.compile(r'\breturn\b(?P<expression>[^;]*);')
C_INCLUDE_DIRECTIVE = re.compile(
    r'^[ \t\f\v]*#\s*(include(?:_next)?|import)\b(.*)$'
)
C_QUOTED_INCLUDE_PAYLOAD = re.compile(r'"([^"\r\n]+)"\s*$')
C_ANGLE_INCLUDE_PAYLOAD = re.compile(r'<([^>\r\n]+)>\s*$')
C_LOCAL_INCLUDE_SUFFIXES = ('.h', '.hpp')
C_ALLOWED_EXTERNAL_QUOTED_INCLUDES = frozenset(('stdio.h',))
C_ALLOWED_EXTERNAL_ANGLE_INCLUDES = frozenset((
    'atomic',
    'ctype.h',
    'modsecurity/modsecurity.h',
    'modsecurity/rules.h',
    'modsecurity/rules_set.h',
    'modsecurity/transaction.h',
    'nginx.h',
    'ngx_config.h',
    'ngx_core.h',
    'ngx_http.h',
    'stdarg.h',
    'stdatomic.h',
    'stddef.h',
    'stdint.h',
    'stdio.h',
    'string.h',
))
CONTROL_FLOW_KEYWORDS = re.compile(r'\b(?:if|for|while|switch)\b')
ELSE_OR_DO_KEYWORDS = re.compile(r'\b(?:else|do)\b')
NON_LINEAR_CONTROL_FLOW = re.compile(r'\b(?:goto|case|default)\b')

def c_skip_whitespace(source, position):
    while position < len(source) and source[position].isspace():
        position += 1
    return position

def c_matching_parenthesis(source, opening):
    depth = 0
    for position in range(opening, len(source)):
        if source[position] == '(':
            depth += 1
        elif source[position] == ')':
            depth -= 1
            if depth == 0:
                return position
    return None

def c_has_unstructured_control_flow(source):
    for match in CONTROL_FLOW_KEYWORDS.finditer(source):
        opening = c_skip_whitespace(source, match.end())
        if opening == len(source) or source[opening] != '(':
            return True
        closing = c_matching_parenthesis(source, opening)
        if closing is None:
            return True
        following = c_skip_whitespace(source, closing + 1)
        if following == len(source) or source[following] != '{':
            return True
    for match in ELSE_OR_DO_KEYWORDS.finditer(source):
        following = c_skip_whitespace(source, match.end())
        if following == len(source) or source[following] != '{':
            return True
    return NON_LINEAR_CONTROL_FLOW.search(source) is not None

def c_has_ucn_escape(source):
    return C_UNIVERSAL_CHARACTER_NAME.search(source) is not None

def c_local_include_candidates(source_path, include_name):
    return (
        source_path.parent / include_name,
        ROOT / include_name,
        common_include / include_name,
    )

def c_has_existing_local_include_candidate(source_path, include_name):
    for candidate in c_local_include_candidates(source_path, include_name):
        try:
            if candidate.exists():
                return True
        except OSError:
            return True
    return False

def c_resolves_to_scanned_source(source_path, include_name):
    for candidate in c_local_include_candidates(source_path, include_name):
        try:
            resolved = candidate.resolve(strict=True)
        except (OSError, RuntimeError):
            continue
        if resolved in critical_macro_source_resolved_paths:
            return True
    return False

def c_has_unsafe_local_include_directive(source_path, source):
    """Reject quoted local includes outside the source-level macro proof."""
    _, visible = c_noncode_views(source)
    for line in visible.splitlines():
        directive = C_INCLUDE_DIRECTIVE.match(line)
        if directive is None:
            continue
        if directive.group(1) != 'include':
            return True
        payload = directive.group(2).strip()
        angle = C_ANGLE_INCLUDE_PAYLOAD.fullmatch(payload)
        if angle is not None:
            include_name = angle.group(1)
            if include_name not in C_ALLOWED_EXTERNAL_ANGLE_INCLUDES:
                return True
            if (
                c_has_existing_local_include_candidate(source_path, include_name)
                and not c_resolves_to_scanned_source(source_path, include_name)
            ):
                return True
            continue
        quoted = C_QUOTED_INCLUDE_PAYLOAD.fullmatch(payload)
        if quoted is None:
            return True
        include_name = quoted.group(1)
        if (
            include_name in C_ALLOWED_EXTERNAL_QUOTED_INCLUDES
            and not c_has_existing_local_include_candidate(source_path, include_name)
        ):
            continue
        components = include_name.split('/')
        if (
            include_name.startswith('/')
            or '\\' in include_name
            or not include_name.endswith(C_LOCAL_INCLUDE_SUFFIXES)
            or any(component in ('', '.', '..') for component in components)
        ):
            return True
        if not c_resolves_to_scanned_source(source_path, include_name):
            return True
    return False

SECURITY_CRITICAL_MACRO_SYMBOLS = frozenset((
    'NGX_ERROR',
    'NGX_HTTP_BAD_REQUEST',
    'NGX_OK',
    'msc_add_n_response_header',
    'ngx_http_modsecurity_add_n_response_header',
    'ngx_http_modsecurity_initialize_request',
    'ngx_http_modsecurity_map_request',
    'ngx_http_modsecurity_map_response_from_ctx',
    'ngx_http_modsecurity_validate_common_request_mapper',
    'ngx_http_modsecurity_validate_header',
    'ngx_http_modsecurity_validate_response_mapper',
))
C_SECURITY_CRITICAL_MACRO_TOKEN = re.compile(
    r'\b(?:' + '|'.join(
        re.escape(symbol) for symbol in sorted(SECURITY_CRITICAL_MACRO_SYMBOLS)
    ) + r')\b'
)
C_MACRO_DIRECTIVE = re.compile(
    r'^[ \t\f\v]*#\s*(define|undef)\s+([A-Za-z_]\w*)\b'
    r'(?P<parameters>\([^)]*\))?'
)
C_ALLOWED_LOCAL_MACRO_NAME = re.compile(
    r'(?:'
    r'MSCONN(?:ECTOR)?_[A-Z0-9_]*|'
    r'MODSECURITY_[A-Z0-9_]*|'
    r'NGX_HTTP_MODSECURITY_[A-Z0-9_]*|'
    r'_NGX_HTTP_MODSECURITY_COMMON_H_INCLUDED_|'
    r'MSC_USE_RULES_SET|'
    r'dd(?:_check_(?:read|write)_event_handler)?|'
    r'ngx_http_modsecurity_pcre_malloc_(?:init|done)|'
    r'strdup'
    r')\Z'
)
C_MACRO_CONTROL_FLOW_TOKEN = re.compile(
    r'\b(?:break|case|continue|default|do|else|for|goto|if|return|switch|while)\b'
)
C_DIAGNOSTIC_STATEMENT_MACRO_NAME = re.compile(
    r'dd(?:_check_(?:read|write)_event_handler)?\Z'
)
C_SAFE_DIAGNOSTIC_STATEMENT_MACRO = re.compile(
    r'\s*do\s*\{(?P<body>.*)\}\s*while\s*\(\s*0\s*\)\s*\Z'
)
C_SAFE_FUNCTION_LIKE_MACRO_REPLACEMENTS = frozenset((
    ('ngx_http_modsecurity_pcre_malloc_init', '(x)', 'NULL'),
    ('ngx_http_modsecurity_pcre_malloc_done', '(x)', '(void)x'),
))

def c_is_safe_diagnostic_statement_macro(directive, replacement):
    """Permit only the existing bounded do/while(0) diagnostic macro form."""
    if (
        C_DIAGNOSTIC_STATEMENT_MACRO_NAME.fullmatch(directive.group(2)) is None
        or directive.group('parameters') is None
    ):
        return False
    if directive.group(2) == 'dd' and not replacement.strip():
        return True
    match = C_SAFE_DIAGNOSTIC_STATEMENT_MACRO.fullmatch(replacement)
    return (
        match is not None
        and C_MACRO_CONTROL_FLOW_TOKEN.search(match.group('body')) is None
    )

def c_is_safe_function_like_macro(directive, replacement):
    """Accept only existing bounded function-like macro semantics."""
    return (
        c_is_safe_diagnostic_statement_macro(directive, replacement)
        or (
            directive.group(2), directive.group('parameters'), replacement.strip()
        ) in C_SAFE_FUNCTION_LIKE_MACRO_REPLACEMENTS
    )

def c_has_security_critical_macro_mutation(source):
    """Reject macro forms that can change or indirectly supply a checked token."""
    active, _ = c_noncode_views(source)
    if C_UNIVERSAL_CHARACTER_NAME.search(active) is not None:
        return True
    for line in active.splitlines():
        directive = C_MACRO_DIRECTIVE.match(line)
        if directive is None:
            continue
        if directive.group(1) != 'define':
            return True
        if C_ALLOWED_LOCAL_MACRO_NAME.fullmatch(directive.group(2)) is None:
            return True
        if directive.group(2) in SECURITY_CRITICAL_MACRO_SYMBOLS:
            return True
        if C_UNIVERSAL_CHARACTER_NAME.search(line) is not None:
            return True
        replacement = line[directive.end():]
        if '##' in replacement:
            return True
        if C_SECURITY_CRITICAL_MACRO_TOKEN.search(replacement) is not None:
            return True
        if (
            directive.group('parameters') is not None
            and not c_is_safe_function_like_macro(directive, replacement)
        ):
            return True
        if (
            C_MACRO_CONTROL_FLOW_TOKEN.search(replacement) is not None
            and not c_is_safe_function_like_macro(directive, replacement)
        ):
            return True
    return False

critical_macro_controls_are_safe = not any(
    path.is_symlink()
    or c_has_security_critical_macro_mutation(source)
    or c_has_unsafe_local_include_directive(path, source)
    for path, source in critical_macro_source_inputs
)

server_header_resolver, _ = c_checked_function(header_c, server_header_resolver_marker)
custom_server_header_marker = 'ngx_table_elt_t *h = r->headers_out.server;'
custom_server_header_start = server_header_resolver.find(custom_server_header_marker)
custom_server_header_match = re.search(
    r'value\.len\s*=\s*h->value\.len;', server_header_resolver[
        custom_server_header_start:]) if custom_server_header_start != -1 else None
custom_server_header_branch = server_header_resolver[custom_server_header_start:
    custom_server_header_start + custom_server_header_match.end()] if (
        custom_server_header_match is not None) else ''
header_all_code, _ = c_noncode_views(header_c)

access_event = c_function(access_c,
    'static void\nngx_http_modsecurity_request_intervention_log_event')
request_mapper_validator_unmasked, _ = c_unmasked_function(access_c,
    'static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper')
request_mapper_validator, request_mapper_validator_visible = c_checked_function(access_c,
    'static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper')
request_initializer_unmasked, _ = c_unmasked_function(access_c,
    'static ngx_int_t\nngx_http_modsecurity_initialize_request')
request_initializer, _ = c_checked_function(access_c,
    'static ngx_int_t\nngx_http_modsecurity_initialize_request')
response_mapper_helper = c_function(mapper_c,
    'void\nngx_http_modsecurity_validate_response_mapper')
response_mapper_from_ctx = c_function(mapper_c,
    'int ngx_http_modsecurity_map_response_from_ctx')
body_response_mapper_once = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_validate_response_mapper_once')
body_filter_prepare = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_prepare_response_body_filter')
body_limited_response_plan = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_plan_limited_response_body')
body_response_chain_append = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_append_response_chain_buffer')
body_response_chain = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_process_response_body_chain')
body_filter = c_function(body_c,
    'ngx_int_t\nngx_http_modsecurity_body_filter(ngx_http_request_t *r, ngx_chain_t *in)')
header_filter = c_function(header_c,
    'ngx_int_t\nngx_http_modsecurity_header_filter(ngx_http_request_t *r)')
phase3_log_event = c_function(header_c,
    'static ngx_int_t\nngx_http_modsecurity_phase3_log_event')
phase4_log_event = c_function(body_c,
    'static ngx_int_t\nngx_http_modsecurity_phase4_log_event')
response_header_sink_unmasked, _ = c_unmasked_function(
    common_h,
    'static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header',
)
response_header_sink, _ = c_checked_function(
    common_h,
    'static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header',
    allow_outer_include_guard=True,
)
request_mapper_call_pattern = re.compile(
    r'ngx_http_modsecurity_map_request\s*\(\s*r\s*,\s*&contract\s*,\s*'
    r'&mapped_request\s*,\s*mapper_error\s*,\s*'
    r'sizeof\s*\(\s*mapper_error\s*\)\s*\)'
)
request_mapper_any_call_pattern = re.compile(
    r'\bngx_http_modsecurity_map_request\s*\('
)
request_mapper_contract_init_pattern = re.compile(
    r'msconnector_request_mapper_contract_init\s*\(\s*&contract\s*\)\s*;'
)
request_mapper_failure_rejection_pattern = re.compile(
    r'if\s*\(\s*!ngx_http_modsecurity_map_request\s*\(\s*'
    r'r\s*,\s*&contract\s*,\s*&mapped_request\s*,\s*mapper_error\s*,\s*'
    r'sizeof\s*\(\s*mapper_error\s*\)\s*\)\s*\)\s*\{\s*'
    r'ngx_log_error\s*\(\s*NGX_LOG_ERR\s*,\s*r->connection->log\s*,\s*0\s*,\s*'
    r'"modsecurity common request mapper validation failed: %s"\s*,\s*'
    r'mapper_error\s*\)\s*;\s*return\s+NGX_HTTP_BAD_REQUEST\s*;\s*\}'
)
request_mapper_failure_propagation_pattern = re.compile(
    r'rc\s*=\s*ngx_http_modsecurity_validate_common_request_mapper\(r\);\s*'
    r'if\s*\(rc\s*!=\s*NGX_OK\)\s*\{\s*'
    r'ctx->intervention_triggered\s*=\s*1;\s*'
    r'return\s+rc;\s*\}',
)
response_header_validation_rejection_pattern = re.compile(
    r'if\s*\(\s*ngx_http_modsecurity_validate_header\s*\(\s*'
    r'ctx\s*,\s*name\s*,\s*name_len\s*,\s*value\s*,\s*'
    r'value_len\s*,\s*1\s*\)\s*!=\s*NGX_OK\s*\)\s*\{\s*'
    r'return\s+NGX_ERROR;\s*\}',
)
response_header_raw_sink_pattern = re.compile(
    r'msc_add_n_response_header\s*\(\s*ctx->modsec_transaction\s*,\s*'
    r'name\s*,\s*name_len\s*,\s*value\s*,\s*value_len\s*\)'
)
response_header_raw_sink_return_pattern = re.compile(
    r'return\s+msc_add_n_response_header\s*\(\s*ctx->modsec_transaction\s*,\s*'
    r'name\s*,\s*name_len\s*,\s*value\s*,\s*value_len\s*\)\s*'
    r'==\s*1\s*\?\s*1\s*:\s*NGX_ERROR\s*;'
)
response_header_raw_sink_name_pattern = re.compile(
    r'\bmsc_add_n_response_header\s*\('
)
request_mapper_calls = list(request_mapper_call_pattern.finditer(request_mapper_validator))
request_mapper_any_calls = list(
    request_mapper_any_call_pattern.finditer(request_mapper_validator))
request_mapper_direct_calls = c_direct_matches(
    request_mapper_validator, request_mapper_call_pattern)
request_mapper_contract_inits = c_direct_matches(
    request_mapper_validator, request_mapper_contract_init_pattern)
request_mapper_failure_rejections = c_direct_visible_matches(
    request_mapper_validator, request_mapper_validator_visible,
    request_mapper_failure_rejection_pattern)
request_mapper_failure_propagations = c_direct_matches(
    request_initializer, request_mapper_failure_propagation_pattern)
request_mapper_failure_propagations_unmasked = c_direct_matches(
    request_initializer_unmasked, request_mapper_failure_propagation_pattern)
request_mapper_initializer_calls = list(re.finditer(
    r'ngx_http_modsecurity_validate_common_request_mapper\s*\(\s*r\s*\)',
    request_initializer))
request_mapper_initializer_direct_calls = c_direct_matches(
    request_initializer,
    re.compile(r'ngx_http_modsecurity_validate_common_request_mapper\s*\(\s*r\s*\)'))
response_header_validation_rejections = c_direct_matches(
    response_header_sink, response_header_validation_rejection_pattern)
response_header_raw_sinks = c_direct_matches(
    response_header_sink, response_header_raw_sink_pattern)
response_header_raw_sink_occurrences = list(
    response_header_raw_sink_pattern.finditer(response_header_sink))
response_header_raw_sink_name_occurrences = list(
    response_header_raw_sink_name_pattern.finditer(response_header_sink))
response_header_raw_sink_returns = c_direct_matches(
    response_header_sink, response_header_raw_sink_return_pattern)
request_mapper_return_statements = list(
    C_RETURN_STATEMENT.finditer(request_mapper_validator_unmasked))
request_initializer_return_statements = list(
    C_RETURN_STATEMENT.finditer(request_initializer_unmasked))
request_initializer_pre_mapper_return_statements = [
    statement for statement in request_initializer_return_statements
    if request_mapper_failure_propagations_unmasked
    and statement.start() < request_mapper_failure_propagations_unmasked[0].start()
]
response_header_return_occurrences = list(
    C_RETURN_STATEMENT.finditer(response_header_sink_unmasked))
mapper_validation_call = 'ngx_http_modsecurity_validate_response_mapper(ctx, r,'
body_mapper_validation_call = (mapper_validation_call + '\n'
    '        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY);')
header_mapper_validation_call = (mapper_validation_call + '\n'
    '        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER);')
caller_mapper_validation = body_response_mapper_once + header_filter
request_hostname_call = request_initializer.find(
    'ngx_http_modsecurity_set_request_hostname')
request_headers_call = request_initializer.find(
    'ngx_http_modsecurity_process_request_headers')
request_mapper_contract_is_fail_closed = (
    critical_macro_controls_are_safe
    and
    len(request_mapper_calls) == 1
    and len(request_mapper_any_calls) == 1
    and len(request_mapper_direct_calls) == 1
    and len(request_mapper_contract_inits) == 1
    and len(request_mapper_failure_rejections) == 1
    and request_mapper_contract_inits[0].start()
    < request_mapper_failure_rejections[0].start()
    <= request_mapper_direct_calls[0].start()
    < request_mapper_failure_rejections[0].end()
    and C_PREPROCESSOR_DIRECTIVE.search(request_mapper_validator_unmasked) is None
    and len(request_mapper_return_statements) == 2
    and request_mapper_return_statements[0].group('expression').strip()
    == 'NGX_HTTP_BAD_REQUEST'
    and request_mapper_return_statements[1].group('expression').strip()
    == 'NGX_OK'
    and not c_has_unstructured_control_flow(request_mapper_validator)
    and not c_has_ucn_escape(request_mapper_validator)
    and 'validation skipped' not in request_mapper_validator_visible
    and len(request_mapper_failure_propagations) == 1
    and len(request_mapper_failure_propagations_unmasked) == 1
    and C_PREPROCESSOR_DIRECTIVE.search(request_initializer_unmasked) is None
    and len(request_initializer_pre_mapper_return_statements) == 1
    and request_initializer_pre_mapper_return_statements[0].group(
        'expression').strip() == 'NGX_HTTP_INTERNAL_SERVER_ERROR'
    and len(request_mapper_initializer_calls) == 1
    and len(request_mapper_initializer_direct_calls) == 1
    and request_mapper_failure_propagations[0].start()
    <= request_mapper_initializer_direct_calls[0].start()
    < request_mapper_failure_propagations[0].end()
    and not c_has_unstructured_control_flow(request_initializer)
    and not c_has_ucn_escape(request_initializer)
    and request_mapper_failure_propagations[0].start() < request_hostname_call
    < request_headers_call
)
response_header_sink_is_bounded = (
    critical_macro_controls_are_safe
    and 'return ngx_http_modsecurity_add_n_response_header(ctx,' in server_header_resolver
    and '(const unsigned char *) value.data,' in server_header_resolver
    and 'value.len);' in server_header_resolver
    and 'msc_add_n_response_header' not in header_all_code
    and not c_has_ucn_escape(header_all_code)
    and len(response_header_validation_rejections) == 1
    and len(response_header_raw_sinks) == 1
    and len(response_header_raw_sink_occurrences) == 1
    and len(response_header_raw_sink_name_occurrences) == 1
    and len(response_header_raw_sink_returns) == 1
    and len(response_header_return_occurrences) == 2
    and C_PREPROCESSOR_DIRECTIVE.search(response_header_sink_unmasked) is None
    and response_header_return_occurrences[0].group('expression').strip()
    == 'NGX_ERROR'
    and response_header_validation_rejections[0].start()
    < response_header_raw_sink_returns[0].start()
    and response_header_return_occurrences[-1].start()
    == response_header_raw_sink_returns[0].start()
    and not c_has_unstructured_control_flow(response_header_sink)
    and not c_has_ucn_escape(response_header_sink)
)
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
(
    request_mapper_contract_is_fail_closed,
    'NGINX request mapper validation fails closed before request-header initialization',
),
('msconnector_response' in mapper_h and 'msconnector_response_mapper_contract' in mapper_h and 'msconnector_response_mapper_validate_output' in mapper_c, 'NGINX response mapper contract is present'),
('typedef enum {' in mapper_h and 'NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER' in mapper_h and 'NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY' in mapper_h and 'void ngx_http_modsecurity_validate_response_mapper(' in mapper_h, 'NGINX mapper owns an internal compile-time response diagnostic discriminator'),
('msconnector_response_mapper_contract contract;' in response_mapper_helper and 'msconnector_response mapped_response;' in response_mapper_helper and 'char mapper_error[128];' in response_mapper_helper and 'msconnector_response_mapper_contract_init(&contract);' in response_mapper_helper and response_mapper_helper.count('ngx_http_modsecurity_map_response_from_ctx') == 1, 'NGINX mapper helper exclusively owns the common response mapper contract/map tail'),
('void\nngx_http_modsecurity_validate_response_mapper' in response_mapper_helper and 'NGX_LOG_WARN' in response_mapper_helper and 'NGX_ERROR' not in response_mapper_helper and 'NGX_HTTP_INTERNAL_SERVER_ERROR' not in response_mapper_helper, 'NGINX response mapper helper is void and warning-only'),
(not any(marker in response_mapper_helper for marker in ('common_response_validated', 'ctx->processed', 'ctx->intervention_triggered', 'ctx->phase4_', 'ctx->response_body_', 'ctx->response_committed', 'msc_process_response_headers', 'msc_process_response_body', 'msc_add_n_response_header', 'ngx_http_next_', 'ngx_http_filter_finalize_request', 'ngx_palloc', 'ngx_pnalloc', 'ngx_pcalloc')), 'NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control'),
(mapper_validation_call in body_response_mapper_once and mapper_validation_call in header_filter and not any(marker in caller_mapper_validation for marker in ('msconnector_response_mapper_contract contract;', 'msconnector_response mapped_response;', 'char mapper_error[128];', 'msconnector_response_mapper_contract_init(&contract);', 'ngx_http_modsecurity_map_response_from_ctx(ctx, r, &contract,')), 'NGINX filter callers delegate instead of retaining a direct mapper-tail duplicate'),
(
    CTX_RESPONSE_VALIDATED_GUARD + ' {\n        return NGX_OK;\n    }' in body_response_mapper_once
    and body_mapper_validation_call in body_response_mapper_once
    and 'NGX_ERROR' not in body_response_mapper_once
    and body_response_mapper_once.count(RETURN_NGX_OK) == 2
    and body_response_mapper_once.find(CTX_RESPONSE_VALIDATED_GUARD)
    < body_response_mapper_once.find(mapper_validation_call)
    < body_response_mapper_once.find(CTX_RESPONSE_VALIDATED_ASSIGNMENT)
    < body_response_mapper_once.rfind(RETURN_NGX_OK)
    and all(marker in body_filter_prepare for marker in (
        CTX_NULL_GUARD,
        CTX_BODY_MAPPER_SKIP_GUARD,
        'ngx_http_modsecurity_validate_response_mapper_once(r, ctx)',
    ))
    and body_filter_prepare.find(CTX_NULL_GUARD)
    < body_filter_prepare.find(CTX_BODY_MAPPER_SKIP_GUARD)
    < body_filter_prepare.find('ngx_http_modsecurity_validate_response_mapper_once(r, ctx)')
    and 'ngx_http_modsecurity_prepare_response_body_filter(r, in, &ctx)' in body_filter,
    'NGINX body mapper validation remains once-only, post-guard, and non-fatal',
),
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
(
    'phase4_in_scope = ngx_http_modsecurity_phase4_in_scope(r)' in body_response_chain
    and 'if (phase4_in_scope == 0)' in body_response_chain_append
    and body_response_chain_append.find('if (phase4_in_scope == 0)')
    < body_response_chain_append.find('ngx_http_modsecurity_append_response_body_buffer')
    and 'return NGX_OK;' in body_response_chain_append[
        :body_response_chain_append.find('ngx_http_modsecurity_append_response_body_buffer')
    ]
    and 'ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n        chain->buf);'
    in body_response_chain_append
    and 'msconnector_body_limit_plan_chunk(ctx->response_body_bytes_seen,'
    in body_limited_response_plan
    and 'ctx->response_body_bytes_seen = plan.bytes_seen;' in body_limited_response_plan
    and 'ctx->response_body_bytes_seen += len' not in body_limited_response_plan,
    'NGINX records seen bytes through the Common plan only after the in-scope gate',
),
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
    response_header_sink_is_bounded,
    'NGINX Server resolver preserves the bounded explicit-length response-header sink',
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
