#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
from collections import Counter,defaultdict
import yaml

ROOT=Path(__file__).resolve().parents[1]
CASES_ROOT=ROOT/'tests'
IMPORT_STATUS=ROOT/'tests/import-status.json'
OUT=ROOT/'docs/testing/generated'

RULE_RE=re.compile(r'^\s*SecRule\s+([^\s]+)\s+"(@[^\s"]+)')
PHASE_RE=re.compile(r'phase:(\d)')
TRANS_RE=re.compile(r't:([A-Za-z0-9_]+)')


def load_case(path:Path):
    data=yaml.safe_load(path.read_text())
    rules=data.get('rules','') or ''
    vars_=set(); phases=set(); ops=set(); tfs=set()
    for line in rules.splitlines():
        m=RULE_RE.search(line)
        if m:
            vars_.add(m.group(1))
            ops.add(m.group(2))
        for p in PHASE_RE.findall(line):
            phases.add(int(p))
        for t in TRANS_RE.findall(line):
            tfs.add(t)
    status=str(data.get('status','unknown'))
    name=str(data.get('name',path.stem))
    category=str(data.get('category',''))
    caps=data.get('capabilities',{}) or {}
    return {
        'id':name,'path':str(path.relative_to(ROOT)),'status':status,'category':category,
        'variables':sorted(vars_), 'phases':sorted(phases), 'operators':sorted(ops),'transformations':sorted(tfs),
        'response_body': bool(caps.get('response_body',False)) or any('RESPONSE_BODY' in v for v in vars_),
        'scope': 'common' if 'tests/common/' in str(path) else ('nginx' if 'tests/nginx/' in str(path) else 'apache')
    }


def gather_cases():
    files=sorted((ROOT/'tests/common/cases').rglob('*.yaml'))+sorted((ROOT/'tests/nginx/cases').rglob('*.yaml'))+sorted((ROOT/'tests/apache/cases').rglob('*.yaml'))
    return [load_case(p) for p in files]


def load_import_status():
    return json.loads(IMPORT_STATUS.read_text())


def write(path:Path,text:str):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8')


def main():
    cases=gather_cases(); imp=load_import_status()
    by_status=Counter(c['status'] for c in cases)
    phase_cov=Counter(p for c in cases for p in c['phases'])
    vars_cov=Counter(v for c in cases for v in c['variables'])

    rows=['| case_id | path | scope | status | category | phases | variables | operators | transformations | response_body |','|---|---|---|---|---|---|---|---|---|---|']
    for c in cases:
        rows.append(f"| {c['id']} | `{c['path']}` | {c['scope']} | {c['status']} | {c['category']} | {','.join(map(str,c['phases'])) or '-'} | {', '.join(c['variables']) or '-'} | {', '.join(c['operators']) or '-'} | {', '.join(c['transformations']) or '-'} | {'yes' if c['response_body'] else 'no'} |")
    write(OUT/'case-matrix.generated.md','# Generated Case Matrix\n\n'+"\n".join(rows)+"\n")

    summary=['# Generated Coverage Summary','','## Counts',f"- Total cases: {len(cases)}"]
    for k,v in sorted(by_status.items()): summary.append(f"- status `{k}`: {v}")
    summary += ['','## Phase coverage']
    for p in [1,2,3,4]: summary.append(f"- phase {p}: {phase_cov.get(p,0)}")
    summary += ['','## Top variables']
    for v,cnt in vars_cov.most_common(20): summary.append(f"- `{v}`: {cnt}")
    summary += ['','## RESPONSE_BODY note','- RESPONSE_BODY cases remain non-verified targets unless explicitly proven by full runtime evidence.']
    write(OUT/'coverage-summary.generated.md','\n'.join(summary)+'\n')

    xrows=['# Generated XFAIL Summary','','| case_id | path | status | phases | variables | response_body |','|---|---|---|---|---|---|']
    for c in cases:
        if c['status']!='xfail': continue
        xrows.append(f"| {c['id']} | `{c['path']}` | {c['status']} | {','.join(map(str,c['phases'])) or '-'} | {', '.join(c['variables']) or '-'} | {'yes' if c['response_body'] else 'no'} |")
    write(OUT/'xfail-summary.generated.md','\n'.join(xrows)+'\n')

    gaps=['# Generated Connector Gap Summary','','From import-status reasons and xfail case names containing gap/difference/future.','']
    for key in ['connector_specific','mapped_only','blocked','xfail']:
        gaps.append(f"## {key}")
        for e in imp.get(key,[]):
            if isinstance(e,dict):
                label=e.get('case') or e.get('source') or 'unknown'
                reason=e.get('reason','')
                gaps.append(f"- `{label}`: {reason}")
    write(OUT/'connector-gap-summary.generated.md','\n'.join(gaps)+'\n')

    prow=['# Generated Phase Coverage','','| phase | case_count | response_body_cases |','|---|---:|---:|']
    for p in [1,2,3,4]:
        ph=[c for c in cases if p in c['phases']]
        rb=sum(1 for c in ph if c['response_body'])
        prow.append(f"| {p} | {len(ph)} | {rb} |")
    write(OUT/'phase-coverage.generated.md','\n'.join(prow)+'\n')

if __name__=='__main__':
    main()
