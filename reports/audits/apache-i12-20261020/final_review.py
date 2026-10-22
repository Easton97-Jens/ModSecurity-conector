"""Conservative Apache-only decisions over retained physical I12 captures.

This is a Root review procedure, not a host runner or an oracle generator.
Only explicitly registered bounded families can qualify. Every other original
ID remains present with a null decision. A verified separate oracle review is
needed when the immutable original oracle is unresolved. Config/parser controls
use the separate review_controls procedure and are never promoted here.
"""
import argparse
import base64
import collections
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[3]
RESPONSE_RAW = 'response.raw'


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BATCH = load('apache_final_batch', 'ci/runtime/lifecycle/apache-i12/acceptance/review_batch.py')
L = BATCH.REVIEW.LEDGER
O = L.ORACLES
SHARED = L.SHARED
SUPPORTED = frozenset((
    'NEED-request-empty', 'NEED-request-single-chunk',
    'NEED-request-csv',
    'NEED-request-eos-once',
))
NATIVE_HEADER_MAPPING_GAPS = frozenset((
    'NEED-request-content-type-present', 'NEED-request-content-type-missing',
    'NEED-request-charset-present', 'NEED-request-charset-missing',
))
# These lifecycle expectations concern request-body processing, independently of
# the P1 sentinel rule used to prove the exact input reached this transaction.
ORACLE_LIFECYCLE_PHASE = {
    'NEED-request-empty': 2,
    'NEED-request-single-chunk': 2,
    'NEED-request-csv': 2,
    'NEED-request-eos-once': 2,
}
CHECKS = frozenset((
    'one_timed_typed_host_association', 'successful_actual_allocation_join',
    'no_invalid_main_observer_rows', 'one_clean_native_observer_final',
    'controller_cleanup_clean', 'native_cleanup_exactly_once',
    'common_finish_exactly_once', 'common_cleanup_exactly_once',
    'fd_snapshots_same_pid_starttime', 'maps_snapshot_hash_matches_sampler',
    'status_snapshot_hash_matches_sampler', 'sdk_and_observed_module_loaded',
    'loaded_images_match_actual_admission',
))
SUPPORTED_ORACLE_SCOPE = 'Apache bounded request raw-byte lifecycle; no streaming, native-file, limit or sibling-case claim.'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_ref(reference):
    verified = O.verify_reference(reference)
    return json.loads(Path(verified['path']).read_text())


def refs_in(value):
    """Do not stop walking at reference-shaped containers (wrapper bait)."""
    result = []
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and 'sha256' in value:
            result.append(O.verify_reference(value))
        for item in value.values():
            result.extend(refs_in(item))
    elif isinstance(value, list):
        for item in value:
            result.extend(refs_in(item))
    return result


def physical_inventory(*values):
    """Freeze transitive JSON references, including externally reviewed oracles."""
    pending = [ref for value in values for ref in refs_in(value)]
    result = {}
    while pending:
        ref = pending.pop()
        key = (ref['path'], ref['sha256'])
        if key in result:
            continue
        if len(result) >= 10000:
            raise ValueError('Physical evidence graph exceeds bounded review inventory')
        result[key] = ref
        path = Path(ref['path'])
        if path.suffix == '.json':
            if path.stat().st_size > 64 * 1024 * 1024:
                raise ValueError('JSON evidence exceeds bounded review size')
            pending.extend(refs_in(json.loads(path.read_text())))
    return list(result.values())


def bytes_input(value):
    if value.get('encoding') != 'base64':
        raise ValueError('Only explicitly bound base64 fixture bytes are supported')
    data = base64.b64decode(value['data'], validate=True)
    if value.get('bytes') != len(data) or value.get('sha256') != digest(data):
        raise ValueError('Fixture bytes/hash differ')
    return data


def predicate(name, passed, reason, references=()):
    if passed is not None and type(passed) is not bool:
        raise ValueError('Predicate must be true, false or unknown')
    result = None
    if passed is not None:
        result = 'PASS' if passed else 'FAIL'
    return {'name': name, 'result': result,
            'reason': reason, 'physical_references': list(references)}


def values(packet):
    return {name: item.get('value') for name, item in packet.get('observations', {}).items()}


def evidence(packet, *names):
    return [ref for name in names for ref in packet['observations'].get(name, {}).get('evidence', [])]


def identity_matches(packet, expected):
    if any(packet.get(key) != expected[key] for key in ('run_id', 'parent_sha', 'framework_sha', 'mrts_sha')):
        return False
    host = values(packet).get('product_host_identity') or {}
    apache = host.get('apache_binary', {})
    if apache.get('sha256') != expected['apache_sha256']:
        return False
    images = host.get('mapped_images', [])
    for name, key in (('mod_security3.so', 'module_sha256'), ('libmodsecurity.so', 'sdk_sha256')):
        selected = [row for row in images if name in row.get('mapped_path', '')]
        if not selected or any(row.get('sha256') != expected[key]
                               or row.get('admission_sha256_matches') is not True for row in selected):
            return False
    return host.get('actual_uid') == host.get('actual_gid') == 65534


