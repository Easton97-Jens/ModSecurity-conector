from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
connectors=['envoy','traefik','lighttpd']
errors=[]
for c in connectors:
    base=root/'connectors'/c
    text='\n'.join(p.read_text(errors='ignore') for p in base.rglob('*') if p.is_file() and p.suffix in {'.c','.h','.md'})
    mapper=base/'src'/f'{c}_modsecurity_mapper.c'
    header=base/'src'/f'{c}_modsecurity_mapper.h'
    if not mapper.is_file() or not header.is_file(): errors.append(f'{c}: request/response mapper files missing')
    m=mapper.read_text(errors='ignore') if mapper.is_file() else ''
    for term in ['msconnector_config_init','msconnector_config_apply_defaults','msconnector_request_init','msconnector_response_init','msconnector_request_mapper_validate_output','msconnector_response_mapper_validate_output']:
        if term not in m: errors.append(f'{c}: missing {term}')
    if 'free((void *)' in text or re.search(r'free\s*\(\s*\(void \*\).*headers', text): errors.append(f'{c}: const-dropping header free found')
    meta=(base/'metadata.c').read_text(errors='ignore')
    if 'not_verified' not in meta: errors.append(f'{c}: runtime_status not not_verified')
    if not any(x in meta for x in ['connector-gap','not_verified']): errors.append(f'{c}: verification_status missing connector-gap/not_verified')
    bad=['production-ready','runtime secure','security verified','CRS verified','full matrix verified','response body verified','runtime verified']
    for b in bad:
        if b.lower() in text.lower(): errors.append(f'{c}: forbidden claim {b}')
    for dup in [f'{c}_parse_bool(',f'{c}_parse_size(',f'{c}_json_escape(',f'{c}_rule_id_extract(',f'{c}_sanitize_log_message(']:
        if dup in text: errors.append(f'{c}: duplicate helper {dup}')
for doc in ['reports/remaining-connectors-common-adoption.md','reports/remaining-connectors-common-adoption.de.md']:
    if not (root/doc).is_file(): errors.append(f'missing {doc}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('remaining connector common adoption: ok')
