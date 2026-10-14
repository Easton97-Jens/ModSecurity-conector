"""One selected EOS obligation, separate neighbor, original physical artifacts."""
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

SOURCE = Path('/mnt/src')
TASK = Path('/task')
FIXTURES = Path('/mnt/fixtures')
ARTIFACTS = Path('/mnt/artifacts/traefik')
SDK_SHA = '32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407'
CASE = 'I12::traefik-native-uds::NEED-request-eos-once'
RUN = 'tf-i12-eos-20261014'
TARGET = 'eos-target-53b4c671'
NEIGHBOR = 'eos-neighbor-8f217a3c'
SYMBOLS = ('msconnector_transaction_contract_init', 'msconnector_transaction_contract_finish',
    'msconnector_transaction_contract_cleanup', 'msconnector_transaction_contract_complete_phase',
    'msconnector_transaction_contract_set_response_committed', 'msconnector_transaction_contract_record_response_metadata',
    'msc_new_transaction', 'msc_new_transaction_with_id', 'msc_transaction_cleanup',
    'msc_process_request_body', 'msc_process_response_body', 'msc_process_logging',
    'msc_append_request_body', 'msc_append_response_body', 'msc_process_request_headers',
    'msc_process_response_headers', 'msc_intervention',
    'msconnector_runtime_transaction_begin', 'msconnector_runtime_transaction_begin_request_stream',
    'msconnector_runtime_transaction_append_request_body_chunk', 'msconnector_runtime_transaction_finish_request_body',
    'msconnector_runtime_transaction_process_response_headers', 'msconnector_runtime_transaction_append_response_body_chunk',
    'msconnector_runtime_transaction_finish_response_body', 'msconnector_runtime_transaction_finish',
    'msconnector_runtime_transaction_destroy')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(name, value):
    (TASK / name).write_text(json.dumps(value, indent=2) + '\n')

def execute(label, argv, environment):
    command = ['rtk', 'proxy', *map(str, argv)]
    with (TASK / f'{label}.stdout').open('wb') as stdout, (TASK / f'{label}.stderr').open('wb') as stderr:
        result = subprocess.run(command, env=environment, cwd=SOURCE, stdout=stdout, stderr=stderr, timeout=240)
    receipt = {'argv': command, 'cwd': str(SOURCE), 'exit_code': result.returncode,
               'stdout_sha256': digest(TASK / f'{label}.stdout'), 'stderr_sha256': digest(TASK / f'{label}.stderr')}
    write(f'{label}.command.json', receipt)
    if result.returncode:
        raise RuntimeError(f'{label} exited {result.returncode}')

def descendants(process):
    queue, result = [process.pid], []
    while queue:
        pid = queue.pop()
        result.append(pid)
        try:
            child_text = Path(f'/proc/{pid}/task/{pid}/children').read_text()
        except FileNotFoundError:
            continue
        queue.extend(int(value) for value in child_text.split())
        if len(result) > 128:
            raise RuntimeError('bounded task process inventory exceeded')
    return result

def actual_pid(process, marker):
    found = []
    for pid in descendants(process):
        try:
            arguments = Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
        except FileNotFoundError:
            continue
        direct_binary = arguments[0] == marker.encode()
        direct_python = arguments[:3] == [b'/usr/local/bin/python3', b'-P', marker.encode()]
        if direct_binary or direct_python:
            found.append(pid)
    if len(found) != 1:
        raise RuntimeError(f'exact process identity unavailable for {marker}: {found}')
    return found[0]

