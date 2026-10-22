"""Run each bound original native fixture; collect, never qualify measurements."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import socket
import stat
import subprocess
import time

import base_driver as base

TASK = Path('/task')
FIXTURES = Path('/mnt/fixtures')
MANIFEST = FIXTURES / 'acceptance-manifest.json'
FAULT_SYMBOLS = ('openat', 'setvbuf', 'fputs', 'fflush', 'fclose', 'msconnector_generic_map_request')
NEIGHBOR_BATCH_SIZE = 8


def fault_mode(case):
    name = case['id'].split('::')[-1]
    return {'body_size_nonzero_with_null_data': 'mapper-body-null',
            'header_count_nonzero_with_null_headers': 'mapper-headers-null',
            'early_mapping_failure_cleanup': 'mapper-headers-null',
            'transaction_begin_failure_cleanup': 'begin-failure',
            'finish_failure_propagation': 'finish-failure',
            'NEED-invalid-native-return': 'native-invalid-return'}.get(name,
            'sink-' + name.removeprefix('NEED-physical-event-sink-') if name.startswith('NEED-physical-event-sink-') else '')


def stop(label, process, marker):
    record = {'proxy_pid': process.pid}
    if process.poll() is None:
        pid = base.actual_pid(process, marker)
        record['actual_pid'] = pid
        os.kill(pid, signal.SIGTERM)
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            os.kill(pid, signal.SIGKILL)
            process.wait(timeout=5)
            record['graceful_timeout'] = True
    record['exit_code'] = process.returncode
    return record


def command(label, argv, env, pass_fds=(), timeout_seconds=30, absolute_deadline=None):
    if type(timeout_seconds) not in (int, float) or not math.isfinite(timeout_seconds) or not 0 < timeout_seconds <= 120:
        raise ValueError('finite positive command deadline <=120 required')
    command_line = ['rtk', 'proxy', *map(str, argv)]
    started = time.monotonic_ns()
    failure = None
    with (TASK / (label + '.stdout')).open('wb') as stdout, (TASK / (label + '.stderr')).open('wb') as stderr:
        result = subprocess.Popen(command_line, cwd=base.SOURCE, env=env, stdout=stdout, stderr=stderr,
            pass_fds=pass_fds, start_new_session=True)
        try:
            wait_budget = timeout_seconds if absolute_deadline is None else min(timeout_seconds, absolute_deadline - time.monotonic())
            if wait_budget <= 0:
                raise subprocess.TimeoutExpired(command_line, 0)
            result.wait(timeout=wait_budget)
        except subprocess.TimeoutExpired as error:
            failure = error
            try:
                os.killpg(result.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass  # A child can exit between deadline expiry and signaling.
            try:
                result.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(result.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                result.wait(timeout=5)
    receipt = {'argv': command_line, 'exit_code': result.returncode, 'wrapper_pid': result.pid,
               'timed_out': failure is not None,
               'absolute_work_deadline': absolute_deadline, 'wait_budget_seconds': max(0, wait_budget),
               'started_ns': started, 'completed_ns': time.monotonic_ns(),
               'signal': -result.returncode if result.returncode < 0 else None,
               'stdout_sha256': base.digest(TASK / (label + '.stdout')),
               'stderr_sha256': base.digest(TASK / (label + '.stderr'))}
    base.write(label + '.command.json', receipt)
    if failure is not None:
        raise failure
    return receipt


def native_control_counts(path, transaction_id, offset):
    with path.open('rb') as stream:
        stream.seek(offset)
        raw = stream.read()
    rows = []
    malformed = 0
    for line in raw.splitlines():
        try:
            row = json.loads(line)
            if row.get('transaction_id') == transaction_id:
                rows.append(row)
        except (ValueError, AttributeError):
            malformed += 1
    returns = [row for row in rows if row.get('edge') == 'return']
    return {'native_allocations': sum(row.get('result') == 1 for row in returns
                    if row.get('function') in ('native_new', 'native_new_with_id')),
        'native_cleanup_returns': sum(row.get('function') == 'native_cleanup' for row in returns),
        'native_logging_returns': sum(row.get('function') == 'native_process_logging' for row in returns),
        'native_logging_successes': sum(row.get('function') == 'native_process_logging' and row.get('result') == 1 for row in returns),
        'runtime_request_eos_returns': sum(row.get('function') == 'runtime_finish_request_body' for row in returns),
        'runtime_response_eos_returns': sum(row.get('function') == 'runtime_finish_response_body' for row in returns),
        'native_pids': sorted({row['pid'] for row in rows}),
        'invalid_rows': sum(row.get('invalid') is not False for row in rows), 'malformed_rows': malformed}


def http_readiness(case, port, env, lifecycle_path, host_pid):
    deadline = time.monotonic() + 30
    receipt = {'key': case['key'], 'actual_host_pid': host_pid, 'route': 'independent healthy neighbor',
               'qualified_main_control': False, 'attempts': [], 'ready': False}
    for index, identity in enumerate(case['readiness_ids']):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        label = case['key'] + '-readiness-' + str(index)
        key = 'neighbor-readiness-' + str(index) + '-' + case['key']
        offset = lifecycle_path.stat().st_size
        attempt = {'transaction_id': identity, 'key': key, 'native_log_start': offset,
            'command': command(label, ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py',
                        port, MANIFEST, case['key'], 'readiness-' + str(index)], env,
                        timeout_seconds=min(10, remaining), absolute_deadline=deadline)}
        client_path = TASK / 'client' / (key + '.receipt.json')
        client = json.loads(client_path.read_text())
        attempt.update(client_receipt=str(client_path), actual_status=client.get('status'))
        receipt['attempts'].append(attempt)
        base.write(case['key'] + '-readiness.json', receipt)
        if client.get('status') == 404:
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(0.05, remaining))
            continue
        if client.get('status') != 200:
            raise RuntimeError('HTTP readiness returned a non-startup error; preserved receipts')
        while time.monotonic() < deadline:
            counts = native_control_counts(lifecycle_path, identity, offset)
            attempt['native_counts'] = counts
            if (counts['native_allocations'] == 1 and counts['native_logging_returns'] == 1 and counts['native_logging_successes'] == 1 and
                    counts['native_cleanup_returns'] == 1 and not counts['invalid_rows'] and not counts['malformed_rows'] and
                    time.monotonic() <= deadline):
                receipt['ready'] = True
                base.write(case['key'] + '-readiness.json', receipt)
                return receipt
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(0.02, remaining))
        break
    base.write(case['key'] + '-readiness.json', receipt)
    raise RuntimeError('HTTP/native readiness deadline reached; no qualified beforecontrol executed')


def neighbor_scope_status(path, batch, final=False):
    with path.open('rb') as stream:
        stream.seek(batch['native_log_start'])
        raw = stream.read()
    rows, malformed = [], 0
    for line in raw.splitlines():
        try:
            row = json.loads(line)
            if row.get('pid') == batch['pid']:
                rows.append(row)
        except (ValueError, AttributeError):
            malformed += 1
    sequences = [row.get('sequence') for row in rows]
    admitted = bool(rows and rows[0].get('function') == 'observer' and rows[0].get('edge') == 'admitted')
    complete = admitted and sequences == list(range(1, len(rows) + 1)) and not malformed and all(row.get('invalid') is False for row in rows)
    returns = [row for row in rows if row.get('edge') == 'return']
    allocations = [row for row in returns if row.get('function') in ('native_new', 'native_new_with_id') and row.get('result') == 1]
    scopes = []
    for allocation in allocations:
        scope = allocation.get('allocation_scope_call')
        joined = [row for row in returns if row.get('allocation_scope_call') == scope]
        counts = {name: sum(row.get('function') == name for row in joined) for name in
            ('native_process_request_body', 'native_process_response_body', 'native_process_logging', 'native_cleanup')}
        successes = sum(row.get('function') == 'native_process_logging' and row.get('result') == 1 for row in joined)
        done = bool(scope) and all(count == 1 for count in counts.values()) and successes == 1
        scopes.append({'allocation_scope_call': scope, 'transaction_id': allocation.get('transaction_id'),
            'native_returns': counts, 'native_logging_successes': successes, 'complete': done})
        complete = complete and done
    if len({scope['allocation_scope_call'] for scope in scopes}) != len(scopes):
        complete = False
    final_row = rows[-1] if rows else {}
    if final:
        complete = complete and final_row.get('function') == 'observer' and final_row.get('edge') == 'final' and final_row.get('live_mappings') == 0
    return {'pid': batch['pid'], 'native_log_start': batch['native_log_start'], 'native_log_end': batch['native_log_start'] + len(raw),
        'window_sha256': hashlib.sha256(raw).hexdigest(), 'rows': len(rows), 'malformed_rows': malformed,
        'scopes': scopes, 'final_required': final, 'final_row': final_row, 'complete': bool(complete)}


def prepare_neighbor_batch(execution_index, batch, lifecycle_path, socket_path, stop_current, start_new):
    if batch is not None:
        before = neighbor_scope_status(lifecycle_path, batch)
        base.write('neighbor-reuse-' + str(execution_index) + '.json', before)
        if not before['complete']:
            raise RuntimeError('Previous neighbor scopes are incomplete; observer reuse refused')
        if execution_index % NEIGHBOR_BATCH_SIZE:
            return batch
        stopped = stop_current()
        native = neighbor_scope_status(lifecycle_path, batch, final=True)
        receipt = {'batch': batch, 'process': stopped, 'native': native, 'socket_removed': not socket_path.exists()}
        base.write('neighbor-batch-' + str(batch['batch_index']) + '-final.json', receipt)
        if stopped['exit_code'] != 0 or not native['complete'] or not receipt['socket_removed']:
            raise RuntimeError('Neighbor observer final/cleanup proof missing; rotation refused')
    next_index = 0 if batch is None else batch['batch_index'] + 1
    created = start_new(next_index)
    base.write('neighbor-batch-' + str(next_index) + '-start.json', created)
    return created


def dynamic_config(helper, path, backend_port, main_socket, neighbor_socket, reuse_socket,
                   file_target=None):
    helper.write_dynamic_config(path, backend_port, main_socket)
    text = path.read_text()
    text = text.replace('  routers:\n', '  routers:\n    neighbor:\n      entryPoints: [web]\n'
        '      rule: "PathPrefix(`/i12/neighbor/`)"\n      priority: 100\n'
        '      middlewares: [neighbor]\n      service: upstream\n', 1)
    text = text.replace('  routers:\n', '  routers:\n    reuse:\n      entryPoints: [web]\n'
        '      rule: "PathPrefix(`/i12/reuse/`)"\n      priority: 90\n'
        '      middlewares: [reuse]\n      service: upstream\n', 1)
    text = text.replace('  middlewares:\n', '  middlewares:\n    neighbor:\n      plugin:\n'
        '        modsecurityNative:\n          maxHeaderCount: 128\n          maxHeaderBytes: 65536\n'
        '          maxRequestChunkBytes: 32768\n          maxResponseChunkBytes: 32768\n'
        '          transactionIDHeader: X-Request-Id\n          engineMode: uds\n'
        '          engineSocketPath: ' + json.dumps(str(neighbor_socket)) + '\n', 1)
    text = text.replace('  middlewares:\n', '  middlewares:\n    reuse:\n      plugin:\n'
        '        modsecurityNative:\n          maxHeaderCount: 128\n          maxHeaderBytes: 65536\n'
        '          maxRequestChunkBytes: 32768\n          maxResponseChunkBytes: 32768\n'
        '          transactionIDHeader: X-Request-Id\n          engineMode: uds\n'
        '          engineSocketPath: ' + json.dumps(str(reuse_socket)) + '\n', 1)
    if file_target is not None:
        key, port = file_target
        if (not isinstance(key, str) or not key or len(key) > 100 or
                any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in key) or
                type(port) is not int or not 1 <= port <= 65535):
            raise ValueError('literal file target key and loopback port required')
        text = text.replace('  routers:\n', '  routers:\n    file-target:\n'
            '      entryPoints: [web]\n      rule: "Header(`X-I12-Acceptance-Key`, `' + key + '`)"\n'
            '      priority: 200\n      middlewares: [modsecurity]\n      service: file-target\n', 1)
        # Reuse the exact main middleware name from the current helper contract.
        baseline = path.read_text()
        import re
        main_middlewares = re.findall(r'^      middlewares: (.+)$', baseline, re.MULTILINE)
        if len(main_middlewares) != 1:
            raise ValueError('exact baseline main middleware required')
        text = text.replace('      middlewares: [modsecurity]\n      service: file-target',
            '      middlewares: ' + main_middlewares[0] + '\n      service: file-target', 1)
        text = text.replace('  services:\n', '  services:\n    file-target:\n      loadBalancer:\n'
            '        servers:\n          - url: "http://127.0.0.1:' + str(port) + '"\n', 1)
    path.write_text(text)


def stage_file_execution(case, root, env):
    supplement = case['fixture'].get('file_supplement')
    if supplement is None:
        return None
    validate_file_identity(case)
    source_root, evidence_root = root / 'file-source', root / 'file-evidence'
    source_root.mkdir(mode=0o700)
    evidence_root.mkdir(mode=0o700)
    manifest = FIXTURES / 'i12-file-source/manifest.json'
    if base.digest(manifest) != supplement['manifest_sha256'] or base.digest(FIXTURES / 'i12_file/supplement-plan.json') != supplement['supplement_plan_sha256']:
        raise ValueError('file supplement differs from sealed manifest/plan')
    files = json.loads(manifest.read_text())['files']
    if [spec for spec in files if spec['relative_path'] == supplement['fixture']] != [supplement['file_spec']]:
        raise ValueError('file supplement spec differs from sealed fixture')
    arguments = ['/usr/local/bin/python3', '-P', FIXTURES / 'i12_file/run.py']
    # Safe-path suppresses script-directory imports. Bind this child alone to
    # the controller's read-only sealed sibling-source directory instead.
    file_env = env | {'PYTHONPATH': str(FIXTURES / 'i12_file')}
    shared = ['--manifest', manifest, '--private-root', source_root, '--evidence-root', evidence_root]
    staged = command(case['key'] + '-file-stage', arguments + ['stage', *shared,
        '--fixture-root', FIXTURES / 'i12-file-source'], file_env)
    if staged['exit_code'] != 0:
        raise RuntimeError('physical source staging failed')
    return {'argv': arguments, 'shared': shared, 'evidence_root': evidence_root,
            'staging': staged, 'supplement': supplement, 'env': file_env}


def validate_file_identity(case):
    identity, key = case.get('transaction_id'), case.get('key')
    for value in (identity, key):
        if (not isinstance(value, str) or not 1 <= len(value) <= 100 or
                any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in value)):
            raise ValueError('distinct sealed file key and transaction ID required')
    if identity == key:
        raise ValueError('file correlation key must differ from native transaction ID')


def file_process_argv(execution, mode, port, case):
    validate_file_identity(case)
    if mode not in ('client', 'backend'):
        raise ValueError('literal file HTTP mode required')
    argv = execution['argv'] + [mode, *execution['shared'], '--port', port,
        '--key', case['key'], '--transaction-id', case['transaction_id'],
        '--fixture', execution['supplement']['fixture']]
    if mode == 'client':
        argv += ['--uri', case['fixture']['request']['uri']]
    return argv


def strict_configuration(text):
    if text.count('phase4_mode=safe') != 1:
        raise ValueError('exactly one Safe phase4 configuration required for Strict negative')
    return text.replace('phase4_mode=safe', 'phase4_mode=strict', 1)


def file_backend_ready(process, marker, evidence_root, key, port, timeout=10):
    """Observe bind/listen metadata without consuming the single target accept."""
    deadline = time.monotonic() + timeout
    path = evidence_root / (key + '.backend-listening.json')
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError('file backend exited before listening')
        if path.is_file():
            if path.stat().st_size > 4096:
                raise ValueError('bounded file backend listening receipt required')
            try:
                receipt = json.loads(path.read_text())
            except json.JSONDecodeError:
                time.sleep(0.02)
                continue  # The live child can still be writing its fresh receipt.
            if receipt.get('port') != port or receipt.get('pid') != base.actual_pid(process, marker):
                raise ValueError('file backend listening PID/port mismatch')
            return receipt
        time.sleep(0.02)
    raise RuntimeError('file backend listening receipt deadline reached')


def append_rules(path, fixture, log_root):
    lines = list(fixture['rules_lines'])
    # Audit/debug destination relocation only. Product rules/body policies stay
    # exactly fixture-bound; their source digest is recorded separately.
    lines = [line for line in lines if not line.lstrip().startswith(('SecAuditLog ', 'SecAuditLogStorageDir ', 'SecDebugLog '))]
    lines += ['SecAuditEngine On', 'SecAuditLogType Serial', 'SecAuditLogParts ABCEFHJKZ',
              'SecAuditLog ' + str(log_root / 'audit.log'), 'SecDebugLog ' + str(log_root / 'debug.log'), 'SecDebugLogLevel 9']
    path.write_text('\n'.join(lines) + '\n')


def run(helper, inputs, artifacts, engine, host, env):
    manifest = json.loads(MANIFEST.read_text())
    (TASK / 'cases').mkdir(mode=0o700)
    handles, persistent = [], {}
    all_results = []
    backend_port, host_port = helper.free_port(), helper.free_port()
    lifecycle_path = artifacts.logs_dir / 'native-lifecycle.jsonl'
    host_path = artifacts.logs_dir / 'host-lifecycle.jsonl'
    for path in (lifecycle_path, host_path):
        path.touch(mode=0o600, exist_ok=True)
    lifecycle_fd = os.open(lifecycle_path, os.O_WRONLY | os.O_APPEND)
    neighbor_dir = helper.create_private_engine_socket_dir(inputs.engine_socket_parent)
    neighbor_socket = neighbor_dir.path / helper.ENGINE_SOCKET_FILENAME
    neighbor_config = TASK / 'neighbor.conf'
    neighbor_rules = TASK / 'neighbor-rules.conf'
    neighbor_rules.write_text('SecRuleEngine On\nSecRequestBodyAccess On\nSecResponseBodyAccess On\nSecResponseBodyMimeType text/plain\n')
    helper.write_engine_config(neighbor_config, neighbor_rules, TASK / 'neighbor-events.jsonl')
    native_env = env | {'MSCONNECTOR_LIFECYCLE_FD': str(lifecycle_fd),
        'MSCONNECTOR_LIFECYCLE_RUN': 'tf-i12-acceptance-native-20261015',
        'MSCONNECTOR_LIFECYCLE_PROFILE': 'traefik-native-uds'}
    neighbor_batch, neighbor_uses = None, 0

    def start_neighbor_batch(index):
        offset = lifecycle_path.stat().st_size
        process = base.start('neighbor-engine-batch-' + str(index),
            [engine, '--serve', '--config', neighbor_config, '--socket', neighbor_socket],
            native_env | {'MSCONNECTOR_LIFECYCLE_CASE': 'independent-neighbor-control-batch-' + str(index)}, handles, (lifecycle_fd,))
        persistent['neighbor-engine'] = (process, str(engine))
        helper.wait_for_socket(neighbor_socket, process, 'independent healthy native engine')
        return {'batch_index': index, 'pid': base.actual_pid(process, str(engine)), 'native_log_start': offset,
            'configuration_sha256': base.digest(neighbor_config), 'batch_size': NEIGHBOR_BATCH_SIZE}

    def stop_neighbor_batch():
        return stop('neighbor-engine', *persistent['neighbor-engine'])

    try:
        # Parser acceptance and profile startup admission are different claims.
        # Native Strict capability is rejected by profile binding, not necessarily
        # by the generic configuration parser. No traffic/lifecycle is invented.
        strict_dir = helper.create_private_engine_socket_dir(inputs.engine_socket_parent)
        strict_config = TASK / 'strict-capability.conf'
        strict_config.write_text(strict_configuration(neighbor_config.read_text()))
        strict_receipt = {'route': 'traefik-native-uds', 'configuration_sha256': base.digest(strict_config),
            'native_transactions_claimed': False, 'qualification': None}
        try:
            strict_env = native_env | {'MSCONNECTOR_LIFECYCLE_CASE': 'supplementary-native-strict-startup'}
            strict_receipt['parser'] = command('strict-capability-configtest',
                [engine, '--check-config', '--config', strict_config], strict_env, (lifecycle_fd,))
            strict_receipt['startup'] = command('strict-capability-startup',
                [engine, '--serve', '--config', strict_config, '--socket', strict_dir.path / helper.ENGINE_SOCKET_FILENAME],
                strict_env, (lifecycle_fd,))
        except Exception as error:
            strict_receipt['execution_error'] = {'type': type(error).__name__, 'message': str(error)}
        finally:
            strict_receipt['socket_removed'] = not (strict_dir.path / helper.ENGINE_SOCKET_FILENAME).exists()
            strict_receipt['socket_directory_cleanup'] = helper.remove_private_engine_socket_dir(strict_dir, inputs.engine_socket_parent)
            base.write('strict-capability.json', strict_receipt)
        backend_script = FIXTURES / 'acceptance_backend.py'
        backend = base.start('backend', ['/usr/local/bin/python3', '-P', backend_script, backend_port, MANIFEST], env, handles)
        persistent['backend'] = (backend, str(backend_script))
        helper.wait_for_port(backend_port, backend, 'independent early-entry backend')
        executions = manifest['cases'] + manifest.get('supplementary_executions', [])
        selected = manifest.get('selected_keys')
        if selected is not None:
            known = {case['key'] for case in executions}
            if not isinstance(selected, list) or len(set(selected)) != len(selected) or not set(selected) <= known:
                raise ValueError('Invalid original-case execution filter')
            executions = [case for case in executions if case['key'] in selected]
        for case in executions:
            key = case['key']
            root = TASK / 'cases' / key
            root.mkdir(mode=0o700)
            fixture = case['fixture']
            result = {'id': case['id'], 'key': key, 'fixture_sha256': case['fixture_sha256'],
                'started_ns': time.monotonic_ns(), 'qualification': None,
                'contract_blockers': case['contract_blockers'], 'processes': {},
                'native_log_start': lifecycle_path.stat().st_size, 'host_log_start': host_path.stat().st_size}
            processes = {}
            socket_dir = helper.create_private_engine_socket_dir(inputs.engine_socket_parent)
            engine_socket = socket_dir.path / helper.ENGINE_SOCKET_FILENAME
            fault_fd = os.open(root / 'faults.jsonl', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            proxy_identity = None
            try:
                file_execution = stage_file_execution(case, root, env)
                file_target = None
                if file_execution is not None:
                    result['physical_file'] = {'staging': file_execution['staging'],
                        'evidence_root': str(file_execution['evidence_root']),
                        'native_file_api': False, 'qualification': None,
                        'backend_exclusion_expected': False}
                    if file_execution['supplement']['physical_reader'] == 'backend':
                        file_port = helper.free_port()
                        file_script = FIXTURES / 'i12_file/run.py'
                        file_backend = base.start(key + '-file-backend',
                            file_process_argv(file_execution, 'backend', file_port, case), file_execution['env'], handles)
                        processes['file-backend'] = (file_backend, str(file_script))
                        result['physical_file']['listening'] = file_backend_ready(file_backend,
                            str(file_script), file_execution['evidence_root'], key, file_port)
                        file_target = (key, file_port)
                rules_path, config = root / 'rules.conf', root / 'engine.conf'
                append_rules(rules_path, fixture, root)
                helper.write_engine_config(config, rules_path, root / 'events.jsonl')
                config.write_text(config.read_text().replace('phase4_mode=safe', 'phase4_mode=' + fixture['policy']['phase4_mode']))
                if fixture.get('max_event_json_bytes') is not None:
                    limit = fixture['max_event_json_bytes']
                    if not isinstance(limit, int) or not 1 <= limit <= 16384:
                        raise ValueError('event capacity outside current product limit')
                    config.write_text(config.read_text().replace('max_event_json_bytes=16384', 'max_event_json_bytes=' + str(limit)))
                if case['id'].endswith('unsafe_event_path'):
                    unsafe = root / 'unsafe-event-directory'
                    unsafe.mkdir(mode=0o777)
                    config.write_text(config.read_text().replace(str(root / 'events.jsonl'), str(unsafe)))
                if case['classification'] == 'config':
                    result['configtest'] = command(key + '-configtest', [engine, '--check-config', '--config', config],
                        native_env | {'MSCONNECTOR_LIFECYCLE_CASE': case['id']}, (lifecycle_fd,))
                    result['configuration'] = {str(p): base.digest(p) for p in (config, rules_path)}
                    result['configuration_only'] = True
                    continue
                neighbor_batch = prepare_neighbor_batch(neighbor_uses, neighbor_batch, lifecycle_path,
                    neighbor_socket, stop_neighbor_batch, start_neighbor_batch)
                neighbor_uses += 1
                result['neighbor_batch'] = neighbor_batch
                for mode in fixture.get('literal_negative_config_modes', []):
                    negative_config = root / ('negative-' + mode + '.conf')
                    negative_config.write_text(config.read_text().replace('phase4_mode=off', 'phase4_mode=' + mode))
                    result['literal_negative_config'] = command(key + '-negative-' + mode,
                        [engine, '--check-config', '--config', negative_config],
                        native_env | {'MSCONNECTOR_LIFECYCLE_CASE': case['id'] + '::negative-minimal'}, (lifecycle_fd,))
                engine_env = native_env | {'MSCONNECTOR_LIFECYCLE_CASE': case['id'],
                    'I12_ACCEPTANCE_FAULT': fault_mode(case), 'I12_ACCEPTANCE_FAULT_FD': str(fault_fd),
                    'I12_ACCEPTANCE_FAULT_URI': fixture['request']['uri'],
                    'I12_ACCEPTANCE_EVENT_PATH': str(root / 'events.jsonl')}
                host_env = dict(env)
                host_env.pop('I12_NATIVE_GENERATED_CASE', None)
                if fixture['request'].get('omit_transaction_id'):
                    if key != '004-b044cc412aca':
                        raise ValueError('unreviewed generated-ID capture case')
                    host_env['I12_NATIVE_GENERATED_CASE'] = key
                result['generated_id_child_environment'] = {'name': 'I12_NATIVE_GENERATED_CASE',
                    'present': 'I12_NATIVE_GENERATED_CASE' in host_env,
                    'value': host_env.get('I12_NATIVE_GENERATED_CASE'), 'dedicated_host': True}
                if fault_mode(case) == 'sink-open':
                    # Healthy same-image service controls must bracket the actual
                    # constructor failure, not merely the later client request.
                    dynamic_config(helper, artifacts.dynamic_config, backend_port, engine_socket, neighbor_socket, engine_socket)
                    helper.write_static_config(artifacts.static_config, artifacts.dynamic_config, host_port, inputs.module_name)
                    pre_host = base.start(key + '-traefik', [host, '--configFile=' + str(artifacts.static_config)], host_env, handles)
                    processes['traefik'] = (pre_host, str(host))
                    helper.wait_for_port(host_port, pre_host, 'healthy host before sink constructor failure')
                    result['readiness'] = http_readiness(case, host_port, env, lifecycle_path, base.actual_pid(pre_host, str(host)))
                    result['startup_neighbor_before'] = command(key + '-startup-neighbor-before',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'neighbor-before'], env)
                    base.snapshot(key + '-before-startup-fault', persistent | {'traefik': processes['traefik']})
                native = base.start(key + '-engine', [engine, '--serve', '--config', config, '--socket', engine_socket],
                    engine_env, handles, (lifecycle_fd, fault_fd))
                processes['engine'] = (native, str(engine))
                try:
                    helper.wait_for_socket(engine_socket, native, 'selected original-ID native engine')
                    result['engine_started'] = True
                except Exception as error:
                    result['engine_started'] = False
                    result['engine_start_error'] = {'type': type(error).__name__, 'message': str(error)}
                fault_kind = (fixture.get('fault') or {}).get('kind')
                host_socket = engine_socket
                if result['engine_started'] and fault_kind in ('mse1-error', 'invalid-metadata', 'commit-ack-applied',
                        'incomplete-framing', 'no-second-response', 'timeout', 'engine_timeout_before_commit', 'engine_timeout_after_commit'):
                    host_socket = Path('/task/sockets/proxy.sock')
                    script = FIXTURES / 'acceptance_proxy.py'
                    proxy = base.start(key + '-proxy', ['/usr/local/bin/python3', '-P', script,
                        host_socket, engine_socket, MANIFEST, key], env, handles)
                    processes['proxy'] = (proxy, str(script))
                    helper.wait_for_socket(host_socket, proxy, 'selected-operation actual MSE1 relay')
                elif fault_kind == 'uds-error':
                    host_socket = Path('/task/sockets/proxy.sock')
                    peer = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    peer.bind(str(host_socket))
                    proxy_identity = host_socket.lstat()
                    peer.close()  # Physical socket entry, no listener: real ECONNREFUSED.
                dynamic_config(helper, artifacts.dynamic_config, backend_port, host_socket, neighbor_socket, engine_socket, file_target)
                helper.write_static_config(artifacts.static_config, artifacts.dynamic_config, host_port, inputs.module_name)
                result['configuration'] = {str(p): base.digest(p) for p in (config, rules_path, artifacts.static_config, artifacts.dynamic_config)}
                result['native_log_start'] = lifecycle_path.stat().st_size
                result['host_log_start'] = host_path.stat().st_size
                if 'traefik' in processes:
                    host_process = processes['traefik'][0]
                else:
                    host_argv = [host, '--configFile=' + str(artifacts.static_config)]
                    tracer = fixture.get('syscall_observer')
                    if tracer:
                        host_argv = [TASK / 'build/acceptance-syscalls', '--output', root / 'host-syscalls.jsonl',
                            '--nonce', tracer['nonce'], '--host-port', str(host_port), '--peer-port', '0',
                            '--seconds', str(tracer['seconds'])]
                        result['syscall_observer'] = {'argv': list(map(str, host_argv)),
                            'source_sha256': base.digest(FIXTURES / 'acceptance_syscalls.c'),
                            'binary_sha256': base.digest(TASK / 'build/acceptance-syscalls'),
                            'qualification': None, 'missing_kernel_proof_is_unknown': True}
                    host_process = base.start(key + '-traefik', host_argv, host_env, handles)
                    processes['traefik'] = (host_process, str(host))
                helper.wait_for_port(host_port, host_process, 'actual pinned Traefik original-ID fixture')
                if 'readiness' not in result:
                    result['readiness'] = http_readiness(case, host_port, env, lifecycle_path, base.actual_pid(host_process, str(host)))
                alive = persistent | {name: value for name, value in processes.items() if value[0].poll() is None}
                base.snapshot(key + '-before', alive)
                if result['engine_started']:
                    result['main_engine_before'] = command(key + '-main-before',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'main-before'], env)
                if not result['engine_started'] and 'startup_neighbor_before' not in result:
                    result['startup_neighbor_before'] = command(key + '-startup-neighbor-before',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'neighbor-before'], env)
                if fault_kind == 'commit-ack-applied':
                    result['positive_ack_control'] = command(key + '-ack-control',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'ack-control'], env)
                # Exercise independent traffic while the target's host/worker
                # operation is active, and retain same-engine controls separately.
                with ThreadPoolExecutor(max_workers=1) as executor:
                    neighbor_future = executor.submit(command, key + '-neighbor',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'neighbor'], env)
                    client_argv = ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key]
                    if file_execution is not None and file_execution['supplement']['physical_reader'] == 'client':
                        client_argv = file_process_argv(file_execution, 'client', host_port, case)
                    client_env = file_execution['env'] if file_execution is not None and file_execution['supplement']['physical_reader'] == 'client' else env
                    result['client'] = command(key + '-client', client_argv, client_env,
                        timeout_seconds=fixture.get('target_timeout_seconds', 30))
                    result['neighbor'] = neighbor_future.result()
                if fixture.get('sequence'):
                    result['original_sequence'] = [command(key + '-sequence-' + str(index),
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'sequence-' + str(index)], env)
                        for index in range(len(fixture['sequence']))]

                if result['engine_started'] and fixture.get('sink_recovery_control'):
                    result['sink_recovery_control'] = command(key + '-sink-recovery',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'sink-recovery'], env)
                if result['engine_started']:
                    result['main_engine_after'] = command(key + '-main-after',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'main-after'], env)
                if not result['engine_started']:
                    result['startup_neighbor_after'] = command(key + '-startup-neighbor-after',
                        ['/usr/local/bin/python3', '-P', FIXTURES / 'acceptance_client.py', host_port, MANIFEST, key, 'neighbor-after'], env)
                # A failed target must never suppress independent neighbor evidence.
                time.sleep(0.2)
                base.snapshot(key + '-after', persistent | {name: value for name, value in processes.items() if value[0].poll() is None})
            except Exception as error:
                result['execution_error'] = {'type': type(error).__name__, 'message': str(error)}
            finally:
                for label in ('traefik', 'proxy', 'engine', 'file-backend'):
                    if label in processes:
                        try:
                            result['processes'][label] = stop(label, *processes[label])
                        except Exception as error:
                            result.setdefault('cleanup_errors', []).append({'label': label, 'error': str(error)})
                if proxy_identity is not None:
                    candidate = Path('/task/sockets/proxy.sock')
                    current = candidate.lstat()
                    if stat.S_ISSOCK(current.st_mode) and (current.st_dev, current.st_ino) == (proxy_identity.st_dev, proxy_identity.st_ino):
                        candidate.unlink()
                result['socket_removed'] = not engine_socket.exists()
                result['socket_directory_cleanup'] = helper.remove_private_engine_socket_dir(socket_dir, inputs.engine_socket_parent)
                result['native_log_end'] = lifecycle_path.stat().st_size
                result['host_log_end'] = host_path.stat().st_size
                # Preserve each physical append-only segment before admitting
                # the next host process. Keep the original observer's1MiB cap.
                (root / 'host-lifecycle.jsonl').write_bytes(host_path.read_bytes())
                result['host_capture_sha256'] = base.digest(root / 'host-lifecycle.jsonl')
                host_path.write_bytes(b'')
                result['completed_ns'] = time.monotonic_ns()
                os.close(fault_fd)
                (root / 'measurement.json').write_text(json.dumps(result, indent=2) + '\n')
                all_results.append(result)
    finally:
        cleanup = {}
        for label in ('neighbor-engine', 'backend'):
            if label in persistent:
                try:
                    cleanup[label] = stop(label, *persistent[label])
                except Exception as error:
                    cleanup[label] = {'cleanup_error': {'type': type(error).__name__, 'message': str(error)}}
        if neighbor_batch is not None:
            native = neighbor_scope_status(lifecycle_path, neighbor_batch, final=True)
            cleanup['neighbor_native_final'] = native
            base.write('neighbor-batch-' + str(neighbor_batch['batch_index']) + '-final.json', {
                'batch': neighbor_batch, 'process': cleanup.get('neighbor-engine'), 'native': native,
                'socket_removed': not neighbor_socket.exists()})
        os.close(lifecycle_fd)
        for handle in handles:
            handle.close()
        cleanup['neighbor_socket_removed'] = not neighbor_socket.exists()
        cleanup['neighbor_socket_directory_cleanup'] = helper.remove_private_engine_socket_dir(neighbor_dir, inputs.engine_socket_parent)
        base.write('acceptance-result.json', {'route': 'traefik-native-uds', 'qualification': None,
            'original_ids_planned': 118, 'original_ids_attempted': len({row['id'] for row in all_results}),
            'executions_attempted': len(all_results), 'selected_keys': manifest.get('selected_keys'),
            'results': all_results, 'cleanup': cleanup})
