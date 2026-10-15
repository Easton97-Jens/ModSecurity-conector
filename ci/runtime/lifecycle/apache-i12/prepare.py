#!/usr/bin/env python3
"""Seal Apache-only case inputs for the existing private-runtime-v5 controller.

This prepares expectations and input hashes, never host observations or PASS.
Shared source-v5, artifacts-v3, Framework, and observers remain unchanged.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import shutil

RUN = Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle')
CASES = [
    'NEED-request-empty', 'NEED-request-single-chunk',
    'NEED-request-content-type-present', 'NEED-request-content-type-missing',
    'NEED-request-charset-present', 'NEED-request-charset-missing', 'NEED-request-csv',
    'phase4_content_type_with_charset', 'phase4_in_scope_content_type',
    'phase4_out_of_scope_content_type', 'phase4_missing_content_type',
    'phase2_at_limit', 'phase2_over_limit', 'phase2_truncated',
    'phase4_body_at_limit', 'phase4_body_over_limit',
    'phase4_body_process_partial', 'phase4_body_reject',
    'deny_header_marker_403', 'deny_request_body_marker_403',
    'phase3_deny_before_commit', 'phase3_redirect_before_commit',
    'phase4_end_of_stream_evaluation', 'duplicate_header_names',
    'duplicate_header_names_apache_core_merged',
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def supplemental(case, yaml):
    seed = RUN / 'apache-lifecycle/fixtures-v3/tests/cases/connector-specific/apache/NEED-request-eos-once.yaml'
    fixture = yaml.safe_load(seed.read_text())
    fixture['name'] = case
    fixture['title'] = 'Apache native independent case: ' + case
    fixture['metadata']['source_contract'] = 'Apache I12 supplemental host fixture; original oracle remains unchanged'
    request = fixture['request']
    request['body'] = 'apx-eos-request-payload'
    if case == 'NEED-request-empty':
        request['body'] = ''
    if case.endswith('content-type-missing'):
        request['headers'].pop('Content-Type')
    if case.endswith('charset-present'):
        request['headers']['Content-Type'] = 'text/plain; charset=utf-8'
    if case == 'NEED-request-csv':
        request['headers']['Content-Type'] = 'text/csv'
        request['body'] = 'column_a,column_b\nvalue_a,value_b\n'
    if case.startswith('phase2_'):
        fixture['rules'] += '\nSecRequestBodyLimit 64\nSecRequestBodyNoFilesLimit 64\n'
        request['body'] = 'a' * (64 if case == 'phase2_at_limit' else 65)
        if case == 'phase2_truncated':
            fixture['rules'] += 'SecRequestBodyLimitAction ProcessPartial\n'
        else:
            fixture['rules'] += 'SecRequestBodyLimitAction Reject\n'
        if case == 'phase2_over_limit':
            fixture['expect'] = {'status': 403, 'intervention': 'deny'}
    if case in ('phase4_body_process_partial', 'phase4_body_reject'):
        fixture['response']['body'] = 'a' * 65
        action = 'Reject' if case.endswith('reject') else 'ProcessPartial'
        fixture['rules'] += '\nSecResponseBodyLimit 64\nSecResponseBodyLimitAction ' + action + '\n'
        fixture['expect'] = {'status': 200, 'intervention': 'none'}
    return fixture, {'case_id': case, 'expected_oracle': None, 'origin': 'missing_host_fixture_or_oracle'}


def prepare(output, case, deduplicate_response_rule=False):
    import yaml
    output = output.resolve()
    allowed = RUN / 'apache-i12-20261015'
    if not output.is_relative_to(allowed) or output == allowed:
        raise ValueError('output must be a NEW case directory below ' + str(allowed))
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    fixtures = output / 'fixtures'
    fixtures.mkdir(mode=0o700)
    here = Path(__file__).resolve().parent
    original_case = 'duplicate_header_names' if case.endswith('_apache_core_merged') else case
    candidates = list((RUN / 'sealed-common-inputs/framework/tests/cases').rglob(original_case + '.yaml'))
    original_path = candidates[0] if candidates else None
    if original_path:
        original = yaml.safe_load(original_path.read_text())
        fixture = yaml.safe_load(original_path.read_text())
        (fixtures / 'original.yaml').write_bytes(original_path.read_bytes())
        if case == 'duplicate_header_names_apache_core_merged':
            fixture['rules'] = fixture['rules'].replace('&REQUEST_HEADERS:X-No-Crs-Duplicate "@eq 2"', '&REQUEST_HEADERS:X-No-Crs-Duplicate "@eq 1"')
            fixture['rules'] = fixture['rules'].replace('"@streq one" "t:none,chain"\nSecRule REQUEST_HEADERS:X-No-Crs-Duplicate "@streq two" "t:none"', '"@streq one, two" "t:none"')
            fixture['name'] = case
    else:
        fixture, original = supplemental(case, yaml)
    if case == 'phase4_body_process_partial':
        fixture['response']['body'] = 'a' * 65
        fixture['rules'] = re.sub(r'SecRule RESPONSE_BODY[^\n]*\n[^\n]*\n', '', fixture['rules'])
        fixture['rules'] += 'SecRule RESPONSE_BODY "@streq ' + ('a' * 64) + '" "id:91041504,phase:4,pass,log,t:none,msg:apache-i12-native-partial-64"\n'
        fixture['expect'] = {'status': 200, 'intervention': 'none',
            'audit_log': {'required': True, 'rule_id': 91041504, 'message': 'apache-i12-native-partial-64'}}
        fixture.setdefault('metadata', {})['previous_fixture_error'] = 'Previous marker oracle did not match a*65 payload; earlier sealed fixtures and their outcomes remain unchanged'
        fixture['metadata']['independent_native_oracle'] = 'libModSecurity3.0.14 src/transaction.cc1195-1206: ProcessPartial append remaining space up to SecResponseBodyLimit64; native inspection buffer64; wire outcome requires independent capture'
    if deduplicate_response_rule:
        if case not in ('phase4_body_at_limit', 'phase4_body_over_limit', 'phase4_body_reject') or not original_path:
            raise ValueError('deduplication only supports the three pinned response-limit originals')
        proof_path = RUN / 'apache-i12-20261015/native-rule-equivalence/proof.json'
        proof = json.loads(proof_path.read_text())
        record = next(value for value in proof['cases'] if value['case'] == case)
        canonical_path = RUN / 'sealed-common-inputs/framework/tests/rules/no-crs-baseline.conf'
        pattern = re.compile(r'SecRule RESPONSE_BODY[^\n]*\n[^\n]*1100301[^\n]*\n')
        local_match = pattern.search(fixture['rules'])
        canonical_match = pattern.search(canonical_path.read_text())
        if local_match is None or canonical_match is None:
            raise ValueError('expected rule1100301 not found')
        normalize = lambda text: re.sub(r'\s+', ' ', text).strip()
        if (not proof.get('all_equivalent') or not record.get('equivalent_for_exact_fixture')
                or record['comparison']['local'] != record['comparison']['canonical']
                or digest(original_path) != record['source_sha256']
                or digest(canonical_path) != proof['canonical_sha256']
                or digest(Path(proof['sdk_path'])) != proof['sdk_sha256']
                or local_match.group() != record['local_rule']
                or canonical_match.group() != record['canonical_rule']
                or normalize(canonical_match.group().replace(',t:none', '')) != normalize(local_match.group())
                or 'SecDefaultAction' in canonical_path.read_text() + fixture['rules']):
            raise ValueError('scoped native semantic-equivalence proof does not match exact current inputs')
        fixture['rules'] = pattern.sub('', fixture['rules'], count=1)
        fixture.setdefault('metadata', {})['apache_duplicate_rule_normalization'] = {
            'rule_id': 1100301, 'canonical_binding_path': '/mnt/framework/tests/rules/no-crs-baseline.conf',
            'canonical_sha256': proof['canonical_sha256'], 'native_sdk_sha256': proof['sdk_sha256'],
            'semantic_proof_sha256': digest(proof_path), 'semantic_scope': proof['scope'],
            'original_duplicate_load_failure_preserved': True,
            'reason': 'Native SDK probes show identical exact64/65-byte fixture outcomes for absent t:none and explicit t:none with no SecDefaultAction; preamble supplies canonical rule once'}
        shutil.copyfile(proof_path, fixtures / 'rule-equivalence-proof.json')
        shutil.copyfile(proof_path.with_name('probe.py'), fixtures / 'rule-equivalence-probe.py')
    # Add audit/native-body visibility without substituting original oracle values.
    common = '\nSecRequestBodyAccess On\nSecResponseBodyAccess On\nSecResponseBodyMimeType text/plain application/json\n'
    if 'SecAuditLog ' not in fixture['rules']:
        common += 'SecAuditEngine On\nSecAuditLogType Serial\nSecAuditLogParts ABHZ\nSecAuditLog "@@AUDIT_LOG@@"\nSecAuditLogStorageDir "@@AUDIT_LOG_DIR@@"\n'
    if 'SecDebugLog ' not in fixture['rules']:
        common += 'SecDebugLog "@@AUDIT_LOG_DIR@@/native-debug.log"\nSecDebugLogLevel 5\n'
    fixture['rules'] += common
    fixture['connector'] = 'apache'
    fixture.pop('nginx', None)
    fixture['status'] = 'pending'
    relative = 'tests/cases/connector-specific/apache/' + case + '.yaml'
    destination = fixtures / relative
    destination.parent.mkdir(parents=True)
    destination.write_text(yaml.safe_dump(fixture, sort_keys=False))
    for source, target in [('launch.py', 'launch.py'), ('observed_curl.py', 'observed-curl.py')]:
        shutil.copyfile(here / source, fixtures / target)
        (fixtures / target).chmod(0o500)
    shutil.copyfile(RUN / 'apache-lifecycle/fixtures-v3/curl-raw-client.py', fixtures / 'curl-raw-client.py')
    settings = {'case_id': case, 'original_selected_id': 'I12::apache-native::' + original_case,
        'fixture_relative_path': relative, 'selected_uri': fixture['request']['path'],
        'run_id': '20261015-apache-i12-' + case,
        'original_source_path': str(original_path) if original_path else None,
        'original_source_sha256': digest(original_path) if original_path else None,
        'original_expectation': original.get('expect', original.get('expected_oracle')),
        'original_nulls_preserved': True, 'observations': None,
        'canonical_no_crs_baseline': bool(original.get('no_crs_baseline')),
        'canonical_rule_preamble_file': '/mnt/framework/tests/rules/no-crs-baseline.conf' if original.get('no_crs_baseline') else None,
        'supplemental_expectation': fixture.get('expect'),
        'limitations': ['input preparation is not execution',
            'phase2_truncated uses native ProcessPartial and does not prove truncated HTTP framing']}
    (fixtures / 'settings.json').write_text(json.dumps(settings, indent=2) + '\n')
    (fixtures / 'fixture-contract.json').write_text(json.dumps({'original_selected_requirement': original,
        'supplemental_fixture': fixture, 'actual_runtime': None, 'full_lifecycle_qualification': None,
        'settings': settings}, indent=2) + '\n')
    ledger = {'files': {str(p.relative_to(fixtures)): digest(p) for p in sorted(fixtures.rglob('*')) if p.is_file()}}
    ledger_path = output / 'fixtures-ledger.json'
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + '\n')
    spec = json.loads((RUN / 'apache-lifecycle/admission-spec-v3.json').read_text())
    binding = next(item for item in spec['bindings'] if item['target'] == '/mnt/fixtures')
    binding.update(source=str(fixtures), ledger=str(ledger_path), ledger_sha256=digest(ledger_path))
    spec_path = output / 'admission-spec.json'
    spec_path.write_text(json.dumps(spec, indent=2, sort_keys=True) + '\n')
    for path in sorted(fixtures.rglob('*'), reverse=True):
        path.chmod(0o555 if path.is_dir() else (0o555 if path.name in ('launch.py', 'observed-curl.py') else 0o444))
    fixtures.chmod(0o555)
    ledger_path.chmod(0o444)
    spec_path.chmod(0o444)
    output.chmod(0o555)
    print(spec_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-input-root', type=Path)
    parser.add_argument('--case', choices=CASES)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--deduplicate-response-rule', action='store_true')
    args = parser.parse_args()
    if args.list:
        print('\n'.join(CASES))
    elif args.output_input_root is None or args.case is None:
        parser.error('--case and --output-input-root are required')
    else:
        prepare(args.output_input_root, args.case, args.deduplicate_response_rule)