def snapshot(label, processes):
    value = {'monotonic_ns': time.monotonic_ns(), 'wall_ns': time.time_ns(), 'processes': {}}
    value['clock_calibration'] = {'wall_before_ns': time.time_ns(), 'monotonic_ns': time.monotonic_ns(), 'wall_after_ns': time.time_ns()}
    for name, (process, marker) in processes.items():
        pid = actual_pid(process, marker)
        base = Path(f'/proc/{pid}')
        status = base.joinpath('status').read_text()
        maps = base.joinpath('maps').read_text()
        (TASK / f'{label}.{name}.maps.raw').write_text(maps)
        (TASK / f'{label}.{name}.status.raw').write_text(status)
        descriptors = {}
        vanished = []
        for descriptor in sorted(base.joinpath('fd').iterdir(), key=lambda item: int(item.name)):
            try:
                descriptors[descriptor.name] = os.readlink(descriptor)
            except FileNotFoundError:
                vanished.append(descriptor.name)
        executable = os.readlink(base / 'exe')
        libraries = sorted({line.split()[-1] for line in maps.splitlines()
                            if 'libmodsecurity.so' in line and line.split()[-1].startswith('/')})
        record = {'pid': pid, 'proxy_pid': process.pid, 'executable': executable,
                  'executable_sha256': digest(base / 'exe'), 'fd_count': len(descriptors),
                  'fds': descriptors, 'vanished_during_snapshot': vanished,
                  'native_libraries': [{'path': item, 'sha256': digest(item)} for item in libraries],
                  'identity': {key: next((line.split(':', 1)[1].strip() for line in status.splitlines()
                      if line.startswith(key + ':')), None) for key in ('Uid', 'Gid', 'CapEff', 'CapBnd', 'NoNewPrivs')}}
        if name == 'engine' and (len(libraries) != 1 or record['native_libraries'][0]['sha256'] != SDK_SHA):
            raise RuntimeError('actual engine mapping does not bind the selected SDK')
        value['processes'][name] = record
    for name in ('tcp', 'tcp6', 'unix'):
        (TASK / f'{label}.net-{name}.raw').write_text(Path(f'/proc/net/{name}').read_text())
    write(f'{label}.json', value)

def start(label, argv, environment, handles, pass_fds=()):
    stdout = (TASK / f'{label}.stdout').open('wb')
    stderr = (TASK / f'{label}.stderr').open('wb')
    handles.extend((stdout, stderr))
    command = ['rtk', 'proxy', *map(str, argv)]
    process = subprocess.Popen(command, cwd=TASK / 'runtime', env=environment,
                               stdout=stdout, stderr=stderr, pass_fds=pass_fds)
    write(f'{label}.launch.json', {'argv': command, 'proxy_pid': process.pid, 'monotonic_ns': time.monotonic_ns()})
    return process

