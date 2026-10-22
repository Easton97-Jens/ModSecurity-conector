"""Check a completed readiness client's exclusive native allocation window."""
import hashlib
import json
import re


def readiness_client_bound(client, start, end, expected_probe, command):
    """Bind the actual client receipt to the driver's exact readiness command."""
    probe = client.get('probe')
    requests = client.get('requests')
    if (not isinstance(probe, str) or re.fullmatch(r'.+-ready-[0-9]', probe) is None
            or probe != expected_probe or not isinstance(command, dict)
            or client.get('neighbor') is not True or 'error' in client
            or not isinstance(requests, list) or len(requests) != 1):
        return None
    command_start, command_end = command.get('started_ns'), command.get('completed_ns')
    pid = client.get('pid')
    if (type(command_start) is not int or type(command_end) is not int
            or not 0 < command_start <= start <= end <= command_end
            or type(command.get('exit_code')) is not int or command['exit_code'] != 0
            or type(command.get('signal')) is not int or command['signal'] != 0
            or command.get('timed_out') is not False
            or type(command.get('wrapper_pid')) is not int or command['wrapper_pid'] <= 0
            or type(pid) is not int or pid <= 0
            or command.get('argv', [])[-3:] != ['--neighbor', '--readiness-index', probe[-1]]):
        return None
    if 'client_pid' in command and (type(command['client_pid']) is not int or command['client_pid'] != pid):
        return None
    transaction = probe + '-neighbor'
    request = requests[0]
    if (request.get('wire_probe') != transaction
            or request.get('client_framing', {}).get('status') != 200
            or request.get('client_framing', {}).get('complete') is not True):
        return None
    # RTK's wrapper PID is not the Python client's PID. Compare only the actual
    # client process identities the producer records, without inventing lineage.
    for observation in [request, *client.get('connections', []),
                        *(request.get(name) for name in
                          ('socket_before_send', 'socket_after_send', 'socket_after_receive'))]:
        if isinstance(observation, dict) and 'pid' in observation:
            if type(observation['pid']) is not int or observation['pid'] != pid:
                return None
    return True


def public_readiness_scope(rows, allocation, client, start, end, expected_probe, command):
    """Join only this exclusive readiness probe, without claiming a native scope."""
    if readiness_client_bound(client, start, end, expected_probe, command) is not True:
        return None
    transaction = expected_probe + '-neighbor'
    functions = ('native_new', 'native_new_with_id', 'native_process_logging', 'native_cleanup')
    # Include all same-ID lifecycle returns, even outside the window or another PID,
    # so reuse/duplicates cannot be hidden by the temporal or process filter.
    lifecycle = [row for row in rows if row.get('edge') == 'return'
                 and row.get('function') in functions
                 and row.get('transaction_id') == transaction]
    if (len(lifecycle) != 3 or lifecycle[0] is not allocation
            or [row.get('function') for row in lifecycle] !=
               ['native_new_with_id', 'native_process_logging', 'native_cleanup']):
        return None
    pid = allocation.get('pid')
    if type(pid) is not int or pid <= 0:
        return None
    for row in lifecycle:
        if (type(row.get('pid')) is not int or row.get('pid') != pid
                or row.get('invalid') is not False
                or row.get('input_transaction_id') != transaction
                or row.get('transaction_id_origin') != 'sdk_public_m_id'
                or row.get('allocation_scope_call') is not None
                or row.get('allocation_join_verified') is not False):
            return None
    if any(type(row.get('result')) is not int or row['result'] != 1
           for row in lifecycle[:2]):
        return None
    if 'result' not in lifecycle[2] or lifecycle[2]['result'] is not None:
        return None
    for field in ('monotonic_ns', 'sequence', 'call'):
        values = [row.get(field) for row in lifecycle]
        if not all(type(value) is int and value > 0 for value in values):
            return None
        if not values[0] < values[1] < values[2]:
            return None
    if not start <= lifecycle[0]['monotonic_ns'] < lifecycle[2]['monotonic_ns'] <= end:
        return None
    calls = {(row['function'], row['call']) for row in lifecycle}
    related_returns = [row for row in rows if row.get('edge') == 'return'
                       and row.get('function') in functions
                       and ((row.get('function'), row.get('call')) in calls
                            or row.get('transaction_id') == transaction
                            or row.get('input_transaction_id') == transaction)]
    if related_returns != lifecycle:
        return None
    # Pair every return with its physical enter. Include conflicting same-call or
    # same-ID rows outside the window, and all lifecycle enters inside this
    # exclusive probe window, so a damaged join cannot disappear from selection.
    enters = [row for row in rows if row.get('edge') == 'enter'
              and row.get('function') in functions
              and ((row.get('function'), row.get('call')) in calls
                   or row.get('transaction_id') == transaction
                   or row.get('input_transaction_id') == transaction
                   or (type(row.get('monotonic_ns')) is int
                       and start <= row['monotonic_ns'] <= end))]
    if len(enters) != 3:
        return None
    paired = []
    for index, (entered, returned) in enumerate(zip(enters, lifecycle)):
        if (entered.get('function') != returned['function']
                or not all(field in entered for field in
                           ('result', 'transaction_id', 'input_transaction_id', 'allocation_scope_call'))
                or type(entered.get('call')) is not int
                or entered['call'] != returned['call']
                or type(entered.get('pid')) is not int or entered['pid'] != pid
                or entered.get('invalid') is not False or entered.get('result') is not None
                or entered.get('allocation_scope_call') is not None
                or entered.get('allocation_join_verified') is not False):
            return None
        expected_id = None if index == 0 else transaction
        expected_origin = 'unknown' if index == 0 else 'sdk_public_m_id'
        if (entered.get('transaction_id') != expected_id
                or entered.get('input_transaction_id') != expected_id
                or entered.get('transaction_id_origin') != expected_origin):
            return None
        paired.extend([entered, returned])
    for field in ('monotonic_ns', 'sequence'):
        values = [row.get(field) for row in paired]
        if (not all(type(value) is int and value > 0 for value in values)
                or not all(before < after for before, after in zip(values, values[1:]))):
            return None
    if not start <= paired[0]['monotonic_ns'] < paired[-1]['monotonic_ns'] <= end:
        return None
    return {'allocation': allocation, 'logging_returns': [lifecycle[1]],
            'cleanup_returns': [lifecycle[2]], 'join': 'exclusive_readiness_public_transaction_id',
            'lifecycle_enters': enters,
            'native_allocation_scope_inferred': False}


