"""Parse effective host YAML before starting the real host; no qualification."""
import json
from pathlib import Path
import sys
import re



RUN_ID = 'traefik-acceptance-20261015'
RESERVATION = 'X-Msconnector-Trusted-Reservation'
HANDLE = 'X-Msconnector-Response-Handle'
PROVENANCE_SOCKET_CONTRACT = {'socket_mode': 0o600, 'parent_mode': 0o700,
    'socket_uid': 65534, 'socket_gid': 65534, 'parent_uid': 65534, 'parent_gid': 65534,
    'parent_lstat_directory_required': True, 'parent_symlink_forbidden': True}
HOST_BOUNDARY_CASES = frozenset(('NEED-complete-sample', 'NEED-incomplete-sample',
    'NEED-host-request-buffer-bound', 'NEED-host-auth-response-32768-bound',
    'NEED-32768-auth-response-not-application-response', 'NEED-request-above-former-connector-limit'))


def provenance_mode(case):
    # Built-in ForwardAuth rejection must be measured without an outer writer
    # requiring service attestation. Otherwise a host401 can become observer503.
    # Handle lookup/expiry controls likewise retain ordinary MRC1 semantics.
    physical = case['fixture'].get('physical_file_supplement', {})
    return (case['case_id'] not in HOST_BOUNDARY_CASES and
            not physical.get('host_capacity_control', False) and
            not bool(case['fixture'].get('relay', {}).get('handle')))


def validate(path, case=None):
    import yaml
    config = yaml.safe_load(path.read_text())['http']
    middlewares = config['middlewares']
    auth = middlewares['modsecurity-forwardauth']['forwardAuth']
    required = {'preserveRequestMethod': True, 'trustForwardHeader': False,
                'forwardBody': True, 'maxBodySize': 4096,
                'maxResponseBodySize': 32768}
    for key, value in required.items():
        if type(auth.get(key)) is not type(value) or auth[key] != value:
            raise ValueError('effective host contract differs: ' + key)
    routers = config['routers']
    physical = case['fixture'].get('physical_file_supplement') if case else None
    if physical and physical.get('direction') == 'response':
        key = case['probe_id']
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', key):
            raise ValueError('literal physical file target key required')
        target = routers.get('physical-file-target', {})
        expected_rule = 'Header(`X-I12-Probe`, `' + key + '`) && !Header(`X-I12-Neighbor`, `1`)'
        if (target.get('rule') != expected_rule or target.get('priority') != 200 or
                target.get('entryPoints') != ['web'] or target.get('service') != 'physical-file-backend' or
                target.get('middlewares') != routers['smoke']['middlewares']):
            raise ValueError('exclusive physical file target router required')
        servers = config['services'].get('physical-file-backend', {}).get('loadBalancer', {}).get('servers', [])
        if len(servers) != 1 or not re.fullmatch(r'http://127\.0\.0\.1:[0-9]{1,5}', servers[0].get('url', '')):
            raise ValueError('one literal loopback physical file backend required')
        file_port = int(servers[0]['url'].rsplit(':', 1)[1])
        if not 1 <= file_port <= 65535 or servers == config['services']['upstream']['loadBalancer']['servers']:
            raise ValueError('separate bounded physical file backend port required')
    elif 'physical-file-target' in routers or 'physical-file-backend' in config['services']:
        raise ValueError('file target router requires an explicit response-file binding')
    mode = provenance_mode(case) if case is not None else any(
        'provenanceSocketPath' in value.get('plugin', {}).get('modsecurityResponseObserver', {})
        for value in middlewares.values())
    for name, observer in [('smoke', 'modsecurity-response-observer'),
                           ('healthy-neighbor', 'healthy-response-observer')]:
        expected = [observer, 'modsecurity-forwardauth', observer + '-confirm'] if mode else ['modsecurity-forwardauth', observer]
        if routers[name]['middlewares'] != expected:
            raise ValueError('ordered host middleware contract differs: ' + name)
        outer = middlewares[observer]['plugin']['modsecurityResponseObserver']
        socket_root = path.parent.parent.parent / 'sockets'
        companion = socket_root / ('observer.sock' if name == 'smoke' and case and case['fixture'].get('relay', {}).get('companion_fault') else 'companion.sock')
        if outer.get('socketPath') != str(companion):
            raise ValueError('wrong companion socket: ' + name)
        if mode:
            expected_outer = {'socketPath': str(companion), 'provenanceSocketPath': str(socket_root / 'provenance.sock'),
                              'runID': RUN_ID, 'transportCaseID': case['id'] if case else outer.get('transportCaseID'),
                              'timeoutMillis': 1000 if name == 'smoke' and case and case['fixture'].get('relay', {}).get('companion_fault') else 5000}
            if outer != expected_outer or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', outer['transportCaseID']):
                raise ValueError('atomic outer provenance settings differ: ' + name)
            inner = middlewares[observer + '-confirm']['plugin']['modsecurityResponseObserver']
            if inner != {'socketPath': str(companion), 'confirmProvenance': True, 'timeoutMillis': expected_outer['timeoutMillis']}:
                raise ValueError('atomic inner provenance settings differ: ' + name)
        elif any(key in outer for key in ('provenanceSocketPath', 'runID', 'transportCaseID', 'confirmProvenance')):
            raise ValueError('default MRC1 control must not enable provenance')
    request_names = [name.lower() for name in auth['authRequestHeaders']]
    if HANDLE.lower() in request_names:
        raise ValueError('response handle forbidden in authorization request headers')
    if request_names.count(RESERVATION.lower()) != int(mode):
        raise ValueError('reservation forwarding contract differs')
    if auth['authResponseHeaders'] != [HANDLE]:
        raise ValueError('response handle forwarding contract differs')
    return {'parsed_by': yaml.__file__, 'yaml_version': yaml.__version__,
            'effective_auth_contract': required, 'routers': list(routers),
            'observer_mode': 'trusted-provenance' if mode else 'default-mrc1',
            'qualification': None}


if __name__ == '__main__':
    print(json.dumps(validate(Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 else None)))
