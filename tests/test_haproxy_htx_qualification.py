"""Strict prerequisite contracts; these tests are not HAProxy runtime proof."""

import importlib.util
from pathlib import Path
import os
import sys
import socket
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

HARNESS = Path(__file__).resolve().parents[1] / 'connectors/haproxy/harness'
sys.path.insert(0, str(HARNESS))
SPEC = importlib.util.spec_from_file_location('htx_qualification', HARNESS / 'haproxy_htx_qualification.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class QualificationContract(unittest.TestCase):
    def test_host_log_ack_uses_only_suffix_after_unchanged_pinned_prefix(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            root = runner.verified_runtime_root(raw)
            target = root / 'host.log'
            prefix = 'HTXQ synthetic-prefix\n'
            runner.write_text_atomic(root, target, prefix, 'test host log')
            pin = runner.campaign_host_log(root)
            suffix = ('[WARNING]  (123) : Proxy htx_in stopped (cumulated conns: FE: 1, BE: 0).\n'
                      '[WARNING]  (123) : Proxy htx_upstream stopped (cumulated conns: FE: 0, BE: 0).\n')
            with target.open('a') as stream:
                stream.write(suffix)
            full, post = runner.campaign_host_log(root, pin)
            self.assertEqual((full, post), (prefix + suffix, suffix))
            runner.campaign_soft_stop_ack(post, {'pid': 123}, [])
            with self.assertRaisesRegex(ValueError, 'stale stop'):
                runner.campaign_host_log(root)

    def test_host_log_prefix_drift_replacement_partial_and_oversize_fail(self):
        for failure in ('truncate', 'prefix-drift', 'replacement', 'symlink', 'hardlink',
                        'partial-append', 'oversized'):
            with self.subTest(failure=failure):
                with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
                    root = runner.verified_runtime_root(raw)
                    target = root / 'host.log'
                    runner.write_text_atomic(root, target, 'HTXQ synthetic-prefix\n', 'test host log')
                    pin = runner.campaign_host_log(root)
                    if failure == 'truncate':
                        target.write_text('short\n')
                    elif failure == 'prefix-drift':
                        target.write_text('HTXQ SYNTHETIC-prefix\n')
                    elif failure in ('replacement', 'symlink', 'hardlink'):
                        saved = root / 'saved.log'
                        target.rename(saved)
                        if failure == 'replacement':
                            target.write_bytes(saved.read_bytes())
                            target.chmod(0o600)
                        elif failure == 'symlink':
                            target.symlink_to(saved)
                        else:
                            os.link(saved, target)
                    elif failure == 'partial-append':
                        with target.open('a') as stream:
                            stream.write('[WARNING] partial')
                    else:
                        target.write_bytes(b'x' * ((8 << 20) + 1))
                    with self.assertRaises((OSError, ValueError)):
                        runner.campaign_host_log(root, pin)

    def test_log_prefix_is_captured_before_confirmed_signal_delivery(self):
        identity = {'pid': 123, 'start_token': '456', 'exe': '/pinned/haproxy', 'exe_sha256': 'a' * 64}
        child = Mock(descendants={})
        child.identity.return_value = identity
        child.process.poll.return_value = None
        child.process.wait.return_value = 0
        events = []
        pin = {'identity': [], 'offset': 10, 'prefix_sha256': 'a' * 64}
        def snapshot(root):
            events.append('snapshot')
            return pin
        def deliver(*args):
            events.append('signal')
        with patch.object(runner, 'surviving_descendants', return_value=[]), \
                patch.object(runner.os, 'pidfd_open', return_value=88), \
                patch.object(runner.signal, 'pidfd_send_signal', side_effect=deliver), \
                patch.object(runner.os, 'close'), \
                patch.object(runner, 'campaign_host_log', side_effect=snapshot):
            receipt = runner.campaign_stop(child, identity, Path('/private'))
        self.assertEqual(events, ['snapshot', 'signal'])
        self.assertEqual(receipt['host_log_pin'], pin)

    def test_native_soft_stop_ack_requires_exact_pid_proxies_counts_and_uniqueness(self):
        identity = {'pid': 123}
        probes = [{'token': 'q1-allow', 'backend': 1}, {'token': 'q1-p1', 'backend': 0}]
        front = 'Proxy htx_in stopped (cumulated conns: FE: 3, BE: 0).'
        back = 'Proxy htx_upstream stopped (cumulated conns: FE: 0, BE: 2).'
        native = f'[WARNING]  (123) : {front}\n[WARNING]  (123) : {back}\n'
        self.assertEqual(set(runner.campaign_soft_stop_ack(native, identity, probes)),
                         {'htx_in', 'htx_upstream'})
        runner.campaign_soft_stop_ack(native + front + '\n' + back + '\n', identity, probes)
        for bad in ('', native.replace('(123)', '(124)'), native.replace('htx_in', 'other'),
                    native.replace('FE: 3', 'FE: 4'), native.replace('BE: 2', 'BE: 1'),
                    native + native.splitlines()[0] + '\n', native + front + '\n' + front + '\n',
                    native + '[WARNING]  (123) : Proxy htx_in hard-stopped (1 remaining conns will be closed).\n',
                    native + '[WARNING]  (123) : soft-stop running for too long, performing a hard-stop.\n',
                    native.replace('stopped', 'Stopped'), native.replace('[WARNING]  ', '[WARNING] '),
                    native.replace('FE: 3', 'FE: 03'), front + '\n' + back + '\n'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                runner.campaign_soft_stop_ack(bad, identity, probes)

    def test_soft_stop_frontend_count_uses_connections_including_one_readiness_and_keepalive(self):
        probes = [{'token': f'q1-keep-{n}', 'backend': int(n % 2 == 0)} for n in range(5)]
        text = ('[WARNING]  (123) : Proxy htx_in stopped (cumulated conns: FE: 2, BE: 0).\n'
                '[WARNING]  (123) : Proxy htx_upstream stopped (cumulated conns: FE: 0, BE: 5).\n')
        runner.campaign_soft_stop_ack(text, {'pid': 123}, probes)

    def test_proxy_backend_stream_counter_is_distinct_from_origin_dispatch(self):
        probes = [{'token': 'q1-allow', 'case': 'allow', 'body_bytes': 0, 'backend': 1},
                  {'token': 'q1-p1', 'case': 'p1', 'body_bytes': 0, 'backend': 0},
                  {'token': 'q1-p2', 'case': 'p2', 'body_bytes': len(runner.P2_BODY), 'backend': 0}]
        origin = {'requests': [{'token': 'q1-allow', 'case': 'allow', 'body_bytes': 0,
                               'body_sha256': runner.hashlib.sha256(b'').hexdigest()}],
                  'errors': [], 'active': 0, 'accepts': 1}
        text = ('[WARNING]  (123) : Proxy htx_in stopped (cumulated conns: FE: 4, BE: 0).\n'
                '[WARNING]  (123) : Proxy htx_upstream stopped (cumulated conns: FE: 0, BE: 3).\n')
        runner.campaign_backend_check(origin, probes)
        runner.campaign_soft_stop_ack(text, {'pid': 123}, probes)
        for wrong in (1, 2, 4):
            with self.subTest(counter=wrong), self.assertRaises(ValueError):
                runner.campaign_soft_stop_ack(text.replace('BE: 3', f'BE: {wrong}'), {'pid': 123}, probes)
        leaked = {'token': 'q1-p1', 'case': 'p1', 'body_bytes': 0,
                  'body_sha256': runner.hashlib.sha256(b'').hexdigest()}
        with self.assertRaises(ValueError):
            runner.campaign_backend_check({**origin, 'requests': origin['requests'] + [leaked]}, probes)

    def test_zombie_signal_success_exit_zero_without_native_ack_fails(self):
        identity = {'pid': 123, 'start_token': '456', 'exe': '/pinned/haproxy',
                    'exe_sha256': 'a' * 64}
        child = Mock(descendants={})
        child.identity.return_value = identity
        child.process.poll.return_value = None
        child.process.wait.return_value = 0
        with patch.object(runner, 'surviving_descendants', return_value=[]), \
                patch.object(runner.os, 'pidfd_open', return_value=88), \
                patch.object(runner.signal, 'pidfd_send_signal'), \
                patch.object(runner.os, 'close'):
            receipt = runner.campaign_stop(child, identity)
        self.assertEqual(receipt['returncode'], 0)
        with self.assertRaisesRegex(ValueError, 'missing native'):
            runner.campaign_soft_stop_ack('', identity, [])

    def test_missing_pidfd_api_is_controlled_fail_closed(self):
        for namespace, name in ((runner.os, 'pidfd_open'), (runner.signal, 'pidfd_send_signal')):
            child = Mock()
            with patch.object(namespace, name, None):
                with self.assertRaisesRegex(ValueError, 'requires pidfd APIs'):
                    runner.campaign_stop(child, {'pid': 123})
            child.identity.assert_not_called()
            child.stop.assert_called_once_with()

    def observe_synthetic_termination(self, wire, failure, write_failure=False, prior_errors=()):
        class Connection:
            def __init__(self):
                self.data = bytearray(wire)
            def settimeout(self, value):
                pass
            def recv(self, count):
                if not self.data:
                    raise failure
                data = bytes(self.data[:count])
                del self.data[:count]
                return data
            def sendall(self, data):
                if write_failure:
                    raise failure
        upstream = runner.CampaignUpstream()
        upstream.errors.extend(prior_errors)
        connection = Connection()
        upstream.handlers.add(connection)
        try:
            runner.CampaignHandler(connection, ('127.0.0.1', 12345), upstream)
            return upstream.snapshot()
        finally:
            upstream.close()

    def test_connection_reset_only_after_complete_same_connection_request_boundary(self):
        wire = runner.campaign_wire('allow', 'q1-allow', True)
        observed = self.observe_synthetic_termination(wire, ConnectionResetError('synthetic reset'))
        self.assertEqual(observed['errors'], [])
        self.assertEqual(observed['boundary_terminations'],
                         [{'kind': 'connection_reset', 'request_tokens': ['q1-allow']}])
        probe = {'token': 'q1-allow', 'case': 'allow', 'body_bytes': 0, 'backend': 1}
        runner.campaign_backend_check(observed, [probe])
        for bad in ([], ['q1-unknown'], ['q1-allow', 'q1-allow']):
            with self.subTest(tokens=bad), self.assertRaises(ValueError):
                runner.campaign_backend_check({**observed, 'boundary_terminations':
                    [{'kind': 'connection_reset', 'request_tokens': bad}]}, [probe])
        with self.assertRaises(ValueError):
            runner.campaign_backend_check({**observed, 'boundary_terminations':
                observed['boundary_terminations'] * 2}, [probe])
        observed = self.observe_synthetic_termination(
            wire + runner.campaign_wire('allow', 'q1-second', True), ConnectionResetError('reset'),
            prior_errors=['earlier partial request'])
        self.assertEqual(observed['errors'], ['earlier partial request'])
        self.assertEqual(observed['boundary_terminations'],
                         [{'kind': 'connection_reset', 'request_tokens': ['q1-allow', 'q1-second']}])
        with self.assertRaises(ValueError):
            runner.campaign_backend_check(observed, [probe])

    def test_reset_partial_headers_body_send_and_timeout_remain_fatal(self):
        complete = runner.campaign_wire('allow', 'q1-allow', True)
        partial_line = b'POST /htxq/q1-next'
        partial_header = b'POST /htxq/q1-next HTTP/1.1\r\nContent-Length:'
        partial_body = runner.campaign_wire('nonempty', 'q1-next', True)[:-1]
        for suffix in (b'', partial_line, partial_header, partial_body):
            with self.subTest(suffix=suffix):
                # Reset before the first complete request is always fatal.
                observed = self.observe_synthetic_termination(suffix, ConnectionResetError('reset'))
                self.assertTrue(observed['errors'])
                self.assertEqual(observed['boundary_terminations'], [])
                if suffix:
                    observed = self.observe_synthetic_termination(complete + suffix, ConnectionResetError('reset'))
                    self.assertTrue(observed['errors'])
                    self.assertEqual(observed['boundary_terminations'], [])
        for failure, write_failure in ((TimeoutError('timeout'), False),
                                       (ConnectionResetError('write reset'), True)):
            with self.subTest(failure=failure):
                observed = self.observe_synthetic_termination(complete, failure, write_failure)
                self.assertTrue(observed['errors'])
                self.assertEqual(observed['boundary_terminations'], [])

    def test_each_parallel_probe_checks_pins_and_only_returns_one_original_id(self):
        args = object()
        checked = threading.local()
        def check(value):
            self.assertIs(value, args)
            checked.ready = True
        def probe(front, case, token):
            self.assertTrue(checked.ready)
            checked.ready = False
            self.assertEqual((front, case), (20001, 'parallel'))
            return {'id': token}
        results = []
        with patch.object(runner, 'check_campaign_rules', side_effect=check) as pins:
            with patch.object(runner, 'campaign_probe', side_effect=probe) as probes:
                with runner.ThreadPoolExecutor(max_workers=4) as pool:
                    futures = [pool.submit(runner.campaign_parallel_probe, args, 20001,
                                           f'q1-parallel-{n}') for n in range(4)]
                    self.assertEqual(results, [])
                    results.extend(f.result() for f in futures)
        self.assertEqual(pins.call_count, 4)
        self.assertEqual(probes.call_count, 4)
        self.assertEqual(results, [{'id': f'q1-parallel-{n}'} for n in range(4)])

    def test_pin_drift_in_parallel_task_fails_before_its_probe(self):
        lock = threading.Lock()
        count = 0
        def check(args):
            nonlocal count
            with lock:
                count += 1
                if count == 3:
                    raise ValueError('pinned rules drift')
        with patch.object(runner, 'check_campaign_rules', side_effect=check) as pins:
            with patch.object(runner, 'campaign_probe', return_value={'passed': True}) as probes:
                with runner.ThreadPoolExecutor(max_workers=4) as pool:
                    futures = [pool.submit(runner.campaign_parallel_probe, object(), 20001,
                                           f'q1-parallel-{n}') for n in range(4)]
                    with self.assertRaisesRegex(ValueError, 'pinned rules drift'):
                        [f.result() for f in futures]
        self.assertEqual(pins.call_count, 4)
        self.assertEqual(probes.call_count, 3)

    def rules_fixture(self, raw):
        root = runner.verified_runtime_root(str(Path(raw) / 'campaign'))
        source = Path(raw) / 'external.conf'
        text = '\n'.join(('id:1100001,phase:1,deny,status:403',
                          'id:1100002,phase:1,deny,status:429',
                          'id:1100101,phase:2,deny,status:403',
                          'id:1100201,phase:3,deny,status:403',
                          'id:1100301,phase:4,deny,status:403')) + '\n'
        source.write_text(text)
        return root, source, runner.digest(source)

    def test_external_rules_are_copied_before_contained_canonical_validation(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            root, source, expected = self.rules_fixture(raw)
            with patch.object(runner, 'canonical_rules_content', wraps=runner.canonical_rules_content) as canonical:
                destination, source_pin, destination_pin = runner.copy_campaign_rules(root, source, expected)
            canonical.assert_called_once_with(root, str(root / 'rules.conf'))
            self.assertEqual(destination.read_bytes(), source.read_bytes())
            self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
            self.assertNotEqual(source_pin, destination_pin)
            args = Mock(rules=source, rules_sha256=expected, rules_source_pin=source_pin,
                        rules_path=destination, rules_pin=destination_pin, campaign_root=root,
                        start_rules_pins=[])
            runner.check_campaign_rules(args)
            start = runner.verified_runtime_root(str(root / 'start1'))
            local, _, _ = runner.copy_campaign_rules(start, destination, expected, destination_pin)
            self.assertEqual(local.read_bytes(), source.read_bytes())

    def test_rules_source_drift_during_copy_fails(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            root, source, expected = self.rules_fixture(raw)
            original = runner.write_text_atomic
            def drift(*args):
                result = original(*args)
                source.write_text(source.read_text() + '# changed\n')
                return result
            with patch.object(runner, 'write_text_atomic', side_effect=drift):
                with self.assertRaises(ValueError):
                    runner.copy_campaign_rules(root, source, expected)

    def test_pinned_rules_reject_source_or_destination_replacement_and_links(self):
        for target_kind in ('source', 'destination'):
            for change in ('rewrite', 'replace', 'symlink', 'hardlink'):
                with self.subTest(target=target_kind, change=change):
                    with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
                        root, source, expected = self.rules_fixture(raw)
                        destination, source_pin, destination_pin = runner.copy_campaign_rules(root, source, expected)
                        args = Mock(rules=source, rules_sha256=expected, rules_source_pin=source_pin,
                                    rules_path=destination, rules_pin=destination_pin, campaign_root=root,
                                    start_rules_pins=[])
                        target = source if target_kind == 'source' else destination
                        saved = Path(raw) / 'saved.conf'
                        if change == 'rewrite':
                            target.write_text(target.read_text() + '# drift\n')
                        else:
                            target.rename(saved)
                            if change == 'replace':
                                target.write_bytes(saved.read_bytes())
                            elif change == 'symlink':
                                target.symlink_to(saved)
                            else:
                                os.link(saved, target)
                        with self.assertRaises((OSError, ValueError)):
                            runner.check_campaign_rules(args)

    def test_rules_hash_mismatch_never_reaches_canonical_helper(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            root, source, _ = self.rules_fixture(raw)
            with patch.object(runner, 'canonical_rules_content') as canonical:
                with self.assertRaises(ValueError):
                    runner.copy_campaign_rules(root, source, '0' * 64)
            canonical.assert_not_called()
            self.assertFalse((root / 'rules.conf').exists())

    def test_campaign_copy_rejects_existing_destination_links(self):
        for kind in ('symlink', 'hardlink'):
            with self.subTest(kind=kind):
                with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
                    root, source, expected = self.rules_fixture(raw)
                    if kind == 'symlink':
                        (root / 'rules.conf').symlink_to(source)
                    else:
                        os.link(source, root / 'rules.conf')
                    with self.assertRaises((OSError, ValueError)):
                        runner.copy_campaign_rules(root, source, expected)

    def test_rules_mutation_during_descriptor_read_fails(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            _, source, expected = self.rules_fixture(raw)
            original = os.fstat
            calls = 0
            def drift(fd):
                nonlocal calls
                calls += 1
                if calls == 2:
                    source.write_text(source.read_text() + '# drift\n')
                return original(fd)
            with patch.object(runner.os, 'fstat', side_effect=drift):
                with self.assertRaises(ValueError):
                    runner.pinned_rules(source, expected)

    def test_completed_start_copy_remains_pinned_until_campaign_end(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            root, source, expected = self.rules_fixture(raw)
            destination, source_pin, destination_pin = runner.copy_campaign_rules(root, source, expected)
            start = runner.verified_runtime_root(str(root / 'start1'))
            local, _, pin = runner.copy_campaign_rules(start, destination, expected, destination_pin)
            args = Mock(rules=source, rules_sha256=expected, rules_source_pin=source_pin,
                        rules_path=destination, rules_pin=destination_pin, campaign_root=root,
                        start_rules_pins=[(start, local, pin)])
            runner.check_campaign_rules(args)
            local.write_text(local.read_text() + '# late drift\n')
            with self.assertRaises(ValueError):
                runner.check_campaign_rules(args)

    def test_replacement_during_canonical_validation_fails(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            root, source, expected = self.rules_fixture(raw)
            def replace(root, value):
                destination = Path(value)
                text = destination.read_text()
                destination.rename(root / 'replaced.conf')
                destination.write_text(text)
            with patch.object(runner, 'canonical_rules_content', side_effect=replace):
                with self.assertRaises(ValueError):
                    runner.copy_campaign_rules(root, source, expected)

    def test_controlled_shutdown_requires_live_original_executable_and_exit_zero(self):
        identity = {'pid': 123, 'start_token': '456', 'exe': '/pinned/haproxy',
                    'exe_sha256': 'a' * 64}
        child = Mock(descendants={})
        child.identity.return_value = identity
        child.process.poll.return_value = None
        child.process.wait.return_value = 0
        with patch.object(runner, 'surviving_descendants', return_value=[]), \
                patch.object(runner.os, 'pidfd_open', return_value=88) as opened, \
                patch.object(runner.signal, 'pidfd_send_signal') as delivered, \
                patch.object(runner.os, 'close') as closed:
            receipt = runner.campaign_stop(child, identity)
        self.assertEqual(receipt, {'signal': 'SIGUSR1', 'delivery': 'pidfd_send_signal',
                                   'returncode': 0, 'no_kill_fallback': True, 'host_log_pin': None})
        opened.assert_called_once_with(123, 0)
        delivered.assert_called_once_with(88, runner.signal.SIGUSR1, None, 0)
        closed.assert_called_once_with(88)
        child.process.send_signal.assert_not_called()
        child.process.wait.assert_called_once_with(timeout=3)
        child.process.kill.assert_not_called()
        child.stop.assert_called_once_with()

    def test_controlled_shutdown_rejects_exit_kill_and_identity_drift(self):
        identity = {'pid': 123, 'start_token': '456', 'exe': '/pinned/haproxy',
                    'exe_sha256': 'a' * 64}
        for failure in ('early-exit', 'sha-drift', 'pid-drift', 'start-drift', 'exit-one',
                        'unhandled-soft-stop', 'killed', 'timeout', 'descendant', 'dead-before-signal'):
            with self.subTest(failure=failure):
                child = Mock(descendants={})
                child.identity.return_value = dict(identity)
                child.process.poll.return_value = None
                child.process.wait.return_value = 0
                if failure == 'early-exit':
                    child.identity.side_effect = ValueError('owned process exited')
                elif failure.endswith('drift'):
                    key = {'sha-drift': 'exe_sha256', 'pid-drift': 'pid',
                           'start-drift': 'start_token'}[failure]
                    child.identity.return_value[key] = 'changed'
                elif failure == 'timeout':
                    child.process.wait.side_effect = runner.subprocess.TimeoutExpired('host', 3)
                elif failure == 'dead-before-signal':
                    child.process.poll.return_value = 0
                elif failure != 'descendant':
                    child.process.wait.return_value = {'exit-one': 1,
                        'unhandled-soft-stop': -runner.signal.SIGUSR1, 'killed': -runner.signal.SIGKILL}[failure]
                with patch.object(runner, 'surviving_descendants',
                                  return_value=[{'pid': 999}] if failure == 'descendant' else []), \
                        patch.object(runner.os, 'pidfd_open', return_value=88), \
                        patch.object(runner.signal, 'pidfd_send_signal'), \
                        patch.object(runner.os, 'close'):
                    with self.assertRaises(ValueError):
                        runner.campaign_stop(child, identity)
                child.stop.assert_called_once_with()
                if failure in ('early-exit', 'sha-drift', 'pid-drift', 'start-drift', 'descendant'):
                    child.process.send_signal.assert_not_called()

    def test_popen_no_delivery_race_cannot_qualify_shutdown(self):
        identity = {'pid': 123, 'start_token': '456', 'exe': '/pinned/haproxy',
                    'exe_sha256': 'a' * 64}
        process = Mock(pid=123, returncode=None)
        polls = 0
        def raced_poll():
            nonlocal polls
            polls += 1
            if polls == 2:
                process.returncode = 0
            return process.returncode
        process.poll.side_effect = raced_poll
        process.wait.return_value = 0
        # Reproduce the former false pass using the real Popen signal method.
        with patch.object(runner.os, 'kill') as system_call:
            self.assertIsNone(process.poll())
            runner.subprocess.Popen.send_signal(process, runner.signal.SIGUSR1)
            self.assertEqual(process.wait(timeout=3), 0)
        system_call.assert_not_called()
        child = Mock(descendants={})
        child.identity.return_value = identity
        child.process.poll.return_value = None
        child.process.wait.return_value = 0
        with patch.object(runner, 'surviving_descendants', return_value=[]), \
                patch.object(runner.os, 'pidfd_open', return_value=88), \
                patch.object(runner.signal, 'pidfd_send_signal', side_effect=ProcessLookupError('exited')), \
                patch.object(runner.os, 'close') as closed:
            with self.assertRaises(ProcessLookupError):
                runner.campaign_stop(child, identity)
        closed.assert_called_once_with(88)
        child.process.wait.assert_not_called()
        child.stop.assert_called_once_with()

    def test_pidfd_binding_delivery_and_close_errors_fail_and_release_fd(self):
        identity = {'pid': 123, 'start_token': '456', 'exe': '/pinned/haproxy',
                    'exe_sha256': 'a' * 64}
        for failure in ('open-esrch', 'open-permission', 'post-open-exit',
                        'post-open-identity', 'send-esrch', 'send-permission', 'close-error'):
            with self.subTest(failure=failure):
                child = Mock(descendants={})
                child.identity.return_value = identity
                child.process.poll.return_value = None
                child.process.wait.return_value = 0
                if failure == 'post-open-exit':
                    child.process.poll.side_effect = [None, 0]
                if failure == 'post-open-identity':
                    child.identity.side_effect = [identity, identity, {**identity, 'start_token': 'changed'}]
                with patch.object(runner, 'surviving_descendants', return_value=[]), \
                        patch.object(runner.os, 'pidfd_open', return_value=88) as opened, \
                        patch.object(runner.signal, 'pidfd_send_signal') as delivered, \
                        patch.object(runner.os, 'close') as closed:
                    if failure.startswith('open-'):
                        opened.side_effect = ProcessLookupError() if failure == 'open-esrch' else PermissionError()
                    elif failure.startswith('send-'):
                        delivered.side_effect = ProcessLookupError() if failure == 'send-esrch' else PermissionError()
                    elif failure == 'close-error':
                        closed.side_effect = OSError('close failed')
                    with self.assertRaises((OSError, ValueError)):
                        runner.campaign_stop(child, identity)
                    if failure.startswith('open-'):
                        closed.assert_not_called()
                    else:
                        closed.assert_called_once_with(88)
                    if failure.startswith('open-') or failure.startswith('post-open-'):
                        delivered.assert_not_called()
                child.process.wait.assert_not_called()
                child.process.send_signal.assert_not_called()
                child.stop.assert_called_once_with()

    def test_complete_log_reconciliation_rejects_shutdown_panic_and_native_engine_error(self):
        probe = {'case': 'allow', 'token': 'q1-allow', 'status': 200, 'body_bytes': 0, 'backend': 1}
        text = ('HTXQ request_id=/htxq/q1-allow host_id=haproxy-htx-1 status=200 termination=----\n'
                'modsecurity-htx: buffered request inspected before header release; '
                'transaction_id=haproxy-htx-1 body_mode=buffered body_bytes_seen=0 eos_seen=true\n')
        self.assertEqual(len(runner.campaign_correlate(text, [probe])), 1)
        for diagnostic in ('panic: shutdown failed', 'FATAL: shutdown failed',
                           '[ALERT] shutdown failed', 'segmentation fault',
                           'modsecurity-htx: engine error during shutdown',
                           'modsecurity-htx: failed to initialize the ModSecurity engine',
                           'modsecurity-htx: unknown diagnostic'):
            with self.subTest(diagnostic=diagnostic), self.assertRaises(ValueError):
                runner.campaign_correlate(text + diagnostic + '\n', [probe])

    def valid(self):
        return {'accepts': 0, 'complete_headers': 0, 'body_bytes': 0,
                'request_completed': 0, 'parse_errors': 0}

    def test_zero_dispatch_with_real_deny_has_no_observed_failure(self):
        self.assertEqual(runner.assess(403, self.valid(), True), [])

    def test_every_backend_observation_fails_separately(self):
        for field in ('accepts', 'complete_headers', 'body_bytes', 'request_completed', 'parse_errors'):
            with self.subTest(field=field):
                evidence = self.valid()
                evidence[field] = 1
                self.assertTrue(runner.assess(403, evidence, True))

    def test_client_deny_never_substitutes_for_engine_rule(self):
        self.assertTrue(runner.assess(403, self.valid(), False))
        self.assertTrue(runner.assess(503, self.valid(), True))

    def test_config_selects_only_native_htx(self):
        config = runner.config(20001, 20002, Path('/private/rules.conf'))
        self.assertIn('filter modsecurity-htx rules-file', config)
        for forbidden in ('spoe', 'send-spoe', 'http-buffer-request', 'wait-for-body'):
            self.assertNotIn(forbidden, config)

    def test_explicit_buffered_candidate_is_bounded_and_identified(self):
        config = runner.config(20001, 20002, Path('/private/rules.conf'), 'host-buffered')
        self.assertIn('option http-buffer-request', config)
        self.assertIn('request-body-mode host-buffered', config)
        self.assertIn('tune.bufsize 131072', config)
        self.assertIn('timeout http-request 5s', config)
        self.assertNotIn('spoe', config)

    def test_unknown_request_mode_rejected(self):
        with self.assertRaises(ValueError):
            runner.config(20001, 20002, Path('/private/rules.conf'), 'buffered-maybe')

    def test_buffered_eom_rule_proof_can_pass_but_streaming_stays_blocked(self):
        self.assertEqual(runner.qualification_outcome([], True, 'host-buffered'), 'PASS')
        self.assertEqual(runner.qualification_outcome([], False, 'host-buffered'), 'BLOCKED')
        self.assertEqual(runner.qualification_outcome(['backend_accepts'], False, 'host-buffered'), 'FAIL')

    def test_buffered_inspection_proof_binds_exact_id_size_eom_and_multiplicity(self):
        line = (f'modsecurity-htx: buffered request inspected before header release; transaction_id=haproxy-htx-7 '
                f'body_mode=buffered body_bytes_seen={len(runner.P2_BODY)} eos_seen=true\n')
        self.assertTrue(runner.valid_buffered_inspection(line))
        for invalid in (line * 2, line.replace('eos_seen=true', 'eos_seen=false'),
                        line.replace('haproxy-htx-7', 'other'),
                        line.replace('body_mode=buffered', 'body_mode=streaming')):
            self.assertFalse(runner.valid_buffered_inspection(invalid))

    def test_delayed_prefix_does_not_finish_body(self):
        self.assertGreater(len(runner.P2_BODY), 1)
        self.assertEqual(runner.P2_BODY[:-1] + runner.P2_BODY[-1:], runner.P2_BODY)

    def test_decision_requires_single_exact_id_rule_action(self):
        line = 'modsecurity-htx: request-body intervention observed; transaction_id=haproxy-htx-7 phase=2 status=403 rule_id=1100101 action=deny\n'
        self.assertTrue(runner.valid_decision(line))
        self.assertFalse(runner.valid_decision(line * 2))
        self.assertFalse(runner.valid_decision(line.replace('haproxy-htx-7', 'other')))
        self.assertFalse(runner.valid_decision(line.replace('1100101', '1100102')))
        self.assertFalse(runner.valid_decision(line + line.replace('1100101', '1100102')))
        self.assertFalse(runner.valid_decision(line.rstrip() + '-other\n'))

    def test_incomplete_backend_evidence_fails(self):
        self.assertTrue(runner.assess(403, {}, True))
        evidence = self.valid()
        evidence['accepts'] = False
        self.assertTrue(runner.assess(403, evidence, True))

    def test_config_rejects_path_injection(self):
        for suffix in ('${RULES}', '$RULES', '"rules"', "'rules'", 'rules\\escape',
                       'rules#comment', 'rules\nfilter', 'rules path', 'rules\tpath'):
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                runner.config(20001, 20002, Path('/private/' + suffix))

    def test_no_native_prefix_receipt_never_yields_pass(self):
        self.assertEqual(runner.qualification_outcome([], False), 'BLOCKED')
        self.assertEqual(runner.qualification_outcome(['backend_accepts'], False), 'FAIL')

    def test_delayed_observer_drains_real_queued_tcp_dispatch(self):
        gate = threading.Event()

        class DelayedBackend(runner.Backend):
            def serve(self):
                gate.wait(2)
                super().serve()

        backend = DelayedBackend()
        client = socket.create_connection(('127.0.0.1', backend.port), timeout=1)
        client.sendall((f'POST / HTTP/1.1\r\nHost: localhost\r\nX-Request-Id: {runner.REQUEST_ID}\r\n'
                        f'Content-Length: {len(runner.P2_BODY)}\r\n\r\n').encode() + runner.P2_BODY)
        client.close()  # Producer is gone, as the reaped host must be.
        backend.thread.start()
        timer = threading.Timer(0.1, gate.set)
        timer.start()
        try:
            backend.close()
        finally:
            gate.set()
            timer.join()
            backend.listener.close()
            backend.thread.join(2)
        observed = backend.snapshot()
        self.assertEqual(observed['accepts'], 1)
        self.assertEqual(observed['complete_headers'], 1)
        self.assertEqual(observed['body_bytes'], len(runner.P2_BODY))
        self.assertEqual(observed['request_completed'], 1)
        self.assertTrue(backend.barrier_accepted)
        self.assertTrue(backend.drained.is_set())
        self.assertFalse(backend.thread.is_alive())
        self.assertTrue(runner.assess(403, observed, True))

    def test_inputs_reject_digest_mismatch_and_symlink(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            target = Path(raw) / 'rules'
            target.write_bytes(b'rules')
            digest = runner.digest(target)
            self.assertEqual(runner.verified_input(str(target), digest, 5), target)
            with self.assertRaises(ValueError):
                runner.verified_input(str(target), '0' * 64, 5)
            with self.assertRaises(ValueError):
                runner.verified_input(str(target), digest, 4)
            link = Path(raw) / 'link'
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                runner.verified_input(str(link), digest, 5)

    def test_library_identity_binds_maps_inode_and_expected_digest(self):
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            target = Path(raw) / 'libmodsecurity.so'
            target.write_bytes(b'test-library-identity')
            stat = target.stat()
            device = f'{os.major(stat.st_dev):x}:{os.minor(stat.st_dev):x}'
            maps = f'1000-2000 r--p 0 {device} {stat.st_ino} {target}\n'
            identity = runner.mapped_libraries(maps, runner.digest(target))
            self.assertEqual(identity[0]['inode'], stat.st_ino)
            self.assertTrue(identity[0]['expected_digest_verified'])
            mounted = runner.mounted_device_for_path(Path('/proc/self'), str(target))
            translated_device = f'{mounted[0]:x}:{mounted[1]:x}'
            translated = maps.replace(f' {device} ', f' {translated_device} ')
            translated_identity = runner.mapped_libraries(
                translated, runner.digest(target), Path('/proc/self')
            )
            self.assertEqual(translated_identity[0]['map_device'], translated_device)
            unrelated = f'{mounted[0]:x}:{mounted[1] + 1:x}'
            with self.assertRaisesRegex(ValueError, 'process-mount binding'):
                runner.mapped_libraries(
                    maps.replace(f' {device} ', f' {unrelated} '),
                    runner.digest(target), Path('/proc/self')
                )
            with self.assertRaises(ValueError):
                runner.mapped_libraries(maps, '0' * 64)
            with self.assertRaises(ValueError):
                runner.mapped_libraries(
                    maps.replace(f' {stat.st_ino} ', f' {stat.st_ino + 1} '), None
                )


class CampaignContract(unittest.TestCase):
    def test_campaign_config_is_explicit_bounded_and_native(self):
        value = runner.campaign_config(20001, 20002, Path('/private/rules.conf'))
        self.assertIn('request-body-mode host-buffered', value)
        self.assertIn('host_id=haproxy-htx-%rt', value)
        self.assertIn('request_id=%HU', value)
        self.assertNotIn('spoe', value)

    def test_campaign_mapping_rejects_duplicate_unknown_and_wrong_status(self):
        probes = [{'token': 'q1-allow', 'case': 'allow', 'status': 200,
                   'body_bytes': 0, 'backend': 1}]
        line = 'HTXQ request_id=/htxq/q1-allow host_id=haproxy-htx-3 status=200 termination=----\n'
        line += ('modsecurity-htx: buffered request inspected before header release; '
                 'transaction_id=haproxy-htx-3 body_mode=buffered body_bytes_seen=0 eos_seen=true\n')
        records = runner.campaign_correlate(line, probes)
        self.assertEqual(records[0]['host_id'], 'haproxy-htx-3')
        for invalid in (line * 2, line.replace('200', '500'),
                        line.replace('q1-allow', 'unknown'), line.replace('haproxy-htx-3', 'client-id'),
                        line + 'modsecurity-htx: buffered request inspected before header release; transaction_id=haproxy-htx-99 body_mode=buffered body_bytes_seen=0 eos_seen=true\n'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                runner.campaign_correlate(invalid, probes)

    def test_boolean_or_invented_expectations_cannot_validate_a_receipt(self):
        probe = {'token': 'q1-p1', 'case': 'p1', 'status': 403, 'body_bytes': 0, 'backend': 0}
        text = ('HTXQ request_id=/htxq/q1-p1 host_id=haproxy-htx-1 status=403 termination=----\n'
                'modsecurity-htx: request intervention observed; transaction_id=haproxy-htx-1 phase=1 status=403 rule_id=1100001 action=deny\n')
        runner.campaign_correlate(text, [probe])
        for key, value in (('status', 200), ('body_bytes', False), ('backend', False), ('backend', 1)):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                runner.campaign_correlate(text, [{**probe, key: value}])

    def test_wrong_same_length_backend_payload_never_validates(self):
        import hashlib
        probe = {'token': 'q1-nonempty', 'case': 'nonempty', 'status': 200,
                 'body_bytes': len(b'legitimate-body'), 'backend': 1}
        record = {'token': probe['token'], 'case': 'nonempty', 'body_bytes': probe['body_bytes'],
                  'body_sha256': hashlib.sha256(b'legitimate-body').hexdigest()}
        runner.campaign_backend_check({'requests': [record], 'errors': [], 'active': 0}, [probe])
        with self.assertRaises(ValueError):
            runner.campaign_backend_check({'requests': [{**record, 'body_sha256': '0' * 64}],
                                           'errors': [], 'active': 0}, [probe])

    def test_p2_requires_same_host_id_native_rule_and_eos(self):
        probes = [{'token': 'q1-p2', 'case': 'p2', 'status': 403,
                   'body_bytes': len(runner.P2_BODY), 'backend': 0}]
        text = ('HTXQ request_id=/htxq/q1-p2 host_id=haproxy-htx-7 status=403 termination=----\n'
                'modsecurity-htx: buffered request inspected before header release; transaction_id=haproxy-htx-7 body_mode=buffered body_bytes_seen=26 eos_seen=true\n'
                'modsecurity-htx: request-body intervention observed; transaction_id=haproxy-htx-7 phase=2 status=403 rule_id=1100101 action=deny\n')
        self.assertEqual(len(runner.campaign_correlate(text, probes)), 1)
        for bad in (text.replace('eos_seen=true', 'eos_seen=false'),
                    text.replace('rule_id=1100101', 'rule_id=1100102'),
                    text.replace('transaction_id=haproxy-htx-7', 'transaction_id=haproxy-htx-8'),
                    text + text.splitlines()[-1] + '\n'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                runner.campaign_correlate(bad, probes)

    def test_p4_requires_exact_safe_downgrade(self):
        probes = [{'token': 'q1-p4', 'case': 'p4', 'status': 200,
                   'body_bytes': 0, 'backend': 1}]
        text = ('HTXQ request_id=/htxq/q1-p4 host_id=haproxy-htx-4 status=200 termination=----\n'
                'modsecurity-htx: buffered request inspected before header release; transaction_id=haproxy-htx-4 body_mode=buffered body_bytes_seen=0 eos_seen=true\n'
                'modsecurity-htx: response-body late intervention observed; transaction_id=haproxy-htx-4 phase=4 status=403 rule_id=1100301 requested_action=deny resolved_policy_action=log_only host_action=log_only\n')
        self.assertEqual(len(runner.campaign_correlate(text, probes)), 1)
        for bad in (text.replace('host_action=log_only', 'host_action=deny'),
                    text.replace('rule_id=1100301', 'rule_id=1100302')):
            with self.assertRaises(ValueError):
                runner.campaign_correlate(bad, probes)

    def test_backend_rejects_early_block_dispatch_and_hidden_partial_request(self):
        probes = [{'token': 'q1-p1', 'case': 'p1', 'status': 403, 'body_bytes': 0, 'backend': 0}]
        runner.campaign_backend_check({'requests': [], 'errors': [], 'active': 0}, probes)
        for bad in ({'requests': [{'token': 'q1-p1', 'body_bytes': 0}], 'errors': [], 'active': 0},
                    {'requests': [], 'errors': ['truncated header'], 'active': 0},
                    {'requests': [], 'errors': [], 'active': 1}):
            with self.assertRaises(ValueError):
                runner.campaign_backend_check(bad, probes)

    def test_campaign_does_not_run_through_streaming_or_missing_library_pin(self):
        import argparse
        for mode, pin in (('streaming', 'a' * 64), ('host-buffered', None)):
            with self.assertRaises(ValueError):
                runner.run_campaign(argparse.Namespace(request_body_mode=mode, library_sha256=pin))

    def test_campaign_wire_has_exact_length_and_chunked_eos(self):
        wire = runner.campaign_wire('p2', 'q1-p2')
        self.assertIn(b'Content-Length: 26\r\n', wire)
        self.assertTrue(wire.endswith(runner.P2_BODY))
        chunked = runner.campaign_wire('chunked', 'q1-chunked')
        self.assertNotIn(b'Content-Length:', chunked)
        self.assertIn(b'Transfer-Encoding: chunked\r\n', chunked)
        self.assertTrue(chunked.endswith(b'\r\n0\r\n\r\n'))

    def test_real_upstream_counts_exact_body_without_storing_it(self):
        upstream = runner.CampaignUpstream()
        upstream.start()
        try:
            for index, case in enumerate(('allow', 'nonempty', 'chunked', 'boundary')):
                token = f'q1-test-{index}'
                value = runner.campaign_probe(upstream.server_address[1], case, token)
                self.assertEqual(value['status'], 200)
            probes = [{'token': f'q1-test-{index}', 'case': case, 'status': 200,
                       'body_bytes': len(runner.campaign_body(case)), 'backend': 1}
                      for index, case in enumerate(('allow', 'nonempty', 'chunked', 'boundary'))]
        finally:
            upstream.close()
        observed = upstream.snapshot()
        runner.campaign_backend_check(observed, probes)
        self.assertNotIn('body', observed['requests'][0])

    def test_actual_four_handler_overlap(self):
        from concurrent.futures import ThreadPoolExecutor
        upstream = runner.CampaignUpstream()
        upstream.start()
        try:
            with ThreadPoolExecutor(max_workers=4) as pool:
                values = list(pool.map(lambda n: runner.campaign_probe(
                    upstream.server_address[1], 'parallel', f'q1-parallel-{n}'), range(4)))
            self.assertEqual(len(values), 4)
            self.assertEqual(upstream.snapshot()['peak_active'], 4)
        finally:
            upstream.close()
        self.assertEqual(upstream.snapshot()['errors'], [])

    def test_partial_backend_header_remains_an_error_during_cleanup(self):
        upstream = runner.CampaignUpstream()
        upstream.start()
        with socket.create_connection(upstream.server_address) as connection:
            connection.sendall(b'POST /htxq/q1-hidden HTTP/1.1\r\nContent-Length:')
        upstream.close()
        with self.assertRaises(ValueError):
            runner.campaign_backend_check(upstream.snapshot(), [])

    def test_even_a_queued_empty_backend_accept_is_not_zero_dispatch(self):
        upstream = runner.CampaignUpstream()
        connection = socket.create_connection(upstream.server_address)
        connection.close()
        upstream.close()
        with self.assertRaises(ValueError):
            runner.campaign_backend_check(upstream.snapshot(), [])

    def test_declared_limit_error_requires_exact_fail_closed_native_receipt(self):
        probe = {'token': 'q1-limit', 'case': 'limit', 'status': 503,
                 'body_bytes': 65537, 'backend': 0}
        text = ('HTXQ request_id=/htxq/q1-limit host_id=haproxy-htx-9 status=503 termination=----\n'
                'modsecurity-htx: fail-closed host-buffered request exceeds limit or append failed; transaction_id=haproxy-htx-9 status=503\n')
        runner.campaign_correlate(text, [probe])
        for mutated in (text.replace('status=503', 'status=200'),
                        text.replace('transaction_id=haproxy-htx-9', 'transaction_id=haproxy-htx-8')):
            with self.assertRaises(ValueError):
                runner.campaign_correlate(mutated, [probe])


if __name__ == '__main__':
    unittest.main()
