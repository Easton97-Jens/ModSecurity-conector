"""Negative and positive contracts for the trusted Lighttpd artifact sealer."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SEALER_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "trusted_lighttpd_artifact_sealer.py"
SPEC = importlib.util.spec_from_file_location("trusted_lighttpd_artifact_sealer", SEALER_PATH)
assert SPEC is not None and SPEC.loader is not None
SEALER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SEALER
SPEC.loader.exec_module(SEALER)


class TrustedLighttpdArtifactSealerTest(unittest.TestCase):
    """Exercise the fixed layout and fail-closed source boundary."""

    def candidate(self, root: Path) -> Path:
        candidate = root / "candidate"
        for directory in (candidate / "bin", candidate / "modules", candidate / "lib" / "nested"):
            directory.mkdir(parents=True)
            directory.chmod(0o755)
        for path, content, mode in (
            (candidate / "bin" / "lighttpd", b"lighttpd binary\n", 0o755),
            (candidate / "modules" / "mod_msconnector.so", b"connector module\n", 0o644),
            (candidate / "modules" / "mod_proxy.so", b"proxy module\n", 0o644),
            (candidate / "lib" / "nested" / "libmodsecurity.so", b"library\n", 0o644),
        ):
            path.write_bytes(content)
            path.chmod(mode)
        candidate.chmod(0o755)
        return candidate

    def seal(self, root: Path, candidate: Path | None = None) -> tuple[Path, Path]:
        source = candidate or self.candidate(root)
        output_parent = root / "sealed-parent"
        output_parent.mkdir(mode=0o700)
        output_parent.chmod(0o700)
        output = output_parent / "sealed"
        manifest = SEALER.seal_candidate(
            source,
            output,
            provenance={"parent_sha": "a" * 64, "framework_sha": "b" * 64, "mrts_sha": "c" * 64},
        )
        return output, manifest

    def test_valid_candidate_produces_root_owned_immutable_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            output, manifest_path = self.seal(Path(temporary))
            self.assertEqual(manifest_path.name, SEALER.MANIFEST_NAME)
            self.assertEqual(manifest_path.stat().st_uid, 0)
            self.assertEqual(stat.S_IMODE(manifest_path.stat().st_mode), 0o400)
            self.assertEqual(output.stat().st_uid, 0)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o755)
            self.assertEqual(stat.S_IMODE((output / "bin/lighttpd").stat().st_mode), 0o555)
            self.assertEqual(stat.S_IMODE((output / "modules/mod_proxy.so").stat().st_mode), 0o444)
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_layout"], "lighttpd-fixed-v1")
            self.assertEqual(
                [entry["path"] for entry in payload["artifacts"]],
                ["bin/lighttpd", "modules/mod_msconnector.so", "modules/mod_proxy.so", "lib/nested/libmodsecurity.so"],
            )

            def reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
                result: dict[str, object] = {}
                for key, value in pairs:
                    if key in result:
                        raise AssertionError(f"duplicate manifest key: {key}")
                    result[key] = value
                return result

            json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_pairs)

    def test_candidate_manifest_is_not_an_authority_and_unlisted_files_fail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            (candidate / "candidate-manifest.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(SEALER.SealerError, "unlisted top-level"):
                self.seal(root, candidate)

        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            (candidate / "modules" / "unlisted.so").write_bytes(b"unexpected")
            with self.assertRaisesRegex(SEALER.SealerError, "unlisted entry"):
                self.seal(root, candidate)

    def test_rejects_symlinks_special_files_hardlinks_and_writable_files(self) -> None:
        cases: list[tuple[str, object]] = []
        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            (candidate / "modules/mod_proxy.so").unlink()
            (candidate / "modules/mod_proxy.so").symlink_to(candidate / "modules/mod_msconnector.so")
            cases.append(("symbolic links", candidate))
            for message in (
                "special file",
                "hard-linked",
                "group/world writable",
            ):
                fresh = root / message.replace(" ", "-")
                fresh.mkdir(parents=True)
                item = self.candidate(fresh)
                if message == "special file":
                    os.mkfifo(item / "lib/fifo")
                elif message == "hard-linked":
                    os.link(item / "modules/mod_msconnector.so", item / "lib/hardlink")
                else:
                    (item / "modules/mod_msconnector.so").chmod(0o666)
                cases.append((message, item))
            for expected, item in cases:
                parent = item.parent / "out"
                parent.mkdir(mode=0o700)
                with self.assertRaises(SEALER.SealerError, msg=expected):
                    SEALER.seal_candidate(item, parent / "sealed")

    def test_descriptor_walk_rejects_replaced_intermediate_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            nested = candidate / "lib" / "nested"
            retained_name = candidate / "lib" / "nested-real"
            nested.rename(retained_name)
            nested.symlink_to(retained_name, target_is_directory=True)
            descriptor = os.open(candidate, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                with self.assertRaisesRegex(SEALER.SealerError, "cannot open library"):
                    SEALER._source_file(descriptor, "lib/nested/libmodsecurity.so", "library")
            finally:
                os.close(descriptor)

    def test_sealing_remains_bound_when_intermediate_directory_is_replaced(self) -> None:
        """A replacement after enumeration cannot redirect retained source FDs."""

        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            (candidate / "lib/nested/libmodsecurity.so").write_bytes(b"retained library\n")
            output_parent = root / "sealed-parent"
            output_parent.mkdir(mode=0o700)
            output = output_parent / "sealed"
            original_candidate_files = SEALER._candidate_files

            def replace_after_enumeration(_descriptor: int) -> list[object]:
                entries = original_candidate_files(_descriptor)
                nested = candidate / "lib" / "nested"
                retained = candidate / "lib" / "nested-real"
                nested.rename(retained)
                nested.symlink_to(retained, target_is_directory=True)
                return entries

            with mock.patch.object(SEALER, "_candidate_files", side_effect=replace_after_enumeration):
                SEALER.seal_candidate(candidate, output)
            self.assertEqual((output / "lib/nested/libmodsecurity.so").read_bytes(), b"retained library\n")

    def test_sealing_remains_bound_to_opened_candidate_root_after_root_replacement(self) -> None:
        """A replacement of the pathname cannot mix a second candidate into a seal."""

        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            (candidate / "bin" / "lighttpd").write_bytes(b"retained candidate binary\n")
            replacement_parent = root / "replacement-source"
            replacement_parent.mkdir()
            replacement = self.candidate(replacement_parent)
            (replacement / "bin" / "lighttpd").write_bytes(b"replacement candidate binary\n")
            output_parent = root / "sealed-parent"
            output = output_parent / "sealed"
            original_candidate_files = SEALER._candidate_files

            def replace_root_after_open(descriptor: int) -> list[object]:
                entries = original_candidate_files(descriptor)
                candidate.rename(root / "retained-candidate")
                replacement.rename(candidate)
                return entries

            with mock.patch.object(SEALER, "_candidate_files", side_effect=replace_root_after_open):
                self.seal(root, candidate)
            self.assertEqual((output / "bin/lighttpd").read_bytes(), b"retained candidate binary\n")

    def test_sealing_remains_bound_to_opened_output_parent_after_parent_replacement(self) -> None:
        """The final rename stays in the retained root-owned output parent."""

        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            output_parent = root / "sealed-parent"
            output_parent.mkdir(mode=0o700)
            output_parent.chmod(0o700)
            retained_parent = root / "retained-sealed-parent"
            redirected_parent = root / "redirected-sealed-parent"
            redirected_parent.mkdir(mode=0o700)
            output = output_parent / "sealed"
            original_new_root = SEALER._new_sealed_directory

            def replace_parent_after_open(descriptor: int) -> tuple[str, int]:
                name, sealed_descriptor = original_new_root(descriptor)
                output_parent.rename(retained_parent)
                output_parent.symlink_to(redirected_parent, target_is_directory=True)
                return name, sealed_descriptor

            with mock.patch.object(SEALER, "_new_sealed_directory", side_effect=replace_parent_after_open):
                SEALER.seal_candidate(candidate, output)

            self.assertEqual((retained_parent / "sealed/bin/lighttpd").read_bytes(), b"lighttpd binary\n")
            self.assertFalse((redirected_parent / "sealed").exists())

    def test_rejects_traversal_and_empty_or_oversize_library(self) -> None:
        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(SEALER.SealerError, "absolute path"):
                SEALER.seal_candidate(Path("candidate"), root / "sealed")

            candidate = self.candidate(root)
            (candidate / "lib/nested/libmodsecurity.so").unlink()
            with self.assertRaisesRegex(SEALER.SealerError, "at least one file"):
                self.seal(root, candidate)

            candidate = self.candidate(root / "oversize")
            original_limit = SEALER.MAX_FILE_BYTES
            try:
                SEALER.MAX_FILE_BYTES = 4
                with self.assertRaisesRegex(SEALER.SealerError, "size limit"):
                    self.seal(root / "oversize", candidate)
            finally:
                SEALER.MAX_FILE_BYTES = original_limit

    def test_rejects_invalid_provenance_and_existing_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="trusted-lighttpd-sealer-") as temporary:
            root = Path(temporary)
            candidate = self.candidate(root)
            output_parent = root / "sealed-parent"
            output_parent.mkdir(mode=0o700)
            with self.assertRaisesRegex(SEALER.SealerError, "SHA-256"):
                SEALER.seal_candidate(candidate, output_parent / "one", provenance={"mrts_sha": "not-a-sha"})
            existing = output_parent / "existing"
            existing.mkdir()
            with self.assertRaisesRegex(SEALER.SealerError, "fresh"):
                SEALER.seal_candidate(candidate, existing)


if __name__ == "__main__":
    unittest.main()
