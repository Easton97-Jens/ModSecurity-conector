"""Reject filesystem and CLI inputs that escape the admitted Apache task."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    source = ROOT / 'ci/runtime/lifecycle/apache-i12' / (name + '.py')
    spec = importlib.util.spec_from_file_location('apache_boundaries_' + name, source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PATHS = load('paths')
CLIENT = load('observed_curl')
PROJECTION = load('public_projection')


class ApacheBoundaryTests(unittest.TestCase):
    def test_input_and_output_reject_traversal_symlinks_and_shared_parents(self):
        with tempfile.TemporaryDirectory(dir=os.environ['CODEX_TEMP_ROOT']) as root:
            base = Path(root)
            physical = base / 'evidence.json'
            physical.write_text('{}')
            link = base / 'alias.json'
            link.symlink_to(physical)
            with patch.dict(os.environ, CODEX_TEMP_ROOT=root):
                self.assertEqual(PATHS.input_path(physical), physical)
                for supplied in (link, Path('/etc/passwd')):
                    with self.subTest(path=supplied), self.assertRaises(ValueError):
                        PATHS.input_path(supplied)
                with self.assertRaises(ValueError):
                    PATHS.new_output(base / '..' / 'escape')
                shared = base / 'shared'
                shared.mkdir(mode=0o777)
                shared.chmod(0o777)
                with self.assertRaises(ValueError):
                    PATHS.new_output(shared / 'result.json')

    def test_storage_rejects_missing_configuration_and_symlink_root(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError):
                PATHS.storage_root()
        with tempfile.TemporaryDirectory(dir=os.environ['CODEX_TEMP_ROOT']) as root:
            link = Path(root) / 'alias'
            link.symlink_to(Path(root))
            with patch.dict(os.environ, CODEX_TEMP_ROOT=str(link)):
                with self.assertRaises(ValueError):
                    PATHS.storage_root()

    def test_client_rejects_curl_config_external_urls_and_file_injection(self):
        bad = [
            ['--config', '/etc/curlrc'], ['file:///etc/passwd'],
            ['http://example.org:8080/'], ['http://user:pass@127.0.0.1:8080/'],
            ['-H', '@secret', 'http://127.0.0.1:8080/'],
            ['-H', 'X-Test: value\r\nInjected: yes', 'http://127.0.0.1:8080/'],
            ['-o', '/etc/passwd', 'http://127.0.0.1:8080/'],
            ['--data-binary', '@/etc/passwd', 'http://127.0.0.1:8080/'],
            ['http://127.0.0.1:8080/', 'http://127.0.0.1:8080/second'],
        ]
        with patch.dict(os.environ, I12_APACHE_PRIVATE_RUNTIME='/task/runtime'):
            for arguments in bad:
                with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                    CLIENT.checked_arguments(arguments)
            valid = ['-sS', '--http1.1', '-X', 'POST', '-H', 'X-Test: one', '-H', 'Content-Type;',
                     '--data-binary', '@/task/body', '-o', '/task/response',
                     'http://127.0.0.1:18140/fixture']
            self.assertEqual(CLIENT.checked_arguments(valid), valid)

    def test_public_projection_preserves_source_and_only_renames_numeric_join(self):
        original = {'positive_control': {'clients': [{'actual_process': {
            'client_token': '123456789', 'actual_waited_exit_code': 0}}]}, 'faults': []}
        raw = json.dumps(original).encode()
        result = PROJECTION.project(raw, 'git:immutable:source.json')
        self.assertEqual(json.loads(raw), original)
        self.assertFalse(result['public_projection']['is_physical_capture'])
        process = result['positive_control']['clients'][0]['actual_process']
        self.assertEqual(process, {'client_process_correlation_id': '123456789',
                                   'actual_waited_exit_code': 0})
        original['positive_control']['clients'][0]['actual_process']['client_token'] = 'unexpected'
        invalid = json.dumps(original).encode()
        with self.assertRaises(ValueError):
            PROJECTION.project(invalid, 'git:immutable:source.json')


if __name__ == '__main__':
    unittest.main()