def complete_measurements(packet, packet_path):
    if set(packet.get('observations', {})) != set(SHARED.ROLES):
        return False
    for name, item in packet['observations'].items():
        _, complete = SHARED.measurement(name, item, packet_path)
        # These bounded full-host families have no nonapplicable lifecycle roles.
        if not complete or item.get('applicable', True) is not True or item.get('value') is None:
            return False
    return True


def check_wire(plan, packet):
    refs = evidence(packet, 'client_bytes')
    request_refs = [item for item in refs if Path(item['path']).name == 'request.raw']
    response_refs = [item for item in refs if Path(item['path']).name == RESPONSE_RAW]
    if len(request_refs) != 1 or len(response_refs) != 1:
        return False
    request = Path(request_refs[0]['path']).read_bytes()
    response = Path(response_refs[0]['path']).read_bytes()
    head, sep, body = request.partition(b'\r\n\r\n')
    expected = plan['request']
    if not sep or head.split(b'\r\n')[0] != (expected['method'] + ' ' + expected['path'] + ' HTTP/1.1').encode():
        return False
    if body != bytes_input(expected['body']):
        return False
    fields = [line.split(b':', 1) for line in head.split(b'\r\n')[1:]]
    types = [value.strip().decode('latin1') for key, value in fields if key.lower() == b'content-type']
    expected_types = [value for key, value in expected['headers'] if key.lower() == 'content-type']
    if types != expected_types:
        return False
    request_lengths = [value.strip() for key, value in fields if key.lower() == b'content-length']
    if (request_lengths != [str(len(body)).encode()]
            or any(key.lower() == b'transfer-encoding' for key, _ in fields)):
        return False
    _, separator, entity = response.partition(b'\r\n\r\n')
    headers = BATCH.wire_headers(response)
    if not separator or headers is None or headers['status'] != plan['candidate_expectation']['visible_status']:
        return False
    response_body = bytes_input(plan['backend']['body'])
    lengths = [value for key, value in headers['headers'] if key.lower() == 'content-length']
    if (lengths != [str(len(response_body))] or entity != response_body
            or any(key.lower() == 'transfer-encoding' for key, _ in headers['headers'])):
        return False
    v = values(packet)
    return (v['client_exit'] == 0 and v['client_signal']['actual_signal'] is None
            and v['client_headers']['status'] == headers['status']
            and v['client_bytes']['request_wire'] == len(request)
            and v['client_bytes']['response_wire'] == len(response)
            and v['client_bytes']['response_entity'] == len(entity)
            and v['client_sha256']['request_wire'] == digest(request)
            and v['client_sha256']['response_wire'] == digest(response)
            and v['client_sha256']['response_entity'] == digest(entity)
            and v['transport_framing']['kind'] == 'content_length'
            and v['transport_framing']['content_lengths'] == lengths
            and v['transport_framing']['transfer_encoding'] == []
            and v['transport_framing']['decoded_entity_bytes'] == len(entity)
            and v['transport_reset_scope'] == {'tcp_eof_observed': True, 'tcp_reset_observed': False,
                                              'timeout_observed': False, 'error': None})


def check_backend(plan, v):
    actual = v['backend_payload_identity']
    rows = actual['physical_transcript']
    arrivals = [row for row in rows if row.get('kind') == 'request_arrival']
    complete = [row for row in rows if row.get('kind') == 'request']
    eos = [row for row in rows if row.get('kind') == 'backend_eos_write']
    request, response = bytes_input(plan['request']['body']), bytes_input(plan['backend']['body'])
    return (v['backend_request_count']['main'] == plan['candidate_expectation']['backend_requests'] == 1
            and len(arrivals) == len(complete) == len(eos) == 1
            and len({row['request_id'] for row in rows}) == 1
            and complete[0]['uri'] == plan['request']['path']
            and complete[0]['method'] == plan['request']['method']
            and complete[0]['body_bytes'] == len(request) and complete[0]['body_sha256'] == digest(request)
            and eos[0]['body_bytes'] == len(response) and eos[0]['body_sha256'] == digest(response))


def check_native(plan, v):
    phases = [(row.get('phase'), row.get('result')) for row in v['native_phases']
              if row.get('phase') in (1, 2, 3, 4)]
    if phases != [(1, 1), (2, 1), (3, 1), (4, 1)]:
        return False
    chunks = v['native_body_chunks']
    for function, payload in (('native_append_request_body', bytes_input(plan['request']['body'])),
                              ('native_append_response_body', bytes_input(plan['backend']['body']))):
        selected = [row for row in chunks if row.get('function') == function]
        if any(type(row.get('input_size')) is not int or row['input_size'] < 0
               or row.get('result') != 1 for row in selected):
            return False
        if sum(row['input_size'] for row in selected) != len(payload):
            return False
        if function == 'native_append_request_body' and plan['case_id'] == 'NEED-request-single-chunk' and len(selected) != 1:
            return False
    interventions = v['native_intervention_or_first_cause']['actual_native_intervention_returns']
    return bool(interventions) and all(row.get('result') == 0 for row in interventions)


