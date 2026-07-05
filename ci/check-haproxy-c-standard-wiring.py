#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
mk=(ROOT/'Makefile').read_text()
sh=ROOT/'ci/check-haproxy-c-standards.sh'
ok=True
def check(cond,msg):
 global ok
 print(('PASS' if cond else 'FAIL')+': '+msg)
 ok = ok and cond
check(sh.exists(),'ci/check-haproxy-c-standards.sh exists')
for target in ['check-haproxy-c17','check-haproxy-c23','check-haproxy-future-c','check-haproxy-c-standards','check-haproxy-c17-lint']:
 check((target+':') in mk, f'Makefile contains {target}')
check('$(MAKE) check-haproxy-c17-lint' in mk, 'lint invokes check-haproxy-c17-lint')
if sh.exists():
 txt=sh.read_text()
 check('-Wno-error' not in txt, 'script does not disable -Werror')
 check('-std=c17' in txt, 'C17 is mandatory')
 check('c23' in txt and 'c2y' in txt and 'SKIPPED' in txt and 'exit 77' in txt, 'optional C23/future-C skip behavior is present')
 check('HAPROXY_SOURCE_DIR="${HAPROXY_SOURCE_DIR:-${HAPROXY_SRC:-${MODSECURITY_HAPROXY_SOURCE_DIR:-}}}"' in txt, 'script honors HAProxy source fallback variables')
 check('MODSECURITY_INCLUDE_DIR' in txt and 'MODSECURITY_INC' in txt and 'MODSECURITY_INCLUDE_FLAG' in txt, 'script honors ModSecurity include roots and -I flags')
 check('common/src/transaction_state.c' in txt, 'script compiles Common transaction_state.c')
sys.exit(0 if ok else 1)
