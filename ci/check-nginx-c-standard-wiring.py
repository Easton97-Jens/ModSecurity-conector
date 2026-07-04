#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
mk=(ROOT/'Makefile').read_text()
sh=ROOT/'ci/check-nginx-c-standards.sh'
ok=True
def check(cond,msg):
 global ok
 print(('PASS' if cond else 'FAIL')+': '+msg)
 ok = ok and cond
check(sh.exists(),'ci/check-nginx-c-standards.sh exists')
for target in ['check-nginx-c17','check-nginx-c23','check-nginx-future-c','check-nginx-c-standards','check-nginx-c17-lint']:
 check((target+':') in mk, f'Makefile contains {target}')
check('$(MAKE) check-nginx-c17-lint' in mk, 'lint invokes check-nginx-c17-lint')
if sh.exists():
 txt=sh.read_text()
 check('-Wno-error' not in txt, 'script does not disable -Werror')
 check('-std=c17' in txt or 'c17' in txt, 'C17 is mandatory')
 check('c23' in txt and 'c2y' in txt and 'SKIPPED' in txt and 'exit 77' in txt, 'optional C23/future-C skip behavior is present')
 check('NGINX_SOURCE_DIR=${NGINX_SOURCE_DIR:-${NGINX_SRC:-${MODSECURITY_NGINX_SOURCE_DIR:-}}}' in txt, 'script honors NGINX_SOURCE_DIR, NGINX_SRC, then MODSECURITY_NGINX_SOURCE_DIR fallback')
 check('common/src/transaction_state.c' in txt, 'script compiles transaction_state.c with event.c')
sys.exit(0 if ok else 1)