def check_events(plan, v):
    events = v['native_events']
    audit = events['native_audit_lines']
    rule = str(plan['candidate_expectation']['native_rule_id'])
    phase = plan['candidate_expectation']['native_phase']
    if not audit or sum(block.count('[id "' + rule + '"]') for block in audit) != 1:
        return False
    if phase != 1 or plan['candidate_expectation']['visible_status'] != 200:
        return False
    blocks = BATCH.audit_records('\n'.join(audit), v['native_transaction_id']['transaction_id'])
    if len(blocks) != 1 or not blocks[0]['complete_Z_section']:
        return False
    common = events['physical_common_rows']
    if not common or events['common_sink_mode'] != '0o600':
        return False
    if any(row.get('actual_action') != 'allow' or row.get('event') != 'rule_match' for row in common):
        return False
    expected_events = [row for row in common if row.get('rule_id') == rule]
    if (len(expected_events) != 1 or expected_events[0].get('phase') != 'request_headers'
            or expected_events[0].get('transaction_id') != v['common_transaction_id']['transaction_id']
            or expected_events[0].get('connector') != 'apache'
            or expected_events[0].get('integration_mode') != 'native-httpd-module'
            or expected_events[0].get('method') != plan['request']['method']
            or expected_events[0].get('uri') != plan['request']['path']):
        return False
    required = plan['original_oracle'].get('event_fields', [])
    return (all(all(field in row for field in required) for row in common)
            and v['terminal_event_count']['actual_common_terminal_subset_count'] == 0)


def check_eos_finish(v):
    eos = collections.Counter(row.get('kind') for row in v['host_eos']['actual_apr_eos_rows'])
    return (eos == {'actual_request_apr_eos': 1, 'actual_response_apr_eos': 1}
            and len(v['native_eos']['native_request_finalization_returns']) == 1
            and len(v['native_eos']['native_response_finalization_returns']) == 1
            and v['finish_calls'] == {'common_finish': 1, 'native_logging': 1}
            and v['native_free_calls'] == {'native_cleanup': 1, 'common_cleanup': 1, 'host_association_retire': 1}
            and v['finish_transitions']['completed_status_3_transitions'] == 1)


def principal_physical_api(packet):
    references = evidence(packet, 'native_api_returns')
    selected = {item['path']: item for item in references if Path(item['path']).name == 'native-api.jsonl'}
    if len(selected) != 1:
        raise ValueError('Exactly one actual native-api.jsonl producer is required')
    ref = O.verify_reference(next(iter(selected.values())))
    association = values(packet)['observed_handle_association']['host_association']
    rows = BATCH.REVIEW.json_lines(Path(ref['path']))
    return [row for row in rows if row.get('pid') == association['pid']
            and row.get('run') == packet['run_id']
            and row.get('allocation_scope_call') == association['allocation_scope_call']
            and row.get('allocation_scope_kind') == 'host']


def paired_native_operation(rows, function):
    entries = [row for row in rows if row.get('function') == function and row.get('edge') == 'enter']
    returns = [row for row in rows if row.get('function') == function and row.get('edge') == 'return']
    if len(entries) != 1 or len(returns) != 1:
        raise ValueError('Exactly one paired physical call required: ' + function)
    entry, returned = entries[0], returns[0]
    if (type(entry.get('call')) is not int or entry['call'] <= 0 or entry['call'] != returned.get('call')
            or 'result' not in entry or 'result' not in returned
            or type(entry.get('sequence')) is not int or type(returned.get('sequence')) is not int
            or entry['sequence'] >= returned['sequence']
            or type(entry.get('monotonic_ns')) is not int or type(returned.get('monotonic_ns')) is not int
            or entry['monotonic_ns'] >= returned['monotonic_ns']
            or entry.get('invalid') is not False or returned.get('invalid') is not False):
        raise ValueError('Invalid actual call/sequence/time pairing: ' + function)
    return entry, returned


def eos_precedes_native(eos, operation, association):
    entry, _ = operation
    return (eos.get('pid') == association['pid']
            and eos.get('allocation_scope_call') == association['allocation_scope_call']
            and eos.get('actual_apr_bucket_is_eos') is True and eos.get('invalid') is False
            and type(eos.get('monotonic_ns')) is int and eos['monotonic_ns'] < entry['monotonic_ns']
            and type(eos.get('sequence')) is int)