def native_receipt(path, client, *, expected_probe=None, command=None):
    raw = path.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    start, end = client.get('monotonic_ns'), client.get('completed_ns')
    if type(start) is not int or type(end) is not int or end < start:
        raise ValueError('actual readiness client window required')
    caller_bound = ((expected_probe is None and command is None)
                    or readiness_client_bound(client, start, end, expected_probe, command) is True)
    allocations = [row for row in rows
        if row.get('function') in ('native_new', 'native_new_with_id')
        and row.get('edge') == 'return'
        and type(row.get('monotonic_ns')) is int
        and start <= row['monotonic_ns'] <= end]
    selected = []
    for allocation in allocations:
        key = (allocation.get('pid'), allocation.get('allocation_scope_call'))
        if None in key:
            continue
        returns = [row for row in rows if row.get('edge') == 'return'
            and (row.get('pid'), row.get('allocation_scope_call')) == key]
        selected.append({'allocation': allocation,
            'logging_returns': [row for row in returns if row.get('function') == 'native_process_logging'],
            'cleanup_returns': [row for row in returns if row.get('function') == 'native_cleanup']})
    if not selected and len(allocations) == 1:
        public_scope = public_readiness_scope(rows, allocations[0], client, start, end, expected_probe, command)
        if public_scope is not None:
            selected.append(public_scope)
    positive = caller_bound and len(selected) == 1 and len(allocations) == 1 and all(
        scope['allocation'].get('result') == 1
        and scope['allocation'].get('invalid') is False
        and len(scope['logging_returns']) == len(scope['cleanup_returns']) == 1
        and scope['logging_returns'][0].get('result') == 1
        and scope['logging_returns'][0].get('invalid') is False
        and scope['cleanup_returns'][0].get('invalid') is False
        for scope in selected)
    return {'positive_allocation_finish_free': positive, 'client_window': [start, end],
        'allocation_scopes': selected, 'native_log_path': str(path),
        'native_log_sha256_at_check': hashlib.sha256(raw).hexdigest(),
        'http_status_alone_is_not_native_readiness': True, 'qualification': None}
