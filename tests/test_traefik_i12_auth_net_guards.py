"""Exercise the physical fixture's fixed HTTP, path and child-command boundaries."""
import http.server
import importlib.util
import io
from email.message import Message
import os
from pathlib import Path
import socket
import threading
from types import SimpleNamespace
import unittest
from unittest import mock


HARNESS = Path(__file__).resolve().parents[1] / 'connectors/traefik/harness/i12_auth'


def load(name):
    spec = importlib.util.spec_from_file_location(name, HARNESS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NetBoundaries(unittest.TestCase):
    def setUp(self):
        self.net = load('acceptance_net')
        self.signal = load('acceptance_signal')
        self.root = Path('/task/cases/ac-' + 'a' * 20)

    def test_authorization_sample_labels_cannot_choose_paths(self):
        self.assertEqual(self.net.authorization_sample_path(self.root, 'readiness-9'),
                         self.root / 'auth-readiness-9.sample.raw')
        for label in ('../escape', '/other', 'readiness-10', 'sequence-3'):
            with self.assertRaises(ValueError):
                self.net.authorization_sample_path(self.root, label)

    def test_relay_refuses_api_paths_outside_fixed_authorization_endpoint(self):
        relay = object.__new__(self.net.Relay)
        relay.path = '/other-native-api'
        relay.send_error = mock.Mock()
        relay.forward()
        relay.send_error.assert_called_once_with(404)

    def test_relay_uses_fixed_native_api_and_preserves_forwarded_original_uri(self):
        relay = object.__new__(self.net.Relay)
        relay.path = '/authorize'
        relay.command = 'POST'
        relay.root = self.root
        relay.engine_port = 18081
        relay.spec = {'probe_id': 'sample', 'fixture': {'request': {}}}
        relay.headers = Message()
        relay.headers['X-Forwarded-Uri'] = '/original?inspection=1'
        relay.rfile = io.BytesIO(b'')
        relay.relay_response = mock.Mock()
        upstream = mock.Mock()
        upstream.getresponse.return_value.status = 403
        upstream.getresponse.return_value.read.return_value = b'deny'
        with mock.patch.object(self.net, 'loopback_connection', return_value=upstream), \
                mock.patch.object(self.net, 'authorization_sample_path'), \
                mock.patch.object(self.net, 'dump'):
            relay.forward()
        upstream.putrequest.assert_called_once_with('POST', '/authorize', skip_host=True, skip_accept_encoding=True)
        upstream.putheader.assert_any_call('X-Forwarded-Uri', '/original?inspection=1')
        self.assertEqual(relay.relay_response.call_args.args[1], b'deny')

    def test_socket_pair_requires_fixed_paths_and_private_owned_directory(self):
        observer = self.root / 'sockets/observer.sock'
        native = self.root / 'sockets/companion.sock'
        observer_argument = str(observer)
        native_argument = str(native)
        with mock.patch.object(Path, 'resolve', autospec=True, side_effect=lambda path, **_: path), \
                mock.patch.object(Path, 'is_dir', return_value=True), \
                mock.patch.object(Path, 'is_symlink', return_value=False), \
                mock.patch.object(Path, 'stat', return_value=SimpleNamespace(st_uid=os.geteuid(), st_mode=0o40700)):
            self.assertEqual(self.net.companion_paths(self.root, observer_argument, native_argument),
                             (observer, native))
            with self.assertRaises(ValueError):
                self.net.companion_paths(self.root, '/other/observer.sock', native_argument)
            with mock.patch.object(Path, 'is_symlink', return_value=True):
                with self.assertRaises(ValueError):
                    self.net.companion_paths(self.root, observer_argument, native_argument)
            with mock.patch.object(Path, 'stat', return_value=SimpleNamespace(st_uid=os.geteuid(), st_mode=0o40777)):
                with self.assertRaises(ValueError):
                    self.net.companion_paths(self.root, observer_argument, native_argument)

    def test_signal_child_command_is_built_from_validated_case(self):
        with mock.patch.object(self.signal, 'validate_case', return_value={}) as validate:
            argv = self.signal.client_arguments(self.root, 18081)
        validate.assert_called_once_with(self.root, 18081)
        self.assertEqual(argv, ['/usr/local/bin/python3', '-P', '/mnt/fixtures/acceptance_net.py',
                               'client', '--spec', str(self.root / 'case.json'),
                               '--root', str(self.root), '--port', '18081'])
        with mock.patch.object(self.signal, 'validate_case', side_effect=ValueError('unadmitted')), \
                mock.patch.object(self.signal.os, 'fork') as fork:
            with self.assertRaises(ValueError):
                self.signal.start_client(self.root, 18081)
        fork.assert_not_called()

    def test_loopback_server_keeps_plain_http_wire_semantics(self):
        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'

            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Length', '3')
                self.end_headers()
                self.wfile.write(b'ok\n')

            def log_message(self, *_):
                return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        server = self.net.LoopbackEvidenceServer(port, Handler)
        thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.01})
        thread.start()
        try:
            self.assertEqual(server.server_address[0], '127.0.0.1')
            with socket.create_connection(('127.0.0.1', port), timeout=2) as connection:
                connection.sendall(b'GET /physical-http HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n')
                response = bytearray()
                while True:
                    chunk = connection.recv(4096)
                    if not chunk:
                        break
                    response.extend(chunk)
            self.assertTrue(bytes(response).startswith(b'HTTP/1.1 200 OK\r\n'))
            self.assertTrue(bytes(response).endswith(b'\r\n\r\nok\n'))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)
        self.assertFalse(thread.is_alive(), 'fixture accept loop must terminate')
        self.assertEqual(server.fileno(), -1, 'fixture listener must be closed')


if __name__ == '__main__':
    unittest.main()