def check_lifecycle_order(packet):
    v = values(packet)
    rows = principal_physical_api(packet)
    functions = ('native_process_request_body', 'native_process_response_body', 'common_finish',
                 'native_process_logging', 'common_cleanup', 'native_cleanup', 'host_association_retire')
    operations = {name: paired_native_operation(rows, name) for name in functions}
    p2, p4 = operations['native_process_request_body'], operations['native_process_response_body']
    eos = v['host_eos']['actual_apr_eos_rows']
    request = [row for row in eos if row.get('kind') == 'actual_request_apr_eos']
    response = [row for row in eos if row.get('kind') == 'actual_response_apr_eos']
    if len(request) != 1 or len(response) != 1:
        return False
    association = v['observed_handle_association']['host_association']
    if not (eos_precedes_native(request[0], p2, association)
            and eos_precedes_native(response[0], p4, association)
            and request[0]['sequence'] < response[0]['sequence']
            and p2[1]['monotonic_ns'] < response[0]['monotonic_ns']):
        return False
    if (v['native_eos']['native_request_finalization_returns'] != [p2[1]]
            or v['native_eos']['native_response_finalization_returns'] != [p4[1]]
            or v['commit_order']['native_p4_edges'] != list(p4)):
        return False
    return cleanup_after_physical_commit(v, operations, p4)


def cleanup_after_physical_commit(v, operations, p4):
    calls = v['commit_order']['physical_socket_observation']['actual_socket_call_brackets']
    if not calls or any(type(row.get('entered_ns')) is not int or type(row.get('return_ns')) is not int
                        or row['entered_ns'] < p4[1]['monotonic_ns']
                        or row['return_ns'] < row['entered_ns'] for row in calls):
        return False
    last_time = max(row['return_ns'] for row in calls)
    previous = p4[1]
    for name, result in (('common_finish', 0), ('native_process_logging', 1), ('common_cleanup', 0),
                         ('native_cleanup', None), ('host_association_retire', 1)):
        entry, returned = operations[name]
        if (entry['monotonic_ns'] <= last_time or entry['call'] <= previous['call']
                or entry['sequence'] <= previous['sequence'] or returned.get('result') != result):
            return False
        previous, last_time = returned, returned['monotonic_ns']
    return True


def check_commit(v):
    commit = v['commit_order']
    physical = commit['physical_socket_observation']
    p4 = [row for row in commit['native_p4_edges'] if row.get('edge') == 'return']
    calls = physical['actual_socket_call_brackets']
    flags = commit['internal_committed_flag_returns']
    return (len(p4) == 1 and p4[0].get('result') == 1 and bool(calls) and bool(flags)
            and all(type(row.get('entered_ns')) is int and row['entered_ns'] >= p4[0]['monotonic_ns']
                    and row.get('return_ns', -1) >= row['entered_ns'] for row in calls)
            and len(flags) == 1 and flags[0].get('result') == 0
            and flags[0].get('argument_committed') == 1)


def check_cleanup(v):
    process = v['process_listener_cleanup']
    receipts = v['cleanup_receipts']
    finals = receipts['actual_native_observer_finals']
    differences = v['descriptor_cleanup']['actual_fd_differences']
    return (process['supervisor_reaped'] is True and process['surviving_namespace_pids'] == []
            and process['outside_mount_leaks'] == [] and process['errors'] == []
            and process['exitcode'] == process['controller_exitcode'] == 0
            and receipts['sampler_thread_stopped'] is True and receipts['sampler_errors'] == []
            and len(finals) == 1 and finals[0]['pending_calls'] == finals[0]['live_mappings'] == 0
            and set(differences) == {'main', 'neighbor'}
            and all(not row[key] for row in differences.values() for key in ('added', 'removed', 'changed')))


def check_neighbor(v):
    neighbor = v['neighbor_health']
    main = v['observed_handle_association']['host_association']
    associated = neighbor['actual_host_association']
    return (neighbor['same_native_host_pid'] is True and associated['pid'] == main['pid']
            and associated['allocation_scope_call'] != main['allocation_scope_call']
            and neighbor['separate_actual_client']['status'] == 200
            and neighbor['actual_waited_process'].get('waited_exit') == 0
            and len(neighbor['independent_backend']) == 1)


def check_native_identity(v, expected):
    association = v['observed_handle_association']['host_association']
    rows = v['native_api_returns']
    return bool(rows) and all(row.get('run') == expected['run_id']
                             and row.get('pid') == association['pid']
                             and row.get('allocation_scope_call') == association['allocation_scope_call']
                             and row.get('allocation_scope_kind') == 'host' for row in rows)


def check_registered_oracle_lifecycle(plan, packet):
    phase = ORACLE_LIFECYCLE_PHASE[plan['case_id']]
    rows = [row for row in values(packet)['native_phases'] if row.get('phase') == phase]
    return (len(rows) == 1 and rows[0].get('function') == 'native_process_request_body'
            and rows[0].get('edge') == 'return' and rows[0].get('result') == 1)


