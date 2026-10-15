#!/usr/local/bin/python3
"""Reviewed external controller: no host starts without an explicit sealed spec.

Root must review this file, seal it and its sibling, and supply the approved
binding ledgers/spec. No scanner, native harness or namespace attestation is
modified here. Bootstrap -> chroot -> setpriv removes privileged setup before
any candidate is executed. Only the controller retains host authority.
"""
import argparse
import datetime
import hashlib
import json
import os
import resource
from pathlib import Path
import signal
import select
import socket
import stat
import subprocess
import sys
import time
import tomllib

RUN = Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle')
ROOT = RUN / 'isolation'
RTK = '/root/.local/bin/rtk'
SYSTEM = {'unshare': '/usr/bin/unshare', 'setpriv': '/usr/bin/setpriv', 'mount': '/usr/bin/mount', 'ip': '/usr/sbin/ip'}
CAPS = ('CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb')

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()

def trusted(path, directory=False):
    path = Path(path)
    current = path
    while True:
        detail = current.lstat()
        sticky_parent = current == Path('/var/tmp') and detail.st_uid == 0 and bool(detail.st_mode & stat.S_ISVTX)
        if stat.S_ISLNK(detail.st_mode) or detail.st_uid != 0 or (detail.st_mode & 0o022 and not sticky_parent):
            raise ValueError('untrusted input path: ' + str(current))
        if current == Path('/'):
            break
        current = current.parent
    d = path.lstat()
    if directory != stat.S_ISDIR(d.st_mode):
        raise ValueError('unexpected input kind: ' + str(path))
    if not directory and not stat.S_ISREG(d.st_mode):
        raise ValueError('input is not regular')

def sealed(path):
    trusted(path)
    if path.stat().st_mode & 0o222:
        raise ValueError('input must be sealed read-only: ' + str(path))

