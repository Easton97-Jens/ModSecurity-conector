"""Evidence paths cannot escape, probe secrets, follow links or change mid-read."""
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import evidence_io


class EvidenceIOControls(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(
            prefix='envoy-io-controls-', dir=os.environ.get('TMPDIR', tempfile.gettempdir()))
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.roots = (self.root,)
        self.file = self.root / 'receipt.json'
        self.file.write_bytes(b'{"status":"measured"}\n')

    def test_regular_owned_file_and_hash_are_read(self):
        self.assertEqual({'status': 'measured'}, evidence_io.read_json(self.file, self.roots))
        self.assertEqual({'path': str(self.file), 'bytes': 22,
                          'sha256': hashlib.sha256(self.file.read_bytes()).hexdigest()},
                         evidence_io.reference(self.file, self.roots))

    def test_outside_path_is_rejected_before_any_filesystem_probe(self):
        with patch.object(evidence_io.os, 'open') as opened:
            with self.assertRaisesRegex(ValueError, 'outside approved'):
                evidence_io.read_bytes('/etc/shadow', self.roots)
            opened.assert_not_called()

    def test_sibling_with_same_prefix_is_outside(self):
        sibling = str(self.root) + '-other/receipt.json'
        with self.assertRaisesRegex(ValueError, 'outside approved'):
            evidence_io.read_bytes(sibling, self.roots)

    def test_private_configuration_is_rejected_before_filesystem_probe(self):
        with patch.object(evidence_io.os, 'open') as opened:
            with self.assertRaisesRegex(ValueError, 'private configuration'):
                evidence_io.read_bytes(self.root / '.aws' / 'credentials', self.roots)
            opened.assert_not_called()

    def test_traversal_is_rejected_before_any_filesystem_probe(self):
        value = str(self.root / 'nested') + '/../receipt.json'
        with patch.object(evidence_io.os, 'open') as opened:
            with self.assertRaisesRegex(ValueError, 'without traversal'):
                evidence_io.read_bytes(value, self.roots)
            opened.assert_not_called()

    def test_leaf_symlink_is_rejected(self):
        link = self.root / 'link.json'
        link.symlink_to(self.file)
        with self.assertRaises(OSError):
            evidence_io.read_bytes(link, self.roots)

    def test_directory_symlink_is_rejected_even_when_inside_root(self):
        directory = self.root / 'real'
        directory.mkdir()
        (directory / 'data').write_text('measured')
        link = self.root / 'alias'
        link.symlink_to(directory, target_is_directory=True)
        with self.assertRaises(OSError):
            evidence_io.read_bytes(link / 'data', self.roots)

    def test_writable_domain_root_is_rejected(self):
        self.root.chmod(0o777)
        with self.assertRaisesRegex(ValueError, 'not group/other writable'):
            evidence_io.read_bytes(self.file, self.roots)

    def test_writable_file_is_rejected(self):
        self.file.chmod(0o666)
        with self.assertRaisesRegex(ValueError, 'not group/other writable'):
            evidence_io.read_bytes(self.file, self.roots)

    def test_size_limit_is_enforced_before_read(self):
        with self.assertRaisesRegex(ValueError, 'bounded physical regular file'):
            evidence_io.read_bytes(self.file, self.roots, max_bytes=1)

    def test_fifo_is_rejected_without_blocking(self):
        fifo = self.root / 'fifo'
        os.mkfifo(fifo)
        with self.assertRaisesRegex(ValueError, 'bounded physical regular file'):
            evidence_io.read_bytes(fifo, self.roots)

    def test_in_place_change_is_detected_on_same_descriptor(self):
        with self.assertRaisesRegex(ValueError, 'changed while reading'):
            with evidence_io.open_evidence(self.file, self.roots) as (stream, _):
                stream.read()
                self.file.write_bytes(b'changed')

    def test_rename_does_not_redirect_an_open_descriptor(self):
        with self.assertRaisesRegex(ValueError, 'changed while reading'):
            with evidence_io.open_evidence(self.file, self.roots) as (stream, _):
                moved = self.root / 'moved.json'
                self.file.rename(moved)
                self.file.write_bytes(b'other')
                self.assertEqual(b'{"status":"measured"}\n', stream.read())


if __name__ == '__main__':
    unittest.main()