def check_registered_fixture(plan):
    name = plan['case_id']
    if name == 'NEED-request-empty':
        body = b''
    elif name == 'NEED-request-csv':
        body = b'column_a,column_b\nvalue_a,value_b\n'
    else:
        body = b'Apache-I12-request-payload'
    content_type = 'text/csv' if name == 'NEED-request-csv' else 'text/plain'
    types = [value for key, value in plan['request']['headers'] if key.lower() == 'content-type']
    expected = plan['candidate_expectation']
    return (bytes_input(plan['request']['body']) == body
            and bytes_input(plan['backend']['body']) == b'Apache I12 healthy body\n'
            and types == [content_type]
            and plan['request']['method'] == 'POST' and plan['request']['path'] == '/i12/' + name
            and plan['request']['framing'] == plan['backend']['framing'] == 'content_length'
            and plan['request']['peer_action'] == 'normal'
            and not plan.get('fault') and not plan.get('driver_seams')
            and expected['visible_status'] == 200 and expected['native_rule_id'] == 91041950
            and expected['native_phase'] == 1 and expected['backend_requests'] == 1)


def control_references(packet):
    driver = packet.get('driver_execution', {}).get('reference')
    if not driver:
        return []
    root = Path(driver['path']).parent
    return [O.reference(root / label / filename) for label in ('followup', 'neighbor')
            for filename in ('receipt.json', 'process.command.json', RESPONSE_RAW)
            if (root / label / filename).is_file()]


def check_controls(plan, packet):
    driver = packet['driver_execution']['reference']
    root = Path(driver['path']).parent
    transcript_path = root / 'backend/requests.jsonl'
    transcript = BATCH.REVIEW.json_lines(transcript_path)
    controls = plan['controls']
    if [item['label'] for item in controls] != ['followup', 'neighbor']:
        return False
    for control in controls:
        directory = root / control['label']
        receipt = json.loads((directory / 'receipt.json').read_text())
        process = json.loads((directory / 'process.command.json').read_text())
        raw = (directory / RESPONSE_RAW).read_bytes()
        headers = BATCH.wire_headers(raw)
        body = bytes_input(control['backend_body'])
        if (receipt['path'] != control['path'] or receipt['method'] != control['method']
                or receipt['status'] != control['expected_status'] or control['expected_status'] != 200
                or process['waited_exit'] != 0 or headers is None or headers['status'] != 200
                or raw.partition(b'\r\n\r\n')[2] != body or receipt['entity_sha256'] != digest(body)):
            return False
        rows = [row for row in transcript if row.get('kind') == 'request'
                and row.get('uri') == control['path']
                and receipt['started_ns'] <= row.get('monotonic_ns', -1) <= receipt['completed_ns']]
        if len(rows) != 1 or rows[0]['method'] != control['method']:
            return False
    return True


def host_predicates(plan, packet):
    """Explicit family registry; no unknown ID can inherit these predicates."""
    if plan['case_id'] not in SUPPORTED:
        return [predicate('registered_case_semantics', None, 'No independently implemented family predicate for this original ID.')]
    v = values(packet)
    functions = (
        ('registered_fixture_identity', lambda: check_registered_fixture(plan), ()),
        ('wire_status_bytes_mime_charset', lambda: check_wire(plan, packet), ('client_bytes', 'client_sha256', 'client_headers')),
        ('independent_backend_payload', lambda: check_backend(plan, v), ('backend_payload_identity', 'backend_request_count')),
        ('native_phases_appendbytes_and_allow', lambda: check_native(plan, v), ('native_phases', 'native_body_chunks', 'native_intervention_or_first_cause')),
        ('registered_oracle_lifecycle_phase', lambda: check_registered_oracle_lifecycle(plan, packet), ('native_phases',)),
        ('native_rule_and_physical_jsonl', lambda: check_events(plan, v), ('native_events', 'terminal_event_count')),
        ('eos_finish_and_free', lambda: check_eos_finish(v), ('host_eos', 'native_eos', 'finish_calls', 'native_free_calls', 'finish_transitions')),
        ('physical_eos_p2_p4_commit_finish_free_order', lambda: check_lifecycle_order(packet),
         ('host_eos', 'native_eos', 'native_api_returns', 'commit_order')),
        ('p4_before_physical_commit', lambda: check_commit(v), ('commit_order',)),
        ('process_descriptor_cleanup', lambda: check_cleanup(v), ('process_listener_cleanup', 'descriptor_cleanup', 'cleanup_receipts')),
        ('separate_healthy_neighbor_identity', lambda: check_neighbor(v), ('neighbor_health', 'observed_handle_association')),
        ('physical_followup_and_neighbor_controls', lambda: check_controls(plan, packet), ('neighbor_health',)),
    )
    result = []
    for name, function, fields in functions:
        try:
            passed = function()
            reason = 'Physical family predicate evaluated.'
        except (KeyError, TypeError, ValueError, OSError, IndexError) as error:
            passed, reason = None, 'Missing or unsupported physical shape: ' + str(error)
        result.append(predicate(name, passed, reason, evidence(packet, *fields)))
    result[-1]['physical_references'].extend(control_references(packet))
    return result


