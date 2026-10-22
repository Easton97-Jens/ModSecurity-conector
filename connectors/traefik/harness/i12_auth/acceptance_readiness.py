"""Check a completed readiness client's exclusive native allocation window."""
import hashlib
import json


def native_receipt(path, client):
    raw = path.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    start, end = client.get('monotonic_ns'), client.get('completed_ns')
    if not isinstance(start, int) or not isinstance(end, int) or end < start:
        raise ValueError('actual readiness client window required')
    allocations = [row for row in rows
        if row.get('function') in ('native_new', 'native_new_with_id')
        and row.get('edge') == 'return'
        and start <= row.get('monotonic_ns', -1) <= end]
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
    positive = len(selected) == 1 and len(allocations) == 1 and all(
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