def read_spec(path):
    sealed(path)
    spec = json.loads(path.read_text())
    if spec['mode'] not in ('nonroot', 'nginx-root-master', 'nginx-root-master-dac', 'nginx-root-master-lifecycle'):
        raise ValueError('unsupported identity mode')
    if not isinstance(spec['timeout_seconds'], int) or not 1 <= spec['timeout_seconds'] <= 1800:
        raise ValueError('invalid timeout')
    if not spec['argv'] or not all(isinstance(x, str) and x and '\x00' not in x and len(x) <= 8192 for x in spec['argv']):
        raise ValueError('invalid argv')
    if not spec['argv'][0].startswith('/'):
        raise ValueError('absolute candidate executable required')
    if any(k.startswith(('LD_', 'LIGHTTPD_NO_CRS_FIXTURE_NAMESPACE')) or (k.startswith('PYTHON') and k != 'PYTHON') for k in spec.get('environment', {})):
        raise ValueError('loader/Python/native attestation environment forbidden')
    allowed = {'CONNECTOR_ROOT', 'FRAMEWORK_ROOT', 'RUNTIME_ROOT', 'BUILD_ROOT', 'VERIFIED_RUN_ROOT', 'MODSEC_SMOKE_ROOT', 'LIGHTTPD_PATCHED_ROOT', 'NGINX_BINARY', 'APACHE_BINARY', 'APACHE_MODULE', 'RULES_FILE', 'RUN_ID', 'FIXTURE_ID', 'FRAMEWORK_OUTPUT_ROOT', 'PYTHON', 'TMP_ROOT', 'EVENT_OUTPUT_ROOT'}
    if set(spec.get('environment', {})) - allowed:
        raise ValueError('environment key outside explicit allowlist')
    for value in spec.get('environment', {}).values():
        if not isinstance(value, str) or '\x00' in value or '\n' in value or len(value) > 4096:
            raise ValueError('invalid environment value')
    if type(spec.get('nginx_worker_alias', False)) is not bool or (spec.get('nginx_worker_alias') and spec['mode'] not in ('nginx-root-master', 'nginx-root-master-dac', 'nginx-root-master-lifecycle')):
        raise ValueError('worker runtime alias requires the explicit NGINX master mode')
    destinations = set()
    for binding in spec['bindings']:
        target = binding['target']
        if target not in ('/mnt/src', '/mnt/framework', '/mnt/artifacts', '/mnt/fixtures', '/mnt/git', '/mnt/git-framework', '/usr/local/lib/python3.14/site-packages') or target in destinations:
            raise ValueError('invalid/duplicate binding destination')
        destinations.add(target)
        source = Path(binding['source'])
        if not source.is_absolute() or '..' in source.parts or source.resolve(strict=True) != source or not source.is_relative_to(RUN):
            raise ValueError('binding outside current run')
        trusted(source, True)
        if source.stat().st_mode & 0o222:
            raise ValueError('binding root must be sealed read-only')
        ledger = Path(binding['ledger'])
        sealed(ledger)
        if digest(ledger) != binding['ledger_sha256']:
            raise ValueError('ledger identity mismatch')
        inventory = json.loads(ledger.read_text())
        records = inventory['files']
        approved_links = inventory.get('symlinks', {})
        if approved_links and target != '/mnt/framework':
            raise ValueError('only exact Framework-contained Git links may be admitted')
        if approved_links:
            prefix = 'tests/mrts/infra-overlays/nginx-pr24/infra/'
            reviewed = {prefix + 'modules-enabled/' + name: '../modules-available/' + name for name in ('mod-http-geoip2.conf', 'mod-http-headers-more-filter.conf', 'mod-http-image-filter.conf', 'mod-http-modsecurity.conf', 'mod-http-xslt-filter.conf', 'mod-mail.conf', 'mod-stream-geoip2.conf', 'mod-stream.conf')}
            reviewed[prefix + 'sites-enabled/default'] = '../sites-available/default'
            if approved_links != reviewed:
                raise ValueError('Framework links differ from reviewed exact99a set')
        actual = set()
        actual_links = {}
        for parent, directories, files in os.walk(source, followlinks=False):
            for name in directories + files:
                p = Path(parent) / name
                d = p.lstat()
                if stat.S_ISLNK(d.st_mode):
                    relative = str(p.relative_to(source))
                    link = os.readlink(p)
                    if d.st_uid != 0 or approved_links.get(relative) != link or Path(link).is_absolute() or not p.resolve(strict=True).is_relative_to(source) or not p.resolve(strict=True).is_file():
                        raise ValueError('unapproved or escaping Framework symlink')
                    actual_links[relative] = link
                    continue
                if d.st_uid != 0 or d.st_mode & 0o222:
                    raise ValueError('binding contains mutable/foreign/symlink input: ' + str(p))
                if not (stat.S_ISDIR(d.st_mode) or stat.S_ISREG(d.st_mode)):
                    raise ValueError('binding contains special input')
                if stat.S_ISREG(d.st_mode):
                    actual.add(str(p.relative_to(source)))
        if actual != set(records) or actual_links != approved_links:
            raise ValueError('binding ledger inventory mismatch')
        for relative, sha in records.items():
            path = source / relative
            if not path.is_relative_to(source) or '..' in Path(relative).parts or digest(path) != sha:
                raise ValueError('binding content mismatch')
        git_binding = target in ('/mnt/git', '/mnt/git-framework')
        if not git_binding and any('.git' in Path(x).parts for x in actual):
            raise ValueError('candidate source must not expose host Git metadata')
        if git_binding:
            # Root still reviews a credential-free real Git snapshot. Fail closed
            # for includes, URLs, executable hooks and any credential fields.
            config = source / 'config'
            text = config.read_text() if config.is_file() else ''
            if any(word in text.lower() for word in ('url', 'credential', 'include', 'hook', 'ssh', 'proxy')):
                raise ValueError('Git snapshot config is not credential-free')
            if any(x.startswith('hooks/') for x in actual):
                raise ValueError('Git snapshot hooks forbidden')
            if 'objects/info/alternates' in actual or 'commondir' in actual:
                raise ValueError('Git snapshot external object/worktree references forbidden')
            if 'worktree' in text.lower():
                raise ValueError('Git snapshot cannot redirect the mounted worktree')
    return spec

def run(command, **kw):
    return subprocess.run([RTK, 'proxy', *command], check=True, env={'PATH': '/usr/bin:/usr/sbin:/bin', 'HOME': str(ROOT), 'XDG_DATA_HOME': str(ROOT / 'rtk-data')}, **kw)