def validate_inputs(baseline, plan, index):
    rows = L.apache_rows(baseline)
    originals = {row['run_scoped_case_id']: row for row in rows}
    expected_ids = list(originals)
    if [row.get('original_id') for row in plan['rows']] != expected_ids:
        raise ValueError('Case plan must preserve all155 original IDs and order')
    if index.get('unsigned') is not True or [row.get('run_scoped_case_id') for row in index['cases']] != expected_ids:
        raise ValueError('Unsigned index must preserve all155 original IDs and order')
    for item in plan['rows']:
        original = originals[item['original_id']]['selected_requirement']
        if (item.get('original_contract') != original or item.get('original_oracle') != original['expected_oracle']
                or item.get('case_id') != original.get('case_id')):
            raise ValueError('Original contract/oracle changed in case plan')
    return rows


def inventory_item(plan):
    """Inventory every original obligation; categories never confer approval."""
    case = plan['case_id']
    if plan['execution_kind'] == 'configtest' or case in BATCH.CONTROLS.PRE_NATIVE_CASES:
        category = 'separate_typed_control_review'
        reason = 'Use the separate review_controls approval and shared typed validator.'
    elif case in SUPPORTED:
        category = 'registered_bounded_request'
        reason = 'Explicit bounded request fixture, full native lifecycle and independent controls predicates.'
    elif case in NATIVE_HEADER_MAPPING_GAPS:
        category = 'native_header_mapping_evidence_missing'
        reason = 'Wire Content-Type/charset is observed, but exact native mapper/header/MIME propagation is not independently proven.'
    elif plan.get('fault'):
        category = 'physical_fault_family_review_needed'
        reason = 'Requires boundary-specific first-cause/APR/native return and recovery semantics; no ordinary allow transfer.'
    elif plan.get('driver_seams'):
        category = 'special_operation_family_review_needed'
        reason = 'Requires case-specific proof of operations: ' + ', '.join(plan['driver_seams'])
    elif any(plan.get('candidate_expectation', {}).get(key) is None
             for key in ('visible_status', 'backend_requests', 'native_rule_id', 'native_phase')):
        category = 'independent_expectation_and_family_review_needed'
        reason = 'At least one status/backend/rule/phase expectation is unresolved; do not infer it from execution.'
    else:
        category = 'additional_semantic_family_review_needed'
        reason = 'Plan expectations exist but an independent case-specific complete lifecycle predicate is not implemented.'
    return {'run_scoped_case_id': plan['original_id'], 'case_id': case, 'category': category,
            'reason': reason, 'candidate_expectation': copy.deepcopy(plan.get('candidate_expectation')),
            'oracle_source_refs': copy.deepcopy(plan.get('oracle_source_refs', [])),
            'registered': case in SUPPORTED, 'outcome': None}


def supported_oracle(oracle, plan):
    allowed = {'native_result', 'visible_status', 'phase', 'rule_id', 'event_fields',
               'physical_evidence_not_projection', 'unresolved_expected_value_reason',
               'request_body_bytes', 'request_content_type', 'request_apr_eos', 'response_apr_eos',
               'native_request_body_finalizations', 'native_response_body_finalizations',
               'common_finish_calls', 'native_free_calls', 'scope'}
    if not set(oracle) <= allowed:
        return None
    if 'scope' in oracle and oracle['scope'] != SUPPORTED_ORACLE_SCOPE:
        return None
    types = [value for key, value in plan['request']['headers'] if key.lower() == 'content-type']
    extra_expected = {'request_body_bytes': len(bytes_input(plan['request']['body'])),
                      'request_content_type': types[0] if types else None,
                      'request_apr_eos': 1, 'response_apr_eos': 1,
                      'native_request_body_finalizations': 1, 'native_response_body_finalizations': 1,
                      'common_finish_calls': 1, 'native_free_calls': 1}
    return (oracle.get('unresolved_expected_value_reason') is None
            and oracle.get('native_result') == 'allow' and oracle.get('visible_status') == 200
            and oracle.get('phase') == ORACLE_LIFECYCLE_PHASE[plan['case_id']]
            and oracle.get('rule_id') in (None, plan['candidate_expectation']['native_rule_id'])
            and oracle.get('physical_evidence_not_projection') is True
            and oracle.get('event_fields', []) == plan['original_oracle'].get('event_fields', [])
            and all(oracle[key] == value for key, value in extra_expected.items() if key in oracle))


