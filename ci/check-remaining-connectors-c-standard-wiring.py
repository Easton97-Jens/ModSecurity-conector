from pathlib import Path
root=Path(__file__).resolve().parents[1]
mk=(root/'Makefile').read_text()
script=(root/'ci/check-remaining-connectors-c-standards.sh').read_text()
need=['check-remaining-connectors-c17','check-remaining-connectors-c23','check-remaining-connectors-future-c','check-remaining-connectors-c17-lint']
missing=[n for n in need if n not in mk]
if missing: raise SystemExit('missing Makefile targets: '+', '.join(missing))
for header in ['envoy_modsecurity_mapper.h','traefik_modsecurity_mapper.h','lighttpd_modsecurity_mapper.h']:
    if header not in script: raise SystemExit(f'missing header smoke for {header}')
if '|| true' in script: raise SystemExit('compiler invocation must not be masked with || true')
if 'command -v "$cc"' not in script or 'missing C compiler' not in script or 'exit 77' not in script:
    raise SystemExit('missing C compiler must return blocked exit 77')
if 'rc=$?' not in script or 'return "$rc"' not in script: raise SystemExit('compiler return code must be captured and preserved')
if 'FAIL: remaining connectors C standard check failed' not in script: raise SystemExit('source/header compile failures must be reported as failures')
compile_body=script.split('compile_one() {',1)[1].split('\n}',1)[0]
if 'return 77' in compile_body or 'exit 77' in compile_body: raise SystemExit('compile_one must not convert compile failures to 77')
if '*)' not in script or 'unknown remaining connector C standard profile' not in script: raise SystemExit('profile case must have an explicit default error')
print('remaining connector C standard wiring: ok')
