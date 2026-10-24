"""Negative contracts for bounded real-host composite qualification."""
import importlib.util
from pathlib import Path
import socket
import os
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch, Mock
import unittest

MODULE = Path(__file__).resolve().parents[1] / "connectors/composite_harness/qualification.py"
spec = importlib.util.spec_from_file_location("qualification", MODULE)
qualification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualification)
upstream_spec = importlib.util.spec_from_file_location('qualification_upstream', MODULE.with_name('upstream.py'))
upstream = importlib.util.module_from_spec(upstream_spec)
upstream_spec.loader.exec_module(upstream)


class QualificationContracts(unittest.TestCase):
    @staticmethod
    def observation(count=1):
        return {'requests_seen': count, 'lease_header_observed': False,
                'parallel_requests_seen': 0, 'parallel_max_inflight': 0, 'parallel_inflight': 0,
                'parallel_barrier_passes': 0, 'parallel_barrier_errors': 0}

    def test_duplicate_terminal_rejected(self):
        events = self.allow_events()
        with self.assertRaises(ValueError):
            qualification.verify_events(events + [events[-1]], {"allow": 1})

    def test_concurrent_aggregate_does_not_join_client_ids(self):
        events = self.allow_events("a") + self.allow_events("b")
        self.assertEqual(qualification.verify_events(events, {"allow": 2})["allow"], 2)

    def test_wrong_rule_rejected(self):
        events = [{"decision_id": "a", "phase": "P1", "outcome": "deny", "rule_id": "wrong", "requested_action": "deny"},
                  {"decision_id": "a", "phase": "terminal", "cleanup_outcome": "closed", "outcome": "closed"}]
        with self.assertRaises(ValueError):
            qualification.verify_events(events, {"p1": 1})

    @staticmethod
    def allow_events(identifier="a"):
        def record(phase, **fields):
            return {'decision_id': identifier * 43, 'connector': 'envoy', 'phase': phase,
                    'outcome': qualification.EVENT_OUTCOME[phase], 'event_time': '2026-10-03T00:00:00Z',
                    'request_path': 'envoy.ext_authz', 'response_path': 'envoy.ext_proc',
                    'transport': 'envoy_ext_authz_ext_proc_grpc', **fields}
        return [record('P1', requested_action='allow'), record('P2', requested_action='allow'),
                record('lease'), record('claim'), record('P3', requested_action='allow'), record('P4', requested_action='allow'),
                record('neutral_outcome', actual_host_action='allow', visible_status=200),
                record('terminal', cleanup_outcome='closed', reason='response_end_of_stream')]

    def test_connection_close_rejected(self):
        a, b = socket.socketpair()
        try:
            b.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            with self.assertRaises(ValueError):
                qualification.read_response(a, require_keepalive=True)
        finally:
            a.close()
            b.close()

    def test_request_wire_no_client_lease(self):
        wire = qualification.request_wire("p1", 1234)
        self.assertIn(b"msconnector-p1-only", wire)
        self.assertNotIn(b"Connection: close", wire)
        self.assertNotIn(b"Composite-Lease", wire)

    def test_caps_are_fixed(self):
        self.assertEqual(qualification.CLIENTS, 4)
        self.assertEqual(qualification.PARALLEL_REQUESTS_PER_CLIENT, 4)
        self.assertEqual(qualification.FRESH_STARTS, 3)

    def test_missing_actual_allow_action_rejected(self):
        events = [e for e in self.allow_events() if e['phase'] != 'neutral_outcome']
        with self.assertRaises(ValueError):
            qualification.verify_events(events, {'allow': 1})

    def test_duplicate_claim_rejected(self):
        events = self.allow_events()
        events.append(next(e for e in events if e['phase'] == 'claim'))
        with self.assertRaises(ValueError):
            qualification.verify_events(events, {'allow': 1})

    def test_timeout_requires_admission_then_terminal(self):
        events = self.allow_events()
        events = [e for e in events if e['phase'] in {'P1', 'P2', 'lease', 'terminal'}]
        events[-1]['reason'] = 'timeout'
        self.assertEqual(qualification.verify_events(events, {'timeout': 1}), {'timeout': 1})
        events.insert(2, {'decision_id': 'a', 'phase': 'P3', 'requested_action': 'allow'})
        with self.assertRaises(ValueError):
            qualification.verify_events(events, {'timeout': 1})

    def test_wrong_profile_metadata_rejected(self):
        events = self.allow_events()
        events[0]['connector'] = 'traefik'
        with self.assertRaises(ValueError):
            qualification.verify_events(events, {'allow': 1}, 'envoy')

    def test_receipt_symlink_hardlink_and_permissions_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = root / 'receipt.json'
            receipt.write_text(qualification.json.dumps(self.observation()))
            receipt.chmod(0o600)
            self.assertEqual(qualification.backend_count(receipt), 1)
            alias = root / 'alias'
            alias.symlink_to(receipt)
            with self.assertRaises(OSError):
                qualification.backend_count(alias)
            alias.unlink()
            os.link(receipt, alias)
            with self.assertRaises(ValueError):
                qualification.backend_count(receipt)
            alias.unlink()
            receipt.chmod(0o644)
            with self.assertRaises(ValueError):
                qualification.backend_count(receipt)

    def test_backend_bool_count_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt.json'
            receipt.write_text(qualification.json.dumps(self.observation(True)))
            receipt.chmod(0o600)
            with self.assertRaises(ValueError):
                qualification.backend_count(receipt)

    def test_root_not_empty_rejected(self):
        with tempfile.TemporaryDirectory(dir=qualification.STORAGE_ROOT) as directory:
            root = Path(directory)
            qualification.validate_runtime_root(root)
            (root / 'foreign').touch()
            with self.assertRaises(ValueError):
                qualification.validate_runtime_root(root)

    def test_source_root_isolation(self):
        # Reject before traversing or creating artifacts in the source tree.
        with self.assertRaises(ValueError):
            qualification.validate_runtime_root(qualification.REPO)

    def test_profile_templates_render_completely(self):
        for profile in ('envoy', 'traefik'):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                args = SimpleNamespace(composite_bin=Path('/operator/composite'), host_bin=Path('/operator/host'),
                                       runtime_config=Path('/operator/runtime.conf'), cert=Path('/operator/cert.pem'), key=Path('/operator/key.pem'))
                service, host, events, uds = qualification.render(profile, args, root, [12000, 12001, 12002, 12003])
                self.assertIn(profile, service)
                self.assertTrue(host)
                self.assertEqual(events.parent, root)
                for config in root.glob('*.yaml'):
                    self.assertNotRegex(config.read_text(), r'@[A-Z_]+@|__[A-Z_]+__')
                    self.assertEqual(config.stat().st_mode & 0o777, 0o600)
                self.assertEqual(uds is not None, profile == 'traefik')

    def test_entrypoints_import_shared_runner(self):
        for profile in ('envoy', 'traefik'):
            path = qualification.REPO / f'connectors/{profile}/harness/run_{profile}_composite_qualification.py'
            text = path.read_text()
            self.assertIn('from qualification import main', text)
            self.assertIn(f"main('{profile}')", text)

    def test_oversized_chunked_response_rejected(self):
        a, b = socket.socketpair()
        try:
            b.sendall(b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n10001\r\n')
            with self.assertRaises(ValueError):
                qualification.read_response(a, True)
        finally:
            a.close()
            b.close()

    def test_fifo_receipt_rejected_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt'
            os.mkfifo(receipt, 0o600)
            with self.assertRaises(ValueError):
                qualification.backend_count(receipt)

    def test_absolute_request_deadline(self):
        a, b = socket.socketpair()
        try:
            with self.assertRaises(TimeoutError):
                qualification.read_response(a, True, deadline=qualification.time.monotonic() - 1)
        finally:
            a.close()
            b.close()

    def test_main_runs_three_distinct_generations(self):
        with tempfile.TemporaryDirectory(dir=qualification.STORAGE_ROOT) as directory:
            root = Path(directory)
            campaign = root / 'campaign'
            campaign.mkdir(mode=0o700)
            inputs = []
            for name in ('host', 'composite', 'runtime', 'cert', 'key', 'rules'):
                path = root / name
                path.write_text('operator input')
                path.chmod(0o700 if name in {'host', 'composite'} else 0o600)
                inputs.append(path)
            inputs[-1].write_bytes((qualification.REPO / 'common/rules/modsecurity_p1_p4_vectors.conf').read_bytes())
            inputs[2].write_text('rules_file=' + str(inputs[-1]) + '\n')
            def fake_start(profile, args, start_root, deadline):
                index = int(start_root.name.rsplit('-', 1)[1])
                return {'passed': True, 'cleanup': {'passed': True}, 'gates': dict.fromkeys(('G2', 'G5', 'G6'), 'passed'),
                        'processes': {label: {'pid': 100 + index, 'start_token': str(index)} for label in ('host', 'service', 'upstream')}}
            arguments = ['--root', str(campaign)]
            for name, path in zip(('host-bin', 'composite-bin', 'runtime-config', 'cert', 'key', 'rules-file'), inputs):
                arguments.extend(['--' + name, str(path)])
            arguments.extend(['--rules-sha256', qualification.digest(inputs[-1]), '--library-sha256', 'a' * 64])
            with patch.object(qualification, 'run_start', side_effect=fake_start) as run, patch.object(qualification, 'source_manifest', return_value={}):
                self.assertEqual(qualification.main('envoy', arguments), 0)
                self.assertEqual(run.call_count, 3)
            result = qualification.json.loads((campaign / 'qualification-result.json').read_text())
            self.assertFalse(result['catalog_acceptance'])
            self.assertEqual(result['gates'], {'G2': 'passed', 'G5': 'passed', 'G6': 'passed'})

    def test_closed_event_state_machine_rejects_reordering_payload_and_types(self):
        for mutation in ('late_claim', 'early_terminal', 'payload', 'bool_status', 'bad_time', 'too_long', 'missing_time'):
            with self.subTest(mutation=mutation):
                events = self.allow_events()
                if mutation == 'late_claim':
                    events[3], events[4] = events[4], events[3]
                elif mutation == 'early_terminal':
                    events[3], events[-1] = events[-1], events[3]
                elif mutation == 'payload':
                    events[0]['request_body'] = 'forbidden'
                elif mutation == 'bool_status':
                    events[-2]['visible_status'] = True
                elif mutation == 'bad_time':
                    events[0]['event_time'] = '2026-02-30T00:00:00Z'
                elif mutation == 'too_long':
                    events[0]['rule_id'] = 'x' * 129
                else:
                    del events[0]['event_time']
                with self.assertRaises(ValueError):
                    qualification.verify_events(events, {'allow': 1})

    def test_p1_denial_cannot_issue_lease_or_claim(self):
        allow = self.allow_events()
        p1 = {**allow[0], 'requested_action': 'deny', 'rule_id': '1101001', 'visible_status': 403}
        action = {**allow[-2], 'phase': 'request_host_action', 'outcome': 'recorded',
                  'requested_action': 'block', 'actual_host_action': 'deny', 'visible_status': 403}
        terminal = {**allow[-1], 'reason': 'request_block'}
        good = [p1, action, terminal]
        self.assertEqual(qualification.verify_events(good, {'p1': 1}), {'p1': 1})
        for forbidden in (allow[2], allow[3], allow[4], allow[5], allow[6]):
            with self.subTest(phase=forbidden['phase']), self.assertRaises(ValueError):
                qualification.verify_events([p1, forbidden, action, terminal], {'p1': 1})

    def test_cleanup_stop_error_overrides_saved_pass(self):
        self.cleanup_failure_fixture(stop_error=True, survivor=False)

    def test_cleanup_descendant_survivor_overrides_saved_pass(self):
        self.cleanup_failure_fixture(stop_error=False, survivor=True)

    def cleanup_failure_fixture(self, stop_error, survivor):
        with tempfile.TemporaryDirectory(dir=qualification.STORAGE_ROOT) as directory:
            root = Path(directory)
            child = SimpleNamespace(label='service', token='original', descendants={2: {'pid': 2, 'start_token': 'owned'}},
                                    process=SimpleNamespace(pid=1, poll=lambda: 0),
                                    stop=Mock(side_effect=ValueError('simulated stop failure') if stop_error else None))
            result = {'passed': True, 'catalog_acceptance': False, 'gates': dict.fromkeys(('G2', 'G5', 'G6'), 'passed')}
            with patch.object(qualification, 'start_token', side_effect=FileNotFoundError), patch.object(qualification, 'surviving_descendants', return_value=[{'pid': 2}] if survivor else []), patch.object(qualification.socket, 'create_connection', side_effect=ConnectionRefusedError):
                with self.assertRaises(ValueError):
                    qualification.finalize_cleanup(root, result, [child], [1234], None, None)
            saved = qualification.json.loads((root / 'start-result.json').read_text())
            self.assertFalse(saved['passed'])
            self.assertFalse(saved['cleanup']['passed'])
            self.assertEqual(set(saved['gates'].values()), {'failed'})
            self.assertIn('owned cleanup failed', saved['error'])
            self.assertFalse(saved['catalog_acceptance'])

    def test_partial_event_tail_is_retried_not_ignored(self):
        event = self.allow_events()[0]
        complete = qualification.json.dumps(event) + '\n'
        with patch.object(qualification, 'private_read', side_effect=['{"decision_id":', complete]):
            self.assertEqual(qualification.read_events(Path('/unused')), [event])
        with patch.object(qualification, 'private_read', return_value='broken\n'):
            with self.assertRaises(ValueError):
                qualification.read_events(Path('/unused'))
        with patch.object(qualification, 'private_read', return_value='{"incomplete":'), patch.object(qualification.time, 'monotonic', side_effect=[0, 1]):
            with self.assertRaises(ValueError):
                qualification.read_events(Path('/unused'))

    def test_external_runtime_root_rejected(self):
        with self.assertRaises(ValueError):
            qualification.validate_runtime_root(Path('/outside/qualification'))

    def test_rules_file_pin_duplicate_and_include_rejected(self):
        with tempfile.TemporaryDirectory(dir=qualification.STORAGE_ROOT) as directory:
            root = Path(directory)
            rules, config = root / 'rules.conf', root / 'runtime.conf'
            rules.write_bytes((qualification.REPO / 'common/rules/modsecurity_p1_p4_vectors.conf').read_bytes())
            config.write_text('rules_file=' + str(rules) + '\n')
            pin = qualification.digest(rules)
            qualification.validate_rule_binding(config, rules, pin)
            with self.assertRaises(ValueError):
                qualification.validate_rule_binding(config, rules, 'a' * 64)
            config.write_text('rules_file=' + str(rules) + '\nrules_file=' + str(rules) + '\n')
            with self.assertRaises(ValueError):
                qualification.validate_rule_binding(config, rules, pin)
            config.write_text('rules_file=' + str(rules) + '\n')
            rules.write_text('Include /external/other.conf\n')
            with self.assertRaises(ValueError):
                qualification.validate_rule_binding(config, rules, qualification.digest(rules))

    def test_loaded_library_requires_exact_pin(self):
        child = SimpleNamespace(process=SimpleNamespace(pid=123))
        maps = '0000-1111 r-xp 0000 00:00 1 /operator/libmodsecurity.so.3\n'
        with patch.object(Path, 'read_text', return_value=maps), patch.object(Path, 'stat', return_value=SimpleNamespace(st_ino=1, st_dev=os.makedev(0, 0))), patch.object(qualification, 'trusted_path', side_effect=lambda p: p), patch.object(qualification, 'digest', return_value='a' * 64):
            result = qualification.loaded_library(child, 'a' * 64)
            self.assertEqual(result[0]['sha256'], 'a' * 64)
            with self.assertRaises(ValueError):
                qualification.loaded_library(child, 'b' * 64)

    def test_library_mapping_inode_must_match_hashed_file(self):
        child = SimpleNamespace(process=SimpleNamespace(pid=123))
        maps = '0000-1111 r-xp 0000 00:00 1 /operator/libmodsecurity.so.3\n'
        with patch.object(Path, 'read_text', return_value=maps), patch.object(Path, 'stat', return_value=SimpleNamespace(st_ino=2, st_dev=os.makedev(0, 0))), patch.object(qualification, 'trusted_path', side_effect=lambda p: p):
            with self.assertRaises(ValueError):
                qualification.loaded_library(child, 'a' * 64)

    def test_library_device_translation_requires_process_mount_binding(self):
        child = SimpleNamespace(process=SimpleNamespace(pid=123))
        maps = '0000-1111 r-xp 0000 00:2d 1 /operator/libmodsecurity.so.3\n'
        mountinfo = '1 0 0:45 / /operator rw - ext4 /dev/root rw\n'

        def proc_file(path):
            return mountinfo if path.name == 'mountinfo' else maps

        metadata = SimpleNamespace(st_ino=1, st_dev=os.makedev(0, 48))
        with patch.object(Path, 'read_text', autospec=True, side_effect=proc_file), \
                patch.object(Path, 'stat', return_value=metadata), \
                patch.object(qualification, 'trusted_path', side_effect=lambda p: p), \
                patch.object(qualification.os, 'stat', return_value=SimpleNamespace(st_dev=1, st_ino=2)), \
                patch.object(qualification, 'digest', return_value='a' * 64):
            result = qualification.loaded_library(child, 'a' * 64)
            self.assertTrue(result[0]['device_translation_verified'])

        mountinfo = '1 0 0:44 / /operator rw - ext4 /dev/root rw\n'
        with patch.object(Path, 'read_text', autospec=True, side_effect=proc_file), \
                patch.object(Path, 'stat', return_value=metadata), \
                patch.object(qualification, 'trusted_path', side_effect=lambda p: p), \
                patch.object(qualification.os, 'stat', return_value=SimpleNamespace(st_dev=1, st_ino=2)):
            with self.assertRaises(ValueError):
                qualification.loaded_library(child, 'a' * 64)

    def test_library_mapping_segments_and_mount_namespace_must_be_stable(self):
        child = SimpleNamespace(process=SimpleNamespace(pid=123))
        path = '/operator/libmodsecurity.so.3'
        mixed = (f'0000-1111 r--p 0000 00:2d 1 {path}\n'
                 f'1111-2222 r-xp 0000 00:30 1 {path}\n'
                 '2222-3333 rw-p 0000 00:00 0 [stack]\n')
        metadata = SimpleNamespace(st_ino=1, st_dev=os.makedev(0, 48))
        with patch.object(Path, 'read_text', return_value=mixed), \
                patch.object(Path, 'stat', return_value=metadata), \
                patch.object(qualification, 'trusted_path', side_effect=lambda p: p):
            with self.assertRaises(ValueError):
                qualification.loaded_library(child, 'a' * 64)

        maps = f'0000-1111 r-xp 0000 00:2d 1 {path}\n'
        mountinfo = '1 0 0:45 / /operator rw - ext4 /dev/root rw\n'
        with patch.object(Path, 'read_text', autospec=True,
                          side_effect=lambda value: mountinfo if value.name == 'mountinfo' else maps), \
                patch.object(Path, 'stat', return_value=metadata), \
                patch.object(qualification, 'trusted_path', side_effect=lambda p: p), \
                patch.object(qualification.os, 'stat', side_effect=(
                    SimpleNamespace(st_dev=1, st_ino=2),
                    SimpleNamespace(st_dev=1, st_ino=3))):
            with self.assertRaises(ValueError):
                qualification.loaded_library(child, 'a' * 64)

    def test_duplicate_raw_json_fields_rejected(self):
        with patch.object(qualification, 'private_read', return_value='{"phase":"P1","phase":"P2"}\n'):
            with self.assertRaises(ValueError):
                qualification.read_events(Path('/unused'))

    def test_pid_reuse_is_not_owned_descendant(self):
        old = {'pid': 123, 'start_token': 'original'}
        with patch.object(qualification, 'process_record', return_value={'pid': 123, 'start_token': 'reused'}):
            self.assertEqual(qualification.surviving_descendants([old]), [])

    def test_traefik_requires_reservation_and_finish_reason(self):
        events = self.allow_events()
        for event in events:
            event.update(connector='traefik', request_path='traefik.forwardAuth', response_path='traefik.native_uds', transport='traefik_forwardauth_private_uds')
        events[-1]['reason'] = 'finish'
        reservation = {k: v for k, v in events[0].items() if k in qualification.EVENT_BASE}
        reservation.update(phase='reservation', outcome='reserved')
        events.insert(0, reservation)
        self.assertEqual(qualification.verify_events(events, {'allow': 1}, 'traefik'), {'allow': 1})
        with self.assertRaises(ValueError):
            qualification.verify_events(events[1:], {'allow': 1}, 'traefik')

    def test_runtime_alternate_rule_sources_cannot_pass(self):
        with tempfile.TemporaryDirectory(dir=qualification.STORAGE_ROOT) as directory:
            root = Path(directory)
            rules, config = root / 'rules.conf', root / 'runtime.conf'
            rules.write_bytes((qualification.REPO / 'common/rules/modsecurity_p1_p4_vectors.conf').read_bytes())
            for key, value in (('rules_remote_url', 'https://untrusted.invalid/rules'), ('rules_remote_key', 'dummy'), ('rules_inline', 'SecRuleEngine Off')):
                with self.subTest(key=key):
                    config.write_text(f'rules_file={rules}\n{key}={value}\n')
                    with self.assertRaises(ValueError):
                        qualification.validate_rule_binding(config, rules, qualification.digest(rules))

    def test_external_rule_operators_actions_and_scripts_cannot_pass(self):
        fixture = (qualification.REPO / 'common/rules/modsecurity_p1_p4_vectors.conf').read_text()
        with tempfile.TemporaryDirectory(dir=qualification.STORAGE_ROOT) as directory:
            root = Path(directory)
            rules, config = root / 'rules.conf', root / 'runtime.conf'
            config.write_text(f'rules_file={rules}\n')
            additions = ('SecRuleScript /external/script.lua',
                         'SecRule REQUEST_URI "@pmFromFile /external/list" "id:9,phase:1,deny"',
                         'SecRule FILES_TMPNAMES "@inspectFile /external/script" "id:9,phase:2,deny"',
                         'SecAction "id:9,phase:1,exec:/external/script"',
                         'SecRemoteRules dummy https://untrusted.invalid/rules')
            for addition in additions:
                with self.subTest(addition=addition):
                    rules.write_text(fixture + '\n' + addition + '\n')
                    with self.assertRaises(ValueError):
                        qualification.validate_rule_binding(config, rules, qualification.digest(rules))

    def test_traefik_yaml_values_are_complete_quoted_scalars(self):
        value = '/private/: # ["quoted"]\\filename'
        template = 'socketPath: __PATH__\nfilename: "__PATH__"\nurl: "https://__ADDR__"\n'
        rendered = qualification.render_traefik_yaml(template, {'__PATH__': value, '__ADDR__': '127.0.0.1:12000'})
        decoded = [qualification.json.loads(line.split(': ', 1)[1]) for line in rendered.splitlines()]
        self.assertEqual(decoded, [value, value, 'https://127.0.0.1:12000'])
        for unsafe in ('/private\nrouters: injected', '/private\x00file', '/private/__PATH__'):
            with self.subTest(unsafe=unsafe), self.assertRaises(ValueError):
                qualification.render_traefik_yaml(template, {'__PATH__': unsafe, '__ADDR__': '127.0.0.1:12000'})

    def test_actual_traefik_template_url_scalars_preserve_prefix_and_suffix(self):
        template = (qualification.REPO / 'connectors/traefik/config/traefik-forwardauth-composite-dynamic.yaml').read_text()
        self.assertIn('address: http://__AUTH_ADDRESS__/authorize', template)
        self.assertIn('- url: https://__UPSTREAM_ADDRESS__', template)
        values = {'__AUTH_ADDRESS__': '127.0.0.1:12002', '__UPSTREAM_ADDRESS__': '127.0.0.1:12001',
                  '__COMPOSITE_SOCKET__': '/private/socket # "quoted".sock', '__UPSTREAM_CERTIFICATE__': '/private/ca # "quoted".pem'}
        rendered = qualification.render_traefik_yaml(template, values)
        address = next(line.strip()[len('address: '):] for line in rendered.splitlines() if line.strip().startswith('address: '))
        upstream_url = next(line.strip()[len('- url: '):] for line in rendered.splitlines() if line.strip().startswith('- url: '))
        self.assertEqual(qualification.json.loads(address), 'http://127.0.0.1:12002/authorize')
        self.assertEqual(qualification.json.loads(upstream_url), 'https://127.0.0.1:12001')
        socket_path = next(line.strip()[len('socketPath: '):] for line in rendered.splitlines() if line.strip().startswith('socketPath: '))
        self.assertEqual(qualification.json.loads(socket_path), values['__COMPOSITE_SOCKET__'])

    def test_four_actual_upstream_handlers_overlap(self):
        server = SimpleNamespace(lock=threading.Lock(), parallel_barrier=threading.Barrier(4),
                                 parallel=dict.fromkeys(('parallel_requests_seen', 'parallel_inflight', 'parallel_max_inflight', 'parallel_barrier_passes', 'parallel_barrier_errors'), 0))
        def handler(_index):
            passed = upstream.parallel_enter(server)
            upstream.parallel_leave(server)
            return passed
        with patch.object(upstream, 'persist'):
            with ThreadPoolExecutor(max_workers=4) as pool:
                self.assertEqual(list(pool.map(handler, range(4))), [True] * 4)
        self.assertEqual(server.parallel['parallel_max_inflight'], 4)
        self.assertEqual(server.parallel['parallel_barrier_passes'], 4)
        self.assertEqual(server.parallel['parallel_inflight'], 0)
        complete = self.observation(8)
        complete.update(server.parallel)
        complete.update(parallel_requests_seen=8, parallel_barrier_passes=8)
        qualification.verify_parallel_overlap(complete)
        complete['parallel_max_inflight'] = 1
        with self.assertRaises(ValueError):
            qualification.verify_parallel_overlap(complete)


if __name__ == "__main__":
    unittest.main()