def evaluate(row, plan, packet, packet_ref, expected, reextracted, oracle=None):
    """Return a decision only; publication is a distinct shared-validator step."""
    result = {'run_scoped_case_id': row['run_scoped_case_id'], 'case_id': plan['case_id'],
              'original_oracle': copy.deepcopy(plan['original_oracle']), 'oracle_decision': None,
              'outcome': None, 'full_lifecycle_qualified': False, 'predicates': [],
              'registry_inventory': inventory_item(plan)}
    p = result['predicates']
    if packet is None:
        p.append(predicate('candidate_present', None, 'Missing unsigned candidate.'))
        return result
    if plan['execution_kind'] == 'configtest' or packet.get('execution_kind') == 'host_pre_native_rejection':
        p.append(predicate('separate_control_approval', None, 'Use review_controls with a separately bound explicit approval.'))
        return result
    p.append(predicate('physical_reextraction_equal', packet == reextracted,
                       'Candidate must equal fresh unchanged extractor output from the same retained attempt/spec.', [packet_ref]))
    p.append(predicate('exact_original_identity', packet.get('run_scoped_case_id') == row['run_scoped_case_id']
                       and packet.get('original_selected_requirement') == row['selected_requirement']
                       and packet.get('actual_scenario_variant') == plan['case_id'],
                       'Candidate cannot transfer another original ID or contract.', [packet_ref]))
    p.append(predicate('exact_product_run_identity', identity_matches(packet, expected),
                       'Exact run, Parent, Framework, MRTS, Apache, observed module and SDK identities.',
                       evidence(packet, 'product_host_identity', 'source_config_binding')))
    try:
        native_identity = check_native_identity(values(packet), expected)
    except (KeyError, TypeError, ValueError):
        native_identity = None
    p.append(predicate('principal_native_run_allocation_identity', native_identity,
                       'Every principal native return must bind the actual run/PID/allocation scope.',
                       evidence(packet, 'native_api_returns', 'observed_handle_association')))
    checks = packet.get('review_checks', {})
    p.append(predicate('shared_extractor_checks', CHECKS <= checks.keys() and all(value is True for value in checks.values()),
                       'Every required extractor check must be present and true.', [packet_ref]))
    driver = packet.get('driver_execution', {})
    p.append(predicate('actual_case_contract', packet.get('execution_observed') is True
                       and driver.get('actual_principal_execution') is True and driver.get('executed_case_contract') is True
                       and driver.get('missing_operations') == [] and driver.get('execution_error') is None,
                       'Actual selected contract, without driver seams or execution errors.', [packet_ref]))
    try:
        complete = complete_measurements(packet, Path(packet_ref['path']))
        reason = 'All35 applicable roles require physical evidence through unchanged shared measurement validation.'
    except (ValueError, OSError, KeyError, TypeError) as error:
        complete, reason = False, str(error)
    p.append(predicate('all35_physical_roles', complete, reason, [packet_ref]))
    p.extend(host_predicates(plan, packet))
    if oracle is None:
        p.append(predicate('independent_oracle', None, 'Original unresolved oracle needs separate independent review.'))
    else:
        valid = supported_oracle(oracle, plan) if plan['case_id'] in SUPPORTED else None
        p.append(predicate('independent_oracle', valid, 'Separate oracle remains unchanged and must describe this bounded allow family.'))
        result['oracle_decision'] = {'effective_oracle_sha256': O.canonical_digest(oracle), 'resolved_by_this_producer': False}
    if p and all(item['result'] == 'PASS' for item in p):
        result.update(outcome='PASS', full_lifecycle_qualified=True)
    return result


def publish_packet(output, packet, decision, row, oracle):
    if decision.get('outcome') != 'PASS' or decision.get('full_lifecycle_qualified') is not True:
        raise ValueError('Only complete positive decisions may enter publication')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', decision['case_id']):
        raise ValueError('Unsafe original case filename')
    reviewed = copy.deepcopy(packet)
    reviewed.update(reviewed_by='root', candidate_is_not_an_approval=False, unsigned=False,
                    oracle_evaluated=True, oracle_sha256=O.canonical_digest(oracle),
                    outcome=decision['outcome'], full_lifecycle_qualified=True)
    path = output / (decision['case_id'] + '.reviewed.json')
    # Validate an exclusive temporary candidate before publishing any approval.
    temporary = output / (decision['case_id'] + '.validation.json')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(reviewed, stream, indent=2)
        stream.write('\n')
    temporary.chmod(0o600)
    try:
        qualified = SHARED.reviewed_packet(O.reference(temporary), row, oracle)
        if qualified['full_lifecycle_qualified'] is not True:
            raise ValueError('Shared validator did not fully qualify reviewed packet')
        if path.exists():
            raise ValueError('Output already exists')
        temporary.rename(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return O.reference(path)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('baseline', 'plan', 'unsigned-index', 'identity', 'spec'):
        parser.add_argument('--' + name, type=Path, required=True)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--attempt', type=Path, required=True)
    parser.add_argument('--oracle-reviews', type=Path)
    parser.add_argument('--oracle-reviews-sha256')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--approve-supported-families', action='store_true',
                        help='Explicitly execute this Root review procedure for the registered families only')
    return parser.parse_args()


