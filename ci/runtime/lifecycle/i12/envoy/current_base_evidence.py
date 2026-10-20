#!/usr/bin/env python3
"""Bind current-base native and streaming observations without qualifying IDs."""
import argparse
import json
from pathlib import Path

import evidence_io
import review_runs
import source_inventory

HERE = Path(__file__).resolve().parent
PARENT = 'a62296fb57263f9be18c6ac879e36e0ab2a9935c'
SCENARIOS = {
    'ext-proc-streaming': 'envoy-ext-proc',
    'ext-authz-request-streaming': 'envoy-ext-authz-request',
    'ext-authz-response-companion-streaming': 'envoy-ext-authz-response-companion',
}
CHECKS = {'source-head', 'source-archive', 'observer', 'accessor', 'observer-archive',
          'go-version', 'sdk-identity-build', 'sdk-identity', 'composite-build',
          'go-native', 'go-race', 'go-vet', 'native-observer-controls'}
ISOLATION_CHECKS = {'go-environment', 'go-compile-version', 'go-link-version'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bind(path, expected, references):
    ref = evidence_io.reference(path)
    require(ref['sha256'] == expected, 'physical reference changed: ' + str(path))
    references[str(path)] = ref
    return ref


def go_provenance(proof, references, allow_legacy=False, require_isolation=True):
    provenance = proof.get('go_provenance')
    if allow_legacy and provenance is None:
        return
    require(isinstance(provenance, dict), 'native Go provenance required')
    expected = 'go version go1.27.2 linux/amd64'
    require(provenance.get('required_version') == '1.27.2'
            and provenance.get('required_identity') == expected
            and provenance.get('actual_identity') == expected
            and provenance.get('verified') is True
            and proof['environment'].get('GOTOOLCHAIN') == 'local',
            'native Go provenance identity or local toolchain differs')
    configured = Path(provenance['configured_path'])
    executable = Path(provenance['executable_path'])
    evidence_io.approved_path(configured, evidence_io.DEFAULT_ROOTS)
    evidence_io.approved_path(executable, evidence_io.DEFAULT_ROOTS)
    require(configured.name == 'go' and configured.resolve(strict=True) == executable,
            'native Go configured/executable path differs')
    for check in proof['checks']:
        if check['label'] in ('go-version', 'go-native', 'go-race', 'go-vet'):
            require(check['argv'][:3] == ['rtk', 'proxy', str(configured)],
                    'native Go check executable differs')
    bind(executable, provenance['executable_sha256'], references)
    if not require_isolation:
        return
    root = executable.parent.parent
    required = {'GOROOT': str(root), 'GOOS': 'linux', 'GOARCH': 'amd64', 'GOVERSION': 'go1.27.2',
                'GOTOOLDIR': str(root / 'pkg/tool/linux_amd64')}
    require(provenance.get('required_environment') == required
            and provenance.get('actual_environment') == required
            and provenance.get('environment_output') == ''.join(value + '\n' for value in required.values())
            and all(proof['environment'].get(key) == required[key] for key in ('GOROOT', 'GOOS', 'GOARCH')),
            'isolated native Go environment differs')
    checks = {check['label']: check for check in proof['checks']}
    require(checks['go-environment']['argv'] == ['rtk', 'proxy', str(configured), 'env', *required],
            'isolated Go environment command differs')
    tools = provenance.get('tools', {})
    require(set(tools) == {'compile', 'link'}, 'both isolated Go tool identities required')
    for name, tool in tools.items():
        tool_path = root / 'pkg/tool/linux_amd64' / name
        expected_identity = name + ' version go1.27.2'
        require(tool.get('path') == str(tool_path)
                and tool.get('required_identity') == expected_identity
                and tool.get('actual_identity') == expected_identity
                and checks['go-' + name + '-version']['argv'] == ['rtk', 'proxy', str(tool_path), '-V'],
                'isolated Go compiler/linker identity differs')
        bind(tool_path, tool['sha256'], references)


def native_evidence(path, references, go_version='1.27.2', allow_legacy=False):
    proof = evidence_io.read_json(path)
    bind(path, evidence_io.reference(path)['sha256'], references)
    require(proof.get('actual_source_commit') == PARENT, 'current-base native revision differs')
    require(proof.get('status') == 'pass' and proof.get('build_ready') is True
            and proof.get('host_launched') is False,
            'current-base native checks must pass')
    expected_checks = CHECKS if allow_legacy else CHECKS | ISOLATION_CHECKS
    require({check['label'] for check in proof['checks']} == expected_checks
            and len(proof['checks']) == len(expected_checks)
            and all(check['exit_code'] == 0 for check in proof['checks']),
            'complete native check set required')
    go_provenance(proof, references, allow_legacy)
    for check in proof['checks']:
        for channel in ('stdout', 'stderr'):
            bind(path.parent / (check['label'] + '.' + channel),
                 check[channel + '_sha256'], references)
    if not allow_legacy:
        provenance = proof['go_provenance']
        require(evidence_io.read_bytes(path.parent / 'go-environment.stdout')
                == provenance['environment_output'].encode(), 'physical Go environment output differs')
        for name, tool in provenance['tools'].items():
            require(evidence_io.read_bytes(path.parent / ('go-' + name + '-version.stdout'))
                    == (tool['actual_identity'] + '\n').encode(), 'physical Go tool identity output differs')
    source = Path(proof['source_copy'])
    require(source_inventory.verify(source, proof) == proof['complete_source_inventory'],
            'native source inventory differs')
    for name, sha in proof['module_inputs'].items():
        bind(source / 'connectors/envoy/ext_proc' / name, sha, references)
    module = evidence_io.read_bytes(source / 'connectors/envoy/ext_proc/go.mod')
    require(b'golang.org/x/net v0.61.0' in module, 'patched x/net identity differs')
    require(evidence_io.read_bytes(path.parent / 'go-version.stdout').strip()
            == ('go version go' + go_version + ' linux/amd64').encode(), 'current Go identity differs')
    require(evidence_io.read_bytes(source / '.go-version').strip() == b'1.27.2',
            'archived Base Go version differs')
    require(evidence_io.read_bytes(path.parent / 'sdk-identity.stdout').strip()
            == b'ModSecurity v3.0.14 (Linux)', 'current SDK identity differs')
    require(proof['sdk_library'] == {
        'path': '/usr/lib/x86_64-linux-gnu/libmodsecurity.so',
        'sha256': '32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407'},
        'native SDK library identity differs')
    require(len(proof['binaries']) == 2, 'both native host binaries required')
    for name, sha in proof['binaries'].items():
        bind(path.parent / name, sha, references)
        bind(Path(proof['host_ready_binaries']) / Path(name).name, sha, references)
    return proof


def rejected_native_evidence(path, references):
    proof = evidence_io.read_json(path)
    receipt = bind(path, evidence_io.reference(path)['sha256'], references)
    require(proof.get('actual_source_commit') == PARENT and proof.get('host_launched') is False
            and proof.get('status') == 'failed' and 'build_ready' not in proof and 'binaries' not in proof,
            'rejected native must be an exact-base pre-host build failure')
    checks = proof['checks']
    labels = CHECKS - {'go-native', 'go-race', 'go-vet', 'native-observer-controls'}
    require(len(checks) == len(labels) and {check['label'] for check in checks} == labels
            and checks[-1]['label'] == 'composite-build' and checks[-1]['exit_code'] != 0
            and all(check['exit_code'] == 0 for check in checks[:-1]),
            'rejected native must retain sole terminal composite-build failure')
    go_provenance(proof, references, require_isolation=False)
    for check in checks:
        for channel in ('stdout', 'stderr'):
            bind(path.parent / (check['label'] + '.' + channel), check[channel + '_sha256'], references)
    require(evidence_io.read_bytes(path.parent / 'go-version.stdout')
            == b'go version go1.27.2 linux/amd64\n', 'rejected native driver identity differs')
    diagnostic = b'compile: version "go1.27.3" does not match go tool version "go1.27.2"'
    require(diagnostic in evidence_io.read_bytes(path.parent / 'composite-build.stderr'),
            'rejected native lacks physical compiler/tool mismatch')
    require(source_inventory.verify(Path(proof['source_copy']), proof) == proof['complete_source_inventory'],
            'rejected native source inventory differs')
    return {'classification': 'rejected_toolchain_isolation', 'receipt': receipt,
            'host_launched': False, 'status': 'failed', 'failure_check': 'composite-build',
            'driver_go': '1.27.2', 'compiler_go': '1.27.3', 'original_oracle_case_ids': [],
            'oracle_progress_assigned': False, 'new_lifecycle_pass': 0}


def nonqualification(review):
    require(review.get('parent_sha') == PARENT, 'current-base review revision differs')
    require(review.get('host_lifecycle_qualified') is False
            and review.get('oracle_progress_assigned') is False,
            'review cannot qualify original oracles')
    rows = review['scenarios']
    require(len(rows) == 3 and {row['scenario']: row['route'] for row in rows} == SCENARIOS,
            'exactly three current-base route scenarios required')
    require(all(row.get('original_oracle_case_ids') == []
                and row.get('host_lifecycle_qualified') is False for row in rows),
            'original ID injection or lifecycle qualification prohibited')


def observed_contract(row, proof):
    controller = row['controller']
    require(row['runner_exit_code'] == 0 and row['observation_state'] == 'driver_result_observed'
            and row['artifact_integrity_issues'] == []
            and controller == {'exitcode': 0, 'controller_exitcode': 0, 'timeout': False,
                'supervisor_reaped': True, 'resource_violation': None, 'namespace_pin_verified': True,
                'error_count': 0, 'surviving_namespace_pid_count': 0,
                'outside_mount_leak_count': 0, 'executed_input_hashes_unchanged': True}
            and row['driver']['remaining_owned_process_count'] == 0,
            'current-base cleanup or physical integrity differs')
    require(row['build']['source_git_baseline'] == PARENT
            and row['source_equality']['source_contract_parent_sha'] == PARENT
            and row['source_equality']['complete_archived_build_inventory_verified'] is True
            and row['build']['engine_sha256'] in proof['binaries'].values(),
            'host/native source or binary binding differs')
    images = row['loaded_images']
    require(set(images) == {'before-request', 'after-target', 'after-neighbor'}
        and all(isinstance(snapshot, dict) and {'engine', 'envoy'} <= set(snapshot) and all(
        image.get('matches_build_manifest') is True
        and (name != 'engine' or image.get('sdk_matches_native_build') is True)
        for name, image in snapshot.items() if name in ('engine', 'envoy'))
        for snapshot in images.values()), 'loaded host/native image identity differs')
    for role, request, response in (('target', 95, 96), ('neighbor', 6, 7)):
        client = row['clients'][role]
        require(client['request_body_bytes'] == request and client['response_body_bytes'] == response
                and client['raw_http_status'] == 200 and client['process_exit'] == 0
                and client['independent_raw_response']['framing_complete'] is True
                and client['request_body_hash_verified'] is True
                and client['response_body_hash_verified'] is True,
                'current-base client bytes or completion differ')
        transport = row['grpc_transport'][role]
        require(transport['process']['remote_grpc_status'] is None
                and transport['process']['successful_grpc_completion'] is False,
                'missing Process status cannot become successful completion')
        authorization = transport['authorization']
        unknown = (authorization['remote_grpc_status'] is None
                   and authorization['successful_grpc_completion'] is False
                   and authorization['classification'] == 'unknown')
        explicit = (row['route'] != 'envoy-ext-proc'
                    and authorization['remote_grpc_status'] == 0
                    and authorization['successful_grpc_completion'] is True
                    and authorization['classification'] == 'explicit_remote_status_and_close')
        require(unknown or explicit,
                'Authorization completion requires its explicit scoped status')
    backend = row['backend']
    require(backend['request_count'] == 2 and backend['request_count_is_lower_bound'] is False
            and backend['completed_receipt_count'] == 2
            and {(x['role'], x['request_body_bytes'], x['response_body_bytes'])
                 for x in backend['requests']} == {('target', 95, 96), ('neighbor', 6, 7)},
            'two independently measured backend requests required')
    versions = row['versions']
    require(versions['go-version']['identity'] == 'go version go1.27.3 linux/amd64'
            and versions['sdk-who']['identity'] == 'ModSecurity v3.0.14 (Linux)'
            and '/1.39.1/Clean/RELEASE/BoringSSL' in versions['host-version']['identity']
            and all(x['command_exit_code'] == 0 for x in versions.values()),
            'current host runtime identities differ')


def review_evidence(path, proof, admission, references):
    review = evidence_io.read_json(path)
    bind(path, evidence_io.reference(path)['sha256'], references)
    nonqualification(review)
    snapshot = Path(review['runs_snapshot'])
    bind(snapshot, review['runs_sha256'], references)
    runs = evidence_io.read_json(snapshot)
    require(runs['parent_sha'] == PARENT and len(runs['runs']) == 3,
            'runner source scope differs')
    helpers = Path(proof['source_copy']) / '.i12-capture/envoy'
    transport, capture, hashes = review_runs.parser_modules(helpers)
    require(hashes == review['helper_sha256'], 'capture helper identity differs')
    bind(HERE / 'transport.py', review['transport_wrapper_sha256'], references)
    for name, sha in hashes.items():
        bind(helpers / name, sha, references)
    review_runs.BINDING_CACHE.clear()
    actual = []
    for record in runs['runs']:
        label = record['case']['label']
        for channel in ('stdout', 'stderr'):
            bind(snapshot.parent / ('runs-' + label + '.' + channel),
                 record[channel + '_sha256'], references)
        row = review_runs.review_run(record, transport, capture, PARENT)
        actual.append(row)
        if admission:
            require(row['runner_exit_code'] == 77
                    and row['observation_state'] == 'controller_admission_failed_or_unknown'
                    and 'controller' not in row and 'driver' not in row and 'attempt' not in row,
                    'admission failure cannot claim execution or cleanup')
        else:
            observed_contract(row, proof)
            attempt = Path(row['attempt'])
            bind(attempt / 'controller-result.json', row['controller_result_sha256'], references)
            bind(attempt / 'retained-original-ownership.json', row['handoff_receipt_sha256'], references)
            controller = evidence_io.read_json(attempt / 'controller-result.json')
            spec_path = Path(record['case']['spec'])
            bind(spec_path, controller['spec_sha256'], references)
            for name, sha in controller['executed_input_hashes_before'].items():
                # Configuration ownership belongs to the controller; never read private configuration.
                if '.codex' not in Path(name).parts:
                    bind(Path(name), sha, references)
            spec = evidence_io.read_json(spec_path)
            for binding in spec['bindings']:
                bind(Path(binding['ledger']), binding['ledger_sha256'], references)
            for name, metadata in row['physical_files'].items():
                bind(attempt / 'data' / name, metadata['sha256'], references)
    require(actual == review['scenarios'], 'physical review differs from independent replay')
    return review


def produce(native, admission_review, review, superseded_native, superseded_review, rejected_native):
    references = {}
    proof = native_evidence(native, references)
    previous = native_evidence(superseded_native, references, '1.27.3', allow_legacy=True)
    rejected = rejected_native_evidence(rejected_native, references)
    failed = review_evidence(admission_review, previous, True, references)
    superseded = review_evidence(superseded_review, previous, False, references)
    observed = review_evidence(review, proof, False, references)
    return {'schema': 'i12.envoy.current-base-evidence.v1', 'parent_sha': PARENT,
            'host_lifecycle_qualified': False, 'oracle_progress_assigned': False,
            'original_oracle_case_ids': [], 'new_lifecycle_pass': 0,
            'toolchains': {'required_engine_build_go': '1.27.2', 'actual_engine_build_go': '1.27.2',
                'host_environment_go': '1.27.3',
                'host_go_scope': 'installed_host_probe_not_engine_build_toolchain'},
            'route_transport_observations': {row['route']: row['grpc_transport']
                                             for row in observed['scenarios']},
            'inputs': {name: evidence_io.reference(path) for name, path in (
                ('native', native), ('admission_review', admission_review), ('review', review),
                ('superseded_native', superseded_native), ('superseded_review', superseded_review),
                ('rejected_native', rejected_native))},
            'rejected_native': rejected,
            'admission_failures': failed['scenarios'], 'observations': observed['scenarios'],
            'superseded': {'classification': 'wrong_toolchain_nonqualifying',
                'engine_build_go': '1.27.3', 'required_engine_build_go': '1.27.2',
                'host_environment_go': '1.27.3',
                'original_oracle_case_ids': [], 'oracle_progress_assigned': False,
                'new_lifecycle_pass': 0, 'observations': superseded['scenarios']},
            'physical_references': references}


def validate(path):
    supplement = evidence_io.read_json(path)
    inputs = supplement['inputs']
    for ref in inputs.values():
        require(evidence_io.reference(Path(ref['path'])) == ref, 'supplement input changed')
    actual = produce(*(Path(inputs[key]['path']) for key in (
        'native', 'admission_review', 'review', 'superseded_native', 'superseded_review', 'rejected_native')))
    require(supplement == actual, 'current-base supplement differs from fresh validation')
    return actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('native', 'admission-review', 'review', 'superseded-native', 'superseded-review', 'rejected-native', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    result = produce(args.native, args.admission_review, args.review,
                     args.superseded_native, args.superseded_review, args.rejected_native)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'output': str(args.output), 'new_lifecycle_pass': 0}))


if __name__ == '__main__':
    main()
