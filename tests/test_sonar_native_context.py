"""Native context preparation fails before importing unverified host headers."""

from __future__ import annotations

import hashlib
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sonar_native_context", ROOT / "ci/checks/analysis/prepare-sonar-native-context.py")
assert SPEC is not None and SPEC.loader is not None
NATIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NATIVE)


class SonarNativeContextTests(unittest.TestCase):
    def test_bad_cached_checksum_cannot_reach_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "host.tar.gz"
            archive.write_bytes(b"unapproved replacement")
            item = {"url": "https://example.invalid/host.tar.gz", "sha256": "0" * 64}
            with mock.patch.object(NATIVE.urllib.request, "urlopen") as network:
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    NATIVE.verified_archive(item, root, root)
            network.assert_not_called()
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["host.tar.gz"])

    def test_verified_cached_archive_is_read_without_mutation_or_network(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "host.tar.gz"
            data = b"reviewed archive control"
            archive.write_bytes(data)
            item = {"url": "https://example.invalid/host.tar.gz", "sha256": hashlib.sha256(data).hexdigest()}
            with mock.patch.object(NATIVE.urllib.request, "urlopen") as network:
                selected = NATIVE.verified_archive(item, root / "unused", root)
            self.assertEqual(selected, archive)
            self.assertEqual(archive.read_bytes(), data)
            network.assert_not_called()

    def test_archive_cannot_escape_its_expected_source_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "host.tar.gz"
            with tarfile.open(archive, "w:gz") as output:
                member = tarfile.TarInfo("host-1.2.3/../../outside")
                member.size = 8
                output.addfile(member, io.BytesIO(b"sentinel"))
            sources = root / "sources"
            sources.mkdir()
            with self.assertRaisesRegex(ValueError, "unexpected top-level"):
                NATIVE.unpack(archive, sources, "host-1.2.3")
            self.assertFalse((root / "outside").exists())

    def test_output_roots_reject_source_reuse_and_symlink_redirection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            existing = parent / "existing"
            existing.mkdir()
            (parent / "redirect").symlink_to(existing, target_is_directory=True)
            for candidate in ("/", str(ROOT / "context-output"), str(existing), str(parent / "redirect/child")):
                with self.subTest(candidate=candidate):
                    with self.assertRaises(ValueError):
                        NATIVE.fresh_root(candidate)
            self.assertFalse((ROOT / "context-output").exists())
            self.assertFalse((existing / "child").exists())
            output = NATIVE.fresh_root(str(parent / "new-private-context"))
            self.assertTrue(output.is_dir())
            self.assertEqual(output.stat().st_mode & 0o777, 0o700)

    def test_required_generated_artifacts_must_be_regular_and_nonempty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            header = root / "config.h"
            with self.assertRaisesRegex(ValueError, "missing or invalid"):
                NATIVE.required_files([header])
            header.touch()
            with self.assertRaisesRegex(ValueError, "missing or invalid"):
                NATIVE.required_files([header])
            header.write_bytes(b"fixture feature configuration")
            linked = root / "linked.h"
            linked.symlink_to(header)
            with self.assertRaisesRegex(ValueError, "missing or invalid"):
                NATIVE.required_files([linked])
            self.assertEqual(NATIVE.required_files([header]), {str(header): hashlib.sha256(header.read_bytes()).hexdigest()})

    def test_include_manifest_uses_only_existing_configured_host_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "host"
            (source / "objs").mkdir(parents=True)
            (source / "src/core").mkdir(parents=True)
            (source / "objs/Makefile").write_text(
                "ALL_INCS = -I src/core \\\n\t-I objs \\\n\t-I /unrelated/build-context\n\nCFLAGS = -O\n")
            includes = NATIVE.nginx_includes(source)
            self.assertEqual(includes, [source / "src/core", source / "objs"])
            self.assertEqual(NATIVE.include_value(includes), f"{source}/src/core,{source}/objs")
            with self.assertRaisesRegex(ValueError, "must exist"):
                NATIVE.include_value(includes + [source / "missing"])
            bad = source / "comma,path"
            bad.mkdir()
            with self.assertRaisesRegex(ValueError, "unambiguous"):
                NATIVE.include_value([bad])


if __name__ == "__main__":
    unittest.main()
