#!/usr/local/bin/python3
"""Actual post-drop measurements, followed by approved candidate exec."""
import json
import os
import socket
from pathlib import Path
import sys

fields = {}
for line in Path('/proc/self/status').read_text().splitlines():
    key, separator, value = line.partition(':')
    if separator and key in ('Uid', 'Gid', 'Groups', 'CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb', 'NoNewPrivs'):
        fields[key] = value.strip()
admission = json.loads(Path('/opt/controller/admission.json').read_text())
mode = os.environ.pop('I12_APPROVED_MODE')
assert mode == admission['mode']
masks = {'nonroot': 0, 'nginx-root-master': 0xc1, 'nginx-root-master-dac': 0xc3, 'nginx-root-master-lifecycle': 0xe3}
allowed = masks[mode]
expected = 65534 if mode == 'nonroot' else 0
assert os.geteuid() == expected and os.getegid() == expected
assert fields['NoNewPrivs'] == '1'
assert fields['CapInh'] == fields['CapAmb'] == '0000000000000000'
if mode == 'nonroot':
    assert all(int(fields[key], 16) == 0 for key in ('CapPrm', 'CapEff', 'CapBnd'))
else:
    # Only the exact approved mask; DAC and KILL only for their separate explicit modes.
    assert all(int(fields[key], 16) == allowed for key in ('CapPrm', 'CapEff', 'CapBnd'))
assert not os.getgroups()
maps = {key: Path('/proc/self/' + key).read_text() for key in ('uid_map', 'gid_map')}
assert all([tuple(map(int, row.split())) for row in value.splitlines()] == [(0, 0, 1), (65534, 65534, 1)] for value in maps.values())
mounts = Path('/proc/self/mountinfo').read_text()
assert not any('shared:' in row or 'master:' in row for row in mounts.splitlines())
for hidden in ('/root/.ssh', '/root/.codex', '/home/.aws', '/run/secrets', '/sys/kernel'):
    assert not Path(hidden).exists()
for readonly in ['/', *admission['readonly']]:
    rows = [line.split(' - ')[0].split() for line in mounts.splitlines() if line.split(' - ')[0].split()[4] == readonly]
    assert len(rows) == 1 and 'ro' in rows[0][5].split(',')
namespaces = {key: os.readlink('/proc/self/ns/' + key) for key in admission['outside_namespaces']}
assert all(namespaces[key] != value for key, value in admission['outside_namespaces'].items())
interfaces = [line.split(':', 1)[0].strip() for line in Path('/proc/net/dev').read_text().splitlines()[2:]]
assert interfaces == ['lo']
assert not Path('/proc/net/route').read_text().splitlines()[1:]
assert os.stat('/task').st_ino == os.stat('/var/tmp/codex/ModSecurity-conector').st_ino
if admission.get('nginx_worker_alias'):
    import stat
    worker_tree = Path('/var/tmp/codex/ModSecurity-nginx-i12')
    assert os.stat(worker_tree).st_ino == os.stat('/task/nginx-worker-runtime').st_ino
    assert stat.S_IMODE(os.stat('/task').st_mode) == 0o700
    assert stat.S_IMODE(os.stat(worker_tree).st_mode) == 0o711
    assert all(os.stat(path).st_mode & stat.S_IXOTH for path in (worker_tree, *worker_tree.parents))
# Observe every visible process before candidate code is executed. No process
# may retain capabilities beyond this admitted identity's bounding set.
processes = []
for process in Path('/proc').iterdir():
    if not process.name.isdigit():
        continue
    try:
        status = dict(line.split(':', 1) for line in (process / 'status').read_text().splitlines() if ':' in line)
        assert all(int(status[key].strip(), 16) & ~allowed == 0 for key in ('CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb'))
        processes.append({'pid': int(process.name), 'uid': status['Uid'].strip(), 'caps': {key: status[key].strip() for key in ('CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb')}})
    except FileNotFoundError:
        pass
record = {'uid': os.getuid(), 'gid': os.getgid(), 'mode': mode, 'status': fields, 'maps': maps, 'namespaces': namespaces, 'mountinfo': mounts, 'processes': processes, 'interfaces': interfaces, 'cwd': os.getcwd(), 'argv': sys.argv[2:], 'admission_is_not_host_pass': True}
packet = json.dumps(record, indent=2).encode() + b'\n'
channel = socket.socket(fileno=int(sys.argv[1]))
assert channel.send(packet) == len(packet)
channel.close()
with open('/task/isolation-admission.json', 'x') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
os.chmod('/task/isolation-admission.json', 0o600)
assert len(sys.argv) > 2 and sys.argv[2].startswith('/')
os.execv('/opt/controller/rtk', ['/opt/controller/rtk', 'proxy', *sys.argv[2:]])
