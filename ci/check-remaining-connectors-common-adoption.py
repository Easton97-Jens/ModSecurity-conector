from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
connectors=['envoy','traefik','lighttpd']
errors=[]
existing_mapper_sources=[]
for c in connectors:
    base=root/'connectors'/c
    text='\n'.join(p.read_text(errors='ignore') for p in base.rglob('*') if p.is_file() and p.suffix in {'.c','.h','.md'})
    source=base/'src'/f'{c}_modsecurity_mapper.c'
    header=base/'src'/f'{c}_modsecurity_mapper.h'
    if not header.is_file(): errors.append(f'{c}: mapper header missing')
    h=header.read_text(errors='ignore') if header.is_file() else ''
    m=source.read_text(errors='ignore') if source.is_file() else ''
    if source.is_file(): existing_mapper_sources.append((c, m))
    combined=h+'\n'+m
    for term in ['msconnector_generic_map_request','msconnector_generic_map_response']:
        if term not in combined: errors.append(f'{c}: missing {term}')
    if 'msconnector_generic_config_init' not in combined: errors.append(f'{c}: missing generic config init alias')
    if 'free((void *)' in text or re.search(r'free\s*\(\s*\(void \*\).*headers', text): errors.append(f'{c}: const-dropping header free found')
    copied_terms=['headers_to_common','msconnector_headers_find_first','msconnector_request_init','msconnector_response_init','msconnector_request_mapper_validate_output','msconnector_response_mapper_validate_output','owned_headers']
    for copied in copied_terms:
        if copied in m: errors.append(f'{c}: copied mapper helper remains: {copied}')
    meta=(base/'metadata.c').read_text(errors='ignore')
    if 'not_verified' not in meta and 'not-verified' not in meta: errors.append(f'{c}: runtime_status not not_verified/not-verified')
    if 'connector-gap' not in meta: errors.append(f'{c}: verification_status missing connector-gap')
    for bad in ['production-ready','runtime secure','security verified','CRS verified','full matrix verified','response body verified','runtime verified']:
        if bad.lower() in text.lower(): errors.append(f'{c}: forbidden claim {bad}')
    for dup in [f'{c}_parse_bool(',f'{c}_parse_size(',f'{c}_json_escape(',f'{c}_rule_id_extract(',f'{c}_sanitize_log_message(']:
        if dup in text: errors.append(f'{c}: duplicate helper {dup}')
if len(existing_mapper_sources) == 3 and all(len(m.splitlines()) > 40 for _, m in existing_mapper_sources):
    errors.append('all three mapper source files still exist and are larger than thin adapters')
starter=(root/'connectors/lighttpd/src/lighttpd_build_starter.c').read_text(errors='ignore')
lighttpd_meta=(root/'connectors/lighttpd/metadata.c').read_text(errors='ignore')
if 'not_verified' in lighttpd_meta and 'not_verified' not in starter:
    errors.append('lighttpd starter check does not accept not_verified runtime status')
if 'connector-gap' not in lighttpd_meta:
    errors.append('lighttpd metadata missing connector-gap')
common=(root/'common/src/generic_mapper.c').read_text(errors='ignore') if (root/'common/src/generic_mapper.c').is_file() else ''
if 'msconnector_generic_map_request' not in common or 'msconnector_generic_map_response' not in common:
    errors.append('common generic mapper implementation missing')
for c in connectors:
    source_map=(root/'connectors'/c/'SOURCE_MAP.json').read_text(errors='ignore')
    expected=f'connectors/{c}/src/{c}_modsecurity_mapper.h'
    if expected not in source_map:
        errors.append(f'{c}: mapper header missing from SOURCE_MAP.json')
for doc in ['reports/remaining-connectors-common-adoption.md','reports/remaining-connectors-common-adoption.de.md']:
    if not (root/doc).is_file(): errors.append(f'missing {doc}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('remaining connector common adoption: ok')