def namespace_processes(namespace):
    result = []
    if namespace is None:
        return result
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit():
            continue
        try:
            if os.readlink(proc / 'ns/pid') != namespace:
                continue
            fields = dict(line.split(':', 1) for line in (proc / 'status').read_text().splitlines() if ':' in line)
            result.append({'pid': int(proc.name), 'rss_bytes': int(fields.get('VmRSS', '0 kB').split()[0]) * 1024, 'threads': int(fields.get('Threads', '1'))})
        except (FileNotFoundError, ProcessLookupError):
            continue
    return result

def regular_bytes(path):
    size = 0
    for parent, dirs, names in os.walk(path, followlinks=False):
        dirs[:] = [name for name in dirs if not (Path(parent) / name).is_symlink()]
        for name in names:
            try:
                entry = (Path(parent) / name).lstat()
                if stat.S_ISREG(entry.st_mode):
                    size += entry.st_size
            except FileNotFoundError:
                continue
    return size

def matching_init(boot):
    if not boot:
        return False
    init = Path('/proc') / str(boot['host_pid'])
    try:
        start = (init / 'stat').read_text().rsplit(')', 1)[1].split()[19]
        return start == boot['start_time'] and os.readlink(init / 'ns/pid') == boot['namespaces']['pid']
    except (FileNotFoundError, ProcessLookupError):
        return False

