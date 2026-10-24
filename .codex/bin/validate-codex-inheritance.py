#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, sys, tomllib

PARENT = Path(__file__).resolve().parents[2]
STRUCTURE = PARENT / '.codex' / 'structure-manifest.toml'
PARENT_MANIFEST = PARENT / '.codex' / 'inheritance-manifest.toml'


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def load_toml(path: Path):
    with path.open('rb') as f: return tomllib.load(f)


def collect_parent_ids(obj):
    found=[]
    def walk(x):
        if isinstance(x, dict):
            for k,v in x.items():
                if isinstance(v,str) and v.startswith('PARENT-') and (k.lower().endswith('id') or k.lower() in {'id','policy','parent'}):
                    found.append(v)
                else: walk(v)
        elif isinstance(x, list):
            for v in x:
                if isinstance(v,str) and v.startswith('PARENT-'): found.append(v)
                else: walk(v)
    walk(obj)
    return found


def parent_catalog(violations, warnings):
    if not PARENT_MANIFEST.is_file():
        violations.append(('parent','manifest_missing','.codex/inheritance-manifest.toml','canonical Parent inheritance manifest is missing'))
        return {},{}
    data=load_toml(PARENT_MANIFEST)
    aliases=data.get('aliases',{})
    catalog={}
    for row in data.get('policies',[]):
        pid=row.get('id'); src=row.get('source'); expected=row.get('sha256')
        if not pid or not src:
            violations.append(('parent','catalog_row_invalid','.codex/inheritance-manifest.toml',f'invalid policy row: {row!r}')); continue
        path=PARENT/src
        if not path.is_file():
            violations.append(('parent','parent_policy_source_missing',src,f'{pid} source must be a regular file')); continue
        observed=sha256(path)
        if expected != observed:
            violations.append(('parent','parent_policy_digest_stale',src,f'{pid} digest is stale: expected {observed}, observed {expected}'))
        catalog[pid]={'source':src,'sha256':observed}
    # inventory drift only for top-level operational context markdown
    ctx=PARENT/'.codex/context'
    actual={f'.codex/context/{p.name}' for p in ctx.glob('*.md') if p.is_file()}
    registered={v['source'] for v in catalog.values()}
    extra=sorted(actual-registered)
    missing=sorted(registered-actual)
    if extra:
        violations.append(('parent','parent_policy_inventory_drift','.codex/inheritance-manifest.toml','unregistered sources: '+', '.join(extra)))
    if missing:
        violations.append(('parent','parent_policy_inventory_drift','.codex/inheritance-manifest.toml','registered sources missing: '+', '.join(missing)))
    agents=PARENT/'AGENTS.md'
    if not agents.is_file() or 'codex-control-plane-routing:parent' not in agents.read_text(errors='replace'):
        violations.append(('parent','agents_routing_marker','AGENTS.md','missing routing marker codex-control-plane-routing:parent'))
    return catalog,aliases


def resolve(pid,catalog,aliases):
    seen=set()
    while pid in aliases and pid not in seen:
        seen.add(pid); pid=aliases[pid]
    return pid


def child_root(name, structure):
    return PARENT / structure[name]['root']


def validate_child(name,catalog,aliases,structure,violations,warnings):
    root=child_root(name,structure)
    manifest=root/'.codex/inheritance-manifest.toml'
    if not root.exists():
        warnings.append((name,'repository_missing',str(root),'repository root is not present in this checkout'))
        return
    if not manifest.is_file():
        violations.append((name,'inheritance_manifest_missing',str(manifest.relative_to(PARENT)),f'{name} inheritance manifest is missing'))
        return
    try: data=load_toml(manifest)
    except Exception as e:
        violations.append((name,'inheritance_manifest_invalid',str(manifest.relative_to(PARENT)),str(e))); return
    ids=collect_parent_ids(data)
    # V3.2 schema uses [[inherit]] and should always be discovered; legacy schemas are recursively scanned.
    if not ids and data.get('inherit'):
        ids=[r.get('id') for r in data['inherit'] if isinstance(r,dict) and isinstance(r.get('id'),str)]
    if not ids:
        violations.append((name,'no_parent_policies',str(manifest.relative_to(PARENT)),'no Parent policy IDs were found'))
        return
    for old in ids:
        new=resolve(old,catalog,aliases)
        if old != new:
            warnings.append((name,'legacy_parent_policy_id',str(manifest.relative_to(PARENT)),f'{old} -> {new}'))
        if new not in catalog:
            violations.append((name,'unknown_parent_policy_id',str(manifest.relative_to(PARENT)),f'{old} is not in the canonical Parent catalog'))
    # Strong digest pins for V3.2 child manifests.
    for row in data.get('inherit',[]):
        if not isinstance(row,dict): continue
        old=row.get('id'); pin=row.get('parent_sha256')
        if not isinstance(old,str): continue
        new=resolve(old,catalog,aliases)
        if new in catalog and pin and pin != catalog[new]['sha256']:
            violations.append((name,'parent_policy_digest_stale',str(manifest.relative_to(PARENT)),f'{old} parent digest is stale: expected {catalog[new]["sha256"]}, observed {pin}'))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    g=ap.add_mutually_exclusive_group()
    g.add_argument('--repository', choices=['parent','framework','mrts'])
    g.add_argument('--all', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--explain', action='store_true')
    args=ap.parse_args()
    if not args.check:
        ap.error('--check is required')
    violations=[]; warnings=[]
    if not STRUCTURE.is_file():
        violations.append(('parent','structure_manifest_missing','.codex/structure-manifest.toml','structure manifest is missing'))
        structure={'parent':{'root':'.'},'framework':{'root':'modules/ModSecurity-test-Framework'},'mrts':{'root':'modules/ModSecurity-test-Framework/tools/MRTS'}}
    else: structure=load_toml(STRUCTURE)
    catalog,aliases=parent_catalog(violations,warnings)
    selected=[args.repository] if args.repository else ['parent','framework','mrts']
    if 'framework' in selected: validate_child('framework',catalog,aliases,structure,violations,warnings)
    if 'mrts' in selected: validate_child('mrts',catalog,aliases,structure,violations,warnings)
    # If only child requested, parent catalog violations still matter because child inheritance cannot be validated without it.
    result={'ok':not violations,'repositories':selected,'violations':[{'repository':r,'code':c,'path':p,'message':m} for r,c,p,m in violations], 'warnings':[{'repository':r,'code':c,'path':p,'message':m} for r,c,p,m in warnings]}
    if args.json:
        print(json.dumps(result,indent=2,sort_keys=True))
    else:
        if violations:
            repos=', '.join(sorted({r for r,_,_,_ in violations}))
            print('VIOLATIONS: '+repos)
            for r,c,p,m in violations: print(f'VIOLATION [{r}:{c}] {p}: {m}')
        else:
            print('Inheritance: OK')
        if args.explain or warnings:
            for r,c,p,m in warnings: print(f'WARNING [{r}:{c}] {p}: {m}')
    return 1 if violations else 0

if __name__=='__main__': raise SystemExit(main())