def main():
    if (os.geteuid(), os.getegid()) != (65534, 65534):
        raise RuntimeError('same v5 nonroot host identity required')
    for name in ('build', 'tmp', 'sockets', 'cache', 'go-cache'):
        (TASK / name).mkdir(mode=0o700)
    host = TASK / 'cache/traefik'
    shutil.copyfile(ARTIFACTS / 'host', host)
    host.chmod(0o700)
    if digest(host) != digest(ARTIFACTS / 'host'):
        raise RuntimeError('pinned host copy identity changed')
    shutil.copytree(ARTIFACTS / 'offline-mod', TASK / 'go-mod', symlinks=False)
    for path in (TASK / 'go-mod', *(TASK / 'go-mod').rglob('*')):
        path.chmod(0o700 if path.is_dir() else 0o600)
    env = os.environ.copy()
    env.update(PYTHON='/usr/local/bin/python3', BUILD_ROOT='/task/build', TMPDIR='/task/tmp', TMP_ROOT='/task/tmp',
               GOTOOLCHAIN='local', GOPROXY='off', GOSUMDB='off', GOMODCACHE='/task/go-mod', GOCACHE='/task/go-cache',
               GO='/usr/local/go/bin/go', GOFLAGS='-mod=readonly', CC='/mnt/fixtures/cc-wrapper.sh',
               CXX='/mnt/fixtures/cxx-wrapper.sh', MODSECURITY_INCLUDE_DIR='/usr/include',
               MODSECURITY_LIB_DIR='/usr/lib/x86_64-linux-gnu', TRAEFIK_BIN=str(host),
               TRAEFIK_NATIVE_RUNTIME_ROOT='/task/runtime', TRAEFIK_ENGINE_SOCKET_PARENT='/task/sockets',
               MSCONNECTOR_RULES_FILE='/task/rules.conf')
    rules = ['SecRuleEngine On', 'SecRequestBodyAccess On', 'SecResponseBodyAccess On',
             'SecRequestBodyLimit 1024', 'SecRequestBodyNoFilesLimit 1024', 'SecRequestBodyLimitAction Reject',
             'SecResponseBodyLimit 1024', 'SecResponseBodyLimitAction Reject', 'SecResponseBodyMimeType text/plain',
             'SecAuditEngine On', 'SecAuditLogType Serial', 'SecAuditLogParts ABCEFHJKZ',
             'SecAuditLog /task/runtime/logs/native-audit.log',
             'SecDebugLog /task/runtime/logs/native-debug.log', 'SecDebugLogLevel 9']
    for index, nonce in enumerate((TARGET, NEIGHBOR)):
        rules.extend((f'SecRule REQUEST_URI "@streq /i12-eos-{nonce}" "id:{1999101 + index * 10},phase:1,pass,log,msg:\'i12-p1-{nonce}\'"',
                      f'SecRule RESPONSE_BODY "@contains i12-response-marker:{nonce}" "id:{1999104 + index * 10},phase:4,pass,log,msg:\'i12-p4-{nonce}\'"'))
    (TASK / 'rules.conf').write_text('\n'.join(rules) + '\n')
    os.environ.update(env)
    spec = importlib.util.spec_from_file_location('native_fixture', SOURCE / 'connectors/traefik/scripts/runtime_native_smoke.py')
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    inputs = helper.collect_native_runtime_inputs()
    artifacts = helper.stage_native_runtime(inputs)
    socket_dir = helper.create_private_engine_socket_dir(inputs.engine_socket_parent)
    engine_socket = socket_dir.path / helper.ENGINE_SOCKET_FILENAME
    backend_port, host_port = helper.free_port(), helper.free_port()
    helper.write_static_config(artifacts.static_config, artifacts.dynamic_config, host_port, inputs.module_name)
    helper.write_dynamic_config(artifacts.dynamic_config, backend_port, engine_socket)
    helper.write_engine_config(artifacts.engine_config, inputs.rules_file, artifacts.event_path)
    for name in ('native-audit.log', 'native-debug.log', 'native-lifecycle.jsonl', 'host-lifecycle.jsonl'):
        descriptor = os.open(artifacts.logs_dir / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(descriptor)
    for label, argv in (('go-version', ['/usr/local/go/bin/go', 'version']),
                        ('host-version', [host, 'version'])):
        execute(label, argv, env)
    observer, accessor = TASK / 'build/observer.o', TASK / 'build/sdk-accessor.o'
    execute('observer-compile', ['/usr/bin/gcc', '-std=c17', '-Wall', '-Wextra', '-Werror', '-pthread',
        '-I', SOURCE / 'common/include', '-I', '/usr/include', '-c',
        SOURCE / 'ci/runtime/lifecycle/native-lifecycle-observer.c', '-o', observer], env)
    execute('sdk-accessor-compile', ['/usr/bin/g++', '-std=c++17', '-Wall', '-Wextra', '-Werror',
        '-c', SOURCE / 'ci/runtime/lifecycle/native-lifecycle-sdk.cpp', '-o', accessor], env)
    execute('sdk-who-compile', ['/usr/bin/gcc', '-std=c17', '-Wall', '-Wextra', '-Werror',
        FIXTURES / 'sdk-who.c', '-lmodsecurity', '-o', TASK / 'build/sdk-who'], env)
    execute('sdk-who', [TASK / 'build/sdk-who'], env)
    env['TRAEFIK_ENGINE_SERVICE_LDFLAGS'] = ' '.join([str(observer), str(accessor), *(f'-Wl,--wrap={symbol}' for symbol in SYMBOLS)])
    env['TRAEFIK_ENGINE_SERVICE_BUILD_DIR'] = '/task/build/engine'
    env['TRAEFIK_ENGINE_SERVICE_BIN'] = '/task/build/engine/traefik-engine-service'
    execute('engine-build', [SOURCE / 'connectors/traefik/build/build-engine-service.sh', 'build'], env)
    engine = Path(env['TRAEFIK_ENGINE_SERVICE_BIN'])
    product = json.loads((ARTIFACTS / 'preparation-manifest.json').read_text())
    equality = [{'path': relative, 'expected': expected, 'observed': digest(SOURCE / relative)}
                for relative, expected in product['source_inputs'].items()]
    write('prepared-product-source-equality.json', equality)
    overlays = json.loads((FIXTURES / 'approved-product-test-overlays.json').read_text())
    write('approved-product-test-overlays.json', overlays)
    if any((item['expected'] != item['observed'] and
            (item['path'] not in overlays or overlays[item['path']]['baseline_a9_sha256'] != item['expected'] or
             overlays[item['path']]['instrumented_sha256'] != item['observed'])) for item in equality):
        raise RuntimeError('actual product inputs differ from independently prepared source contract')
    write('build-manifest.json', {'case': CASE, 'run': RUN, 'product_base': 'a9d48bb58aa948aea7d79e20cdf09d3f239b7808',
        'delivery_base': '02754040bced960cfc1857416cd7101bb3116ef4', 'host_sha256': digest(host),
        'engine_sha256': digest(engine), 'observer_object_sha256': digest(observer),
        'sdk_accessor_object_sha256': digest(accessor), 'wrap_symbols': SYMBOLS,
        'source_inputs': {str(path.relative_to(SOURCE)): digest(path) for path in
            sorted((SOURCE / 'common/src').glob('*.c')) + sorted((SOURCE / 'common/runtime').glob('*.c')) +
            [SOURCE / 'connectors/profile_registry.c', SOURCE / 'connectors/traefik/src/traefik_engine_service.c',
             SOURCE / 'ci/runtime/lifecycle/native-lifecycle-observer.c', SOURCE / 'ci/runtime/lifecycle/native-lifecycle-sdk.cpp']},
        'configuration': {str(path): digest(path) for path in (TASK / 'rules.conf', artifacts.engine_config,
                                                             artifacts.static_config, artifacts.dynamic_config)}})
    handles, processes = [], {}
    lifecycle_fd = os.open(artifacts.logs_dir / 'native-lifecycle.jsonl', os.O_WRONLY | os.O_APPEND)
    failure = None
    final = {'case': CASE, 'qualification': 'unreviewed_measurements', 'selected_case_count': 1,
             'neighbor_health_probe_count': 1, 'processes': {}}
    try:
        backend = start('backend', ['/usr/local/bin/python3', '-P', FIXTURES / 'backend.py', str(backend_port)], env, handles)
        processes['backend'] = (backend, str(FIXTURES / 'backend.py'))
        helper.wait_for_port(backend_port, backend, 'independent backend')
        engine_env = env | {'MSCONNECTOR_LIFECYCLE_FD': str(lifecycle_fd), 'MSCONNECTOR_LIFECYCLE_RUN': RUN,
            'MSCONNECTOR_LIFECYCLE_PROFILE': 'traefik-native-uds', 'MSCONNECTOR_LIFECYCLE_CASE': CASE}
        native = start('engine', [engine, '--serve', '--config', artifacts.engine_config, '--socket', engine_socket],
                       engine_env, handles, (lifecycle_fd,))
        processes['engine'] = (native, str(engine))
        helper.wait_for_socket(engine_socket, native, 'actual instrumented native service')
        host_process = start('traefik', [host, f'--configFile={artifacts.static_config}'], env, handles)
        processes['traefik'] = (host_process, str(host))
        helper.wait_for_port(host_port, host_process, 'actual pinned Traefik')
        snapshot('before-target', processes)
        for label, nonce in (('target', TARGET), ('neighbor', NEIGHBOR)):
            transaction_id = 'tf-' + nonce
            execute(f'client-{label}', ['/usr/local/bin/python3', '-P', FIXTURES / 'client.py', str(host_port),
                                      nonce, transaction_id, label], env)
            time.sleep(0.15)
            snapshot(f'after-{label}', processes)
        final['target_and_neighbor_commands_exit'] = 0
    except Exception as error:
        failure = error
        final['failure'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        for label in ('traefik', 'engine', 'backend'):
            if label not in processes:
                continue
            process, marker = processes[label]
            target_pid = None
            try:
                if process.poll() is None:
                    target_pid = actual_pid(process, marker)
                    os.kill(target_pid, signal.SIGTERM)
                    process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.kill(target_pid, signal.SIGKILL)
                process.wait(timeout=5)
                final.setdefault('cleanup_errors', []).append({'process': label, 'reason': 'graceful-stop timeout'})
            except Exception as error:
                final.setdefault('cleanup_errors', []).append({'process': label, 'type': type(error).__name__, 'message': str(error)})
            final['processes'][label] = {'actual_pid': target_pid, 'proxy_pid': process.pid, 'exit_code': process.returncode}
        os.close(lifecycle_fd)
        for handle in handles:
            handle.close()
        final['socket_removed'] = not engine_socket.exists()
        final['socket_directory_cleanup'] = helper.remove_private_engine_socket_dir(socket_dir, inputs.engine_socket_parent)
        write('result.json', final)
    if failure is not None:
        raise failure
    if final.get('cleanup_errors') or not final['socket_removed'] or not final['socket_directory_cleanup']:
        raise RuntimeError('private service socket cleanup incomplete')
    print(json.dumps({'case': CASE, 'selected_case_count': 1, 'neighbor_count': 1, 'driver_exit': 0}))

if __name__ == '__main__':
    main()