def controller(spec_path):
    if os.geteuid() != 0:
        raise ValueError('trusted external controller needs actual root')
    sealed(Path(__file__))
    sealed(ROOT / 'candidate-admission-v5.py')
    spec = read_spec(spec_path)
    config_path = Path('/root/git/ModSecurity-conector/.codex/config.toml')
    configured_limits = tomllib.loads(config_path.read_text())['shell_environment_policy']['set']
    min_free_runtime = int(configured_limits['CODEX_STORAGE_MIN_FREE_RUNTIME_GIB']) * 1024**3
    # Config owns global storage thresholds; spec owns task-local memory/PID
    # limits. No global threshold is duplicated as a magic constant here.
    normal_budget = int(configured_limits['CODEX_STORAGE_NORMAL_BUDGET_GIB']) * 1024**3
    hard_budget = int(configured_limits['CODEX_STORAGE_HARD_LIMIT_GIB']) * 1024**3
    budget_receipt_path = RUN / '.codex-storage-budget.json'
    trusted(budget_receipt_path)
    budget_receipt = json.loads(budget_receipt_path.read_text())
    if budget_receipt['status'] != 'registered' or budget_receipt['run_root'] != str(RUN):
        raise ValueError('missing native registered task storage budget')
    for key, value in [('hard_limit_gib', hard_budget), ('normal_budget_gib', normal_budget), ('min_free_runtime_gib', min_free_runtime)]:
        if budget_receipt['thresholds_gib'][key] * 1024**3 != value:
            raise ValueError('native cached budget/config threshold mismatch')
    receipt_age = time.time() - datetime.datetime.fromisoformat(budget_receipt['registered_at_utc'].replace('Z', '+00:00')).timestamp()
    requested_limits = spec['resource_limits']
    memory_limit = requested_limits['memory_bytes']
    process_limit = requested_limits['processes']
    output_limit = requested_limits['output_bytes']
    if any(type(value) is not int or value <= 0 for value in (memory_limit, process_limit, output_limit)) or output_limit > normal_budget:
        raise ValueError('invalid explicit task resource limits')
    memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    if memory_limit > int(memory['MemAvailable'].split()[0]) * 1024 // 2:
        raise ValueError('task memory limit exceeds half actual available memory')
    fs = os.statvfs(ROOT)
    if fs.f_bavail * fs.f_frsize < min_free_runtime + output_limit or output_limit > budget_receipt['estimate_gib'] * 1024**3:
        raise ValueError('configured storage preflight refused task budget')
    source_hashes = {str(path): digest(path) for path in (Path(__file__), ROOT / 'candidate-admission-v5.py', spec_path, config_path, budget_receipt_path)}
    for p in (RTK, *SYSTEM.values(), '/usr/local/bin/python3'):
        trusted(Path(p).resolve())
    stamp = str(time.time_ns())
    attempt = ROOT / ('attempt-' + stamp)
    attempt.mkdir(mode=0o700)
    data = attempt / 'data'
    data.mkdir(mode=0o700)
    os.chown(data, 65534 if spec['mode'] == 'nonroot' else 0, 65534 if spec['mode'] == 'nonroot' else 0)
    (attempt / 'jail').mkdir(mode=0o700)
    originals = attempt / 'executed-input-originals'
    originals.mkdir(mode=0o700)
    for index, path in enumerate([Path(__file__), ROOT / 'candidate-admission-v5.py', spec_path, config_path, budget_receipt_path, *(Path(binding['ledger']) for binding in spec['bindings'])]):
        copy = originals / (str(index) + '-' + path.name)
        copy.write_bytes(path.read_bytes())
        copy.chmod(0o444)
    # Small explicit harmless probe inputs are also retained verbatim. Product
    # snapshots stay immutable at their approved retained binding locations.
    for binding in spec['bindings']:
        if binding['source'] == str(ROOT / 'probe-input'):
            copy = originals / 'probe.py'
            copy.write_bytes((Path(binding['source']) / 'probe.py').read_bytes())
            copy.chmod(0o444)
    namespaces = {n: os.readlink('/proc/self/ns/' + n) for n in ('user', 'mnt', 'net', 'pid', 'ipc', 'uts')}
    (attempt / 'outside-namespaces.json').write_text(json.dumps(namespaces) + '\n')
    reader, writer = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    writer.set_inheritable(True)
    args = [RTK, 'proxy', SYSTEM['unshare'], '--user', '--map-user=0', '--map-users=65534:65534:1', '--map-group=0', '--map-groups=65534:65534:1', '--setgroups=allow', '--keep-caps', '--mount', '--propagation', 'private', '--net', '--pid', '--fork', '--kill-child', '--ipc', '--uts', '/usr/local/bin/python3', '-I', str(Path(__file__)), '--bootstrap', str(spec_path), str(attempt), str(writer.fileno())]
    start = time.monotonic()
    timeout = False
    resource_violation = None
    errors = []
    admitted = None
    boot = None
    rc = None
    peak_bytes = peak_memory = peak_processes = 0
    survivors = []
    outside_mount_leaks = []
    ownership = []
    child = None
    def limits():
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_FSIZE, (output_limit, output_limit))
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
        resource.setrlimit(resource.RLIMIT_NPROC, (process_limit, process_limit))
        resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
    old_term = signal.getsignal(signal.SIGTERM)
    def interrupted(signum, frame):
        raise InterruptedError('external controller termination signal ' + str(signum))
    signal.signal(signal.SIGTERM, interrupted)
    with (attempt / 'stdout.log').open('xb') as stdout, (attempt / 'stderr.log').open('xb') as stderr:
        try:
            child = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, close_fds=True, pass_fds=(writer.fileno(),), preexec_fn=limits, start_new_session=True, env={'PATH': '/usr/bin:/usr/sbin:/bin', 'HOME': str(ROOT), 'XDG_DATA_HOME': str(ROOT / 'rtk-data')})
            writer.close()
            deadline = start + spec.get('setup_timeout_seconds', 90)
            checked_at = start
            channel_live = True
            while child.poll() is None:
                if channel_live and select.select([reader], [], [], 0.05)[0]:
                    packet = reader.recv(1024 * 1024)
                    if not packet:
                        channel_live = False
                    else:
                        if admitted is not None:
                            raise ValueError('duplicate admission packet')
                        admitted = json.loads(packet)
                        with (attempt / 'admission.original.json').open('xb') as original:
                            original.write(packet)
                        deadline = time.monotonic() + spec['timeout_seconds']
                elif not channel_live:
                    time.sleep(0.05)
                boot_path = attempt / 'bootstrap-observation.json'
                if boot is None and boot_path.is_file():
                    boot = json.loads(boot_path.read_text())
                    if not matching_init(boot) or any(boot['namespaces'][key] == namespaces[key] for key in namespaces):
                        raise ValueError('actual init identity or isolation mismatch')
                if time.monotonic() - checked_at >= 0.5:
                    checked_at = time.monotonic()
                    fs = os.statvfs(ROOT)
                    current_bytes = regular_bytes(data) + stdout.tell() + stderr.tell()
                    processes = namespace_processes(boot['namespaces']['pid'] if boot else None)
                    current_memory = sum(p['rss_bytes'] for p in processes)
                    current_processes = sum(p['threads'] for p in processes)
                    peak_bytes, peak_memory, peak_processes = max(peak_bytes, current_bytes), max(peak_memory, current_memory), max(peak_processes, current_processes)
                    if fs.f_bavail * fs.f_frsize < min_free_runtime or current_bytes > output_limit or current_memory > memory_limit or current_processes > process_limit:
                        resource_violation = 'measured aggregate memory/process/task-output/configured-global-storage budget'
                        break
                if time.monotonic() >= deadline:
                    timeout = True
                    break
            if admitted is None and select.select([reader], [], [], 0)[0]:
                packet = reader.recv(1024 * 1024)
                if packet:
                    admitted = json.loads(packet)
                    with (attempt / 'admission.original.json').open('xb') as original:
                        original.write(packet)
        except BaseException as error:
            errors.append(type(error).__name__ + ': ' + str(error)[:500])
        finally:
            # Do not let a repeated external termination interrupt the short
            # bounded reap phase after its first signal was recorded.
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            # Producer/monitor errors and early RTK exit cannot skip cleanup.
            writer.close()
            reader.close()
            try:
                boot_path = attempt / 'bootstrap-observation.json'
                if boot is None and boot_path.is_file():
                    boot = json.loads(boot_path.read_text())
                if matching_init(boot):
                    os.kill(boot['host_pid'], signal.SIGKILL)
            except BaseException as error:
                errors.append('init cleanup: ' + type(error).__name__ + ': ' + str(error)[:300])
            if child is not None:
                if child.poll() is None:
                    try:
                        os.killpg(child.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                try:
                    rc = child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    try:
                        rc = child.wait(timeout=5)
                    except BaseException as error:
                        errors.append('wrapper cleanup: ' + type(error).__name__)
            try:
                for _ in range(100):
                    survivors = namespace_processes(boot['namespaces']['pid'] if boot else None)
                    if not survivors:
                        break
                    time.sleep(0.05)
                outside_mount_leaks = [line for line in Path('/proc/self/mountinfo').read_text().splitlines() if str(attempt / 'jail') in line]
                # Record original retained UID/GID/modes before task-only
                # handoff; use lstat and no-follow chown, never foreign paths.
                if not survivors and not outside_mount_leaks:
                    for parent, dirs, files in os.walk(data, followlinks=False):
                        for p in [Path(parent), *(Path(parent) / name for name in files)]:
                            d = p.lstat()
                            ownership.append({'path': str(p.relative_to(data)), 'uid': d.st_uid, 'gid': d.st_gid, 'mode': oct(stat.S_IMODE(d.st_mode)), 'kind': stat.S_IFMT(d.st_mode)})
                            os.chown(p, 0, 0, follow_symlinks=False)
                (attempt / 'retained-original-ownership.json').write_text(json.dumps(ownership, indent=2) + '\n')
            except BaseException as error:
                errors.append('postcleanup measurement/handoff: ' + type(error).__name__ + ': ' + str(error)[:300])
    signal.signal(signal.SIGTERM, old_term)
    source_hashes_after = {}
    for path in (Path(__file__), ROOT / 'candidate-admission-v5.py', spec_path, config_path, budget_receipt_path):
        try:
            source_hashes_after[str(path)] = digest(path)
        except OSError as error:
            errors.append('final source identity: ' + type(error).__name__)
    if admitted is None:
        errors.append('missing immutable outside admission')
    elif not isinstance(admitted, dict) or boot is None or admitted.get('namespaces') != boot['namespaces'] or admitted.get('argv') != spec['argv']:
        errors.append('original admission/init/approved argv mismatch')
    if source_hashes != source_hashes_after:
        errors.append('executed source/spec/config changed during attempt')
    accepted = rc == 0 and not (timeout or resource_violation or errors or survivors or outside_mount_leaks)
    controller_rc = 0 if accepted else 77
    result = {'spec_sha256': source_hashes[str(spec_path)], 'controller_sha256': source_hashes[str(Path(__file__))], 'executed_input_hashes_before': source_hashes, 'executed_input_hashes_after': source_hashes_after, 'argv': args, 'cwd': str(ROOT), 'exitcode': rc, 'controller_exitcode': controller_rc, 'signal': -rc if rc is not None and rc < 0 else None, 'timeout': timeout, 'errors': errors, 'resource_violation': resource_violation, 'configured_storage_limits': {'config_sha256': source_hashes[str(config_path)], 'minimum_free_bytes': min_free_runtime, 'normal_budget_bytes': normal_budget, 'hard_budget_bytes': hard_budget, 'native_cached_registration_sha256': source_hashes[str(budget_receipt_path)], 'native_cached_registration_age_seconds': receipt_age, 'native_cached_estimate_bytes': budget_receipt['estimate_gib'] * 1024**3, 'fresh_global_accounting': False}, 'task_resource_limits': requested_limits, 'peak_task_output_bytes': peak_bytes, 'peak_aggregate_rss_bytes': peak_memory, 'peak_aggregate_process_threads': peak_processes, 'duration_seconds': time.monotonic() - start, 'supervisor_reaped': child is not None and child.returncode is not None, 'outside_namespaces': namespaces, 'data': str(data), 'admission_sha256': digest(attempt / 'admission.original.json') if admitted is not None else None, 'surviving_namespace_pids': survivors, 'outside_mount_leaks': outside_mount_leaks, 'admission_is_not_host_pass': True}
    (attempt / 'controller-result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'attempt': str(attempt), 'exitcode': rc, 'timeout': timeout}))
    return controller_rc

def bootstrap(spec_path, attempt, admission_fd):
    # No candidate code is imported before capability drop.
    spec = read_spec(spec_path)
    host_pid = int(Path('/proc/self/stat').read_text().split(' ', 1)[0])
    start_time = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19]
    boot = {'host_pid': host_pid, 'start_time': start_time, 'namespaces': {key: os.readlink('/proc/self/ns/' + key) for key in ('user', 'mnt', 'net', 'pid', 'ipc', 'uts')}}
    (attempt / 'bootstrap-observation.json').write_text(json.dumps(boot) + '\n')
    jail = attempt / 'jail'
    run([SYSTEM['mount'], '-t', 'tmpfs', '-o', 'mode=0755,nosuid,nodev,size=128m', 'tmpfs', str(jail)])
    def target(path, directory=True):
        p = jail / path.lstrip('/')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.mkdir(exist_ok=True) if directory else p.touch(exist_ok=True)
        return p
    def bind(source, destination, directory=True, readonly=True):
        p = target(destination, directory)
        run([SYSTEM['mount'], '--bind', str(source), str(p)])
        flags = 'remount,bind,nosuid,nodev' + (',ro' if readonly else '')
        run([SYSTEM['mount'], '-o', flags, str(p)])
    # System executable/library code only; no broad /usr/local config/tool data.
    for name in ('bin', 'sbin', 'lib', 'lib64', 'share', 'include'):
        source = Path('/usr') / name
        if source.is_dir():
            bind(source, '/usr/' + name)
    # Existing pinned compiler subprocesses and Go; no host configuration/data.
    bind('/usr/libexec/gcc/x86_64-linux-gnu/15', '/usr/libexec/gcc/x86_64-linux-gnu/15')
    bind('/usr/local/go', '/usr/local/go')
    bind('/usr/local/bin/python3.14', '/usr/local/bin/python3.14', False)
    target('/usr/local/bin')
    (jail / 'usr/local/bin/python3').symlink_to('python3.14')
    (jail / 'usr/local/bin/python').symlink_to('python3.14')
    bind('/usr/local/lib/python3.14', '/usr/local/lib/python3.14')
    for name in ('bin', 'sbin', 'lib', 'lib64'):
        source = Path('/') / name
        if source.exists():
            if source.is_symlink():
                (jail / name).symlink_to(os.readlink(source))
            else:
                bind(source, '/' + name)
    for name in ('etc', 'proc', 'dev', 'mnt', 'run', 'root', 'home', 'sys', 'var/tmp', 'tmp', 'opt/controller'):
        target('/' + name)
    (jail / 'etc/passwd').write_text('root:x:0:0:root:/task:/usr/bin/false\nnobody:x:65534:65534:nobody:/task:/usr/bin/false\n')
    # Private locked fixture accounts, never a host credential store. PAM keeps
    # root authentication, Unix account checks and existing resource limits.
    shadow = jail / 'etc/shadow'
    shadow.write_text('root:!:20700:0:99999:7:::\nnobody:!:20700:0:99999:7:::\n')
    shadow.chmod(0o600)
    target('/etc/pam.d')
    target('/etc/security')
    (jail / 'etc/security/limits.conf').write_text('# Explicit inherited task limits remain unchanged.\n')
    (jail / 'etc/pam.d/runuser').write_text('auth required pam_rootok.so\naccount required pam_unix.so\nsession required pam_limits.so\nsession required pam_unix.so\n')
    (jail / 'etc/group').write_text('root:x:0:\nnogroup:x:65534:\n')
    (jail / 'etc/nsswitch.conf').write_text('passwd: files\ngroup: files\nhosts: files\n')
    (jail / 'etc/hosts').write_text('127.0.0.1 localhost\n::1 localhost\n')
    (jail / 'etc/gitconfig').write_text('[safe]\n\tdirectory = /mnt/src\n\tdirectory = /mnt/framework\n\tdirectory = /mnt/src/modules/ModSecurity-test-Framework\n')
    target('/etc/alternatives')
    # Minimal trusted compiler aliases, not the host alternatives/config tree.
    trusted(Path('/usr/bin/gawk'))
    for name, executable in [('cc', '/usr/bin/gcc'), ('c++', '/usr/bin/g++'), ('awk', '/usr/bin/gawk')]:
        if Path(executable).exists():
            (jail / 'etc/alternatives' / name).symlink_to(executable)
    for name in ('mime.types', 'ld.so.cache'):
        p = Path('/etc') / name
        if p.is_file():
            trusted(p)
            bind(p, '/etc/' + name, False)
    # No host device tree, sysfs, /run, HOME, machine identity, resolv.conf or
    # credential store is bound. Only the four ordinary null/random devices.
    for name in ('null', 'zero', 'random', 'urandom', 'full'):
        p = target('/dev/' + name, False)
        run([SYSTEM['mount'], '--bind', '/dev/' + name, str(p)])
        run([SYSTEM['mount'], '-o', 'remount,bind,nosuid,noexec', str(p)])
    bind(RTK, '/opt/controller/rtk', False)
    bind(ROOT / 'candidate-admission-v5.py', '/opt/controller/candidate-admission.py', False)
    readonly = ['/usr/bin', '/usr/sbin', '/usr/lib', '/usr/libexec/gcc/x86_64-linux-gnu/15', '/usr/local/go', '/usr/share', '/usr/include', '/usr/local/bin/python3.14', '/usr/local/lib/python3.14', '/opt/controller/rtk', '/opt/controller/candidate-admission.py']
    for binding in spec['bindings']:
        bind(binding['source'], binding['target'])
        readonly.append(binding['target'])
    if any(b['target'] == '/mnt/src' for b in spec['bindings']) and any(b['target'] == '/mnt/framework' for b in spec['bindings']):
        alias = '/mnt/src/modules/ModSecurity-test-Framework'
        if not (jail / alias.lstrip('/')).is_dir():
            raise ValueError('Framework alias target missing from source snapshot')
        run([SYSTEM['mount'], '--bind', str(jail / 'mnt/framework'), str(jail / alias.lstrip('/'))])
        run([SYSTEM['mount'], '-o', 'remount,bind,ro,nosuid,nodev', str(jail / alias.lstrip('/'))])
        readonly.append(alias)
    git_aliases = [('/mnt/git', '/mnt/src'), ('/mnt/git-framework', '/mnt/framework')]
    if any(b['target'] == '/mnt/src' for b in spec['bindings']) and any(b['target'] == '/mnt/framework' for b in spec['bindings']):
        git_aliases.append(('/mnt/git-framework', '/mnt/src/modules/ModSecurity-test-Framework'))
    for git_path, source_path in git_aliases:
        if any(b['target'] == git_path for b in spec['bindings']):
            alias = source_path + '/.git'
            if not (jail / alias.lstrip('/')).is_dir():
                raise ValueError('sealed Git alias placeholder is missing')
            run([SYSTEM['mount'], '--bind', str(jail / git_path.lstrip('/')), str(jail / alias.lstrip('/'))])
            run([SYSTEM['mount'], '-o', 'remount,bind,ro,nosuid,nodev', str(jail / alias.lstrip('/'))])
            readonly.append(alias)
    bind(attempt / 'data', '/task', readonly=False)
    bind(attempt / 'data', '/var/tmp/codex/ModSecurity-conector', readonly=False)
    bind(attempt / 'data', '/var/tmp/ModSecurity-conector-verified', readonly=False)
    if spec.get('nginx_worker_alias'):
        # Host attempt/data stay 0700; only this private namespace alias permits
        # worker traversal. All case/config/evidence leaves retain their modes.
        worker_tree = attempt / 'data' / 'nginx-worker-runtime'
        worker_tree.mkdir(mode=0o711)
        bind(worker_tree, '/var/tmp/codex/ModSecurity-nginx-i12', readonly=False)
    admission = {'nginx_worker_alias': bool(spec.get('nginx_worker_alias')), 'mode': spec['mode'], 'readonly': readonly, 'outside_namespaces': json.loads((attempt / 'outside-namespaces.json').read_text())}
    (jail / 'opt/controller/admission.json').write_text(json.dumps(admission) + '\n')
    (jail / 'opt/controller/admission.json').chmod(0o444)
    # Private tmpfs is safe transient data, never a host /tmp view.
    run([SYSTEM['mount'], '-t', 'tmpfs', '-o', 'mode=1777,nosuid,nodev,noexec,size=128m', 'tmpfs', str(jail / 'tmp')])
    run([SYSTEM['mount'], '-t', 'proc', '-o', 'ro,nosuid,nodev,noexec', 'proc', str(jail / 'proc')])
    run([SYSTEM['ip'], 'link', 'set', 'lo', 'up'])
    run([SYSTEM['mount'], '-o', 'remount,ro,nosuid,nodev', str(jail)])
    # No open directory descriptor, cwd or privileged in-jail parent survives.
    os.chdir(jail)
    os.chroot('.')
    os.chdir('/task')
    env = {'PATH': '/opt/controller:/usr/local/bin:/usr/bin:/usr/sbin:/bin', 'HOME': '/task', 'TMPDIR': '/task', 'XDG_CACHE_HOME': '/task/cache', 'XDG_DATA_HOME': '/task/rtk-data', 'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C', 'TZ': 'UTC', **spec.get('environment', {})}
    # Pass exact approved argv without shell expansion; config never travels in
    # inherited environment. The admission process verifies actual cap masks.
    env['I12_APPROVED_MODE'] = spec['mode']
    if spec['mode'] == 'nonroot':
        identity = ['--reuid=65534', '--regid=65534', '--clear-groups', '--bounding-set=-all']
    elif spec['mode'] == 'nginx-root-master':
        identity = ['--reuid=0', '--regid=0', '--clear-groups', '--bounding-set=-all,+chown,+setuid,+setgid']
    else:
        # Exact additional DAC_OVERRIDE permits native master log opening;
        # no FOWNER, SYSADMIN, SYSCHROOT, PTRACE, networking or ambient powers.
        if spec['mode'] == 'nginx-root-master-dac':
            identity = ['--reuid=0', '--regid=0', '--clear-groups', '--bounding-set=-all,+chown,+dac_override,+setuid,+setgid']
        else:
            # Required only to inspect/signal own nonroot workers in this private PID namespace.
            identity = ['--reuid=0', '--regid=0', '--clear-groups', '--bounding-set=-all,+chown,+dac_override,+kill,+setuid,+setgid']
    # setpriv replaces PID1 before candidate RTK exists. There must be no
    # privileged RTK parent left reachable in the candidate PID namespace.
    args = [SYSTEM['setpriv'], *identity, '--inh-caps=-all', '--ambient-caps=-all', '--no-new-privs', '/usr/local/bin/python3', '-I', '/opt/controller/candidate-admission.py', str(admission_fd), *spec['argv']]
    os.execve(args[0], args, env)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 5 and sys.argv[1] == '--bootstrap':
            bootstrap(Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]))
        elif len(sys.argv) == 2:
            sys.exit(controller(Path(sys.argv[1])))
        else:
            raise ValueError('usage: private-runtime.py ROOT_REVIEWED_SEALED_SPEC.json')
    except Exception as error:
        print('ISOLATION_BLOCKED: ' + type(error).__name__ + ': ' + str(error), file=sys.stderr)
        sys.exit(77)