def validate_expected_identity(expected):
    required = ('run_id', 'parent_sha', 'framework_sha', 'mrts_sha', 'apache_sha256', 'module_sha256', 'sdk_sha256')
    if any(not isinstance(expected.get(key), str) or not expected[key] for key in required):
        raise ValueError('Expected identity must explicitly bind every product/run component')
    for key in required[1:]:
        size = 40 if key in ('parent_sha', 'framework_sha', 'mrts_sha') else 64
        if not re.fullmatch('[0-9a-f]{' + str(size) + '}', expected[key]):
            raise ValueError('Expected immutable identity is not a full digest: ' + key)


def load_candidates(data, inputs):
    packets = [read_ref(entry['reference']) if entry.get('reference') else None
               for entry in data['unsigned-index']['cases']]
    inventory = physical_inventory(data['unsigned-index'], packets)
    for packet in packets:
        if packet:
            inventory.extend(control_references(packet))
            plan_ref = packet.get('batch_plan_reference', {})
            if plan_ref.get('sha256') != inputs['plan']['sha256']:
                raise ValueError('Candidate is not bound to the supplied exact case plan')
    return packets, inventory


def load_oracle_reviews(args, inputs, rows, inventory):
    reviews = {}
    if not args.oracle_reviews:
        return reviews
    if not args.oracle_reviews_sha256:
        raise ValueError('Oracle review hash required')
    inputs['oracle_reviews'] = {'path': str(args.oracle_reviews.resolve(strict=True)), 'sha256': args.oracle_reviews_sha256}
    originals = {row['run_scoped_case_id']: row for row in rows}
    for record in read_ref(inputs['oracle_reviews'])['records']:
        identity = record['run_scoped_case_id']
        if identity in reviews or identity not in originals:
            raise ValueError('Duplicate or foreign oracle review')
        inventory.extend(physical_inventory(record))
        reviews[identity] = O.review_record(record, originals[identity])
    return reviews


def evaluate_batch(rows, data, packets, extracted, reviews, approve):
    decisions, pending = [], []
    for row, plan, entry, packet in zip(rows, data['plan']['rows'], data['unsigned-index']['cases'], packets):
        ref = entry.get('reference')
        identity = row['run_scoped_case_id']
        oracle = L.effective_oracle(reviews.get(identity), row['selected_requirement']['expected_oracle'])
        decision = evaluate(row, plan, packet, ref, data['identity'], extracted.get(identity), oracle)
        if decision['full_lifecycle_qualified']:
            if approve:
                pending.append((packet, decision, row, oracle))
            else:
                decision.update(outcome=None, full_lifecycle_qualified=False)
                decision['predicates'].append(predicate('explicit_root_review_invocation', None,
                                                       'Use --approve-supported-families after inspecting physical evidence.'))
        decisions.append(decision)
    return decisions, pending


def write_results(output, inputs, inventory, decisions, approved):
    result = {'schema_version': 1, 'scope': 'apache-native', 'i12_complete': False,
              'input_evidence': inputs, 'required_cases': 155, 'rows': decisions,
              'physical_input_inventory': inventory,
              'registry_categories': dict(collections.Counter(item['registry_inventory']['category'] for item in decisions)),
              'qualified_pass': len(approved), 'unknown_or_unqualified': 155 - len(approved)}
    with (output / 'decisions.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    with (output / 'reviewed-packets.json').open('x', encoding='utf-8') as stream:
        json.dump({'packets': approved}, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'cases': 155, 'qualified_pass': len(approved), 'i12_complete': False}))


def main():
    args = arguments()
    inputs = {name: {'path': str(getattr(args, name.replace('-', '_')).resolve(strict=True)),
                     'sha256': getattr(args, name.replace('-', '_') + '_sha256')}
              for name in ('baseline', 'plan', 'unsigned-index', 'identity', 'spec')}
    data = {name: read_ref(ref) for name, ref in inputs.items()}
    rows = validate_inputs(data['baseline'], data['plan'], data['unsigned-index'])
    validate_expected_identity(data['identity'])
    packets, inventory = load_candidates(data, inputs)
    extracted = {item['run_scoped_case_id']: item for item in BATCH.extract_all(args.attempt, args.spec)}
    reviews = load_oracle_reviews(args, inputs, rows, inventory)
    decisions, pending = evaluate_batch(rows, data, packets, extracted, reviews, args.approve_supported_families)
    # Freeze all declared inputs again after evaluation; no changed-input result.
    for ref in [*inputs.values(), *inventory]:
        O.verify_reference(ref)
    output = L.PATHS.new_output(args.output)
    output.mkdir(mode=0o700)
    approved = []
    for packet, decision, row, oracle in pending:
        decision['reviewed_packet'] = publish_packet(output, packet, decision, row, oracle)
        approved.append(decision['reviewed_packet'])
    write_results(output, inputs, inventory, decisions, approved)


if __name__ == '__main__':
    main()
