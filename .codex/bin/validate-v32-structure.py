#!/usr/bin/env python3
from pathlib import Path
import sys, tomllib

ROOT = Path(__file__).resolve().parents[2]
CTX = ROOT / '.codex' / 'context'
SKILL = '/root/.agents/skills/goal-driven-execution/SKILL.md'
SONAR_WRAPPER = '/usr/local/bin/sonar-with-env'

required = [
    ROOT/'AGENTS.md', CTX/'index.md', CTX/'manifest.toml', ROOT/'.codex/inheritance-manifest.toml', ROOT/'.codex/structure-manifest.toml', ROOT/'.codex/bin/validate-codex-inheritance.py',
    CTX/'command-execution-policy.md', CTX/'sonarqube-policy.md', CTX/'task-workflow.md',
    CTX/'profiles/connector-security-assessment.md',
    CTX/'profiles/all-connectors-security-assessment.md',
    CTX/'profiles/full-repository-assessment.md',
    CTX/'profiles/phase4-migration-assessment.md',
    CTX/'profiles/evidence-integrity-assessment.md',
    CTX/'profiles/connector-runtime-assessment.md',
    CTX/'profiles/all-connectors-runtime-assessment.md',
    CTX/'profiles/ci-supply-chain-assessment.md',
    CTX/'profiles/strict-completeness-assessment.md',
    CTX/'security/connector-deep-assessment.md',
    CTX/'security/quality-scoring-policy.md',
    CTX/'security/analysis-services-policy.md',
]

connectors = ['apache','nginx','haproxy','envoy','traefik','lighttpd']
required += [CTX/'security'/'connectors'/f'{c}.md' for c in connectors]
checks = [
'advisory-research','concurrency-races','config-injection','evidence-integrity',
'filesystem-ipc','finding-validation','http-normalization','logging-disclosure',
'memory-lifecycle','modsecurity-bypass','request-desync','resource-exhaustion',
'response-commit-phase4','runtime-failure-recovery','supply-chain','protocol-framing']
required += [CTX/'security'/'checks'/f'{c}.md' for c in checks]

errors=[]
for q in required:
    if not q.is_file():
        errors.append(f'missing: {q.relative_to(ROOT)}')

manifest = tomllib.loads((CTX/'manifest.toml').read_text())
if str(manifest.get('version')) != '3.2':
    errors.append(f"manifest version is not 3.2: {manifest.get('version')!r}")
for group in ('primary_policies','profiles','connectors'):
    if group not in manifest:
        errors.append(f'manifest missing section: {group}')
        continue
    for key, rel in manifest[group].items():
        if not (ROOT/rel).is_file():
            errors.append(f'manifest missing target {group}.{key}: {rel}')

agents = (ROOT/'AGENTS.md').read_text(errors='replace')
workflow = (CTX/'task-workflow.md').read_text(errors='replace')
index = (CTX/'index.md').read_text(errors='replace')
cmd = (CTX/'command-execution-policy.md').read_text(errors='replace')
sonar = (CTX/'sonarqube-policy.md').read_text(errors='replace')
services = (CTX/'security/analysis-services-policy.md').read_text(errors='replace')


if 'codex-control-plane-routing:parent' not in agents:
    errors.append('AGENTS.md lacks codex-control-plane-routing:parent marker')
if SKILL not in agents:
    errors.append('AGENTS.md does not explicitly reference the global goal-driven skill path')
if SKILL not in workflow:
    errors.append('task-workflow.md does not explicitly reference the global goal-driven skill path')
if 'command-execution-policy.md' not in index:
    errors.append('index.md does not route RTK/command execution to command-execution-policy.md')
if 'RTK is the mandatory local execution proxy' not in cmd:
    errors.append('command-execution-policy.md lacks the mandatory RTK baseline')
if SONAR_WRAPPER not in sonar:
    errors.append('sonarqube-policy.md lacks canonical sonar-with-env wrapper')
if SONAR_WRAPPER in services:
    errors.append('analysis-services-policy.md duplicates the canonical Sonar wrapper path')
if '../sonarqube-policy.md' not in services:
    errors.append('analysis-services-policy.md does not delegate Sonar to ../sonarqube-policy.md')

for q in ROOT.rglob('*'):
    if q.is_file() and q.suffix in {'.md','.toml','.py'}:
        text=q.read_text(errors='replace')
        legacy = '/root/git' + '/.codex-runtime/'
        if legacy in text:
            errors.append(f'legacy runtime root in {q.relative_to(ROOT)}')

if len(agents.splitlines()) > 150:
    errors.append('AGENTS.md exceeds 150 lines')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('V3.2 structure: OK')
