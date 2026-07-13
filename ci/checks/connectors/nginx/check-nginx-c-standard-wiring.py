#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
mk=(ROOT/'Makefile').read_text()
sh=ROOT/'ci/checks/connectors/nginx/check-nginx-c-standards.sh'
ok=True
def check(cond,msg):
 global ok
 print(('PASS' if cond else 'FAIL')+': '+msg)
 ok = ok and cond
check(sh.exists(),'ci/checks/connectors/nginx/check-nginx-c-standards.sh exists')
for target in ['check-nginx-c17','check-nginx-c23','check-nginx-future-c','check-nginx-c-standards','check-nginx-c17-lint']:
 check((target+':') in mk, f'Makefile contains {target}')
check('$(MAKE) check-nginx-c17-lint' in mk, 'lint invokes check-nginx-c17-lint')
if sh.exists():
 txt=sh.read_text()
 check('-Wno-error' not in txt, 'script does not disable -Werror')
 check('-std=c17' in txt or 'c17' in txt, 'C17 is mandatory')
 check('c23' in txt and 'c2y' in txt and 'SKIPPED' in txt and 'exit 77' in txt, 'optional C23/future-C skip behavior is present')
 check('FRAMEWORK_COMMON' in txt and 'require_or_provision_nginx_headers' in txt, 'script uses framework common NGINX header provision helper')
 check('require_command_or_blocked' in txt, 'script uses framework common command blocker helper')
 check('modsecurity_include_flags_or_provision' in txt, 'script uses framework common libmodsecurity header provision helper')
 check('common/src/transaction_state.c' in txt, 'script compiles transaction_state.c with event.c')
 check('connectors/nginx/src/ngx_http_modsecurity_log.c' in txt, 'script compiles NGINX log source when present')
 cfg=(ROOT/'connectors/nginx/config').read_text()
 check('MSCONNECTOR_COMMON_SRC' in cfg and '$MSCONNECTOR_COMMON_SRC/event.c' in cfg and '$MSCONNECTOR_COMMON_SRC/transaction_state.c' in cfg, 'nginx config uses stable Common source root and keeps event/transaction_state together')
sys.exit(0 if ok else 1)
