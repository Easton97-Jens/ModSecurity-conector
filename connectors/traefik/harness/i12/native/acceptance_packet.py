"""Adapt complete native producer receipts to the existing candidate packet API.

This adapter never reviews an oracle or assigns a qualifier verdict. Missing
sources, malformed physical records and absent measurements remain explicit.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


def contracts():
    path = ROOT / 'connectors/traefik/harness/i12_ledger.py'
    spec = importlib.util.spec_from_file_location('acceptance_packet_contracts', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.contracts()


def read(path):
    return json.loads(path.read_text()) if path.is_file() else None


def reference(path, role):
    if not path.is_file():
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
            'bytes': len(raw), 'role': role}


def records(path):
    if not path.is_file():
        return None, [{'path': str(path), 'reason': 'missing physical source'}]
    try:
        raw = path.read_bytes()
    except OSError as error:
        return None, [{'path': str(path), 'reader_error': type(error).__name__, 'errno': error.errno,
                       'reason': 'Physical source could not be read; absence is not zero.'}]
    rows, errors = [], []
    for index, line in enumerate(raw.splitlines()):
        try:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError('physical JSONL row is not an object')
            rows.append(value)
        except (ValueError, UnicodeDecodeError) as error:
            errors.append({'path': str(path), 'line': index, 'reason': str(error),
                           'raw_sha256': hashlib.sha256(line).hexdigest()})
    return rows, errors


def generated_join(case, measurement, before, client, native, raw_request):
    """Resolve only the admitted original blank-ID experiment by physical scope."""
    if (case.get('key') != '004-b044cc412aca' or
            not case.get('id', '').endswith('::transaction_id_generated_or_fallback') or
            not case.get('fixture', {}).get('request', {}).get('omit_transaction_id')):
        return None
    admitted = (measurement or {}).get('generated_id_child_environment', {})
    if admitted != {'name': 'I12_NATIVE_GENERATED_CASE', 'present': True,
                    'value': '004-b044cc412aca', 'dedicated_host': True}:
        return None
    if not raw_request or b'x-request-id:' in raw_request.split(b'\r\n\r\n', 1)[0].lower():
        return None
    pid = (before or {}).get('processes', {}).get('engine', {}).get('pid')
    start, end = (client or {}).get('started_ns'), (client or {}).get('completed_ns')
    if not all(isinstance(v, int) and v > 0 for v in (pid, start, end)) or end < start:
        return None
    allocations = [r for r in native or [] if r.get('pid') == pid and
        start <= r.get('monotonic_ns', 0) <= end and r.get('function') in ('native_new', 'native_new_with_id') and
        r.get('edge') == 'return' and r.get('result') == 1 and r.get('invalid') is False]
    if len(allocations) != 1:
        return None
    allocation = allocations[0]
    scope, identity = allocation.get('allocation_scope_call'), allocation.get('transaction_id')
    if not scope or not identity or allocation.get('transaction_id_origin') != 'sdk_public_m_id':
        return None
    joined = [r for r in native or [] if r.get('pid') == pid and r.get('allocation_scope_call') == scope
              and r.get('allocation_join_verified')]
    if not joined or any(r.get('invalid') is not False for r in joined):
        return None
    return {'pid': pid, 'allocation_scope_call': scope, 'transaction_id': identity,
            'client_transaction_id': None, 'binding': 'exact admitted case/PID/client window/single actual SDK allocation'}


def physical_content_types(path):
    if not path.is_file():
        return None
    head, separator, _ = path.read_bytes().partition(b'\r\n\r\n')
    if not separator or len(head) > 65536:
        return None
    return [line.partition(b':')[2].strip().decode('latin1') for line in head.split(b'\r\n')[1:]
            if line.partition(b':')[0].lower() == b'content-type']


def paired_accessor_call(row, native_rows):
    function = 'native_cleanup' if row['native_method'] == 'transaction_cleanup_before_free' else 'native_' + row['native_method']
    related = [r for r in native_rows if r.get('pid') == row['pid'] and r.get('function') == function and r.get('invalid') is False]
    entered = {r.get('call') for r in related if r.get('edge') == 'enter' and r.get('monotonic_ns', 0) <= row['monotonic_ns']}
    returned = {r.get('call') for r in related if r.get('edge') == 'return' and row['monotonic_ns'] <= r.get('monotonic_ns', 0)}
    return bool((entered & returned) - {None})


def retained_body_records(root, direction, pid, proof):
    rows, malformed = records(root / 'faults.jsonl')
    if malformed:
        return []
    allowed_methods = ('append_' + direction + '_body', 'process_' + direction + '_body', 'transaction_cleanup_before_free')
    retained = []
    for row in rows or []:
        if (row.get('operation'), row.get('accessor'), row.get('pid')) != (
                'native_retained_body', 'msc_get_' + direction + '_body_length', pid) or row.get('injected') is not False:
            continue
        if (pid, row.get('allocation_scope_call')) not in proof['scopes'] or row.get('native_method') not in allowed_methods:
            continue
        if type(row.get('retained_body_bytes')) is not int or row['retained_body_bytes'] < 0 or type(row.get('monotonic_ns')) is not int:
            continue
        client = proof['client']
        in_window = client['started_ns'] <= row['monotonic_ns'] <= client['completed_ns']
        if (in_window or row['native_method'] == 'transaction_cleanup_before_free') and paired_accessor_call(row, proof['associated']):
            retained.append(row)
    return retained


def complete_pid_observer(rows, pid):
    rows = [r for r in rows if r.get('pid') == pid]
    if not rows or [r.get('sequence') for r in rows] != list(range(1, len(rows) + 1)):
        return False
    admitted = rows[0].get('function') == 'observer' and rows[0].get('edge') in ('admitted', 'fork')
    final = rows[-1].get('function') == 'observer' and rows[-1].get('edge') in ('final', 'snapshot')
    return admitted and final and rows[-1].get('live_mappings') == 0 and all(r.get('invalid') is False for r in rows)


def body_selection_candidate(case, root, proof):
    """Return joined physical facts; Root alone interprets MIME/charset policy."""
    client, before = proof['client'] or {}, proof['before'] or {}
    start, end = client.get('started_ns'), client.get('completed_ns')
    pid = before.get('processes', {}).get('engine', {}).get('pid')
    if not all(type(v) is int and v > 0 for v in (start, end, pid)) or end < start:
        return None
    response = 'response' in case['id'].rsplit('::', 1)[-1] or 'phase4' in case['id']
    direction = 'response' if response else 'request'
    raw_path = proof['response_path'] if response else proof['request_path']
    headers = physical_content_types(raw_path)
    if headers is None:
        return None
    rows = proof['associated']
    if response and not any(row.get('function') == 'native_process_response_headers' and
            row.get('edge') == 'return' and row.get('argument_response_status') == client.get('status') for row in rows):
        return None  # A locally generated error response is not the upstream header sample.
    retained = retained_body_records(root, direction, pid, proof)
    rules_path, debug_path = root / 'rules.conf', root / 'debug.log'
    if not retained or not rules_path.is_file() or not debug_path.is_file():
        return None
    rules = rules_path.read_text()
    ids = set(re.findall(r'\bid:(\d+)', rules))
    debug = [line for line in debug_path.read_text().splitlines() if line.startswith('[' + proof['transaction_id'] + ']')]
    body_variable = direction.upper() + '_BODY'
    executed = [line for line in debug if 'Executing operator' in line and 'against ' + body_variable in line
                and any('(Rule: ' + identifier + ')' in line for identifier in ids)]
    exclusion = [line for line in debug if response and 'not marked to be inspected' in line]
    continuous = complete_pid_observer(proof['all_native'], pid)
    final = [r for r in retained if r['native_method'] == 'transaction_cleanup_before_free']
    if not executed and not exclusion and not (continuous and final):
        return None
    return {'schema': 'traefik-native-body-selection-candidate-v1', 'direction': direction,
        'actual_content_type_headers': headers, 'header_source_layer': 'client_response' if response else 'client_request', 'header_source': reference(raw_path, 'client_process'),
        'actual_retained_body_records': retained, 'sdk_rule_operator_debug': executed,
        'sdk_mime_exclusion_debug': exclusion, 'effective_rule_source': reference(rules_path, 'effective_configuration'),
        'actual_native_body_calls': [r for r in rows if r.get('pid') == pid and r.get('edge') == 'return' and
            r.get('function') in ('native_append_' + direction + '_body', 'native_process_' + direction + '_body')],
        'actual_native_interventions': [r for r in rows if r.get('function') == 'native_intervention' and r.get('edge') == 'return'],
        'complete_pid_observer_window': continuous, 'retained_is_inspected': False,
        'selection_interpretation': 'sdk_rule_operator_execution_observed' if executed else
            'sdk_mime_exclusion_debug_observed' if exclusion else 'final_retention_and_native_call_trace_observed',
        'root_approval': 'pending', 'inspection_byte_count_claimed': False}


def packet(attempt, case):
    data = attempt / 'data'
    key, tx = case['key'], case['transaction_id']
    root = data / 'cases' / key
    measurement = read(root / 'measurement.json')
    if measurement is not None and (measurement.get('id') != case['id'] or
            measurement.get('fixture_sha256') != case.get('fixture_sha256')):
        raise ValueError('Actual original-ID/fixture hash differs from the supplied case binding')
    required_roles = contracts().ROLES
    observations = {name: {'applicable': True, 'value': None, 'evidence': [],
        'reason': 'No matching complete physical measurement was found.'}
        for name in required_roles}
    errors = []

    def observed(name, value, *proofs):
        refs = [item for item in proofs if item is not None]
        if any(item['role'] not in required_roles[name] for item in refs):
            raise ValueError('Physical evidence role outside central observation contract: ' + name)
        if value is not None and required_roles[name] <= {item['role'] for item in refs}:
            observations[name] = {'applicable': True, 'value': value, 'evidence': refs}

    native_path = data / 'runtime/logs/native-lifecycle.jsonl'
    native, invalid = records(native_path)
    errors.extend(invalid)
    native_ref = reference(native_path, 'native_api')
    before_path, after_path = data / (key + '-before.json'), data / (key + '-after.json')
    client_path = data / 'client' / (key + '.receipt.json')
    client = read(client_path)
    request_path = data / 'client' / (key + '.request.raw')
    fallback = generated_join(case, measurement, read(before_path), client, native,
                              request_path.read_bytes() if request_path.is_file() else None)
    if fallback:
        tx = fallback['transaction_id']
    direct = [row for row in native or [] if row.get('transaction_id') == tx and
              (not fallback or row.get('pid') == fallback['pid'])]
    scopes = {(row.get('pid'), row.get('allocation_scope_call')) for row in direct
              if row.get('allocation_join_verified')}
    associated = [row for row in native or [] if
        (not fallback or row.get('pid') == fallback['pid']) and
        (row.get('transaction_id') == tx or (row.get('allocation_join_verified') and
         (row.get('pid'), row.get('allocation_scope_call')) in scopes))]
    returns = [row for row in associated if row.get('edge') == 'return']
    counts = Counter(row['function'] for row in returns)
    host_path = root / 'host-lifecycle.jsonl'
    host_rows, invalid = records(host_path)
    errors.extend(invalid)
    # Host records expose their own monotonic epoch, not Linux CLOCK_MONOTONIC.
    # Exact dedicated PID + admitted blank-only target binds these records;
    # the native allocation join above uses the actual client clock window.
    host_pid = (read(before_path) or {}).get('processes', {}).get('traefik', {}).get('pid')
    host = [row for row in host_rows or [] if row.get('transaction_id') == tx or
        (fallback and host_pid is not None and row.get('pid') == host_pid and row.get('transaction_id') == '')]
    host_ref = reference(host_path, 'host_callback')
    client_ref = reference(client_path, 'client_process')
    raw_ref = reference(data / 'client' / (key + '.response.raw'), 'client_process')
    waited = read(data / 'client' / (key + '.wait.json'))
    backend_path = data / 'backend/receipts.jsonl'
    backend_rows, invalid = records(backend_path)
    errors.extend(invalid)
    arrivals = [row for row in backend_rows or [] if row.get('key') == key and
                row.get('operation') == 'headers-arrived']
    backend_ref = reference(backend_path, 'backend_process')
    events_path = root / 'events.jsonl'
    sink, invalid = records(events_path)
    errors.extend(invalid)
    events = [row for row in sink or [] if row.get('transaction_id') == tx]
    sink_ref = reference(events_path, 'physical_event_sink')
    controller = read(attempt / 'controller-result.json')
    isolation_ref = reference(attempt / 'controller-result.json', 'isolation_receipt')
    result_ref = reference(data / 'acceptance-result.json', 'cleanup_observer')
    case_ref = reference(root / 'measurement.json', 'cleanup_observer')
    debug_ref = reference(root / 'debug.log', 'native_debug')
    audit_ref = reference(root / 'audit.log', 'physical_event_sink')
    binding = read(data / 'current-product-binding.json')
    build = read(data / 'acceptance-build.json')
    observed('product_host_identity', {'before': read(before_path), 'after': read(after_path),
        'controller': controller}, reference(before_path, 'loaded_image'), isolation_ref)
    if measurement is not None:
        observed('source_config_binding', {'build': build, 'product_binding': binding,
            'configuration': measurement.get('configuration')},
            reference(data / 'acceptance-build.json', 'source_manifest'),
            reference(data / 'current-product-binding.json', 'source_manifest'),
            reference(root / 'engine.conf', 'effective_configuration'))
    if client is not None:
        observed('client_exit', waited.get('returncode') if waited else None,
                 reference(data / 'client' / (key + '.wait.json'), 'client_process'))
        observed('client_signal', waited, reference(data / 'client' / (key + '.wait.json'), 'client_process'))
        observed('client_headers', client.get('response_headers_latin1'), client_ref, raw_ref)
        observed('client_bytes', client.get('entity_bytes'), client_ref,
                 reference(data / 'client' / (key + '.response-entity.raw'), 'client_process'))
        observed('client_sha256', client.get('entity_sha256'), client_ref)
        observed('transport_framing', {'client': client, 'waited': waited}, client_ref, raw_ref)
        observed('transport_reset_scope', {'actual_client': client, 'host_errors': [row for row in host
            if row.get('fields', {}).get('error')]}, client_ref, host_ref)
    if backend_rows is not None:
        observed('backend_request_count', len(arrivals), backend_ref)
        observed('backend_payload_identity', {'arrivals': arrivals, 'client': client,
            'records': [row for row in backend_rows if row.get('key') == key]}, backend_ref, client_ref)
        observed('client_backend_correlation', {'key': key, 'transaction_id': tx,
            'arrivals': arrivals, 'client': client}, backend_ref, client_ref)
    if sink is not None:
        observed('native_events', {'physical_common_events': events,
            'malformed_physical_rows': [row for row in errors if row['path'] == str(events_path)]}, sink_ref, audit_ref)
        observed('physical_event_order', events, sink_ref)
        observed('terminal_event_count', len(events), sink_ref)
    if direct:
        observed('native_api_returns', returns, native_ref)
        observed('native_transaction_id', [row for row in direct if row.get('transaction_id_origin') == 'sdk_public_m_id'], native_ref)
        observed('common_transaction_id', [row for row in direct if row.get('canonical_transaction_id')], native_ref)
        observed('observed_handle_association', {'verified_pid_scopes': sorted(scopes), 'direct': direct}, native_ref)
        observed('native_phases', {name: counts[name] for name in ('native_process_request_headers',
            'native_process_request_body', 'native_process_response_headers', 'native_process_response_body',
            'native_process_logging')}, native_ref, debug_ref)
        observed('native_body_chunks', [row for row in returns if row['function'] in
            ('native_append_request_body', 'native_append_response_body')], native_ref)
        observed('native_intervention_or_first_cause', {'native_interventions': [row for row in returns
            if row['function'] == 'native_intervention'], 'fault_rows': records(root / 'faults.jsonl')[0],
            'injected_adapter_return_is_sdk_return': False}, native_ref,
            reference(root / 'faults.jsonl', 'native_api'))
        observed('finish_calls', {'actual_runtime_finish': counts['runtime_finish'],
            'actual_common_finish': counts['common_finish'], 'actual_native_logging': counts['native_process_logging']}, native_ref)
        observed('finish_transitions', [row for row in associated if row['function'] in
            ('common_complete_phase', 'common_finish')], native_ref)
        observed('native_free_calls', counts['native_cleanup'], native_ref)
    if direct and host:
        observed('native_eos', {'runtime_handoffs': [row for row in returns if row['function'] in
            ('runtime_finish_request_body', 'runtime_finish_response_body')], 'native_finalizations': [row for row in returns
            if row['function'] in ('native_process_request_body', 'native_process_response_body')],
            'tcp_eof_is_native_eos': False}, native_ref, host_ref)
    if host:
        observed('capability', {'selected_route': 'traefik-native-uds', 'actual_host_rows': host}, host_ref,
                 reference(ROOT / 'connectors/traefik/native_middleware/middleware.go', 'source_contract'))
        observed('host_eos', [row for row in host if row.get('fields', {}).get('end_argument') or
            row.get('fields', {}).get('opcode') in (3, 6)], host_ref)
        observed('commit_order', {'host': host, 'client': client,
            'actual_native_committed_updates': [row for row in associated if row['function'] == 'common_set_response_committed']}, host_ref, client_ref)
        observed('host_action', {'writer_rows': [row for row in host if row['operation'].startswith('writer_')],
            'actual_status': client.get('status') if client else None}, host_ref, client_ref)
    if measurement is not None and controller is not None:
        observed('cleanup_receipts', {'case': measurement, 'controller': controller,
            'final_native': [row for row in native or [] if row.get('function') == 'observer' and row.get('edge') == 'final']}, case_ref, result_ref, isolation_ref)
        observed('descriptor_cleanup', {'before': read(before_path), 'after_case': read(after_path),
            'postcase_stop': measurement.get('processes')}, reference(after_path, 'cleanup_observer'), case_ref)
        observed('process_listener_cleanup', {'case': measurement, 'survivors': controller.get('surviving_namespace_pids'),
            'outside_mount_leaks': controller.get('outside_mount_leaks')}, case_ref, result_ref, isolation_ref)
    neighbor_path = data / 'client' / ('neighbor-' + key + '.receipt.json')
    observed('neighbor_health', {'client': read(neighbor_path), 'backend': [row for row in backend_rows or []
        if row.get('key') == 'neighbor-' + key]}, reference(neighbor_path, 'client_process'), backend_ref)
    selection = body_selection_candidate(case, root, {'client': client, 'before': read(before_path),
        'request_path': request_path, 'response_path': data / 'client' / (key + '.response.raw'),
        'associated': associated, 'all_native': native or [], 'scopes': scopes, 'transaction_id': tx})
    if selection is not None:
        observed('mime_gate', selection, reference(root / 'faults.jsonl', 'native_api'), native_ref, debug_ref, sink_ref)
    output = {'run_scoped_case_id': case['id'], 'leg_id': 'traefik-native-uds',
        'reviewed_by': 'pending_root', 'execution_observed': measurement is not None,
        'fixture_sha256': case.get('fixture_sha256'),
        'execution_kind': None if case['classification'] == 'config' else 'host_http',
        'run_id': native[0].get('run') if native else None,
        'parent_sha': binding.get('checkout_base') if binding else None,
        'framework_sha': '99a7985c1be92a2297b1b59208f64df6768f2cbf',
        'framework_scope': 'read-only original catalog; not executed',
        'mrts_sha': '8a6bb546c4c81d8ffc7be801dceac60c6925685f',
        'mrts_scope': 'read-only original catalog identity; not executed',
        'effective_config_sha256': reference(root / 'engine.conf', 'effective_configuration'),
        'generated_id_physical_join': fallback, 'observations': observations, 'oracle_evaluated': False, 'oracle_sha256': None,
        'outcome': None, 'full_lifecycle_qualified': False, 'physical_source_errors': errors,
        'contract_blockers': case.get('contract_blockers', []),
        'scope': 'Candidate only; Root must select own config/preallocation/runtime contract, approve independent oracle and evaluate.'}
    config = output['effective_config_sha256']
    output['effective_config_sha256'] = config['sha256'] if config else None
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('attempt', type=Path)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('key')
    args = parser.parse_args()
    selected = next(case for case in read(args.manifest)['cases'] + read(args.manifest).get('supplementary_executions', []) if case['key'] == args.key)
    print(json.dumps(packet(args.attempt, selected), indent=2))
